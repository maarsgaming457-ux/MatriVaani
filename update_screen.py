import os

filepath = 'android/lib/screens/classroom_screen.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = "print('DEBUG: Failed to delete audio for job \\: \\');"
replacement = "print('DEBUG: Failed to delete audio for job \: \');"

content = content.replace(target, replacement)
content = content.replace("print('DEBUG: Failed to delete audio for job \: \');", replacement)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Fixed Screen")
