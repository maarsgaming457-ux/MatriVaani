import os
import sys
import subprocess

candidates = [
    "models/santhali_asr_final"
]

for c in candidates:
    for q in ["False"]:
        print(f"Running {c} (INT8={q})...")
        subprocess.run([sys.executable, "ai/asr/benchmark_candidates.py", c, q])
