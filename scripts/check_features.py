from datasets import load_dataset, Audio

def main():
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split="train", streaming=True)
    print("Features:", ds.features)

if __name__ == "__main__":
    main()
