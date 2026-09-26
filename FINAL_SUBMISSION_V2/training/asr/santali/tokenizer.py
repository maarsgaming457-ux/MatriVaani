import os
from transformers import Wav2Vec2CTCTokenizer

def get_santali_tokenizer(vocab_file="datasets/santhali_vocab.json"):
    """
    Returns a Wav2Vec2CTCTokenizer initialized with the deterministic Santali vocabulary.
    """
    if not os.path.exists(vocab_file):
        raise FileNotFoundError(f"Vocab file {vocab_file} not found. Run scripts/build_vocab.py first.")
        
    tokenizer = Wav2Vec2CTCTokenizer(
        vocab_file, 
        unk_token="[UNK]", 
        pad_token="[PAD]", 
        word_delimiter_token="|"
    )
    
    return tokenizer
