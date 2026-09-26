import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';
import 'dart:typed_data';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:flutter/foundation.dart';

class ApiService {
  static String get baseUrl {
    if (kIsWeb) {
      return dotenv.env['API_BASE_URL'] ?? "http://127.0.0.1:8000";
    }
    if (Platform.isAndroid) {
      return "http://10.0.2.2:8000";
    }
    return dotenv.env['API_BASE_URL'] ?? "http://127.0.0.1:8000";
  }

  static Future<bool> isOnline() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(Duration(seconds: 3));
      return response.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  static Future<String?> transcribeAudio(File audioFile,
      {String language = 'sat'}) async {
    try {
      print('[MATRI-ASR] file path: ${audioFile.path}');
      bool exists = await audioFile.exists();
      print('[MATRI-ASR] file exists: $exists');
      if (exists) {
        print('[MATRI-ASR] file size: ${await audioFile.length()}');
      }

      var request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/asr'),
      );

      String apiLang = 'hi';
      if (language == 'sat') apiLang = 'santali';
      if (language == 'ho') apiLang = 'ho';
      request.fields['language'] = apiLang;

      request.files.add(
        await http.MultipartFile.fromPath('file', audioFile.path),
      );

      print('[MATRI-ASR] upload started');
      var res = await request.send();
      print('[MATRI-ASR] upload completed');
      print('[MATRI-ASR] HTTP status: ${res.statusCode}');

      final responseData = await res.stream.bytesToString();
      print('[MATRI-ASR] transcript received: $responseData');

      if (res.statusCode == 200) {
        final data = json.decode(responseData);
        return data['transcript'];
      }

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
    if (sourceLang == 'hi' && targetLang == 'unr') {
      return await translateHindiToMundari(text);
    }
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

  static Future<Map<String, dynamic>?> translateExperimentalHo(
      String text) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/experimental/translate/ho-hi'),
            headers: {
              'Content-Type': 'application/json',
            },
            body: json.encode({
              'text': text,
            }),
          )
          .timeout(const Duration(seconds: 30));

      print(
          'DEBUG: Experimental Ho Translation HTTP status: ${response.statusCode}');
      print('DEBUG: Experimental Ho Translation response: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        return data;
      }

      print(
        'DEBUG: Experimental Ho Translation request failed: '
        '${response.statusCode} ${response.body}',
      );
      return null;
    } catch (e) {
      print('DEBUG: Experimental Ho Translation connection/error: $e');
      return null;
    }
  }

  static Future<String?> translateHindiToMundari(String text) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/translate/hindi-to-mundari'),
            headers: {
              'Content-Type': 'application/json',
            },
            body: json.encode({
              'text': text,
            }),
          )
          .timeout(const Duration(seconds: 30));

      print('DEBUG: Hindi-Mundari NMT HTTP status: ${response.statusCode}');
      print('DEBUG: Hindi-Mundari NMT response: ${response.body}');

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return data['translation'] as String?;
      }

      print(
        'DEBUG: Hindi-Mundari Translation request failed: '
        '${response.statusCode} ${response.body}',
      );

      return null;
    } catch (e) {
      print('DEBUG: Hindi-Mundari Translation connection/error: $e');
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

      print(
          'DEBUG: TTS request failed: ${response.statusCode} - ${response.body}');
      return null;
    } catch (e) {
      print('DEBUG: TTS connection error: $e');
      return null;
    }
  }

  static Future<List<dynamic>> syncData(
      List<Map<String, dynamic>> localChanges) async {
    // Kept for offline sync compatibility
    return [];
  }
}
