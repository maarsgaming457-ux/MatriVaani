# MatriVaani Architecture

## Overview
MatriVaani is an AI-Powered Vernacular Pedagogy and Real-Time Translation Engine, designed specifically to process Santali speech into structured educational content.

## Components

### 1. Frontend (Streamlit)
- `app/frontend/app.py`: Provides the user interface for audio upload, language selection, and visualization of the multi-stage AI pipeline.

### 2. Backend API (FastAPI)
- `app/api/main.py`: Exposes REST endpoints (`/health`, `/api/v1/process`, etc.) to trigger the backend workflows. It handles file uploads, saves temporary files, calls the LangGraph pipeline, and cleans up resources.

### 3. Pipeline Orchestration (LangGraph)
- `app/graph/workflow.py`: Manages the sequential state flow of the data.
- **Nodes**:
  - `ASR`: Transcribes Santali audio using a Wav2Vec2 checkpoint.
  - `Cleaner`: Normalizes the transcript, removes noise, and preserves Ol Chiki script.
  - `Translator`: Translates the cleaned Santali text into the target language (e.g., Hindi, English).
  - `Scriptwriter`: Uses an LLM to generate a structured educational script from the translated text.
  - `Copy Editor`: Uses an LLM to professionally edit the generated script for clarity and flow.
  - `Finalizer`: Consolidates the outputs, maps metadata, and determines the final success/failure state of the pipeline.

### 4. Services (Adapters)
- `ASRService`: Singleton service wrapping the Hugging Face `Wav2Vec2ForCTC` model. Supports a `checkpoint` provider (real model) and a `mock` provider.
- `TranslationService`: Connects to OpenAI for translation, with a `mock` fallback.
- `LLMService`: Handles Scriptwriter and Copy Editor prompts using OpenAI API.
- `TTSService`: Placeholder for future Santali text-to-speech capabilities.

## Data Flow
`Audio File -> ASR -> Raw Santali -> Cleaner -> Clean Santali -> Translator -> Translated Text -> Scriptwriter -> Draft Script -> Copy Editor -> Final Script`
