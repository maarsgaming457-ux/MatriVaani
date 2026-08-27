import traceback
from datasets import load_dataset, Audio

def main():
    try:
        print("Starting dataset load...")
        ds = load_dataset(
            "ai4bharat/IndicVoices",
            "santali",
            split="train",
            streaming=True
        )
        print("Casting audio_filepath...")
        ds = ds.cast_column("audio_filepath", Audio(decode=False))
        print("Getting iterator...")
        ds_iter = iter(ds)
        print("Fetching first element...")
        sample = next(ds_iter)
        print("Successfully fetched first element!")
        print(f"Sample keys: {list(sample.keys())}")
        print(f"Text: {sample['text']}")
        print(f"Audio path/bytes: {sample['audio_filepath']}")
    except Exception as e:
        print(f"FAILED with Exception: {type(e).__name__}")
        print(f"Error Message: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
