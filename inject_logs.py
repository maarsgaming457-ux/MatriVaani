import re

filepath = r"C:\study_files\sih project\android\lib\screens\translator_screen.dart"
with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

# Add logging to startRecording
start_rec_replacement = """  Future<void> _startRecording() async {
    print('[MATRI-MIC] permission requested');
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      print('[MATRI-MIC] permission granted');
      try {
        Directory tempDir = await getTemporaryDirectory();
        String path = '${tempDir.path}/translator_audio_${DateTime.now().millisecondsSinceEpoch}.wav';
        print('[MATRI-MIC] recorder initialized at $path');
        await _audioRecorder.start(
          const RecordConfig(encoder: AudioEncoder.wav, sampleRate: 16000, numChannels: 1),
          path: path,
        );
        print('[MATRI-MIC] recording started');
        setState(() {
          _isRecording = true;
          _statusMessage = 'ðŸ”´ Listening...';
        });
      } catch (e) {
        print('[MATRI-MIC] recorder error: $e');
        setState(() {
          _statusMessage = "Unable to connect to MatriVaani server.\\nPlease check the connection.";
        });
      }
    } else {
      print('[MATRI-MIC] permission denied');
      setState(() {
        _statusMessage = "Microphone permission denied.";
      });
    }
  }"""

content = re.sub(
    r"  Future<void> _startRecording\(\) async \{.*?\n  \}\n",
    start_rec_replacement + "\n",
    content,
    flags=re.DOTALL
)

# Add logging to stopRecording
stop_rec_replacement = """  Future<void> _stopRecording() async {
    if (!_isRecording) return;
    try {
      print('[MATRI-MIC] recording stopped');
      String? path = await _audioRecorder.stop();
      setState(() {
        _isRecording = false;
        _isLoading = true;
        _statusMessage = 'Recognizing speech...';
      });
      if (path != null) {
        File audioFile = File(path);
        int fileSize = await audioFile.length();
        print('[MATRI-MIC] file path: $path');
        print('[MATRI-MIC] file size: $fileSize bytes');
        
        String? transcript = await ApiService.transcribeAudio(audioFile, language: _sourceLang);
        if (transcript != null && transcript.trim().isNotEmpty && !transcript.contains('[SILENCE DETECTED]')) {
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
        }
      }
    } catch (e) {
      print('[MATRI-MIC] stop recording error: $e');
      setState(() {
        _isRecording = false;
        _isLoading = false;
      });
    }
  }"""

content = re.sub(
    r"  Future<void> _stopRecording\(\) async \{.*?\n  \}\n",
    stop_rec_replacement + "\n",
    content,
    flags=re.DOTALL
)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)
