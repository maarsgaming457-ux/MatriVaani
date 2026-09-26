import pandas as pd
import codecs
import sys

# Set encoding
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# 1. Load results
df = pd.read_csv('COMMON_SENTENCE_VERIFICATION_RESULTS.csv')

# 2. Create FINAL_DEMO_TRANSLATION_VALIDATION.csv
demo_rows = []
for idx, row in df.iterrows():
    ev_source = ""
    if pd.notna(row['exact_karya_match']) and row['exact_karya_match'] != 'Not found':
        ev_source = "Karya Corpus"
    elif pd.notna(row['closest_karya_match']) and row['closest_karya_match'] != 'Not found':
        ev_source = "Karya Corpus (Similar)"
    elif pd.notna(row['dictionary_evidence']) and row['dictionary_evidence'] != 'Not found':
        ev_source = "Dictionary/Grammar"
    else:
        ev_source = "None"
        
    demo_rows.append({
        'No.': idx + 1,
        'Hindi': row['hindi_source'],
        'Model Mundari': row['model_prediction'],
        'Evidence Status': row['status'],
        'Evidence Source': ev_source,
        'Confidence': row['confidence'],
        'Human Validation Status': 'NOT AVAILABLE',
        'Notes': row['notes'] if pd.notna(row['notes']) else ""
    })

demo_df = pd.DataFrame(demo_rows)
demo_df.to_csv('FINAL_DEMO_TRANSLATION_VALIDATION.csv', index=False, encoding='utf-8')

# Calculate counts
v_correct = (df['status'] == 'VERIFIED CORRECT').sum()
l_correct = (df['status'] == 'LIKELY CORRECT').sum()
l_incorrect = (df['status'] == 'LIKELY INCORRECT').sum()
incorrect = (df['status'] == 'INCORRECT').sum()
n_validation = (df['status'] == 'NEEDS NATIVE VALIDATION').sum()
no_evidence = (df['status'] == 'NO EVIDENCE FOUND').sum()

# 3. Create FINAL_SIH_MUNDARI_VALIDATION_REPORT.md
sih_report = f"""# Hindi → Mundari Validation

## Method

The frozen Hindi→Mundari NMT model was evaluated using:

* Karya Hindi→Mundari corpus
* Mundari dictionary resources
* Mundari grammar resources
* available machine-translation cross-checks
* linguistic analysis

Because a native Mundari reviewer was not available within the project timeline, uncertain translations were NOT falsely labeled as human-verified.

## Results

* **VERIFIED CORRECT**: {v_correct}
* **LIKELY CORRECT**: {l_correct}
* **LIKELY INCORRECT**: {l_incorrect}
* **INCORRECT**: {incorrect}
* **NEEDS NATIVE VALIDATION**: {n_validation}
* **NO EVIDENCE FOUND**: {no_evidence}

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
"""
with open('FINAL_SIH_MUNDARI_VALIDATION_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(sih_report)

# 4. Create SIH_TRANSLATION_VALIDATION_SUMMARY.txt
summary_txt = """Model:
Hindi → Mundari NMT

Evaluation:
50 common Hindi sentences

Evidence:
Karya corpus + Mundari lexical/grammar resources + available machine cross-checks

Human validation:
Not available within current project timeline

Important:
Uncertain translations were not falsely labeled as verified.

Example:
क्या कर रहे हो?
→ चिनअःम कमितना।
→ Likely correct; native validation required.

Model:
Frozen and unchanged.
"""
with open('SIH_TRANSLATION_VALIDATION_SUMMARY.txt', 'w', encoding='utf-8') as f:
    f.write(summary_txt)

print("Final presentation files generated.")
