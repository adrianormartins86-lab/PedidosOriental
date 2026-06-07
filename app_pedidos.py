import streamlit as st
import pandas as pd


# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Gestão de Pedidos - Horti Oriental",
    page_icon="🍣",
    layout="wide",
    initial_sidebar_state="expanded"  # será sobrescrito via CSS para lojas
)

# ─────────────────────────────────────────────
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;500;700&display=swap');

/* ── Variáveis de cor ── */
:root {
    --bg-main:        #0d1117;
    --bg-card:        #161b22;
    --bg-sidebar:     #0d1117;
    --green-dark:     #1a3a2a;
    --green-mid:      #1f4d35;
    --green-accent:   #2ea043;
    --green-bright:   #3fb950;
    --green-glow:     rgba(46,160,67,.25);
    --text-primary:   #e6edf3;
    --text-muted:     #7d8590;
    --text-header:    #cae8cb;
    --border:         #21262d;
    --border-active:  #2ea043;
    --row-hover:      rgba(46,160,67,.08);
    --row-selected:   rgba(46,160,67,.18);
    --danger:         #da3633;
    --warning:        #d29922;
}

/* ── Reset global ── */
.stApp, .main { background-color: var(--bg-main) !important; color: var(--text-primary) !important; }
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif !important; }
section[data-testid="stSidebar"] { background-color: var(--bg-sidebar) !important; border-right: 1px solid var(--border); }

/* ── Sidebar texto ── */
section[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
section[data-testid="stSidebar"] .stRadio label { font-size: 14px; }

/* ── Botões primários ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--green-mid) 0%, var(--green-accent) 100%) !important;
    color: #fff !important;
    border: 1px solid var(--green-accent) !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: .3px;
    transition: all .2s ease !important;
    box-shadow: 0 0 0 0 var(--green-glow);
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 18px var(--green-glow) !important;
    border-color: var(--green-bright) !important;
}

/* ── Botões secundários ── */
.stButton > button {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    transition: all .2s ease !important;
}
.stButton > button:hover {
    border-color: var(--green-accent) !important;
    color: var(--green-bright) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs / Selects ── */
.stTextInput input, .stSelectbox > div > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stTextInput input:focus, .stSelectbox > div > div:focus-within {
    border-color: var(--green-accent) !important;
    box-shadow: 0 0 0 3px var(--green-glow) !important;
}

/* ── Data Editor: cabeçalho verde escuro ── */
[data-testid="stDataEditor"] [data-testid="glideDataEditor"] .gdg-header-cell,
[data-testid="stDataEditor"] .dvn-stack .gdg-header,
iframe[title*="dataframe"] {
    background-color: var(--green-dark) !important;
    color: var(--text-header) !important;
}

/* Wrapper da tabela: borda verde sutil */
[data-testid="stDataEditor"] {
    border-radius: 10px !important;
    overflow: hidden;
    border: 1px solid var(--green-mid) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,.4);
}

/* ── Célula selecionada: destaque verde vibrante ── */
[data-testid="stDataEditor"] .gdg-cell.gdg-selected,
[data-testid="stDataEditor"] .gdg-cell[data-state="focused"],
[data-testid="stDataEditor"] .gdg-cell[aria-selected="true"] {
    background-color: var(--row-selected) !important;
    outline: 2px solid var(--green-accent) !important;
    outline-offset: -2px;
}

/* Linha hover */
[data-testid="stDataEditor"] .gdg-row:hover .gdg-cell {
    background-color: var(--row-hover) !important;
}

/* ── Containers / Cards ── */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    transition: box-shadow .25s ease, border-color .25s ease;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--green-mid) !important;
    box-shadow: 0 6px 24px rgba(0,0,0,.35) !important;
}

/* ── Métricas ── */
[data-testid="stMetric"] {
    background-color: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] { color: var(--green-bright) !important; font-weight: 700; }
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }

