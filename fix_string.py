import re

filepath = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Fix broken strings
content = content.replace('_statusMessage = "No speech detected.\n  Please speak clearly and try again.";', 
                          '_statusMessage = "No speech detected.\\nPlease speak clearly and try again.";')
content = content.replace('_statusMessage = "Unable to connect to MatriVaani server.\n  Please check the connection.";', 
                          '_statusMessage = "Unable to connect to MatriVaani server.\\nPlease check the connection.";')
content = content.replace('_statusMessage = "Unable to connect to MatriVaani server.\nPlease check the connection.";',
                          '_statusMessage = "Unable to connect to MatriVaani server.\\nPlease check the connection.";')
content = content.replace('_statusMessage = "No speech detected.\nPlease speak clearly and try again.";',
                          '_statusMessage = "No speech detected.\\nPlease speak clearly and try again.";')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
