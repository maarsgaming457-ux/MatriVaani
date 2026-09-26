from safetensors import safe_open
try:
    with safe_open(r"C:\Users\maars\.cache\huggingface\hub\models--ai4bharat--indic-parler-tts\snapshots\7b527af5ee8ed1f9a28d80b19703ed9bb8ba10ca\model.safetensors", framework="pt") as f:
        print("text_encoder" in f.keys()[0])
        keys = f.keys()
        has_text_embed = "text_encoder.encoder.embed_tokens.weight" in keys
        has_dec_embed = "decoder.embed_tokens.weight" in keys
        print("text_encoder.encoder.embed_tokens.weight in safetensors:", has_text_embed)
        print("decoder.embed_tokens.weight in safetensors:", has_dec_embed)
except Exception as e:
    print(e)
