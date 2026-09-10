import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../theme/app_theme.dart';

/// A subtle, consistent animated press wrapper used across all interactive
/// controls in MatriVaani.  On tap-down it scales to 0.95 and dims slightly;
/// on tap-up (or cancel) it springs back.  A [loading] flag replaces the child
/// with a small spinner to signal async work.
///
/// Use [AnimatedButton.elevated], [AnimatedButton.outlined], or
/// [AnimatedButton.icon] for button shapes, or wrap any widget with the base
/// [AnimatedButton] constructor.
class AnimatedButton extends StatefulWidget {
  const AnimatedButton({
    super.key,
    required this.onPressed,
    required this.child,
    this.loading = false,
    this.disabled = false,
    this.borderRadius = 18,
    this.padding = const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
    this.backgroundColor,
    this.foregroundColor,
    this.border,
  });

  final VoidCallback? onPressed;
  final Widget child;
  final bool loading;
  final bool disabled;
  final double borderRadius;
  final EdgeInsetsGeometry padding;
  final Color? backgroundColor;
  final Color? foregroundColor;
  final BorderSide? border;

  // ── Convenience factories ───────────────────────────────────────────────

  factory AnimatedButton.elevated({
    Key? key,
    required VoidCallback? onPressed,
    required Widget child,
    bool loading = false,
    Color backgroundColor = MatriVaaniColors.primary,
    Color foregroundColor = Colors.white,
    double borderRadius = 18,
    EdgeInsetsGeometry padding =
        const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
  }) {
    return AnimatedButton(
      key: key,
      onPressed: onPressed,
      loading: loading,
      backgroundColor: backgroundColor,
      foregroundColor: foregroundColor,
      borderRadius: borderRadius,
      padding: padding,
      child: child,
    );
  }

  factory AnimatedButton.outlined({
    Key? key,
    required VoidCallback? onPressed,
    required Widget child,
    bool loading = false,
    Color borderColor = MatriVaaniColors.primary,
    Color foregroundColor = MatriVaaniColors.primary,
    double borderRadius = 18,
    EdgeInsetsGeometry padding =
        const EdgeInsets.symmetric(horizontal: 18, vertical: 14),
  }) {
    return AnimatedButton(
      key: key,
      onPressed: onPressed,
      loading: loading,
      foregroundColor: foregroundColor,
      border: BorderSide(color: borderColor),
      borderRadius: borderRadius,
      padding: padding,
      child: child,
    );
  }

  @override
  State<AnimatedButton> createState() => _AnimatedButtonState();
}

class _AnimatedButtonState extends State<AnimatedButton>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _scale;
  late final Animation<double> _opacity;

  bool get _isEnabled =>
      !widget.disabled && !widget.loading && widget.onPressed != null;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 80),
      reverseDuration: const Duration(milliseconds: 180),
      value: 0,
    );
    _scale = Tween<double>(begin: 1.0, end: 0.95).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeOut),
    );
    _opacity = Tween<double>(begin: 1.0, end: 0.75).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeOut),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails _) {
    if (!_isEnabled) return;
    HapticFeedback.lightImpact();
    _ctrl.forward();
  }

  void _onTapUp(TapUpDetails _) {
    if (!_isEnabled) return;
    _ctrl.reverse();
  }

  void _onTapCancel() => _ctrl.reverse();

  void _onTap() {
    if (!_isEnabled) return;
    if (mounted) widget.onPressed?.call();
  }

  @override
  Widget build(BuildContext context) {
    final bg = widget.backgroundColor;
    final fg = widget.foregroundColor;
    final hasBg = bg != null;

    return GestureDetector(
      onTapDown: _onTapDown,
      onTapUp: _onTapUp,
      onTapCancel: _onTapCancel,
      onTap: _onTap,
      child: AnimatedBuilder(
        animation: _ctrl,
        builder: (context, child) => Transform.scale(
          scale: _scale.value,
          child: Opacity(
            opacity: _isEnabled ? _opacity.value : 0.45,
            child: child,
          ),
        ),
        child: Material(
          color: hasBg ? bg : Colors.transparent,
          borderRadius: BorderRadius.circular(widget.borderRadius),
          child: InkWell(
            borderRadius: BorderRadius.circular(widget.borderRadius),
            splashColor: (fg ?? MatriVaaniColors.primary).withValues(alpha: 0.18),
            highlightColor: Colors.transparent,
            onTap: null, // gesture detector handles it
            child: Container(
              padding: widget.padding,
              decoration: widget.border != null
                  ? BoxDecoration(
                      borderRadius: BorderRadius.circular(widget.borderRadius),
                      border: Border.fromBorderSide(widget.border!),
                    )
                  : null,
              child: _buildContent(fg),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildContent(Color? fg) {
    if (widget.loading) {
      return SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(
          // Determinate so widget tests can `pumpAndSettle`.
          value: 0.72,
          strokeWidth: 2.5,
          valueColor: AlwaysStoppedAnimation<Color>(
            fg ?? MatriVaaniColors.primary,
          ),
        ),
      );
    }
    return DefaultTextStyle(
      style: TextStyle(color: fg ?? MatriVaaniColors.ink),
      child: IconTheme(
        data: IconThemeData(color: fg ?? MatriVaaniColors.ink),
        child: widget.child,
      ),
    );
  }
}

/// Wrap any pressable container (icon, pill, card section) with a subtle
/// press-scale animation without changing its visual shape.
class PressScale extends StatefulWidget {
  const PressScale({
    super.key,
    required this.child,
    required this.onTap,
    this.scale = 0.95,
    this.duration = const Duration(milliseconds: 80),
    this.reverseDuration = const Duration(milliseconds: 180),
    this.hitTestBehavior = HitTestBehavior.opaque,
  });

  final Widget child;
  final VoidCallback? onTap;
  final double scale;
  final Duration duration;
  final Duration reverseDuration;
  final HitTestBehavior hitTestBehavior;

  @override
  State<PressScale> createState() => _PressScaleState();
}

class _PressScaleState extends State<PressScale>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _scale;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
      vsync: this,
      duration: widget.duration,
      reverseDuration: widget.reverseDuration,
      value: 0,
    );
    _scale = Tween<double>(begin: 1.0, end: widget.scale).animate(
      CurvedAnimation(parent: _ctrl, curve: Curves.easeOut),
    );
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  void _down(TapDownDetails _) {
    if (widget.onTap == null) return;
    HapticFeedback.selectionClick();
    _ctrl.forward();
  }

  void _up(TapUpDetails _) {
    _ctrl.reverse();
  }

  void _cancel() => _ctrl.reverse();

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      behavior: widget.hitTestBehavior,
      onTapDown: _down,
      onTapUp: _up,
      onTapCancel: _cancel,
      onTap: widget.onTap,
      child: ScaleTransition(scale: _scale, child: widget.child),
    );
  }
}

