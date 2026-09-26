import os
import time
import torch
import psutil
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

def get_ram_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def print_memory(label):
    print(f"[{label}] RAM Usage: {get_ram_usage():.2f} MB")

def main():
    print("================================================================================")
    print("MATRI VAANI - STANDALONE INDICTRANS2 TEST")
    print("================================================================================")
    print(f"PyTorch: {torch.__version__}")
    try:
        import transformers
        print(f"Transformers: {transformers.__version__}")
    except:
        pass
        
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    
    model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
    print_memory("Before Model Load")
    
    t_start_load = time.time()
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
    model.eval()
    ip = IndicProcessor(inference=True)
    t_end_load = time.time()
    
    print(f"Model loaded in {t_end_load - t_start_load:.2f} seconds")
    print_memory("After Model Load")
    print(f"Model Architecture: {model.__class__.__name__}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters())}")
    
    # Check language codes
    print("\n--- SUPPORTED LANGUAGES ---")
    print(f"Hindi code 'hin_Deva' in tokenizer: {'hin_Deva' in tokenizer.get_vocab()}")
    print(f"Santali code 'sat_Olck' in tokenizer: {'sat_Olck' in tokenizer.get_vocab()}")
    print(f"Ho code (hoc_Wara) in tokenizer: {'hoc_Wara' in tokenizer.get_vocab()}")
    
    hi_sentences = [
        "नमस्ते बच्चों।",
        "आज हम गिनती सीखेंगे।",
        "अपने सामने रखी वस्तुओं को गिनिए।"
    ]
    
    # Do not fabricate Santali text if not available, but user says "if reliable Santali input is available". 
    # I will just do Hindi -> Santali as requested, and skip Santali -> Hindi unless I have good text. 
    # The user says "If reliable Santali input cannot be obtained, test Hindi → Santali and report that Santali → Hindi could not be fairly evaluated."
    
    def run_translations(sentences, src, tgt, label):
        print(f"\n--- {label} ---")
        total_inf_time = 0
        total_time = 0
        
        for i, text in enumerate(sentences):
            t0 = time.time()
            batch = ip.preprocess_batch([text], src_lang=src, tgt_lang=tgt)
            inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
            t_prep = time.time()
            
            with torch.no_grad():
                outputs = model.generate(**inputs, max_length=256, num_beams=5)
            t_inf = time.time()
            
            decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            postprocessed = ip.postprocess_batch(decoded, lang=tgt)
            t_post = time.time()
            
            inf_time = t_inf - t_prep
            full_time = t_post - t0
            
            total_inf_time += inf_time
            total_time += full_time
            
            print(f"Test {i+1}:")
            print(f"  Source: {text}")
            print(f"  Translation: {postprocessed[0]}")
            print(f"  Pre-proc: {t_prep - t0:.2f}s | Inference: {inf_time:.2f}s | Post-proc: {t_post - t_inf:.2f}s | Total: {full_time:.2f}s")
            
        print(f"Average {label} Inference: {total_inf_time/len(sentences):.2f}s")
        print(f"Average {label} Total: {total_time/len(sentences):.2f}s")
        
    run_translations(hi_sentences, "hin_Deva", "sat_Olck", "Hindi -> Santali")

if __name__ == '__main__':
    main()
