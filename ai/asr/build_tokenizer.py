import os
from transformers import Wav2Vec2CTCTokenizer, Wav2Vec2FeatureExtractor, Wav2Vec2Processor
from pathlib import Path

def build_tokenizer_and_processor(vocab_file: str, model_dir: str):
    print(f"Loading vocabulary from {vocab_file}")
    
    # 1. Create Tokenizer
    # We define unk_token and pad_token matching our vocab
    # word_delimiter_token is '|'
    tokenizer = Wav2Vec2CTCTokenizer(
        vocab_file, 
        unk_token="[UNK]",
        pad_token="[PAD]",
        word_delimiter_token="|"
    )
    
    # 2. Create Feature Extractor
    # facebook/wav2vec2-base-100k-voxpopuli uses standard 16kHz audio, with feature extraction
    feature_extractor = Wav2Vec2FeatureExtractor(
        feature_size=1, 
        sampling_rate=16000, 
        padding_value=0.0, 
        do_normalize=True, 
        return_attention_mask=True
    )
    
    # 3. Create Processor
    processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    
    # 4. Save to model directory
    os.makedirs(model_dir, exist_ok=True)
    processor.save_pretrained(model_dir)
    print(f"Saved custom Santhali processor to {model_dir}")

if __name__ == "__main__":
    vocab_path = "datasets/santhali_vocab.json"
    output_dir = "models/santhali_wav2vec2_processor"
    build_tokenizer_and_processor(vocab_path, output_dir)
