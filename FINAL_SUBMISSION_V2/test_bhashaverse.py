import os
import time
import json

start = time.time()
print("Downloading BhashaVerse (this may take a while)...")

import torch
from transformers import MBartForConditionalGeneration
from huggingface_hub import hf_hub_download
import sentencepiece as spm

HF_REPO = "ltrciiith/bhashaverse"
# Just test if we can download the dict and sentencepiece models first
spm_path = hf_hub_download(HF_REPO, "onemtv3b_spm.model")
dict_path = hf_hub_download(HF_REPO, "fairseq_dict.json")
print(f"Downloaded SPM and dict in {time.time() - start:.2f}s")

# Let's try downloading the model
start_model = time.time()
model = MBartForConditionalGeneration.from_pretrained(HF_REPO)
print(f"Downloaded and loaded model in {time.time() - start_model:.2f}s")

# Load SPM and dict
sp = spm.SentencePieceProcessor(model_file=spm_path)
with open(dict_path, encoding="utf-8") as f:
    _fs = json.load(f)

src_sym2id = _fs["src"]
tgt_id2sym = {v: k for k, v in _fs["tgt"].items()}
_sp = _fs["special"]
EOS_ID, PAD_ID, BOS_ID, UNK_ID = _sp["eos"], _sp["pad"], _sp["bos"], _sp["unk"]

DEVICE = "cpu"
model.eval().to(DEVICE)
print(f"Ready on {DEVICE}  ({model.num_parameters():,} parameters)")

def encode(text: str, src_flores: str, tgt_flores: str) -> list:
    tagged = f"###{src_flores}-to-{tgt_flores}### {text}"
    pieces = sp.encode(tagged, out_type=str)
    return [src_sym2id.get(p, UNK_ID) for p in pieces] + [EOS_ID]

def decode(token_ids: list) -> str:
    clean = [t for t in token_ids if t not in (BOS_ID, PAD_ID, EOS_ID)]
    pieces = [tgt_id2sym.get(t, "<unk>") for t in clean]
    return sp.decode(pieces).strip()

def translate(text, sl, tl):
    encoded = encode(text, sl, tl)
    input_ids = torch.tensor([encoded], dtype=torch.long).to(DEVICE)
    attn_mask = torch.ones_like(input_ids).to(DEVICE)
    
    t0 = time.time()
    with torch.no_grad():
        generated = model.generate(
            input_ids=input_ids,
            attention_mask=attn_mask,
            decoder_start_token_id=EOS_ID,
            num_beams=5,
            max_new_tokens=256,
            early_stopping=True,
            no_repeat_ngram_size=3,
            repetition_penalty=1.3,
        )
    out_text = decode(generated[0].tolist())
    latency = time.time() - t0
    return out_text, latency

print("--- Testing Ho -> Hindi ---")
with open('ho_transcripts.json', 'r', encoding='utf-8') as f:
    ho_sentences = json.load(f)

res_dict = {}

for i, ho in enumerate(ho_sentences):
    res, lat = translate(ho, "hoc_Wara", "hin_Deva")
    res_dict[f"Ho_{i+1}_Input"] = ho
    res_dict[f"Ho_{i+1}_Output"] = res
    res_dict[f"Ho_{i+1}_Latency"] = lat
    print(f"Ho {i+1} translated in {lat:.2f}s")

print("--- Testing Hindi -> Ho ---")
hi_sentences = [
    "नमस्ते बच्चों, आज हम गिनती सीखेंगे।",
    "यह एक किताब है।",
    "यह लाल गेंद है।",
    "बच्चे स्कूल जा रहे हैं।"
]

for i, hi in enumerate(hi_sentences):
    res, lat = translate(hi, "hin_Deva", "hoc_Wara")
    res_dict[f"Hi_{i+1}_Input"] = hi
    res_dict[f"Hi_{i+1}_Output"] = res
    res_dict[f"Hi_{i+1}_Latency"] = lat
    print(f"Hi {i+1} translated in {lat:.2f}s")

with open('bhashaverse_results.json', 'w', encoding='utf-8') as f:
    json.dump(res_dict, f, ensure_ascii=False, indent=2)
print("Results saved to bhashaverse_results.json")
