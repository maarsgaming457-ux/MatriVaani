import json
import os

def build_vocab():
    with open("evaluation/datasets/santali/character_statistics.json", "r", encoding="utf-8") as f:
        stats = json.load(f)
        
    unique_chars = stats.get("unique_characters", [])
    
    # Filter out Latin characters, `<` and `>` (used for <unintelligible>)
    # and standard spaces (which will map to the special word delimiter)
    filtered_chars = [
        c for c in unique_chars 
        if c.strip() and not c.isascii()
    ]
    
    # Sort for deterministic index assignment
    filtered_chars.sort()
    
    vocab = {
        "[PAD]": 0,
        "[UNK]": 1,
        "|": 2,
    }
    
    idx = 3
    for c in filtered_chars:
        vocab[c] = idx
        idx += 1
        
    os.makedirs("datasets", exist_ok=True)
    with open("datasets/santhali_vocab.json", "w", encoding="utf-8") as f:
        json.dump(vocab, f, indent=4, ensure_ascii=False)
        
    print(f"Vocabulary built with {len(vocab)} tokens.")
    print("Tokens:", vocab)

if __name__ == "__main__":
    build_vocab()
