import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

class ClassroomScreen extends StatefulWidget {
  const ClassroomScreen({super.key});

  @override
  State<ClassroomScreen> createState() => _ClassroomScreenState();
}

class _ClassroomScreenState extends State<ClassroomScreen> {
  int _step = 1;

  String _status = 'Ready';
  String _teacherPrompt = 'Amag ñutum ched?';
  String _asrOutput = 'ᱢᱚᱡ ᱟᱨᱮ';
  String _translation = 'Inyạg ñutum dɔ Sona Marandi.';
  double _audioProgress = 0.35;
  bool _isRecording = false;

  Future<void> _simulateSpeak() async {
    setState(() {
      _status = 'Listening…';
    });
    await Future.delayed(const Duration(milliseconds: 550));
    if (!mounted) return;

    setState(() {
      _status = 'Done';
      _asrOutput = 'ᱫᱟᱨᱮ Dare';
      _translation = 'Inyạg ñutum dɔ Sona Marandi.';
    });
  }

  void _onRecordStart() {
    setState(() {
      _isRecording = true;
      _status = 'Recording…';
    });
  }

  void _onRecordStop() {
    setState(() {
      _isRecording = false;
      _status = 'Done';
      _asrOutput = 'ᱫᱟᱨᱮ Dare';
    });
  }

