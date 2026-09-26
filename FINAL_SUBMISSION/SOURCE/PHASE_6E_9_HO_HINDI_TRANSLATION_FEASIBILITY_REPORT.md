# MATRI VAANI — PHASE 6E.9: HO ? HINDI TRANSLATION FEASIBILITY REPORT

## 1. Executive Summary
This report investigates the technical feasibility of implementing a full Ho Speech ? Ho Text ? Hindi Text ? Hindi TTS pipeline within the MatriVaani architecture. Current findings show that while Ho ASR is functional and a 100-record annotation queue is prepared, there is currently **zero existing Ho-Hindi parallel data** in the project, and existing machine translation services (IndicTrans2, Sarvam, Bhashini) do not natively support the Ho language. Therefore, immediate machine translation of Ho to Hindi is not feasible without first collecting parallel data through human annotation and then training or fine-tuning a custom/multilingual translation model.

## 2. Existing Ho Data Inventory
- **Ho Audio:** 100 genuine Ho WAV files (recovered and verified).
- **Ho ASR Transcripts:** 100 raw ASR outputs stored in the annotation database.
- **Ho-Hindi Parallel Data:** 0 pairs exist. No historical parallel data was found in the project.
- **Human-verified Translations:** 0 real records.
- **Machine-generated Translations:** None exist, as no model is capable of generating them for Ho.

## 3. Existing Ho ASR Capability
- **Model Path:** models/ho_asr
- **Architecture:** Wav2Vec2
- **Parameters / Size:** ~377 MB on disk.
- **Status:** Functional and successfully integrated into the annotation tool.

## 4. Existing Translation Capabilities
- **IndicTrans2:** Evaluated via local WSL API. Supports 22 scheduled Indian languages including Santali, but **does not support Ho**.
- **Sarvam API:** API key present, but Sarvam does not natively support Ho translation.
- **Bhashini API:** Credentials are NOT_CONFIGURED. Even if configured, Bhashini lacks native Ho support.

## 5. Ho Language Support Matrix
| Model/Service | Supports Ho Natively? |
| --- | --- |
| IndicTrans2 | No |
| Sarvam API | No |
| Bhashini API | No |
| NLLB-200 | No (not natively mapped to Ho script/language id) |

## 6. Existing Ho-Hindi Parallel Data Status
There is absolutely no Ho-Hindi parallel dataset in the project repository. The 100 records currently in the annotation database are exclusively audio + raw Ho ASR text. They are *candidates* for becoming parallel data, provided human annotators manually translate them.

## 7. Model/Approach Comparison
### A. Existing API/service (Sarvam, Bhashini)
- **Support:** None natively.
- **Feasibility:** Not viable.

### B. IndicTrans2 adaptation to Ho
- **Data Required:** Large parallel corpus (100k+ sentences).
- **Feasibility:** Not viable in the short term due to massive data and GPU requirements for adapting such a large sequence-to-sequence model to a wholly unseen language.

### C. NLLB / Multilingual Translation Model
- **Data Required:** 10k-50k parallel sentences for fine-tuning.
- **Feasibility:** Moderate long-term approach if we can amass enough data. Would require significant fine-tuning (LoRA/QLoRA) on GPUs.

### D. Small custom Ho?Hindi model (e.g., MarianMT/Transformer)
- **Data Required:** ~10k+ sentences.
- **Feasibility:** Most viable for a standalone offline Android app if data becomes available. Model size would be small (~50-100MB), suitable for edge deployment.

## 8. Data Requirements
- **Minimum Proof-of-Concept:** ~100-500 sentences. (Can be achieved manually via the current annotation tool pilot).
- **Useful Pilot Dataset:** 1,000 - 5,000 sentences.
- **Production-Quality Dataset:** 10,000+ sentences.

## 9. Annotation Tool Readiness
- **Status:** **READY**. 
- The Ho Annotation Tool (Phase 6E.8) has been fully prepared. It exposes Ho Audio, Raw ASR (read-only), editable Corrected Ho, editable Human Hindi Translation, Categories, and explicit Human Verification controls.

## 10. Online Architecture
Currently proven segments:
Ho ASR (Local/FastAPI) -> (MISSING) -> Hindi TTS (API)
The Ho?Hindi translation node is missing and will need to return a fallback message ("Ho translation unavailable") until a model is trained.

## 11. Offline Architecture
Currently proven segments:
Ho ASR (Windows Local)
Android offline ASR is not yet proven for the Ho Wav2Vec2 model due to mobile hardware constraints. Offline translation is currently impossible due to the lack of a trained model.

## 12. Recommended Next Experiment
The smallest safe experiment is to **manually annotate the 5-record pilot** using the established Ho annotation tool. 
- *Goal:* Verify that human annotators can effectively translate the raw Ho ASR into Devanagari Hindi. 
- *Action:* A human Ho speaker should complete the 5 records. This will give us our first 5 ground-truth Ho-Hindi parallel sentences.

## 13. Risks and Blockers
- **Blocker:** Zero parallel data means zero capability to train or evaluate a machine translation model.
- **Risk:** Human annotation is time-consuming and expensive. Scaling from 100 sentences to the required 10,000+ will require a dedicated annotation team.

## 14. Exact Changes That Would Be Required Later
- **Service Router (pp.py / services/translation.py):** Update the translation routing logic to check if source_lang == "ho". If so, route to a mock/fallback response until a model is deployed. 

## 15. Production Safety Audit
- Production FastAPI: UNCHANGED
- Flutter/Android: UNCHANGED
- Ho ASR model: UNCHANGED
- IndicTrans2: UNCHANGED
- .env: UNCHANGED
- Annotation DB: UNCHANGED
- Production datasets: UNCHANGED

## 16. Final Status
**PASS** - The investigation is complete and conclusive. Ho machine translation is blocked purely by a lack of parallel training data, which the annotation tool is now ready to collect.
