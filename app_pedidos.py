import streamlit as st
import pandas as pd

# Configuração inicial da página
st.set_page_config(page_title="Gestão de Pedidos - Horti Japonês", layout="wide")

# Base de produtos extraída da sua imagem (Produtos Orientais)
produtos_base = [
    {"Código": 521798, "Descrição": "Ampan Azuki C/6 Satsumaya", "Marca": "Satsumaya"},
    {"Código": 520504, "Descrição": "Kamaboko 200g Agronippo", "Marca": "Agronippo"},
    {"Código": 521150, "Descrição": "Kamaboko 200g Kai-Ho Agronippo", "Marca": "Agronippo"},
    {"Código": 521974, "Descrição": "Lokyozuke Cebolinha 200g Marunaka Cons", "Marca": "Agronippo"},
    {"Código": 533623, "Descrição": "Massa Gobomaki Kai-Ho 200g", "Marca": "Agronippo"},
    {"Código": 53662, "Descrição": "Massa Konnyaku 350g C/Alga", "Marca": "Agronippo"},
    {"Código": 524768, "Descrição": "Massa Shirataki 200g Agronippo Noodles", "Marca": "Agronippo"},
    {"Código": 583497, "Descrição": "Massa Shirataki 200g Hyde Alimentos", "Marca": "Hyde Alimentos"},
    {"Código": 577362, "Descrição": "Mirinzuke 200g Conserva De Nabo", "Marca": "Agronippo"},
    {"Código": 520911, "Descrição": "Narutomakii Kai.Ho 200g", "Marca": "Agronippo"},
    {"Código": 141820, "Descrição": "Nippo Kyoka Natto 100g", "Marca": "Agronippo"},
    {"Código": 524713, "Descrição": "Nippo Shirataki 200g", "Marca": "Agronippo"},
    {"Código": 139940, "Descrição": "Shogazuke 245g Beni Shoga", "Marca": "Agronippo"},
    {"Código": 55406, "Descrição": "Sushi Ague 110g Agronippo", "Marca": "Agronippo"}
]

# Lista de lojas conforme a imagem 3
lojas = ["Loja 1", "Loja 2", "Loja 5", "Loja 6", "Loja 7", "Loja 8"]

# Inicialização do banco de dados temporário na sessão (Session State)
# Posteriormente, você pode conectar isso diretamente à API do Google Sheets
if 'df_pedidos' not in st.session_state:
    df = pd.DataFrame(produtos_base)
    for loja in lojas:
        df[loja] = 0 # Inicializa todas as lojas com zero pedidos
    st.session_state['df_pedidos'] = df

st.title("🍣 Gestão de Pedidos Web - Produtos Orientais")

# Navegação Lateral
menu = st.sidebar.radio("Selecione o Perfil de Acesso:", ["Área da Loja (Digitação)", "Área do Supervisor (Gerencial)"])

# ---------------------------------------------------------
# VISÃO DA LOJA
# ---------------------------------------------------------
if menu == "Área da Loja (Digitação)":
    st.header("Lançamento Semanal de Pedidos")
    
    loja_selecionada = st.selectbox("Selecione a sua Loja:", lojas)
    st.info(f"Preencha as quantidades solicitadas para a **{loja_selecionada}**. Os demais campos estão bloqueados para edição.")
    
    # Filtra o dataframe para mostrar apenas os produtos e a coluna da loja atual
    df_exibicao = st.session_state['df_pedidos'][['Código', 'Descrição', 'Marca', loja_selecionada]].copy()
    
    # st.data_editor permite que a loja edite apenas a sua coluna
    df_editado = st.data_editor(
        df_exibicao,
        column_config={
            "Código": st.column_config.NumberColumn(disabled=True),
            "Descrição": st.column_config.TextColumn(disabled=True),
            "Marca": st.column_config.TextColumn(disabled=True),
            loja_selecionada: st.column_config.NumberColumn("Qtd Pedido", min_value=0, step=1)
        },
        hide_index=True,
        use_container_width=True,
        height=500
    )
    
    if st.button("💾 Salvar Pedido da Semana", type="primary"):
        # Atualiza a base principal com os dados digitados pela loja
        st.session_state['df_pedidos'][loja_selecionada] = df_editado[loja_selecionada]
        st.success(f"Pedido da {loja_selecionada} salvo com sucesso!")

# ---------------------------------------------------------
# VISÃO DO SUPERVISOR
# ---------------------------------------------------------
elif menu == "Área do Supervisor (Gerencial)":
    st.header("Consolidado Geral de Pedidos")
    
    # Exibe a tabela completa em formato largo (Wide) igual à aba gerencial da foto
    st.dataframe(st.session_state['df_pedidos'], hide_index=True, use_container_width=True, height=500)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exportação")
        # Gera o CSV para o supervisor poder abrir no Excel ou imprimir
        csv = st.session_state['df_pedidos'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Planilha Consolidada (CSV)",
            data=csv,
            file_name='pedidos_consolidados_orientais.csv',
            mime='text/csv',
        )
        
    with col2:
        st.subheader("Fechamento Semanal")
        st.warning("Atenção: Ao limpar os pedidos, as quantidades de todas as lojas voltarão a zero.")
        # Botão para zerar os pedidos para a próxima semana
        if st.button("🔄 Limpar Pedidos (Nova Semana)"):
            for loja in lojas:
                st.session_state['df_pedidos'][loja] = 0
            st.success("Tabela zerada! Pronta para a digitação da próxima semana.")
            st.rerun()
