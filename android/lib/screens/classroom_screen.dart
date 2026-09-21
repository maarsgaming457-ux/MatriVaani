import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import '../services/api_service.dart';
import '../services/tts_player_service.dart';
import '../services/db_service.dart';
import 'package:path_provider/path_provider.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'dart:async';

class ClassroomScreen extends StatefulWidget {
  @override
  _ClassroomScreenState createState() => _ClassroomScreenState();
}

class _ClassroomScreenState extends State<ClassroomScreen> {
  final AudioRecorder _audioRecorder = AudioRecorder();
  bool _isRecording = false;
  String _transcript = "";
  String _translation = "";
  String _ttsProvider = 'sarvam';
  String _status = "Ready";
  final _ttsPlayer = TtsPlayerService();

  StreamSubscription<List<ConnectivityResult>>? _connectivitySubscription;
  bool _isOnline = false;

  @override
  void initState() {
    super.initState();
    _cleanupOldJobs().then((_) {
      _checkInitialQueue();
    });
    _connectivitySubscription = Connectivity().onConnectivityChanged.listen((List<ConnectivityResult> results) {
      bool online = results.any((r) => r != ConnectivityResult.none);
      if (online && !_isOnline) {
        _isOnline = true;
        _processQueue();
      } else if (!online) {
        _isOnline = false;
      }
    });
  }

  Future<void> _cleanupOldJobs() async {
    try {
      final cutoff = DateTime.now().subtract(const Duration(days: 7));
      final expiredJobs = await DatabaseService.instance.getExpiredCompletedJobs(cutoff);
      
      for (var job in expiredJobs) {
        String? audioPath = job['audio_path'] as String?;
        if (audioPath != null) {
          final file = File(audioPath);
          if (await file.exists()) {
            try {
              await file.delete();
            } catch (e) {
              print('DEBUG: Failed to delete audio for job \${job["id"]}: \$e');
              continue; // Do NOT delete DB row if audio deletion failed
            }
          }
        }
        await DatabaseService.instance.deleteClassroomJob(job['id'] as String);
      }
    } catch (e) {
      print('DEBUG: Cleanup error: ');
    }
  }

  Future<void> _checkInitialQueue() async {
    final results = await Connectivity().checkConnectivity();
    bool online = results.any((r) => r != ConnectivityResult.none);
    if (online) {
      _isOnline = true;
      _processQueue();
    }
  }

  bool _isQueueProcessing = false;

  Future<void> _processQueue() async {
    if (_isQueueProcessing || _isRecording || _isProcessing) return;
    _isQueueProcessing = true;

    try {
      final jobs = await DatabaseService.instance.getAllIncompleteJobs();
      for (var job in jobs) {
        if (!mounted) break;
        if (!_isOnline) break;

        // Double check status in case it was modified elsewhere
        final currentJob = await DatabaseService.instance.getClassroomJob(job['id'] as String);
        if (currentJob == null || currentJob['status'] == 'COMPLETED') continue;

        int newCount = (currentJob['retry_count'] as int? ?? 0) + 1;
        await DatabaseService.instance.updateClassroomJob(currentJob['id'] as String, {'retry_count': newCount});
        
        final mutableJob = Map<String, dynamic>.from(currentJob);
        mutableJob['retry_count'] = newCount;

        await _processClassroomJob(currentJob['id'] as String, mutableJob);

        await Future.delayed(const Duration(milliseconds: 500));
      }
    } finally {
      if (mounted) {
        _isQueueProcessing = false;
      }
    }
  }

  String _sourceLang = 'sat';
  String _targetLang = 'hi';

  void _swapLanguages() {
    if (_isProcessing || _isRecording) return;
    setState(() {
      final temp = _sourceLang;
      _sourceLang = _targetLang;
      _targetLang = temp;
      _clear();
    });
  }

  @override
  void dispose() {
    _connectivitySubscription?.cancel();
    _audioRecorder.dispose();
    _ttsPlayer.dispose();
    super.dispose();
  }

  bool _isProcessing = false;

