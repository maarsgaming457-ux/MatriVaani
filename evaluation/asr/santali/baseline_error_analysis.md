# Baseline Error Analysis: facebook/wav2vec2-base-100k-voxpopuli

**Average WER:** 1.00
**Average CER:** 1.41

## Observations
The model outputs empty or garbage predictions because it is a PRETRAINED base encoder with a randomly initialized LM head. It has zero knowledge of Ol Chiki characters, thus resulting in 100% WER/CER.

## Sample Errors

### Sample 1 (Duration: 11.90s)
- **Reference:** ᱟᱞᱮ ᱚᱲᱟᱜ ᱨᱮ ᱛᱮᱦᱤᱧ ᱤᱧ ᱵᱚᱭᱦᱟ ᱠᱩᱲᱤᱭᱟᱜ ᱡᱚᱱᱢᱚ ᱫᱤᱱ ᱢᱮᱱᱟᱜᱼᱟ ᱚᱱᱟ ᱠᱟᱨᱚᱱ ᱛᱮ ᱟᱢᱟᱜ ᱫᱚᱠᱟᱱ ᱠᱷᱚᱱ ᱠᱤᱪᱷᱩ ᱡᱤᱱᱤᱥ ᱤᱧ ᱡᱚᱢ ᱡᱤᱱᱤᱥ ᱤᱧ ᱤᱫᱤᱭᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 2 (Duration: 14.19s)
- **Reference:** ᱟᱸᱡᱚᱢ ᱞᱤᱫᱟᱹᱧ ᱟᱢᱟᱜ ᱫᱚᱠᱟᱱ ᱨᱮ ᱵᱚᱞᱮ ᱟᱹᱰᱤ ᱵᱷᱟᱞᱮ ᱵᱷᱟᱞᱮ ᱡᱤᱱᱤᱥ ᱧᱟᱢᱚᱜ ᱠᱟᱱᱟ ᱟᱞᱮ ᱚᱲᱟᱜ ᱯᱷᱮᱰ ᱨᱮᱱ ᱢᱤᱫᱴᱮᱱ ᱫᱟᱫᱟᱭ ᱞᱟᱹᱭ ᱟᱫᱤᱧᱟ ᱡᱮ ᱱᱚᱸᱰᱮ ᱟᱭᱢᱟ ᱠᱤᱪᱷᱩ ᱢᱚᱡᱽ ᱡᱤᱱᱤᱥ ᱧᱟᱢᱚᱜ ᱠᱟᱱᱟ ᱚᱱᱟᱛᱮ ᱟᱢ ᱴᱷᱮᱱ ᱤᱧ ᱦᱮᱡ ᱮᱱᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 3 (Duration: 7.04s)
- **Reference:** ᱛᱳ ᱤᱧ ᱠᱮᱠ ᱟᱨ ᱠᱤᱪᱷᱩ ᱵᱷᱟᱡᱟ ᱯᱳᱲᱟ ᱡᱤᱱᱤᱥ ᱡᱮᱢᱚᱱ ᱡᱮᱢᱚᱱ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 4 (Duration: 15.28s)
- **Reference:** ᱥᱤᱸᱜᱟᱲᱟ ᱵᱨᱮᱰ ᱪᱚᱯ ᱚᱱᱟᱠᱚᱜᱮ ᱵᱷᱟᱡᱟ ᱡᱤᱱᱤᱥ ᱤᱧ ᱤᱫᱤ ᱛᱟᱢᱟ ᱚᱱᱟ ᱥᱚᱸᱜᱮ ᱚᱱᱟ ᱠᱚ ᱡᱤᱱᱤᱥ ᱤᱧ ᱦᱟᱛᱟᱣ ᱞᱮᱠᱷᱟᱱ ᱤᱧ ᱥᱚᱥ ᱟᱨ ᱪᱟᱹᱴᱱᱤ ᱚᱱᱟ ᱠᱚ ᱯᱷᱨᱤᱧ ᱧᱟᱢ ᱟᱥᱮ ᱵᱟᱝ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 5 (Duration: 5.28s)
- **Reference:** ᱚᱱᱟᱛᱤᱧ ᱟᱸᱡᱚᱢᱮᱫᱟ ᱟᱢ ᱴᱷᱮᱱ ᱟᱨ ᱚᱱᱟ ᱞᱟᱹᱭ ᱞᱟᱹᱜᱤᱫ ᱤᱧ ᱦᱮᱡ ᱮᱱᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 6 (Duration: 14.69s)
- **Reference:** ᱵᱷᱟᱨᱚᱛ ᱫᱤᱥᱚᱢ ᱨᱮᱫᱚ ᱯᱷᱩᱴᱵᱚᱞ ᱠᱚ ᱮᱱᱮᱡᱼᱟ ᱟᱨ ᱠᱨᱤᱠᱮᱴ ᱵᱷᱟᱞᱩᱠ ᱜᱩᱰᱩ ᱟᱨ ᱥᱚᱨᱮᱥ ᱮᱱᱮᱡ ᱠᱤᱱᱫᱚ ᱮᱸᱜ ᱥᱚᱪᱤᱱ ᱟᱨ ᱫᱷᱚᱱᱤ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 7 (Duration: 1.48s)
- **Reference:** ᱛᱩᱨᱩᱭ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.40

