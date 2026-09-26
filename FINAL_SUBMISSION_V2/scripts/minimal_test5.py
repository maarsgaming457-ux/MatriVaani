import sys
import traceback
from datasets import load_dataset, Audio

def test_split(split_name, num_samples=5):
    print(f"Loading {split_name} split...")
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split=split_name, streaming=True)
    ds = ds.cast_column("audio_filepath", Audio(decode=False))
    
    ds_iter = iter(ds)
    samples = []
    
    for i in range(num_samples):
        print(f"Fetching sample {i+1}...")
        sample = next(ds_iter)
        
        # Verify fields
        assert "audio_filepath" in sample, "Missing audio_filepath"
        assert sample["audio_filepath"] is not None, "Audio is None"
        audio = sample["audio_filepath"]
        assert "bytes" in audio or "path" in audio, "Audio missing bytes/path"
        
        assert sample["duration"] > 0, "Duration <= 0"
        assert sample["text"], "Text is empty"
        assert sample["lang"] == "sat", "Lang is not sat"
        
        samples.append({
            "id": sample.get("speaker_id", "unknown"),
            "duration": sample["duration"],
            "text": sample["text"],
            "lang": sample["lang"],
            "audio": audio
        })
        print(f"  Success: len(text)={len(sample['text'])}, duration={sample['duration']}")
    
    return samples

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    try:
        print("Testing TRAIN split...")
        train_samples = test_split("train", 5)
        
        print("\nTesting VALIDATION split...")
        valid_samples = test_split("valid", 5)
        
        print("\nALL TESTS PASSED")
    except Exception as e:
        print(f"\nFAILED with Exception: {type(e).__name__}")
        print(f"Error Message: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
