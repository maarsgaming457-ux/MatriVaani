import os
import numpy as np
import soundfile as sf
import pandas as pd
from pathlib import Path

def generate_synthetic_dataset():
    out_dir = Path("datasets/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    audio_dir = out_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    # Some dummy Ol Chiki transcriptions
    samples = [
        "ᱚᱛᱜᱝᱞᱟ",
        "ᱠᱡᱢᱣᱤᱥ",
        "ᱦᱧᱨᱩᱪᱫ",
        "ᱬᱭᱮᱯᱰᱱ",
        "ᱲᱳᱴᱵᱶᱷ"
    ]

    metadata = []
    
    for i, transcript in enumerate(samples):
        # Generate 2 seconds of random noise or simple sine wave to simulate audio
        sample_rate = 16000
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        # Sine wave with changing frequency + noise
        audio = 0.5 * np.sin(2 * np.pi * (440 + i * 50) * t) + 0.05 * np.random.randn(len(t))
        
        filename = f"synthetic_santhali_{i:03d}.wav"
        filepath = audio_dir / filename
        
        sf.write(str(filepath), audio, sample_rate)
        
        metadata.append({
            "file_name": f"audio/{filename}",
            "transcription": transcript
        })
        print(f"Generated {filepath} successfully.")

    # Write metadata.csv compatible with HuggingFace datasets
    df = pd.DataFrame(metadata)
    csv_path = out_dir / "metadata.csv"
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"Wrote metadata to {csv_path}")

if __name__ == "__main__":
    generate_synthetic_dataset()