### Sample 8 (Duration: 17.79s)
- **Reference:** ᱯᱚᱨᱟᱱ ᱱᱚᱢᱵᱚᱨ ᱛᱷᱨᱤ ᱱᱟᱭᱤᱱ ᱯᱷᱳᱨ ᱚᱣᱟᱱ ᱰᱚᱵᱚᱞ ᱯᱷᱟᱭᱤᱵᱷ ᱱᱟᱭᱤᱱ ᱥᱮᱵᱷᱮᱱ ᱯᱷᱟᱭᱤᱵᱷ ᱚᱣᱟᱱ ᱥᱤᱠᱥ ᱚᱣᱟᱱ ᱥᱟᱶ ᱤᱧᱟᱹᱜ ᱮ ᱯᱤ ᱮᱠᱟᱣᱩᱱᱴ ᱨᱮᱭᱟᱜ ᱞᱮᱱᱫᱮᱱ ᱨᱮᱭᱟᱜ ᱵᱚᱨᱱᱚᱱᱟ ᱩᱫᱩᱜ ᱟᱹᱧ ᱢᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 9 (Duration: 20.88s)
- **Reference:** ᱛᱩᱨᱩᱭ ᱮᱭᱟᱭ ᱯᱮ ᱛᱩᱨᱩᱭ ᱮᱭᱟᱭ ᱢᱚᱬᱮ ᱤᱨᱟᱹᱞ ᱥᱩᱱ ᱢᱚᱬᱮ ᱤᱨᱟᱹᱞ ᱯᱮ ᱯᱷᱚᱱ ᱱᱚᱢᱵᱚᱨ ᱠᱚ ᱞᱟᱹᱜᱤᱫ ᱴᱷᱤᱠᱟᱹ ᱥᱤᱫᱽ ᱥᱟᱠᱟᱢ ᱰᱟᱣᱩᱱᱞᱳᱰ ᱞᱟᱹᱜᱤᱫ ᱫᱟᱭᱟ ᱠᱟᱛᱮᱫ ᱥᱩᱵᱤᱫᱷᱟ ᱧᱟᱢ ᱠᱚᱣᱟᱜ ᱧᱩᱛᱩᱢ ᱵᱟᱪᱷᱟᱣ ᱢᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 10 (Duration: 0.54s)
- **Reference:** ᱦᱮᱞᱳ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.75

### Sample 11 (Duration: 7.28s)
- **Reference:** ᱦᱮᱞᱳ ᱤᱧ ᱜᱮ ᱥᱩᱠᱩᱨᱢᱩᱱᱤ ᱢᱩᱨᱢᱩ ᱢᱮᱱᱮᱜᱼᱟᱹᱧ ᱤᱭᱟᱹ ᱞᱩᱠᱩᱭᱠᱟᱱᱟᱞᱤ ᱠᱷᱚᱱᱟᱜ ᱟᱢ ᱜᱮ ᱨᱟ ᱪᱤ ᱨᱤᱱᱤᱡ ᱥᱮᱬᱟ ᱰᱟᱠᱛᱟᱨ ᱫᱚ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 12 (Duration: 12.53s)
- **Reference:** ᱚ ᱦᱚᱸ ᱟᱫᱚ ᱤᱧ ᱢᱮᱱᱮᱫ ᱟᱹᱧ ᱦᱟᱯᱮ ᱥᱮ ᱤᱧ ᱦᱚᱸ ᱱᱤᱛᱳᱜ ᱯᱮᱥᱮᱱᱤᱧ ᱵᱮᱱᱟᱣ ᱠᱟᱱᱟᱹᱧ ᱟᱫᱚ ᱢᱮᱱᱮᱜᱼᱟᱹᱧ ᱦᱟᱯᱮᱥᱮᱧ ᱯᱷᱳᱱᱟᱭᱟ ᱞᱟᱹᱭᱮᱜᱼᱟᱹᱧ ᱚᱸᱰᱮ ᱢᱮᱱᱮᱫ ᱫᱚᱠᱚ ᱥᱮᱬᱟ ᱰᱟᱠᱛᱟᱨ ᱢᱮᱱᱟᱭᱟ ᱟᱫᱚ ᱪᱮᱫᱞᱮᱠᱟᱱ ᱨᱩᱜᱤ ᱠᱚᱢ ᱧᱮᱞ ᱠᱟᱣᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 13 (Duration: 1.24s)
- **Reference:** <unintelligible>
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 14 (Duration: 1.15s)
- **Reference:** ᱢᱟᱱᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.75

