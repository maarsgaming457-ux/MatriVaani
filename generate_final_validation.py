import pandas as pd
import codecs
import sys
import os

# Set encoding to avoid print crashes on Windows
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())

# 1. Load data
prev_results_path = 'COMMON_SENTENCE_VERIFICATION_RESULTS.csv'
if not os.path.exists(prev_results_path):
    print(f"Error: {prev_results_path} not found.")
    sys.exit(1)

df = pd.read_csv(prev_results_path)

# Prepare DataFrames
human_csv_rows = []
adivaani_csv_rows = []
adivaani_text_lines = []

for idx, row in df.iterrows():
    h_id = row['id']
    hindi = row['hindi_source']
    our_pred = row['model_prediction']
    
    # Karya / Dictionary / Grammar
    karya_ref = ""
    if pd.notna(row['exact_karya_match']) and row['exact_karya_match'] != 'Not found':
        karya_ref = f"Exact Match: {row['exact_karya_match']}"
    elif pd.notna(row['closest_karya_match']) and row['closest_karya_match'] != 'Not found':
        karya_ref = f"Closest Match: {row['closest_karya_match']}"
        
    dict_ev = row['dictionary_evidence'] if pd.notna(row['dictionary_evidence']) else ""
    gram_ev = row['grammar_evidence'] if pd.notna(row['grammar_evidence']) else ""
    status = row['status']
    
    ev_summary = ""
    if karya_ref: ev_summary += f"Karya: {karya_ref}\n"
    if dict_ev: ev_summary += f"Dict: {dict_ev}\n"
    
    human_csv_rows.append({
        'id': h_id,
        'category': row['category'],
        'hindi_sentence': hindi,
        'our_model_translation': our_pred,
        'karya_reference': karya_ref,
        'adivaani_translation': '',  # To be filled manually
        'dictionary_evidence': dict_ev,
        'grammar_evidence': gram_ev,
        'current_status': status,
        'evidence_summary': ev_summary.strip(),
        'human_decision': '',
        'human_corrected_translation': '',
        'human_notes': ''
    })
    
    adivaani_csv_rows.append({
        'id': h_id,
        'hindi_sentence': hindi,
        'target_language': 'Mundari',
        'adivaani_output': '',
        'notes': ''
    })
    
    adivaani_text_lines.append(f"{idx+1}. {hindi}")

# Write FINAL_MUNDARI_HUMAN_VALIDATION.csv
human_df = pd.DataFrame(human_csv_rows)
human_df.to_csv('FINAL_MUNDARI_HUMAN_VALIDATION.csv', index=False, encoding='utf-8')

# Write ADIVAANI_MANUAL_CHECK files
pd.DataFrame(adivaani_csv_rows).to_csv('ADIVAANI_MANUAL_CHECK.csv', index=False, encoding='utf-8')
with open('ADIVAANI_MANUAL_CHECK.txt', 'w', encoding='utf-8') as f:
    f.write("\n".join(adivaani_text_lines))

# Create Excel with Data Validation using openpyxl or xlsxwriter
import xlsxwriter

workbook = xlsxwriter.Workbook('FINAL_MUNDARI_HUMAN_VALIDATION.xlsx')
worksheet = workbook.add_worksheet('Validation')

# Formats
header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
cell_format = workbook.add_format({'border': 1, 'text_wrap': True, 'valign': 'top'})

headers = ['No.', 'Hindi', 'Our Mundari', 'Reference/Comparison', 'Human Decision', 'Correct Mundari (if needed)', 'Notes']
for col_num, header in enumerate(headers):
    worksheet.write(0, col_num, header, header_format)

# Column widths
worksheet.set_column('A:A', 5)
worksheet.set_column('B:B', 25)
worksheet.set_column('C:C', 30)
worksheet.set_column('D:D', 40)
worksheet.set_column('E:E', 25)
worksheet.set_column('F:F', 30)
worksheet.set_column('G:G', 30)

for row_num, r in enumerate(human_csv_rows, start=1):
    worksheet.write(row_num, 0, row_num, cell_format)
    worksheet.write(row_num, 1, r['hindi_sentence'], cell_format)
    worksheet.write(row_num, 2, r['our_model_translation'], cell_format)
    worksheet.write(row_num, 3, r['evidence_summary'], cell_format)
    worksheet.write(row_num, 4, '', cell_format)
    worksheet.write(row_num, 5, '', cell_format)
    worksheet.write(row_num, 6, '', cell_format)

# Add data validation to "Human Decision" column (Column E)
worksheet.data_validation(1, 4, len(human_csv_rows), 4, {
    'validate': 'list',
    'source': ['CORRECT', 'INCORRECT', 'CORRECT_WITH_VARIATION', 'UNCERTAIN'],
    'input_message': 'Select a validation status',
    'error_message': 'Value must be selected from the dropdown.'
})

workbook.close()

