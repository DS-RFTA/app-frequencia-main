import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64 # Importação necessária para processar a imagem em HTML

# ------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (Layout Largo para o Dashboard)
# ------------------------------------------------
# Adicione o page_icon apontando para o arquivo da sua imagem
st.set_page_config(page_title="Gestão de Pregação Infantil", layout="wide", page_icon="logos.png")

#=========================================================
# 2. INTERFACE COM ABAS (TABS) E LOGO CENTRALIZADA
# =========================================================

# --- Função Auxiliar (Necessária para centralizar imagem via HTML) ---
def render_centered_logo(image_path, width=150):
    """Lê a imagem local, converte para base64 e insere centralizada via HTML/CSS."""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Gera o HTML com alinhamento centralizado e tamanho ajustável
        html_code = f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="data:image/png;base64,{encoded_string}" width="{width}">
            </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
    except FileNotFoundError:
        # Se não encontrar o arquivo de imagem, mostra uma mensagem amigável
        st.error(f"Arquivo de imagem '{image_path}' não encontrado na pasta.")

# --- Execução da Logo e Título ---

# 1. Mostra a logo centralizada (Substitua "logo.png" pelo nome do seu arquivo se for diferente)
render_centered_logo("logo.png", width=150) 

# 2. Mostra o título centralizado abaixo da logo
st.markdown("<h2 style='text-align: center;'>SISTEMA DE GESTÃO - PONTO DE PREGAÇÃO</h2>", unsafe_allow_html=True)

