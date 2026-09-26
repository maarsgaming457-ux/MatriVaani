import 'dart:typed_data';
import 'package:audioplayers/audioplayers.dart';
import 'api_service.dart';

class TtsPlayerService {
  final AudioPlayer _audioPlayer = AudioPlayer();
  bool _isPlaying = false;

  bool get isPlaying => _isPlaying;

  Future<bool> playTts(String text, String language, {String provider = 'sarvam'}) async {
    try {
      final Uint8List? audioBytes = await ApiService.synthesizeSpeech(text, language, provider: provider);
      
      if (audioBytes == null || audioBytes.isEmpty) {
        return false;
      }

      await _audioPlayer.play(BytesSource(audioBytes));
      _isPlaying = true;

      _audioPlayer.onPlayerComplete.listen((event) {
        _isPlaying = false;
      });

      return true;
    } catch (e) {
      print('DEBUG: TtsPlayerService playback error: $e');
      _isPlaying = false;
      return false;
    }
  }

  Future<void> stop() async {
    await _audioPlayer.stop();
    _isPlaying = false;
  }

  void dispose() {
    _audioPlayer.dispose();
  }
}
