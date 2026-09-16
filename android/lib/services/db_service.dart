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
    return await openDatabase(
      path, 
      version: 2, 
      onCreate: _createDB,
      onUpgrade: _upgradeDB,
    );
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
    if (version >= 2) {
      await _createClassroomJobsTable(db);
    }
  }

  Future _upgradeDB(Database db, int oldVersion, int newVersion) async {
    if (oldVersion < 2) {
      await _createClassroomJobsTable(db);
    }
  }

  Future _createClassroomJobsTable(Database db) async {
    await db.execute('''
CREATE TABLE classroom_jobs (
  id TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  source_lang TEXT NOT NULL,
  target_lang TEXT NOT NULL,
  audio_path TEXT NOT NULL,
  transcription TEXT,
  translation TEXT,
  status TEXT NOT NULL,
  retry_count INTEGER DEFAULT 0,
  last_error TEXT
)
''');
  }

  // ClassroomJob CRUD Methods

  Future<String> createClassroomJob({
    required String sourceLang,
    required String targetLang,
    required String audioPath,
  }) async {
    final db = await instance.database;
    final id = const Uuid().v4();
    final now = DateTime.now().toIso8601String();
    await db.insert('classroom_jobs', {
      'id': id,
      'created_at': now,
      'updated_at': now,
      'source_lang': sourceLang,
      'target_lang': targetLang,
      'audio_path': audioPath,
      'status': 'RECORDED',
      'retry_count': 0,
    });
    return id;
  }

  Future<void> updateClassroomJob(String id, Map<String, dynamic> updates) async {
    final db = await instance.database;
    updates['updated_at'] = DateTime.now().toIso8601String();
    await db.update('classroom_jobs', updates, where: 'id = ?', whereArgs: [id]);
  }

  Future<Map<String, dynamic>?> getClassroomJob(String id) async {
    final db = await instance.database;
    final results = await db.query('classroom_jobs', where: 'id = ?', whereArgs: [id]);
    if (results.isNotEmpty) {
      return results.first;
    }
    return null;
  }

  Future<List<Map<String, dynamic>>> getAllIncompleteJobs() async {
    final db = await instance.database;
    return await db.query(
      'classroom_jobs',
      where: 'status != ?',
      whereArgs: ['COMPLETED'],
      orderBy: 'created_at ASC',
    );
  }

  Future<Map<String, dynamic>?> getLatestIncompleteJob() async {
    final db = await instance.database;
    final results = await db.query(
      'classroom_jobs',
      where: 'status != ?',
      whereArgs: ['COMPLETED'],
      orderBy: 'created_at DESC',
      limit: 1,
    );
    if (results.isNotEmpty) {
      return results.first;
    }
    return null;
  }

  Future<List<Map<String, dynamic>>> getExpiredCompletedJobs(DateTime cutoffDate) async {
    final db = await instance.database;
    return await db.query(
      'classroom_jobs',
      where: 'status = ? AND updated_at < ?',
      whereArgs: ['COMPLETED', cutoffDate.toIso8601String()],
    );
  }

  Future<void> deleteClassroomJob(String id) async {
    final db = await instance.database;
    await db.delete('classroom_jobs', where: 'id = ?', whereArgs: [id]);
  }

  // Content Methods (Existing)

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
    final id = const Uuid().v4();
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
