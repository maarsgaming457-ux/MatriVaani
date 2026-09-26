from safetensors import safe_open
with safe_open(r"C:\Users\maars\.cache\huggingface\hub\models--ai4bharat--indic-parler-tts\snapshots\7b527af5ee8ed1f9a28d80b19703ed9bb8ba10ca\model.safetensors", framework="pt") as f:
    keys = f.keys()
    print("shared in keys:", "text_encoder.shared.weight" in keys)
