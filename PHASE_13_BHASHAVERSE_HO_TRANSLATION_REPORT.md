# PHASE 13 BHASHAVERSE HO TRANSLATION REPORT

**1. Date/time:** 2026-09-16 17:57:51
**2. Model:** ltrciiith/bhashaverse
**3. Model license:** MIT (from HuggingFace metadata)
**4. Dataset metadata:** ltrciiith/bhashik-parallel-corpora-generic. License: CC-BY-NC-4.0. Contains language:hoc. Access is gated (requires accepting terms on HuggingFace).
**5. Ho language code:** hoc_Wara (inferred from Bhashik tags)
**6. Hindi language code:** hin_Deva
**7. Model language support:** Although hoc appears in dataset tags, Ho is NOT explicitly listed in the language_mapping inside the hf_inference.py script provided by the authors. Language tags (e.g., ###hoc_Wara-to-hin_Deva###) are not explicit monolithic tokens in airseq_dict.json but are dynamically constructed and tokenized into subwords by the SentencePiece model.
**8. Ho→Hindi tests:**
- **Input 1:** "आबु एन हो को नेनता काबु बेटा इचि कोआ"
- **Output 1:** "अबू एन हो को नेन्टा काबू बेटा इचिहोक"
- **Input 2:** "एनको नेनता: काबु बेटा इचि कोआ"
- **Output 2:** "एनकोआरा नेन्टाः काबू बेटा इची कोआ"
**9. Hindi→Ho tests:**
- **Input 1:** "नमस्ते बच्चों, आज हम गिनती सीखेंगे।"
- **Output 1:** "नमस्कार kids#ara, आज हामी countoc सीखू।"
- **Input 2:** "यह एक किताब है।"
- **Output 2:** "It 's a bookwachara."
- **Input 3:** "यह लाल गेंद है।"
- **Output 3:** "It 's red#hoc ballawara."
- **Input 4:** "बच्चे स्कूल जा रहे हैं।"
- **Output 4:** "बच्च#hoc school."
**10. Exact outputs:** Recorded above. The outputs consist of source-copying and English/Nepali code-mixing with random subwords like #ara, wachara, and #hoc.
**11. Latencies:** 
- Ho→Hindi: ~3.3 - 3.5 seconds per sentence (CPU)
- Hindi→Ho: ~2.2 - 3.9 seconds per sentence (CPU)
**12. Failure analysis:**
- **Ho→Hindi:** Fails via Copying source (Category B). Because the Ho text is written in Devanagari script, the model simply regurgitated the source text with minor orthographic tweaks.
- **Hindi→Ho:** Fails via Wrong language & Garbage (Category D & E). The model generates English and Nepali mixed with bizarre suffixes (e.g., ookwachara).
**13. Independent lexical validation:** Fails immediately. The output does not resemble Ho vocabulary from any known dictionary (e.g., Digital Ho Dictionary).
**14. Dataset access status:** Gated on Hugging Face; requires accepting research terms.
**15. Human validation status:** Fails; completely unusable output.
**16. CPU/GPU:** Tested on CPU.
**17. RAM:** ~4.4 GB memory required for inference.
**18. Model size:** ~4.4 GB on disk, 1.1B parameters.
**19. Backend experimental status:** Due to absolute translation failure, the /translate-experimental endpoint and HoBhashaVerseProvider have NOT been created.
**20. Quality-gate result:** FAILED. 
**21. Whether Ho translation can proceed to product integration:** NO. Zero-shot BhashaVerse inference for Ho is totally non-functional.

**BHASHAVERSE HO TRANSLATION EXPERIMENT FAILED**
