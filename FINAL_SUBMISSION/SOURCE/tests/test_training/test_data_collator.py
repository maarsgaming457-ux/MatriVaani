import torch
from transformers import AutoFeatureExtractor
from training.asr.santali.tokenizer import get_santali_tokenizer
from training.asr.santali.data_collator import DataCollatorCTCWithPadding

def test_data_collator():
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    processor = AutoFeatureExtractor.from_pretrained("facebook/wav2vec2-base-100k-voxpopuli")
    
    collator = DataCollatorCTCWithPadding(processor=processor, tokenizer=tokenizer)
    
    # Mock some features
    features = [
        {"input_values": torch.randn(1000).tolist(), "labels": tokenizer("ᱚᱞ").input_ids},
        {"input_values": torch.randn(2000).tolist(), "labels": tokenizer("ᱪᱤᱠᱤ").input_ids}
    ]
    
    batch = collator(features)
    
    assert "input_values" in batch
    assert "labels" in batch
    
    assert batch["input_values"].shape == (2, 2000)
    
    labels = batch["labels"]
    # ᱪᱤᱠᱤ is 4 characters, ᱚᱞ is 2. The first one should be padded with -100
    assert labels.shape == (2, 4)
    assert (labels[0, 2:] == -100).all()
