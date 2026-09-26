import os

db_path = 'android/lib/services/db_service.dart'
with open(db_path, 'r', encoding='utf-8') as f:
    db_content = f.read()

get_all_target = '''  Future<Map<String, dynamic>?> getLatestIncompleteJob() async {'''
get_all_replacement = '''  Future<List<Map<String, dynamic>>> getAllIncompleteJobs() async {
    final db = await instance.database;
    return await db.query(
      'classroom_jobs',
      where: 'status != ?',
      whereArgs: ['COMPLETED'],
      orderBy: 'created_at ASC',
    );
  }

  Future<Map<String, dynamic>?> getLatestIncompleteJob() async {'''

db_content = db_content.replace(get_all_target, get_all_replacement)

with open(db_path, 'w', encoding='utf-8') as f:
    f.write(db_content)


screen_path = 'android/lib/screens/classroom_screen.dart'
with open(screen_path, 'r', encoding='utf-8') as f:
    sc_content = f.read()

queue_target = '''    try {
      while (true) {
        if (!mounted) break;
        final job = await DatabaseService.instance.getLatestIncompleteJob();
        if (job == null) break;

        // Skip if internet dropped
        if (!_isOnline) break;

        int newCount = (job['retry_count'] as int? ?? 0) + 1;
        await DatabaseService.instance.updateClassroomJob(job['id'] as String, {'retry_count': newCount});
        
        final mutableJob = Map<String, dynamic>.from(job);
        mutableJob['retry_count'] = newCount;

        await _processClassroomJob(job['id'] as String, mutableJob);

        // Wait a tiny bit between jobs to prevent API flooding or UI locking
        await Future.delayed(const Duration(milliseconds: 500));
      }
    } finally {'''

queue_replacement = '''    try {
      final jobs = await DatabaseService.instance.getAllIncompleteJobs();
      for (var job in jobs) {
        if (!mounted) break;
        if (!_isOnline) break;

        // Double check status in case it was modified elsewhere
        final currentJob = await DatabaseService.instance.getClassroomJob(job['id'] as String);
        if (currentJob == null || currentJob['status'] == 'COMPLETED') continue;

        int newCount = (currentJob['retry_count'] as int? ?? 0) + 1;
        await DatabaseService.instance.updateClassroomJob(currentJob['id'] as String, {'retry_count': newCount});
        
        final mutableJob = Map<String, dynamic>.from(currentJob);
        mutableJob['retry_count'] = newCount;

        await _processClassroomJob(currentJob['id'] as String, mutableJob);

        await Future.delayed(const Duration(milliseconds: 500));
      }
    } finally {'''

sc_content = sc_content.replace(queue_target, queue_replacement)

with open(screen_path, 'w', encoding='utf-8') as f:
    f.write(sc_content)
print("Done")
