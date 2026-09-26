# Phase 36A: Hindi -> Ho Translation Foundation Implementation Plan

## Goal
Build the first complete experimental Hindi -> Ho translation capability safely, using actual verified Ho resources without fabricating capabilities, transliterating, or contaminating with Santali/Mundari.

## Proposed Changes

### 1. Audit Resources & Build Inventories
- **Lexicon** (data/ho_hindi/experimental/hindi_to_ho/HINDI_TO_HO_LEXICON.json): Will parse ipil_discovered_entries.json and ho_translation_map.json to build a clean Hindi-to-Ho dictionary, dropping unsupported or hallucinated terms.
- **Grammar** (HO_GRAMMAR_RULES.json): Reversing the analysis in ho_translation_map.json (e.g., Pronoun + Object + -te [locative] + Verb) to formulate rules for Hindi-to-Ho construction.
- **Templates** (HO_TEMPLATES.json): Identifying reusable structural templates from the 100-sentence mappings.

### 2. Experimental Translator Service
- Modify pp/services/experimental_ho_translation/translation_service.py (or create a dedicated module internally) to add 	ranslate_hindi_to_ho(text: str).
- **Pipeline Stages**:
  1. **Exact Match**: Reverse mapping of ho_translation_map.json.
  2. **Lexical/Grammar Transformation**: Rule-based construction if Hindi exactly matches a known template (e.g. Subject + Location + Motion Verb).
  3. **Resource-Assisted AI Fallback**: Using the same Gemini fallback but injected with the newly built Lexicon and Grammar rules, explicitly instructed NOT to transliterate or use Santali/Mundari.
  4. **Controlled Fallback**: When confidence is too low or resources don't exist.

### 3. Testing
- Develop script scripts/phase36a_hindi_to_ho_eval.py to evaluate the 5 test categories.
- Language Contamination Check: Scan AI outputs for common Santali words, Devanagari transliteration of the Hindi input, or unknown stems.
- Round-trip evaluation against existing Ho->Hindi.

### 4. API Endpoints
- Add POST /experimental/translate/hi-ho to pp/api/endpoints/experimental.py.
- Response format matching the specification exactly.

## User Review Required
No backend production models (IndicTrans2/Sarvam/ASR) are being changed. This operates purely on the experimental endpoint level.

Please review this implementation plan and let me know if I may proceed with building the Hindi -> Ho pipeline!
