import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'dart:convert';
import 'package:uuid/uuid.dart';

class DatabaseService {
  static final DatabaseService instance = DatabaseService._init();
  static Database? _database;

  DatabaseService._init();

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB('matrivaani_local.db');
    return _database!;
  }

  Future<Database> _initDB(String filePath) async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, filePath);
    return await openDatabase(path, version: 1, onCreate: _createDB);
  }

  Future _createDB(Database db, int version) async {
    await db.execute('''
CREATE TABLE content (
  id TEXT PRIMARY KEY,
  content_type TEXT NOT NULL,
  topic TEXT,
  language TEXT,
  data TEXT NOT NULL,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  deleted INTEGER DEFAULT 0,
  dirty INTEGER DEFAULT 0
)
''');
  }

  Future<List<Map<String, dynamic>>> getDirtyRecords() async {
    final db = await instance.database;
    return await db.query('content', where: 'dirty = ?', whereArgs: [1]);
  }

  Future<void> saveServerRecords(List<dynamic> records) async {
    final db = await instance.database;
    Batch batch = db.batch();
    for (var rec in records) {
      batch.insert('content', {
        'id': rec['id'],
        'content_type': rec['content_type'],
        'topic': rec['topic'],
        'language': rec['language'],
        'data': json.encode(rec['data']),
        'created_at': rec['created_at'],
        'updated_at': rec['updated_at'],
        'deleted': rec['deleted'] ? 1 : 0,
        'dirty': 0
      }, conflictAlgorithm: ConflictAlgorithm.replace);
    }
    await batch.commit(noResult: true);
    await db.rawUpdate('UPDATE content SET dirty = 0');
  }

  Future<List<Map<String, dynamic>>> getContent(String type) async {
    final db = await instance.database;
    return await db.query('content', where: 'content_type = ? AND deleted = 0', whereArgs: [type]);
  }

  Future<String> createContentOffline(String type, String topic, String language, Map<String, dynamic> data) async {
    final db = await instance.database;
    final id = Uuid().v4();
    final now = DateTime.now().toIso8601String();
    await db.insert('content', {
      'id': id,
      'content_type': type,
      'topic': topic,
      'language': language,
      'data': json.encode(data),
      'created_at': now,
      'updated_at': now,
      'deleted': 0,
      'dirty': 1
    });
    return id;
  }
}
