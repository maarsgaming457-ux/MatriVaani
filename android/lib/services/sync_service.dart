import 'api_service.dart';
import 'db_service.dart';
import 'dart:convert';

class SyncService {
  static Future<bool> syncData() async {
    try {
      bool online = await ApiService.isOnline();
      if (!online) return false;

      final dirtyRecords = await DatabaseService.instance.getDirtyRecords();
      
      List<Map<String, dynamic>> payload = dirtyRecords.map((r) {
        return {
          "id": r['id'],
          "content_type": r['content_type'],
          "topic": r['topic'],
          "language": r['language'],
          "data": json.decode(r['data'] as String),
          "created_at": r['created_at'],
          "updated_at": r['updated_at'],
          "deleted": r['deleted'] == 1
        };
      }).toList();

      final serverState = await ApiService.syncData(payload);
      await DatabaseService.instance.saveServerRecords(serverState);
      return true;
    } catch (e) {
      print("Sync Error: $e");
      return false;
    }
  }
}