/* ── Info box ── */
.stAlert[data-baseweb="notification"] {
    background-color: rgba(46,160,67,.1) !important;
    border: 1px solid var(--green-mid) !important;
    border-radius: 8px !important;
    color: var(--text-header) !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Títulos ── */
h1 { color: var(--text-primary) !important; font-weight: 700 !important; letter-spacing: -.5px; }
h2, h3 { color: var(--text-primary) !important; }

/* ── Badge de loja (sidebar) ── */
.loja-badge {
    display: inline-block;
    background: var(--green-dark);
    border: 1px solid var(--green-mid);
    color: var(--green-bright);
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 6px;
    font-family: 'IBM Plex Mono', monospace;
}

/* ── Page header band ── */
.page-header {
    background: linear-gradient(90deg, var(--green-dark) 0%, #0d2018 100%);
    border: 1px solid var(--green-mid);
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.page-header-icon { font-size: 26px; }
.page-header-title {
    font-size: 20px;
    font-weight: 700;
    color: var(--text-header);
    font-family: 'IBM Plex Sans', sans-serif;
}
.page-header-sub {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 2px;
}

/* ── Seção de ação (download, limpar) ── */
.action-section {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 16px;
}
.action-section h4 {
    color: var(--text-muted) !important;
    font-size: 11px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 10px !important;
}

/* ── Login box ── */
.login-hint {
    font-size: 11px;
    color: var(--text-muted);
    text-align: center;
    margin-top: 10px;
}

/* ── Ocultar sidebar para lojas ── */
.sidebar-hidden section[data-testid="stSidebar"],
.sidebar-hidden [data-testid="collapsedControl"] {
    display: none !important;
}
.sidebar-hidden .main .block-container {
    max-width: 100% !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* ── Barra de topo para lojas ── */
.topbar-loja {
    background: linear-gradient(90deg, var(--green-dark) 0%, #0d2018 100%);
    border: 1px solid var(--green-mid);
    border-radius: 10px;
    padding: 10px 18px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.topbar-left {
    display: flex;
    align-items: center;
    gap: 12px;
}
.topbar-badge {
    background: var(--green-mid);
    border: 1px solid var(--green-accent);
    color: var(--green-bright);
    font-size: 13px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
}
.topbar-title {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-header);
}
.topbar-sub {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────
LOJAS = ["Loja 01", "Loja 02", "Loja 05", "Loja 06", "Loja 07", "Loja 08"]

# ─────────────────────────────────────────────
# SISTEMA DE LOGIN
# ─────────────────────────────────────────────
if 'usuario_logado' not in st.session_state:
    st.session_state['usuario_logado'] = None

if st.session_state['usuario_logado'] is None:
    st.write("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1.4, 1])

    with col2:
        with st.container(border=True):
            # Header do login
            h1, h2 = st.columns([4, 1])
            with h1:
                st.markdown("""
                    <h2 style='margin-bottom:0'>Portal de Pedidos</h2>
                    <p style='color:#7d8590;font-size:14px;margin-top:4px'>Horti Oriental — Molicenter</p>
                """, unsafe_allow_html=True)
            with h2:
                st.write("")
                try:
                    st.image("passaro_logo.png", width=60)
                except Exception:
                    st.markdown("🐦", unsafe_allow_html=True)

            st.divider()

            usuarios_permitidos = ["Selecione..."] + ["Administrador"] + LOJAS
            usuario_selecionado = st.selectbox("👤 Usuário de acesso:", usuarios_permitidos)
            senha_digitada = st.text_input("🔑 Senha de acesso:", type="password")

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
                elif senha_digitada:
                    st.error("⚠️ Senha incorreta. Tente novamente.")

            st.markdown('<p class="login-hint">🔒 Acesso restrito — Molicenter © 2026</p>', unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────
# ESTADO E DADOS
# ─────────────────────────────────────────────
usuario_atual = st.session_state['usuario_logado']
acesso_total  = usuario_atual == "Administrador"

# Oculta sidebar completamente para usuários de loja
if not acesso_total:
    st.markdown("""
    <script>
        document.body.classList.add('sidebar-hidden');
        const root = window.parent.document.querySelector('.stApp');
        if (root) root.classList.add('sidebar-hidden');
    </script>
    <style>
        section[data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"]  { display: none !important; }
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2.5rem !important;
            padding-right: 2.5rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Limpeza de cache se estrutura mudou
limpar_cache = False
if 'df_pedidos' in st.session_state:
    if any(l not in st.session_state['df_pedidos'].columns for l in LOJAS):
        limpar_cache = True
if 'df_produtos' in st.session_state:
    cols = st.session_state['df_produtos'].columns.tolist()
    if ('Código Barra' not in cols
            or len(st.session_state['df_produtos']) < 23
            or any(l not in cols for l in LOJAS)):
        limpar_cache = True

if limpar_cache:
    for k in ('df_pedidos', 'df_produtos'):
        st.session_state.pop(k, None)

if 'df_produtos' not in st.session_state:
    produtos_iniciais = [
        {"Código": 521798, "Descrição": "Ampan Azuki C/6 Satsumaya",                   "Código Barra": "7897327901294", "Marca": "Satsumaya"},
        {"Código": 520504, "Descrição": "Kamaboko 200g Agronippo",                      "Código Barra": "7896293804165", "Marca": "Agronippo"},
        {"Código": 521150, "Descrição": "Kamaboko 200g Kai-Ho Agronippo",               "Código Barra": "7896293804110", "Marca": "Agronippo"},
        {"Código": 521974, "Descrição": "Lokyozuke Cebolinha 200g Marunaka Cons",       "Código Barra": "7897231100134", "Marca": "Agronippo"},
        {"Código": 533623, "Descrição": "Massa Gobomaki Kai-Ho 200g",                   "Código Barra": "7896293804134", "Marca": "Agronippo"},
        {"Código": 53662,  "Descrição": "Massa Konnyaku 350g C/Alga",                   "Código Barra": "7896293805100", "Marca": "Agronippo"},
        {"Código": 524768, "Descrição": "Massa Shirataki 200g Agronippo Noodles Konjac","Código Barra": "7898944092266", "Marca": "Agronippo"},
        {"Código": 583497, "Descrição": "Massa Shirataki 200g Hyde Alimentos Noodles",  "Código Barra": "7898944092211", "Marca": "Hyde Alimentos"},
        {"Código": 577362, "Descrição": "Mirinzuke 200g Conserva De Nabo",              "Código Barra": "7896101500265", "Marca": "Agronippo"},
        {"Código": 520911, "Descrição": "Narutomakii Kai.Ho 200g",                      "Código Barra": "7896293804158", "Marca": "Agronippo"},
        {"Código": 141820, "Descrição": "Nippo Kyoka Natto 100g",                       "Código Barra": "7896293805001", "Marca": "Agronippo"},
        {"Código": 524713, "Descrição": "Nippo Shirataki 200g",                         "Código Barra": "7896293805117", "Marca": "Agronippo"},
        {"Código": 139940, "Descrição": "Shogazuke 245g Beni Shoga Gengibre Ralado",    "Código Barra": "7897231100042", "Marca": "Agronippo"},
        {"Código": 55406,  "Descrição": "Sushi Ague 110g Agronippo",                    "Código Barra": "7896293803014", "Marca": "Agronippo"},
        {"Código": 608981, "Descrição": "Takuan 200g Haruko Amarelo",                   "Código Barra": "0798190064482", "Marca": "Haruko"},
        {"Código": 521965, "Descrição": "Takuan 500g Haruko Amarelo",                   "Código Barra": "0798190022024", "Marca": "Haruko"},
        {"Código": 100221, "Descrição": "Takuwan 200g Takaki Pequeno",                  "Código Barra": "7896101500272", "Marca": "Ceasa Box"},
        {"Código": 176507, "Descrição": "Takuwan 500g Takaki Grande",                   "Código Barra": "7896101500234", "Marca": "Ceasa Box"},
        {"Código": 530112, "Descrição": "Tempura 200g Kai Ho",                          "Código Barra": "7896293804127", "Marca": "Agronippo"},
        {"Código": 53679,  "Descrição": "Tikuwa 200g Agronippo",                        "Código Barra": "7896293804103", "Marca": "Agronippo"},
        {"Código": 577380, "Descrição": "Tiocenzuke 245 conserva Pic Nabo Acelga",      "Código Barra": "7897231100219", "Marca": "Agronippo"},
        {"Código": 524722, "Descrição": "Tofu 1kg Agronippo Nigari Momen",              "Código Barra": "7896293808156", "Marca": "Agronippo"},
        {"Código": 524731, "Descrição": "Tofu 500g Agronippo Tradicional",              "Código Barra": "7896293802048", "Marca": "Agronippo"},
    ]
    df_init = pd.DataFrame(produtos_iniciais)
    for loja in LOJAS:
        df_init[loja] = True
    st.session_state['df_produtos'] = df_init

if 'df_pedidos' not in st.session_state:
    df_p = pd.DataFrame(columns=["Código"] + LOJAS)
    df_p["Código"] = st.session_state['df_produtos']["Código"]
    df_p[LOJAS] = 0
    st.session_state['df_pedidos'] = df_p

def sincronizar_tabelas():
    df_prod = st.session_state['df_produtos']
    df_ped  = st.session_state['df_pedidos']
    df_ped  = df_ped[df_ped["Código"].isin(df_prod["Código"])]
    novos   = df_prod[~df_prod["Código"].isin(df_ped["Código"])]["Código"]
    if not novos.empty:
        df_n = pd.DataFrame({"Código": novos})
        df_n[LOJAS] = 0
        df_ped = pd.concat([df_ped, df_n], ignore_index=True)
    st.session_state['df_pedidos'] = df_ped

sincronizar_tabelas()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    try:
        st.image("passaro_logo.png", width=72)
    except Exception:
        st.markdown("🐦")

    st.markdown(f"### Olá, **{usuario_atual}**")
    st.markdown(f'<span class="loja-badge">{"🔑 Admin" if acesso_total else usuario_atual}</span>', unsafe_allow_html=True)
    st.caption("Sistema de Pedidos Integrado")
    st.divider()

    if acesso_total:
        perfil_navegacao = st.radio("📍 Navegação:", [
            "Separação e Fechamento",
            "Visão das Lojas",
            "Catálogo de Produtos"
        ])
    else:
        perfil_navegacao = "Visão das Lojas"

    st.divider()

    # Contador rápido de pedidos com itens
    total_preenchidos = (st.session_state['df_pedidos'][LOJAS] > 0).any(axis=1).sum()
    st.metric("Itens c/ pedido", total_preenchidos, help="Itens que têm ao menos 1 quantidade preenchida")

    st.divider()
    if st.button("🚪 Sair / Logout", use_container_width=True):
        st.session_state['usuario_logado'] = None
        st.rerun()

# ─────────────────────────────────────────────
# HELPER: cabeçalho de página
# ─────────────────────────────────────────────
def page_header(icon: str, title: str, subtitle: str = ""):
    sub_html = f'<div class="page-header-sub">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="page-header">
        <span class="page-header-icon">{icon}</span>
        <div>
            <div class="page-header-title">{title}</div>
            {sub_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ROTA 1: SEPARAÇÃO E FECHAMENTO
# ─────────────────────────────────────────────
if perfil_navegacao == "Separação e Fechamento":

    page_header("📊", "Separação e Fechamento",
                "Consolidado geral — edite quantidades diretamente na tabela")

    with st.container(border=True):
        df_base  = st.session_state['df_produtos'][["Código","Descrição","Código Barra","Marca"]]
        df_final = pd.merge(df_base, st.session_state['df_pedidos'], on="Código")
        df_final["TOTAL GERAL"] = df_final[LOJAS].sum(axis=1)

        col_cfg = {
            "Código":       st.column_config.NumberColumn(width=80,  format="%d",   disabled=True),
            "Descrição":    st.column_config.TextColumn(             disabled=True),
            "Código Barra": st.column_config.TextColumn("Cód. Barras", width=130,   disabled=True),
            "Marca":        st.column_config.TextColumn(width=110,   disabled=True),
            "TOTAL GERAL":  st.column_config.NumberColumn("TOTAL ▶", width=90,  format="%d", disabled=True),
        }
        for loja in LOJAS:
            col_cfg[loja] = st.column_config.NumberColumn(loja, format="%d", min_value=0, step=1)

        df_editado_admin = st.data_editor(
            df_final, hide_index=True, use_container_width=True,
            height=580, column_config=col_cfg
        )

        st.divider()

        col_salvar, col_exp, col_limpa, _ = st.columns([2, 2, 2, 4])

        with col_salvar:
            if st.button("💾 Salvar Alterações", type="primary", use_container_width=True):
                for loja in LOJAS:
                    st.session_state['df_pedidos'][loja] = df_editado_admin[loja]
                st.success("✅ Ajustes salvos com sucesso!")
                st.rerun()

        with col_exp:
            csv = df_editado_admin.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Exportar CSV",
                data=csv,
                file_name="separacao_semanal_horti.csv",
                mime="text/csv",
                use_container_width=True
            )

        with col_limpa:
            if st.button("🚨 Zerar Pedidos", use_container_width=True):
                st.session_state['df_pedidos'][LOJAS] = 0
                st.success("✅ Tabela zerada! Pronto para nova semana.")
                st.rerun()

# ─────────────────────────────────────────────
# ROTA 2: VISÃO DAS LOJAS
# ─────────────────────────────────────────────
elif perfil_navegacao == "Visão das Lojas":

    if acesso_total:
        loja_selecionada = st.selectbox("👁️ Visualizar como:", LOJAS)
    else:
        loja_selecionada = usuario_atual

    # ── Topbar: identidade + logout (sem sidebar) ──
    col_info, col_logout = st.columns([8, 2])
    with col_info:
        st.markdown(f"""
        <div class="topbar-loja">
            <div class="topbar-left">
                <span style="font-size:22px">📋</span>
                <div>
                    <div class="topbar-title">{loja_selecionada} — FLV Oriental</div>
                    <div class="topbar-sub">Preencha as quantidades necessárias e salve o pedido da semana</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_logout:
        # Alinha o botão verticalmente com o banner (46px = altura aprox do banner)
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("🚪 Sair / Logout", use_container_width=True):
            st.session_state['usuario_logado'] = None
            st.rerun()

    # ── Produtos visíveis para esta loja ──
    df_visiveis = st.session_state['df_produtos'][
        st.session_state['df_produtos'][loja_selecionada] == True
    ]
    df_loja = pd.merge(
        df_visiveis[["Código","Descrição","Código Barra","Marca"]],
        st.session_state['df_pedidos'][["Código", loja_selecionada]],
        on="Código"
    )

    with st.container(border=True):
        st.info("💡 **Dica:** Clique em uma célula da coluna **Qtde** para editar. "
                "Linhas com quantidade > 0 ficam destacadas automaticamente.")

        col_cfg_loja = {
            "Código":         st.column_config.NumberColumn(width=85,  format="%d", disabled=True),
            "Descrição":      st.column_config.TextColumn(disabled=True),
            "Código Barra":   st.column_config.TextColumn("Cód. Barras", width=130, disabled=True),
            "Marca":          st.column_config.TextColumn(width=110, disabled=True),
            loja_selecionada: st.column_config.NumberColumn(
                "🛒 Qtde", width=100, min_value=0, step=1,
                help="Digite a quantidade desejada para esta semana"
            ),
        }

        df_editado = st.data_editor(
            df_loja, column_config=col_cfg_loja,
            hide_index=True, use_container_width=True, height=520
        )

        itens_com_pedido = int((df_editado[loja_selecionada] > 0).sum())
        total_itens      = len(df_editado)
        total_unidades   = int(df_editado[loja_selecionada].sum())
        pct              = round(itens_com_pedido / total_itens * 100) if total_itens else 0

        st.divider()

        m1, m2, m3, _, col_btn = st.columns([1.5, 1.5, 1.5, 2, 3])

        with m1:
            st.metric("Itens preenchidos", f"{itens_com_pedido} / {total_itens}")
        with m2:
            st.metric("Total de unidades", total_unidades)
        with m3:
            st.metric("Cobertura", f"{pct}%")
        with col_btn:
            st.write("<br>", unsafe_allow_html=True)
            if st.button("💾 Salvar Pedido da Semana", type="primary", use_container_width=True):
                for _, row in df_editado.iterrows():
                    mask = st.session_state['df_pedidos']["Código"] == row["Código"]
                    st.session_state['df_pedidos'].loc[mask, loja_selecionada] = row[loja_selecionada]
                st.success(f"✅ Pedido da {loja_selecionada} salvo com sucesso!")

# ─────────────────────────────────────────────
# ROTA 3: CATÁLOGO DE PRODUTOS
# ─────────────────────────────────────────────
elif perfil_navegacao == "Catálogo de Produtos":

    page_header("🏷️", "Catálogo de Produtos",
                "Gerencie itens disponíveis e permissões por loja")

    with st.container(border=True):
        st.caption("➕ Adicione produtos na última linha  •  🗑️ Selecione a linha e pressione **Delete** para remover  •  ✅ Checkboxes controlam visibilidade por loja")

        config_catalogo = {
            "Código":       st.column_config.NumberColumn("Cód. Interno", width=90,  required=True, min_value=1, format="%d"),
            "Descrição":    st.column_config.TextColumn("Descrição do Item", width=310, required=True),
            "Código Barra": st.column_config.TextColumn("Cód. Barras",   width=130, required=True),
            "Marca":        st.column_config.TextColumn("Fabricante",    width=120, required=True),
        }
        for loja in LOJAS:
            config_catalogo[loja] = st.column_config.CheckboxColumn(loja, default=True, width=70)

        df_cat_editado = st.data_editor(
            st.session_state['df_produtos'],
            num_rows="dynamic",
            column_config=config_catalogo,
            hide_index=True,
            use_container_width=True,
            height=580
        )

        st.divider()

        col_atualizar, col_info, _ = st.columns([2, 4, 4])
        with col_atualizar:
            if st.button("🔄 Atualizar Catálogo", type="primary", use_container_width=True):
                st.session_state['df_produtos'] = df_cat_editado
                sincronizar_tabelas()
                st.success("✅ Catálogo e permissões atualizados para todas as lojas!")
                st.rerun()
        with col_info:
            total_prods = len(df_cat_editado)
            st.info(f"📦 **{total_prods}** produtos cadastrados  •  "
                    f"**{len(LOJAS)}** lojas configuradas")
