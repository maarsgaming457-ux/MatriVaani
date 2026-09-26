import re

with open('tools/ho_annotator/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_return = '''    c.execute(\"""
        UPDATE annotations SET
        ho = ?, hindi = ?, category = ?, human_verified = ?, review_status = ?, notes = ?
        WHERE id = ?
    \""", (data.ho, data.hindi, data.category, data.human_verified, data.review_status, data.notes, record_id))
    conn.commit()
    conn.close()
    return {"status": "success"}'''

new_return = '''    c.execute(\"""
        UPDATE annotations SET
        ho = ?, hindi = ?, category = ?, human_verified = ?, review_status = ?, notes = ?
        WHERE id = ?
    \""", (data.ho, data.hindi, data.category, data.human_verified, data.review_status, data.notes, record_id))
    conn.commit()
    conn.close()
    return {"status": "success", "human_verified": data.human_verified, "review_status": data.review_status}'''

content = content.replace(old_return, new_return)

with open('tools/ho_annotator/app.py', 'w', encoding='utf-8') as f:
    f.write(content)
