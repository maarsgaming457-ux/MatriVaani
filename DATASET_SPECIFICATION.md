# Dataset Specification

## Overview
The PALASH Corpus is specifically designed for low-resource tribal-language education.

## Dataset Categories

### 1. ASR Dataset
- Pairs: Speech -> Transcript
- Attributes: Multiple speakers, genders, speeds, dialects.
- Environments: Classroom, conversational, noisy.

### 2. Translation Dataset
- Aligned Hindi <-> Santhali educational text.
- Domains: Alphabet, numbers, colors, shapes, classroom instructions, stories.

### 3. TTS Dataset
- High-quality native-speaker recordings paired with verified transcripts.

## Metadata Schema
- `sample_id`: Unique identifier
- `language`: Language code
- `speaker_id`: Speaker identifier
- `text`: Transcript / text content
- `audio_path`: Path to audio file
- `domain`: Educational domain (e.g., math, vocabulary)
- `dialect`: Specific dialect
- `quality_score`: Human/automated quality rating
- `verification_status`: Status of validation
- `dataset_version`: Version (e.g., v0.1)

## Quality Constraints
- Validation pipeline ensures high quality over quantity.
- Versioned datasets (e.g., PALASH-DATA-v0.1).
- Strict separation of train, validation, and test sets.
