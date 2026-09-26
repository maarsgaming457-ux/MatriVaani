import os

dart_code = '''
import 'dart:io';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:typed_data';

void main() async {
  String baseUrl = 'http://127.0.0.1:8000';
  print('Testing Backend Connection...');
  try {
    var res = await http.get(Uri.parse(baseUrl + '/health'));
    print('Health: ' + res.statusCode.toString());
  } catch (e) {
    print('Failed to connect: ' + e.toString());
  }
}
'''

with open('test_api.dart', 'w') as f:
    f.write(dart_code)
