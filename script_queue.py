import os

filepath = 'android/lib/screens/classroom_screen.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports
import_target = "import 'package:path_provider/path_provider.dart';"
new_imports = '''import 'package:path_provider/path_provider.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'dart:async';'''

content = content.replace(import_target, new_imports)

# Add variables and initState
vars_target = "  final _ttsPlayer = TtsPlayerService();"
new_vars = '''  final _ttsPlayer = TtsPlayerService();

  StreamSubscription<List<ConnectivityResult>>? _connectivitySubscription;
  bool _isOnline = false;

  @override
  void initState() {
    super.initState();
    _checkInitialQueue();
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
      while (true) {
        if (!mounted) break;
        final job = await DatabaseService.instance.getLatestIncompleteJob();
        if (job == null) break;

        // Skip if internet dropped
        if (!_isOnline) break;

        int newCount = (job['retry_count'] as int? ?? 0) + 1;
        await DatabaseService.instance.updateClassroomJob(job['id'] as String, {'retry_count': newCount});
        
        final mutableJob = Map<String, dynamic>.from(job);
        mutableJob['retry_count'] = newCount;

        await _processClassroomJob(job['id'] as String, mutableJob);

        // Wait a tiny bit between jobs to prevent API flooding or UI locking
        await Future.delayed(const Duration(milliseconds: 500));
      }
    } finally {
      if (mounted) {
        _isQueueProcessing = false;
      }
    }
  }'''

content = content.replace(vars_target, new_vars)

# Update dispose
dispose_target = '''  @override
  void dispose() {
    _audioRecorder.dispose();'''
new_dispose = '''  @override
  void dispose() {
    _connectivitySubscription?.cancel();
    _audioRecorder.dispose();'''

content = content.replace(dispose_target, new_dispose)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
