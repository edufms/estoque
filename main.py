import streamlit as st
from database.db import create_tables
from api.controllers import adicionar_produto, listar_produtos, registrar_compra, registrar_uso, calcular_estoque_atual, listar_categorias, adicionar_categoria
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

    categorias_existentes = listar_categorias()
    opcoes = categorias_existentes + ['__nova__']

    categoria_escolhida = st.selectbox(
        'Categoria',
        options=opcoes,
        format_func=lambda x: '➕ Criar nova categoria' if x == '__nova__' else x
    )

    if categoria_escolhida == '__nova__':
        nova_categoria = st.text_input('Digite o nome da nova categoria')
        if nova_categoria:
            adicionar_categoria(nova_categoria)
            categoria_final = nova_categoria
        else:
            categoria_final = None
    else:
        categoria_final = categoria_escolhida

    if st.button('Salvar Produto'):
        if nome and categoria_final:
            produto = Produto(nome=nome, categoria=categoria_final)
            adicionar_produto(produto)
            st.success('Produto adicionado com sucesso!')
        else:
            st.error('Por favor, preencha o nome e a categoria!')


elif menu == 'Registrar Compra':
    st.header('Registrar Compra')

    produtos = listar_produtos()
    produto_nomes = [produto.nome for produto in produtos]

    produto_selecionado = st.selectbox('Produto', produto_nomes)

    data_compra = st.date_input('Data da compra', value=datetime.date.today())
    valor = st.number_input('Valor da compra', min_value=0.0, step=0.01, format="%.2f")
    mercado = st.text_input('Mercado onde comprou')
    validade = st.date_input('Data de validade do produto')

    if st.button('Salvar Compra'):
        produto_obj = next((p for p in produtos if p.nome == produto_selecionado), None)
        if produto_obj:
            registrar_compra(produto_id=produto_obj.id, data_compra=data_compra, valor=valor, mercado=mercado, validade=validade)
            st.success('Compra registrada com sucesso!')
        else:
            st.error('Produto não encontrado!')


elif menu == 'Registrar Uso':
    st.header('Registrar Uso')

    produtos = listar_produtos()
    produto_nomes = [produto.nome for produto in produtos]

    produto_selecionado = st.selectbox('Produto', produto_nomes)

    data_lancamento = st.date_input('Data de lançamento', value=datetime.date.today())
    data_uso = st.date_input('Data de uso', value=datetime.date.today())
    quantidade = st.number_input('Quantidade utilizada', min_value=0.0, step=0.1)

    if st.button('Salvar Uso'):
        produto_obj = next((p for p in produtos if p.nome == produto_selecionado), None)
        if produto_obj:
            registrar_uso(produto_id=produto_obj.id, data_lancamento=data_lancamento, data_uso=data_uso, quantidade=quantidade)
            st.success('Uso registrado com sucesso!')
        else:
            st.error('Produto não encontrado!')


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
