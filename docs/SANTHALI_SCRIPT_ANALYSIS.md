# Santhali Script Analysis

## Overview
Santhali is officially recognized in India and is primarily written in three scripts, depending on geography and domain:
1. **Ol Chiki**: The official script of Santhali, created by Pandit Raghunath Murmu. This is the dominant script for education, government, and modern digital text in Jharkhand, Odisha, and West Bengal.
2. **Devanagari**: Historically and commonly used in Bihar and Jharkhand due to the regional prominence of Hindi.
3. **Latin/Roman**: Used in some historical texts, Christian missionary materials, and occasionally by the diaspora.

## MatriVaani Project Decision
### Recommended Primary Script: **Ol Chiki**

**Evidence and Rationale:**
1. **Primary Education Focus**: MatriVaani is an AI tool for *Mother Tongue-Based Primary Education*. State educational boards in Jharkhand and Odisha increasingly mandate Ol Chiki for primary schooling in Santhali.
2. **Foundation Model Support**: The NMT foundation model candidate, AI4Bharat's IndicTrans2, explicitly supports Santhali exclusively via the `sat_Olck` (Ol Chiki) token. Devanagari Santhali requires transliteration layers that degrade translation quality.
3. **Linguistic Purity**: Ol Chiki was designed explicitly for the phonetics of Santhali, whereas Devanagari lacks specific characters for some unique Santhali sounds.

## Handling Multi-Script Data
In Phase 8.5 Data Acquisition, any dataset found in Devanagari or Latin will NOT be automatically discarded, but they must be carefully tagged in the dataset metadata (`script: "Devanagari"`). They will require transliteration to Ol Chiki before entering the NMT pipeline, or they may be used solely for ASR (where audio is script-agnostic, though the transcription targets must eventually match the NMT input script).
