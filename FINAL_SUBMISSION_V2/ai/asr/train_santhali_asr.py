import os
import torch
import pandas as pd
import soundfile as sf
from dataclasses import dataclass
from typing import Dict, List, Union
from datasets import Dataset
from transformers import (
    Wav2Vec2Processor,
    Wav2Vec2ForCTC,
    TrainingArguments,
    Trainer
)

def prepare_dataset(batch, processor):
    # Load audio
    audio_path = os.path.join("datasets/raw", batch["file_name"])
    speech, _ = sf.read(audio_path)
    
    # Process audio
    batch["input_values"] = processor(speech, sampling_rate=16000).input_values[0]
    
    # Process text
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

def main():
    print("Loading Processor...")
    processor = Wav2Vec2Processor.from_pretrained("models/santhali_wav2vec2_processor")
    
    print("Loading Dataset...")
    df = pd.read_csv("datasets/raw/metadata.csv")
    raw_dataset = Dataset.from_pandas(df)
    
    # Split for dummy train/eval
    dataset = raw_dataset.train_test_split(test_size=0.2)
    
    print("Preparing Dataset...")
    dataset = dataset.map(
        lambda batch: prepare_dataset(batch, processor), 
        remove_columns=dataset["train"].column_names
    )
    
    data_collator = DataCollatorCTCWithPadding(processor=processor, padding=True)
    
    print("Loading Model...")
    # Load the base model and swap the LM head for our Santhali Vocab
    model = Wav2Vec2ForCTC.from_pretrained(
        "facebook/wav2vec2-base-100k-voxpopuli",
        ctc_loss_reduction="mean", 
        pad_token_id=processor.tokenizer.pad_token_id,
        vocab_size=len(processor.tokenizer)
    )
    
    # Freeze feature extractor to save RAM and keep acoustic robustness
    model.freeze_feature_encoder()

    # Define training arguments (Fast dummy settings)
    training_args = TrainingArguments(
        output_dir="models/santhali_asr_checkpoints",
        per_device_train_batch_size=2,
        eval_strategy="steps",
        num_train_epochs=3,
        fp16=False, # Safe for CPU / basic environments
        save_steps=10,
        eval_steps=10,
        logging_steps=5,
        learning_rate=1e-4,
        warmup_steps=5,
        save_total_limit=2,
    )
    
    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        data_collator=data_collator,
        args=training_args,
        train_dataset=dataset["train"],
        eval_dataset=dataset["test"],
        processing_class=processor.feature_extractor,
    )
    
    print("Starting Training...")
    trainer.train()
    
    print("Saving Final Model...")
    model.save_pretrained("models/santhali_asr_final")
    processor.save_pretrained("models/santhali_asr_final")
    print("Training Complete! Saved to models/santhali_asr_final")

if __name__ == "__main__":
    main()
