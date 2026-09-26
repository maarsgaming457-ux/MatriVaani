import os
import gc
import psutil
import torch
from transformers import (
    AutoFeatureExtractor, 
    Wav2Vec2ForCTC, 
    Wav2Vec2Processor,
    Trainer, 
    TrainingArguments
)
import jiwer
import numpy as np

from training.asr.santali.tokenizer import get_santali_tokenizer
from training.asr.santali.data_collator import DataCollatorCTCWithPadding
from data_modules.santali.indicvoices_loader import IndicVoicesLoader

def get_ram_mb():
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

def run_pilot():
    print(f"Initial RAM: {get_ram_mb():.2f} MB")
    
    # 1. Initialize tokenizer and processor
    model_id = "facebook/wav2vec2-base-100k-voxpopuli"
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_id)
    
    # processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    
    # 2. Initialize Model
    # Load pretrained weights, but resize the LM head to match our new vocab
    model = Wav2Vec2ForCTC.from_pretrained(
        model_id, 
        vocab_size=len(tokenizer),
        pad_token_id=tokenizer.pad_token_id,
        ctc_loss_reduction="mean",
        ignore_mismatched_sizes=True
    )
    
    # Freeze feature extractor (the CNN layers) to save massive amounts of RAM
    model.freeze_feature_encoder()
    print("Frozen feature extractor (CNN) layers.")
    
    print(f"Model Load RAM: {get_ram_mb():.2f} MB")
    
    # 3. Use IterableDataset to save massive RAM (strictly < 2 GB constraint)
    from torch.utils.data import IterableDataset
    
    class StreamDataset(IterableDataset):
        def __init__(self, stream_func, max_samples):
            self.stream_func = stream_func
            self.max_samples = max_samples
            
        def __iter__(self):
            count = 0
            for item in self.stream_func():
                if count >= self.max_samples:
                    break
                    
                # 4. Map Dataset to features lazily
                inputs = feature_extractor(item["waveform"], sampling_rate=item["sample_rate"])
                labels = tokenizer(item["normalized_text"])
                
                yield {
                    "input_values": inputs.input_values[0],
                    "labels": labels.input_ids
                }
                count += 1

    print("Initializing lazy iterable datasets...")
    loader = IndicVoicesLoader()
    train_data = StreamDataset(loader.stream_train, 1000)
    valid_data = StreamDataset(loader.stream_valid, 200)
    
    print(f"Pre-training RAM (lazy): {get_ram_mb():.2f} MB")
    
    # 5. Data Collator
    data_collator = DataCollatorCTCWithPadding(processor=feature_extractor, tokenizer=tokenizer)
    
    # 6. Metrics
    def compute_metrics(pred):
        pred_logits = pred.predictions
        pred_ids = np.argmax(pred_logits, axis=-1)
        
        pred.label_ids[pred.label_ids == -100] = tokenizer.pad_token_id
        
        pred_str = tokenizer.batch_decode(pred_ids)
        # we do not want to group tokens when decoding the labels
        label_str = tokenizer.batch_decode(pred.label_ids, group_tokens=False)
        
        # Calculate WER/CER
        # filter out empty references
        valid_preds = []
        valid_refs = []
        for p, r in zip(pred_str, label_str):
            if r.strip():
                valid_preds.append(p)
                valid_refs.append(r)
        
        if not valid_refs:
            return {"wer": 1.0, "cer": 1.0}
            
        wer = jiwer.wer(valid_refs, valid_preds)
        cer = jiwer.cer(valid_refs, valid_preds)
        
        return {"wer": wer, "cer": cer}
        
    # 7. Training Arguments
    # We use a memory efficient config
    # max_steps is required for IterableDataset
    training_args = TrainingArguments(
        output_dir="models/santhali_asr_v0_1_pilot",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4, # Effective batch size = 16
        eval_strategy="steps",
        max_steps=187, # 1000 / 16 = 62 steps per epoch. 3 epochs = 187 steps
        fp16=True, # Hardware dependent
        gradient_checkpointing=True,
        save_steps=50,
        eval_steps=50,
        logging_steps=10,
        learning_rate=3e-4,
        weight_decay=0.005,
        warmup_steps=20,
        save_total_limit=1,
        dataloader_num_workers=0, # Avoid memory leaks on windows
        push_to_hub=False,
    )
    
    # Auto-disable fp16 if running on CPU or unsupported hardware
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
    
    # 8. Train
    print("Starting Training...")
    trainer.train()
    
    # 9. Save
    print("Saving Model...")
    trainer.save_model("models/santhali_asr_v0_1_pilot")
    tokenizer.save_pretrained("models/santhali_asr_v0_1_pilot")
    
    print(f"Post-training RAM: {get_ram_mb():.2f} MB")
    print("Pilot complete!")

if __name__ == "__main__":
    run_pilot()
