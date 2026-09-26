# MatriVaani Judge Demonstration Guide

This guide walks through a 3–5 minute demonstration of the MatriVaani application, emphasizing the AI-powered transformation of Santali speech into structured educational content.

## Prerequisites
- The backend FastAPI server is running (`uvicorn app.api.main:app --reload`)
- The Streamlit UI is running (`streamlit run app/frontend/app.py`)
- An `OPENAI_API_KEY` is configured in the `.env` file to enable translation and scriptwriting.
- Ensure the `ASR_PROVIDER` is set to `checkpoint` with the weights accessible locally, OR set to `mock` if demonstrating on a machine without the checkpoint.

## The Demonstration Steps

### 1. Start the Application & Explain Mode
- Open the Streamlit UI in the browser.
- Point out the **AI MODE** indicator at the top. It explicitly states whether the system is running in `PRODUCTION` or `DEMO`.
- Show the **Health Dashboard** in the sidebar. This gives transparency on which AI components are online (ASR, Translation, Scriptwriter, Copy Editor).

### 2. Upload Santali Audio
- Select a real `.flac` or `.wav` Santali audio file.
- Explain: *"This is a raw recording of a teacher speaking in Santali."*
- Click **Process Audio**.

### 3. Show ASR Transcript
- Expand the **Santali Transcript** section.
- Point out the native Ol Chiki script.
- Explain: *"The Wav2Vec2 ASR engine accurately transcribes the spoken Santali into text. We've verified this checkpoint decodes correctly (e.g. 'ᱠᱷᱚᱫᱮ ᱪᱟᱣᱞᱮ') with approximately a 10x ratio on CPU hardware (e.g. 16 seconds for a 1.6 second clip) but scales excellently on GPU."*

### 4. Show Cleaned Transcript
- Expand the **Cleaned Transcript** section.
- Explain: *"The cleaner node removes noise, unintelligible artifacts, and normalizes the text for the translation engine."*

### 5. Show Translation
- Highlight that the target language (e.g., Hindi) was selected at the beginning.
- Expand the **Translation** section.
- Explain: *"The translation engine accurately converts the text while preserving cultural context and meaning."*

### 6. Show Generated Script
- Expand the **Generated Script** section.
- Explain: *"The Scriptwriter AI takes the raw translated text and formats it into a structured educational lesson plan with a Title, Introduction, Main Content, and Conclusion."*

### 7. Show Expert-Edited Script
- Expand the **Final Edited Script** section.
- Explain: *"The Copy Editor AI performs a final pass to improve readability, flow, and grammar without hallucinating facts."*

### 8. Show Pipeline Statuses
- Expand the **Node Timings & Status** section.
- Explain: *"The backend LangGraph orchestrator logs the success/failure state of every micro-service, ensuring transparency if an API call fails."*

### 9. Export Result
- Click **Download Script (TXT)** or **Download Full Result (JSON)** to demonstrate how teachers can take this content offline and use it immediately.

## Key Takeaway for Judges
*MatriVaani successfully bridges the vernacular gap by taking raw, under-resourced Santali audio and autonomously producing structured, professional educational content in major languages.*
