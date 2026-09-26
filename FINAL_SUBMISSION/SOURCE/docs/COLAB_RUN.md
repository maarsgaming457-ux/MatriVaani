# MatriVaani - Google Colab Run Guide

To run the complete MatriVaani application in Google Colab (where the `checkpoint-1500` directory currently lives), follow these exact steps:

## 1. Mount Google Drive
In your first Colab cell, mount your drive to access the weights:

```python
from google.colab import drive
drive.mount('/content/drive')
```

## 2. Clone Repository & Install Dependencies
Clone the MatriVaani repository and install its dependencies. Note: Replace `YOUR_GITHUB_URL` with your actual repository URL.

```bash
!git clone YOUR_GITHUB_URL MatriVaani
%cd MatriVaani
!pip install -r requirements.txt
```

## 3. Configure Environment
Create a `.env` file pointing exactly to the physical weights in your drive.

```bash
%%writefile .env
APP_NAME=MatriVaani
LOG_LEVEL=INFO
APP_MODE=PRODUCTION

# REAL ASR CONFIGURATION
ASR_PROVIDER=checkpoint
ASR_MODEL_PATH=/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500
PROCESSOR_PATH=/content/drive/MyDrive/MatriVaani_ASR/processor

# REAL LLM CONFIGURATION (Insert your API key here)
GROQ_API_KEY=gsk_your-real-api-key
TRANSLATION_PROVIDER=groq
LLM_PROVIDER=groq
GROQ_MODEL=llama-3.3-70b-versatile
TARGET_LANGUAGE=hi
```

## 4. Run Real ASR Test
Verify that the checkpoint loads correctly on Colab's hardware:

```bash
!python scripts/test_real_asr.py
```
*(Expected Output: The CPU inference will take approximately 16.2 seconds for a 1.6s audio clip and correctly transcribe valid Ol Chiki characters).*

## 5. Run Complete Pipeline
Execute the full multi-modal pipeline end-to-end to verify everything works offline from the UI:

```bash
!python scripts/run_real_pipeline.py
```

## 6. Start FastAPI & Streamlit (Optional in Colab)
Running web servers in Colab requires tunneling. You can use `localtunnel` or `ngrok` to expose them:

```bash
# Start FastAPI in background
!nohup uvicorn app.api.main:app --port 8000 &

# Start Streamlit in background
!nohup streamlit run app/frontend/app.py --server.port 8501 &

# Use localtunnel to get a public URL for Streamlit
!npm install -g localtunnel
!npx localtunnel --port 8501
```
