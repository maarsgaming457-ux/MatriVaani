# Data Source Audit

This document tracks legitimate sources for Santhali speech and text datasets.

| Dataset | Task | Language | Size | Script | License | Access | Quality | Usable? |
|---|---|---|---|---|---|---|---|---|
| **COILD-MT-Corpus** | NMT | hi <-> sat | ~20,603 pairs | Unknown | Academic | **UNAVAILABLE** (Gated) | Unknown | **NO** |
| **Mozilla Common Voice v17** | ASR/TTS | sat | ~10 hours | Ol Chiki | CC0 | Requires Account | Variable | Yes (if downloaded manually) |
| **IndicVoices-R** | TTS | sat | Unknown | Ol Chiki | CC-BY-NC 4.0 | **UNAVAILABLE** (Gated) | High | **NO** (Without Token) |
| **AI4Bharat Rasa** | TTS | sat | Unknown | Ol Chiki | CC-BY-NC 4.0 | **UNAVAILABLE** (Gated) | High | **NO** (Without Token) |
| **SraVaani Dataset** | ASR | sat | Unknown | Unknown | Unknown | **UNAVAILABLE** (Gated) | High | **NO** (Without Token) |
| **Manual Curation Tool** | NMT | hi <-> sat | 0 (Starting) | Ol Chiki | Project | Fully Open | TBD (Human Verified) | **YES** |

> [!CAUTION]
> **PHASE 8 DATASET REALITY:**
> While we have an operational Manual Curation Tool and identified Common Voice targets, as of Phase 8 execution, `0` physical data pairs have been acquired or generated. Because fabrication is strictly forbidden, all training gates correctly read `BLOCKED_NO_DATA`.
