
import json
import torch
import sentencepiece as spm
from transformers import MBartForConditionalGeneration

from huggingface_hub import hf_hub_download

HF_REPO        = "ltrciiith/bhashaverse"   

SPM_MODEL_PATH = hf_hub_download(HF_REPO, "onemtv3b_spm.model")
DICT_PATH      = hf_hub_download(HF_REPO, "fairseq_dict.json")


DEVICE         = "cuda" if torch.cuda.is_available() else "cpu"
BEAM_SIZE      = 5
MAX_NEW_TOKENS = 256

language_mapping = {
    "asm":      "asm_Beng",
    "ben":      "ben_Beng",
    "ban":      "ben_Beng",
    "brx":      "brx_Deva",
    "doi":      "doi_Deva",
    "gom":      "gom_Deva",
    "guj":      "guj_Gujr",
    "hin":      "hin_Deva",
    "kan":      "kan_Knda",
    "kas_arab": "kas_Arab",
    "kas":      "kas_Arab",
    "kas_deva": "kas_Deva",
    "mai":      "mai_Deva",
    "mal":      "mal_Mlym",
    "mar":      "mar_Deva",
    "mni_beng": "mni_Beng",
    "mni":      "mni_Beng",
    "mni_mtei": "mni_Mtei",
    "npi":      "npi_Deva",
    "ory":      "ory_Orya",
    "ori":      "ory_Orya",
    "odi":      "ory_Orya",
    "pan":      "pan_Guru",
    "pun":      "pan_Guru",
    "san":      "san_Deva",
    "sat":      "sat_Olck",
    "snd_arab": "snd_Arab",
    "snd_deva": "snd_Deva",
    "snd":      "snd_Arab",
    "tam":      "tam_Taml",
    "tel":      "tel_Telu",
    "urd_arab": "urd_Arab",
    "urd":      "urd_Arab",
    "eng":      "eng_Latn",
}


print("Loading SPM model …")
sp = spm.SentencePieceProcessor(model_file=SPM_MODEL_PATH)

print("Loading fairseq dictionary …")
with open(DICT_PATH, encoding="utf-8") as f:
    _fs = json.load(f)

src_sym2id = _fs["src"]                              # piece(str)  → src dict ID(int)
tgt_id2sym = {v: k for k, v in _fs["tgt"].items()}  # tgt dict ID(int) → piece(str)

_sp    = _fs["special"]
EOS_ID = _sp["eos"]   # 2
PAD_ID = _sp["pad"]   # 1
BOS_ID = _sp["bos"]   # 0
UNK_ID = _sp["unk"]   # 3

print("Loading HF model …")
model = MBartForConditionalGeneration.from_pretrained(HF_REPO)
model.eval().to(DEVICE)
print(f"Ready on {DEVICE}  ({model.num_parameters():,} parameters)")



def encode(text: str, src_flores: str, tgt_flores: str) -> list:

    tagged = f"###{src_flores}-to-{tgt_flores}### {text}"
    pieces = sp.encode(tagged, out_type=str)
    return [src_sym2id.get(p, UNK_ID) for p in pieces] + [EOS_ID]


def decode(token_ids: list) -> str:
   
    clean  = [t for t in token_ids if t not in (BOS_ID, PAD_ID, EOS_ID)]
    pieces = [tgt_id2sym.get(t, "<unk>") for t in clean]
    return sp.decode(pieces).strip()


def _translate_batch(encoded_batch: list) -> list:

    if not encoded_batch:
        return []

    max_len   = max(len(ids) for ids in encoded_batch)
    input_ids = torch.full((len(encoded_batch), max_len), PAD_ID, dtype=torch.long)
    attn_mask = torch.zeros_like(input_ids)

    for i, ids in enumerate(encoded_batch):
        input_ids[i, :len(ids)] = torch.tensor(ids, dtype=torch.long)
        attn_mask[i, :len(ids)] = 1

    input_ids = input_ids.to(DEVICE)
    attn_mask = attn_mask.to(DEVICE)

    with torch.no_grad():
        generated = model.generate(
            input_ids               = input_ids,
            attention_mask          = attn_mask,
            decoder_start_token_id  = EOS_ID,   # fairseq convention: start with EOS
            num_beams               = BEAM_SIZE,
            max_new_tokens          = MAX_NEW_TOKENS,
            early_stopping          = True,
            no_repeat_ngram_size    = 3,
            repetition_penalty      = 1.3,
        )

    return [decode(out.tolist()) for out in generated]


def split_into_parts(text: str, num_words: int = 100) -> list:

    words, parts, cur = text.split(), [], []
    for w in words:
        cur.append(w)
        if len(cur) == num_words:
            parts.append(" ".join(cur))
            cur = []
    if cur:
        parts.append(" ".join(cur))
    return parts


def translate_onemt(text: str, sl: str, tl: str) -> str:
    
    nsl = language_mapping[sl]   # "hin" → "hin_Deva"
    ntl = language_mapping[tl]   # "tel" → "tel_Telu"

    if len(text.split()) > 200:
        parts, outputs = split_into_parts(text), []
        for part in parts:
            out = _translate_batch([encode(part, nsl, ntl)])
            outputs.append(out[0] if out and out[0] else part)
        return " ".join(outputs).strip()
    else:
        out = _translate_batch([encode(text, nsl, ntl)])
        return (out[0] if out and out[0] else text).strip()


def translate_batch(texts: list, sl: str, tl: str,
                    batch_size: int = 32) -> list:
    
    nsl, ntl = language_mapping[sl], language_mapping[tl]
    results  = []
    for i in range(0, len(texts), batch_size):
        batch   = texts[i:i + batch_size]
        encoded = [encode(t, nsl, ntl) for t in batch]
        results.extend(_translate_batch(encoded))
        print(f"  Translated {min(i + batch_size, len(texts))}/{len(texts)}")
    return results


print(translate_onemt("నమస్కారం, మీరు ఎలా ఉన్నారు?", 'tel', 'eng'))