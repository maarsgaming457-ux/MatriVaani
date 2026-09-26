# MATRIVAANI - PHASE 8.5-A REPORT
## REAL SANTALI DATA ACCESS VERIFICATION (SUCCESS)

### 1. Objective
Verify actual programmatic retrieval of real Santali speech data from `ai4bharat/IndicVoices` on Windows without triggering native audio codec crashes or loading the entire dataset into RAM.

### 2. The Bottleneck
The previous pipeline iterations were failing due to two core issues:
1. `torchcodec` attempting to eagerly initialize native C++ FFmpeg libraries on Windows, causing `FileNotFoundError` inside `ctypes.CDLL`. This crashed the pipeline completely when `datasets` tried to load the audio decoder.
2. `sys.modules` shadowing: The local directory `datasets` conflicted with the official HF `datasets` library, breaking `pytest` collection and causing silent import failures across the repository.

### 3. Resolution
1. **Audio Decoder Bypass:** We used `ds = ds.cast_column("audio_filepath", datasets.Audio(decode=False))` to force the dataset loader to download the raw audio bytes without attempting to decode them via `torchcodec`. This successfully decoupled the download stream from the decoder constraints.
2. **Namespace Correction:** We renamed the local `datasets` directory to `data_modules` to permanently resolve the namespace shadowing. All `tests/` and `scripts/` were updated to reflect this architectural fix, and `pytest` now passes 100% (23/23 tests).
3. **Split Correction:** The validation split string was corrected from `"validation"` to `"valid"` per the `IndicVoices` HF configuration.

### 4. Data Extraction Results (First 5 Samples)
#### Train Split (`"train"`)
- **Sample 1:** `duration=8.02s`, Script: Ol Chiki
- **Sample 2:** `duration=1.498s`, Script: Ol Chiki
- **Sample 3:** `duration=2.474s`, Script: Ol Chiki
- **Sample 4:** `duration=1.813s`, Script: Ol Chiki
- **Sample 5:** `duration=1.638s`, Script: Ol Chiki

#### Validation Split (`"valid"`)
- **Sample 1:** `duration=11.898s`, Script: Ol Chiki
- **Sample 2:** `duration=14.188s`, Script: Ol Chiki
- **Sample 3:** `duration=7.038s`, Script: Ol Chiki
- **Sample 4:** `duration=15.275s`, Script: Ol Chiki
- **Sample 5:** `duration=5.284s`, Script: Ol Chiki

**All 10 samples successfully verified as using the native Ol Chiki script (U+1C50 - U+1C7F).**

### 5. Memory Verification
- **Baseline RAM:** 141.50 MB
- **Peak RAM:** 1042.43 MB
The peak RAM usage stabilized at ~1 GB during streaming, definitively proving that the full ~224k dataset is **NOT** being downloaded into memory, adhering to the 2 GB strict RAM target.

### 6. Next Steps
Phase 8.5-A is complete. We now have real, validated programmatic access to the `IndicVoices` Santali dataset stream. The raw bytes can now be explicitly decoded using a pure-Python or pre-compiled Windows wheel (e.g., `soundfile` or `scipy.io.wavfile`) in the MatriVaani processing pipeline before being fed to `wav2vec2`.