  void _saveToSQLite() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Saved to SQLite (simulated)'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  void _clearFeed() {
    setState(() {
      _asrOutput = 'ᱢᱚᱡ ᱟᱨᱮ';
      _status = 'Ready';
      _audioProgress = 0.0;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Feed cleared'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  void _nextPhrase() {
    setState(() {
      _step = (_step % 3) + 1;
      _teacherPrompt = _step == 1 ? 'Amag ñutum ched?' : 'Amag sutum ched?';
      _asrOutput = _step == 1 ? 'ᱫᱟᱨᱮ Dare' : 'ᱥᱟᱨᱟᱹ';
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Next phrase'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 24),
      children: [
        // Top server status
        Row(
          children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
                decoration: BoxDecoration(
                  color: MatriVaaniColors.forest2.withValues(alpha: 0.15),
                  border: Border.all(color: MatriVaaniColors.forest2.withValues(alpha: 0.35)),
                  borderRadius: BorderRadius.circular(999),
                ),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Icon(Icons.cloud_done_outlined, color: MatriVaaniColors.forest, size: 18),
                    SizedBox(width: 8),
                    Text('FastAPI ASR Engine', style: TextStyle(color: MatriVaaniColors.forest, fontWeight: FontWeight.w900, fontSize: 13)),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: MatriVaaniColors.surface,
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: MatriVaaniColors.border),
              ),
              child: const Text('240ms', style: TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.primaryDark, fontSize: 12)),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
              decoration: BoxDecoration(
                color: MatriVaaniColors.forest.withValues(alpha: 0.25),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: MatriVaaniColors.forest.withValues(alpha: 0.35)),
              ),
              child: const Text('16kHz Mono', style: TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.forest, fontSize: 12)),
            ),
          ],
        ),

        const SizedBox(height: 14),

        // Lesson step header
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
              decoration: BoxDecoration(
                color: MatriVaaniColors.surface,
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: MatriVaaniColors.border),
              ),
              child: const Text('Lesson 02: Introduction', style: TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.primaryDark)),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: BoxDecoration(
                color: MatriVaaniColors.amber.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(color: MatriVaaniColors.amber),
              ),
              child: Text('Step $_step/3', style: const TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.primaryDark)),
            )
          ],
        ),

        const SizedBox(height: 12),

        // Teacher prompt
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Teacher Prompt •', style: TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.primaryDark)),
                const SizedBox(height: 10),
                Row(
                  children: [
                    PressScale(
                      key: const Key('classroom_btn_teacher_listen'),
                      onTap: _simulateSpeak,
                      child: Container(
                        decoration: BoxDecoration(
                          color: MatriVaaniColors.forest.withValues(alpha: 0.12),
                          borderRadius: BorderRadius.circular(999),
                          border: Border.all(color: MatriVaaniColors.forest.withValues(alpha: 0.25)),
                        ),
                        padding: const EdgeInsets.all(8),
                        child: const Icon(
                          Icons.play_circle_outline_rounded,
                          color: MatriVaaniColors.forest,
                          size: 34,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('ᱢᱚᱦᱟᱹ : ᱥᱟᱱᱟᱹ ᱢᱤᱟᱨ ?', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w900, color: MatriVaaniColors.ink)),
                          const SizedBox(height: 6),
                          Text('Speak: "$_teacherPrompt" (What is your name?)', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w700)),
                          const SizedBox(height: 8),
                          Text('Status: $_status', style: TextStyle(color: MatriVaaniColors.primaryDark, fontWeight: FontWeight.w900, fontSize: 12)),
                        ],
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),
        ),

        const SizedBox(height: 12),

        // Your Santali Speech card
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    CircleAvatar(
                      radius: 18,
                      backgroundColor: MatriVaaniColors.forest.withValues(alpha: 0.16),
                      child: const Icon(Icons.mic_none_rounded, color: MatriVaaniColors.forest),
                    ),
                    const SizedBox(width: 10),
                    Text('Your Santali', style: const TextStyle(fontWeight: FontWeight.w900, color: MatriVaaniColors.primaryDark)),
                    const Spacer(),
                    Chip(
                      label: const Text('98% Match', style: TextStyle(fontWeight: FontWeight.w900)),
                      backgroundColor: MatriVaaniColors.forest.withValues(alpha: 0.14),
                      side: BorderSide(color: MatriVaaniColors.forest.withValues(alpha: 0.35)),
                    ),
                  ],
                ),
                const SizedBox(height: 10),
                const Text('OL CHIKI ASR OUTPUT', style: TextStyle(color: MatriVaaniColors.primaryDark, fontWeight: FontWeight.w900, fontSize: 12)),
                const SizedBox(height: 6),
                Text(_asrOutput, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
                const SizedBox(height: 8),
                Text('Auto-Punctuation: ON', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w700, fontSize: 12)),
                const SizedBox(height: 10),
                Row(
                  children: [
                    PressScale(
                      key: const Key('classroom_btn_play_pause'),
                      onTap: () {
                        setState(() => _audioProgress = (_audioProgress < 1.0) ? 1.0 : 0.0);
                      },
                      child: const Padding(
                        padding: EdgeInsets.all(8),
                        child: Icon(Icons.play_circle_outline_rounded),
                      ),
                    ),
                    Expanded(
                      child: Slider(
                        value: _audioProgress.clamp(0.0, 1.0),
                        onChanged: (v) => setState(() => _audioProgress = v),
                        activeColor: MatriVaaniColors.primary,
                        inactiveColor: MatriVaaniColors.border,
                      ),
                    ),
                    Text('${(_audioProgress * 3.2).toStringAsFixed(1)}s', style: const TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800)),
                  ],
                ),
                const SizedBox(height: 8),
                Text('"$_translation"', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800)),
              ],
            ),
          ),
        ),

        const SizedBox(height: 20),

        // PTT Button Center
        Center(
          child: Column(
            children: [
              PttButton(
                isRecording: _isRecording,
                onRecordStart: _onRecordStart,
                onRecordStop: _onRecordStop,
              ),
              const SizedBox(height: 12),
              Text(
                _isRecording ? 'Listening to Santali Speech...' : 'Hold to Speak Santali',
                style: const TextStyle(
                  color: MatriVaaniColors.muted,
                  fontWeight: FontWeight.w700,
                  fontSize: 14,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 24),

        // Actions: Save / Clear / Next
        Row(
          children: [
            Expanded(
              child: AnimatedButton.outlined(
                key: const Key('classroom_btn_save_sqlite'),
                onPressed: _saveToSQLite,
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.save_alt_rounded, size: 18),
                    SizedBox(width: 6),
                    Text('Save to SQLite'),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 8),
            Expanded(
              child: AnimatedButton.outlined(
                key: const Key('classroom_btn_clear_feed'),
                onPressed: _clearFeed,
                borderColor: MatriVaaniColors.muted,
                foregroundColor: MatriVaaniColors.muted,
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.delete_outline_rounded, size: 18),
                    SizedBox(width: 6),
                    Text('Clear Feed'),
                  ],
                ),
              ),
            ),
          ],
        ),

        const SizedBox(height: 12),

        AnimatedButton.elevated(
          key: const Key('classroom_btn_next_phrase'),
          onPressed: _nextPhrase,
          child: const Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text('Next phrase'),
              SizedBox(width: 6),
              Icon(Icons.arrow_forward_rounded, size: 18),
            ],
          ),
        ),
      ],
    );
  }
}
