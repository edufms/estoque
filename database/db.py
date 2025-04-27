import sqlite3
from pathlib import Path

DB_PATH = Path('estoque.db')  # muda para criar na raiz

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT,
        validade DATE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS compras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        data_compra DATE,
        mercado TEXT,
        valor REAL,
        quantidade INTEGER,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER,
        data_uso DATE,
        quantidade INTEGER,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL
    )
    ''')


    conn.commit()
    conn.close()
