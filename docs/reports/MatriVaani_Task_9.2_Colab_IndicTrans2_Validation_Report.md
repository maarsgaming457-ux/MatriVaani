# MatriVaani — Task 9.2 Colab IndicTrans2 Validation Report

## 1. Objective
Verify that the actual IndicTrans2 model (i4bharat/indictrans2-indic-indic-dist-320M) can be loaded and used for real Hindi ↔ Santali translation in Google Colab.

## 2. Previous Task 9.1 Status
Task 9.1 identified that the backend translation service is blocked pending a remote Colab API. The immediate recommendation was to validate the Colab environment.

## 3. Colab Environment
NOT_VALIDATED (Agent is constrained to the local Windows sandbox and cannot provision external cloud infrastructure).

## 4. Python Version
NOT_VALIDATED

## 5. PyTorch Version
NOT_VALIDATED

## 6. CUDA
NOT_VALIDATED

## 7. GPU
NONE

## 8. HF Authentication Status
BLOCKED (No HF_TOKEN Colab Secret available locally).

## 9. IndicTransToolkit Status
BLOCKED

## 10. Model Loading Status
BLOCKED

## 11. Tokenizer Status
BLOCKED

## 12. Processor Status
BLOCKED

## 13. Model Device
BLOCKED

## 14. Direct Inference Method
NOT_VALIDATED

## 15. Hindi → Santali Results
NOT_VALIDATED

## 16. Santali → Hindi Results
NOT_VALIDATED

## 17. Special Tests
NOT_VALIDATED

## 18. Round-Trip Tests
NOT_VALIDATED

## 19. Ol Chiki Verification
NOT_VALIDATED

## 20. Performance
NOT_MEASURED

## 21. Resource Usage
NOT_MEASURED

## 22. Errors Encountered
- **ERROR:** Colab Environment & GPU Unavailable.
- **ROOT CAUSE:** The autonomous agent lacks cloud API keys to autonomously spawn Google Colab sessions and cannot prompt the user for the HF_TOKEN in chat.
- **FIX ATTEMPT:** Acknowledged the physical constraint per instructions.
- **RESULT:** Execution halted safely at Phase 2 (HF Authentication).

## 23. Fixes
None applied. Proceeding with safe-fail.

## 24. Reproducible Setup
For a human developer executing this task in Colab:
`python
# 1. Install dependencies
!pip install -q transformers torch pydantic fastapi uvicorn nest-asyncio pyngrok
!pip install -q git+https://github.com/VarunGumma/IndicTransToolkit.git

# 2. Authentication
import os
from google.colab import userdata
os.environ["HF_TOKEN"] = userdata.get('HF_TOKEN')

# 3. Load Model
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from IndicTransToolkit import IndicProcessor

model_name = "ai4bharat/indictrans2-indic-indic-dist-320M"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, trust_remote_code=True).to(device)
model.eval()
ip = IndicProcessor(inference=True)

# 4. Inference Function
def translate(text, src, tgt):
    batch = ip.preprocess_batch([text], src_lang=src, tgt_lang=tgt)
    inputs = tokenizer(batch, padding="longest", truncation=True, max_length=256, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=256, num_beams=5)
    decoded = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return ip.postprocess_batch(decoded, lang=tgt)[0]
`

## 25. Security Review
- No HF tokens printed or requested.
- No local codebase files modified.

## 26. Files Modified
None.

## 27. Remaining Blockers
Human execution of the Colab notebook is required.

## 28. Recommended Next Task
Pending Manual Colab Validation.

## 29. Final Decision
E. COLAB GPU OR AUTHENTICATION BLOCKED
