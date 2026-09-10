import 'package:flutter/material.dart';

class MatriVaaniColors {
  // Warm earth / terracotta
  static const Color primary = Color(0xFFA63F1B);
  static const Color primaryDark = Color(0xFF8B2E0F);

  // Forest green
  static const Color forest = Color(0xFF2D6A4F);
  static const Color forest2 = Color(0xFF387B57);

  // Cream / background
  static const Color background = Color(0xFFF7F8FC);
  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceAlt = Color(0xFFFFF7F2);

  // Amber / gold
  static const Color amber = Color(0xFFEAA034);

  // Text
  static const Color ink = Color(0xFF1C1B1F);
  static const Color muted = Color(0xFF6B6A70);

  // Borders/shadows
  static const Color border = Color(0xFFE7E1DD);
  static const Color shadow = Color(0x19000000);
}

class MatriVaaniTheme {
  static ThemeData build({bool isDark = false}) {
    final base = ThemeData(
      useMaterial3: true,
      scaffoldBackgroundColor: MatriVaaniColors.background,
      colorScheme: ColorScheme.fromSeed(seedColor: MatriVaaniColors.primary),
      textTheme: const TextTheme(
        headlineSmall: TextStyle(fontSize: 20, fontWeight: FontWeight.w700),
        titleMedium: TextStyle(fontSize: 16, fontWeight: FontWeight.w600),
        bodyLarge: TextStyle(fontSize: 14, fontWeight: FontWeight.w400),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
    );

    return base.copyWith(
      cardTheme: CardThemeData(
        color: MatriVaaniColors.surface,
        elevation: 2,
        shadowColor: MatriVaaniColors.shadow,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(18),
          side: const BorderSide(color: MatriVaaniColors.border),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          elevation: 0,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
          backgroundColor: MatriVaaniColors.primary,
          foregroundColor: Colors.white,
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
          textStyle: const TextStyle(fontSize: 15, fontWeight: FontWeight.w700),
        ),
      ),
      outlinedButtonTheme: OutlinedButtonThemeData(
        style: OutlinedButton.styleFrom(
          foregroundColor: MatriVaaniColors.primary,
          side: const BorderSide(color: MatriVaaniColors.primary),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(18),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
        ),
      ),
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          backgroundColor: MatriVaaniColors.primary,
          foregroundColor: Colors.white,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(18)),
          padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
        ),
      ),
      sliderTheme: const SliderThemeData(
        trackHeight: 8,
        activeTrackColor: MatriVaaniColors.primary,
        inactiveTrackColor: MatriVaaniColors.border,
        thumbShape: RoundSliderThumbShape(enabledThumbRadius: 12),
        overlayShape: RoundSliderOverlayShape(overlayRadius: 22),
      ),
    );
  }
}
