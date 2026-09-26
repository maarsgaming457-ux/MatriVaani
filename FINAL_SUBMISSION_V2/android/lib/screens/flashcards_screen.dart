import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

class FlashcardsScreen extends StatefulWidget {
  const FlashcardsScreen({super.key});

  @override
  State<FlashcardsScreen> createState() => _FlashcardsScreenState();
}

class _FlashcardsScreenState extends State<FlashcardsScreen> {
  String _category = 'Letters';
  int _cardIndex = 3; // 0-indexed, showing "Card 4 of 30"
  final int _totalCards = 30;
  bool _isListening = false;
  bool _tracingEnabled = false;

  void _prevCard() {
    if (_cardIndex > 0) setState(() => _cardIndex--);
  }

  void _nextCard() {
    if (_cardIndex < _totalCards - 1) setState(() => _cardIndex++);
  }

  void _markKnown() {
    setState(() {
      if (_cardIndex < _totalCards - 1) _cardIndex++;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('✓ Marked as Known! +10 ⭐'),
        backgroundColor: MatriVaaniColors.forest,
        duration: Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final progress = (_cardIndex + 1) / _totalCards;

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 24),
      children: [
        // Category pills
        Row(
          children: [
            _CategoryPill(
              label: 'Letters',
              selected: _category == 'Letters',
              icon: Icons.text_fields,
              onTap: () => setState(() => _category = 'Letters'),
            ),
            const SizedBox(width: 10),
            _CategoryPill(
              label: 'Animals',
              selected: _category == 'Animals',
              icon: Icons.cruelty_free,
              onTap: () => setState(() => _category = 'Animals'),
            ),
          ],
        ),
        const SizedBox(height: 16),

        // Progress header
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: MatriVaaniColors.surface,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: MatriVaaniColors.border),
          ),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text.rich(
                    TextSpan(children: [
                      TextSpan(
                        text: 'Card ${_cardIndex + 1}',
                        style: const TextStyle(
                          color: MatriVaaniColors.primary,
                          fontWeight: FontWeight.w800,
                          fontSize: 18,
                        ),
                      ),
                      TextSpan(
                        text: ' of $_totalCards •',
                        style: const TextStyle(
                          color: MatriVaaniColors.muted,
                          fontWeight: FontWeight.w600,
                          fontSize: 15,
                        ),
                      ),
                    ]),
                  ),
                  // XP badge
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: MatriVaaniColors.amber.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(color: MatriVaaniColors.amber),
                    ),
                    child: const Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(Icons.stars, color: MatriVaaniColors.amber, size: 16),
                        SizedBox(width: 4),
                        Text('+10', style: TextStyle(fontWeight: FontWeight.w800, color: MatriVaaniColors.amber)),
                        Text(' ⭐', style: TextStyle(fontSize: 14)),
                      ],
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 10),
              ClipRRect(
                borderRadius: BorderRadius.circular(999),
                child: LinearProgressIndicator(
                  value: progress,
                  backgroundColor: MatriVaaniColors.border,
                  valueColor: const AlwaysStoppedAnimation<Color>(MatriVaaniColors.primary),
                  minHeight: 8,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // Main flashcard
        Container(
          decoration: BoxDecoration(
            color: MatriVaaniColors.surface,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: MatriVaaniColors.border),
            boxShadow: [
              BoxShadow(
                color: MatriVaaniColors.shadow.withValues(alpha: 0.08),
                blurRadius: 20,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                // Glyph header badge
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
                      decoration: BoxDecoration(
                        color: MatriVaaniColors.forest.withValues(alpha: 0.12),
                        borderRadius: BorderRadius.circular(999),
                        border: Border.all(color: MatriVaaniColors.forest.withValues(alpha: 0.5)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Container(
                            width: 7,
                            height: 7,
                            decoration: const BoxDecoration(
                              color: MatriVaaniColors.forest,
                              shape: BoxShape.circle,
                            ),
                          ),
                          const SizedBox(width: 5),
                          const Text('Primary Glyph •', style: TextStyle(color: MatriVaaniColors.forest, fontWeight: FontWeight.w700, fontSize: 12)),
                        ],
                      ),
                    ),
                    Icon(Icons.compare, color: MatriVaaniColors.muted, size: 22),
                  ],
                ),
                const SizedBox(height: 12),

                // Dual panel: stroke order + illustration
                Row(
                  children: [
                    // Stroke order diagram
                    Expanded(
                      child: Container(
                        height: 130,
                        decoration: BoxDecoration(
                          color: const Color(0xFFF2EDF5),
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: Stack(
                          children: [
                            const Center(
                              child: Text(
                                'ᱫ',
                                style: TextStyle(
                                  fontSize: 56,
                                  color: MatriVaaniColors.primaryDark,
                                  fontWeight: FontWeight.w900,
                                ),
                              ),
                            ),
                            Positioned(
                              top: 8,
                              left: 8,
                              child: _StepBadge(label: '1', color: MatriVaaniColors.primaryDark),
                            ),
                            Positioned(
                              top: 8,
                              right: 8,
                              child: _StepBadge(label: '2', color: MatriVaaniColors.forest),
                            ),
                            Positioned(
                              bottom: 8,
                              right: 8,
                              child: _StepBadge(label: '3', color: MatriVaaniColors.forest),
                            ),
                            const Positioned(
                              bottom: 8,
                              left: 0,
                              right: 0,
                              child: Center(
                                child: Text(
                                  'LA /ɔ/',
                                  style: TextStyle(
                                    color: MatriVaaniColors.primary,
                                    fontWeight: FontWeight.w700,
                                    fontSize: 13,
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(width: 8),

                    // Illustration
                    Expanded(
                      child: Container(
                        height: 130,
                        decoration: BoxDecoration(
                          color: const Color(0xFFF5EEDD),
                          borderRadius: BorderRadius.circular(16),
                        ),
                        child: const Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.park, size: 52, color: MatriVaaniColors.forest),
                              Text('Sal Tree', style: TextStyle(fontWeight: FontWeight.w700, color: MatriVaaniColors.forest, fontSize: 13)),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                // Word display
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: const [
                    Text('ᱫᱟᱨᱮ  ', style: TextStyle(fontSize: 24, fontWeight: FontWeight.w900, color: MatriVaaniColors.ink)),
                    Text('Dare', style: TextStyle(fontSize: 22, fontWeight: FontWeight.w700, color: MatriVaaniColors.ink)),
                    Text('  /da:re/', style: TextStyle(fontSize: 13, color: MatriVaaniColors.muted)),
                  ],
                ),
                const SizedBox(height: 2),
                const Text('Tree •', style: TextStyle(color: MatriVaaniColors.muted, fontSize: 14)),
                const SizedBox(height: 16),

                // Listen button
                SizedBox(
                  width: double.infinity,
                  child: AnimatedButton.elevated(
                    onPressed: () {
                      setState(() => _isListening = !_isListening);
                    },
                    backgroundColor: MatriVaaniColors.forest,
                    foregroundColor: Colors.white,
                    borderRadius: 14,
                    padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(_isListening ? Icons.volume_up : Icons.volume_up_outlined, size: 20),
                        const SizedBox(width: 8),
                        Text(
                          _isListening ? 'Playing …' : 'Listen •',
                          style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 15),
                        ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 14),

                // Usage example
                Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: MatriVaaniColors.background,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: MatriVaaniColors.border),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: const [
                      Row(
                        children: [
                          Icon(Icons.book, size: 14, color: MatriVaaniColors.primary),
                          SizedBox(width: 4),
                          Text('USAGE EXAMPLE •', style: TextStyle(fontSize: 11, letterSpacing: 0.5, fontWeight: FontWeight.w800, color: MatriVaaniColors.primary)),
                        ],
                      ),
                      SizedBox(height: 6),
                      Text('"ᱫᱟᱨᱮ ᱫᱚ ᱡᱤᱣᱤ ᱮᱢᱚᱜ-ᱟ"', style: TextStyle(fontSize: 14, fontWeight: FontWeight.w600, color: MatriVaaniColors.ink)),
                      Text('"Dare do jiwi emog-a." (Trees give us life.)', style: TextStyle(fontSize: 12, color: MatriVaaniColors.muted)),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 14),

        // Practice Tracing button
        PressScale(
          onTap: () => setState(() => _tracingEnabled = !_tracingEnabled),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
            decoration: BoxDecoration(
              color: const Color(0xFFFDEDE8),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: MatriVaaniColors.primary.withValues(alpha: 0.25)),
            ),
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(
                    color: MatriVaaniColors.primary.withValues(alpha: 0.15),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: const Icon(Icons.draw_outlined, color: MatriVaaniColors.primary, size: 20),
                ),
                const SizedBox(width: 12),
                const Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('Practice Tracing', style: TextStyle(fontWeight: FontWeight.w700, fontSize: 15, color: MatriVaaniColors.ink)),
                      Text('Finger draw Ol Chiki stroke order', style: TextStyle(fontSize: 12, color: MatriVaaniColors.muted)),
                    ],
                  ),
                ),
                Switch(
                  value: _tracingEnabled,
                  onChanged: (v) => setState(() => _tracingEnabled = v),
                  activeThumbColor: MatriVaaniColors.primary,
                ),
              ],
            ),
          ),
        ),
        const SizedBox(height: 14),

        // Know This button
        SizedBox(
          width: double.infinity,
          child: AnimatedButton.elevated(
            onPressed: _markKnown,
            backgroundColor: MatriVaaniColors.forest,
            foregroundColor: Colors.white,
            borderRadius: 18,
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.check_circle_outline_rounded, size: 20),
                const SizedBox(width: 8),
                const Text('I Know This! •', style: TextStyle(fontWeight: FontWeight.w800, fontSize: 16)),
              ],
            ),
          ),
        ),
        const SizedBox(height: 10),

        // Previous / Next row
        Row(
          children: [
            Expanded(
              child: AnimatedButton.outlined(
                onPressed: _prevCard,
                borderColor: MatriVaaniColors.border,
                foregroundColor: MatriVaaniColors.muted,
                borderRadius: 16,
                padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(Icons.arrow_back_rounded, size: 18, color: MatriVaaniColors.muted),
                    SizedBox(width: 8),
                    Text('Previous •', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: AnimatedButton.elevated(
                onPressed: _nextCard,
                backgroundColor: MatriVaaniColors.primary,
                foregroundColor: Colors.white,
                borderRadius: 16,
                padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text('Next •', style: TextStyle(fontWeight: FontWeight.w700)),
                    SizedBox(width: 6),
                    Icon(Icons.arrow_forward_rounded, size: 18),
                  ],
                ),
              ),
            ),
          ],
        ),
      ],
    );
  }
}

class _CategoryPill extends StatelessWidget {
  final String label;
  final bool selected;
  final IconData icon;
  final VoidCallback onTap;

  const _CategoryPill({required this.label, required this.selected, required this.icon, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return PressScale(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 12),
        decoration: BoxDecoration(
          color: selected ? MatriVaaniColors.primaryDark : MatriVaaniColors.surface,
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: selected ? MatriVaaniColors.primaryDark : MatriVaaniColors.border),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 16, color: selected ? Colors.white : MatriVaaniColors.muted),
            const SizedBox(width: 6),
            Text(
              '$label •',
              style: TextStyle(
                fontWeight: FontWeight.w700,
                color: selected ? Colors.white : MatriVaaniColors.muted,
                fontSize: 14,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _StepBadge extends StatelessWidget {
  final String label;
  final Color color;

  const _StepBadge({required this.label, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 22,
      height: 22,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
      ),
      child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w800)),
    );
  }
}
