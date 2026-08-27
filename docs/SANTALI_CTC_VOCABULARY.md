# MATRIVAANI - SANTALI CTC VOCABULARY

## 1. Overview
The Santali vocabulary for `MatriVaani-ASR-Santhali-v0.1` has been derived directly from the empirical character statistics of the 1,200 real development samples from `ai4bharat/IndicVoices` (`santali` config).

## 2. Special Tokens
CTC models and Hugging Face pipelines require standardized special tokens to control blank prediction, unknown symbols, and word boundaries.

- `[PAD]` (Index 0): Used as the **CTC Blank Token**. CTC dynamically predicts blanks between character emissions.
- `[UNK]` (Index 1): The **Unknown Token**. Any character not in the vocabulary will map here. (For example, out-of-domain Latin words or untranscribed `<unintelligible>` blocks will be replaced with `[UNK]`).
- `|` (Index 2): The **Word Delimiter Token**. In transcription, standard spaces `" "` are mapped to `|`. When the model predicts `|`, the tokenizer decodes it back to a standard space.

## 3. Ol Chiki Character Set
The dataset organically contained exactly **36** unique Ol Chiki characters/modifiers (Unicode U+1C50 - U+1C7F). These have been assigned indices `3` through `38`.

### Empirical Frequencies (from 1,200 samples)
1. ᱟ : 10,598
2. ᱚ : 5,201
3. ᱮ : 4,864
4. ᱱ : 3,443
5. ᱠ : 3,267
6. ᱤ : 2,741
7. ᱜ : 2,642
8. ᱨ : 2,334
9. ᱫ : 2,128
10. ᱢ : 1,778
11. ᱩ : 1,751
12. ᱦ : 1,674
13. ᱛ : 1,637
14. ᱵ : 1,579
15. ᱭ : 1,545
16. ᱥ : 1,464
17. ᱞ : 1,451
18. ᱹ : 1,385
19. ᱷ : 1,134
20. ᱡ : 1,117
21. ᱸ : 876
22. ᱯ : 787
23. ᱪ : 699
24. ᱧ : 673
25. ᱣ : 611
26. ᱴ : 583
27. ᱼ : 550
28. ᱲ : 543
29. ᱰ : 527
30. ᱝ : 355
31. ᱳ : 347
32. ᱽ : 195
33. ᱬ : 63
34. ᱶ : 47
35. ᱺ : 20
36. ᱻ : 6

## 4. Unnecessary Characters Handled
The transcribers of the original dataset used the string `<unintelligible>` to demarcate unclear audio. The Latin characters (`<, >, b, e, g, i, l, n, t, u`) associated with this tag were explicitly filtered out of the active vocabulary to constrain the ASR acoustic model strictly to the Santali script. The ASR tokenizer will natively collapse these to `[UNK]` during target encoding.

## 5. Total Vocabulary Size
The complete vocabulary size for `Wav2Vec2ForCTC.lm_head` is exactly **39** (indices 0 to 38).
