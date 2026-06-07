import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Pedidos - Horti Japonês", layout="wide")

# Lista de lojas (01 a 08)
LOJAS = ["Loja 01", "Loja 02", "Loja 03", "Loja 04", "Loja 05", "Loja 06", "Loja 07", "Loja 08"]

# ---------------------------------------------------------
# SISTEMA DE LOGIN
# ---------------------------------------------------------
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

# Se não estiver logado, exibe apenas a tela de login e para a execução
if st.session_state['usuario_logado'] is None:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Acesso ao Sistema")
        st.markdown("Selecione seu perfil para acessar os pedidos semanais.")
        
        usuarios_permitidos = ["Selecione..."] + ["Analista", "Supervisor"] + LOJAS
        
        usuario_selecionado = st.selectbox("Usuário:", usuarios_permitidos)
        
        if st.button("Entrar", type="primary", use_container_width=True):
            if usuario_selecionado != "Selecione...":
                st.session_state['usuario_logado'] = usuario_selecionado
                st.rerun() 
            else:
                st.error("Por favor, selecione um usuário válido na lista.")
    st.stop() 

# Recupera quem está logado no momento
usuario_atual = st.session_state['usuario_logado']

# ---------------------------------------------------------
# INICIALIZAÇÃO DE DADOS E CACHE
# ---------------------------------------------------------
# Limpeza de cache inteligente (força a atualização para os 23 itens e código de barras)
limpar_cache = False
if 'df_pedidos' in st.session_state:
    colunas_atuais = st.session_state['df_pedidos'].columns.tolist()
    faltando_loja = [loja for loja in LOJAS if loja not in colunas_atuais]
    if faltando_loja:
        limpar_cache = True

if 'df_produtos' in st.session_state:
    if 'Código Barra' not in st.session_state['df_produtos'].columns or len(st.session_state['df_produtos']) < 23:
        limpar_cache = True

if limpar_cache:
    if 'df_pedidos' in st.session_state:
        del st.session_state['df_pedidos']
    if 'df_produtos' in st.session_state:
        del st.session_state['df_produtos']

