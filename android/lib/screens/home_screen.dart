import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

class HomeScreen extends StatefulWidget {
  final ValueChanged<int> onGoToTab;
  const HomeScreen({super.key, required this.onGoToTab});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isHearing = false;

  void _goTo(int tabIndex) => widget.onGoToTab(tabIndex);

  void _onHearWord() {
    setState(() => _isHearing = true);

    // Show immediately so widget tests don't need timer pumping.
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Playing word pronunciation…')),
    );

    Future.delayed(const Duration(milliseconds: 250)).then((_) {
      if (!mounted) return;
      setState(() => _isHearing = false);
    });
  }

  @override
  Widget build(BuildContext context) {
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 24),
      children: [
        // Top greeting banner
        Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    _ClassChip(text: 'Class 2 •'),
                    const Spacer(),
                    _StatChip(
                      icon: Icons.local_fire_department_outlined,
                      label: '5 Days',
                      color: MatriVaaniColors.primary.withValues(alpha: 0.13),
                      fg: MatriVaaniColors.primary,
                    ),
                    const SizedBox(width: 8),
                    _StatChip(
                      icon: Icons.star_border_rounded,
                      label: '120',
                      color: MatriVaaniColors.amber.withValues(alpha: 0.18),
                      fg: MatriVaaniColors.primaryDark,
                      isStars: true,
                    ),
                  ],
                ),
                const SizedBox(height: 12),
                Text(
                  'ᱡᱚᱦᱟᱨ, ᱥᱚᱱᱟ! Ready to speak today?',
                  style: const TextStyle(fontSize: 18, fontWeight: FontWeight.w900),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // Local mode pill + sync shortcut
        Card(
          color: MatriVaaniColors.surface,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(
              children: [
                const Icon(Icons.offline_bolt_outlined, size: 26, color: MatriVaaniColors.forest),
                const SizedBox(width: 10),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Text('Local Mode Active', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                      SizedBox(height: 4),
                      Text('3 voice logs saved offline (matrivaani_local.db…)', style: TextStyle(color: MatriVaaniColors.muted, fontSize: 12, fontWeight: FontWeight.w700)),
                    ],
                  ),
                ),
                AnimatedButton.elevated(
                  key: const Key('home_btn_sync'),
                  onPressed: () => _goTo(3),
                  backgroundColor: MatriVaaniColors.forest2,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.sync_alt_rounded, size: 20),
                      SizedBox(width: 8),
                      Text('Sync'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // Classroom hero card
        Card(
          color: const Color(0xFFA8431D),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    _HeroBadge(text: 'Voice Interactive • Instant AI Echo'),
                    const Spacer(),
                    const Icon(Icons.mic, color: Colors.white, size: 28),
                  ],
                ),
                const SizedBox(height: 10),
                Text(
                  'Classroom',
                  style: TextStyle(color: Colors.white.withValues(alpha: 0.95), fontSize: 22, fontWeight: FontWeight.w900),
                ),
                const SizedBox(height: 6),
                Text(
                  'Speak in Santali, see Ol Chiki words live!',
                  style: TextStyle(color: Colors.white.withValues(alpha: 0.9), fontSize: 14, fontWeight: FontWeight.w600),
                ),
                const SizedBox(height: 14),
                Row(
                  children: [
                    _LiveRecDot(color: Colors.greenAccent),
                    const SizedBox(width: 8),
                    const Expanded(
                      child: Text(
                        'Live recognition',
                        style: TextStyle(color: Colors.white, fontWeight: FontWeight.w800),
                      ),
                    ),
                    AnimatedButton.elevated(
                      key: const Key('home_btn_start_classroom'),
                      onPressed: () => _goTo(1),
                      backgroundColor: Colors.white,
                      foregroundColor: const Color(0xFFA8431D),
                      padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.mic_none_rounded, size: 20),
                          SizedBox(width: 8),
                          Text('Start •'),
                        ],
                      ),
                    ),
                  ],
                )
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // Today's word card
        Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(22)),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    const Icon(Icons.book_outlined, color: MatriVaaniColors.primaryDark),
                    const SizedBox(width: 8),
                    const Text('Today\'s Word •', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16)),
                    const Spacer(),
                    _LetterChip(text: 'Letter 1'),
                  ],
                ),
                const SizedBox(height: 12),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.center,
                  children: [
                    Container(
                      width: 86,
                      height: 86,
                      decoration: BoxDecoration(
                        color: MatriVaaniColors.primaryDark,
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: const Center(
                        child: Text('ᱫ', style: TextStyle(fontSize: 44, color: Colors.white, fontWeight: FontWeight.w900)),
                      ),
                    ),
                    const SizedBox(width: 14),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('ᱫᱚᱨᱚᱡ (Doroj)', style: TextStyle(fontSize: 20, fontWeight: FontWeight.w900)),
                          const SizedBox(height: 6),
                          Text('Say it back: "ᱫᱚᱨᱚᱡ"', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w700)),
                        ],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 14),
                AnimatedButton.elevated(
                  key: const Key('home_btn_hear_word'),
                  onPressed: _onHearWord,
                  loading: _isHearing,
                  child: const Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.hearing_rounded, size: 20),
                      SizedBox(width: 8),
                      Text('Hear •'),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // Feature chips
        Wrap(
          spacing: 10,
          runSpacing: 10,
          children: const [
            _FeatureChip(icon: Icons.record_voice_over, text: 'PTT Mode', color: MatriVaaniColors.primary),
            _FeatureChip(icon: Icons.translate, text: 'Bilingual Echo', color: MatriVaaniColors.forest),
            _FeatureChip(icon: Icons.offline_bolt_outlined, text: 'Offline Voice DB', color: MatriVaaniColors.amber),
            _FeatureChip(icon: Icons.fast_forward_rounded, text: 'Fast Inference', color: MatriVaaniColors.primaryDark),
          ],
        ),

        const SizedBox(height: 22),

        // Design cards
        Row(
          children: [
            _DesignMock(
              path: 'assets/designs/figma_classroom.png',
              fallbackColor: const Color(0xFFF2EDF5),
              fallbackIcon: Icons.mic_none_rounded,
              label: 'Classroom •',
            ),
            const SizedBox(width: 12),
            _DesignMock(
              path: 'assets/designs/figma_flashcards.png',
              fallbackColor: const Color(0xFFF5EEDD),
              fallbackIcon: Icons.book_outlined,
              label: 'Flashcards •',
            ),
          ],
        ),

        const SizedBox(height: 22),
      ],
    );
  }
}

