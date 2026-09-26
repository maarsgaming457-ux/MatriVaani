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
import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

enum RecordState {
  idle,
  starting,
  recording,
  stopping,
  processing,
  success,
  error
}

class ClassroomScreen extends StatefulWidget {
  const ClassroomScreen({super.key});

  @override
  State<ClassroomScreen> createState() => _ClassroomScreenState();
}

class _ClassroomScreenState extends State<ClassroomScreen> {
  int _step = 1;
  RecordState _state = RecordState.idle;

  bool get _isRecording => _state == RecordState.recording;
  bool get _isProcessing =>
      _state == RecordState.starting ||
      _state == RecordState.stopping ||
      _state == RecordState.processing;

  String _status = 'Ready';
  String _teacherPrompt = 'Amag ÃƒÂ±utum ched?';
  String _asrOutput = 'Ã¡Â±Â¢Ã¡Â±Å¡Ã¡Â±Â¡ Ã¡Â±Å¸Ã¡Â±Â¨Ã¡Â±Â®';
  String _translation = 'InyÃ¡ÂºÂ¡g ÃƒÂ±utum dÃ‰â€ Sona Marandi.';
  double _audioProgress = 0.35;

  String _ttsProvider = 'sarvam';
  final _ttsPlayer = TtsPlayerService();
  final _audioRecorder = AudioRecorder();

  StreamSubscription<List<ConnectivityResult>>? _connectivitySubscription;
  bool _isOnline = false;

  @override
  void initState() {
    super.initState();
    _cleanupOldJobs().then((_) {
      _checkInitialQueue();
    });
    _connectivitySubscription = Connectivity()
        .onConnectivityChanged
        .listen((List<ConnectivityResult> results) {
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
      final expiredJobs =
          await DatabaseService.instance.getExpiredCompletedJobs(cutoff);

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
        final currentJob =
            await DatabaseService.instance.getClassroomJob(job['id'] as String);
        if (currentJob == null || currentJob['status'] == 'COMPLETED') continue;

        int newCount = (currentJob['retry_count'] as int? ?? 0) + 1;
        await DatabaseService.instance.updateClassroomJob(
            currentJob['id'] as String, {'retry_count': newCount});

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

  Future<void> _startRecording() async {
    if (_state != RecordState.idle &&
        _state != RecordState.success &&
        _state != RecordState.error) return;

    _ttsPlayer.stop();
    setState(() {
      _state = RecordState.starting;
      _status = "माइक्रोफ़ोन शुरू हो रहा है…";
    });

    print('[MATRI-ASR] recording start requested');
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      try {
        Directory tempDir = await getTemporaryDirectory();
        String path =
            '${tempDir.path}/audio_${DateTime.now().millisecondsSinceEpoch}.wav';
        print('[MATRI-ASR] recording start. Path: $path');
        await _audioRecorder.start(
          const RecordConfig(
              encoder: AudioEncoder.wav, sampleRate: 16000, numChannels: 1),
          path: path,
        );
        if (!mounted) return;
        setState(() {
          _state = RecordState.recording;

          _translation = "";
          _status = "रिकॉर्डिंग हो रही है…";
        });
      } catch (e) {
        if (!mounted) return;
        setState(() {
          _state = RecordState.error;
          _status = "Could not start the microphone.";
        });
        print('[MATRI-ASR] error starting recorder: $e');
      }
    } else {
      if (!mounted) return;
      setState(() {
        _state = RecordState.error;
        _status = "Microphone permission denied.";
      });
    }
  }

  Future<String?> _stopRecording() async {
    if (_state != RecordState.recording) return null;

    setState(() {
      _state = RecordState.stopping;
      _status = "रुक रहा है…";
    });

    print('[MATRI-ASR] recording stop requested');
    try {
      String? path = await _audioRecorder.stop();
      print('[MATRI-ASR] recording stopped');
      return path;
    } catch (e) {
      print('[MATRI-ASR] error stopping recorder: $e');
      return null;
    }
  }

  Future<void> _simulateSpeak() async {
    setState(() {
      _status = 'ListeningÃ¢â‚¬Â¦';
    });
    await Future.delayed(const Duration(milliseconds: 550));
    if (!mounted) return;

    setState(() {
      _status = 'Done';
      _asrOutput = 'Ã¡Â±Â«Ã¡Â±Å¸Ã¡Â±Â¨Ã¡Â±Â® Dare';
      _translation = 'InyÃ¡ÂºÂ¡g ÃƒÂ±utum dÃ‰â€ Sona Marandi.';
    });
  }

  void _onRecordStop() async {
    setState(() {
      _state = RecordState.idle;
      _state = RecordState.processing;
      _status = "प्रोसेसिंग…";
    });

    String? path = await _stopRecording();

    if (path != null) {
      String? jobId;
      try {
        File file = File(path);
        bool exists = await file.exists();
        int size = exists ? await file.length() : 0;
        print('DEBUG: file size: $size bytes');

        if (size == 0) {
          setState(() {
            _state = RecordState.idle;
            _status = "Error: Recorded file is empty.";
          });
          return;
        }

        // Persist the audio file
        Directory appDir = await getApplicationDocumentsDirectory();
        String persistentPath =
            '${appDir.path}/audio_${DateTime.now().millisecondsSinceEpoch}.wav';
        await file.copy(persistentPath);
        // File persistentFile = File(persistentPath);

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
          _state = RecordState.idle;
          _status = "Error processing audio (Online required)";
        });
      }
    } else {
      setState(() {
        _state = RecordState.idle;
        _status = "Error: Recording failed.";
      });
    }
  }

