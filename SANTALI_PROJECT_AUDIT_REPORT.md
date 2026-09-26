# SANTALI PROJECT AUDIT

## 1. Executive Summary
- **Total Santali Files Discovered:** 11333
- **Total Size:** 18120.85 MB
- **Current Status:** Santali training exists for ASR, but the NMT pipeline was explicitly blocked due to data constraints. The ASR model is trained but the backend configuration is currently pointing to a dead Google Drive path instead of the local final model. Flutter UI integration is incomplete/hidden, and TTS is officially unsupported.

## 2. All Santali Files Found
```text
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\MATRIVAANI_SANTALI_DATASET_REPORT.md
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\ai\asr\train_santhali_asr.py
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\evaluation\classroom_santhali\README.md
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\evaluation\classroom_santhali\fln_evaluation_set.json
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\metadata\santali_character_inventory.json
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\metadata\santali_indicvoices_statistics.json
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\metadata\santali_provenance.json
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\raw\audio\synthetic_santhali_000.wav
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\raw\audio\synthetic_santhali_001.wav
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\raw\audio\synthetic_santhali_002.wav
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\raw\audio\synthetic_santhali_003.wav
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\raw\audio\synthetic_santhali_004.wav
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\__pycache__\audio.cpython-314.pyc
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\__pycache__\indicvoices_loader.cpython-314.pyc
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\__pycache__\local_cache_loader.cpython-314.pyc
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\__pycache__\text_normalizer.cpython-314.pyc
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\audio.py
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\dataset_analyzer.py
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\indicvoices_loader.py
C:\study_files\sih project\FINAL_SUBMISSION\SOURCE\data_modules\santali\local_cache_loader.py
... (and many more, documented internally)
```


## 3. Dataset Inventory
- **Path:** `C:\study_files\sih project\datasets\cache\santali` and `FINAL_SUBMISSION_V2\datasets\cache\santali`
- **Source:** `ai4bharat/IndicVoices`
- **Target Script:** Ol Chiki (`sat_Olck`)
- **Status:** Cached locally as lazy `IterableDataset` streams.

## 4. Dataset Statistics
Based on the `SANTALI_ASR_MODEL_CARD.md`:
- **Total Available:** 224,000 samples
- **Pilot Train Split:** 1,000 samples
- **Pilot Validation Split:** 200 samples

## 5. Base Model
- **ASR Base:** `facebook/wav2vec2-base-100k-voxpopuli`
- **NMT Base:** N/A (Training was blocked via `nmt_dataset_report.json`).

## 6. Santali Fine-Tuned Model
- **ASR Final Model:** `C:\study_files\sih project\models\santhali_asr_final`
- **NMT Model:** Does not exist (Training blocked).

## 7. Tokenizer
- **Path:** `C:\study_files\sih project\models\santhali_wav2vec2_processor`
- **Type:** `Wav2Vec2CTCTokenizer` configured for 39-token Ol Chiki CTC vocabulary.

## 8. Training History
- **Pilot Phase:** Trained on CPU due to `< 2 GB` RAM ceiling.
- **Batches:** 16, **Epochs:** 2.5
- **Behavior:** Exhibited CTC blank collapse (100% WER/CER) during pilot due to short training, but structurally valid.
- **NMT Phase:** Aborted gracefully.

## 9. Evaluation Results
- **ASR Zero-Shot:** 100% WER, 141% CER (Hallucinated Latin characters)
- **ASR Pilot:** 100% WER, 100% CER (CTC blank collapse).
- **NMT:** No evaluation possible.

## 10. Best Santali Examples
No successful end-to-end translation or transcription examples exist in the logs due to the CTC blank collapse in the pilot ASR model and the absence of an NMT model.

## 11. Existing Inference Pipeline
- **ASR:** Handled by `app/services/asr_service.py`. It dynamically loads a Santali processor and model. However, `app/core/config.py` hardcodes the path to a Google Drive directory (`/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500`), which breaks local Windows execution.
- **NMT:** Handled by `app/services/translation_service.py`, mapping `Santali` -> `sat_Olck`. Relies on external API because no local model exists.

## 12. Existing FastAPI Integration
- **Endpoint:** `POST /asr`
- **Parameters:** Accepts `language="santali"`.
- **Status:** Implemented but broken due to the Google Drive config path.

## 13. Existing Flutter Integration
- **Status:** Partially implemented.
- **Details:** `classroom_screen.dart` and `translator_screen.dart` (in backups) contained logic for `_targetLang = 'sat'`. However, the current active UI dropdown only exposes Hindi and Mundari.

## 14. Existing TTS
- **Status:** NOT IMPLEMENTED.
- **Details:** `app/frontend/app.py` explicitly issues `st.warning("TTS NOT AVAILABLE (No offline model available for Santhali)")`.

## 15. Existing ASR
- **Status:** IMPLEMENTED BUT INCOMPLETE.
- **Details:** Model exists locally, but config points to the cloud. Model currently suffers from blank collapse.

## 16. Santali vs Mundari Architecture

| Component | Mundari | Santali | Status |
|---|---|---|---|
| Dataset | Yes | Yes (IndicVoices) | |
| Base Model | Yes (IndicTrans2) | Yes (Wav2Vec2) | |
| Fine-Tuned Model | Yes (NMT) | Yes (ASR) | NMT is missing for Santali |
| FastAPI | Working | Broken | Path config issue |
| Flutter UI | Working | Hidden | Code exists but disabled |
| TTS | Working (Sarvam) | Unavailable | |
| ASR | Working (Cloud) | Local Pilot | |

## 17. What Is Already Complete
- Santali Ol Chiki vocabulary mapping.
- Local streaming dataloader infrastructure.
- Local ASR pilot model export (`santhali_asr_final`).
- FastAPI route structure for ASR.

## 18. What Is Missing
- NMT Training (Hindi -> Santali).
- Fixed ASR model paths in FastAPI `config.py`.
- Further ASR training to overcome CTC blank collapse.
- Re-enabling Santali in the Flutter dropdown.
- A functional TTS provider.

## 19. Exact Final Santali Model Path
`C:\study_files\sih project\models\santhali_asr_final`

## 20. Exact Next Steps
STEP 1: Fix `app/core/config.py` to point `ASR_MODEL_PATH` to the local `models/santhali_asr_final` directory.
STEP 2: Re-enable the Santali language option in the Flutter `translator_screen.dart` dropdown.
STEP 3: Configure `translation_service.py` to reliably fallback to the Bhashini API for Hindi->Santali since the local NMT training was blocked.

## 21. Files That MUST NOT Be Modified
`C:\study_files\sih project\backend\best_model_main2\*`

## 22. Final Conclusion
The Santali integration is fundamentally a hybrid WIP. The ASR component was successfully prototyped locally but disconnected from the backend API via a cloud path configuration error. The NMT component was strictly blocked by a quality gate, and the TTS component is definitively unsupported. The most critical immediate step is to fix the ASR config paths and rely on an external API for the translation layer.
