import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';
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

  static Future<String?> transcribeAudio(File audioFile) async {
    var request = http.MultipartRequest('POST', Uri.parse('$baseUrl/transcribe'));
    request.files.add(await http.MultipartFile.fromPath('file', audioFile.path));
    var res = await request.send();
    if (res.statusCode == 200) {
      var responseData = await res.stream.bytesToString();
      return json.decode(responseData)['transcription'];
    }
    return null;
  }

  static Future<List<dynamic>> syncData(List<Map<String, dynamic>> localChanges) async {
    // Kept for offline sync compatibility
    return [];
  }
}
