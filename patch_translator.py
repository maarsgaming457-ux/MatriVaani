import re
import os

filepath = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Add imports if not present
if "import 'package:record/record.dart';" not in content:
    content = content.replace(
        "import '../services/tts_player_service.dart';",
        "import '../services/tts_player_service.dart';\nimport 'package:record/record.dart';\nimport 'package:permission_handler/permission_handler.dart';\nimport 'dart:io';\nimport 'package:path_provider/path_provider.dart';\nimport '../widgets/animated_button.dart';"
    )

# Add state variables
if "final _audioRecorder = AudioRecorder();" not in content:
    content = content.replace(
        "final TtsPlayerService _ttsPlayer = TtsPlayerService();",
        "final TtsPlayerService _ttsPlayer = TtsPlayerService();\n  final _audioRecorder = AudioRecorder();\n  bool _isRecording = false;"
    )

# Add recording logic
recording_logic = """
  Future<void> _startRecording() async {
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      try {
        Directory tempDir = await getTemporaryDirectory();
        String path = '${tempDir.path}/translator_audio_${DateTime.now().millisecondsSinceEpoch}.wav';
        await _audioRecorder.start(
          const RecordConfig(encoder: AudioEncoder.wav, sampleRate: 16000, numChannels: 1),
          path: path,
        );
        setState(() {
          _isRecording = true;
          _errorMessage = '';
        });
      } catch (e) {
        setState(() {
          _errorMessage = "Could not start microphone.";
        });
      }
    } else {
      setState(() {
        _errorMessage = "Microphone permission denied.";
      });
    }
  }

  Future<void> _stopRecording() async {
    if (!_isRecording) return;
    try {
      String? path = await _audioRecorder.stop();
      setState(() {
        _isRecording = false;
        _isLoading = true;
      });
      if (path != null) {
        File audioFile = File(path);
        String? transcript = await ApiService.transcribeAudio(audioFile, language: _sourceLang);
        if (transcript != null && transcript.trim().isNotEmpty) {
          _inputController.text = transcript;
          await _translate();
          // Auto-play TTS if available
          if (_targetLang != 'ho') {
             await _playTts();
          }
        } else {
          setState(() {
            _isLoading = false;
            _errorMessage = "Speech could not be recognized.";
          });
        }
      }
    } catch (e) {
      setState(() {
        _isRecording = false;
        _isLoading = false;
        _errorMessage = "Recording stopped with error.";
      });
    }
  }
"""
if "_startRecording" not in content:
    content = content.replace("void _swapLanguages() {", recording_logic + "\n  void _swapLanguages() {")

# Add mic button next to translate button
mic_button = """
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _isLoading || !_isTranslationSupported ? null : _translate,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: _isLoading
                        ? const SizedBox(
                            height: 20, width: 20,
                            child: CircularProgressIndicator(strokeWidth: 2)
                          )
                        : Text(
                            (_sourceLang == 'ho' && _targetLang == 'hi')
                                ? 'Translate [Experimental]'
                                : 'Translate',
                            style: const TextStyle(fontSize: 18),
                          ),
                  ),
                ),
                const SizedBox(width: 10),
                GestureDetector(
                  onTapDown: (_) => _startRecording(),
                  onTapUp: (_) => _stopRecording(),
                  onTapCancel: () => _stopRecording(),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: _isRecording ? Colors.red : Colors.blue,
                      shape: BoxShape.circle,
                    ),
                    child: Icon(Icons.mic, color: Colors.white, size: 28),
                  ),
                ),
              ],
            ),
"""

if "GestureDetector(" not in content:
    import re
    content = re.sub(
        r"ElevatedButton\(\s*onPressed: _isLoading.*?\),",
        mic_button,
        content,
        flags=re.DOTALL
    )

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
print("translator_screen.dart patched successfully.")
