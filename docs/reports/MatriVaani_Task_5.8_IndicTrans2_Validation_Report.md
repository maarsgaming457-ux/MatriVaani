# MatriVaani — Task 5.8 IndicTrans2 Validation Report

**Status:** CONDITIONAL PASS  
**Model:** i4bharat/indictrans2-indic-indic-dist-320M  
**Purpose:** Evaluate IndicTrans2 as a replacement candidate for the current Groq translation backend.  
**Next step:** Task 6 — IndicTrans2 backend integration, after review and approval of this report.  

---

## 1. Colab Environment

The validation was executed in a real Google Colab environment to ensure isolated testing without modifying the production Windows host.

- **Python:** 3.13.15
- **PyTorch:** 2.11.0+cu128
- **CUDA:** True
- **GPU:** Tesla T4
- **IndicTransToolkit:** IndicProcessor loaded successfully

## 2. Hugging Face Authentication

- Hugging Face authentication was initially rejected with an invalid token.
- A new Read token was created and stored securely in Google Colab Secrets as HF_TOKEN.
- Authentication was then verified successfully using whoami():
  - Token loaded: True
  - Token length: 37
  - Authentication successful
  - Account: Sumit-Patel123
- The gated model access was subsequently successful.

## 3. Model

- **Model:** i4bharat/indictrans2-indic-indic-dist-320M
- **Language mapping:**
  - Hindi: hin_Deva
  - Santali: sat_Olck
- The tokenizer and model were successfully downloaded.
- **Downloaded model.safetensors:** approximately 1.28 GB
- Model loaded successfully on **Tesla T4 GPU**.

## 4. Toolkit Installation

- The initially installed IndicTransToolkit version caused: ModuleNotFoundError: No module named \'IndicTransToolkit.processor\'.
- The toolkit was then removed and installed from the official source repository using editable installation.
- After restarting the Colab runtime, rom IndicTransToolkit import IndicProcessor loaded successfully.
- IndicProcessor(inference=True) initialized successfully.

## 5. Hindi → Santali Results

**H1**  
- Hindi: मैं संथाली में बोलता हूँ।  
- Santali: ᱤᱧ ᱥᱟᱱᱛᱷᱟᱞᱤ ᱨᱮ ᱠᱟᱛᱷᱟ ᱞᱟᱹᱭ ᱮᱫᱟ ᱾  

**H2**  
- Hindi: आप कैसे हैं?  
- Santali: ᱟᱢ ᱪᱮᱫ ᱞᱮᱠᱟ?  

**H3**  
- Hindi: मेरा नाम सुमित है।  
- Santali: ᱤᱧᱟᱹᱜ ᱧᱩᱛᱩᱢ ᱦᱩᱭᱩᱜ ᱠᱟᱱᱟ ᱥᱩᱢᱤᱛ ᱾  

**H4**  
- Hindi: आज मौसम बहुत अच्छा है।  
- Santali: ᱛᱮᱦᱮᱧ ᱦᱚᱭᱦᱩᱫᱤᱥ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱠᱟᱱᱟ ᱾  

**H5**  
- Hindi: कृपया दरवाजा बंद कर दीजिए।  
- Santali: ᱫᱟᱭᱟ ᱠᱟᱛᱮ ᱫᱟᱹᱨᱟᱹ ᱫᱚ ᱵᱚᱱᱚᱫᱚᱞ ᱢᱮ ᱾  

**H6**  
- Hindi: मैं अपने परिवार के साथ गाँव में रहता हूँ।  
- Santali: ᱤᱧ ᱤᱧᱟᱹᱜ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱥᱟᱶᱛᱮ ᱟᱛᱳ ᱨᱮ ᱛᱟᱦᱮᱸᱱᱟ ᱾  

**H7**  
- Hindi: कल हम स्कूल जाएंगे।  
- Santali: ᱦᱚᱭᱦᱩᱫᱮ ᱤᱧᱟᱹᱜ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱪᱟᱞᱟᱣ ᱦᱩᱭᱩᱜᱼᱟ ᱾  

**H8**  
- Hindi: बच्चे मैदान में खेल रहे हैं।  
- Santali: ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱠᱷᱮᱞᱳᱰ ᱴᱷᱟᱶ ᱨᱮ ᱠᱷᱮᱞᱳᱰ ᱟᱠᱟᱫᱟᱭ ᱾  

**H9**  
- Hindi: मुझे पानी चाहिए।  
- Santali: ᱤᱧ ᱫᱟᱜ ᱠᱷᱚᱡ ᱠᱟᱱᱟ ᱾  

