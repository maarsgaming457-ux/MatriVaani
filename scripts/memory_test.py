import os
import psutil
from datasets import load_dataset, Audio

def get_ram():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def main():
    baseline_ram = get_ram()
    
    ds = load_dataset("ai4bharat/IndicVoices", "santali", split="train", streaming=True)
    ds = ds.cast_column("audio_filepath", Audio(decode=False))
    ds_iter = iter(ds)
    loader_ram = get_ram()
    
    sample = next(ds_iter)
    first_sample_ram = get_ram()
    
    for _ in range(4):
        sample = next(ds_iter)
        
    five_sample_ram = get_ram()
    
    print(f"baseline_ram_mb: {baseline_ram:.2f}")
    print(f"loader_ram_mb: {loader_ram:.2f}")
    print(f"first_sample_ram: {first_sample_ram:.2f}")
    print(f"five_sample_ram: {five_sample_ram:.2f}")
    print(f"peak_ram_mb: {max(baseline_ram, loader_ram, first_sample_ram, five_sample_ram):.2f}")

if __name__ == "__main__":
    main()
