from safetensors import safe_open
with safe_open(r"C:\Users\maars\.cache\huggingface\hub\models--ai4bharat--indic-parler-tts\snapshots\7b527af5ee8ed1f9a28d80b19703ed9bb8ba10ca\model.safetensors", framework="pt") as f:
    keys = f.keys()
    print("Total keys:", len(keys))
    for k in [k for k in keys if "embed_tokens" in k]:
        print(k)
