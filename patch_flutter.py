import sys

path = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = """  Future<void> _translate() async {
    final text = _inputController.text.trim();"""

replacement = """  Future<void> _translate() async {
    final text = "मेरा नाम सुमित है";"""

if target in content:
    content = content.replace(target, replacement)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched!")
else:
    print("Target not found!")
