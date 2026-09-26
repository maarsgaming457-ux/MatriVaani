import re

filepath = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Add Mundari to dropdown
content = content.replace(
    "DropdownMenuItem(value: 'ho', child: Text('Ho')),",
    "DropdownMenuItem(value: 'ho', child: Text('Ho')),\n        DropdownMenuItem(value: 'unr', child: Text('Mundari')),"
)

# Fix _getLangName
content = content.replace(
    "if (code == 'ho') return 'Ho';",
    "if (code == 'ho') return 'Ho';\n    if (code == 'unr') return 'Mundari';"
)

# Update _isTranslationSupported
# Let's just make it simple: 'hi' -> 'sat', 'hi' -> 'unr', 'ho' -> 'hi'
# The old logic:
#     if (_sourceLang == 'ho' && _targetLang == 'hi') return true; // Experimental supported
#     if (_sourceLang == 'hi' && _targetLang == 'ho') return false; // Reverse not supported
#     if (_sourceLang == 'ho' || _targetLang == 'ho') return false; // Any other Ho combo not supported
#     return true; // hi <-> sat supported
content = re.sub(
    r"bool get _isTranslationSupported\s*\{.*?\n\s*\}",
    """bool get _isTranslationSupported {
    if (_sourceLang == 'hi' && _targetLang == 'unr') return true;
    if (_sourceLang == 'unr' && _targetLang == 'hi') return false;
    if (_sourceLang == 'ho' && _targetLang == 'hi') return true;
    if (_sourceLang == 'hi' && _targetLang == 'ho') return false;
    if (_sourceLang == 'ho' || _targetLang == 'ho') return false;
    if (_sourceLang == 'unr' || _targetLang == 'unr') return false;
    return true;
  }""",
    content,
    flags=re.DOTALL
)

# Update _translate
#     // Case 2: Standard Production Route (e.g. Santali <-> Hindi)
#     final result = await ApiService.translateText(text, _sourceLang, _targetLang);
content = content.replace(
    "final result = await ApiService.translateText(text, _sourceLang, _targetLang);",
    "String? result;\n    if (_sourceLang == 'hi' && _targetLang == 'unr') {\n      result = await ApiService.translateHindiToMundari(text);\n    } else {\n      result = await ApiService.translateText(text, _sourceLang, _targetLang);\n    }"
)

# Update _playTts
#     if (_targetLang == 'ho') {
content = content.replace(
    "if (_targetLang == 'ho') {",
    "if (_targetLang == 'ho' || _targetLang == 'unr') {"
)

# Wait, we DO want TTS for Mundari! The prompt says "Mundari TTS -> Flutter Android audio playback".
# So remove `|| _targetLang == 'unr'`. We will just use `hi` TTS backend for Mundari since they said "The existing backend currently returns audio... Do not change the backend TTS implementation merely because the language field looks unusual."
# And in the prompt: "Flutter sends POST /tts JSON: {text: ..., language: hi}"
# So we need to pass `hi` as language to TTS when target is `unr`.

content = content.replace(
    "final success = await _ttsPlayer.playTts(_translatedText, _targetLang, provider: _ttsProvider);",
    "final success = await _ttsPlayer.playTts(_translatedText, _targetLang == 'unr' ? 'hi' : _targetLang, provider: _ttsProvider);"
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("Updated Mundari routing.")
