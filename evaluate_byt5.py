import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import evaluate
from tqdm import tqdm

model_path = "ho_nmt_models/byt5_small_hindi_ho_v1"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

test_data = load_jsonl('ho_nmt_data_audit/test.jsonl')

def prepare_bidirectional(data):
    formatted = []
    for x in data:
        hi = x['source_text']
        ho = x['target_text']
        formatted.append({
            'input': f"translate Hindi to Ho: {hi}",
            'reference': ho,
            'direction': 'hin2hoc',
            'script': x['script_class']
        })
        formatted.append({
            'input': f"translate Ho to Hindi: {ho}",
            'reference': hi,
            'direction': 'hoc2hin',
            'script': x['script_class']
        })
    return formatted

test_fmt = prepare_bidirectional(test_data)

sacrebleu = evaluate.load("sacrebleu")
chrf = evaluate.load("chrf")

results = []

for ex in tqdm(test_fmt):
    input_text = ex['input']
    inputs = tokenizer(input_text, return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_length=128)
    
    # Safely decode
    valid_ids = [tid for tid in outputs[0].tolist() if tid < 256 or tid in tokenizer.all_special_ids]
    pred = tokenizer.decode(valid_ids, skip_special_tokens=True).strip()
    
    ref = ex['reference']
    ex['prediction'] = pred
    ex['exact_match'] = (pred == ref)
    results.append(ex)

with open('ho_nmt_models/test_predictions.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

def calc_metrics(subset):
    preds = [x['prediction'] for x in subset]
    refs = [[x['reference']] for x in subset]
    if not preds: return None
    b = sacrebleu.compute(predictions=preds, references=refs)['score']
    c = chrf.compute(predictions=preds, references=refs)['score']
    em = sum(x['exact_match'] for x in subset) / len(subset) * 100
    return {"bleu": b, "chrf": c, "em": em}

hin2hoc = [x for x in results if x['direction'] == 'hin2hoc']
hoc2hin = [x for x in results if x['direction'] == 'hoc2hin']

hin2hoc_metrics = calc_metrics(hin2hoc)
hoc2hin_metrics = calc_metrics(hoc2hin)

metrics = {
    'hin2hoc': hin2hoc_metrics,
    'hoc2hin': hoc2hin_metrics
}

with open('ho_nmt_models/test_metrics.json', 'w', encoding='utf-8') as f:
    json.dump(metrics, f, indent=2)

print("Evaluation complete.")
