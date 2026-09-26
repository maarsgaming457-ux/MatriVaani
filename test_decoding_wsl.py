import os
import time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

def main():
    model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
    device = "cpu"
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
    model.eval()
    ip = IndicProcessor(inference=True)
    
    sentences = [
        "?????? ???????",
        "?? ?? ????? ????????",
        "???? ????? ??? ??????? ?? ??????"
    ]
    
    src = "hin_Deva"
    tgt = "sat_Olck"
    
    print("\n--- Testing Decoding Strategies ---")
    batch = ip.preprocess_batch(sentences, src_lang=src, tgt_lang=tgt)
    inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
    
    t0 = time.time()
    with torch.no_grad():
        out1 = model.generate(**inputs, max_length=256, num_beams=5)
    t1 = time.time()
    res1 = ip.postprocess_batch(tokenizer.batch_decode(out1, skip_special_tokens=True), lang=tgt)
    
    print(f"\nOriginal Decoding ({(t1-t0):.2f}s):")
    for s, r in zip(sentences, res1): print(f"{s} -> {r}")
    
    t0 = time.time()
    with torch.no_grad():
        out2 = model.generate(**inputs, max_length=256, num_beams=5, repetition_penalty=1.2, no_repeat_ngram_size=3)
    t1 = time.time()
    res2 = ip.postprocess_batch(tokenizer.batch_decode(out2, skip_special_tokens=True), lang=tgt)
    
    print(f"\nSafeguards Decoding ({(t1-t0):.2f}s):")
    for s, r in zip(sentences, res2): print(f"{s} -> {r}")

if __name__ == '__main__':
    main()
