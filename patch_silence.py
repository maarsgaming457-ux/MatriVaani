import os

filepath = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Current block:
#         if (transcript != null && transcript.trim().isNotEmpty && !transcript.contains('[SILENCE DETECTED]')) {
#           _inputController.text = transcript;
#           await _translate();
#         } else {
#           setState(() {
#             _isLoading = false;
#             _statusMessage = "Unable to connect to MatriVaani server.\nPlease check the connection.";
#           });
#         }

# New block:
new_block = """        if (transcript != null && transcript.trim().isNotEmpty && !transcript.contains('[SILENCE DETECTED]')) {
          _inputController.text = transcript;
          await _translate();
        } else {
          setState(() {
            _isLoading = false;
            if (transcript != null && (transcript.trim().isEmpty || transcript.contains('[SILENCE DETECTED]'))) {
              _statusMessage = "No speech detected.\\nPlease speak clearly and try again.";
            } else {
              _statusMessage = "Unable to connect to MatriVaani server.\\nPlease check the connection.";
            }
          });
        }"""

import re
# We need to replace the `if (transcript != null ...` block inside `_stopRecording`
content = re.sub(
    r"if\s*\(transcript\s*!=\s*null\s*&&\s*transcript\.trim\(\)\.isNotEmpty(.*?)\)\s*\{.*?\n.*?\s*\}\s*else\s*\{.*?\n.*?\s*setState\(\(\)\s*\{.*?\n.*?\n.*?\s*\}\);\s*\}",
    new_block,
    content,
    flags=re.DOTALL
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("translator_screen.dart patched for silence handling.")
