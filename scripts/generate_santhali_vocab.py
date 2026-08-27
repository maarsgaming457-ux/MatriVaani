import json
from pathlib import Path

def generate_vocab():
    # 30 Ol Chiki characters
    ol_chiki_chars = [
        'ᱚ', 'ᱛ', 'ᱜ', 'ᱝ', 'ᱞ', 'ᱟ', 'ᱠ', 'ᱡ', 'ᱢ', 'ᱣ',
        'ᱤ', 'ᱥ', 'ᱦ', 'ᱧ', 'ᱨ', 'ᱩ', 'ᱪ', 'ᱫ', 'ᱬ', 'ᱭ',
        'ᱮ', 'ᱯ', 'ᱰ', 'ᱱ', 'ᱲ', 'ᱳ', 'ᱴ', 'ᱵ', 'ᱶ', 'ᱷ'
    ]
    
    # Sort them for consistency
    ol_chiki_chars.sort()
    
    # Standard special tokens for Wav2Vec2 CTC
    # [PAD] is for CTC blank token
    # [UNK] is for unknown characters
    # | is for word boundary
    vocab_dict = {
        "[PAD]": 0,
        "<s>": 1,
        "</s>": 2,
        "[UNK]": 3,
        "|": 4
    }
    
    for i, char in enumerate(ol_chiki_chars):
        vocab_dict[char] = i + 5
        
    out_dir = Path("datasets")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "santhali_vocab.json"
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(vocab_dict, f, ensure_ascii=False, indent=2)
        
    print(f"Generated {out_path} with {len(vocab_dict)} tokens.")

if __name__ == "__main__":
    generate_vocab()
