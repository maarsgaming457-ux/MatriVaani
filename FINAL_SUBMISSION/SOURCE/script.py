import os

filepath = 'android/lib/screens/classroom_screen.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = '''        // Create ClassroomJob
        jobId = await DatabaseService.instance.createClassroomJob(
          sourceLang: _sourceLang,
          targetLang: _targetLang,
          audioPath: persistentPath,
        );'''

end_marker = '''        if (!mounted) return;
        setState(() {
          _isProcessing = false;
          _status = "Error processing audio (Online required)";
        });
      }'''

replacement = '''        // Create ClassroomJob
        jobId = await DatabaseService.instance.createClassroomJob(
          sourceLang: _sourceLang,
          targetLang: _targetLang,
          audioPath: persistentPath,
        );

        final job = await DatabaseService.instance.getClassroomJob(jobId);
        if (job != null) {
          await _processClassroomJob(jobId, job);
        }
      } catch (e) {
        if (jobId != null) {
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'FAILED',
            'last_error': e.toString(),
          });
        }
        if (!mounted) return;
        setState(() {
          _isProcessing = false;
          _status = "Error processing audio (Online required)";
        });
      }'''

start_idx = content.find(start_marker)
end_idx = content.find(end_marker) + len(end_marker)

if start_idx == -1 or end_idx == -1:
    print('Failed to find markers')
    exit(1)

content = content[:start_idx] + replacement + content[end_idx:]

clear_marker = '  void _clear() {'

new_methods = '''  Future<void> _processClassroomJob(String jobId, Map<String, dynamic> jobData) async {
    try {
      String source = jobData['source_lang'] as String;
      String target = jobData['target_lang'] as String;
      String status = jobData['status'] as String;
      
      String transcript = jobData['transcription'] as String? ?? "";
      String translation = jobData['translation'] as String? ?? "";

      setState(() {
        _sourceLang = source;
        _targetLang = target;
        _transcript = transcript;
        _translation = translation;
        _status = "Processing...";
        _isProcessing = true;
      });

      // 1. ASR Stage
      if (status == 'RECORDED' || status == 'ASR_FAILED' || status == 'FAILED') {
        String audioPath = jobData['audio_path'] as String;
        File file = File(audioPath);
        if (!await file.exists()) {
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'FAILED',
            'last_error': 'Audio file missing.'
          });
          setState(() {
            _isProcessing = false;
            _status = "Error: Audio file missing.";
          });
          return;
        }

        await DatabaseService.instance.updateClassroomJob(jobId, {'status': 'ASR_PENDING'});
        String? asrResult = await ApiService.transcribeAudio(file, language: source);
        if (!mounted) return;
        
        if (asrResult != null) {
          if (asrResult.trim().isEmpty) {
            await DatabaseService.instance.updateClassroomJob(jobId, {
              'status': 'ASR_FAILED',
              'last_error': 'Transcription empty.',
            });
            setState(() {
              _isProcessing = false;
              _status = "Error: Transcription empty.";
            });
            return;
          }
          transcript = asrResult;
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'TRANSLATING',
            'transcription': transcript,
          });
          setState(() {
            _transcript = transcript;
            _status = "Translating...";
          });
          status = 'TRANSLATING';
        } else {
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'ASR_FAILED',
            'last_error': 'Transcription failed.',
          });
          setState(() {
            _isProcessing = false;
            _status = "Error: Transcription failed.";
          });
          return;
        }
      }

      // 2. Translation Stage
      if (status == 'TRANSLATING' || status == 'TRANSLATION_FAILED') {
        String? translationResult = await ApiService.translateText(transcript, source, target);
        if (!mounted) return;
        
        if (translationResult != null) {
          if (translationResult.trim().isEmpty) {
            await DatabaseService.instance.updateClassroomJob(jobId, {
              'status': 'TRANSLATION_FAILED',
              'last_error': 'Translation empty.',
            });
            setState(() {
              _isProcessing = false;
              _status = "Error: Translation empty.";
            });
            return;
          }
          translation = translationResult;
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'COMPLETED',
            'translation': translation,
          });
          setState(() {
            _translation = translation;
            _status = "Playing Audio...";
          });
          status = 'COMPLETED';
        } else {
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'TRANSLATION_FAILED',
            'last_error': 'Translation failed.',
          });
          setState(() {
            _isProcessing = false;
            _status = "Error: Translation failed.";
          });
          return;
        }
      }

      // 3. TTS Stage
      if (status == 'COMPLETED' || status == 'TTS_UNAVAILABLE') {
        bool success = await _ttsPlayer.playTts(translation, target);
        if (!mounted) return;
        setState(() {
          _isProcessing = false;
          if (!success) {
            _status = "TTS is currently unavailable.";
          } else {
            _status = "Done";
          }
        });
      }
    } catch (e) {
      if (!mounted) return;
      await DatabaseService.instance.updateClassroomJob(jobId, {
        'status': 'FAILED',
        'last_error': e.toString(),
      });
      setState(() {
        _isProcessing = false;
        _status = "Error processing audio (Online required)";
      });
    }
  }

  Future<void> _retryLastFailedJob() async {
    if (_isProcessing || _isRecording) return;
    
    final job = await DatabaseService.instance.getLatestIncompleteJob();
    if (job == null) {
      setState(() {
        _status = "No failed jobs to retry.";
      });
      return;
    }

    int newCount = (job['retry_count'] as int? ?? 0) + 1;
    await DatabaseService.instance.updateClassroomJob(job['id'] as String, {'retry_count': newCount});
    
    final mutableJob = Map<String, dynamic>.from(job);
    mutableJob['retry_count'] = newCount;

    await _processClassroomJob(job['id'] as String, mutableJob);
  }

'''

content = content.replace(clear_marker, new_methods + clear_marker)

button_marker = '''            ElevatedButton(
              onPressed: _clear,
              child: const Text("Clear"),
            )'''

new_buttons = '''            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: _clear,
                  child: const Text("Clear"),
                ),
                ElevatedButton(
                  onPressed: _isProcessing || _isRecording ? null : _retryLastFailedJob,
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                  child: const Text("Retry Last Failed"),
                ),
              ],
            )'''

content = content.replace(button_marker, new_buttons)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
