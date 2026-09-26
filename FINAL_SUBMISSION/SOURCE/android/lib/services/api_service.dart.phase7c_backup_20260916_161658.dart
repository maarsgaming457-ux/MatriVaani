import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter_dotenv/flutter_dotenv.dart';

class ApiService {
  static String get baseUrl => dotenv.env['API_BASE_URL'] ?? "http://10.0.2.2:8000";

  static Future<bool> isOnline() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health')).timeout(Duration(seconds: 3));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  static Future<String?> transcribeAudio(File audioFile, {String language = 'sat'}) async {
    try {
      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/asr'),
      );

      request.fields['language'] = language == 'sat' ? 'santali' : 'hi';

      request.files.add(
        await http.MultipartFile.fromPath('file', audioFile.path),
      );

      var res = await request.send();

      print('DEBUG: HTTP status: ${res.statusCode}');

      final responseData = await res.stream.bytesToString();

      print('DEBUG: Full API response: $responseData');

      if (res.statusCode == 200) {
        final data = json.decode(responseData);
        return data['transcript'];
      }

      print('DEBUG: ASR request failed: $responseData');
      return null;
    } catch (e) {
      print('DEBUG: ASR connection error: $e');
      return null;
    }
  }

  static Future<String?> translateText(
    String text,
    String sourceLang,
    String targetLang,
  ) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/translate'),
            headers: {
              'Content-Type': 'application/json',
            },
            body: json.encode({
              'text': text,
              'source_lang': sourceLang,
              'target_lang': targetLang,
            }),
          )
          .timeout(const Duration(seconds: 30));

      print('DEBUG: Translation HTTP status: ${response.statusCode}');
      print('DEBUG: Translation response: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['translation'] as String?;
      }

      print(
        'DEBUG: Translation request failed: '
        '${response.statusCode} ${response.body}',
      );

      return null;
    } catch (e) {
      print('DEBUG: Translation connection/error: $e');
      return null;
    }
  }

  static Future<Uint8List?> synthesizeSpeech(
    String text,
    String language, {
    String provider = 'sarvam',
  }) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/tts'),
            headers: {
              'Content-Type': 'application/json',
            },
            body: json.encode({
              'text': text,
              'language': language,
              'provider': provider,
            }),
          )
          .timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        return response.bodyBytes;
      }
      
      print('DEBUG: TTS request failed: ${response.statusCode} - ${response.body}');
      return null;
    } catch (e) {
      print('DEBUG: TTS connection error: $e');
      return null;
    }
  }

  static Future<List<dynamic>> syncData(List<Map<String, dynamic>> localChanges) async {
    // Kept for offline sync compatibility
    return [];
  }
}

