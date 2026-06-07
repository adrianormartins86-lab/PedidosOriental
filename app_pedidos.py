import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Pedidos - Horti Oriental", page_icon="🍣", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA ---
st.markdown("""
<style>
    /* Estilização dos botões principais */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.2);
    }
    
    /* Suaviza as bordas dos containers */
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px;
        transition: box-shadow 0.3s ease;
    }
    div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Lista de lojas (01 a 08)
LOJAS = ["Loja 01", "Loja 02", "Loja 05", "Loja 06", "Loja 07", "Loja 08"]

# ---------------------------------------------------------
# SISTEMA DE LOGIN
# ---------------------------------------------------------
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

if st.session_state['usuario_logado'] is None:
    st.write("<br><br><br>", unsafe_allow_html=True) 
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.container(border=True):
            h_col1, h_col2 = st.columns([4, 1])
            with h_col1:
                st.markdown("""
                    <h2 style='margin-bottom: 0px; padding-bottom: 0px;'>Portal de Pedidos</h2>
                    <p style='color: #a0aec0; font-size: 15px; margin-top: 5px;'>Horti Oriental - Molicenter</p>
                """, unsafe_allow_html=True)
            with h_col2:
                st.write("") 
                st.image("passaro_logo.png", width=65)
                
            st.divider() 
            
            usuarios_permitidos = ["Selecione..."] + ["Administrador"] + LOJAS
            usuario_selecionado = st.selectbox("Usuário de acesso:", usuarios_permitidos)
            
            senha_digitada = st.text_input("Senha de acesso:", type="password")
            
            st.write("<br>", unsafe_allow_html=True)
            
            if st.button("Entrar no Sistema", type="primary", use_container_width=True):
                if usuario_selecionado == "Selecione...":
                    st.error("⚠️ Por favor, selecione um usuário.")
                elif usuario_selecionado == "Administrador" and senha_digitada == "moli0000":
                    st.session_state['usuario_logado'] = usuario_selecionado
                    st.rerun()
                elif usuario_selecionado in LOJAS and senha_digitada == "moli1234":
                    st.session_state['usuario_logado'] = usuario_selecionado
                    st.rerun()
                elif senha_digitada != "":
                    st.error("⚠️ Senha incorreta. Tente novamente.")
    st.stop() 

usuario_atual = st.session_state['usuario_logado']
acesso_total = usuario_atual == "Administrador"

# ---------------------------------------------------------
# INICIALIZAÇÃO DE DADOS E CACHE
# ---------------------------------------------------------
limpar_cache = False
if 'df_pedidos' in st.session_state:
    colunas_atuais = st.session_state['df_pedidos'].columns.tolist()
    if any(loja not in colunas_atuais for loja in LOJAS):
        limpar_cache = True

if 'df_produtos' in st.session_state:
    colunas_produtos = st.session_state['df_produtos'].columns.tolist()
    # Limpa o cache se as colunas de visibilidade das lojas não existirem no cadastro de produtos
    if 'Código Barra' not in colunas_produtos or len(st.session_state['df_produtos']) < 23 or any(loja not in colunas_produtos for loja in LOJAS):
        limpar_cache = True

if limpar_cache:
    if 'df_pedidos' in st.session_state: del st.session_state['df_pedidos']
    if 'df_produtos' in st.session_state: del st.session_state['df_produtos']

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
    df_prod_inicial = pd.DataFrame(produtos_iniciais)
    # Adiciona uma coluna de visibilidade (True/False) para cada loja, padrão True (visível)
    for loja in LOJAS:
        df_prod_inicial[loja] = True
        
    st.session_state['df_produtos'] = df_prod_inicial

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
# MENU LATERAL
# ---------------------------------------------------------
if acesso_total:
    with st.sidebar:
        st.image("passaro_logo.png", width=80) 
        st.markdown(f"### Olá, **{usuario_atual}**")
        st.caption("Sistema de Pedidos Integrado")
        st.divider()
        
        perfil_navegacao = st.radio("📍 Navegação:", [
            "Separação e Fechamento", 
            "Visão das Lojas", 
            "Catálogo de Produtos"
        ])
        
        st.divider()
        if st.button("🚪 Sair / Logout", use_container_width=True):
            st.session_state['usuario_logado'] = None
            st.rerun()
else:
    perfil_navegacao = "Visão das Lojas"

# ---------------------------------------------------------
# ROTA 1: SEPARAÇÃO E FECHAMENTO (ADMINISTRADOR)
# ---------------------------------------------------------
if perfil_navegacao == "Separação e Fechamento":
    st.title("📊 Separação e Fechamento")
    st.markdown("Consolidado Geral de Pedidos. Como administrador, você pode editar diretamente as quantidades de qualquer loja.")
    
    with st.container(border=True):
        # Filtra apenas as colunas base de produtos para não conflitar as colunas booleanas das lojas com as quantidades
        df_produtos_base = st.session_state['df_produtos'][["Código", "Descrição", "Código Barra", "Marca"]]
        df_final = pd.merge(df_produtos_base, st.session_state['df_pedidos'], on="Código")
        df_final["TOTAL GERAL"] = df_final[LOJAS].sum(axis=1)
        
        colunas_config_consolidado = {
            "Código": st.column_config.NumberColumn(width=80, format="%d", disabled=True),
            "Descrição": st.column_config.TextColumn(disabled=True),
            "Código Barra": st.column_config.TextColumn("Cód. Barras", width=120, disabled=True),
            "Marca": st.column_config.TextColumn(width=100, disabled=True),
            "TOTAL GERAL": st.column_config.NumberColumn("TOTAL GERAL", width=100, format="**%d**", disabled=True)
        }
        
        for loja in LOJAS:
            colunas_config_consolidado[loja] = st.column_config.NumberColumn(loja, format="%d", min_value=0, step=1)
        
        df_editado_admin = st.data_editor(
            df_final, 
            hide_index=True, 
            use_container_width=False, 
            height=600,
            column_config=colunas_config_consolidado
        )
        
        st.divider()
        col_salvar, col_vazia = st.columns([3, 7])
        with col_salvar:
            if st.button("💾 Salvar Alterações nas Lojas", type="primary", use_container_width=True):
                for loja in LOJAS:
                    st.session_state['df_pedidos'][loja] = df_editado_admin[loja]
                st.success("✅ Ajustes salvos com sucesso!")
                st.rerun()

        st.divider()
        
        col_exp, col_limpeza, col_vazia2 = st.columns([3, 3, 4])
        with col_exp:
            st.markdown("#### 📥 Exportar Tabela")
            csv = df_editado_admin.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Download em CSV",
                data=csv,
                file_name='separacao_semanal_horti.csv',
                mime='text/csv'
            )
            
        with col_limpeza:
            st.markdown("#### 🧹 Nova Semana")
            if st.button("🚨 Limpar Lojas (Zerar Pedidos)"):
                st.session_state['df_pedidos'][LOJAS] = 0
                st.success("✅ Tabela limpa! Sistema pronto para nova semana.")
                st.rerun()

# ---------------------------------------------------------
# ROTA 2: VISÃO DAS LOJAS
# ---------------------------------------------------------
elif perfil_navegacao == "Visão das Lojas":
    
    if acesso_total:
        loja_selecionada = st.selectbox("👁️ Visão como (Selecione a Loja):", LOJAS)
    else:
        loja_selecionada = usuario_atual
    
    col_titulo, col_logout = st.columns([8, 2])
    with col_titulo:
        st.title(f"📋 {loja_selecionada} : FLV - Oriental")
    with col_logout:
        st.write("<br>", unsafe_allow_html=True)
        if not acesso_total: 
            if st.button("🚪 Sair"):
                st.session_state['usuario_logado'] = None
                st.rerun()

    st.markdown("Preencha as quantidades necessárias para a sua loja.")
    
    # 1. Filtra o cadastro de produtos exibindo apenas aqueles onde a coluna da loja está como True (marcada)
    df_produtos_visiveis = st.session_state['df_produtos'][st.session_state['df_produtos'][loja_selecionada] == True]
    
    # 2. Faz o merge apenas com os produtos autorizados para esta loja
    df_loja = pd.merge(df_produtos_visiveis[["Código", "Descrição", "Código Barra", "Marca"]], st.session_state['df_pedidos'][["Código", loja_selecionada]], on="Código")
    
    with st.container(border=True):
        st.info("💡 Clique na coluna 'Qtde' para digitar.")
        
        df_editado = st.data_editor(
            df_loja,
            column_config={
                "Código": st.column_config.NumberColumn(width=80, disabled=True, format="%d"),
                "Descrição": st.column_config.TextColumn(disabled=True),
                "Código Barra": st.column_config.TextColumn("Cód. Barras", width=120, disabled=True),
                "Marca": st.column_config.TextColumn(width=100, disabled=True),
                loja_selecionada: st.column_config.NumberColumn("🛒 Qtde", width=95, min_value=0, step=1)
            },
            hide_index=True,
            use_container_width=False, 
            height=600 
        )
        
        itens_com_pedido = (df_editado[loja_selecionada] > 0).sum()
        total_itens = len(df_editado)
        
        st.divider()
        col_metric, col_btn, col_vazia = st.columns([2, 3, 5])
        
        with col_metric:
            st.metric("Itens Preenchidos", f"{itens_com_pedido} / {total_itens}")
            
        with col_btn:
            st.write("<br>", unsafe_allow_html=True) 
            if st.button("💾 Salvar Pedido da Semana", type="primary"):
                for idx, row in df_editado.iterrows():
                    cod = row["Código"]
                    qtd = row[loja_selecionada]
                    st.session_state['df_pedidos'].loc[st.session_state['df_pedidos']["Código"] == cod, loja_selecionada] = qtd
                st.success(f"✅ Pedido da {loja_selecionada} salvo com sucesso no banco de dados!")

# ---------------------------------------------------------
# ROTA 3: CATÁLOGO DE PRODUTOS (ADMINISTRADOR)
# ---------------------------------------------------------
elif perfil_navegacao == "Catálogo de Produtos":
    st.title("🏷️ Catálogo de Produtos")
    st.markdown("Gerencie os produtos disponíveis e marque quais lojas podem visualizar cada item.")
    
    with st.container(border=True):
        st.caption("Adicione novos produtos na última linha (com o '+') ou delete selecionando a linha e apertando 'Delete'.")
        
        # Configuração dinâmica das colunas do catálogo (adiciona as checkboxes das lojas)
        config_catalogo = {
            "Código": st.column_config.NumberColumn("Código Interno", width=80, required=True, min_value=1, format="%d"),
            "Descrição": st.column_config.TextColumn("Descrição do Item", width=300, required=True),
            "Código Barra": st.column_config.TextColumn("Cód. Barras", width=120, required=True),
            "Marca": st.column_config.TextColumn("Fabricante/Marca", width=100, required=True)
        }
        
        for loja in LOJAS:
            config_catalogo[loja] = st.column_config.CheckboxColumn(f"Exibir: {loja}", default=True)
        
        df_produtos_editado = st.data_editor(
            st.session_state['df_produtos'],
            num_rows="dynamic",
            column_config=config_catalogo,
            hide_index=True,
            use_container_width=False,
            height=600
        )
        
        st.write("<br>", unsafe_allow_html=True)
        col_salvar, col_vazia = st.columns([3, 7])
        with col_salvar:
            if st.button("🔄 Atualizar Catálogo e Permissões", type="primary", use_container_width=True):
                st.session_state['df_produtos'] = df_produtos_editado
                sincronizar_tabelas()
                st.success("✅ Catálogo e permissões atualizados em tempo real para todas as lojas!")
                st.rerun()
