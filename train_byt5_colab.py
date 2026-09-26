import os
import sys
import json
import torch
import numpy as np
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments, EarlyStoppingCallback
import evaluate

def load_jsonl(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

import unicodedata
import re

def normalize_text(text):
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    text = "".join(ch for ch in text if not unicodedata.category(ch).startswith('P'))
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def check_leakage(train_data, val_data, test_data):
    def get_sets(data):
        src_exact = set(x['source_text'] for x in data)
        tgt_exact = set(x['target_text'] for x in data)
        pair_exact = set((x['source_text'], x['target_text']) for x in data)
        src_norm = set(normalize_text(x['source_text']) for x in data)
        tgt_norm = set(normalize_text(x['target_text']) for x in data)
        pair_norm = set((normalize_text(x['source_text']), normalize_text(x['target_text'])) for x in data)
        return src_exact, tgt_exact, pair_exact, src_norm, tgt_norm, pair_norm

    train_sets = get_sets(train_data)
    val_sets = get_sets(val_data)
    test_sets = get_sets(test_data)
    
    names = ["EXACT_SOURCE_LEAKAGE", "EXACT_TARGET_LEAKAGE", "EXACT_PAIR_LEAKAGE", 
             "NORMALIZED_SOURCE_LEAKAGE", "NORMALIZED_TARGET_LEAKAGE", "NORMALIZED_PAIR_LEAKAGE"]
             
    leakage_found = False
    
    for i, name in enumerate(names):
        leak_tv = train_sets[i].intersection(val_sets[i])
        leak_tt = train_sets[i].intersection(test_sets[i])
        leak_vt = val_sets[i].intersection(test_sets[i])
        
        if leak_tv or leak_tt or leak_vt:
            print("LEAKAGE_STATUS = FAIL")
            if leak_tv:
                print(f"Check: {name}, Boundary: train <-> validation, Collisions: {len(leak_tv)}")
            if leak_tt:
                print(f"Check: {name}, Boundary: train <-> test, Collisions: {len(leak_tt)}")
            if leak_vt:
                print(f"Check: {name}, Boundary: validation <-> test, Collisions: {len(leak_vt)}")
            leakage_found = True
        else:
            print(f"{name} = 0")
            
    if leakage_found:
        sys.exit(1)
    else:
        print("LEAKAGE_STATUS = PASS")

def contains_warang_citi(text):
    return any(0x118A0 <= ord(c) <= 0x118FF for c in text)

def count_scripts(data):
    wc, lat = 0, 0
    mismatch = False
    for x in data:
        has_wc = contains_warang_citi(x['source_text']) or contains_warang_citi(x['target_text'])
        precomputed_wc = (x['script_class'] == 'WARANG_CITI')
        
        if has_wc != precomputed_wc:
            print(f"DISAGREEMENT DETECTED: Pair ID {x.get('id', 'unknown')} has_wc={has_wc}, precomputed={precomputed_wc}")
            mismatch = True
            
        if has_wc:
            wc += 1
        else:
            lat += 1
            
    if mismatch:
        print("STOPPING due to Warang Citi detection disagreement.")
        sys.exit(1)
    return wc, lat

def prepare_bidirectional(data):
    formatted = []
    for x in data:
        hi = x['source_text']
        ho = x['target_text']
        orig_id = x.get('id', 'unknown')
        formatted.append({
            'input': f"translate Hindi to Ho: {hi}",
            'reference': ho,
            'direction': 'hin2hoc',
            'script_class': x['script_class'],
            'original_id': orig_id
        })
        formatted.append({
            'input': f"translate Ho to Hindi: {ho}",
            'reference': hi,
            'direction': 'hoc2hin',
            'script_class': x['script_class'],
            'original_id': orig_id
        })
    return formatted

def main():
    print("STEP 1: VERIFYING HARDWARE")
    if not torch.cuda.is_available():
        print("ERROR: GPU REQUIRED FOR FINAL RUN. CUDA is not available. STOPPING BEFORE TRAINING.")
        sys.exit(1)
    
    gpu_name = torch.cuda.get_device_name(0)
    gpu_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    print(f"GPU Model: {gpu_name}")
    print(f"GPU VRAM: {gpu_vram:.2f} GB")
    print(f"CUDA Version: {torch.version.cuda}")
    print(f"PyTorch Version: {torch.__version__}")
    
    import transformers
    import datasets as ds
    print(f"Transformers Version: {transformers.__version__}")
    print(f"Datasets Version: {ds.__version__}")

    print("\nSTEP 2: VERIFY DATA")
    train_data = load_jsonl('ho_nmt_data_audit/train.jsonl')
    val_data = load_jsonl('ho_nmt_data_audit/validation.jsonl')
    test_data = load_jsonl('ho_nmt_data_audit/test.jsonl')
    
    print(f"Original Pairs -> Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")
    if len(train_data) != 173 or len(val_data) != 46 or len(test_data) != 111:
        print("ERROR: Discrepancy in data counts.")
        sys.exit(1)
        
    print("\nSTEP 3: LEAKAGE CHECK")
    check_leakage(train_data, val_data, test_data)
    
    print("\nSTEP 4: WARANG CITI DISTRIBUTION")
    for name, split in [("Train", train_data), ("Validation", val_data), ("Test", test_data)]:
        wc, lat = count_scripts(split)
        print(f"{name} - WC: {wc}, Latin: {lat}")

    train_fmt = prepare_bidirectional(train_data)
    val_fmt = prepare_bidirectional(val_data)
    test_fmt = prepare_bidirectional(test_data)
    print(f"Effective Directional Training Examples: {len(train_fmt)}")
    
    print("\nSTEP 5: PREPARE MODEL & TOKENIZER")
    model_name = "google/byt5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    def preprocess(examples):
        inputs = examples['input']
        targets = examples['reference']
        model_inputs = tokenizer(inputs, padding="max_length", max_length=128, truncation=True)
        labels = tokenizer(text_target=targets, padding="max_length", max_length=128, truncation=True)
        model_inputs['labels'] = labels['input_ids']
        return model_inputs

    train_ds = Dataset.from_list(train_fmt).map(preprocess, batched=True)
    val_ds = Dataset.from_list(val_fmt).map(preprocess, batched=True)
    
    sacrebleu = evaluate.load("sacrebleu")
    chrf = evaluate.load("chrf")
    
    def compute_metrics(eval_preds):
        preds, labels = eval_preds
        if isinstance(preds, tuple):
            preds = preds[0]
        # Safeguard decoding
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        
        decoded_preds = []
        for p in preds:
            valid_ids = [tid for tid in p.tolist() if tid < 256 or tid in tokenizer.all_special_ids]
            decoded_preds.append(tokenizer.decode(valid_ids, skip_special_tokens=True).strip())
            
        decoded_labels = [tokenizer.decode(l, skip_special_tokens=True).strip() for l in labels]
        decoded_labels = [[l] for l in decoded_labels]
        
        bleu = sacrebleu.compute(predictions=decoded_preds, references=decoded_labels)["score"]
        c = chrf.compute(predictions=decoded_preds, references=decoded_labels)["score"]
        return {"bleu": bleu, "chrf": c}

    print("\nSTEP 6: TRAINING")
    
    # Determine precision based on GPU
    use_fp16 = False
    use_bf16 = False
    if torch.cuda.is_available():
        if torch.cuda.is_bf16_supported():
            use_bf16 = True
        else:
            use_fp16 = True
            
    training_args = Seq2SeqTrainingArguments(
        output_dir="ho_nmt_models/checkpoints",
        eval_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        warmup_ratio=0.05,
        max_grad_norm=1.0,
        optim="adamw_torch",
        save_total_limit=1,
        num_train_epochs=30,
        predict_with_generate=True,
        fp16=use_fp16,
        bf16=use_bf16,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        seed=42
    )
    
    config_dict = {
        "model": model_name,
        "learning_rate": training_args.learning_rate,
        "batch_size": training_args.per_device_train_batch_size,
        "gradient_accumulation": training_args.gradient_accumulation_steps,
        "epochs": training_args.num_train_epochs,
        "seed": training_args.seed,
        "optimizer": "AdamW",
        "weight_decay": training_args.weight_decay,
        "warmup": training_args.warmup_ratio,
        "precision": "bf16" if use_bf16 else "fp16" if use_fp16 else "fp32",
        "GPU": gpu_name,
        "transformers_version": transformers.__version__,
        "pytorch_version": torch.__version__,
        "dataset_version": ds.__version__
    }
    
    with open("ho_nmt_models/byt5_small_hindi_ho_v1/training_config.json", "w") as f:
        json.dump(config_dict, f, indent=2)

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        processing_class=tokenizer,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)]
    )
    
    trainer.train()
    
    print("\nSTEP 7: SAVING BEST CHECKPOINT")
    out_dir = "ho_nmt_models/byt5_small_hindi_ho_v1"
    if os.path.exists(out_dir) and os.listdir(out_dir):
        print("CHECKPOINT_SAVE = BLOCKED")
        print("PREVIOUS_CHECKPOINT_DETECTED = TRUE")
        sys.exit(1)
    else:
        print("CHECKPOINT_SAVE = ALLOWED")
        print("PREVIOUS_CHECKPOINT_DETECTED = FALSE")
        os.makedirs(out_dir, exist_ok=True)
        trainer.save_model(out_dir)
    
    print("\nSTEP 8: EVALUATING TEST SET")
    test_results_hin2hoc = []
    test_results_hoc2hin = []
    model.eval()
    
    def evaluate_subset(subset, direction_list):
        for ex in subset:
            inputs = tokenizer(ex['input'], return_tensors="pt").to(model.device)
            outputs = model.generate(**inputs, max_length=128)
            valid_ids = [tid for tid in outputs[0].tolist() if tid < 256 or tid in tokenizer.all_special_ids]
            pred = tokenizer.decode(valid_ids, skip_special_tokens=True).strip()
            ex['prediction'] = pred
            ex['exact_match'] = (pred == ex['reference'])
            direction_list.append(ex)

    hin2hoc_test = [x for x in test_fmt if x['direction'] == 'hin2hoc']
    hoc2hin_test = [x for x in test_fmt if x['direction'] == 'hoc2hin']
    
    evaluate_subset(hin2hoc_test, test_results_hin2hoc)
    evaluate_subset(hoc2hin_test, test_results_hoc2hin)
    
    def calc_metrics(subset):
        if not subset: return None
        preds = [x['prediction'] for x in subset]
        refs = [[x['reference']] for x in subset]
        b = sacrebleu.compute(predictions=preds, references=refs)['score']
        c = chrf.compute(predictions=preds, references=refs)['score']
        em = sum(x['exact_match'] for x in subset) / len(subset) * 100
        return {"bleu": b, "chrf": c, "exact_match": em}
        
    metrics = {
        "hin2hoc": calc_metrics(test_results_hin2hoc),
        "hoc2hin": calc_metrics(test_results_hoc2hin)
    }
    
    with open("ho_nmt_models/byt5_small_hindi_ho_v1/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
        
    with open("ho_nmt_models/byt5_small_hindi_ho_v1/predictions_hindi_to_ho.jsonl", "w", encoding='utf-8') as f:
        for res in test_results_hin2hoc:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            
    with open("ho_nmt_models/byt5_small_hindi_ho_v1/predictions_ho_to_hindi.jsonl", "w", encoding='utf-8') as f:
        for res in test_results_hoc2hin:
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            
    print("Pipeline finished successfully! Outputs saved in ho_nmt_models/byt5_small_hindi_ho_v1/")

if __name__ == "__main__":
    main()
