# -*- coding: utf-8 -*-
import json

md_content = """# MATRI VAANI - HO CANONICAL SCRIPT VALIDATION

## 1. Why Devanagari is appropriate for Ho in MatriVaani
The target users of MatriVaani are Hindi-medium trained primary teachers in Jharkhand's PALASH MTB-MLE programme. Because these teachers already read Devanagari fluently, providing Ho translations and TTS in Devanagari reduces their cognitive load. Using an unfamiliar script (like Warang Citi) would defeat the pedagogical intent of giving them a usable bridge to the tribal language.

## 2. Natural Usage by Native Ho Speakers
In Jharkhand, Devanagari is the primary state script. Most bilingual Ho speakers (who also speak Hindi or Sadri) are literate in Devanagari. While Warang Citi is the cultural/indigenous script for Ho, Devanagari is the pragmatic standard used in government schools and local publications in Jharkhand.

## 3. Existing Dataset/Resource Representations
- **Warang Citi**: Used in cultural preservation, indigenous literature, and Unicode standards, but practically absent from NLP datasets.
- **Devanagari**: Dominant in Jharkhand's state educational materials (including PALASH programme textbooks).
- **Latin**: Used in early missionary texts, linguistic grammars (e.g., Deeney, 1978), and some modern field notes.
- **Odia**: Used heavily in Ho populations residing in Odisha. (This is why facebook/mms-tts-hoc relies on Odia script, as it was trained on religious texts published there).

## 4. Preservation of Linguistic Information
Ho belongs to the Munda language family and contains specific phonological features not native to Indo-Aryan languages, most notably **checked consonants / glottal stops** (k', c', t', p').
- **Issue**: Standard Devanagari lacks dedicated characters for these.
- **Resolution**: To preserve linguistic information, Devanagari Ho employs orthographic conventions, such as appending an apostrophe (') or using halant forms to indicate unreleased checked consonants. As long as a strict orthographic standard is maintained, linguistic preservation is achieved for ASR, Translation, and TTS.

## 5. Unicode Normalization Requirements
- Devanagari Ho must adhere to standard Unicode Normalization (NFC).
- Explicit rules must define how checked consonants are written (e.g., strict use of U+0027 APOSTROPHE vs. standard halants) so that TTS grapheme-to-phoneme (G2P) systems can deterministically trigger the correct glottal stop.

## 6. Tokenization Implications
Using Devanagari provides an immense advantage with BPE/SentencePiece tokenizers. Because models like IndicTrans2 and NLLB have heavily optimized Devanagari vocabularies, Ho words will tokenize efficiently into phonetically meaningful subwords, rather than fracturing into single bytes (which would happen with Warang Citi).

## 7. Hindi/Ho Vocabulary Collision
Because both languages will use Devanagari, there is a risk of vocabulary collision (where a Ho word is identical in spelling to a Hindi word but differs in meaning). However, modern Seq2Seq models handle this easily through context and language tags. The shared script actually aids in zero-shot cross-lingual transfer for loanwords.

## 8. IndicTrans2 / NLLB Compatibility
- **IndicTrans2**: Fully supports Devanagari. While Ho is not explicitly in its training data, the tokenizer will parse Devanagari Ho efficiently.
- **NLLB-200**: Handles Devanagari perfectly.

## 9. Future Ho TTS Models
End-to-end TTS models (like VITS) map characters/phonemes to spectrograms. Training a TTS model on Devanagari Ho is entirely feasible, provided the G2P (Grapheme-to-Phoneme) dictionary explicitly maps the Devanagari checked-consonant conventions to their actual acoustic glottal equivalents.

## 10. ASR Transcript Consistency
ASR transcripts can consistently use Devanagari. Field workers and annotators in Jharkhand are typically bilingual and comfortable transcribing tribal languages using the Hindi alphabet.

## 11. Is there a better canonical representation?
- **Warang Citi** is culturally superior but computationally and pedagogically fatal for our specific target audience (Hindi-medium teachers).
- **Latin** is linguistically excellent for Munda languages but introduces a reading barrier for rural Hindi-medium teachers.
- Therefore, for the specific problem statement of MatriVaani (Jharkhand PALASH program), Devanagari is the optimal choice.

---

## EVIDENCE SEPARATION

### LINGUISTIC EVIDENCE
- Ho features checked vowels/consonants lacking in native Devanagari.
- Modification (apostrophes or halants) is required to prevent phonological loss.

### DATASET EVIDENCE
- Datasets are fragmented across Odia (MMS), Latin (academic), and Devanagari (Jharkhand schools). There is no single dominant NLP script.

### MODEL/TOKENIZER EVIDENCE
- Devanagari is highly optimized in Indic NLP tokenizers. Warang Citi is virtually non-existent in model vocabularies.

### ENGINEERING CONVENIENCE
- Devanagari avoids custom tokenizer training, simplifies Android UI rendering, and ensures compatibility with existing Indic NMT architectures.

---

## FINAL VERDICT

CANONICAL_HO_SCRIPT:
**KEEP DEVANAGARI**

**Reasoning**:
While Devanagari requires strict orthographic rules to handle Ho's glottal stops, it is the only script that perfectly intersects our two hardest constraints:
1. **User Requirement**: The end-users (Hindi-medium teachers in Jharkhand) can read it instantly without learning a new alphabet.
2. **Computational Requirement**: Existing foundation models (IndicTrans2, Whisper, NLLB) already possess rich, robust Devanagari tokenizers. 
Switching to Latin or Warang Citi would solve a minor linguistic inconvenience at the cost of alienating the end-users and destroying tokenizer efficiency.
"""

json_content = {
  "validation_objective": "Canonical Ho Script Selection",
  "selected_script": "Devanagari",
  "evidence_separation": {
    "linguistic": "Requires orthographic conventions (apostrophes/halants) to handle Munda checked consonants/glottal stops.",
    "dataset": "Highly fragmented globally (Latin, Odia, Devanagari, Warang Citi). Devanagari is standard in Jharkhand schools.",
    "model_tokenizer": "Devanagari is highly optimized in IndicTrans2 and NLLB. Warang Citi would cause severe token fragmentation.",
    "engineering": "Simplifies UI rendering, avoids custom BPE training, aligns with Hindi hub."
  },
  "key_findings": {
    "target_user_appropriateness": "Hindi-medium teachers in Jharkhand can read it natively.",
    "linguistic_preservation": "Possible, provided strict grapheme-to-phoneme rules are enforced for checked consonants.",
    "unicode_normalization": "Requires standard NFC and strict conventions for glottal stops.",
    "tokenizer_compatibility": "Excellent. Indic tokenizers support Devanagari natively.",
    "tts_asr_readiness": "Fully feasible with custom G2P mapping."
  },
  "final_verdict": {
    "decision": "KEEP DEVANAGARI",
    "rationale": "It is the only script that satisfies both the pedagogical needs of the end-users (Hindi-medium teachers) and the computational realities of modern Indic NLP tokenizers."
  }
}

with open('HO_CANONICAL_SCRIPT_VALIDATION.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

with open('HO_CANONICAL_SCRIPT_VALIDATION.json', 'w', encoding='utf-8') as f:
    json.dump(json_content, f, indent=2)

print('Validation files created successfully.')
