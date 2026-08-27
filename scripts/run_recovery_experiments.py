import os
import sys
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
from torch.utils.data import IterableDataset

from training.asr.santali.tokenizer import get_santali_tokenizer
from training.asr.santali.data_collator import DataCollatorCTCWithPadding
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def run_experiment(exp_name):
    print(f"=== RUNNING EXPERIMENT {exp_name.upper()} ===")
    
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
    
    # Configure experiments
    if exp_name == "a":
        # A: baseline config
        model.freeze_feature_encoder()
        lr = 3e-4
        warmup = 10
        steps = 20
    elif exp_name == "b":
        # B: unfreeze encoder (CNN)
        # model.freeze_feature_encoder() is NOT called.
        lr = 3e-4
        warmup = 10
        steps = 20
    elif exp_name == "c":
        # C: Adjusted LR/warmup
        model.freeze_feature_encoder()
        lr = 1e-3
        warmup = 5
        steps = 20
    else:
        raise ValueError("Invalid exp name")
        
    class StreamDataset(IterableDataset):
        def __init__(self, stream_func, max_samples):
            self.stream_func = stream_func
            self.max_samples = max_samples
            
        def __iter__(self):
            count = 0
            for item in self.stream_func():
                if count >= self.max_samples:
                    break
                inputs = feature_extractor(item["waveform"], sampling_rate=item["sample_rate"])
                labels = tokenizer(item["normalized_text"])
                yield {
                    "input_values": inputs.input_values[0],
                    "labels": labels.input_ids
                }
                count += 1

    loader = IndicVoicesLoader()
    train_data = StreamDataset(loader.stream_train, 1000)
    valid_data = StreamDataset(loader.stream_valid, 200)
    
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
        
    output_dir = f"models/santhali_asr_v0_1_recovery_{exp_name}"
    
    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        eval_strategy="steps",
        max_steps=steps, 
        fp16=True, 
        gradient_checkpointing=True,
        save_steps=steps,
        eval_steps=steps,
        logging_steps=10,
        learning_rate=lr,
        weight_decay=0.005,
        warmup_steps=warmup,
        save_total_limit=1,
        dataloader_num_workers=0,
        push_to_hub=False,
    )
    
    if not torch.cuda.is_available():
        training_args.fp16 = False
        
    trainer = Trainer(
        model=model,
        data_collator=data_collator,
        args=training_args,
        compute_metrics=compute_metrics,
        train_dataset=train_data,
        eval_dataset=valid_data,
    )
    
    trainer.train()
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    
    # Save the log history (loss trajectory) to evaluation folder
    eval_dir = "evaluation/asr/santali"
    os.makedirs(eval_dir, exist_ok=True)
    
    history = trainer.state.log_history
    
    with open(f"{eval_dir}/recovery_{exp_name}.json", "w") as f:
        json.dump(history, f, indent=2)
        
if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_experiment(sys.argv[1].lower())
    else:
        print("Provide exp name (a, b, c)")
