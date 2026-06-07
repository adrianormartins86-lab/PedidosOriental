import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Pedidos - Horti Japonês", layout="wide")

# Lista de lojas (baseada no layout das suas planilhas)
LOJAS = ["Loja 01", "Loja 02", "Loja 05", "Loja 06", "Loja 07", "Loja 08"]

# 2. INICIALIZAÇÃO DO BANCO DE DADOS TEMPORÁRIO (Session State)
# Nota: Em produção, você substituirá essa parte pela leitura/escrita do seu Google Sheets.
if 'df_produtos' not in st.session_state:
    # Produtos iniciais extraídos da imagem enviada
    produtos_iniciais = [
        {"Código": 521798, "Descrição": "Ampan Azuki C/6 Satsumaya", "Marca": "Satsumaya"},
        {"Código": 520504, "Descrição": "Kamaboko 200g Agronippo", "Marca": "Agronippo"},
        {"Código": 521150, "Descrição": "Kamaboko 200g Kai-Ho Agronippo", "Marca": "Agronippo"},
        {"Código": 521974, "Descrição": "Lokyozuke Cebolinha 200g Marunaka Cons", "Marca": "Agronippo"},
        {"Código": 533623, "Descrição": "Massa Gobomaki Kai-Ho 200g", "Marca": "Agronippo"},
        {"Código": 53662, "Descrição": "Massa Konnyaku 350g C/Alga", "Marca": "Agronippo"},
        {"Código": 524768, "Descrição": "Massa Shirataki 200g Agronippo Noodles", "Marca": "Agronippo"},
        {"Código": 583497, "Descrição": "Massa Shirataki 200g Hyde Alimentos", "Marca": "Hyde Alimentos"},
        {"Código": 577362, "Descrição": "Mirinzuke 200g Conserva De Nabo", "Marca": "Agronippo"},
        {"Código": 520911, "Descrição": "Narutomakii Kai.Ho 200g", "Marca": "Agronippo"}
    ]
    st.session_state['df_produtos'] = pd.DataFrame(produtos_iniciais)

if 'df_pedidos' not in st.session_state:
    # Cria a matriz de pedidos vinculada aos códigos ativos
    df_p = pd.DataFrame(columns=["Código"] + LOJAS)
    df_p["Código"] = st.session_state['df_produtos']["Código"]
    df_p[LOJAS] = 0  # Começa tudo zerado
    st.session_state['df_pedidos'] = df_p


# 3. FUNÇÃO DE SINCRONIZAÇÃO EM TEMPO REAL
def sincronizar_tabelas():
    """Garante que a tabela de digitação das lojas siga exatamente o cadastro do supervisor"""
    df_prod = st.session_state['df_produtos']
    df_ped = st.session_state['df_pedidos']
    
    # Remove da tabela de pedidos os produtos que o supervisor deletou
    df_ped = df_ped[df_ped["Código"].isin(df_prod["Código"])]
    
    # Identifica novos produtos adicionados pelo supervisor
    novos_codigos = df_prod[~df_prod["Código"].isin(df_ped["Código"])]["Código"]
    
    if not novos_codigos.empty:
        df_novos = pd.DataFrame(columns=["Código"] + LOJAS)
        df_novos["Código"] = novos_codigos
        df_novos[LOJAS] = 0  # Inicializa o novo item com zero para todas as lojas
        df_ped = pd.concat([df_ped, df_novos], ignore_index=True)
        
    st.session_state['df_pedidos'] = df_ped

# Executa a sincronização preventiva
sincronizar_tabelas()


# 4. INTERFACE DO USUÁRIO
st.title("🍣 Sistema Central de Pedidos - Horti Japonês")

# Menu de navegação lateral
perfil = st.sidebar.radio("Selecione o seu Perfil:", ["Área da Loja (Digitação)", "Painel do Supervisor (Gerencial)"])

