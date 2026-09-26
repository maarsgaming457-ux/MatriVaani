import os, torch, unicodedata
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
model_path = r"C:\study_files\sih project\backend\best_model_main2"
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True)
model.to(device)
model.eval()
def normalize_hindi(text: str) -> str:
    norm = unicodedata.normalize("NFKC", text.strip())
    terminal_punctuations = ("।", "?", "!", ".")
    if not norm.endswith(terminal_punctuations): norm += "।"
    return norm
def run_test(text: str):
    norm_text = normalize_hindi(text)
    input_str = f"hin_Deva unr_Deva {norm_text}"
    inputs = tokenizer(input_str, return_tensors="pt").to(device)
    with torch.inference_mode():
        outputs = model.generate(**inputs, num_beams=5, repetition_penalty=1.2, length_penalty=0.7, max_new_tokens=256, decoder_start_token_id=2, pad_token_id=1, eos_token_id=2, use_cache=False, do_sample=False)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True).replace("unr_Deva", "").replace("hin_Deva", "").replace(" ", " ").strip()
    return decoded

import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
print("1: " + run_test('क्या कर रहे हो'))
print("2: " + run_test('क्या कर रहे हो।'))
print("3: " + run_test('क्या कर रहे हो?'))
