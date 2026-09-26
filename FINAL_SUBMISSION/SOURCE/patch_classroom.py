import re

with open('android/lib/screens/classroom_screen.dart', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace hardcoded Text fields in the header with DropdownButton
dropdown_code = '''
  String _getLangName(String code) {
    if (code == 'hi') return 'Hindi';
    if (code == 'sat') return 'Santali';
    if (code == 'ho') return 'Ho';
    return code;
  }

  Widget _buildLangDropdown({required String value, required ValueChanged<String?> onChanged}) {
    return DropdownButton<String>(
      value: value,
      items: const [
        DropdownMenuItem(value: 'hi', child: Text('Hindi')),
        DropdownMenuItem(value: 'sat', child: Text('Santali')),
        DropdownMenuItem(value: 'ho', child: Text('Ho')),
      ],
      onChanged: onChanged,
    );
  }
'''

# We need to insert the helper methods inside _ClassroomScreenState
if '_getLangName' not in text:
    text = text.replace('bool _isProcessing = false;', bool_is_processing := 'bool _isProcessing = false;\\n' + dropdown_code)
    if bool_is_processing not in text:
        # Fallback if bool _isProcessing = false; is not unique
        text = text.replace('  void _swapLanguages() {', dropdown_code + '\\n  void _swapLanguages() {')

# Replace the specific Row containing the texts
old_row = '''Row(
                children: [
                  Text(_sourceLang == 'sat' ? "Santali" : "Hindi", style: const TextStyle(fontWeight: FontWeight.bold)),
                  IconButton(
                    icon: const Icon(Icons.swap_horiz, color: MatriVaaniColors.primaryDark),
                    onPressed: _swapLanguages,
                    tooltip: 'Swap languages',
                  ),
                  Text(_targetLang == 'sat' ? "Santali" : "Hindi", style: const TextStyle(fontWeight: FontWeight.bold)),
                ],
              ),'''

new_row = '''Row(
                children: [
                  _buildLangDropdown(
                    value: _sourceLang,
                    onChanged: (val) {
                      if (val != null && !_isProcessing && !_isRecording) {
                        setState(() { _sourceLang = val; _clear(); });
                      }
                    },
                  ),
                  IconButton(
                    icon: const Icon(Icons.swap_horiz, color: MatriVaaniColors.primaryDark),
                    onPressed: _swapLanguages,
                    tooltip: 'Swap languages',
                  ),
                  _buildLangDropdown(
                    value: _targetLang,
                    onChanged: (val) {
                      if (val != null && !_isProcessing && !_isRecording) {
                        setState(() { _targetLang = val; _clear(); });
                      }
                    },
                  ),
                ],
              ),'''

text = text.replace(old_row, new_row)

# Replace 'Your Santali'
text = re.sub(r"Text\('Your Santali'", r"Text('Your \'", text)

# Replace 'Listening to Santali Speech...' and 'Hold to Speak Santali'
text = text.replace("'Listening to Santali Speech...' : 'Hold to Speak Santali'", "'Listening to \ Speech...' : 'Hold to Speak \'")
text = text.replace('// Your Santali Speech card', '// Your Speech card')

with open('android/lib/screens/classroom_screen.dart', 'w', encoding='utf-8') as f:
    f.write(text)
