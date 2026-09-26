import traceback
from datasets import load_dataset, Audio
import sys

def main():
    try:
        ds = load_dataset(
            "ai4bharat/IndicVoices",
            "santali",
            split="train",
            streaming=True
        )
        ds = ds.cast_column("audio", Audio(decode=False))
        ds_iter = iter(ds)
        sample = next(ds_iter)
        print("SUCCESSFULLY LOADED SAMPLE")
        print(f"Sample keys: {list(sample.keys())}")
        print(f"Audio details: {sample['audio']}")
        print(f"Text: {sample['text']}")
    except Exception as e:
        with open("error_trace3.txt", "w") as f:
            f.write(f"Exception Type: {type(e).__name__}\n")
            f.write(f"Exception Message: {e}\n")
            traceback.print_exc(file=f)
        print("FAILED, check error_trace3.txt")

if __name__ == "__main__":
    main()