**H10**  
- Hindi: यह किताब बहुत अच्छी है।  
- Santali: ᱱᱚᱶᱟ ᱯᱚᱛᱚᱵ ᱫᱚ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱠᱟᱱᱟ ᱾  

## 6. Santali → Hindi Results

**S1**  
- ᱤᱧ ᱫᱚ ᱥᱟᱱᱛᱟᱲᱤ ᱛᱮᱧ ᱨᱚᱲᱟ᱾  
- → मैं काली मिर्च के बारे में बात करता हूँ। *(Semantic failure)*

**S2**  
- ᱟᱢ ᱪᱮᱫ ᱞᱮᱠᱟ?  
- → आप कैसे हैं?  

**S3**  
- ᱤᱧᱟᱹᱜ ᱧᱩᱛᱩᱢ ᱥᱩᱢᱤᱛ ᱾  
- → मेरा नाम सुमित है।  

**S4**  
- ᱟᱢ ᱠᱟᱹᱣᱟ ᱨᱮ ᱥᱮᱱᱚᱜ ᱠᱟᱱᱟ?  
- → आप कहाँ जा रहे हैं?  

**S5**  
- ᱤᱧ ᱫᱟᱜ ᱠᱷᱚᱡ ᱠᱟᱱᱟ ᱾  
- → मुझे पानी चाहिए।  

**S6**  
- ᱱᱚᱶᱟ ᱯᱚᱛᱚᱵ ᱫᱚ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱠᱟᱱᱟ ᱾  
- → यह पुस्तक बहुत अच्छी है।  

**S7**  
- ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱠᱷᱮᱞᱳᱰ ᱴᱷᱟᱶ ᱨᱮ ᱠᱷᱮᱞᱳᱰ ᱟᱠᱟᱫᱟᱭ ᱾  
- → बच्चे खेल के मैदान में खेल रहे हैं।  

**S8**  
- ᱦᱚᱭᱦᱩᱫᱮ ᱤᱧᱟᱹᱜ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱪᱟᱞᱟᱣ ᱦᱩᱭᱩᱜᱼᱟ ᱾  
- → कल हमें स्कूल जाना होगा।  

**S9**  
- ᱤᱧ ᱤᱧᱟᱹᱜ ᱜᱷᱟᱨᱚᱸᱡᱽ ᱥᱟᱶᱛᱮ ᱟᱛᱳ ᱨᱮ ᱛᱟᱦᱮᱸᱱᱟ ᱾  
- → मैं अपने परिवार के साथ गाँव में रहता हूँ।  

**S10**  
- ᱫᱟᱭᱟ ᱠᱟᱛᱮ ᱫᱟᱹᱨᱟᱹ ᱫᱚ ᱵᱚᱱᱚᱫᱚᱞ ᱢᱮ ᱾  
- → कृपया दरवाजा बंद कर दें।  

## 7. Special Case Results

**SP1**  
- मेरी कक्षा में 25 विद्यार्थी हैं।  
- → ᱤᱧᱟᱹᱜ ᱛᱷᱚᱱᱚᱛ ᱨᱮ 25 ᱦᱚᱲ ᱥᱮᱪᱮᱫᱤᱭᱟᱹ ᱢᱮᱱᱟᱜ ᱠᱚᱣᱟ ᱾  

**SP2**  
- आज सुबह 10 बजे स्कूल जाना है।  
- → ᱛᱮᱦᱮᱧ सुबह 10 ᱴᱟᱲᱟᱝ ᱨᱮ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱪᱟᱞᱟᱣ ᱦᱩᱭᱩᱜ ᱠᱟᱱᱟ ᱾ *(Devanagari leakage issue)*

**SP3**  
- सुमित और राहुल स्कूल जा रहे हैं।  
- → ᱥᱩᱢᱤᱛ ᱟᱨ ᱨᱟᱡᱩᱞ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱨᱮ ᱪᱟᱞᱟᱣᱚᱜ ᱠᱟᱱᱟ ᱾  

**SP4**  
- क्या आप मेरी मदद कर सकते हैं?  
- → ᱟᱢ ᱠᱤ ᱤᱧ ᱜᱚᱲᱚ ᱮᱢ ᱫᱟᱲᱮᱭᱟᱜᱼᱟ?  

**SP5**  
- धन्यवाद!  
- → ᱥᱟᱨᱦᱟᱶ ᱮᱢ ᱢᱮ ᱾  

## 8. Round-Trip Results

**RT1**  
- Original: मेरा नाम सुमित है।  
- Santali: ᱤᱧᱟᱹᱜ ᱧᱩᱛᱩᱢ ᱦᱩᱭᱩᱜ ᱠᱟᱱᱟ ᱥᱩᱢᱤᱛ ᱾  
- Back: मेरा नाम सुमित है।  
- **Exact match:** True  

