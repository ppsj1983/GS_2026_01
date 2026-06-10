import pandas as pd
import oracledb
import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
from branca.element import MacroElement
from jinja2 import Template
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import (r2_score, mean_absolute_error, root_mean_squared_error,
                             accuracy_score, classification_report)


# 1. Definição das consultas SQL (Correção: ajustado o nome da primeira variável)
consultas = {
    'df_cadastro_estacoes': "SELECT * FROM df_cadastro_estacoes",
    'df_historico_chuva': "SELECT * FROM HISTORICO_CHUVA",
    'df_historico_temperatura': "SELECT * FROM HISTORICO_TEMPERATURA",
    'df_historico_umidade': "SELECT * FROM HISTORICO_UMIDADE",
    'df_historico_ventos': "SELECT * FROM HISTORICO_VENTOS",
    'df_historico_DADOS_NOAA': "SELECT * FROM DADOS_NOAA"
}

# Dicionário que vai armazenar os DataFrames após a importação
dataframes_importados = {}

conn = None
cursor = None

try:
    # 2. Estabelecer a conexão única com o banco de dados
    print("-> Conectando ao servidor Oracle...")
    conn = oracledb.connect(
        user='rm567787',
        password='281083',
        dsn='oracle.fiap.com.br:1521/ORCL'
    )
    cursor = conn.cursor()
    print("-> Conexão estabelecida com sucesso.")

    # 3. Loop para executar cada consulta e carregar no Pandas
    for nome_df, sql in consultas.items():
        print(f"\n-> Importando dados de: {sql.split()[-1]}...")

        cursor.execute(sql)
        dados = cursor.fetchall()
        colunas = [desc[0] for desc in cursor.description]

        # Cria o DataFrame e armazena no dicionário
        dataframes_importados[nome_df] = pd.DataFrame(dados, columns=colunas)
        print(f"✅ {nome_df} carregado com {len(dataframes_importados[nome_df])} linhas.")

    # 4. Criação das variáveis globais para acesso direto (opcional)
    df_cadastro_estacoes = dataframes_importados['df_cadastro_estacoes']
    HISTORICO_CHUVA = dataframes_importados['df_historico_chuva']
    HISTORICO_TEMPERATURA = dataframes_importados['df_historico_temperatura']
    HISTORICO_UMIDADE = dataframes_importados['df_historico_umidade']
    HISTORICO_VENTOS = dataframes_importados['df_historico_ventos']
    df_noaa = dataframes_importados['df_historico_DADOS_NOAA']

    print("\n🎉 Todas as tabelas foram importadas com sucesso!")

except Exception as e:
    print(f"\n❌ Erro durante o processo de importação: {e}")

finally:
    # 5. Fecho seguro dos recursos do banco de dados
    if cursor and getattr(cursor, '_impl', None) is not None:
        try:
            cursor.close()
            print("\n-> Cursor fechado.")
        except Exception:
            pass

    if conn:
        try:
            conn.close()
            print("-> Conexão com o Oracle encerrada.")
        except Exception:
            pass

# 1. Criação do DataFrame agrupado (Usando o seu df_noaa real)
df_resumo_noaa = df_noaa.groupby(['TIPO_EVENTO', 'EVENTO_INTENSIDADE']).agg({
    'TOTAL': 'mean',
    'ANOM': 'mean'
}).reset_index()

# Renomear as colunas para deixar claro que são médias
df_resumo_noaa.columns = ['TIPO_EVENTO', 'EVENTO_INTENSIDADE', 'MEDIA_TOTAL', 'MEDIA_ANOM']

# Configuração da página do Streamlit
st.set_page_config(page_title="Previsão Climática Inteligente", layout="wide")

st.title("⛈️ Painel de Previsão Climática Estacional")
st.markdown("Selecione os parâmetros climáticos na barra lateral para calcular os modelos e atualizar o mapa.")

st.sidebar.header("🎛️ Parâmetros do Cenário")

PREV_MES = st.sidebar.selectbox(
    "Selecione o Mês Alvo:",
    options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    index=5  # Padrão: Junho
)
PREV_TIPO_EVENTO = st.sidebar.selectbox(
    "Tipo de Evento NOAA:",
    options=["EL_NINO", "LA_NINA", "NEUTRO"],
    index=0
)
PREV_EVENTO_INTENSIDADE = st.sidebar.selectbox(
    "Intensidade do Evento:",
    options=["1_FRACO", "2_MODERADO", "3_FORTE"],
    index=0
)

