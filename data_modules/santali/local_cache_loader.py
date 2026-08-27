import os
import json
import torch
import torchaudio
from torch.utils.data import Dataset

class LocalSantaliDataset(Dataset):
    """
    Lazy loads audio from the local cache to avoid HuggingFace streaming latency.
    """
    def __init__(self, meta_file):
        self.meta_file = meta_file
        self.data = []
        
        with open(meta_file, "r", encoding="utf-8") as f:
            for line in f:
                self.data.append(json.loads(line))
                
    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, idx):
        item = self.data[idx]
        audio_path = item["audio_path"]
        
        # Lazy load audio using soundfile to avoid torchcodec issues
        import soundfile as sf
        waveform_np, sample_rate = sf.read(audio_path)
        waveform = torch.from_numpy(waveform_np)
        
        # Ensure 2D for processing
        if len(waveform.shape) == 1:
            waveform = waveform.unsqueeze(0)
            
        # Ensure mono
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)
            
        # Ensure 16kHz
        if sample_rate != 16000:
            import librosa
            waveform_np = librosa.resample(waveform.squeeze().numpy(), orig_sr=sample_rate, target_sr=16000)
            waveform = torch.from_numpy(waveform_np).unsqueeze(0)
            sample_rate = 16000
            
        return {
            "sample_id": item["sample_id"],
            "waveform": waveform.squeeze().numpy(),  # 1D array
            "sample_rate": sample_rate,
            "normalized_text": item["transcript"],
            "duration": item["duration"]
        }
