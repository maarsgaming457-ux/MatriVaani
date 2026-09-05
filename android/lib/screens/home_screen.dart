import 'package:flutter/material.dart';
import '../services/sync_service.dart';
import 'classroom_screen.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _syncStatus = "Checking...";

  @override
  void initState() {
    super.initState();
    _performSync();
  }

  Future<void> _performSync() async {
    setState(() => _syncStatus = "Syncing...");
    bool success = await SyncService.syncData();
    setState(() {
      _syncStatus = success ? "Synced (Online)" : "Offline (Cached Mode)";
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('MatriVaani'),
        actions: [
          Center(
            child: Padding(
              padding: const EdgeInsets.only(right: 16.0),
              child: Text(_syncStatus, style: TextStyle(fontSize: 12)),
            ),
          )
        ],
      ),
      body: GridView.count(
        crossAxisCount: 2,
        padding: EdgeInsets.all(16.0),
        children: [
          _buildCard("Classroom (Voice)", Icons.mic, () {
            Navigator.push(context, MaterialPageRoute(builder: (_) => ClassroomScreen()));
          }),
          _buildCard("Lessons", Icons.book, () {}),
          _buildCard("Worksheets", Icons.assignment, () {}),
          _buildCard("Flashcards", Icons.style, () {}),
          _buildCard("Sync Data", Icons.sync, _performSync),
        ],
      ),
    );
  }

  Widget _buildCard(String title, IconData icon, VoidCallback onTap) {
    return Card(
      elevation: 4.0,
      margin: EdgeInsets.all(8.0),
      child: InkWell(
        onTap: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 50.0, color: Colors.green),
            SizedBox(height: 10),
            Text(title, textAlign: TextAlign.center, style: TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
