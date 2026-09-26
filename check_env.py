import os
from dotenv import load_dotenv

load_dotenv()
print(f"Translation provider in env: {os.getenv('TRANSLATION_PROVIDER')}")
