# MATRI VAANI - REAL DATA AUDIT AND SIMULATION QUARANTINE

## 1. OBJECTIVE
This audit strictly separates genuine, physically collected or independently verified Ho data from the simulated artifacts generated during the HO-DATA-2 and HO-DATA-3 pilot/scaling tests. **SIMULATED DATA MUST NOT BE USED AS GROUND TRUTH OR TRAINING DATA.**

## 2. QUARANTINE ACTIONS
All simulated records have been logically isolated into data/ho_quarantine/simulated/. These include:
- data/ho_asr/collection_v1 & 2
- data/ho_translation/collection_v1 & 2
- data/ho_tts/collection_v1 & 2
They will not appear in the training-ready manifests.

## 3. REAL ASR AUDIT
- **Real Native Recordings (Local)**: 0 hours
- **Real Native Recordings (External Metadata)**: 100 utterances (from project-boli/ho)
- **Simulated Recordings Quarantined**: 7,250
- **Audio Validation**: The 100 real utterances point to /content/drive/.... They do not exist locally as physical WAV files in this repository.
- **Result**: The real ASR dataset contains 0 hours of locally verified audio.

## 4. REAL TRANSLATION AUDIT
- **Real Human-Ground-Truth Pairs**: 0
- **Real Synthetic / AI-Generated / Resource-Supported Pairs**: 223 (Derived from the experimental v3 dataset, explicitly downgraded to SYNTHETIC status)
- **Simulated Pairs Quarantined**: 1,300
- **Result**: The real Translation dataset contains 0 human-verified pairs.

## 5. REAL TTS AUDIT
- **Real Native Recordings**: 0 hours
- **Simulated Recordings Quarantined**: 750
- **Result**: The real TTS dataset contains 0 hours of audio.

## 6. TRAINING GATE (REAL DATA ONLY)
Based **strictly on real data**:
- **ASR**: **NOT READY - REAL DATA INSUFFICIENT** (0 local hours, 100 external metadata records)
- **TRANSLATION**: **NOT READY - REAL DATA INSUFFICIENT** (0 Human Ground Truth pairs)
- **TTS**: **NOT READY - REAL DATA INSUFFICIENT** (0 hours)

**Important Notice**: The previous classifications of "READY FOR BASELINE TRAINING" were based on simulated volumes designed to test the architectural pipeline. The physical reality is that we possess zero native Ho recordings locally and zero native-verified sentence pairs. Actual human data collection must occur before any model training can begin.
