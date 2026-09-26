export PATH="/home/maars/.pyenv/bin:$PATH"
eval "$(/home/maars/.pyenv/bin/pyenv init -)"
cd "/mnt/c/study_files/sih project"
if [ ! -d "indictrans2_env/bin" ]; then
    echo "Creating env..."
    /home/maars/.pyenv/versions/3.12.9/bin/python -m venv indictrans2_env
    source indictrans2_env/bin/activate
    python -m pip install --upgrade pip setuptools wheel
    python -m pip install torch==2.5.1+cpu --index-url https://download.pytorch.org/whl/cpu
    python -m pip install transformers==4.40.1 sacremoses sentencepiece psutil IndicTransToolkit fastapi uvicorn
else
    source indictrans2_env/bin/activate
fi
python indictrans2_server.py
source indictrans2_env/bin/activate
python indictrans2_server.py
