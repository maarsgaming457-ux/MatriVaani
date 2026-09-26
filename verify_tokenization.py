import time
from app.services.mundari_translation_service import mundari_translation_service

print("--- 10. Verify model is loaded only once ---")
start = time.time()
res1 = mundari_translation_service.translate("मेरा नाम सुमित है।")
print(f"First inference (includes model load): {time.time()-start:.4f}s")

start = time.time()
res2 = mundari_translation_service.translate("आप कैसे हैं?")
print(f"Second inference: {time.time()-start:.4f}s")

start = time.time()
res3 = mundari_translation_service.translate("धन्यवाद।")
print(f"Third inference: {time.time()-start:.4f}s")

print("--- 3. Verify IndicTrans2 tokenization ---")
text = "मेरा नाम सुमित है।"
norm = mundari_translation_service._normalize_hindi(text)
input_str = f"hin_Deva unr_Deva {norm}"
print(f"1. Final source string: '{input_str}'")

tokenizer = mundari_translation_service.tokenizer
tokens = tokenizer.tokenize(input_str)
print(f"2. SentencePiece output (tokens): {tokens}")
print(f"4. Final model input IDs: {tokenizer.encode(input_str)}")
