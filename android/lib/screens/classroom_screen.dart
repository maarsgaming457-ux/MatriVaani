import 'package:flutter/material.dart';
import 'package:record/record.dart';
import 'package:permission_handler/permission_handler.dart';
import 'dart:io';
import '../services/api_service.dart';
import 'package:path_provider/path_provider.dart';

class ClassroomScreen extends StatefulWidget {
  @override
  _ClassroomScreenState createState() => _ClassroomScreenState();
}

class _ClassroomScreenState extends State<ClassroomScreen> {
  final AudioRecorder _audioRecorder = AudioRecorder();
  bool _isRecording = false;
  String _transcript = "";
  String _status = "Ready";

  @override
  void dispose() {
    _audioRecorder.dispose();
    super.dispose();
  }

  Future<void> _startRecording() async {
    var status = await Permission.microphone.request();
    if (status.isGranted) {
      Directory tempDir = await getTemporaryDirectory();
      String path = '${tempDir.path}/audio.wav';
      await _audioRecorder.start(
        const RecordConfig(encoder: AudioEncoder.wav),
        path: path,
      );
      if (!mounted) return;
      setState(() {
        _isRecording = true;
        _status = "Recording...";
      });
    } else {
      setState(() {
        _status = "Microphone Permission Denied!";
      });
    }
  }

  Future<void> _stopRecording() async {
    String? path = await _audioRecorder.stop();
    if (!mounted) return;
    setState(() {
      _isRecording = false;
      _status = "Processing...";
    });

    if (path != null) {
      try {
        File file = File(path);
        bool exists = await file.exists();
        int size = exists ? await file.length() : 0;

        if (size == 0) {
          setState(() {
            _status = "Error: Recorded file is empty.";
          });
          return;
        }

        String? transcript = await ApiService.transcribeAudio(file);
        if (!mounted) return;
        
        if (transcript != null) {
          setState(() {
            _transcript = transcript;
            _status = "Done";
          });
        } else {
          setState(() {
            _status = "Error: Transcription failed.";
          });
        }
      } catch (e) {
        if (!mounted) return;
        setState(() {
          _status = "Error processing audio (Online required)";
        });
      }
    }
  }

  void _clear() {
    setState(() {
      _transcript = "";
      _status = "Ready";
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
            const SizedBox(height: 20),
            Text("Status:\n$_status", textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue, fontSize: 16)),
            const SizedBox(height: 40),
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
            const SizedBox(height: 40),
            const Align(alignment: Alignment.centerLeft, child: Text("Santali Transcription:", style: TextStyle(fontWeight: FontWeight.bold))),
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
            ElevatedButton(
              onPressed: _clear,
              child: const Text("Clear"),
            )
          ],
        ),
      ),
    );
  }
}
