# MATRIVAANI - REAL ASR SETUP AND DEPLOYMENT

The MatriVaani application utilizes a real Santali Wav2Vec2 checkpoint (`checkpoint-1500`) trained separately in a Linux/Google Colab environment.

To run the application with real inference capabilities instead of the UI mock adapter, you must make the checkpoint available to the application.

## A. Google Colab Deployment

If running the API from Google Colab:

1. Mount Google Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

2. Configure `.env` or system environment variables:
   ```env
   ASR_PROVIDER=checkpoint
   ASR_MODEL_PATH=/content/drive/MyDrive/MatriVaani_ASR/checkpoints/checkpoint-1500
   PROCESSOR_PATH=/content/drive/MyDrive/MatriVaani_ASR/processor
   ```

## B. Local Windows or Linux Deployment

If running locally:

1. Copy the `checkpoint-1500` directory and `processor` directory from your Google Drive to your local machine (e.g., `C:\models\MatriVaani_ASR\`).

2. Configure your `.env` file to point to the local paths:
   ```env
   ASR_PROVIDER=checkpoint
   ASR_MODEL_PATH=C:\models\MatriVaani_ASR\checkpoint-1500
   PROCESSOR_PATH=C:\models\MatriVaani_ASR\processor
   ```
   *(Use forward slashes `/` on Linux).*

**IMPORTANT RULES:**
- DO NOT modify the checkpoint files.
- DO NOT resume training on `checkpoint-1500`. The model is already trained.
- If the model is not found at the configured path, the application will intentionally refuse to initialize rather than silently falling back to a Hugging Face baseline.
