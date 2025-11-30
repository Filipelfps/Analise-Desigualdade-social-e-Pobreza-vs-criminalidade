import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns



st.set_page_config(
    page_title="Dashboard de Análise Criminal",
    page_icon="🗺️",
    layout="wide",  # 'wide' usa toda a largura da tela
    initial_sidebar_state="expanded"
)


@st.cache_data
def carregar_dados():
    

    df = pd.read_csv('dados_tratados_final.csv')
    
    # Faz o DE-PARA dos nomes das colunas
    df = df.rename(columns={
        'NM_MUNICIP': 'Bairro',  
        'taxa_homicidio_100k': 'Taxa_Homicidios_100k', 
        'Índice de Gini 2010': 'Índice_Gini',
        'Taxa de desocupação - 10 anos ou mais de idade 2010': 'Taxa_Desemprego_Pct', # Nome longo que aparece na imagem
        'Renda per capita 2010': 'Renda_Media_Salarial'
    })
    
    
    
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



st.write("---") 
st.subheader("Distribuição Espacial da Violência")

# Função para carregar o mapa (usa cache para não travar)
@st.cache_data
def carregar_mapa():
    # Carrega o arquivo GeoJSON que você subiu
    return gpd.read_file("mapa_completo.geojson")

try:
    gdf_final = carregar_mapa()
     
    # Mapa 1: Violencia
    st.subheader("Distribuição da Violência")
    
    # Criação da Figura 
    fig_vio, ax_vio = plt.subplots(figsize=(12, 10))
    
    gdf_final.plot(
        column='taxa_homicidio_100k',
        cmap='Reds',
        legend=True,
        legend_kwds={'label': "Taxa de Homicídios por 100k habitantes",
                     'orientation': "vertical"},
        edgecolor='gray',
        linewidth=0.3,
        missing_kwds={'color': 'lightgrey'},
        ax=ax_vio
    )

    ax_vio.set_axis_off() 
    st.pyplot(fig_vio) 

    # --- TABELA: TOP 10 VIOLÊNCIA ---
    st.write("### 🚨 Detalhamento: Os 10 Municípios com Maiores Taxas")
    
    # Pegamos os 10 maiores e selecionamos só as colunas que importam
    top_10_violencia = gdf_final.nlargest(10, 'taxa_homicidio_100k')[
        ['NM_MUNICIP', 'taxa_homicidio_100k', 'População total 2010']
    ]

    # Renomeando as collunas para ficar mais agradavel
    top_10_formatada = top_10_violencia.rename(columns={
        'NM_MUNICIP': 'Município',
        'taxa_homicidio_100k': 'Homicídios (por 100k hab)',
        'População total 2010': 'População Total'
    })

    # Exibindo a Tabela
    st.dataframe(
        top_10_formatada, 
        hide_index=True, 
        use_container_width=True
    )

    # Mapa 2: Desigualdade Social
    st.write("---") 
    st.subheader("Distribuição da Desigualdade Social (Gini)")


    fig_gini, ax_gini = plt.subplots(figsize=(12, 10))

    gdf_final.plot(
    column='Índice de Gini 2010', 
    cmap='Blues', 
    legend=True,
    legend_kwds={'label': "Índice de Gini (0 a 1)", 'orientation': "vertical"},
    edgecolor='gray',
    linewidth=0.3,
    missing_kwds={'color': '#f0f0f0', 'label': 'Dados indisponíveis'},
    ax=ax_gini
    )

    plt.tight_layout()
    ax_gini.set_axis_off()

    st.pyplot(fig_gini)

    # TABELA: TOP 10 DESIGUALDADE 
    st.write("### 📉 Detalhamento: Os 10 Municípios mais Desiguais")
    
    # 1. Filtra os dados (A mágica acontece no .nlargest)
    # Buscamos os 10 maiores valores na coluna do Gini
    top_10_gini = gdf_final.nlargest(10, 'Índice de Gini 2010')[
        ['NM_MUNICIP', 'Índice de Gini 2010', 'População total 2010']
    ]

    # 2. Estética: Renomear para ficar bonito na tela
    top_10_gini_formatada = top_10_gini.rename(columns={
        'NM_MUNICIP': 'Município',
        'Índice de Gini 2010': 'Índice de Gini',
        'População total 2010': 'População Total'
    })

    # Exibir a Tabela
    st.dataframe(
        top_10_gini_formatada, 
        hide_index=True, 
        use_container_width=True
    )

    
    st.write("---")
    st.subheader("🔎 Análise de Correlação: O que influencia a violência?")
    st.markdown("Verificando se existe relação direta entre **Desigualdade** ou **Renda** com a taxa de homicídios.")

   
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # GRÁFICO 1: GINI vs CRIME 
    sns.scatterplot(
        data=gdf_final,
        x='Índice de Gini 2010',
        y='taxa_homicidio_100k',
        color='blue',
        alpha=0.6,
        ax=ax1 # Desenhamos no lado esquerdo
    )
    
    ax1.set_title('Desigualdade vs. Violência', fontsize=14)
    ax1.set_xlabel('Índice de Gini (0 a 1)')
    ax1.set_ylabel('Homicídios por 100k hab')

    #  GRÁFICO 2: RENDA vs CRIME 
    
    sns.scatterplot(
        data=gdf_final,
        x='Renda per capita 2010',
        y='taxa_homicidio_100k',
        color='green',
        alpha=0.6,
        ax=ax2 # Desenhamos no lado direito
    )
    ax2.set_title('Renda vs. Violência', fontsize=14)
    ax2.set_xlabel('Renda per Capita (R$)')
    ax2.set_ylabel('Homicídios por 100k hab')

    # Ajuste fino visual
    plt.tight_layout()
    
    # Mostra tudo na tela
    st.pyplot(fig)

    #  MATRIZ DE CORRELAÇÃO (HEATMAP) 
    
    st.write("---")
    st.subheader("🔥 Matriz de Correlação: Resumo Estatístico")
    st.markdown("Visualização matemática de como as variáveis se relacionam entre si. Cores quentes (vermelho) indicam forte relação positiva, cores frias (azul) indicam relação negativa.")


    colunas_interesse = [
        'taxa_homicidio_100k',
        'Índice de Gini 2010',
        'Renda per capita 2010',
        'População total 2010'
    ]

    # Calculo da Matriz
    correlacao = gdf_final[colunas_interesse].corr()

    # Criação do Gráfico
    
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))

    sns.heatmap(
        correlacao,
        annot=True,         
        cmap='coolwarm',    
        fmt=".2f",          
        vmin=-1, vmax=1,    
        linewidths=0.5,     
        square=True,        
        ax=ax_corr          
    
    )
    plt.tight_layout()
    st.pyplot(fig_corr)


except Exception as e:
    st.error(f"Erro ao carregar o mapa. Verifique se o arquivo 'mapa_completo.geojson' está na pasta. Detalhe: {e}")

    