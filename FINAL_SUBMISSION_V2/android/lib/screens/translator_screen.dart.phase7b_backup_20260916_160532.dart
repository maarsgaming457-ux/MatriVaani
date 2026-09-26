import 'package:flutter/material.dart';
import '../services/api_service.dart';
import '../services/tts_player_service.dart';

class TranslatorScreen extends StatefulWidget {
  @override
  _TranslatorScreenState createState() => _TranslatorScreenState();
}

class _TranslatorScreenState extends State<TranslatorScreen> {
  String _sourceLang = 'hi';
  String _targetLang = 'sat';
  
  final TextEditingController _inputController = TextEditingController();
  final TtsPlayerService _ttsPlayer = TtsPlayerService();
  String _translatedText = '';
  bool _isLoading = false;
  String _errorMessage = '';
  
  bool _isTtsLoading = false;
  String _ttsMessage = '';
  String _ttsProvider = 'sarvam';

  @override
  void dispose() {
    _ttsPlayer.dispose();
    _inputController.dispose();
    super.dispose();
  }

  void _swapLanguages() {
    setState(() {
      final temp = _sourceLang;
      _sourceLang = _targetLang;
      _targetLang = temp;
      
      final tempText = _inputController.text;
      _inputController.text = _translatedText;
      _translatedText = tempText;
      _errorMessage = '';
      _ttsMessage = '';
    });
  }

  Future<void> _translate() async {
    final text = _inputController.text.trim();
    if (text.isEmpty) {
      setState(() {
        _errorMessage = 'Please enter text to translate.';
        _translatedText = '';
        _ttsMessage = '';
      });
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = '';
      _translatedText = '';
      _ttsMessage = '';
    });

    final result = await ApiService.translateText(text, _sourceLang, _targetLang);

    setState(() {
      _isLoading = false;
      if (result != null) {
        _translatedText = result;
      } else {
        _errorMessage = 'Error: Translation failed or backend is unreachable.';
      }
    });
  }

  Future<void> _playTts() async {
    if (_translatedText.isEmpty) return;
    
    setState(() {
      _isTtsLoading = true;
      _ttsMessage = '';
    });
    
    final success = await _ttsPlayer.playTts(_translatedText, _targetLang, provider: _ttsProvider);
    
    if (mounted) {
      setState(() {
        _isTtsLoading = false;
        if (!success) {
          _ttsMessage = 'TTS is currently unavailable.';
        } else {
          _ttsMessage = '';
        }
      });
    }
  }

  String _getLangName(String code) {
    return code == 'hi' ? 'Hindi' : 'Santali';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Text Translator')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Language Selectors and Swap Button
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildLangDropdown(
                  value: _sourceLang,
                  onChanged: (val) {
                    if (val != null) setState(() => _sourceLang = val);
                  },
                ),
                IconButton(
                  icon: const Icon(Icons.swap_horiz, size: 32),
                  onPressed: _swapLanguages,
                  tooltip: 'Swap languages',
                ),
                _buildLangDropdown(
                  value: _targetLang,
                  onChanged: (val) {
                    if (val != null) setState(() => _targetLang = val);
                  },
                ),
              ],
            ),
            const SizedBox(height: 20),
            
            // Input Area
            TextField(
              controller: _inputController,
              maxLines: 4,
              decoration: InputDecoration(
                labelText: 'Enter ${_getLangName(_sourceLang)} text',
                border: const OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            
            // Translate Button
            ElevatedButton(
              onPressed: _isLoading ? null : _translate,
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
              ),
              child: _isLoading 
                  ? const SizedBox(
                      height: 20, width: 20, 
                      child: CircularProgressIndicator(strokeWidth: 2)
                    )
                  : const Text('Translate', style: TextStyle(fontSize: 18)),
            ),
            const SizedBox(height: 20),
            
            // Error Message
            if (_errorMessage.isNotEmpty)
              Text(
                _errorMessage,
                style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
              
            const SizedBox(height: 10),
            
            // Output Area
            const Text('Translation:', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Container(
              constraints: const BoxConstraints(minHeight: 100),
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8.0),
                color: Colors.grey.shade100,
              ),
              child: SelectableText(
                _translatedText.isEmpty ? '...' : _translatedText,
                style: const TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 10),
            
            // TTS Message
            if (_ttsMessage.isNotEmpty)
              Text(
                _ttsMessage,
                style: const TextStyle(color: Colors.orange, fontWeight: FontWeight.bold),
                textAlign: TextAlign.center,
              ),
            const SizedBox(height: 10),

            
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('TTS Provider: '),
                DropdownButton<String>(
                  value: _ttsProvider,
                  items: const [
                    DropdownMenuItem(value: 'sarvam', child: Text('Sarvam')),
                    DropdownMenuItem(value: 'bhashini', child: Text('Bhashini')),
                    DropdownMenuItem(value: 'local', child: Text('Local')),
                  ],
                  onChanged: (val) {
                    if (val != null) setState(() => _ttsProvider = val);
                  },
                ),
              ],
            ),
            const SizedBox(height: 10),

            // TTS Play Button
            ElevatedButton.icon(
              onPressed: (_translatedText.isEmpty || _isTtsLoading) ? null : _playTts,
              icon: _isTtsLoading 
                  ? const SizedBox(height: 16, width: 16, child: CircularProgressIndicator(strokeWidth: 2))
                  : const Icon(Icons.volume_up),
              label: const Text('Play Audio'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 12),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLangDropdown({required String value, required ValueChanged<String?> onChanged}) {
    return DropdownButton<String>(
      value: value,
      items: const [
        DropdownMenuItem(value: 'hi', child: Text('Hindi')),
        DropdownMenuItem(value: 'sat', child: Text('Santali')),
      ],
      onChanged: onChanged,
    );
  }
}
