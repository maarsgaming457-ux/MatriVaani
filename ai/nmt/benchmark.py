import time
import os
import psutil

def benchmark_nmt_model(model_name: str, test_text: str = "नमस्ते, आप कैसे हैं?"):
    """
    Benchmarks the NMT model's loading time, inference latency, and memory footprint.
    """
    from .model_loader import load_nmt_model
    
    process = psutil.Process(os.getpid())
    base_ram = process.memory_info().rss / (1024 * 1024)
    
    print(f"--- Benchmarking NMT: {model_name} ---")
    print(f"Base RAM: {base_ram:.2f} MB")
    
    t0 = time.time()
    model = load_nmt_model(model_name)
    load_time = time.time() - t0
    
    if not model:
        print("Benchmark Failed: Model failed to load.")
        return
        
    post_load_ram = process.memory_info().rss / (1024 * 1024)
    print(f"Load Time: {load_time:.2f} s")
    print(f"Post-Load RAM: {post_load_ram:.2f} MB")
    
    t1 = time.time()
    output = model.translate(test_text)
    inference_time = time.time() - t1
    
    post_inf_ram = process.memory_info().rss / (1024 * 1024)
    
    print(f"Test Input: {test_text}")
    print(f"Output: {output}")
    print(f"Inference Latency: {inference_time:.3f} s")
    print(f"Post-Inference RAM: {post_inf_ram:.2f} MB")
