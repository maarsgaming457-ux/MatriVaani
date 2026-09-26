import os
import torch
import unicodedata
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_path = r"C:\study_files\sih project\backend\best_model_main2"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True)
model.to(device)
model.eval()

def normalize_hindi(text: str) -> str:
    if not text: return ""
    norm = unicodedata.normalize("NFKC", text.strip())
    terminal_punctuations = ("।", "?", "!", ".")
    if not norm.endswith(terminal_punctuations):
        norm += "।"
    return norm

def run_test(text: str, apply_norm: bool = True):
    norm_text = normalize_hindi(text) if apply_norm else text
    input_str = f"hin_Deva unr_Deva {norm_text}"
    inputs = tokenizer(input_str, return_tensors="pt").to(device)
    
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            num_beams=5,
            repetition_penalty=1.2,
            length_penalty=0.7,
            max_new_tokens=256,
            decoder_start_token_id=2,
            pad_token_id=1,
            eos_token_id=2,
            use_cache=False,
            do_sample=False,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    decoded = decoded.replace("unr_Deva", "").replace("hin_Deva", "").replace(" ", " ").strip()
    return norm_text, input_str, decoded

tests = [
    ("मेरा नाम सुमित है", True),
    ("क्या कर रहे हो?", False),
    ("क्या कर रहे हो?", True),
]

for t, do_norm in tests:
    norm_txt, inp_str, out = run_test(t, do_norm)
    print(f"Input: {t}")
    print(f"Normalized: {norm_txt}")
    print(f"Input string: {inp_str}")
    print(f"Output: {out}\n")
