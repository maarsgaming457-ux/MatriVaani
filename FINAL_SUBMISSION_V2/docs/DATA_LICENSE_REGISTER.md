# Data License Register

This document tracks the legal restrictions of all datasets investigated for the MatriVaani project.

| Dataset | License | Allowed Use | Training Allowed | Redistribution Allowed | Attribution Required | Restrictions | Source Evidence |
|---|---|---|---|---|---|---|---|
| **Mozilla Common Voice (Santhali)** | CC0 (Public Domain) | Any (Commercial/Research) | **YES** | **YES** | NO (But good practice) | None | Mozilla CV Website |
| **AI4Bharat IndicVoices-R (Santhali)** | CC-BY-NC 4.0 | Research/Non-Commercial | **YES** (Non-Commercial only) | **NO** (Strictly gated behind AIKosh) | YES | Non-Commercial Only, Gated | AI4Bharat AIKosh |
| **COILD-MT-Corpus** | Unknown/Academic | Academic Research Only | **YES** | **NO** (Gated on HF) | YES | Gated behind HF Auth | HuggingFace |
| **MatriVaani Manual Curation** | Custom Open (CC-BY 4.0) | Any | **YES** | **YES** | YES | None | Project Repo |

> [!WARNING]
> **License Blocker Rule**
> If a dataset requires a token to download (like IndicVoices or COILD) and we do not have the token, its physical readiness is `LICENSE_BLOCKED` or `DATA_BLOCKED`. We cannot bypass legal gating.