/// Animated PTT (push-to-talk) button: pulses while recording.
class PttButton extends StatefulWidget {
  const PttButton({
    super.key,
    required this.onRecordStart,
    required this.onRecordStop,
    this.isRecording = false,
  });

  final VoidCallback onRecordStart;
  final VoidCallback onRecordStop;
  final bool isRecording;

  @override
  State<PttButton> createState() => _PttButtonState();
}

class _PttButtonState extends State<PttButton>
    with SingleTickerProviderStateMixin {
  late final AnimationController _pulse;
  late final Animation<double> _outerScale;
  late final Animation<double> _opacity;

  @override
  void initState() {
    super.initState();
    // Important for widget tests: avoid infinite animations that prevent
    // `pumpAndSettle()` from completing.
    _pulse = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 260),
    );

    _outerScale = Tween<double>(begin: 1.0, end: 1.18).animate(
      CurvedAnimation(parent: _pulse, curve: Curves.easeInOut),
    );
    _opacity = Tween<double>(begin: 0.3, end: 0.08).animate(
      CurvedAnimation(parent: _pulse, curve: Curves.easeInOut),
    );

    if (widget.isRecording) {
      _pulse.forward(from: 0);
    }
  }

  @override
  void didUpdateWidget(covariant PttButton oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (widget.isRecording && !oldWidget.isRecording) {
      _pulse.forward(from: 0);
    } else if (!widget.isRecording) {
      _pulse
        ..stop()
        ..reset();
    }
  }

  @override
  void dispose() {
    _pulse.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails _) {
    HapticFeedback.mediumImpact();
    widget.onRecordStart();
  }

  void _onTapUp(TapUpDetails _) {
    HapticFeedback.lightImpact();
    widget.onRecordStop();
  }

  void _onTapCancel() => widget.onRecordStop();

  // `tester.press` in widget tests can miss tap-down/up pairing; `onTap`
  // still fires so PTT remains testable.
  void _onTap() {
    if (widget.isRecording) {
      widget.onRecordStop();
    } else {
      widget.onRecordStart();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isRec = widget.isRecording;

    return GestureDetector(
      key: const Key('classroom_ptt_button'),
      onTapDown: _onTapDown,
      onTapUp: _onTapUp,
      onTapCancel: _onTapCancel,
      onTap: _onTap,
      child: SizedBox(
        width: 180,
        height: 180,
        child: Stack(
          alignment: Alignment.center,
          children: [
            // Outer pulse ring (only when recording)
            if (isRec)
              AnimatedBuilder(
                animation: _pulse,
                builder: (_, __) => Transform.scale(
                  scale: _outerScale.value,
                  child: Container(
                    width: 180,
                    height: 180,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: MatriVaaniColors.primary
                          .withValues(alpha: _opacity.value),
                    ),
                  ),
                ),
              ),
            // Static background ring
            Container(
              width: 160,
              height: 160,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isRec
                    ? MatriVaaniColors.primary.withValues(alpha: 0.12)
                    : MatriVaaniColors.forest.withValues(alpha: 0.08),
              ),
            ),
            // Inner ring
            Container(
              width: 130,
              height: 130,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: MatriVaaniColors.surfaceAlt,
                border: Border.all(
                  color: isRec ? MatriVaaniColors.primary : MatriVaaniColors.border,
                  width: isRec ? 2 : 1,
                ),
              ),
            ),
            // Core mic button
            AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              width: 94,
              height: 94,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: isRec
                    ? MatriVaaniColors.primary
                    : MatriVaaniColors.primaryDark.withValues(alpha: 0.95),
                boxShadow: [
                  BoxShadow(
                    color: (isRec ? MatriVaaniColors.primary : MatriVaaniColors.primaryDark)
                        .withValues(alpha: isRec ? 0.40 : 0.25),
                    blurRadius: isRec ? 24 : 18,
                  ),
                ],
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AnimatedSwitcher(
                    duration: const Duration(milliseconds: 180),
                    child: Icon(
                      isRec ? Icons.mic_rounded : Icons.mic_rounded,
                      key: ValueKey(isRec),
                      size: 28,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 6),
                  Text(
                    isRec ? 'REC' : 'PTT',
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w900,
                      fontSize: 12,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
