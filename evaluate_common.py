import pandas as pd
import torch
import unicodedata
import os
import sys
import codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

csv_file = 'COMMON_HINDI_MUNDARI_EXPANSION.csv'
df = pd.read_csv(csv_file)

# 1. REPORT CSV STATS
total_rows = len(df)
populated_refs = df['mundari_reference'].notna() & (df['mundari_reference'] != '')
blank_refs_count = total_rows - populated_refs.sum()
verified_count = (df['validation_status'] == 'VERIFIED').sum()
needs_validation_count = (df['validation_status'] == 'NEEDS HUMAN VALIDATION').sum()

print(f"Total rows: {total_rows}")
print(f"Rows with Mundari reference: {populated_refs.sum()}")
print(f"Rows with blank Mundari reference: {blank_refs_count}")
print(f"Rows marked VERIFIED: {verified_count}")
print(f"Rows marked NEEDS HUMAN VALIDATION: {needs_validation_count}")

# 4. LOAD MODEL
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
model_path = r'C:\study_files\sih project\backend\best_model_main2'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path, trust_remote_code=True).to(device).eval()

def normalize_hindi(text: str) -> str:
    norm = unicodedata.normalize('NFKC', text.strip())
    terminal_punctuations = ('।', '?', '!', '.')
    if not norm.endswith(terminal_punctuations): 
        norm += '।'
    return norm

# 7. KNOWN-GOOD TEST
def run_model(text: str) -> tuple:
    norm_text = normalize_hindi(text)
    input_str = f"hin_Deva unr_Deva {norm_text}"
    inputs = tokenizer(input_str, return_tensors='pt').to(device)
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
            do_sample=False
        )
    pred = tokenizer.decode(outputs[0], skip_special_tokens=True).replace('unr_Deva','').replace('hin_Deva','').replace(' ',' ').strip()
    return norm_text, input_str, pred

norm_text, source_format, pred_known = run_model("मेरा नाम सुमित है")
if pred_known != "आञाः नुतुम सुमित मेनाः।":
    print(f"REGRESSION DETECTED on known-good test! Expected: आञाः नुतुम सुमित मेनाः। Got: {pred_known}")
    sys.exit(1)
print(f"KNOWN-GOOD TEST PASSED: {pred_known}")

# 8. TEST "क्या कर रहे हो?"
norm_text_kya, source_format_kya, pred_kya = run_model("क्या कर रहे हो?")
print(f"क्या कर रहे हो? -> {pred_kya}")

# 9. RUN ALL CSV TESTS
results = []
for idx, row in df.iterrows():
    src = str(row['hindi_source']).strip() if pd.notna(row['hindi_source']) else ""
    ref = str(row['mundari_reference']).strip() if pd.notna(row['mundari_reference']) else ""
    cat = row['category']
    val_status = row['validation_status']
    
    norm_text, src_format, pred = run_model(src)
    
    # Evaluate status
    if ref == "" or ref.lower() == "nan":
        eval_status = "REFERENCE UNAVAILABLE"
        ref_avail = "No"
    else:
        if val_status == "VERIFIED":
            eval_status = "REFERENCE VERIFIED"
        else:
            eval_status = "HUMAN REVIEW REQUIRED"
        ref_avail = "Yes"
        
    if eval_status == "REFERENCE UNAVAILABLE":
        eval_status = "MODEL PREDICTION ONLY"
        
    results.append({
        'hindi_source': src,
        'normalized_input': norm_text,
        'model_prediction': pred,
        'mundari_reference': ref,
        'category': cat,
        'validation_status': val_status,
        'reference_available': ref_avail,
        'evaluation_status': eval_status,
        'notes': ''
    })

res_df = pd.DataFrame(results)
res_df.to_csv('COMMON_SENTENCE_MODEL_PREDICTIONS.csv', index=False, encoding='utf-8')
print("Saved COMMON_SENTENCE_MODEL_PREDICTIONS.csv")