  Future<void> _startRecording() async {
    if (_isProcessing) return;
    
    _ttsPlayer.stop();

    print('DEBUG: recording started');
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      Directory tempDir = await getTemporaryDirectory();
      String path = '${tempDir.path}/audio.wav';
      print('DEBUG: recording file/path: $path');
      await _audioRecorder.start(
        const RecordConfig(encoder: AudioEncoder.wav, sampleRate: 16000, numChannels: 1),
        path: path,
      );
      if (!mounted) return;
      setState(() {
        _isRecording = true;
        _transcript = "";
        _translation = "";
        _status = "Recording...";
      });
    } else {
      setState(() {
        _status = "Microphone Permission Denied!";
      });
    }
  }

  Future<void> _stopRecording() async {
    if (!_isRecording) return;
    
    String? path = await _audioRecorder.stop();
    print('DEBUG: recording stopped');
    if (!mounted) return;
    setState(() {
      _isRecording = false;
      _isProcessing = true;
      _status = "Processing...";
    });

    if (path != null) {
      String? jobId;
      try {
        File file = File(path);
        bool exists = await file.exists();
        int size = exists ? await file.length() : 0;
        print('DEBUG: file size: $size bytes');

        if (size == 0) {
          setState(() {
            _isProcessing = false;
            _status = "Error: Recorded file is empty.";
          });
          return;
        }

        // Persist the audio file
        Directory appDir = await getApplicationDocumentsDirectory();
        String persistentPath = '${appDir.path}/audio_${DateTime.now().millisecondsSinceEpoch}.wav';
        await file.copy(persistentPath);
        File persistentFile = File(persistentPath);

        // Create ClassroomJob
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
      }
    } else {
      setState(() {
        _isProcessing = false;
        _status = "Error: Recording failed.";
      });
    }
  }

  Future<void> _processClassroomJob(String jobId, Map<String, dynamic> jobData) async {
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
          if (asrResult.trim() == "[SILENCE DETECTED]") {
            await DatabaseService.instance.updateClassroomJob(jobId, {
              'status': 'ASR_FAILED',
              'last_error': 'No speech detected.',
            });
            setState(() {
              _isProcessing = false;
              _status = "No speech detected. Please try again.";
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
        bool success = await _ttsPlayer.playTts(translation, target, provider: _ttsProvider);
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

  void _clear() {
    setState(() {
      _transcript = "";
      _translation = "";
      _status = "Ready";
      _isProcessing = false;
      _isRecording = false;
      _ttsPlayer.stop();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Santali Voice Assistant')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const SizedBox(height: 10),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(_sourceLang == 'sat' ? "Santali" : "Hindi", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                IconButton(
                  icon: const Icon(Icons.swap_horiz, size: 32),
                  onPressed: _swapLanguages,
                  tooltip: 'Swap languages',
                ),
                Text(_targetLang == 'sat' ? "Santali" : "Hindi", style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ],
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
            Text("Status:\n$_status", textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue, fontSize: 16)),
            const SizedBox(height: 20),
            GestureDetector(
              onTapDown: (_) => _startRecording(),
              onTapUp: (_) => _stopRecording(),
              child: CircleAvatar(
                radius: 60,
                backgroundColor: _isRecording ? Colors.red : Colors.green,
                child: const Icon(Icons.mic, size: 50, color: Colors.white),
              ),
            ),
            const SizedBox(height: 20),
            Text(_isRecording ? "Release to Stop Recording" : "Hold to Start Recording", style: const TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),
            Align(alignment: Alignment.centerLeft, child: Text("${_sourceLang == 'sat' ? 'Santali' : 'Hindi'} Transcription:", style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 10),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8.0),
              ),
              child: Text(
                _transcript.isEmpty ? "..." : _transcript,
                style: const TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 20),
            Align(alignment: Alignment.centerLeft, child: Text("${_targetLang == 'sat' ? 'Santali' : 'Hindi'} Translation:", style: const TextStyle(fontWeight: FontWeight.bold))),
            const SizedBox(height: 10),
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(16.0),
              decoration: BoxDecoration(
                border: Border.all(color: Colors.grey),
                borderRadius: BorderRadius.circular(8.0),
              ),
              child: Text(
                _translation.isEmpty ? "..." : _translation,
                style: const TextStyle(fontSize: 18),
              ),
            ),
            const SizedBox(height: 20),
            Row(
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
            )
          ],
        ),
      ),
    );
  }
}


