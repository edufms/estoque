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

def registrar_compra(produto_id, data_compra, valor, mercado, validade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO compras (produto_id, data_compra, valor, mercado)
        VALUES (?, ?, ?, ?)
    ''', (produto_id, data_compra, valor, mercado))
    conn.commit()

    # Atualiza a validade no produto
    cursor.execute('''
        UPDATE produtos SET validade = ? WHERE id = ?
    ''', (validade, produto_id))

    conn.commit()
    conn.close()

def registrar_uso(produto_id, data_lancamento, data_uso, quantidade):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usos (produto_id, data_uso, quantidade)
        VALUES (?, ?, ?)
    ''', (produto_id, data_uso, quantidade))
    conn.commit()
    conn.close()


def calcular_estoque_atual():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    SELECT 
        p.id, 
        p.nome, 
        p.categoria,
        p.validade,
        IFNULL(SUM(c.quantidade), 0) as total_comprado,
        IFNULL(SUM(u.quantidade), 0) as total_usado,
        (IFNULL(SUM(c.quantidade), 0) - IFNULL(SUM(u.quantidade), 0)) as estoque_atual
    FROM produtos p
    LEFT JOIN compras c ON p.id = c.produto_id
    LEFT JOIN usos u ON p.id = u.produto_id
    GROUP BY p.id
    ''')

    rows = cursor.fetchall()
    conn.close()
    return rows

def listar_categorias():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT nome FROM categorias')
    categorias = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categorias

def adicionar_categoria(nome_categoria):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO categorias (nome) VALUES (?)', (nome_categoria,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # se já existir, ignora
    conn.close()