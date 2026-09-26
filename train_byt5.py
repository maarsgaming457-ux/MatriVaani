import os
import json
import torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, EarlyStoppingCallback
import evaluate
import numpy as np
import random

os.makedirs('ho_nmt_models/byt5_small_hindi_ho_v1', exist_ok=True)

# 1. Verify Data Files
def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

train_data = load_jsonl('ho_nmt_data_audit/train.jsonl')
val_data = load_jsonl('ho_nmt_data_audit/validation.jsonl')
test_data = load_jsonl('ho_nmt_data_audit/test.jsonl')

print(f"Expected: Train 173, Val 46, Test 111")
print(f"Actual: Train {len(train_data)}, Val {len(val_data)}, Test {len(test_data)}")
if len(train_data) != 173 or len(val_data) != 46 or len(test_data) != 111:
    print("Discrepancy detected!")
    exit(1)

# 2. Leakage Check
def get_texts(data):
    return set(x['source_text'] for x in data), set(x['target_text'] for x in data)

train_src, train_tgt = get_texts(train_data)
val_src, val_tgt = get_texts(val_data)
test_src, test_tgt = get_texts(test_data)

leak_train_val = train_src.intersection(val_src) or train_tgt.intersection(val_tgt)
leak_train_test = train_src.intersection(test_src) or train_tgt.intersection(test_tgt)
leak_val_test = val_src.intersection(test_src) or val_tgt.intersection(test_tgt)

if leak_train_val or leak_train_test or leak_val_test:
    print(f"Leakage detected! Train/Val: {len(leak_train_val)}, Train/Test: {len(leak_train_test)}, Val/Test: {len(leak_val_test)}")
    exit(1)
else:
    print("No leakage detected.")

# 3. Script Check
def count_scripts(data):
    wc, lat = 0, 0
    for x in data:
        if x['script_class'] == 'WARANG_CITI': wc += 1
        elif x['script_class'] == 'LATIN': lat += 1
    return wc, lat

wc_tr, lat_tr = count_scripts(train_data)
wc_v, lat_v = count_scripts(val_data)
wc_te, lat_te = count_scripts(test_data)
print(f"Train - WC: {wc_tr}, Lat: {lat_tr}")
print(f"Val - WC: {wc_v}, Lat: {lat_v}")
print(f"Test - WC: {wc_te}, Lat: {lat_te}")

# 4. Direction Format (Bidirectional)
def prepare_bidirectional(data):
    formatted = []
    for x in data:
        hi = x['source_text']
        ho = x['target_text']
        # Hindi -> Ho
        formatted.append({
            'input': f"translate Hindi to Ho: {hi}",
            'target': ho,
            'direction': 'hin2hoc',
            'script': x['script_class']
        })
        # Ho -> Hindi
        formatted.append({
            'input': f"translate Ho to Hindi: {ho}",
            'target': hi,
            'direction': 'hoc2hin',
            'script': x['script_class']
        })
    return formatted

train_fmt = prepare_bidirectional(train_data)
val_fmt = prepare_bidirectional(val_data)
test_fmt = prepare_bidirectional(test_data)
print(f"Effective Train pairs: {len(train_fmt)}")

# 5. Tokenizer & Model
model_name = "google/byt5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# 6. Environment
print(f"PyTorch Version: {torch.__version__}")
print(f"CUDA Available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")

# Datasets
train_ds = Dataset.from_list(train_fmt)
val_ds = Dataset.from_list(val_fmt)
test_ds = Dataset.from_list(test_fmt)

def preprocess(examples):
    inputs = [ex for ex in examples['input']]
    targets = [ex for ex in examples['target']]
    model_inputs = tokenizer(inputs, padding="max_length", max_length=128, truncation=True)
    labels = tokenizer(text_target=targets, padding="max_length", max_length=128, truncation=True)
    model_inputs['labels'] = labels['input_ids']
    return model_inputs

train_ds = train_ds.map(preprocess, batched=True)
val_ds = val_ds.map(preprocess, batched=True)

# Metric
sacrebleu = evaluate.load("sacrebleu")
chrf = evaluate.load("chrf")

def compute_metrics(eval_preds):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)
    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [[label.strip()] for label in decoded_labels]
    
    bleu_score = sacrebleu.compute(predictions=decoded_preds, references=decoded_labels)
    chrf_score = chrf.compute(predictions=decoded_preds, references=decoded_labels)
    
    return {"bleu": bleu_score["score"], "chrf": chrf_score["score"]}

# 7. Training Config
training_args = Seq2SeqTrainingArguments(
    output_dir="ho_nmt_models/checkpoints",
    eval_strategy="no",
    save_strategy="no",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=1,
    num_train_epochs=1,
    predict_with_generate=True,
    fp16=False,
    load_best_model_at_end=False,
    dataloader_num_workers=0,
    dataloader_pin_memory=False,
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    
    seed=42
)

trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=val_ds,
    processing_class=tokenizer,
    compute_metrics=compute_metrics,
)

# Train
print("Starting training...")
trainer.train()

# 16. Save best model
trainer.save_model("ho_nmt_models/byt5_small_hindi_ho_v1")

print("Training finished. Evaluating on test set...")
# Let's save a flag file
with open("ho_nmt_models/training_done.txt", "w") as f:
    f.write("done")
