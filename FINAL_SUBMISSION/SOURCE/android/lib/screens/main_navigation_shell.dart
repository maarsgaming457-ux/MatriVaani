import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

import 'home_screen.dart';
import 'classroom_screen.dart';
import 'flashcards_screen.dart';
import 'sync_screen.dart';

class MainNavigationShell extends StatefulWidget {
  const MainNavigationShell({super.key});

  @override
  State<MainNavigationShell> createState() => _MainNavigationShellState();
}

class _MainNavigationShellState extends State<MainNavigationShell> {
  int _index = 0;

  void _setIndex(int index) {
    setState(() => _index = index);
  }

  @override
  Widget build(BuildContext context) {
    final pages = [
      HomeScreen(onGoToTab: _setIndex),
      const ClassroomScreen(),
      const FlashcardsScreen(),
      const SyncScreen(),
    ];

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        titleSpacing: 0,
        title: Padding(
          padding: const EdgeInsets.only(right: 8),
          child: Row(
            children: [
              const _AppLogo(),
              const SizedBox(width: 10),
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: const [
                  Text(
                    'MatriVaani',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.w800),
                  ),
                  Text(
                    'Santali Learning •',
                    style: TextStyle(fontSize: 12, color: MatriVaaniColors.muted),
                  ),
                ],
              ),
              const Spacer(),
              const CircleAvatar(radius: 20, backgroundColor: Colors.grey),
            ],
          ),
        ),
      ),
      backgroundColor: MatriVaaniColors.background,
      body: AnimatedSwitcher(
        duration: const Duration(milliseconds: 250),
        switchInCurve: Curves.easeOut,
        switchOutCurve: Curves.easeIn,
        transitionBuilder: (child, animation) => FadeTransition(
          opacity: animation,
          child: child,
        ),
        child: SafeArea(
          key: ValueKey(_index),
          top: false,
          child: pages[_index],
        ),
      ),
      bottomNavigationBar: _BottomNavBar(index: _index, onTap: _setIndex),
    );
  }
}

class _BottomNavBar extends StatelessWidget {
  final int index;
  final ValueChanged<int> onTap;

  const _BottomNavBar({required this.index, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: MatriVaaniColors.surface,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.06),
            blurRadius: 18,
            offset: const Offset(0, -2),
          ),
        ],
        borderRadius: const BorderRadius.only(
          topLeft: Radius.circular(20),
          topRight: Radius.circular(20),
        ),
      ),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _NavItem(
            key: const Key('nav_home'),
            selected: index == 0,
            icon: Icons.home_outlined,
            selectedIcon: Icons.home_rounded,
            label: '/ Home',
            onTap: () => onTap(0),
          ),
          _NavItem(
            key: const Key('nav_classroom'),
            selected: index == 1,
            icon: Icons.mic_none,
            selectedIcon: Icons.mic_rounded,
            label: 'Class',
            onTap: () => onTap(1),
          ),
          _NavItem(
            key: const Key('nav_flashcards'),
            selected: index == 2,
            icon: Icons.book_outlined,
            selectedIcon: Icons.book_rounded,
            label: 'Cards',
            onTap: () => onTap(2),
          ),
          _NavItem(
            key: const Key('nav_sync'),
            selected: index == 3,
            icon: Icons.checklist_outlined,
            selectedIcon: Icons.checklist_rounded,
            label: 'Sync',
            onTap: () => onTap(3),
          ),
        ],
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  final bool selected;
  final IconData icon;
  final IconData selectedIcon;
  final String label;
  final VoidCallback onTap;

  const _NavItem({
    super.key,
    required this.selected,
    required this.icon,
    required this.label,
    required this.onTap,
    IconData? selectedIcon,
  }) : selectedIcon = selectedIcon ?? icon;

  @override
  Widget build(BuildContext context) {
    final fg = selected ? MatriVaaniColors.primaryDark : MatriVaaniColors.muted;

    return PressScale(
      onTap: onTap,
      scale: 0.92,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        curve: Curves.easeOut,
        padding: EdgeInsets.symmetric(
          horizontal: selected ? 16 : 6,
          vertical: 6,
        ),
        decoration: BoxDecoration(
          color: selected
              ? MatriVaaniColors.primary.withValues(alpha: 0.10)
              : Colors.transparent,
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedSwitcher(
              duration: const Duration(milliseconds: 200),
              child: Icon(
                selected ? selectedIcon : icon,
                key: ValueKey('$label-$selected'),
                color: fg,
                size: selected ? 26 : 24,
              ),
            ),
            const SizedBox(height: 4),
            Text(label,
                style: TextStyle(
                  fontSize: 11,
                  color: fg,
                  fontWeight: selected ? FontWeight.w700 : FontWeight.w600,
                )),
          ],
        ),
      ),
    );
  }
}

class _AppLogo extends StatelessWidget {
  const _AppLogo();

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        color: MatriVaaniColors.surface,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: MatriVaaniColors.border, width: 2),
      ),
      child: const Icon(Icons.eco_outlined, color: MatriVaaniColors.primaryDark),
    );
  }
}
