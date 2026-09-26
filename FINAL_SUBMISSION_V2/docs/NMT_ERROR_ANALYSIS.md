# MatriVaani NMT Error Analysis Tracking

This document serves as the central registry for tracking, categorizing, and debugging translation errors encountered by the MatriVaani NMT engine during evaluation.

## Current Baseline Status
- **Baseline Models Tested**: None (Pending verified dataset)
- **Primary Direction**: Hindi -> Santhali
- **Total Errors Tracked**: 0

## Error Categories

When evaluating baseline models or fine-tuned checkpoints, human annotators must classify translation errors into one of the following categories:

1. **Lexical Error**: Incorrect vocabulary choice (e.g., translating "dog" to "cat").
2. **Grammar Error**: Incorrect verb tense, subject-verb agreement, or pluralization.
3. **Word Order**: Grammatically valid words placed in the wrong syntactic order.
4. **Missing Words (Under-translation)**: The model dropped crucial information from the source sentence.
5. **Extra Words (Over-translation/Hallucination)**: The model generated words that do not exist in the source text.
6. **Mistranslation**: The translation fundamentally alters the meaning of the source text.
7. **Named Entity Problem**: Failing to transliterate names, places, or proper nouns correctly.
8. **Number Error**: Failing to translate or accurately transfer numerical values.
9. **Educational Terminology Error**: Using a generic word when a specific pedagogical term was required.
10. **Script Problem**: Mixing Devnagari/Roman characters into Ol Chiki output.
11. **Context Error**: Translating a word correctly in isolation, but incorrectly for the given sentence context.

## Error Log (Template)

| ID | Source (Hindi) | Expected (Santhali) | Model Output | Error Category | Notes/Fix |
|----|----------------|---------------------|--------------|----------------|-----------|
| 001 | [Example] | [Expected] | [Output] | - | - |

*(To be populated post-evaluation)*
