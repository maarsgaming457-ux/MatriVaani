import os
import sqlite3
import json
from datetime import datetime
import uuid

class OfflineService:
    def __init__(self, db_path="content/matrivaani_offline.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
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
                    deleted INTEGER DEFAULT 0
                )
            ''')
            # Check if columns updated_at and deleted exist for legacy databases
            cursor.execute("PRAGMA table_info(content)")
            columns = [c[1] for c in cursor.fetchall()]
            if 'updated_at' not in columns:
                cursor.execute("ALTER TABLE content ADD COLUMN updated_at TEXT")
                cursor.execute("UPDATE content SET updated_at = created_at")
            if 'deleted' not in columns:
                cursor.execute("ALTER TABLE content ADD COLUMN deleted INTEGER DEFAULT 0")
            
            # If id is INTEGER in legacy, we have a migration issue. For simplicity, we drop and recreate if legacy integer ID is found, or we just handle it. 
            # In our previous implementation, id was INTEGER PRIMARY KEY AUTOINCREMENT.
            # We will migrate to TEXT UUIDs.
            cursor.execute("PRAGMA table_info(content)")
            id_type = [c[2] for c in cursor.fetchall() if c[1] == 'id'][0]
            if id_type == 'INTEGER':
                # Migration: rename table, create new, copy data
                cursor.execute("ALTER TABLE content RENAME TO content_old")
                cursor.execute('''
                    CREATE TABLE content (
                        id TEXT PRIMARY KEY,
                        content_type TEXT NOT NULL,
                        topic TEXT,
                        language TEXT,
                        data TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        updated_at TEXT NOT NULL,
                        deleted INTEGER DEFAULT 0
                    )
                ''')
                cursor.execute('''
                    INSERT INTO content (id, content_type, topic, language, data, created_at, updated_at, deleted)
                    SELECT CAST(id AS TEXT), content_type, topic, language, data, created_at, IFNULL(updated_at, created_at), IFNULL(deleted, 0) FROM content_old
                ''')
                cursor.execute("DROP TABLE content_old")
            conn.commit()

    def save_content(self, content_type: str, topic: str, language: str, data: dict, item_id: str = None) -> str:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            
            if item_id:
                # Check if exists
                cursor.execute('SELECT id FROM content WHERE id = ?', (item_id,))
                exists = cursor.fetchone()
                if exists:
                    cursor.execute('''
                        UPDATE content 
                        SET content_type = ?, topic = ?, language = ?, data = ?, updated_at = ?, deleted = 0
                        WHERE id = ?
                    ''', (content_type, topic, language, json.dumps(data, ensure_ascii=False), now, item_id))
                    conn.commit()
                    return item_id

            item_id = item_id or str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO content (id, content_type, topic, language, data, created_at, updated_at, deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            ''', (item_id, content_type, topic, language, json.dumps(data, ensure_ascii=False), now, now))
            conn.commit()
            return item_id

    def delete_content(self, item_id: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            now = datetime.now().isoformat()
            cursor.execute('UPDATE content SET deleted = 1, updated_at = ? WHERE id = ?', (now, item_id))
            conn.commit()

    def get_content(self, content_type: str = None, include_deleted: bool = False):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = 'SELECT id, content_type, topic, language, data, created_at, updated_at, deleted FROM content'
            params = []
            conditions = []
            
            if content_type:
                conditions.append('content_type = ?')
                params.append(content_type)
            if not include_deleted:
                conditions.append('deleted = 0')
                
            if conditions:
                query += ' WHERE ' + ' AND '.join(conditions)
                
            query += ' ORDER BY updated_at DESC'
            
            cursor.execute(query, tuple(params))
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

    def sync(self, client_changes: list) -> list:
        # Two-way sync: push client changes, return server changes
        server_state = {item['id']: item for item in self.get_content(include_deleted=True)}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for change in client_changes:
                client_id = change['id']
                if client_id in server_state:
                    # Conflict resolution: Last Write Wins (LWW)
                    if change['updated_at'] > server_state[client_id]['updated_at']:
                        cursor.execute('''
                            UPDATE content 
                            SET content_type=?, topic=?, language=?, data=?, updated_at=?, deleted=?
                            WHERE id=?
                        ''', (
                            change['content_type'], change['topic'], change['language'], 
                            json.dumps(change['data'], ensure_ascii=False), change['updated_at'], 
                            1 if change.get('deleted') else 0, client_id
                        ))
                else:
                    # New from client
                    cursor.execute('''
                        INSERT INTO content (id, content_type, topic, language, data, created_at, updated_at, deleted)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        client_id, change['content_type'], change['topic'], change['language'], 
                        json.dumps(change['data'], ensure_ascii=False), change['created_at'], 
                        change['updated_at'], 1 if change.get('deleted') else 0
                    ))
            conn.commit()
            
        # Return new state to client
        return self.get_content(include_deleted=True)
