import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Pedidos - Horti Japonês", page_icon="🍣", layout="wide", initial_sidebar_state="expanded")

# --- ESTILIZAÇÃO CSS CUSTOMIZADA (MODERNA) ---
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
    
    /* Estilização da tela de Login */
    .login-header {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .login-subheader {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Lista de lojas (01 a 08)
LOJAS = ["Loja 01", "Loja 02", "Loja 03", "Loja 04", "Loja 05", "Loja 06", "Loja 07", "Loja 08"]

# ---------------------------------------------------------
# SISTEMA DE LOGIN (VISUAL ATUALIZADO)
# ---------------------------------------------------------
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

if st.session_state['usuario_logado'] is None:
    st.write("<br><br><br>", unsafe_allow_html=True) # Espaçamento
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.container(border=True):
            st.markdown('<div class="login-header">🍣 Portal de Pedidos</div>', unsafe_allow_html=True)
            st.markdown('<div class="login-subheader">Horti Japonês • Molicenter</div>', unsafe_allow_html=True)
            
            usuarios_permitidos = ["Selecione..."] + ["Analista", "Supervisor"] + LOJAS
            usuario_selecionado = st.selectbox("Selecione seu perfil de acesso:", usuarios_permitidos)
            
            st.write("<br>", unsafe_allow_html=True)
            if st.button("🚀 Acessar Sistema", type="primary", use_container_width=True):
                if usuario_selecionado != "Selecione...":
                    st.session_state['usuario_logado'] = usuario_selecionado
                    st.rerun() 
                else:
                    st.error("⚠️ Por favor, selecione um usuário válido na lista.")
    st.stop() 

usuario_atual = st.session_state['usuario_logado']

# ---------------------------------------------------------
# INICIALIZAÇÃO DE DADOS E CACHE (Mantido igual)
# ---------------------------------------------------------
limpar_cache = False
if 'df_pedidos' in st.session_state:
    colunas_atuais = st.session_state['df_pedidos'].columns.tolist()
    if any(loja not in colunas_atuais for loja in LOJAS):
        limpar_cache = True

if 'df_produtos' in st.session_state:
    if 'Código Barra' not in st.session_state['df_produtos'].columns or len(st.session_state['df_produtos']) < 23:
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
# MENU LATERAL (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3143/3143644.png", width=60) # Ícone decorativo
    st.markdown(f"### Olá, **{usuario_atual}**")
    st.caption("Sistema de Pedidos Integrado")
    st.divider()
    
    acesso_total = usuario_atual in ["Analista", "Supervisor"]

    if acesso_total:
        perfil_navegacao = st.radio("📍 Navegação:", ["Painel Administrativo", "Visão das Lojas"])
    else:
        perfil_navegacao = "Visão das Lojas"
    
    st.divider()
    if st.button("🚪 Sair / Logout", use_container_width=True):
        st.session_state['usuario_logado'] = None
        st.rerun()

# ---------------------------------------------------------
# VISÃO DA LOJA (DIGITAÇÃO)
# ---------------------------------------------------------
if perfil_navegacao == "Visão das Lojas":
    st.title("📋 Lançamento Semanal")
    st.markdown("Preencha as quantidades necessárias para a sua loja.")
    
    if acesso_total:
        loja_selecionada = st.selectbox("👁️ Visão como (Selecione a Loja):", LOJAS)
    else:
        loja_selecionada = usuario_atual
    
    df_loja = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'][["Código", loja_selecionada]], on="Código")
    
    # Card de Informação
    with st.container(border=True):
        st.info(f"💡 Editando catálogo para: **{loja_selecionada}**")
        
        # O Data Editor com altura ampliada
        df_editado = st.data_editor(
            df_loja,
            column_config={
                "Código": st.column_config.NumberColumn(disabled=True),
                "Descrição": st.column_config.TextColumn(disabled=True),
                "Código Barra": st.column_config.TextColumn("Cód. Barras", disabled=True),
                "Marca": st.column_config.TextColumn(disabled=True),
                loja_selecionada: st.column_config.NumberColumn("🛒 Qtd Pedido", min_value=0, step=1)
            },
            hide_index=True,
            use_container_width=True,
            height=600 
        )
        
        # Cálculo de métricas para a loja
        itens_com_pedido = (df_editado[loja_selecionada] > 0).sum()
        total_itens = len(df_editado)
        
        st.divider()
        col_metric, col_btn = st.columns([1, 1])
        
        with col_metric:
            st.metric("Itens Preenchidos", f"{itens_com_pedido} / {total_itens}")
            
        with col_btn:
            st.write("<br>", unsafe_allow_html=True) # Alinha o botão com a métrica
            if st.button("💾 Salvar Pedido da Semana", type="primary", use_container_width=True):
                for idx, row in df_editado.iterrows():
                    cod = row["Código"]
                    qtd = row[loja_selecionada]
                    st.session_state['df_pedidos'].loc[st.session_state['df_pedidos']["Código"] == cod, loja_selecionada] = qtd
                st.success(f"✅ Pedido da {loja_selecionada} salvo com sucesso no banco de dados!")

# ---------------------------------------------------------
# VISÃO DO SUPERVISOR / ANALISTA
# ---------------------------------------------------------
elif perfil_navegacao == "Painel Administrativo":
    st.title("⚙️ Painel de Controle Integrado")
    
    aba_cadastro, aba_consolidado = st.tabs(["🏷️ Catálogo de Produtos", "📊 Separação e Fechamento"])
    
    with aba_cadastro:
        with st.container(border=True):
            st.subheader("Gerenciar Produtos")
            st.caption("Adicione novos produtos na última linha (com o '+') ou delete selecionando a linha e apertando 'Delete'.")
            
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
                height=500
            )
            
            if st.button("🔄 Atualizar Catálogo para as Lojas", type="primary"):
                st.session_state['df_produtos'] = df_produtos_editado
                sincronizar_tabelas()
                st.success("✅ Novo catálogo sincronizado e disponível para todas as lojas em tempo real!")
                st.rerun()

    with aba_consolidado:
        with st.container(border=True):
            st.subheader("Consolidado Geral")
            
            df_final = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'], on="Código")
            df_final["TOTAL GERAL"] = df_final[LOJAS].sum(axis=1)
            
            # Formatação visual da coluna total
            st.dataframe(
                df_final, 
                hide_index=True, 
                use_container_width=True, 
                height=450,
                column_config={
                    "TOTAL GERAL": st.column_config.NumberColumn("TOTAL GERAL", format="**%d**")
                }
            )
            
            st.divider()
            
            col_exp, col_limpeza = st.columns(2)
            with col_exp:
                st.markdown("#### 📥 Exportar Tabela")
                st.caption("Baixe o resultado para imprimir ou levar ao Excel.")
                csv = df_final.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download em CSV",
                    data=csv,
                    file_name='separacao_semanal_horti.csv',
                    mime='text/csv',
                    use_container_width=True
                )
                
            with col_limpeza:
                st.markdown("#### 🧹 Fechamento Semanal")
                st.caption("Zera a digitação das lojas para iniciar o novo ciclo.")
                if st.button("🚨 Limpar Lojas (Zerar Pedidos)", use_container_width=True):
                    st.session_state['df_pedidos'][LOJAS] = 0
                    st.success("✅ Tabela limpa! Sistema pronto para nova semana.")
                    st.rerun()
