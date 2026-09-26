# MatriVaani NMT Dataset Specification

## Current Status: INSUFFICIENT VERIFIED DATA

As of the current Phase 4 audit, the local `datasets/raw/` repository contains **0** verified human-translated Hindi-Santhali parallel pairs. We only have synthetic single-word Santhali ASR audio files from Phase 3.

### Required Dataset Structure
When parallel data is supplied, it must conform to the following schema to be ingested by the MatriVaani pipeline:

```json
{
    "source_language": "hi",
    "target_language": "sat",
    "source": "बच्चों, अपनी किताब खोलो।",
    "target": "ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ, ᱟᱯᱮᱭᱟᱜ ᱯᱚᱛᱚᱵ ᱡᱷᱤᱡᱽ ᱯᱮ᱾"
}
```

### Dataset Statistics (Placeholder)
- **Total Pairs**: 0
- **Unique Source Sentences**: 0
- **Unique Target Sentences**: 0
- **Duplicate Rate**: N/A
- **Source Length Distribution**: N/A
- **Target Length Distribution**: N/A
- **Domains**: Primary Education, FLN, Conversational
- **Educational-domain percentage**: N/A
- **Train/Validation/Test counts**: 0/0/0

### Validation Pipeline Requirements
The upcoming `ai/nmt/` data loaders will enforce the following checks before any model fine-tuning occurs:
1. **Empty Source/Target**: Reject pairs with missing text.
2. **Duplicate Pairs**: Remove identical parallel rows.
3. **Source-Target Mismatch**: Reject if the source and target are completely identical (usually indicates copy-paste errors or untranslated data).
4. **Corrupted Unicode**: Reject invalid UTF-8 sequences.
5. **Language Identification (LID)**: FastText-based heuristic to ensure the source is predominantly Hindi.
6. **Length Filtering**: Reject excessively long sentences (>128 tokens) unsuitable for real-time mobile NMT.
7. **Invalid Characters**: Flag sentences with non-Devanagari (for Hindi) or non-Ol Chiki/Roman (for Santhali) characters for manual review.

**Note**: Unusual Santhali text will be flagged for review, NOT automatically deleted, due to the low-resource nature of the language.

### Versioning
The initial dataset, once populated, will be tagged as **MATRI-NMT-HI-SAT-v0.1**.
