export PATH="/home/maars/.pyenv/bin:$PATH"
eval "/home/maars/.pyenv/bin/pyenv init -"
cd "/mnt/c/study files/sih project"

echo "Creating env..."
/home/maars/.pyenv/versions/3.12.9/bin/python -m venv indictrans2_env

echo "Activating and upgrading pip..."
source indictrans2_env/bin/activate
python -m pip install --upgrade pip setuptools wheel

echo "Installing torch and transformers..."
python -m pip install torch==2.5.1+cpu --index-url https://download.pytorch.org/whl/cpu
python -m pip install transformers==4.40.1 sacremoses sentencepiece psutil IndicTransToolkit

echo "Running tests..."
python test_indictrans2_local.py
