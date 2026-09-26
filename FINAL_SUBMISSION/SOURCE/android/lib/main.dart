import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'screens/main_navigation_shell.dart';
import 'theme/app_theme.dart';

Future<void> main() async {
  await dotenv.load(fileName: '.env', isOptional: true);
  runApp(const MatriVaaniApp());
}

class MatriVaaniApp extends StatelessWidget {
  const MatriVaaniApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MatriVaani',
      debugShowCheckedModeBanner: false,
      theme: MatriVaaniTheme.build(),
      home: MainNavigationShell(),
    );
  }
}