with st.spinner("Processando dados e treinando os modelos..."):
    # CORREÇÃO 1: Evita erro se a coluna tiver espaços ou nulos ao aplicar .str
    df_resumo_noaa["TIPO_EVENTO"] = df_resumo_noaa["TIPO_EVENTO"].astype(str).str.strip().str.upper()
    df_resumo_noaa["EVENTO_INTENSIDADE"] = df_resumo_noaa["EVENTO_INTENSIDADE"].astype(str).str.strip().str.upper()

    dados_previsao = df_resumo_noaa[
        (df_resumo_noaa["TIPO_EVENTO"] == PREV_TIPO_EVENTO.upper()) &
        (df_resumo_noaa["EVENTO_INTENSIDADE"] == PREV_EVENTO_INTENSIDADE.upper())
        ]

    if dados_previsao.empty:
        st.error("❌ Combinação de Evento e Intensidade não encontrada na base NOAA resumo.")
        st.stop()

    PREV_TOTAL = dados_previsao["MEDIA_TOTAL"].iloc[0]
    PREV_ANOM = dados_previsao["MEDIA_ANOM"].iloc[0]

    # CORREÇÃO 2: Filtragem correta usando máscaras booleanas no Pandas
    df_chuva_filtrado = HISTORICO_CHUVA[HISTORICO_CHUVA['MES_NUM'] == PREV_MES][
        ['COD', 'PRECIPITACAO_MM', 'ANO_MES', 'MES_NUM']].copy()
    df_temp_filtrado = HISTORICO_TEMPERATURA[HISTORICO_TEMPERATURA['MES_NUM'] == PREV_MES][
        ['COD', 'TEMPERATURA_C', 'ANO_MES', 'MES_NUM']].copy()
    df_umi_filtrado = HISTORICO_UMIDADE[HISTORICO_UMIDADE['MES_NUM'] == PREV_MES][
        ['COD', 'UMIDADE_RELATIVA', 'ANO_MES', 'MES_NUM']].copy()
    df_vent_filtrado = HISTORICO_VENTOS[HISTORICO_VENTOS['MES_NUM'] == PREV_MES][
        ['COD', 'VENTO_VELOCIDADE', 'ANO_MES', 'MES_NUM']].copy()

    df_chuva_filtrado = df_chuva_filtrado.reset_index(drop=True)
    df_temp_filtrado = df_temp_filtrado.reset_index(drop=True)
    df_umi_filtrado = df_umi_filtrado.reset_index(drop=True)
    df_vent_filtrado = df_vent_filtrado.reset_index(drop=True)

    # Cruzamentos estruturais (Garante relacionamento chave com df_noaa e df_cadastro_estacoes)
    df_chuva_filtrado = pd.merge(pd.merge(df_chuva_filtrado, df_noaa, on='ANO_MES', how='inner'), df_cadastro_estacoes,
                                 on='COD', how='inner')
    df_temp_filtrado = pd.merge(pd.merge(df_temp_filtrado, df_noaa, on='ANO_MES', how='inner'), df_cadastro_estacoes,
                                on='COD', how='inner')
    df_umi_filtrado = pd.merge(pd.merge(df_umi_filtrado, df_noaa, on='ANO_MES', how='inner'), df_cadastro_estacoes,
                               on='COD', how='inner')
    df_vent_filtrado = pd.merge(pd.merge(df_vent_filtrado, df_noaa, on='ANO_MES', how='inner'), df_cadastro_estacoes,
                                on='COD', how='inner')

    df_chuva_filtrado['CHOVEU'] = np.where(df_chuva_filtrado['PRECIPITACAO_MM'] > 0, 1, 0)

    for df_hist in [df_chuva_filtrado, df_temp_filtrado, df_umi_filtrado, df_vent_filtrado]:
        if 'MES' not in df_hist.columns:
            df_hist['MES'] = PREV_MES

    datasets_config = {
        "Chuva": {"df": df_chuva_filtrado, "target": "PRECIPITACAO_MM", "unidade": "mm"},
        "Temperatura": {"df": df_temp_filtrado, "target": "TEMPERATURA_C", "unidade": "°C"},
        "Umidade": {"df": df_umi_filtrado, "target": "UMIDADE_RELATIVA", "unidade": "%"},
        "Ventos": {"df": df_vent_filtrado, "target": "VENTO_VELOCIDADE", "unidade": "km/h"}
    }

    # CORREÇÃO 3: Verificação de colunas geradas pelo merge com df_noaa (ajuste se os nomes forem diferentes no seu banco)
    features_comuns = ['TOTAL', 'ANOM', 'MES', 'ALTITUDE', 'DIST_EQUADOR']

    df_cadastro_estacoes_pred = df_cadastro_estacoes.copy()
    df_cadastro_estacoes_pred['TOTAL'] = PREV_TOTAL
    df_cadastro_estacoes_pred['ANOM'] = PREV_ANOM
    df_cadastro_estacoes_pred['MES'] = PREV_MES
    X_estacoes = df_cadastro_estacoes_pred[features_comuns]

    # Execução das Regressões
    modelos_regressao = {}

    for nome, config in datasets_config.items():
        df_atual = config["df"]
        target = config["target"]

        # Garante que existem linhas suficientes após o dropna para evitar colapso no split
        df_filtrado = df_atual.dropna(subset=features_comuns + [target])
        if len(df_filtrado) < 10:
            st.error(f"❌ Dados históricos insuficientes para treinar o modelo de {nome} no mês selecionado.")
            st.stop()

        X = df_filtrado[features_comuns]
        y = df_filtrado[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)
        modelos_regressao[nome] = model

        df_cadastro_estacoes_pred[f"pred_{target}"] = model.predict(X_estacoes)

    # Execução da Classificação Binomial de Chuva
    df_chuva_clf = df_chuva_filtrado.dropna(subset=features_comuns + ['CHOVEU'])
    X_clf = df_chuva_clf[features_comuns]
    y_clf = df_chuva_clf['CHOVEU']

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X_clf, y_clf, test_size=0.2, random_state=42,
                                                                stratify=y_clf)
    modelo_rf_classificador = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced',
                                                     n_jobs=-1)
    modelo_rf_classificador.fit(X_train_c, y_train_c)
    preds_clf = modelo_rf_classificador.predict(X_test_c)
    acuracia = accuracy_score(y_test_c, preds_clf)

    # Arredondamento dos resultados finais
    df_cadastro_estacoes_pred['pred_PRECIPITACAO_MM'] = df_cadastro_estacoes_pred['pred_PRECIPITACAO_MM'].round(2)
    df_cadastro_estacoes_pred['pred_TEMPERATURA_C'] = df_cadastro_estacoes_pred['pred_TEMPERATURA_C'].round(2)
    df_cadastro_estacoes_pred['pred_UMIDADE_RELATIVA'] = df_cadastro_estacoes_pred['pred_UMIDADE_RELATIVA'].round(2)
    df_cadastro_estacoes_pred['pred_VENTO_VELOCIDADE'] = df_cadastro_estacoes_pred['pred_VENTO_VELOCIDADE'].round(2)
    df_cadastro_estacoes_pred['DIST_EQUADOR'] = df_cadastro_estacoes_pred['DIST_EQUADOR'].round(3)

    df_cadastro_estacoes_pred['PREV_CHUVA_BINOMIAL'] = modelo_rf_classificador.predict(X_estacoes)
    df_cadastro_estacoes_pred['PREV_CHUVA_PROB'] = modelo_rf_classificador.predict_proba(X_estacoes)[:, 1]