# Carga dos 23 itens extraídos da planilha
if 'df_produtos' not in st.session_state:
    produtos_iniciais = [
        {"Código": 521798, "Descrição": "Ampan Azuki C/6 Satsumaya", "Código Barra": "7897327901294", "Marca": "Satsumaya"},
        {"Código": 520504, "Descrição": "Kamaboko 200g Agronippo", "Código Barra": "7896293804165", "Marca": "Agronippo"},
        {"Código": 521150, "Descrição": "Kamaboko 200g Kai-Ho Agronippo", "Código Barra": "7896293804110", "Marca": "Agronippo"},
        {"Código": 521974, "Descrição": "Lokyozuke Cebolinha 200g Marunaka Cons", "Código Barra": "7897231100134", "Marca": "Agronippo"},
        {"Código": 533623, "Descrição": "Massa Gobomaki Kai-Ho 200g", "Código Barra": "7896293804134", "Marca": "Agronippo"},
        {"Código": 53662, "Descrição": "Massa Konnyaku 350g C/Alga", "Código Barra": "7896293805100", "Marca": "Agronippo"},
        {"Código": 524768, "Descrição": "Massa Shirataki 200g Agronippo Noodles Konjac", "Código Barra": "7898944092266", "Marca": "Agronippo"},
        {"Código": 583497, "Descrição": "Massa Shirataki 200g Hyde Alimentos Noodles", "Código Barra": "7898944092211", "Marca": "Hyde Alimentos"},
        {"Código": 577362, "Descrição": "Mirinzuke 200g Conserva De Nabo", "Código Barra": "7896101500265", "Marca": "Agronippo"},
        {"Código": 520911, "Descrição": "Narutomakii Kai.Ho 200g", "Código Barra": "7896293804158", "Marca": "Agronippo"},
        {"Código": 141820, "Descrição": "Nippo Kyoka Natto 100g", "Código Barra": "7896293805001", "Marca": "Agronippo"},
        {"Código": 524713, "Descrição": "Nippo Shirataki 200g", "Código Barra": "7896293805117", "Marca": "Agronippo"},
        {"Código": 139940, "Descrição": "Shogazuke 245g Beni Shoga Gengibre Ralado", "Código Barra": "7897231100042", "Marca": "Agronippo"},
        {"Código": 55406, "Descrição": "Sushi Ague 110g Agronippo", "Código Barra": "7896293803014", "Marca": "Agronippo"},
        {"Código": 608981, "Descrição": "Takuan 200g Haruko Amarelo", "Código Barra": "0798190064482", "Marca": "Haruko"},
        {"Código": 521965, "Descrição": "Takuan 500g Haruko Amarelo", "Código Barra": "0798190022024", "Marca": "Haruko"},
        {"Código": 100221, "Descrição": "Takuwan 200g Takaki Pequeno", "Código Barra": "7896101500272", "Marca": "Ceasa Box"},
        {"Código": 176507, "Descrição": "Takuwan 500g Takaki Grande", "Código Barra": "7896101500234", "Marca": "Ceasa Box"},
        {"Código": 530112, "Descrição": "Tempura 200g Kai Ho", "Código Barra": "7896293804127", "Marca": "Agronippo"},
        {"Código": 53679, "Descrição": "Tikuwa 200g Agronippo", "Código Barra": "7896293804103", "Marca": "Agronippo"},
        {"Código": 577380, "Descrição": "Tiocenzuke 245 conserva Pic Nabo Acelga", "Código Barra": "7897231100219", "Marca": "Agronippo"},
        {"Código": 524722, "Descrição": "Tofu 1kg Agronippo Nigari Momen", "Código Barra": "7896293808156", "Marca": "Agronippo"},
        {"Código": 524731, "Descrição": "Tofu 500g Agronippo Tradicional", "Código Barra": "7896293802048", "Marca": "Agronippo"}
    ]
    st.session_state['df_produtos'] = pd.DataFrame(produtos_iniciais)

if 'df_pedidos' not in st.session_state:
    df_p = pd.DataFrame(columns=["Código"] + LOJAS)
    df_p["Código"] = st.session_state['df_produtos']["Código"]
    df_p[LOJAS] = 0  
    st.session_state['df_pedidos'] = df_p

def sincronizar_tabelas():
    df_prod = st.session_state['df_produtos']
    df_ped = st.session_state['df_pedidos']
    
    df_ped = df_ped[df_ped["Código"].isin(df_prod["Código"])]
    novos_codigos = df_prod[~df_prod["Código"].isin(df_ped["Código"])]["Código"]
    
    if not novos_codigos.empty:
        df_novos = pd.DataFrame(columns=["Código"] + LOJAS)
        df_novos["Código"] = novos_codigos
        df_novos[LOJAS] = 0  
        df_ped = pd.concat([df_ped, df_novos], ignore_index=True)
        
    st.session_state['df_pedidos'] = df_ped

sincronizar_tabelas()

# ---------------------------------------------------------
# INTERFACE DO USUÁRIO E ROTEAMENTO
# ---------------------------------------------------------
st.sidebar.markdown(f"👤 **Logado como:** `{usuario_atual}`")
if st.sidebar.button("Sair / Logout"):
    st.session_state['usuario_logado'] = None
    st.rerun()

st.sidebar.divider()

acesso_total = usuario_atual in ["Analista", "Supervisor"]

if acesso_total:
    perfil_navegacao = st.sidebar.radio("Menu de Navegação:", ["Painel Administrativo", "Visão das Lojas (Digitação)"])
else:
    perfil_navegacao = "Visão das Lojas (Digitação)"

st.title("🍣 Sistema Central de Pedidos - Horti Japonês")

