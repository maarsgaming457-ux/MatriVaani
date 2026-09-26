# -*- coding: utf-8 -*-
import json

audit_md = """# MATRI VAANI - REAL DATA AUDIT AND SIMULATION QUARANTINE

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
"""

audit_json = {
  "audit_type": "Real Data vs Simulation Audit",
  "quarantine_location": "data/ho_quarantine/simulated/",
  "real_data_totals": {
    "asr": {
      "real_local_hours": 0.0,
      "real_metadata_utterances": 100,
      "real_speakers": 1,
      "quarantined_simulations": 7250
    },
    "translation": {
      "real_human_ground_truth_pairs": 0,
      "real_synthetic_pairs": 223,
      "quarantined_simulations": 1300
    },
    "tts": {
      "real_hours": 0.0,
      "real_speakers": 0,
      "quarantined_simulations": 750
    }
  },
  "training_gate": {
    "asr": "NOT READY - REAL DATA INSUFFICIENT",
    "translation": "NOT READY - REAL DATA INSUFFICIENT",
    "tts": "NOT READY - REAL DATA INSUFFICIENT"
  },
  "critical_notice": "SIMULATED DATA MUST NOT BE USED AS GROUND TRUTH OR TRAINING DATA."
}

manifest_summary = """# REAL DATA MANIFEST SUMMARY

The following manifests have been rebuilt to include ONLY genuine, physically collected or previously existing (pre-simulation) data.

## 1. ASR Real Manifest
- **File**: data/ho_asr/ho_asr_real_v1_manifest.jsonl
- **Total Records**: 100
- **Source**: project-boli/ho
- **Audio Availability**: External Drive (Missing Locally)
- **Real Local Duration**: 0.0 Hours

## 2. Translation Real Manifest
- **File**: data/ho_translation/ho_translation_real_v1_manifest.jsonl
- **Total Records**: 223
- **HUMAN_GROUND_TRUTH**: 0
- **SYNTHETIC**: 223
- **Source**: experimental_v3_dataset

## 3. TTS Real Manifest
- **File**: data/ho_tts/ho_tts_real_v1_manifest.jsonl
- **Total Records**: 0
- **Real Local Duration**: 0.0 Hours
"""

with open('HO_REAL_DATA_AUDIT.md', 'w', encoding='utf-8') as f: f.write(audit_md)
with open('HO_REAL_DATA_AUDIT.json', 'w', encoding='utf-8') as f: json.dump(audit_json, f, indent=2)
with open('REAL_DATA_MANIFEST_SUMMARY.md', 'w', encoding='utf-8') as f: f.write(manifest_summary)

print("Audit reports created.")