# Display das condições do cenário calculado nas caixas de métricas do Streamlit
col_info1, col_info2, col_info3 = st.columns(3)
col_info1.metric("Média Total NOAA", f"{PREV_TOTAL:.2f}")
col_info2.metric("Média Anomalia NOAA", f"{PREV_ANOM:.2f}")
col_info3.metric("Acurácia Classif. Chuva", f"{acuracia:.2%}")

import os
import folium
import tempfile
import pandas as pd
import streamlit as st

# ==============================================================================
st.subheader("📊 Consolidado Meteorológico por Unidade Federativa (UF)")

# 1. Agrupar os dados e calcular as métricas agregadas
df_consolidado = df_cadastro_estacoes_pred.groupby('UF').agg(
    Quant_Estacoes=('UF', 'count'),
    Media_Precipitacao_mm=('pred_PRECIPITACAO_MM', 'mean'),
    Media_Temperatura_C=('pred_TEMPERATURA_C', 'mean'),
    Media_Umidade_Relativa=('pred_UMIDADE_RELATIVA', 'mean'),
    Media_Vento_Velocidade=('pred_VENTO_VELOCIDADE', 'mean'),
    Media_Prev_Chuva_Prob=('PREV_CHUVA_PROB', 'mean')
).reset_index()

df_consolidado['Media_Prev_Chuva_Prob'] = df_consolidado['Media_Prev_Chuva_Prob'] * 100

# FILTRO: Manter apenas estados com 8 ou mais estações no estudo
df_consolidado = df_consolidado[df_consolidado['Quant_Estacoes'] >= 8]

# Ordenação para a Tabela: Por quantidade de estações (Decrescente)
df_tabela = df_consolidado.sort_values(by='Quant_Estacoes', ascending=False)

# Ordenação para o Gráfico: Por volume de chuva (Decrescente)
df_grafico = df_consolidado.sort_values(by='Media_Precipitacao_mm', ascending=False)