  Future<void> _processClassroomJob(
      String jobId, Map<String, dynamic> jobData) async {
    try {
      String source = jobData['source_lang'] as String;
      String target = jobData['target_lang'] as String;
      String status = jobData['status'] as String;

      String transcript = jobData['transcription'] as String? ?? "";
      String translation = jobData['translation'] as String? ?? "";

      setState(() {
        _sourceLang = source;
        _targetLang = target;

        _translation = translation;
        _asrOutput = transcript.isNotEmpty ? transcript : _asrOutput;
        _status = "प्रोसेसिंग…";
        _state = RecordState.processing;
      });

      // 1. ASR Stage
      if (status == 'RECORDED' ||
          status == 'ASR_FAILED' ||
          status == 'FAILED') {
        String audioPath = jobData['audio_path'] as String;
        File file = File(audioPath);
        if (!await file.exists()) {
          await DatabaseService.instance.updateClassroomJob(
              jobId, {'status': 'FAILED', 'last_error': 'Audio file missing.'});
          setState(() {
            _state = RecordState.idle;
            _status = "Error: Audio file missing.";
          });
          return;
        }

        await DatabaseService.instance
            .updateClassroomJob(jobId, {'status': 'ASR_PENDING'});
        String? asrResult =
            await ApiService.transcribeAudio(file, language: source);
        if (!mounted) return;

        if (asrResult != null) {
          if (asrResult.trim().isEmpty) {
            await DatabaseService.instance.updateClassroomJob(jobId, {
              'status': 'ASR_FAILED',
              'last_error': 'Transcription empty.',
            });
            setState(() {
              _state = RecordState.idle;
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
              _state = RecordState.idle;
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
            _asrOutput = transcript;
            _status = "Translating...";
          });
          status = 'TRANSLATING';
        } else {
          await DatabaseService.instance.updateClassroomJob(jobId, {
            'status': 'ASR_FAILED',
            'last_error': 'Transcription failed.',
          });
          setState(() {
            _state = RecordState.idle;
            _status = "Error: Transcription failed.";
          });
          return;
        }
      }

      // 2. Translation Stage
      if (status == 'TRANSLATING' || status == 'TRANSLATION_FAILED') {
        String? translationResult =
            await ApiService.translateText(transcript, source, target);
        if (!mounted) return;

        if (translationResult != null) {
          if (translationResult.trim().isEmpty) {
            await DatabaseService.instance.updateClassroomJob(jobId, {
              'status': 'TRANSLATION_FAILED',
              'last_error': 'Translation empty.',
            });
            setState(() {
              _state = RecordState.idle;
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
            _state = RecordState.idle;
            _status = "Error: Translation failed.";
          });
          return;
        }
      }

      // 3. TTS Stage
      if (status == 'COMPLETED' || status == 'TTS_UNAVAILABLE') {
        bool success = await _ttsPlayer.playTts(translation, target,
            provider: _ttsProvider);
        if (!mounted) return;
        setState(() {
          _state = RecordState.idle;
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
        _state = RecordState.idle;
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
    await DatabaseService.instance
        .updateClassroomJob(job['id'] as String, {'retry_count': newCount});

    final mutableJob = Map<String, dynamic>.from(job);
    mutableJob['retry_count'] = newCount;

    await _processClassroomJob(job['id'] as String, mutableJob);
  }

  void _clear() {
    setState(() {
      _translation = "";
      _asrOutput = "";
      _status = "बोलने के लिए दबाएँ";
      _state = RecordState.idle;
      _state = RecordState.idle;
      _ttsPlayer.stop();
    });
  }

  void _saveToSQLite() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Saved to SQLite (simulated)'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  void _clearFeed() {
    _clear();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Feed cleared'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  void _nextPhrase() {
    setState(() {
      _step = (_step % 3) + 1;
      _teacherPrompt = _step == 1 ? 'Amag ÃƒÂ±utum ched?' : 'Amag sutum ched?';
      _asrOutput = _step == 1
          ? 'Ã¡Â±Â«Ã¡Â±Å¸Ã¡Â±Â¨Ã¡Â±Â® Dare'
          : 'Ã¡Â±Â¥Ã¡Â±Å¸Ã¡Â±Â¨Ã¡Â±Å¸Ã¡Â±Â¹';
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Next phrase'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 24),
      children: [
        // Top server status
        Row(
          children: [
            Expanded(
              child: Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(
                  color: MatriVaaniColors.forest2.withValues(alpha: 0.15),
                  border: Border.all(
                      color: MatriVaaniColors.forest2.withValues(alpha: 0.35)),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.cloud_done_outlined,
                        color: MatriVaaniColors.forest, size: 18),
                    SizedBox(width: 8),
                    Text('FastAPI ASR Engine',
                        style: TextStyle(
                            color: MatriVaaniColors.forest,
                            fontWeight: FontWeight.w900,
                            fontSize: 13)),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: MatriVaaniColors.surface,
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: MatriVaaniColors.border),
              ),
              child: const Text('240ms',
                  style: TextStyle(
                      fontWeight: FontWeight.w900,
                      color: MatriVaaniColors.primaryDark,
                      fontSize: 12)),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: MatriVaaniColors.forest.withValues(alpha: 0.25),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(
                    color: MatriVaaniColors.forest.withValues(alpha: 0.35)),
              ),
              child: const Text('16kHz Mono',
                  style: TextStyle(
                      fontWeight: FontWeight.w900,
                      color: MatriVaaniColors.forest,
                      fontSize: 12)),
            ),
          ],
        ),

        const SizedBox(height: 14),

        // Controls
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Row(
              children: [
                Text(_sourceLang == 'sat' ? "Santali" : "Hindi",
                    style: const TextStyle(fontWeight: FontWeight.bold)),
                IconButton(
                  icon: const Icon(Icons.swap_horiz,
                      color: MatriVaaniColors.primaryDark),
                  onPressed: _swapLanguages,
                  tooltip: 'Swap languages',
                ),
                Text(_targetLang == 'sat' ? "Santali" : "Hindi",
                    style: const TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
            ElevatedButton(
              onPressed:
                  _isProcessing || _isRecording ? null : _retryLastFailedJob,
              style: ElevatedButton.styleFrom(
                backgroundColor: MatriVaaniColors.amber,
                foregroundColor: MatriVaaniColors.primaryDark,
                elevation: 0,
              ),
              child: const Text("Retry Failed",
                  style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),

        const SizedBox(height: 14),

        // Lesson step header
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: MatriVaaniColors.surface,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: MatriVaaniColors.border),
              ),
              child: const Text('Lesson 02: Introduction',
                  style: TextStyle(
                      fontWeight: FontWeight.w900,
                      color: MatriVaaniColors.primaryDark)),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: MatriVaaniColors.amber.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: MatriVaaniColors.amber),
              ),
              child: Text('Step $_step/3',
                  style: const TextStyle(
                      fontWeight: FontWeight.w900,
                      color: MatriVaaniColors.primaryDark)),
            )
          ],
        ),

        const SizedBox(height: 12),

        // Teacher prompt
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Teacher Prompt Ã¢â‚¬Â¢',
                    style: TextStyle(
                        fontWeight: FontWeight.w900,
                        color: MatriVaaniColors.primaryDark)),
                const SizedBox(height: 10),
                Row(
                  children: [
                    PressScale(
                      key: const Key('classroom_btn_teacher_listen'),
                      onTap: _simulateSpeak,
                      child: Container(
                        decoration: BoxDecoration(
                          color:
                              MatriVaaniColors.forest.withValues(alpha: 0.12),
                          borderRadius: BorderRadius.circular(999),
                          border: Border.all(
                              color: MatriVaaniColors.forest
                                  .withValues(alpha: 0.25)),
                        ),
                        padding: const EdgeInsets.all(8),
                        child: const Icon(
                          Icons.play_circle_outline_rounded,
                          color: MatriVaaniColors.forest,
                          size: 34,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                              'Ã¡Â±Â¢Ã¡Â±Å¡Ã¡Â±Â¦Ã¡Â±Å¸Ã¡Â±Â¹ : Ã¡Â±Â¥Ã¡Â±Å¸Ã¡Â±Â±Ã¡Â±Å¸Ã¡Â±Â¹ Ã¡Â±Â¢Ã¡Â±Â¤Ã¡Â±Å¸Ã¡Â±Â¨ ?',
                              style: TextStyle(
                                  fontSize: 16,
                                  fontWeight: FontWeight.w900,
                                  color: MatriVaaniColors.ink)),
                          const SizedBox(height: 6),
                          Text('Speak: "$_teacherPrompt" (What is your name?)',
                              style: TextStyle(
                                  color: MatriVaaniColors.muted,
                                  fontWeight: FontWeight.w700)),
                          const SizedBox(height: 8),
                          Text('Status: $_status',
                              style: TextStyle(
                                  color: MatriVaaniColors.primaryDark,
                                  fontWeight: FontWeight.w900,
                                  fontSize: 12)),
                        ],
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),
        ),

        const SizedBox(height: 12),

        // Your Santali Speech card
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    CircleAvatar(
                      radius: 18,
                      backgroundColor:
                          MatriVaaniColors.forest.withValues(alpha: 0.16),
                      child: const Icon(Icons.mic_none_rounded,
                          color: MatriVaaniColors.forest),
                    ),
                    const SizedBox(width: 10),
                    Text('Your Santali',
                        style: const TextStyle(
                            fontWeight: FontWeight.w900,
                            color: MatriVaaniColors.primaryDark)),
                    const Spacer(),
                    Chip(
                      label: const Text('98% Match',
                          style: TextStyle(fontWeight: FontWeight.w900)),
                      backgroundColor:
                          MatriVaaniColors.forest.withValues(alpha: 0.14),
                      side: BorderSide(
                          color:
                              MatriVaaniColors.forest.withValues(alpha: 0.35)),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                const Text('OL CHIKI ASR OUTPUT',
                    style: TextStyle(
                        color: MatriVaaniColors.primaryDark,
                        fontWeight: FontWeight.w900,
                        fontSize: 12)),
                const SizedBox(height: 6),
                Text(_asrOutput,
                    style: const TextStyle(
                        fontSize: 20, fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                Text('Auto-Punctuation: ON',
                    style: TextStyle(
                        color: MatriVaaniColors.muted,
                        fontWeight: FontWeight.w700,
                        fontSize: 12)),
                const SizedBox(height: 10),
                Row(
                  children: [
                    PressScale(
                      key: const Key('classroom_btn_play_pause'),
                      onTap: () {
                        setState(() => _audioProgress =
                            (_audioProgress < 1.0) ? 1.0 : 0.0);
                      },
                      child: const Padding(
                        padding: EdgeInsets.all(8),
                        child: Icon(Icons.play_circle_outline_rounded),
                      ),
                    ),
                    Expanded(
                      child: Slider(
                        value: _audioProgress.clamp(0.0, 1.0),
                        onChanged: (v) => setState(() => _audioProgress = v),
                        activeColor: MatriVaaniColors.primary,
                        inactiveColor: MatriVaaniColors.border,
                      ),
                    ),
                    Text('${(_audioProgress * 3.2).toStringAsFixed(1)}s',
                        style: const TextStyle(
                            color: MatriVaaniColors.muted,
                            fontWeight: FontWeight.w800)),
                  ],
                ),
                const SizedBox(height: 8),
                Text('"$_translation"',
                    style: TextStyle(
                        color: MatriVaaniColors.muted,
                        fontWeight: FontWeight.w800)),
              ],
            ),
          ),
        ),

        const SizedBox(height: 20),

        // PTT Button Center
        Center(
          child: Column(
            children: [
              PttButton(
                isRecording: _isRecording,
                onRecordStart: _startRecording,
                onRecordStop: _onRecordStop,
              ),
              const SizedBox(height: 12),
              Text(
                (_state == RecordState.idle ||
                        _state == RecordState.success ||
                        _state == RecordState.error)
                    ? 'बोलने के लिए दबाएँ'
                    : _status,
                style: const TextStyle(
                  color: MatriVaaniColors.muted,
                  fontWeight: FontWeight.w700,
                  fontSize: 14,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 24),

        // Actions: Save / Clear / Next
        Row(
          children: [
            Expanded(
              child: AnimatedButton.outlined(
                key: const Key('classroom_btn_save_sqlite'),
                onPressed: _saveToSQLite,
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.save_alt_rounded, size: 18),
                    SizedBox(width: 6),
                    Text('Save to SQLite'),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: AnimatedButton.outlined(
                key: const Key('classroom_btn_clear_feed'),
                onPressed: _clearFeed,
                borderColor: MatriVaaniColors.muted,
                foregroundColor: MatriVaaniColors.muted,
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.delete_outline_rounded, size: 18),
                    SizedBox(width: 6),
                    Text('Clear Feed'),
                  ],
                ),
              ),
            ),
          ],
        ),

        const SizedBox(height: 12),

        AnimatedButton.elevated(
          key: const Key('classroom_btn_next_phrase'),
          onPressed: _nextPhrase,
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Next phrase'),
              SizedBox(width: 6),
              Icon(Icons.arrow_forward_rounded, size: 18),
            ],
          ),
        ),
      ],
    );
  }
}
