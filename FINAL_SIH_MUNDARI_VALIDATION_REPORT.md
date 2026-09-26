# Hindi → Mundari Validation

## Method

The frozen Hindi→Mundari NMT model was evaluated using:

* Karya Hindi→Mundari corpus
* Mundari dictionary resources
* Mundari grammar resources
* available machine-translation cross-checks
* linguistic analysis

Because a native Mundari reviewer was not available within the project timeline, uncertain translations were NOT falsely labeled as human-verified.

## Results

* **VERIFIED CORRECT**: 2
* **LIKELY CORRECT**: 2
* **LIKELY INCORRECT**: 0
* **INCORRECT**: 1
* **NEEDS NATIVE VALIDATION**: 45
* **NO EVIDENCE FOUND**: 0

## Important Example

**Hindi:**
क्या कर रहे हो?

**Model:**
चिनअःम कमितना।

**Current conclusion:**
LIKELY CORRECT — NEEDS NATIVE VALIDATION

**Explanation:**
- **चिनअः**: Supported by Bharatavani/Mundari lexicon. Meaning: "what".
- **कमितना**: Morphologically sound progressive verb structure. Meaning: "doing".
- **-म**: Valid Mundari pronominal affix for 2nd person singular.
- **Complete Construction**: The entire construction naturally parses to [what]-[you] [doing]. However, because complete conversational questions are absent from the domain-specific Karya corpus, there is no documented exact reference to confirm if this literal mapping represents *natural* tribal usage. Therefore, it requires human validation.

## Limitation

Native-speaker validation was not available within the current project timeline. Therefore, translations without sufficient documentary evidence are explicitly marked as requiring native validation.

## Model Integrity

best_model_main2 was not modified.
