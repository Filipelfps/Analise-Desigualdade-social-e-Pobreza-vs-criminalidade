import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuração da Página ---
# A configuração da página deve ser o primeiro comando Streamlit
st.set_page_config(
    page_title="Dashboard de Análise Criminal",
    page_icon="🗺️",
    layout="wide",  # 'wide' usa toda a largura da tela
    initial_sidebar_state="expanded"
)

# --- Função para Carregar/Criar Dados (Mock Data) ---
# O decorator @st.cache_data armazena o resultado da função em cache.
# Isso evita que os dados sejam recarregados a cada interação do usuário.
@st.cache_data
def carregar_dados():
    # Carrega o CSV que você exportou do notebook
    # CERTO
    df = pd.read_csv('dados_tratados_final.csv')
    
    # Faz o DE-PARA dos nomes das colunas
    df = df.rename(columns={
        'NM_MUNICIP': 'Bairro',  # O dashboard chama de Bairro, mas vamos colocar as Cidades aqui
        'taxa_homicidio_100k': 'Taxa_Homicidios_100k', # Certifique-se que essa coluna existe no seu CSV exportado
        'Índice de Gini 2010': 'Índice_Gini',
        'Taxa de desocupação - 10 anos ou mais de idade 2010': 'Taxa_Desemprego_Pct', # Nome longo que aparece na imagem
        'Renda per capita 2010': 'Renda_Media_Salarial'
    })
    
    # Criando uma coluna de Ano fictícia se não tiver no dataset, 
    # pois o dashboard usa um filtro de ano
    if 'Ano' not in df.columns:
        df['Ano'] = 2010 
        
    return df

# Carrega os dados
df = carregar_dados()

# --- Barra Lateral (Sidebar) com Filtros ---
st.sidebar.header('Filtros Interativos')

# Filtro de Ano (Slider)
# --- Filtro de Ano Inteligente ---
min_ano = int(df['Ano'].min())
max_ano = int(df['Ano'].max())

if min_ano == max_ano:
    # Se só existe um ano nos dados (2010), mostra apenas texto
    st.sidebar.markdown(f"**Dados disponíveis para o ano: {min_ano}**")
    ano_selecionado = min_ano
else:
    # Se existirem vários anos, mostra o slider
    ano_selecionado = st.sidebar.slider(
        'Selecione o Ano:',
        min_value=min_ano,
        max_value=max_ano,
        value=max_ano
    )

# Filtro de Bairro (Multiselect)
bairros_selecionados = st.sidebar.multiselect(
    'Selecione os Bairros:',
    options=df['Bairro'].unique(),
    default=df['Bairro'].unique() # Por padrão, todos vêm selecionados
)

# Aplica os filtros ao DataFrame
df_filtrado = df[
    (df['Ano'] == ano_selecionado) &
    (df['Bairro'].isin(bairros_selecionados))
]

# --- Título Principal ---
st.title('🗺️ Dashboard: Criminalidade e Desigualdade Social')
st.markdown(f"Analisando dados para o ano de **{ano_selecionado}**.")

# --- Métricas Principais (KPIs) ---
st.subheader('Métricas Principais (Dados Filtrados)')

# Organiza as métricas em colunas
col1, col2, col3 = st.columns(3)

# Métrica 1: Média do Índice Gini
media_gini = df_filtrado['Índice_Gini'].mean()
col1.metric(label="Média do Índice Gini", value=f"{media_gini:.2f}")

# Métrica 2: Média da Taxa de Homicídios
media_homicidios = df_filtrado['Taxa_Homicidios_100k'].mean()
col2.metric(label="Média Homicídios (por 100k hab.)", value=f"{media_homicidios:.1f}")

# Métrica 3: Média da Renda (em Salários Mínimos)
media_renda = df_filtrado['Renda_Media_Salarial'].mean()
col3.metric(label="Média Renda (em Sal. Mín.)", value=f"{media_renda:.1f}")

st.markdown("---") # Linha divisória

# --- Gráficos ---
st.subheader('Visualização dos Dados')

# Organiza os gráficos em colunas
col_graf1, col_graf2 = st.columns(2)

# Gráfico 1: Correlação (Gráfico de Dispersão)
# Usando Plotly Express para gráficos interativos
fig_correlacao = px.scatter(
    df_filtrado,
    x='Índice_Gini',
    y='Taxa_Homicidios_100k',
    hover_name='Bairro',
    title='Correlação: Índice Gini vs. Taxa de Homicídios',
    color='Renda_Media_Salarial',
    color_continuous_scale='Reds',
    labels={
        'Índice_Gini': 'Índice de Desigualdade (Gini)',
        'Taxa_Homicidios_100k': 'Homicídios (por 100k hab.)'
    }
)
col_graf1.plotly_chart(fig_correlacao, use_container_width=True)

# Gráfico 2: Comparação (Gráfico de Barras)
# Agrupando dados por bairro para o gráfico de barras
df_agrupado = df_filtrado.groupby('Bairro')['Taxa_Homicidios_100k'].mean().reset_index()

fig_barras = px.bar(
    df_agrupado.sort_values('Taxa_Homicidios_100k', ascending=False),
    x='Bairro',
    y='Taxa_Homicidios_100k',
    title='Taxa Média de Homicídios por Bairro',
    labels={'Taxa_Homicidios_100k': 'Média de Homicídios'}
)
col_graf2.plotly_chart(fig_barras, use_container_width=True)


# --- Tabela de Dados (Dataframe) ---
st.subheader('Dados Detalhados (Filtrados)')
st.dataframe(df_filtrado)

# Exibindo os dados brutos (opcional, bom para depuração)
# if st.checkbox('Mostrar dados brutos'):
#     st.subheader('Dados Brutos (Completos)')
#     st.write(df)