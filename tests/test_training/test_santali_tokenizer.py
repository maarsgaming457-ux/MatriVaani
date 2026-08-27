import pytest
from training.asr.santali.tokenizer import get_santali_tokenizer

def test_santali_tokenizer():
    tokenizer = get_santali_tokenizer("datasets/santhali_vocab.json")
    
    # Test vocab size (39 + 2 default special tokens BOS/EOS)
    assert len(tokenizer) >= 39
    
    # Test encoding and decoding a real word
    text = "ᱚᱞ ᱪᱤᱠᱤ"
    # Should encode correctly. Spaces should be mapped to the word delimiter | internally
    # but the tokenizer handle that during __call__
    
    inputs = tokenizer(text)
    assert "input_ids" in inputs
    
    decoded = tokenizer.decode(inputs["input_ids"])
    assert decoded == text
    
    # Test unknown token handling
    text_with_unk = "ᱚᱞ ᱪᱤᱠᱤ english"
    inputs_unk = tokenizer(text_with_unk)
    decoded_unk = tokenizer.decode(inputs_unk["input_ids"])
    
    # The english letters should map to [UNK]
    assert "[UNK]" in decoded_unk