### Sample 15 (Duration: 13.63s)
- **Reference:** ᱦᱳᱭ ᱟᱫᱚ ᱚᱱᱟᱜᱤᱧ ᱢᱮᱱᱮᱫᱼᱟ ᱦᱟᱯᱮᱥᱮ ᱞᱟᱹᱭᱮᱜᱼᱟᱹᱧ ᱞᱟᱹᱭᱮᱫ ᱫᱚᱠᱚ ᱮᱱᱠᱷᱟᱱ ᱞᱟᱹᱭᱮᱫᱼᱟᱹᱧ ᱦᱟᱯᱮᱥᱮ ᱯᱷᱳᱱ ᱠᱟᱛᱮᱧ ᱵᱟᱲᱟᱭ ᱤᱭᱟᱹᱭᱟ ᱢᱟᱱᱮ ᱠᱟᱛᱷᱟᱧ ᱦᱟᱛᱟᱣᱟ ᱠᱤ ᱪᱮᱫᱞᱮᱠᱟᱱ ᱯᱮᱥᱮᱱ ᱠᱚ ᱧᱮᱞ ᱠᱚᱣᱟᱭ ᱮᱱᱠᱷᱟᱱ ᱫᱚ ᱪᱟᱞᱟᱜ ᱦᱩᱭᱩᱜᱼᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 16 (Duration: 5.13s)
- **Reference:** ᱟᱫᱚ ᱡᱮᱛᱮᱞᱮᱠᱟᱱ ᱢᱟᱱᱮ ᱤᱭᱟᱹ ᱨᱩᱜᱤ ᱠᱚᱜᱮᱢ ᱧᱮᱞ ᱠᱚᱣᱟ ᱥᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 17 (Duration: 8.25s)
- **Reference:** ᱦᱳᱭ ᱟᱫᱚ ᱚᱱᱟᱜᱮ ᱢᱮᱱᱮᱜᱼᱟ ᱞᱮ ᱟᱨ ᱛᱤᱥ ᱛᱤᱥ ᱠᱚ ᱛᱟᱦᱮᱱᱟ ᱚᱸᱰᱮ ᱫᱚ ᱥᱮ ᱟᱨᱦᱚᱸ ᱮᱴᱟᱜ ᱠᱚᱨᱮ ᱪᱮᱢᱵᱟᱨ ᱠᱚᱢ ᱠᱷᱩᱞᱟᱹᱣ ᱠᱟᱜᱼᱟ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 18 (Duration: 9.16s)
- **Reference:** ᱦᱳᱭᱛᱳ ᱟᱫᱚ ᱛᱤᱱ ᱠᱷᱚᱱ ᱢᱟᱱᱮ ᱴᱟᱭᱤᱢ ᱛᱤᱱ ᱨᱮ ᱛᱤᱱ ᱛᱤᱱᱮᱢ ᱫᱩᱲᱩᱵᱼᱟ ᱛᱤᱱᱟᱹᱜ ᱜᱷᱟᱹᱲᱤᱠ ᱠᱛᱮᱫ ᱮᱢ ᱫᱩᱲᱩᱵᱼᱟ ᱤᱱᱟᱹ ᱫᱚ ᱤᱱᱟᱹ ᱚᱠᱛᱚ ᱨᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

### Sample 19 (Duration: 1.12s)
- **Reference:** ᱚ ᱦᱚᱸ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.40

### Sample 20 (Duration: 15.95s)
- **Reference:** ᱟᱫᱚ ᱚᱱᱟᱜᱤᱧ ᱢᱮᱱᱮᱜᱼᱟ ᱯᱟᱪᱮᱫ ᱟᱨᱦᱚᱸ ᱛᱤᱥ ᱛᱤᱥ ᱠᱚᱨᱮ ᱫᱩᱲᱩᱵᱼᱟᱭ ᱵᱟᱭ ᱵᱟᱭ ᱢᱮᱱᱚᱜᱚᱜᱼᱟ ᱟᱫᱚᱧ ᱢᱮᱱᱮᱜᱼᱟ ᱦᱟᱯᱮᱥᱮ ᱠᱩᱞᱤ ᱠᱟᱛᱮᱫ ᱜᱮᱵᱚᱱ ᱵᱟᱲᱟᱭ ᱧᱟᱢᱟ ᱠᱤ ᱛᱤᱥ ᱠᱚᱨᱮ ᱛᱤᱥ ᱛᱤᱥᱮ ᱫᱩᱲᱩᱵ ᱠᱟᱱᱟ ᱥᱮ ᱪᱷᱩᱴᱤ ᱠᱚ ᱢᱟᱱᱮ ᱟᱨᱦᱚᱸ ᱛᱤᱱᱟᱹᱜ ᱜᱟᱱ ᱤᱭᱟᱹ ᱠᱚ ᱢᱮᱱᱟᱜᱼᱟ ᱪᱮᱢᱵᱟᱨ ᱠᱚ ᱛᱟᱭ ᱢᱮᱱᱟᱜᱼᱟ ᱚᱱᱟ ᱠᱚᱨᱮ ᱫᱩᱲᱩᱵᱼᱟᱭ ᱯᱟᱪᱮᱫ ᱢᱮᱱᱮᱜᱼᱟ ᱞᱮ
- **Predicted:** [EMPTY]
- **WER:** 1.00 | **CER:** 1.00