# Write MUNDARI_VALIDATOR_INSTRUCTIONS.md
with open('MUNDARI_VALIDATOR_INSTRUCTIONS.md', 'w', encoding='utf-8') as f:
    f.write("""You are reviewing Hindi → Mundari translations for a college AI project.

For each sentence:

1. Read the Hindi sentence.
2. Read the proposed Mundari translation.
3. Decide whether the Mundari sentence naturally conveys the same meaning.
4. Mark CORRECT if it is natural and correct.
5. Mark INCORRECT if it does not convey the intended meaning.
6. Mark CORRECT_WITH_VARIATION if the sentence is correct but you would naturally say it differently.
7. Mark UNCERTAIN if you are not sure.
8. If incorrect or you prefer another natural form, write the corrected Mundari sentence.
9. Do not judge based on whether the sentence looks similar to Hindi.
10. Judge according to natural Mundari usage.
""")

# Write FINAL_MUNDARI_VALIDATION_REPORT.md
report_content = f"""# 1. Executive Summary

- **Total sentences:** 50
- **Verified correct:** {(df['status'] == 'VERIFIED CORRECT').sum()}
- **Likely correct:** {(df['status'] == 'LIKELY CORRECT').sum()}
- **Likely incorrect:** {(df['status'] == 'LIKELY INCORRECT').sum()}
- **Incorrect:** {(df['status'] == 'INCORRECT').sum()}
- **Needs human validation:** {(df['status'] == 'NEEDS NATIVE VALIDATION').sum()}

# 2. External Sources

- **Karya Hindi-Mundari Corpus**
  - **Organization:** Karya Inc.
  - **Language:** Mundari (unr)
  - **URL:** https://github.com/karya-inc/dataset-hindi-mundari-translation
  - **Purpose:** Primary authoritative corpus for exact sentence matches and related structures.
  - **Limitations:** Extremely domain-specific. Lacks everyday conversational target sentences.

- **AdiVaani Platform**
  - **Organization:** Ministry of Tribal Affairs (Govt. of India)
  - **Language:** Mundari (unr)
  - **URL:** https://adivaani.tribal.gov.in/
  - **Purpose:** Cross-reference machine translations as supplementary evidence.
  - **Limitations:** Cannot be safely queried automatically without manual authentication/browser interaction. Thus, a manual review package has been provided. Machine outputs are not ground-truth.

- **Bharatavani Dictionary**
  - **Organization:** CIIL
  - **Language:** Mundari (unr)
  - **URL:** https://bharatavani.in/mundari/dictionaries
  - **Purpose:** Verification of isolated lexical mapping.
  - **Limitations:** Word-to-word dictionary lookup does not prove full grammatical sentence structure validity.

# 3. Sentence Results

"""

for idx, row in df.iterrows():
    report_content += f"### {idx+1}. {row['hindi_source']}\n"
    report_content += f"- **Our Model:** {row['model_prediction']}\n"
    k_match = row['exact_karya_match'] if pd.notna(row['exact_karya_match']) and row['exact_karya_match'] != 'Not found' else (row['closest_karya_match'] if pd.notna(row['closest_karya_match']) and row['closest_karya_match'] != 'Not found' else 'None found')
    report_content += f"- **Karya Match:** {k_match}\n"
    report_content += f"- **AdiVaani Output:** Manual verification required.\n"
    report_content += f"- **Current Status:** {row['status']}\n\n"

report_content += """
# 4. Special Investigation

## क्या कर रहे हो? → चिनअःम कमितना।

- **A. चिनअः**: Supported by Bharatavani/Mundari lexicon. Meaning: "what".
- **B. कमितना**: Morphologically sound progressive verb structure. Root *kami* (work/do), suffix *-tana* (progressive). Meaning: "doing".
- **C. -म**: Valid Mundari pronominal affix for 2nd person singular. 
- **D. COMPLETE CONSTRUCTION**: The structure parses correctly as `[what]-[you] [doing]`. However, due to the complete lack of a verified exact match in the Karya corpus for conversational questions, we cannot guarantee natural phrasing without native speaker signoff.
- **Current status**: LIKELY CORRECT — NEEDS NATIVE VALIDATION.

# 5. Human Validation

Final linguistic validation explicitly requires a qualified/native Mundari reviewer. Machine-generated dictionary/grammar lookups, while indicating high plausibility, cannot officially declare a synthesized sentence as "correct". The reviewer can simply use `FINAL_MUNDARI_HUMAN_VALIDATION.xlsx` with dropdown support to officially greenlight these sentences.

# 6. Model Integrity

- **Path:** `C:\\study_files\\sih project\\backend\\best_model_main2`
- **Integrity Status:** UNCHANGED. `model.safetensors` cryptographically matches `D3B7536F64B42EE7EA5F6D48F0D87461B3398ACBD3B84D5B8A233370812986B5`.

"""

with open('FINAL_MUNDARI_VALIDATION_REPORT.md', 'w', encoding='utf-8') as f:
    f.write(report_content)

print("Workflow files generated successfully.")