# ---------------------------------------------------------
# CÓDIGO DA VISÃO DA LOJA
# ---------------------------------------------------------
if perfil == "Área da Loja (Digitação)":
    st.header("📋 Lançamento Semanal de Pedidos")
    loja_selecionada = st.selectbox("Selecione a sua Loja para digitação:", LOJAS)
    
    # Faz um merge dinâmico para trazer a descrição atualizada do produto e a quantidade da loja
    df_loja = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'][["Código", loja_selecionada]], on="Código")
    
    st.info(f"O catálogo abaixo reflete as atualizações mais recentes do supervisor. Insira os pedidos da **{loja_selecionada}**:")
    
    # Editor focado apenas na coluna da loja selecionada
    df_editado = st.data_editor(
        df_loja,
        column_config={
            "Código": st.column_config.NumberColumn(disabled=True),
            "Descrição": st.column_config.TextColumn(disabled=True),
            "Marca": st.column_config.TextColumn(disabled=True),
            loja_selecionada: st.column_config.NumberColumn("Qtd Pedido", min_value=0, step=1)
        },
        hide_index=True,
        use_container_width=True
    )
    
    if st.button("💾 Enviar/Atualizar Pedido da Loja", type="primary"):
        # Transfere os dados editados de volta para o banco de dados principal
        for idx, row in df_editado.iterrows():
            cod = row["Código"]
            qtd = row[loja_selecionada]
            st.session_state['df_pedidos'].loc[st.session_state['df_pedidos']["Código"] == cod, loja_selecionada] = qtd
        st.success(f"Sucesso! Os dados da {loja_selecionada} foram gravados.")

# ---------------------------------------------------------
# CÓDIGO DA VISÃO DO SUPERVISOR
# ---------------------------------------------------------
else:
    st.header("⚙️ Painel Administrativo")
    
    # Divisão por abas para organizar o trabalho do Supervisor
    aba_cadastro, aba_consolidado = st.tabs(["✏️ Cadastrar/Editar Produtos", "📊 Visualizar e Fechar Pedidos"])
    
    with aba_cadastro:
        st.subheader("Gerenciamento do Catálogo Geral")
        st.caption("Dica: Use a última linha vazia com o símbolo '+' para adicionar novos produtos. Para deletar, selecione a linha clicando na lateral esquerda e aperte 'Delete' no teclado.")
        
        # O Editor Dinâmico do Catálogo (num_rows="dynamic" habilita inclusão/exclusão)
        df_produtos_editado = st.data_editor(
            st.session_state['df_produtos'],
            num_rows="dynamic",
            column_config={
                "Código": st.column_config.NumberColumn("Código Interno", required=True, min_value=1),
                "Descrição": st.column_config.TextColumn("Descrição do Item", required=True),
                "Marca": st.column_config.TextColumn("Fabricante/Marca", required=True)
            },
            hide_index=True,
            use_container_width=True
        )
        
        if st.button("🔄 Salvar e Disponibilizar Novo Catálogo para as Lojas", type="primary"):
            st.session_state['df_produtos'] = df_produtos_editado
            sincronizar_tabelas()
            st.success("Catálogo atualizado com sucesso! Todas as visões das lojas foram modificadas em tempo real.")
            st.rerun()

    with aba_consolidado:
        st.subheader("Painel Geral de Separação")
        
        # Consolida as descrições e todas as quantidades digitadas pelas lojas em uma única tabela
        df_final = pd.merge(st.session_state['df_produtos'], st.session_state['df_pedidos'], on="Código")
        
        # Calcula a soma total horizontal para o supervisor saber o quanto pedir do fornecedor
        df_final["Total Consolidado"] = df_final[LOJAS].sum(axis=1)
        
        # Exibe o resultado de forma limpa
        st.dataframe(df_final, hide_index=True, use_container_width=True)
        
        st.divider()
        col_exp, col_limpeza = st.columns(2)
        
        with col_exp:
            st.markdown("### 📥 Exportação de Resultados")
            csv = df_final.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download dos Pedidos Consolidados (CSV)",
                data=csv,
                file_name='separacao_semanal_horti.csv',
                mime='text/csv'
            )
            
        with col_limpeza:
            st.markdown("### 🧹 Preparação para a Próxima Semana")
            st.warning("A ação abaixo vai zerar a quantidade de pedidos digitada pelas lojas, mas preservará o cadastro de produtos.")
            
            if st.button("🚨 Limpar Pedidos das Lojas (Zerar Semana)"):
                st.session_state['df_pedidos'][LOJAS] = 0
                st.success("Tabela limpa! O sistema está pronto para receber as digitações da próxima semana.")
                st.rerun()
