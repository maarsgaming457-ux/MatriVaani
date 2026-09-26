import sys

with open("app/services/asr_service.py", "r", encoding="utf-8") as f:
    content = f.read()

import re
content = re.sub(r'prompt=.*?,\s*', '', content)

with open("app/services/asr_service.py", "w", encoding="utf-8") as f:
    f.write(content)
