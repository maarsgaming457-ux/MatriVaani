import os
import gc
import psutil
import torch
import json
from transformers import (
    AutoFeatureExtractor, 
    Wav2Vec2ForCTC, 
    Trainer, 
    TrainingArguments
)
import jiwer
import numpy as np

from training.asr.santali.tokenizer import get_santali_tokenizer
from training.asr.santali.data_collator import DataCollatorCTCWithPadding
from data_modules.santali.local_cache_loader import LocalSantaliDataset

def get_ram_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def run_training():
    print("=== STARTING 10K ASR TRAINING ===")
    
    model_id = "facebook/wav2vec2-base-100k-voxpopuli"
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_id)
    
    model = Wav2Vec2ForCTC.from_pretrained(
        model_id, 
        vocab_size=len(tokenizer),
        pad_token_id=tokenizer.pad_token_id,
        ctc_loss_reduction="mean",
        ignore_mismatched_sizes=True
    )
    
    # Freeze CNN feature extractor as per standard Wav2Vec2 finetuning
    model.freeze_feature_encoder()
    
    train_data = LocalSantaliDataset("datasets/cache/santali/metadata/train.jsonl")
    valid_data = LocalSantaliDataset("datasets/cache/santali/metadata/validation.jsonl")
    
    # Wrap in map-style dataset that actually returns input_values and labels
    from torch.utils.data import Dataset
    class ASRDataset(Dataset):
        def __init__(self, base_ds):
            self.base_ds = base_ds
        def __len__(self):
            return len(self.base_ds)
        def __getitem__(self, idx):
            item = self.base_ds[idx]
            inputs = feature_extractor(item["waveform"], sampling_rate=item["sample_rate"])
            labels = tokenizer(item["normalized_text"])
            return {
                "input_values": inputs.input_values[0],
                "labels": labels.input_ids
            }
            
    train_mapped = ASRDataset(train_data)
    valid_mapped = ASRDataset(valid_data)
    
    data_collator = DataCollatorCTCWithPadding(processor=feature_extractor, tokenizer=tokenizer)
    
    def compute_metrics(pred):
        pred_logits = pred.predictions
        pred_ids = np.argmax(pred_logits, axis=-1)
        pred.label_ids[pred.label_ids == -100] = tokenizer.pad_token_id
        
        pred_str = tokenizer.batch_decode(pred_ids)
        label_str = tokenizer.batch_decode(pred.label_ids, group_tokens=False)
        
        valid_preds = []
        valid_refs = []
        for p, r in zip(pred_str, label_str):
            if r.strip():
                valid_preds.append(p)
                valid_refs.append(r)
        
        if not valid_refs:
            return {"wer": 1.0, "cer": 1.0, "empty_rate": 1.0, "mean_pred_len": 0.0}
            
        wer = jiwer.wer(valid_refs, valid_preds)
        cer = jiwer.cer(valid_refs, valid_preds)
        
        empty_count = sum(1 for p in valid_preds if not p.strip())
        empty_rate = empty_count / len(valid_preds)
        mean_pred_len = sum(len(p) for p in valid_preds) / len(valid_preds)
        
        return {"wer": wer, "cer": cer, "empty_rate": empty_rate, "mean_pred_len": mean_pred_len}
        
    output_dir = "models/santhali_asr_v0_1_10k"
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,  # effective batch = 8
        eval_strategy="steps",
        max_steps=500,
        fp16=True, 
        gradient_checkpointing=True,
        save_steps=50,
        eval_steps=50,
        logging_steps=10,
        learning_rate=5e-4,  # slightly higher to force escape
        weight_decay=0.005,
        warmup_steps=50,
        save_total_limit=1,
        dataloader_num_workers=0,
        push_to_hub=False,
    )
    
    if not torch.cuda.is_available():
        training_args.fp16 = False
        
    from transformers import TrainerCallback
    class EarlyEscapeCallback(TrainerCallback):
        def on_evaluate(self, args, state, control, metrics=None, **kwargs):
            if metrics and metrics.get("eval_empty_rate", 1.0) < 0.95:
                print(f"\n[EarlyEscapeCallback] ESCAPED BLANK COLLAPSE! eval_empty_rate = {metrics['eval_empty_rate']} < 0.95. Stopping training.")
                control.should_training_stop = True
                
    trainer = Trainer(
        model=model,
        data_collator=data_collator,
        args=training_args,
        compute_metrics=compute_metrics,
        train_dataset=train_mapped,
        eval_dataset=valid_mapped,
        callbacks=[EarlyEscapeCallback()]
    )
    
    trainer.train()
    
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    eval_dir = "evaluation/asr/santali"
    os.makedirs(eval_dir, exist_ok=True)
    history = trainer.state.log_history
    with open(f"{eval_dir}/10k_training_history.json", "w") as f:
        json.dump(history, f, indent=2)

if __name__ == "__main__":
    run_training()
