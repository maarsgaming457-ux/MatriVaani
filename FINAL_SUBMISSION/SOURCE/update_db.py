import os

filepath = 'android/lib/services/db_service.dart'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''  // Content Methods (Existing)'''
new_methods = '''  Future<List<Map<String, dynamic>>> getExpiredCompletedJobs(DateTime cutoffDate) async {
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

  // Content Methods (Existing)'''

content = content.replace(target, new_methods)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done DB")
