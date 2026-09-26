import 'package:flutter/material.dart';
import '../theme/app_theme.dart';
import '../services/api_service.dart';
import 'translator_screen.dart';
import 'dart:async';

class HomeScreen extends StatefulWidget {
  final ValueChanged<int>? onGoToTab;
  const HomeScreen({super.key, this.onGoToTab});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isOnline = false;
  Timer? _pingTimer;

  @override
  void initState() {
    super.initState();
    _checkStatus();
    _pingTimer =
        Timer.periodic(const Duration(seconds: 5), (_) => _checkStatus());
  }

  @override
  void dispose() {
    _pingTimer?.cancel();
    super.dispose();
  }

  Future<void> _checkStatus() async {
    bool online = await ApiService.isOnline();
    if (mounted && online != _isOnline) {
      setState(() {
        _isOnline = online;
      });
    }
  }

  void _navigateToTab(int index) {
    if (widget.onGoToTab != null) {
      widget.onGoToTab!(index);
    }
  }

  void _navigateToTranslator() {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => TranslatorScreen()),
    );
  }

  Widget _buildCard(
      String title, IconData icon, Color color, VoidCallback onTap) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 8),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, size: 48, color: color),
              const SizedBox(height: 12),
              Text(
                title,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: Colors.black87,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey.shade100,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(vertical: 24, horizontal: 16),
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  bottomLeft: Radius.circular(24),
                  bottomRight: Radius.circular(24),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black12,
                    blurRadius: 4,
                    offset: Offset(0, 2),
                  )
                ],
              ),
              child: Column(
                children: [
                  Text(
                    'MatriVaani',
                    style: TextStyle(
                      fontSize: 32,
                      fontWeight: FontWeight.w900,
                      color: Colors.blue.shade900,
                      letterSpacing: 1.2,
                    ),
                  ),
                  const SizedBox(height: 8),
                  const Text(
                    'Learn • Speak • Understand',
                    style: TextStyle(
                      fontSize: 16,
                      color: Colors.black54,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: _isOnline
                          ? Colors.green.shade50
                          : Colors.orange.shade50,
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: _isOnline
                            ? Colors.green.shade300
                            : Colors.orange.shade300,
                      ),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          _isOnline ? Icons.cloud_done : Icons.cloud_off,
                          size: 16,
                          color: _isOnline
                              ? Colors.green.shade700
                              : Colors.orange.shade700,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          _isOnline
                              ? 'Synced (Online)'
                              : 'Offline (Cached Mode)',
                          style: TextStyle(
                            fontSize: 13,
                            fontWeight: FontWeight.bold,
                            color: _isOnline
                                ? Colors.green.shade800
                                : Colors.orange.shade800,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),

            // Grid
            Expanded(
              child: GridView.count(
                padding: const EdgeInsets.all(20),
                crossAxisCount: 2,
                mainAxisSpacing: 16,
                crossAxisSpacing: 16,
                childAspectRatio: 1.1,
                children: [
                  _buildCard('Classroom\nVoice', Icons.mic,
                      Colors.purple.shade600, () => _navigateToTab(1)),
                  _buildCard('Translator', Icons.language, Colors.blue.shade600,
                      _navigateToTranslator),
                  _buildCard('Lessons', Icons.menu_book, Colors.green.shade600,
                      () => _showComingSoon(context)),
                  _buildCard('Worksheets', Icons.edit_note,
                      Colors.orange.shade600, () => _showComingSoon(context)),
                  _buildCard('Flashcards', Icons.style, Colors.red.shade600,
                      () => _navigateToTab(2)),
                  _buildCard('Sync Data', Icons.sync, Colors.teal.shade600,
                      () => _navigateToTab(3)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _showComingSoon(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Feature coming soon!'),
        duration: Duration(seconds: 1),
      ),
    );
  }
}