**RT2**  
- Original: आप कैसे हैं?  
- Santali: ᱟᱢ ᱪᱮᱫ ᱞᱮᱠᱟ?  
- Back: आप कैसे हैं?  
- **Exact match:** True  

**RT3**  
- Original: मुझे पानी चाहिए।  
- Santali: ᱤᱧ ᱫᱟᱜ ᱠᱷᱚᱡ ᱠᱟᱱᱟ ᱾  
- Back: मुझे पानी चाहिए।  
- **Exact match:** True  

**RT4**  
- Original: यह किताब बहुत अच्छी है।  
- Santali: ᱱᱚᱶᱟ ᱯᱚᱛᱚᱵ ᱫᱚ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱠᱟᱱᱟ ᱾  
- Back: यह पुस्तक बहुत अच्छी है।  
- **Exact match:** False *(Semantic meaning preserved)*  

**RT5**  
- Original: बच्चे मैदान में खेल रहे हैं।  
- Santali: ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱠᱷᱮᱞᱳᱰ ᱴᱷᱟᱶ ᱨᱮ ᱠᱷᱮᱞᱳᱰ ᱟᱠᱟᱫᱟᱭ ᱾  
- Back: बच्चे खेल के मैदान में खेल रहे हैं।  
- **Exact match:** False *(Semantic meaning preserved)*  

## 9. Performance

**Final performance suite on Tesla T4 GPU:**
- **Average inference:** 0.167 sec
- **Fastest:** 0.138 sec
- **Slowest:** 0.223 sec

## 10. Groq Comparison

**Previous real Groq Task 5.6 validation (openai/gpt-oss-120b):**
- Hindi → Santali: 0/10 passed
- Santali → Hindi: 0/9 passed, 1 uncertain
- Special cases: 0/5 passed
- Round-trip: 0/3 passed
- **Overall Groq translation quality was classified as:** NOT USABLE

IndicTrans2 is substantially better based on the observed validation samples. However, we DO NOT claim statistically proven superiority or production readiness from this small test suite alone.

## 11. Known Failures

1. **S1 is a clear semantic failure.**
   - Input: ᱤᱧ ᱫᱚ ᱥᱟᱱᱛᱟᱲᱤ ᱛᱮᱧ ᱨᱚᱲᱟ᱾
   - Output: मैं काली मिर्च के बारे में बात करता हूँ।
   - This is unrelated to the intended meaning and must be treated as a translation error.
2. **SP2 has Devanagari leakage in the Santali output.**
   - Output: ᱛᱮᱦᱮᱧ सुबह 10 ...
   - The target is supposed to be purely Santali/Ol Chiki, so this is a quality issue.
3. **RT4 and RT5 are not exact string matches.**
   - किताब → पुस्तक, मैदान → खेल के मैदान.
   - Note: These preserve general meaning and are not semantic failures, despite Exact match=False.
4. **Validation limits.** The validation dataset is small and manually inspected. Native Santali-speaker evaluation was NOT performed during this Colab validation. Therefore, this report does NOT claim 100% translation accuracy, production-ready translation natively, complete correctness of all H1-H10 tests, or statistically validated superiority.

## 12. Final Decision

**Final decision: CONDITIONAL PASS**

IndicTrans2 is selected as the leading translation model candidate for MatriVaani.

**Reason:**
- Successful real model loading
- Successful real T4 GPU execution
- Strong performance
- Multiple successful Hindi ↔ Santali translations
- Correct Ol Chiki output in most tests
- Significantly better observed quality than the previously tested Groq provider

**However:** IndicTrans2 is NOT yet declared production-ready. Production integration must be performed as a separate engineering task after this report.

## 13. Production File Status

- **Files modified during Task 5.8 production validation:** NONE
- **MatriVaani production source code:** NOT MODIFIED
- **Flutter:** NOT MODIFIED
- **ASR:** NOT MODIFIED
- **Groq translation implementation:** NOT MODIFIED
- **.env:** NOT MODIFIED
- **requirements.txt:** NOT MODIFIED
- **IndicTrans2:** NOT YET INTEGRATED INTO MATRI VAANI

The Colab environment was used strictly for isolated model validation.

---

Task 5.8 validated IndicTrans2 using an actual Google Colab Tesla T4 environment. The model successfully loaded and produced substantially better observed Hindi ↔ Santali translation results than the previously tested Groq provider. IndicTrans2 is therefore selected as the leading translation candidate, but remains conditionally approved pending production integration and further validation. No MatriVaani production files were modified during this validation.
