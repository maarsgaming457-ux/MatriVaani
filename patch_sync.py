import 'dart:io';

def patch_sync():
    filepath = r"C:\study_files\sih project\android\lib\screens\sync_screen.dart"
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    if "import '../services/api_service.dart';" not in content:
        content = content.replace("import 'package:flutter/material.dart';", "import 'package:flutter/material.dart';\nimport '../services/api_service.dart';")
    
    content = content.replace(
        "String _endpoint = 'http://10.0.2.2:8000';",
        "String _endpoint = ApiService.baseUrl;"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("sync_screen patched.")

patch_sync()
