from database.db import get_connection
from api.models import Produto, Compra, Uso

def adicionar_produto(produto: Produto):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produtos (nome, categoria, validade) 
        VALUES (?, ?, ?)
    ''', (produto.nome, produto.categoria, produto.validade))
    conn.commit()
    conn.close()

def listar_produtos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, nome, categoria, validade FROM produtos')
    rows = cursor.fetchall()
    conn.close()
    return rows

def registrar_compra(compra: Compra):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO compras (produto_id, data_compra, mercado, valor, quantidade) 
        VALUES (?, ?, ?, ?, ?)
    ''', (compra.produto_id, compra.data_compra, compra.mercado, compra.valor, compra.quantidade))
    conn.commit()
    conn.close()

def registrar_uso(uso: Uso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usos (produto_id, data_uso, quantidade) 
        VALUES (?, ?, ?)
    ''', (uso.produto_id, uso.data_uso, uso.quantidade))
    conn.commit()
    conn.close()