# 2. Renderizar a tabela formatada e interativa no Streamlit
if not df_consolidado.empty:
    st.dataframe(
        df_tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "UF": "Estado (UF)",
            "Quant_Estacoes": st.column_config.NumberColumn("Nº Estações", format="%d"),
            "Media_Precipitacao_mm": st.column_config.NumberColumn("Chuva Média (mm)", format="%.2f"),
            "Media_Temperatura_C": st.column_config.NumberColumn("Temp. Média (°C)", format="%.2f"),
            "Media_Umidade_Relativa": st.column_config.NumberColumn("Humidade Média (%)", format="%.2f"),
            "Media_Vento_Velocidade": st.column_config.NumberColumn("Vento Médio (km/h)", format="%.2f"),
            "Media_Prev_Chuva_Prob": st.column_config.NumberColumn("Prob. Chuva Média", format="%.1f%%")
        }
    )

    st.markdown("---")  # Linha divisória visual

    # 3. Adicionar o Gráfico de Barras no mesmo painel
    st.subheader("🌧️ Ranking de Estados (UF) por Volume de Chuva Média (Mín. 8 Estações)")

    st.bar_chart(
        data=df_grafico,
        x="UF",
        y="Media_Precipitacao_mm",
        color="#1f77b4",  # Cor azul padrão para chuva
        use_container_width=True
    )

    st.markdown("---")

    # 4. GERAÇÃO DO MAPA EM SEGUNDO PLANO (OCULTO DA TELA)
    st.subheader("💾 Exportação de Mapas Espaciais")

    # Filtrar o DataFrame original de mapas para conter apenas as UFs válidas (com >= 8 estações)
    ufs_validas = df_consolidado['UF'].tolist()
    df_mapa = df_cadastro_estacoes_pred[df_cadastro_estacoes_pred['UF'].isin(ufs_validas)].copy()

    # Remover registos sem coordenadas
    df_mapa = df_mapa.dropna(subset=['LATITUDE', 'LONGITUDE', 'pred_PRECIPITACAO_MM'])
    df_mapa['LATITUDE'] = df_mapa['LATITUDE'].astype(float)
    df_mapa['LONGITUDE'] = df_mapa['LONGITUDE'].astype(float)

    if not df_mapa.empty:
        # Criar o objeto do mapa em memória
        lat_media = df_mapa['LATITUDE'].mean()
        lon_media = df_mapa['LONGITUDE'].mean()
        mapa_oculto = folium.Map(location=[lat_media, lon_media], zoom_start=5)

        # Popular o mapa oculto com marcadores das UFs filtradas
        for index, linha in df_mapa.iterrows():
            valor_chuva = linha['pred_PRECIPITACAO_MM']
            prob_chuva = linha['PREV_CHUVA_PROB']
            temp_prev = linha['pred_TEMPERATURA_C']
            nome_estacao = linha.get('ESTACAO', index)
            cod_estacao = linha.get('COD', 'N/A')

            cor_marcador = 'red' if valor_chuva > 170 else 'orange' if valor_chuva > 100 else 'green'

            texto_popup = f"""
            <b>Estação:</b> {nome_estacao}<br>
            <b>Cód:</b> {cod_estacao}<br>
            <b>Chuva Prevista:</b> {valor_chuva:.2f} mm<br>
            <b>Probabilidade:</b> {prob_chuva:.1%}<br>
            <b>Temperatura:</b> {temp_prev} °C
            """

            folium.Marker(
                location=[linha['LATITUDE'], linha['LONGITUDE']],
                popup=folium.Popup(texto_popup, max_width=300),
                icon=folium.Icon(color=cor_marcador, icon='info-sign')
            ).add_to(mapa_oculto)

        # Salva num ficheiro temporário limpo sem argumentos extra
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp_file:
            caminho_temporario = tmp_file.name

        mapa_oculto.save(caminho_temporario)

        # Lê o conteúdo gerado para disponibilizar no botão do Streamlit
        with open(caminho_temporario, "r", encoding="utf-8") as f:
            mapa_html_conteudo = f.read()

        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)

        # Opção 1: Botão nativo de download do Streamlit
        st.download_button(
            label="🗺️ Descarregar Mapa Interativo (HTML)",
            data=mapa_html_conteudo,
            file_name="mapa_distribuicao_chuva_filtrado.html",
            mime="text/html",
            help="Clique para baixar o mapa contendo apenas os estados com 8 ou mais estações."
        )

        # Opção 2: Gravação física automática no SO
        caminho_downloads = os.path.join(os.path.expanduser("~"), "Downloads", "mapa_estacoes_filtrado.html")

        if st.button("📁 Salvar Cópia Direta na Pasta Downloads"):
            mapa_oculto.save(caminho_downloads)
            st.success(f"✅ Mapa guardado com sucesso em: `{caminho_downloads}`")

    else:
        st.warning("⚠️ Nenhuma estação encontrada nas UFs selecionadas para gerar o mapa oculto.")
else:
    st.warning("⚠️ Nenhuma Unidade Federativa (UF) possui o mínimo de 8 estações para ser exibida.")