// --- UI Helpers (unchanged from original file) ---------------------------
class _ClassChip extends StatelessWidget {
  final String text;
  const _ClassChip({required this.text});
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: MatriVaaniColors.primaryDark,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 12)),
    );
  }
}

class _StatChip extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final Color fg;
  final bool isStars;

  const _StatChip({required this.icon, required this.label, required this.color, required this.fg, this.isStars = false});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(999)),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: fg, size: 18),
          const SizedBox(width: 6),
          Text(label, style: TextStyle(color: fg, fontWeight: FontWeight.w900, fontSize: 12)),
          if (isStars) const Text(' ⭐', style: TextStyle(fontSize: 14)),
        ],
      ),
    );
  }
}

class _HeroBadge extends StatelessWidget {
  final String text;
  const _HeroBadge({required this.text});
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.22),
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 12)),
    );
  }
}

class _LiveRecDot extends StatelessWidget {
  final Color color;
  const _LiveRecDot({required this.color});
  @override
  Widget build(BuildContext context) {
    return Container(width: 14, height: 14, decoration: BoxDecoration(color: color, shape: BoxShape.circle));
  }
}

class _LetterChip extends StatelessWidget {
  final String text;
  const _LetterChip({required this.text});
  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: MatriVaaniColors.primaryDark,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(text, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w800, fontSize: 12)),
    );
  }
}

class _FeatureChip extends StatelessWidget {
  final IconData icon;
  final String text;
  final Color color;

  const _FeatureChip({required this.icon, required this.text, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.10),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: color.withValues(alpha: 0.22)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(width: 8),
          Text(text, style: TextStyle(color: color, fontWeight: FontWeight.w900, fontSize: 13)),
        ],
      ),
    );
  }
}

class _DesignMock extends StatelessWidget {
  final String path;
  final Color fallbackColor;
  final IconData fallbackIcon;
  final String label;

  const _DesignMock({required this.path, required this.fallbackColor, required this.fallbackIcon, required this.label});

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        height: 140,
        decoration: BoxDecoration(
          color: fallbackColor,
          borderRadius: BorderRadius.circular(20),
        ),
        child: Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(fallbackIcon, color: MatriVaaniColors.muted, size: 32),
              const SizedBox(height: 8),
              Text(label, style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800)),
            ],
          ),
        ),
      ),
    );
  }
}
