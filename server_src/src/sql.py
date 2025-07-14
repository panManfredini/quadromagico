import sqlite3
from datetime import datetime
from typing import Dict, List

DB_PATH = "/home/pan/Documents/quadromagico/quadromagico.db"


with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            thumbnail_path TEXT NOT NULL,
            image_path TEXT NOT NULL,
            title TEXT,
            prompt TEXT
        );
    ''')



def insert_image_sql_record(created_at:datetime, thumbnail_path:str, image_path:str, title:str="",prompt:str=""):
    dt = created_at.isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()    
        cursor.execute("INSERT INTO images (created_at, thumbnail_path, image_path, title, prompt) VALUES (?,?,?,?,?)",
                                       (dt,         thumbnail_path, image_path, title, prompt))    


def get_all_sql_images()->List[Dict[str,any]]:
    query = """
        SELECT * FROM images
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()    
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
    
    return [dict(zip(columns, row)) for row in rows]