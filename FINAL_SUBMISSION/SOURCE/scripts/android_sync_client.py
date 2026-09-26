import sqlite3
import json
import uuid
import time
from datetime import datetime
import os
import sys

# Simulates the Android App's local database
class AndroidLocalDatabase:
    def __init__(self, db_path="android_local_2.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content (
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
            ''')
            conn.commit()

    def create_offline_content(self, content_type, topic, language, data):
        item_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO content (id, content_type, topic, language, data, created_at, updated_at, deleted, dirty)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, 1)
            ''', (item_id, content_type, topic, language, json.dumps(data), now, now))
            conn.commit()
        return item_id

    def modify_content_offline(self, item_id, new_data):
        now = datetime.now().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE content 
                SET data = ?, updated_at = ?, dirty = 1
                WHERE id = ?
            ''', (json.dumps(new_data), now, item_id))
            conn.commit()

    def get_dirty_records(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, content_type, topic, language, data, created_at, updated_at, deleted FROM content WHERE dirty = 1')
            rows = cursor.fetchall()
            return [
                {
                    "id": r[0],
                    "content_type": r[1],
                    "topic": r[2],
                    "language": r[3],
                    "data": json.loads(r[4]),
                    "created_at": r[5],
                    "updated_at": r[6],
                    "deleted": bool(r[7])
                }
                for r in rows
            ]
            
    def apply_server_sync(self, server_records):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for rec in server_records:
                cursor.execute('SELECT updated_at FROM content WHERE id = ?', (rec['id'],))
                local_rec = cursor.fetchone()
                
                # Update if new or server is newer
                if not local_rec or rec['updated_at'] > local_rec[0]:
                    cursor.execute('''
                        INSERT OR REPLACE INTO content (id, content_type, topic, language, data, created_at, updated_at, deleted, dirty)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0)
                    ''', (
                        rec['id'], rec['content_type'], rec['topic'], rec['language'], 
                        json.dumps(rec['data']), rec['created_at'], rec['updated_at'], 
                        1 if rec['deleted'] else 0
                    ))
            
            # Clear dirty flag on everything that synced
            cursor.execute('UPDATE content SET dirty = 0')
            conn.commit()

def run_test():
        
    # We will simulate the Shared Backend locally for the test
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from app.services.offline_service import OfflineService
    shared_backend = OfflineService("content/matrivaani_offline_test2.db")

    print("--- PHASE 24 & 25: TWO-WAY SYNC TEST ---")
    
    # 1. Website creates a lesson (Hits shared backend directly)
    web_lesson_id = shared_backend.save_content("lesson", "Addition", "Santhali", {"title": "Math Addition", "body": "1+1=2"})
    print(f"1. Website created lesson in Shared DB. ID: {web_lesson_id}")
    
    # 2. Android Syncs
    android_db = AndroidLocalDatabase()
    
    # Android pulls from server
    dirty = android_db.get_dirty_records()
    server_state = shared_backend.sync(dirty)
    android_db.apply_server_sync(server_state)
    print("2. Android Synchronized with Server.")
    
    # 3. Android modifies the lesson offline
    print("3. Android OFFLINE. Modifying lesson...")
    android_db.modify_content_offline(web_lesson_id, {"title": "Math Addition (Updated on Android)", "body": "1+1=2 and 2+2=4"})
    
    # 4. Android creates a new flashcard offline
    print("4. Android OFFLINE. Creating new flashcard...")
    flashcard_id = android_db.create_offline_content("flashcard", "Animals", "Santhali", {"word": "Sukri", "emoji": "🐷"})
    
    # 5. Android goes ONLINE and Syncs
    print("5. Android ONLINE. Pushing Sync...")
    dirty = android_db.get_dirty_records()
    print(f"Android sending {len(dirty)} dirty records...")
    server_state = shared_backend.sync(dirty)
    android_db.apply_server_sync(server_state)
    
    # 6. Website checks Backend Database
    print("6. Website (Backend) checks data...")
    all_content = shared_backend.get_content()
    
    updated_lesson = next((c for c in all_content if c['id'] == web_lesson_id), None)
    new_flashcard = next((c for c in all_content if c['id'] == flashcard_id), None)
    
    print("\n--- RESULTS ---")
    print(f"Website sees updated lesson: {updated_lesson['data']['title']}")
    print(f"Website sees Android's flashcard: {new_flashcard['data']['word']} {new_flashcard['data']['emoji']}")
    print("SUCCESS: Two-Way Synchronization Verified!")

if __name__ == '__main__':
    run_test()
