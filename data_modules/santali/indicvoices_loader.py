import os
import sys

# Prevent shadowing the pip datasets module
sys.path = [p for p in sys.path if p != '' and p != os.getcwd()]

import datasets
import logging
from typing import Iterator, Dict, Any
from data_modules.santali.text_normalizer import SantaliNormalizer
from data_modules.santali.audio import decode_audio_bytes

logger = logging.getLogger(__name__)

class IndicVoicesLoader:
    def __init__(self, dataset_name="ai4bharat/IndicVoices", config="santali", cache_dir="datasets/cache"):
        self.dataset_name = dataset_name
        self.config = config
        self.cache_dir = cache_dir
        
        # Check authentication token
        self.token = os.environ.get("HF_TOKEN", True)
        self.normalizer = SantaliNormalizer()
        
    def stream_train(self) -> Iterator[Dict[str, Any]]:
        return self._stream_split("train")
        
    def stream_valid(self) -> Iterator[Dict[str, Any]]:
        return self._stream_split("valid")
        
    def _stream_split(self, split: str) -> Iterator[Dict[str, Any]]:
        ds = datasets.load_dataset(
            self.dataset_name, 
            self.config, 
            split=split, 
            streaming=True, 
            token=self.token,
            cache_dir=self.cache_dir,
            trust_remote_code=True
        )
        ds = ds.cast_column("audio_filepath", datasets.Audio(decode=False))
        
        for item in ds:
            processed_item = self._process_record(item)
            if processed_item is not None:
                yield processed_item
                
    def _process_record(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processes a raw dictionary from Hugging Face, validating and decoding it.
        Returns None if the record fails validation (logs rejection reason).
        """
        # Validate text
        raw_text = item.get("text", "")
        if not raw_text or not raw_text.strip():
            logger.warning("Rejected: Empty text")
            return None
            
        lang = item.get("lang", "")
        if lang != "sat":
            logger.warning(f"Rejected: Language mismatch ({lang} != sat)")
            return None
            
        script = self.normalizer.identify_script(raw_text)
        if script not in ["ol_chiki", "mixed", "latin", "devanagari"]:
            logger.warning(f"Rejected: Invalid script ({script})")
            return None
            
        normalized = self.normalizer.normalize(raw_text)
        
        # Validate audio
        audio_data = item.get("audio_filepath", {})
        if not audio_data:
            logger.warning("Rejected: Missing audio_filepath field")
            return None
            
        audio_bytes = audio_data.get("bytes", None)
        if not audio_bytes:
            logger.warning("Rejected: Missing audio bytes")
            return None
            
        try:
            waveform, sr = decode_audio_bytes(audio_bytes, target_sr=16000)
        except Exception as e:
            logger.warning(f"Rejected: Audio decode error - {e}")
            return None
            
        metadata_duration = item.get("duration", 0.0)
        decoded_duration = len(waveform) / sr
        
        # Simple duration sanity check (allow small floating point diffs)
        if metadata_duration > 0 and abs(metadata_duration - decoded_duration) > 0.5:
            logger.warning(f"Rejected: Duration mismatch ({metadata_duration} vs {decoded_duration})")
            return None
            
        # Compile validated output payload
        return {
            "waveform": waveform,
            "sample_rate": sr,
            "original_text": normalized["original_text"],
            "normalized_text": normalized["normalized_text"],
            "duration": decoded_duration,
            "language": lang,
            "script_identified": script,
            "decode_status": "SUCCESS"
        }
