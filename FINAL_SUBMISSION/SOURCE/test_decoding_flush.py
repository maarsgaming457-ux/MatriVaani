import sys
import time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

def log(msg):
    print(msg, flush=True)

def main():
    log("Loading model...")
    model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
    device = "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
    model.eval()
    ip = IndicProcessor(inference=True)
    
    sentences = [
        "???? ????? ??? ??????? ?? ??????"
    ]
    
    src = "hin_Deva"
    tgt = "sat_Olck"
    
    batch = ip.preprocess_batch(sentences, src_lang=src, tgt_lang=tgt)
    inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
    
    log("\n--- Testing Decoding Strategies ---")
    log("1. Original...")
    t0 = time.time()
    with torch.no_grad():
        out1 = model.generate(**inputs, max_length=256, num_beams=5)
    t1 = time.time()
    res1 = ip.postprocess_batch(tokenizer.batch_decode(out1, skip_special_tokens=True), lang=tgt)
    log(f"Original: {res1[0]} (took {t1-t0:.2f}s)")
    
    log("2. Safeguards...")
    t0 = time.time()
    with torch.no_grad():
        out2 = model.generate(**inputs, max_length=256, num_beams=5, repetition_penalty=1.2, no_repeat_ngram_size=3)
    t1 = time.time()
    res2 = ip.postprocess_batch(tokenizer.batch_decode(out2, skip_special_tokens=True), lang=tgt)
    log(f"Safeguards: {res2[0]} (took {t1-t0:.2f}s)")

if __name__ == '__main__':
    main()
