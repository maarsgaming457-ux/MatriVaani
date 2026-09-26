import traceback
from datasets import load_dataset
import sys

def main():
    try:
        ds = load_dataset(
            "ai4bharat/IndicVoices",
            "santali",
            split="train",
            streaming=True
        )
        ds_iter = iter(ds)
        sample = next(ds_iter)
    except Exception as e:
        with open("error_trace.txt", "w") as f:
            f.write(f"Exception Type: {type(e).__name__}\n")
            f.write(f"Exception Message: {e}\n")
            traceback.print_exc(file=f)

if __name__ == "__main__":
    main()
