export PATH="/home/maars/.pyenv/bin:$PATH"
eval "/home/maars/.pyenv/bin/pyenv init -"
cd "/mnt/c/study files/sih project"
pyenv --version
pyenv install -s 3.12.9
pyenv local 3.12.9
python --version
which python
python -m venv indictrans2_env
