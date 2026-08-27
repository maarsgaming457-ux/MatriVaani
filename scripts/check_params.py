import torch
from transformers import Wav2Vec2ForCTC

def check_parameters():
    model = Wav2Vec2ForCTC.from_pretrained("models/santhali_asr_v0_1_pilot/checkpoint-150")
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    frozen_params = sum(p.numel() for p in model.parameters() if not p.requires_grad)
    
    lm_head_params = sum(p.numel() for p in model.lm_head.parameters())
    
    # Let's see what is actually frozen.
    frozen_names = [n for n, p in model.named_parameters() if not p.requires_grad]
    trainable_names = [n for n, p in model.named_parameters() if p.requires_grad]
    
    print(f"Total parameters: {total_params:,}")
    print(f"Trainable parameters: {trainable_params:,}")
    print(f"Frozen parameters: {frozen_params:,}")
    print(f"LM head parameters (newly initialized): {lm_head_params:,}")
    
    print(f"\nFrozen blocks:")
    print(set([n.split('.')[1] for n in frozen_names if n.startswith("wav2vec2")]))
    
    print(f"\nTrainable blocks:")
    print(set([n.split('.')[1] for n in trainable_names if n.startswith("wav2vec2")]))

if __name__ == "__main__":
    check_parameters()
