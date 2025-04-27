import streamlit as st
from database.db import create_tables
from api.controllers import adicionar_produto, listar_produtos, registrar_compra, registrar_uso, calcular_estoque_atual
from api.models import Produto, Compra, Uso
import datetime

# Cria tabelas ao iniciar
create_tables()

st.title('🛒 Controle de Estoque Doméstico')

menu = st.sidebar.selectbox('Menu', [
    'Adicionar Produto', 
    'Registrar Compra', 
    'Registrar Uso', 
    'Listar Produtos',
    '📦 Estoque Atual'
])

if menu == 'Adicionar Produto':
    st.header('Adicionar Produto')
    nome = st.text_input('Nome do produto')
    categoria = st.text_input('Categoria')
    validade = st.date_input('Data de validade', value=datetime.date.today())

    if st.button('Salvar Produto'):
        produto = Produto(nome=nome, categoria=categoria, validade=validade)
        adicionar_produto(produto)
        st.success('Produto adicionado com sucesso!')

elif menu == 'Registrar Compra':
    st.header('Registrar Compra')
    produtos = listar_produtos()
    if produtos:
        produto_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in produtos}
        produto_escolhido = st.selectbox('Produto', list(produto_dict.keys()))
        
        data_compra = st.date_input('Data da compra', value=datetime.date.today())
        mercado = st.text_input('Mercado')
        valor = st.number_input('Valor da compra (total)', min_value=0.0, format="%.2f")
        quantidade = st.number_input('Quantidade comprada', min_value=1, step=1)

        if st.button('Registrar Compra'):
            compra = Compra(produto_id=produto_dict[produto_escolhido], data_compra=data_compra, mercado=mercado, valor=valor, quantidade=quantidade)
            registrar_compra(compra)
            st.success('Compra registrada!')
    else:
        st.warning('Nenhum produto cadastrado ainda.')

elif menu == 'Registrar Uso':
    st.header('Registrar Uso')
    produtos = listar_produtos()
    if produtos:
        produto_dict = {f"{p[1]} (ID {p[0]})": p[0] for p in produtos}
        produto_escolhido = st.selectbox('Produto', list(produto_dict.keys()))
        
        data_uso = st.date_input('Data do uso', value=datetime.date.today())
        quantidade = st.number_input('Quantidade usada', min_value=1, step=1)

        if st.button('Registrar Uso'):
            uso = Uso(produto_id=produto_dict[produto_escolhido], data_uso=data_uso, quantidade=quantidade)
            registrar_uso(uso)
            st.success('Uso registrado!')
    else:
        st.warning('Nenhum produto cadastrado ainda.')

elif menu == 'Listar Produtos':
    st.header('Produtos Cadastrados')
    produtos = listar_produtos()
    if produtos:
        for p in produtos:
            st.write(f"**Nome:** {p[1]} | **Categoria:** {p[2]} | **Validade:** {p[3]}")
    else:
        st.info('Nenhum produto cadastrado.')

elif menu == '📦 Estoque Atual':
    st.header('📦 Estoque Atual')
    estoque = calcular_estoque_atual()

    if estoque:
        for item in estoque:
            produto_id, nome, categoria, validade, comprado, usado, atual = item
            validade_dt = datetime.datetime.strptime(validade, '%Y-%m-%d').date() if validade else None
            dias_restantes = (validade_dt - datetime.date.today()).days if validade_dt else None

            st.subheader(f"🔹 {nome}")
            st.write(f"**Categoria:** {categoria}")
            st.write(f"**Quantidade em estoque:** {atual}")

            if validade_dt:
                if dias_restantes < 0:
                    st.error(f"VENCIDO há {-dias_restantes} dias! ⚠️")
                elif dias_restantes <= 7:
                    st.warning(f"Vence em {dias_restantes} dias! ⚠️")
                else:
                    st.info(f"Validade: {validade_dt}")
            else:
                st.info("Sem data de validade.")
    else:
        st.info('Nenhum produto cadastrado ou movimentado ainda.')
