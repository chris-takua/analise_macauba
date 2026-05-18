import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. CAMINHOS
caminho_base = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga"
)

arquivo_picos = caminho_base / "resultados" / "planilhas_araponga" / "todos_os_picos_araponga.csv"
pasta_saida = caminho_base / "resultados" / "planilhas_araponga"
pasta_graficos = caminho_base / "resultados" / "picos_araponga"


# 2. PARÂMETROS
tolerancia_hz = 1.0
ocorrencia_minima = 3


# 3. LEITURA DOS PICOS
df = pd.read_csv(arquivo_picos)

if df.empty:
    print("A planilha de picos está vazia.")
    raise SystemExit

df = df.sort_values(by="frequencia_hz").reset_index(drop=True)

print(f"\nTotal de picos lidos: {len(df)}")


# 4. AGRUPAMENTO DAS FREQUÊNCIAS
grupos = []
grupo_atual = []

for _, linha in df.iterrows():
    frequencia = linha["frequencia_hz"]

    if not grupo_atual:
        grupo_atual.append(linha.to_dict())
    else:
        frequencias_grupo = [item["frequencia_hz"] for item in grupo_atual]
        centro_grupo = sum(frequencias_grupo) / len(frequencias_grupo)

        if abs(frequencia - centro_grupo) <= tolerancia_hz:
            grupo_atual.append(linha.to_dict())
        else:
            grupos.append(grupo_atual)
            grupo_atual = [linha.to_dict()]

if grupo_atual:
    grupos.append(grupo_atual)


# 5. RESUMO DOS GRUPOS
lista_grupos = []

for indice_grupo, grupo in enumerate(grupos, start=1):
    df_grupo = pd.DataFrame(grupo)

    frequencia_media = df_grupo["frequencia_hz"].mean()
    frequencia_min = df_grupo["frequencia_hz"].min()
    frequencia_max = df_grupo["frequencia_hz"].max()
    frequencia_std = df_grupo["frequencia_hz"].std()
    magnitude_media = df_grupo["magnitude"].mean()
    coerencia_media = df_grupo["coerencia"].mean()
    fase_media = df_grupo["fase_graus"].mean()

    arquivos_unicos = sorted(df_grupo["arquivo"].unique())
    n_ocorrencias = len(df_grupo)
    n_arquivos_unicos = len(arquivos_unicos)

    lista_grupos.append({
        "grupo_modal": indice_grupo,
        "frequencia_media_hz": frequencia_media,
        "frequencia_min_hz": frequencia_min,
        "frequencia_max_hz": frequencia_max,
        "desvio_padrao_hz": frequencia_std,
        "magnitude_media": magnitude_media,
        "coerencia_media": coerencia_media,
        "fase_media_graus": fase_media,
        "n_ocorrencias": n_ocorrencias,
        "n_arquivos_unicos": n_arquivos_unicos,
        "arquivos": " | ".join(arquivos_unicos)
    })

df_grupos = pd.DataFrame(lista_grupos)


# 6. FILTRO DE RECORRÊNCIA
df_grupos_relevantes = df_grupos[df_grupos["n_ocorrencias"] >= ocorrencia_minima].copy()
df_grupos_relevantes = df_grupos_relevantes.sort_values(by="frequencia_media_hz").reset_index(drop=True)


# 7. SALVAR PLANILHAS
arquivo_grupos_todos = pasta_saida / "grupos_modais_todos_araponga.csv"
arquivo_grupos_relevantes = pasta_saida / "grupos_modais_relevantes_araponga.csv"

df_grupos.to_csv(arquivo_grupos_todos, index=False, encoding="utf-8-sig")
df_grupos_relevantes.to_csv(arquivo_grupos_relevantes, index=False, encoding="utf-8-sig")


# 8. GRÁFICO DE RECORRÊNCIA (VERSÃO OTIMIZADA)
if not df_grupos_relevantes.empty:
    # Selecionar apenas os 20 grupos mais recorrentes
    df_plot = df_grupos_relevantes.nlargest(20, "n_ocorrencias").sort_values("frequencia_media_hz")

    plt.figure(figsize=(14, 7))

    # Frequências formatadas como texto para o eixo x
    frequencias_rotulos = df_plot["frequencia_media_hz"].round(2).astype(str)

    # Criar gráfico de barras
    barras = plt.bar(
        frequencias_rotulos,
        df_plot["n_ocorrencias"],
        color="skyblue",
        edgecolor="navy"
    )

    # Rótulos no topo das barras
    plt.bar_label(barras, padding=3, fontsize=9)

    plt.xlabel("Frequência modal consolidada (Hz)", fontsize=12)
    plt.ylabel("Número de ocorrências", fontsize=12)
    plt.title(f"Top {len(df_plot)} frequências mais recorrentes - Araponga", fontsize=14, pad=20)

    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.grid(True, axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    arquivo_grafico = pasta_graficos / "recorrencia_frequencias_otimizado.png"
    plt.savefig(arquivo_grafico, dpi=300, bbox_inches="tight")
    plt.show()
    
    #se quiser fechar ao invés de mostrar o gráfico, substitui a linha anterior por
    #plt.close()

    print(f"\nGráfico otimizado salvo em: {arquivo_grafico}")
else:
    print("\nNenhum grupo relevante para gerar o gráfico.")


# 9. SAÍDA NO TERMINAL
print("\nAgrupamento concluído com sucesso.")
print(f"Total de grupos formados: {len(df_grupos)}")
print(f"Grupos com recorrência mínima de {ocorrencia_minima}: {len(df_grupos_relevantes)}")

print(f"\nPlanilha com todos os grupos: {arquivo_grupos_todos}")
print(f"Planilha com grupos relevantes: {arquivo_grupos_relevantes}")
print(f"Gráfico de recorrência: {arquivo_grafico}")