# ---------------------------------------------------------
# VISÃO DA LOJA (DIGITAÇÃO)
# ---------------------------------------------------------
if perfil_navegacao == "Visão das Lojas (Digitação)":
    st.header("📋 Lançamento Semanal de Pedidos")
    
    if acesso_total:
        loja_selecionada = st.selectbox("Selecione qual Loja deseja visualizar/editar:", LOJAS)
    else:
        loja_selecionada = usuario_atual
    
    df_loja = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'][["Código", loja_selecionada]], on="Código")
    
    st.info(f"O catálogo abaixo reflete as atualizações mais recentes. Insira os pedidos da **{loja_selecionada}**:")
    
    df_editado = st.data_editor(
        df_loja,
        column_config={
            "Código": st.column_config.NumberColumn(disabled=True),
            "Descrição": st.column_config.TextColumn(disabled=True),
            "Código Barra": st.column_config.TextColumn("Cód. Barras", disabled=True),
            "Marca": st.column_config.TextColumn(disabled=True),
            loja_selecionada: st.column_config.NumberColumn("Qtd Pedido", min_value=0, step=1)
        },
        hide_index=True,
        use_container_width=True,
        height=600 # Aumentado para visualizar melhor os 23 itens
    )
    
    if st.button("💾 Enviar/Atualizar Pedido", type="primary"):
        for idx, row in df_editado.iterrows():
            cod = row["Código"]
            qtd = row[loja_selecionada]
            st.session_state['df_pedidos'].loc[st.session_state['df_pedidos']["Código"] == cod, loja_selecionada] = qtd
        st.success(f"Sucesso! Os dados da {loja_selecionada} foram gravados.")

# ---------------------------------------------------------
# VISÃO DO SUPERVISOR / ANALISTA
# ---------------------------------------------------------
elif perfil_navegacao == "Painel Administrativo":
    st.header("⚙️ Painel de Controle Integrado")
    
    aba_cadastro, aba_consolidado = st.tabs(["✏️ Cadastrar/Editar Produtos", "📊 Visualizar e Fechar Pedidos"])
    
    with aba_cadastro:
        st.subheader("Gerenciamento do Catálogo Geral")
        st.caption("Adicione novos produtos na última linha ou delete selecionando a linha e apertando 'Delete'.")
        
        df_produtos_editado = st.data_editor(
            st.session_state['df_produtos'],
            num_rows="dynamic",
            column_config={
                "Código": st.column_config.NumberColumn("Código Interno", required=True, min_value=1),
                "Descrição": st.column_config.TextColumn("Descrição do Item", required=True),
                "Código Barra": st.column_config.TextColumn("Cód. Barras", required=True),
                "Marca": st.column_config.TextColumn("Fabricante/Marca", required=True)
            },
            hide_index=True,
            use_container_width=True,
            height=600
        )
        
        if st.button("🔄 Salvar e Disponibilizar Novo Catálogo", type="primary"):
            st.session_state['df_produtos'] = df_produtos_editado
            sincronizar_tabelas()
            st.success("Catálogo atualizado! Todas as visões das lojas foram modificadas.")
            st.rerun()

    with aba_consolidado:
        st.subheader("Painel Geral de Separação")
        
        df_final = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'], on="Código")
        df_final["Total Consolidado"] = df_final[LOJAS].sum(axis=1)
        
        st.dataframe(df_final, hide_index=True, use_container_width=True, height=600)
        
        st.divider()
        col_exp, col_limpeza = st.columns(2)
        
        with col_exp:
            st.markdown("### 📥 Exportação")
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Pedidos (CSV)",
                data=csv,
                file_name='separacao_semanal_horti.csv',
                mime='text/csv'
            )
            
        with col_limpeza:
            st.markdown("### 🧹 Nova Semana")
            st.warning("Zera as quantidades digitadas, mas mantém o cadastro.")
            
            if st.button("🚨 Limpar Pedidos das Lojas"):
                st.session_state['df_pedidos'][LOJAS] = 0
                st.success("Tabela limpa! Pronta para a próxima semana.")
                st.rerun()
