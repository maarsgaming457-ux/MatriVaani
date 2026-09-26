# Deployment Guide

Deploying the MatriVaani backend online requires special consideration due to the size of the neural models (Mundari NMT and Santali ASR).

## Minimum Requirements
- **CPU:** 4+ cores recommended for faster inference.
- **RAM:** Minimum 8GB. The loaded PyTorch models require ~3GB RAM immediately on startup.
- **Storage:** ~5GB required for the OS, Python environment, and the local model `safetensors` files.
- **Python:** 3.10+

## ⚠️ Important Deployment Limitation
Because the production models consume roughly 2.5GB of disk space and >3GB of RAM, deploying this FastAPI backend on free-tier services (like Render's Free Plan, Heroku Free, or Vercel) **will result in Out Of Memory (OOM) crashes**.

For online deployment, you must provision a VPS (e.g., DigitalOcean, AWS EC2, or Google Compute Engine) with at least 8GB of RAM.

## Deployment Steps (VPS / Dedicated Server)
1. Install Git, Git LFS, and Python 3.10.
2. Clone the repository and initialize LFS:
   ```bash
   git clone https://github.com/maarsgaming457-ux/MatriVaani.git
   cd MatriVaani
   git lfs pull
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
4. Define Environment Variables:
   Set up your `.env` file with `SARVAM_API_KEY`, `GROQ_API_KEY`, etc. if you are using fallback external APIs.
5. Start the server using Uvicorn or Gunicorn:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

## CORS Configuration
For deployment, make sure to restrict CORS. If your backend is hosted online, restrict the `allow_origins` in your FastAPI setup to your specific web domains, or allow `*` only if it's purely a public mobile-app backend.

## Health Check
You can test the server is running by hitting `GET /health`.
