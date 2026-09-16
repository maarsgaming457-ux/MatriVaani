# MatriVaani — Task 10.1.2 IndicTrans2 Colab Direct Inference Validation Report

## 1. Objective
Validate the direct model inference of the i4bharat/indictrans2-indic-indic-dist-320M translation model inside a Google Colab environment using a Tesla T4 GPU to guarantee correct semantics, directionality, and Ol Chiki script rendering before exposing it as an API.

## 2. Previous Task 10.1 Status
Task 10.1 identified that the actual Colab API deployment was blocked due to physical constraints of the agent's execution environment (unable to provision Colab automatically).

## 3. Root Cause Carried Forward
The agent executing this task does not possess programmatic access to spin up a Google Colab session or inject the required Hugging Face authentication tokens.

## 4. Colab Environment
NOT_VALIDATED (Agent is constrained to the local Windows sandbox).

## 5. Python Version
NOT_VALIDATED

## 6. PyTorch Version
NOT_VALIDATED

## 7. CUDA Status
NOT_VALIDATED

## 8. GPU
NONE

## 9. HF Authentication Status
BLOCKED (No HF_TOKEN available; cannot prompt user to paste token into chat).

## 10. IndicTransToolkit Status
BLOCKED

## 11. Model Loading
BLOCKED

## 12. Tokenizer
BLOCKED

## 13. Processor
BLOCKED

## 14. Device
BLOCKED

## 15. Direct Inference Method
NOT_VALIDATED

## 16. Hindi → Santali Results
NOT_VALIDATED

## 17. Santali → Hindi Results
NOT_VALIDATED

## 18. Special Tests
NOT_VALIDATED

## 19. Round-Trip Tests
NOT_VALIDATED

## 20. Script Verification
NOT_VALIDATED

## 21. Performance
NOT_VALIDATED

## 22. Resource Usage
NOT_VALIDATED

## 23. Errors Encountered
- **ERROR:** Missing Colab Environment & HF_TOKEN.
- **ROOT CAUSE:** The autonomous agent sandbox lacks external cloud infrastructure provisioning capabilities and user secrets.
- **FIX ATTEMPT:** Acknowledged the constraint safely.
- **RESULT:** Execution safely halted at Phase 2 (HF Authentication).

## 24. Fixes Applied
None. Stopped execution per instructions to prevent fabricating success.

## 25. Reproducible Colab Setup
To perform this validation manually in Colab, use the following code sequence:

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

# 5. Direct Test
print(translate("मैं संथाली में बोलता हूँ।", "hin_Deva", "sat_Olck"))
print(translate("ᱟᱢ ᱪᱮᱫ ᱞᱮᱠᱟ?", "sat_Olck", "hin_Deva"))
`

## 26. Security Review
- No HF tokens printed.
- No secrets requested in chat.

## 27. Files Modified
No local production files were modified.

## 28. Remaining Blockers
- Manual human execution in Google Colab is required to validate the model's direct inference.

## 29. Recommended Next Task
TASK 10.1.3 — CREATE AND VALIDATE COLAB INDICTRANS2 API (Assuming human validation is completed off-band). Or, wait for manual confirmation of direct inference.

## 30. Final Decision
E. COLAB GPU/AUTHENTICATION BLOCKED
