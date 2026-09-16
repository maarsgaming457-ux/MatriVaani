import 'package:flutter/material.dart';

import '../theme/app_theme.dart';
import '../widgets/animated_button.dart';

class SyncScreen extends StatefulWidget {
  const SyncScreen({super.key});

  @override
  State<SyncScreen> createState() => _SyncScreenState();
}

class _SyncScreenState extends State<SyncScreen> {
  bool _autoSyncOnWifi = true;
  bool _saveRawWavLocally = true;

  // Simulated state for UI verification
  double _bufferProgress = 0.5;
  int _bufferOk = 2;
  int _bufferTotal = 4;
  bool _isSyncing = false;
  String _endpoint = 'http://10.0.2.2:8000';
  String _pingStatus = 'Idle';

  void _clearCache() {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Cache cleared'),
        duration: Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  Future<void> _syncAll() async {
    if (_isSyncing) return;
    setState(() => _isSyncing = true);
    await Future.delayed(const Duration(milliseconds: 650));
    if (!mounted) return;
    setState(() {
      _bufferProgress = 1.0;
      _bufferOk = _bufferTotal;
      _isSyncing = false;
    });
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Sync completed ✓')),
    );
  }

  Future<void> _pingServer() async {
    setState(() => _pingStatus = 'Pinging...');
    await Future.delayed(const Duration(milliseconds: 450));
    if (!mounted) return;
    setState(() => _pingStatus = 'Online');
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Ping: $_pingStatus'),
        duration: const Duration(milliseconds: 700),
        behavior: SnackBarBehavior.floating,
        margin: const EdgeInsets.only(left: 16, right: 16, bottom: 80),
      ),
    );
  }

  Widget _pendingRow({
    required String title,
    required String subtitle,
    required bool pending,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 10),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: const BorderSide(color: MatriVaaniColors.border),
      ),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Row(
          children: [
            CircleAvatar(
              radius: 18,
              backgroundColor: pending ? MatriVaaniColors.primary.withValues(alpha: 0.12) : MatriVaaniColors.forest2.withValues(alpha: 0.12),
              child: Icon(
                pending ? Icons.mic_outlined : Icons.check_circle_outline,
                color: pending ? MatriVaaniColors.primaryDark : MatriVaaniColors.forest,
                size: 18,
              ),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(fontWeight: FontWeight.w800, fontSize: 14)),
                  const SizedBox(height: 3),
                  Text(subtitle, style: TextStyle(color: MatriVaaniColors.muted, fontSize: 12)),
                ],
              ),
            ),
            Chip(
              label: Text(pending ? 'Pending' : 'Synced'),
              backgroundColor: pending ? MatriVaaniColors.primary.withValues(alpha: 0.12) : MatriVaaniColors.forest2.withValues(alpha: 0.12),
              side: BorderSide(color: pending ? MatriVaaniColors.primary.withValues(alpha: 0.25) : MatriVaaniColors.forest2.withValues(alpha: 0.25)),
            ),
            const SizedBox(width: 8),
            PressScale(
              key: pending ? const Key('sync_btn_play_pending') : const Key('sync_btn_play_synced'),
              onTap: () {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text(pending ? 'Playing: $title' : 'Replaying: $title')),
                );
              },
              scale: 0.92,
              child: Padding(
                padding: const EdgeInsets.all(8),
                child: Icon(Icons.play_circle_outline_rounded, color: MatriVaaniColors.forest, size: 28),
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final percent = (_bufferProgress * 100).round();

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 24),
      children: [
        const SizedBox(height: 6),
        // Top bar cards
        Row(
          children: [
            Expanded(
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                decoration: BoxDecoration(
                  color: MatriVaaniColors.forest2.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(999),
                  border: Border.all(color: MatriVaaniColors.forest2.withValues(alpha: 0.25)),
                ),
                child: Text(
                  'Local Mode Active',
                  style: TextStyle(color: MatriVaaniColors.forest, fontWeight: FontWeight.w800),
                ),
              ),
            ),
            const SizedBox(width: 10),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
              decoration: BoxDecoration(
                color: MatriVaaniColors.surface,
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: MatriVaaniColors.border),
              ),
              child: Text(
                'SQLite v3.45',
                style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w700, fontSize: 13),
              ),
            ),
          ],
        ),

        const SizedBox(height: 14),

        // Sync buffer summary
        Card(
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
            side: const BorderSide(color: MatriVaaniColors.border),
          ),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('SYNC BUFFER', style: TextStyle(color: MatriVaaniColors.primaryDark, fontWeight: FontWeight.w900, fontSize: 13)),
                      const SizedBox(height: 6),
                      Text('4 Items Pending', style: TextStyle(color: MatriVaaniColors.ink, fontWeight: FontWeight.w900, fontSize: 22)),
                      const SizedBox(height: 4),
                      Text('4 voice clips & student logs\nready to stream', style: TextStyle(color: MatriVaaniColors.muted, fontSize: 12)),
                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            decoration: BoxDecoration(
                              color: MatriVaaniColors.forest2.withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(999),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.wifi_outlined, size: 16, color: MatriVaaniColors.forest),
                                const SizedBox(width: 8),
                                Text('FastAPI ASR Server •', style: TextStyle(color: MatriVaaniColors.forest, fontWeight: FontWeight.w800, fontSize: 12)),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            decoration: BoxDecoration(
                              color: MatriVaaniColors.forest2.withValues(alpha: 0.12),
                              borderRadius: BorderRadius.circular(999),
                            ),
                            child: Text('Online', style: TextStyle(color: MatriVaaniColors.forest, fontWeight: FontWeight.w900, fontSize: 12)),
                          ),
                        ],
                      ),

                      const SizedBox(height: 10),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            decoration: BoxDecoration(
                              color: MatriVaaniColors.surfaceAlt,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: MatriVaaniColors.border),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.storage_outlined, size: 16, color: MatriVaaniColors.primaryDark),
                                const SizedBox(width: 8),
                                Text('SQLite: matrivaani_local.db', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800, fontSize: 12)),
                              ],
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            decoration: BoxDecoration(
                              color: MatriVaaniColors.surface,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(color: MatriVaaniColors.border),
                            ),
                            child: Text('Schema v4 • WAL Mode', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800, fontSize: 12)),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(width: 10),

                // Progress ring
                Column(
                  children: [
                    SizedBox(
                      height: 86,
                      width: 86,
                      child: Stack(
                        alignment: Alignment.center,
                        children: [
                          CircularProgressIndicator(
                            value: _bufferProgress,
                            strokeWidth: 10,
                            backgroundColor: MatriVaaniColors.border,
                            valueColor: AlwaysStoppedAnimation<Color>(MatriVaaniColors.primary),
                          ),
                          Container(
                            width: 54,
                            height: 54,
                            decoration: BoxDecoration(
                              color: MatriVaaniColors.surface,
                              borderRadius: BorderRadius.circular(18),
                              border: Border.all(color: MatriVaaniColors.border),
                            ),
                            child: Center(
                              child: Text(
                                '$percent%',
                                style: const TextStyle(fontWeight: FontWeight.w900),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text('${_bufferOk} / $_bufferTotal OK', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800, fontSize: 12)),
                  ],
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 16),

        // Sync CTA
        SizedBox(
          height: 58,
          width: double.infinity,
          child: AnimatedButton.elevated(
            key: const Key('sync_btn_sync_all'),
            onPressed: _syncAll,
            backgroundColor: MatriVaaniColors.primaryDark,
            foregroundColor: Colors.white,
            borderRadius: 18,
            padding: const EdgeInsets.symmetric(horizontal: 18, vertical: 16),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Icon(Icons.sync_alt_rounded, size: 20),
                const SizedBox(width: 10),
                Flexible(
                  child: Text(
                    _isSyncing ? 'Syncing…' : 'Sync All Data to Server',
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontWeight: FontWeight.w900, fontSize: 16),
                  ),
                ),
              ],
            ),
          ),
        ),

        const SizedBox(height: 14),

        // Storage partition bar
        Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20), side: const BorderSide(color: MatriVaaniColors.border)),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Storage Partition', style: TextStyle(color: MatriVaaniColors.ink, fontWeight: FontWeight.w900, fontSize: 16)),
                const SizedBox(height: 10),
                Text('14.2 GB Available', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800, fontSize: 12)),
                const SizedBox(height: 10),
                ClipRRect(
                  borderRadius: BorderRadius.circular(999),
                  child: Row(
                    children: [
                      Expanded(
                        flex: 18,
                        child: Container(height: 14, color: MatriVaaniColors.primary.withValues(alpha: 0.65)),
                      ),
                      Expanded(
                        flex: 6,
                        child: Container(height: 14, color: MatriVaaniColors.amber.withValues(alpha: 0.65)),
                      ),
                      Expanded(
                        flex: 46,
                        child: Container(height: 14, color: MatriVaaniColors.forest2.withValues(alpha: 0.65)),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 10),
                Row(
                  children: [
                    _LegendDot(color: MatriVaaniColors.primary, label: 'Audio (1.8 MB)'),
                    const SizedBox(width: 10),
                    _LegendDot(color: MatriVaaniColors.amber, label: 'DB (0.6 MB)'),
                    const SizedBox(width: 10),
                    _LegendDot(color: MatriVaaniColors.forest2, label: 'Free (14.2 GB)'),
                  ],
                )
              ],
            ),
          ),
        ),

        const SizedBox(height: 16),

        Text('Pending Queue & Logs', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 16, color: MatriVaaniColors.ink)),
        const SizedBox(height: 10),

        _pendingRow(
          title: 'Record #104',
          subtitle: 'Audio WAV (16kHz Mono • 4…',
          pending: true,
        ),
        _pendingRow(
          title: 'Record #103',
          subtitle: 'Audio WAV (16kHz Mono • 6…',
          pending: true,
        ),
        _pendingRow(
          title: 'Record #102',
          subtitle: 'Flashcard Progress • Synced',
          pending: false,
        ),
        _pendingRow(
          title: 'Record #101',
          subtitle: 'Classroom Session Log • Synced',
          pending: false,
        ),

        const SizedBox(height: 4),
        Align(
          alignment: Alignment.centerRight,
          child: AnimatedButton.outlined(
            key: const Key('sync_btn_clear_cache'),
            onPressed: _clearCache,
            borderColor: MatriVaaniColors.border,
            foregroundColor: MatriVaaniColors.primary,
            borderRadius: 14,
            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 10),
            child: const Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(Icons.delete_outline_rounded, size: 18),
                SizedBox(width: 6),
                Text('Clear Cache', style: TextStyle(fontWeight: FontWeight.w700)),
              ],
            ),
          ),
        ),

        const SizedBox(height: 18),

        // Diagnostics section
        Card(
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20), side: const BorderSide(color: MatriVaaniColors.border)),
          child: Padding(
            padding: const EdgeInsets.all(14),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Diagnostics & Sync Config', style: TextStyle(color: MatriVaaniColors.ink, fontWeight: FontWeight.w900, fontSize: 16)),
                const SizedBox(height: 12),
                _ToggleRow(
                  title: 'Auto-sync when Wi-Fi is available',
                  value: _autoSyncOnWifi,
                  onChanged: (v) => setState(() => _autoSyncOnWifi = v),
                ),
                const SizedBox(height: 12),
                _ToggleRow(
                  title: 'Save raw 16kHz WAV audio files locally',
                  value: _saveRawWavLocally,
                  onChanged: (v) => setState(() => _saveRawWavLocally = v),
                ),
                const SizedBox(height: 14),
                Text('Custom Backend Endpoint (FastAPI ASR)', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w900, fontSize: 13)),
                const SizedBox(height: 10),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: MatriVaaniColors.border),
                    color: MatriVaaniColors.surfaceAlt,
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.link_outlined, size: 18, color: MatriVaaniColors.primaryDark),
                      const SizedBox(width: 8),
                      Expanded(
                        child: TextField(
                          key: const Key('sync_endpoint_field'),
                          decoration: const InputDecoration(
                            isDense: true,
                            border: InputBorder.none,
                            hintText: 'http://…',
                          ),
                          controller: TextEditingController(text: _endpoint),
                          onChanged: (v) => _endpoint = v,
                        ),
                      ),
                      const SizedBox(width: 8),
                      AnimatedButton.outlined(
                        key: const Key('sync_btn_ping_server'),
                        onPressed: _pingServer,
                        borderColor: MatriVaaniColors.border,
                        foregroundColor: MatriVaaniColors.primaryDark,
                        borderRadius: 12,
                        padding: const EdgeInsets.all(8),
                        child: const Icon(Icons.save_alt_rounded, size: 20),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 8),
                Text('Ping Server: $_pingStatus', style: TextStyle(color: MatriVaaniColors.muted, fontWeight: FontWeight.w800, fontSize: 12)),

                const SizedBox(height: 14),
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: MatriVaaniColors.surfaceAlt,
                    borderRadius: BorderRadius.circular(16),
                    border: Border.all(color: MatriVaaniColors.border),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.shield_outlined, color: MatriVaaniColors.forest, size: 18),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(
                          'MatriVaani Offline Guard: All Santali speech samples are encrypted and securely stored in your local phone storage (SQLite).',
                          style: TextStyle(color: MatriVaaniColors.muted, fontSize: 12, fontWeight: FontWeight.w700),
                        ),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),

        const SizedBox(height: 12),
      ],
    );
  }
}

class _LegendDot extends StatelessWidget {
  final Color color;
  final String label;

  const _LegendDot({required this.color, required this.label});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(width: 9, height: 9, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
        const SizedBox(width: 6),
        Text(label, style: TextStyle(color: MatriVaaniColors.muted, fontSize: 12, fontWeight: FontWeight.w800)),
      ],
    );
  }
}

class _ToggleRow extends StatelessWidget {
  final String title;
  final bool value;
  final ValueChanged<bool> onChanged;

  const _ToggleRow({required this.title, required this.value, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: Text(title, style: TextStyle(color: MatriVaaniColors.muted, fontSize: 13, fontWeight: FontWeight.w900)),
        ),
        Switch(
          value: value,
          onChanged: onChanged,
          activeThumbColor: MatriVaaniColors.forest,
        )
      ],
    );
  }
}
