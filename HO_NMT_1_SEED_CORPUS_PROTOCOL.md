# HO NMT 1 SEED CORPUS PROTOCOL

## 1. OBJECTIVE
Establish a strictly human-verified Hindi ? Ho translation pilot dataset of 100 pairs for multilingual NMT evaluation and training.

## 2. COLLECTION STATUS
- **DATA_COLLECTION_STATUS**: NOT_STARTED
- **VERIFIED_HINDI_HO_PAIRS**: 0
- **HUMAN_COLLECTION_REQUIRED**: TRUE
- **MODEL_TRAINING**: NOT_STARTED
- **PRODUCTION_CHANGES**: NONE

## 3. HUMAN TRANSLATION PROTOCOL
1. **Source**: A native/proficient Ho speaker is provided with the 100 Hindi template sentences.
2. **Translation**: The speaker translates the meaning into natural, colloquial Ho.
3. **Script Policy**: The speaker writes in their preferred script (Warang Citi, Devanagari, or Latin). The exact script is recorded. No automatic transliteration is performed.
4. **Independent Verification**: A second speaker verifies meaning preservation, grammar, and script accuracy.
5. **Marking**: Only after verification is human_verified = true and ground_truth = true applied.

## 4. TRAIN/EVALUATION SPLIT
Once 100 valid pairs are collected:
- **70 pairs**: Training Pilot
- **15 pairs**: Validation
- **15 pairs**: Test (STRICTLY ISOLATED)
The test set must NEVER be used for training, template construction, or lexical mining.

## 5. DATA LEAKAGE PROTECTION
- The alidate_seed.py script strictly filters duplicate Hindi and duplicate Ho sentences.
- It rejects identical source/target texts and unverified records.
- Train/Test overlap is prevented by mathematical set disjoint checks in the planned loading pipeline.

## 6. FUTURE MODEL EXPERIMENT
- **Candidate Architecture**: A byte-level model (like ByT5) or a multilingual encoder-decoder architecture.
- **Ho Support Verification**: We DO NOT claim any model natively supports Ho yet. Support must be proven experimentally on the 15-pair test set.
- **Production Isolation**: The production inference FastAPI/Flutter routes remain untouched.

## 7. FINAL VERDICT
The infrastructure is ready. We await human data entry.
