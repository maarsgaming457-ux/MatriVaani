import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import '../lib/main.dart';

void main() {
  Future<void> pumpApp(WidgetTester tester) async {
    await tester.pumpWidget(const MatriVaaniApp());
    await tester.pumpAndSettle();
  }

  /// Helper: scroll a [Scrollable] ancestor until [finder] is visible, then
  /// pump the widget tree. Works for items buried deep below the fold in a
  /// ListView / SingleChildScrollView.
  Future<void> scrollTo(
    WidgetTester tester,
    Finder finder, {
    Finder? scrollable,
  }) async {
    final scroll = scrollable ?? find.byType(Scrollable).first;

    // If the widget is already built/present, ensure it is visible without
    // assuming scroll direction.
    if (finder.evaluate().isNotEmpty) {
      await tester.ensureVisible(finder);
      await tester.pumpAndSettle();
      return;
    }

    // Try scrolling one direction first, then the opposite direction.
    try {
      await tester.scrollUntilVisible(
        finder,
        200,
        scrollable: scroll,
        maxScrolls: 50,
      );
    } catch (_) {
      await tester.scrollUntilVisible(
        finder,
        -200,
        scrollable: scroll,
        maxScrolls: 50,
      );
    }

    await tester.pumpAndSettle();
  }

  // ─── Tab navigation ───────────────────────────────────────────

  testWidgets('bottom navigation switches tabs', (tester) async {
    await pumpApp(tester);

    // Home is visible by default
    expect(find.textContaining('Learning'), findsOneWidget);

    // Home tab explicit tap
    await tester.tap(find.text('/ Home').first);
    await tester.pumpAndSettle();

    // Classroom tab via its icon key
    await tester.tap(find.byKey(const Key('nav_classroom')));
    await tester.pumpAndSettle();
    // The classroom screen shows 'FastAPI ASR Engine'
    expect(find.text('FastAPI ASR Engine'), findsOneWidget);

    // Flashcards tab
    await tester.tap(find.byKey(const Key('nav_flashcards')));
    await tester.pumpAndSettle();

    // Sync tab
    await tester.tap(find.byKey(const Key('nav_sync')));
    await tester.pumpAndSettle();
    // First visible text on sync screen
    expect(find.text('Local Mode Active'), findsOneWidget);
  });

  // ─── Home screen buttons ─────────────────────────────────────

  testWidgets('home buttons navigate/signal', (tester) async {
    await pumpApp(tester);

    // Scroll to hear-word button
    final hearBtn = find.byKey(const Key('home_btn_hear_word'));
    await scrollTo(tester, hearBtn);
    await tester.tap(hearBtn);
    await tester.pumpAndSettle();
    expect(find.text('Playing word pronunciation…'), findsOneWidget);

    // Start classroom button (may need scroll)
    final classroomBtn = find.byKey(const Key('home_btn_start_classroom'));
    await scrollTo(tester, classroomBtn);
    await tester.tap(classroomBtn);
    await tester.pumpAndSettle();
    expect(find.text('FastAPI ASR Engine'), findsOneWidget);

    // Go back home
    await tester.tap(find.byKey(const Key('nav_home')));
    await tester.pumpAndSettle();

    // Sync button on home
    final syncBtn = find.byKey(const Key('home_btn_sync'));
    await scrollTo(tester, syncBtn);
    await tester.tap(syncBtn);
    await tester.pumpAndSettle();
    expect(find.text('SYNC BUFFER'), findsOneWidget);
  });

  // ─── Classroom buttons ───────────────────────────────────────

  testWidgets('classroom buttons change state', (tester) async {
    await pumpApp(tester);

    // Go to classroom tab
    await tester.tap(find.byKey(const Key('nav_classroom')));
    await tester.pumpAndSettle();

    // Teacher prompt listen button
    final teacherBtn = find.byKey(const Key('classroom_btn_teacher_listen'));
    await scrollTo(tester, teacherBtn);
    await tester.tap(teacherBtn);
    await tester.pump(const Duration(milliseconds: 600));
    await tester.pumpAndSettle();
    expect(find.textContaining('Done'), findsOneWidget);

    // PTT press
    final ptt = find.byKey(const Key('classroom_ptt_button'));
    await scrollTo(tester, ptt);
    expect(ptt, findsOneWidget);
    await tester.press(ptt);
    await tester.pump(const Duration(milliseconds: 350));
    await tester.pumpAndSettle();

    // Save to SQLite
    final saveBtn = find.byKey(const Key('classroom_btn_save_sqlite'));
    await scrollTo(tester, saveBtn);
    await tester.tap(saveBtn);
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.text('Saved to SQLite (simulated)'), findsOneWidget);
    await tester.pumpAndSettle();

    // Dismiss any lingering snackbar before tapping Clear Feed
    await tester.pump(const Duration(milliseconds: 800));
    await tester.pumpAndSettle();

    // Clear Feed
    final clearBtn = find.byKey(const Key('classroom_btn_clear_feed'));
    await scrollTo(tester, clearBtn);
    await tester.tap(clearBtn, warnIfMissed: false);
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.text('Feed cleared'), findsOneWidget);
    await tester.pumpAndSettle();

    // Next Phrase
    final nextBtn = find.byKey(const Key('classroom_btn_next_phrase'));
    await scrollTo(tester, nextBtn);
    await tester.tap(nextBtn);
    await tester.pump(const Duration(milliseconds: 100));
    expect(find.text('Next phrase'), findsOneWidget);
    await tester.pumpAndSettle();
  });

  // ─── Flashcards buttons ──────────────────────────────────────

  testWidgets('flashcards buttons update UI', (tester) async {
    await pumpApp(tester);

    // Go to flashcards tab
    await tester.tap(find.byKey(const Key('nav_flashcards')));
    await tester.pumpAndSettle();

    // Tap Listen button
    final listenBtn = find.text('Listen •');
    await scrollTo(tester, listenBtn);
    await tester.tap(listenBtn);
    await tester.pumpAndSettle();

    // Mark known
    final knowBtn = find.text('I Know This! •');
    await scrollTo(tester, knowBtn);
    await tester.tap(knowBtn);
    await tester.pumpAndSettle();
    expect(find.textContaining('Marked as Known'), findsOneWidget);

    // Allow the SnackBar to expire so it doesn't block the next tap.
    await tester.pump(const Duration(seconds: 2));
    await tester.pumpAndSettle();

    // Next card
    final nextBtn = find.text('Next •');
    await scrollTo(tester, nextBtn);
    await tester.tap(nextBtn, warnIfMissed: false);
    await tester.pumpAndSettle();
    expect(find.textContaining('Card'), findsWidgets);
  });

  // ─── Sync buttons & toggles ──────────────────────────────────

  testWidgets('sync buttons and toggles work', (tester) async {
    await pumpApp(tester);

    // Go to sync tab
    await tester.tap(find.byKey(const Key('nav_sync')));
    await tester.pumpAndSettle();

    // Sync All
    final syncAllBtn = find.byKey(const Key('sync_btn_sync_all'));
    await scrollTo(tester, syncAllBtn);
    await tester.tap(syncAllBtn);
    await tester.pump(const Duration(milliseconds: 700));
    await tester.pumpAndSettle();
    expect(find.text('Sync completed ✓'), findsOneWidget);

    // Ping server
    final pingBtn = find.byKey(const Key('sync_btn_ping_server'));
    await scrollTo(tester, pingBtn);
    await tester.tap(pingBtn);
    await tester.pump(const Duration(milliseconds: 500));
    await tester.pumpAndSettle();
    expect(find.textContaining('Ping:'), findsOneWidget);

    // Clear cache
    final clearBtn = find.byKey(const Key('sync_btn_clear_cache'));
    await scrollTo(tester, clearBtn);
    await tester.tap(clearBtn);
    await tester.pumpAndSettle();
    expect(find.text('Cache cleared'), findsOneWidget);

    // Toggle switches (scroll to them first)
    final autoSyncText = find.text('Auto-sync when Wi-Fi is available');
    await scrollTo(tester, autoSyncText);
    await tester.tap(autoSyncText);
    await tester.pumpAndSettle();

    final rawWavText = find.text('Save raw 16kHz WAV audio files locally');
    await scrollTo(tester, rawWavText);
    await tester.tap(rawWavText);
    await tester.pumpAndSettle();
  });
}
