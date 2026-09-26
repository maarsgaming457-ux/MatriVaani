import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_path = r"C:\study_files\sih project\backend\best_model_main2"

print("Loading model and tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval()
print(f"Model loaded on {device}.")

text = "मेरा नाम सुमित है।"
input_str = f"hin_Deva unr_Deva {text}"
print(f"Input string: {input_str}")

inputs = tokenizer(input_str, return_tensors="pt").to(device)
print(f"Input IDs: {inputs['input_ids']}")

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
    )

print(f"Output IDs: {outputs}")
decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"Decoded: {decoded}")