st.divider()
# ------------------------------------------------
# 1. FUNÇÕES DO BANCO DE DADOS
# ------------------------------------------------
def init_db():
    conn = sqlite3.connect('relatorios_infantis.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS relatorios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            local TEXT,
            data DATE,
            comp_jovens_adultos INTEGER,
            comp_criancas INTEGER,
            comp_total INTEGER,
            criancas_locais INTEGER,
            adolescentes_locais INTEGER,
            jovens_adultos_locais INTEGER,
            total_evangelizadas INTEGER,
            conv_criancas INTEGER,
            obs_conv_criancas TEXT,
            conv_adolescentes INTEGER,
            conv_jovens_adultos INTEGER,
            total_conversoes INTEGER,
            lit_manuais INTEGER,
            obs_lit_manuais TEXT,
            lit_impressas INTEGER,
            ativ_biblicas INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def salvar_relatorio(dados):
    conn = sqlite3.connect('relatorios_infantis.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO relatorios (
            local, data, comp_jovens_adultos, comp_criancas, comp_total,
            criancas_locais, adolescentes_locais, jovens_adultos_locais, total_evangelizadas,
            conv_criancas, obs_conv_criancas, conv_adolescentes, conv_jovens_adultos, total_conversoes,
            lit_manuais, obs_lit_manuais, lit_impressas, ativ_biblicas
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', dados)
    conn.commit()
    conn.close()

init_db()

aba_form, aba_dash = st.tabs(["📝 Inserir Relatório", "📊 Dashboard Estratégico"])

# ==========================================
# ABA 1: FORMULÁRIO DE INSERÇÃO
# ==========================================
with aba_form:
    with st.form("form_relatorio", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            local = st.text_input("Local / Ponto de Pregação", placeholder="Ex: Tiradentes")
        with col2:
            data = st.date_input("Data do Relatório")

        st.write("---")
        
        # Componentes
        st.write("**Componentes Presentes**")
        col3, col4 = st.columns(2)
        with col3: comp_jovens_adultos = st.number_input("Jovens/Adultos (Componentes)", min_value=0, step=1)
        with col4: comp_criancas = st.number_input("Crianças (COI)", min_value=0, step=1)

        # Público Local
        st.write("**Público Local e Vidas Evangelizadas**")
        criancas_locais = st.number_input("Crianças Locais Presentes", min_value=0, step=1)
        adolescentes_locais = st.number_input("Adolescentes Locais Presentes", min_value=0, step=1)
        jovens_adultos_locais = st.number_input("Jovens/Adultos Locais Presentes", min_value=0, step=1)
        total_evangelizadas = st.number_input("Total de Vidas Evangelizadas", min_value=0, step=1)

        # Conversões
        st.write("**Conversões**")
        col5, col6 = st.columns([1, 2])
        with col5: conv_criancas = st.number_input("Conversões de Crianças", min_value=0, step=1)
        with col6: obs_conv_criancas = st.text_input("Observação (Conv. Crianças)")
            
        conv_adolescentes = st.number_input("Conversões de Adolescentes", min_value=0, step=1)
        conv_jovens_adultos = st.number_input("Conversões de Jovens e Adultos", min_value=0, step=1)

        # Literaturas
        st.write("**Literaturas e Atividades Entregues**")
        col7, col8 = st.columns([1, 2])
        with col7: lit_manuais = st.number_input("Literaturas Manuais Entregues", min_value=0, step=1)
        with col8: obs_lit_manuais = st.text_input("Observação (Lit. Manuais)")
            
        lit_impressas = st.number_input("Literaturas Impressas Entregues", min_value=0, step=1)
        ativ_biblicas = st.number_input("Atividades Bíblicas Evangelísticas Entregues", min_value=0, step=1)

        submitted = st.form_submit_button("💾 Salvar Relatório no Banco", use_container_width=True)

        if submitted:
            if not local:
                st.error("Preencha o campo 'Local / Ponto de Pregação'.")
            else:
                comp_total = comp_jovens_adultos + comp_criancas
                total_conversoes = conv_criancas + conv_adolescentes + conv_jovens_adultos
                dados = (
                    local, data, comp_jovens_adultos, comp_criancas, comp_total,
                    criancas_locais, adolescentes_locais, jovens_adultos_locais, total_evangelizadas,
                    conv_criancas, obs_conv_criancas, conv_adolescentes, conv_jovens_adultos, total_conversoes,
                    lit_manuais, obs_lit_manuais, lit_impressas, ativ_biblicas
                )
                salvar_relatorio(dados)
                st.success(f"✅ Relatório de '{local}' salvo com sucesso!")

# ==========================================
# ABA 2: DASHBOARD ESTRATÉGICO
# ==========================================
with aba_dash:
    # Conecta ao banco e carrega os dados com Pandas
    conn = sqlite3.connect('relatorios_infantis.db')
    df = pd.read_sql_query("SELECT * FROM relatorios", conn)
    conn.close()

    if df.empty:
        st.info("📊 O banco de dados está vazio. Insira relatórios na aba ao lado para visualizar os gráficos.")
    else:
        # Tratamento de datas
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values(by='data')

        # ---------------- MÉTRICAS PRINCIPAIS (KPIs) ----------------
        st.subheader("Indicadores de Desempenho (KPIs)")
        col1, col2, col3, col4 = st.columns(4)
        
        total_vidas = df['total_evangelizadas'].sum()
        total_conv = df['total_conversoes'].sum()
        total_materiais = df['lit_manuais'].sum() + df['lit_impressas'].sum() + df['ativ_biblicas'].sum()
        media_criancas_locais = df['criancas_locais'].mean()

        col1.metric("Vidas Evangelizadas (Total)", int(total_vidas))
        col2.metric("Conversões (Total)", int(total_conv))
        col3.metric("Materiais Entregues", int(total_materiais))
        col4.metric("Média de Crianças por Culto", int(media_criancas_locais))

        st.divider()

        # ---------------- GRÁFICOS ESTRATÉGICOS ----------------
        c1, c2 = st.columns(2)

        with c1:
            # Evolução de Vidas Evangelizadas ao longo do tempo
            st.markdown("**Evolução de Vidas Evangelizadas**")
            fig_vidas = px.bar(df, x='data', y='total_evangelizadas', text='total_evangelizadas',
                               labels={'data': 'Data do Relatório', 'total_evangelizadas': 'Vidas'},
                               color_discrete_sequence=['#1f77b4'])
            fig_vidas.update_traces(textposition='outside')
            st.plotly_chart(fig_vidas, use_container_width=True)

        with c2:
            # Perfil das Conversões (Gráfico de Rosca)
            st.markdown("**Perfil das Conversões por Faixa Etária**")
            df_conv = pd.DataFrame({
                'Público': ['Crianças', 'Adolescentes', 'Jovens/Adultos'],
                'Conversões': [df['conv_criancas'].sum(), df['conv_adolescentes'].sum(), df['conv_jovens_adultos'].sum()]
            })
            # Filtrar para não mostrar zeros no gráfico de pizza
            df_conv = df_conv[df_conv['Conversões'] > 0]
            
            if not df_conv.empty:
                fig_conv = px.pie(df_conv, values='Conversões', names='Público', hole=0.4,
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_conv, use_container_width=True)
            else:
                st.write("Nenhuma conversão registrada ainda para gerar o gráfico.")

        st.divider()

        c3, c4 = st.columns(2)

        with c3:
            # Distribuição do Público Local
            st.markdown("**Composição do Público por Evento**")
            # Preparando dados para gráfico de barras agrupadas
            df_publico = df[['local', 'data', 'criancas_locais', 'adolescentes_locais', 'jovens_adultos_locais']].copy()
            df_publico['Evento'] = df_publico['local'] + " (" + df_publico['data'].dt.strftime('%d/%m') + ")"
            
            fig_pub = px.bar(df_publico, x='Evento', 
                             y=['criancas_locais', 'adolescentes_locais', 'jovens_adultos_locais'],
                             barmode='group',
                             labels={'value': 'Quantidade Presente', 'variable': 'Faixa Etária'},
                             color_discrete_sequence=px.colors.qualitative.Set2)
            # Ajustando a legenda
            newnames = {'criancas_locais': 'Crianças', 'adolescentes_locais': 'Adolescentes', 'jovens_adultos_locais': 'Jovens/Adultos'}
            fig_pub.for_each_trace(lambda t: t.update(name = newnames[t.name]))
            st.plotly_chart(fig_pub, use_container_width=True)

        with c4:
            # Resumo de Entregas
            st.markdown("**Balanço de Materiais Entregues**")
            df_entregas = pd.DataFrame({
                'Tipo de Material': ['Manuais', 'Impressas', 'Atividades Bíblicas'],
                'Quantidade': [df['lit_manuais'].sum(), df['lit_impressas'].sum(), df['ativ_biblicas'].sum()]
            })
            fig_entregas = px.bar(df_entregas, x='Tipo de Material', y='Quantidade', text='Quantidade',
                                  color='Tipo de Material', color_discrete_sequence=px.colors.qualitative.Vivid)
            fig_entregas.update_traces(textposition='outside')
            st.plotly_chart(fig_entregas, use_container_width=True)
            
        # ---------------- TABELA DE DADOS BRUTOS ----------------
        with st.expander("Ver Tabela Completa de Dados"):
            st.dataframe(df.drop(columns=['id']), use_container_width=True)