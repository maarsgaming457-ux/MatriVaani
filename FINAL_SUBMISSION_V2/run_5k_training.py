import os
import torch
import pandas as pd
import soundfile as sf
import numpy as np
import jiwer
from dataclasses import dataclass
from typing import Dict, List, Union
from datasets import Dataset
from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    TrainingArguments,
    Trainer
)

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

def prepare_dataset(batch, processor):
    audio_path = batch["file_name"]
    speech, _ = sf.read(audio_path)
    if len(speech.shape) > 1:
        speech = speech.mean(axis=1)
    batch["input_values"] = processor(speech, sampling_rate=16000).input_values[0]
    batch["labels"] = processor.tokenizer(batch["transcription"]).input_ids
    return batch

@dataclass
class DataCollatorCTCWithPadding:
    processor: Wav2Vec2Processor
    padding: Union[bool, str] = True

    def __call__(self, features: List[Dict[str, Union[List[int], torch.Tensor]]]) -> Dict[str, torch.Tensor]:
        input_features = [{"input_values": feature["input_values"]} for feature in features]
        label_features = [{"input_ids": feature["labels"]} for feature in features]

        batch = self.processor.pad(
            input_features,
            padding=self.padding,
            return_tensors="pt",
        )
        
        labels_batch = self.processor.tokenizer.pad(
            label_features,
            padding=self.padding,
            return_tensors="pt",
        )

        labels = labels_batch["input_ids"].masked_fill(labels_batch.attention_mask.ne(1), -100)
        batch["labels"] = labels
        return batch

def compute_metrics(pred, processor):
    pred_logits = pred.predictions
    pred_ids = np.argmax(pred_logits, axis=-1)
    pred.label_ids[pred.label_ids == -100] = processor.tokenizer.pad_token_id
    
    pred_str = processor.batch_decode(pred_ids)
    label_str = processor.batch_decode(pred.label_ids, group_tokens=False)
    
    wer = jiwer.wer(label_str, pred_str)
    cer = jiwer.cer(label_str, pred_str)
    return {"wer": wer, "cer": cer}

def main():
    print("Loading Processor...")
    processor = Wav2Vec2Processor.from_pretrained("models/checkpoint-1500")
    
    print("Loading Dataset...")
    train_df = pd.read_csv("datasets/splits/train_5000.csv")
    train_dataset = Dataset.from_pandas(train_df)
    
    # We use a small subset of the test set just for evaluation during training to save time
    test_df = pd.read_csv("datasets/splits/test_2949.csv").head(100)
    test_dataset = Dataset.from_pandas(test_df)
    
    print("Preparing Datasets...")
    train_dataset = train_dataset.map(lambda x: prepare_dataset(x, processor), remove_columns=train_dataset.column_names, num_proc=1)
    test_dataset = test_dataset.map(lambda x: prepare_dataset(x, processor), remove_columns=test_dataset.column_names, num_proc=1)
    
    data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)
    
    print("Loading Model...")
    model = Wav2Vec2ForCTC.from_pretrained(
        "models/checkpoint-1500",
        ctc_loss_reduction="mean", 
        pad_token_id=processor.tokenizer.pad_token_id,
        vocab_size=len(processor.tokenizer)
    )
    
    # Freeze feature extractor to save RAM and keep acoustic robustness
    model.freeze_feature_encoder()

    training_args = TrainingArguments(
        output_dir="models/santhali_asr_5k",
        per_device_train_batch_size=2, # Small batch for CPU
        gradient_accumulation_steps=4, # Effective batch 8
        eval_strategy="steps",
        num_train_epochs=3,
        fp16=False,
        save_steps=100,
        eval_steps=100,
        logging_steps=10,
        learning_rate=3e-4,
        warmup_steps=50,
        save_total_limit=2,
        dataloader_num_workers=0,
    )
    
    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        data_collator=data_collator,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=lambda pred: compute_metrics(pred, processor)
    )
    
    print("Starting/Resuming Training...")
    trainer.train(resume_from_checkpoint=True)
    
    print("Saving Final Model...")
    model.save_pretrained("models/santhali_asr_final_5k")
    processor.save_pretrained("models/santhali_asr_final_5k")
    print("Training Complete!")

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
