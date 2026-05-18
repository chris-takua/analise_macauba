import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. CAMINHOS PRINCIPAIS
caminho_base = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga"
)

pasta_entrada = caminho_base / "dados" / "pretratados_araponga"
pasta_graficos_picos = caminho_base / "resultados" / "picos_araponga"
pasta_planilhas = caminho_base / "resultados" / "planilhas_araponga"


# 2. CRIAR PASTAS DE SAÍDA
pasta_graficos_picos.mkdir(parents=True, exist_ok=True)
pasta_planilhas.mkdir(parents=True, exist_ok=True)


# 3. PARÂMETROS DE DETECÇÃO
coerencia_minima = 0.80
magnitude_minima = 0.01
frequencia_minima = 1.0
frequencia_maxima = 300.0


# 4. LISTAR ARQUIVOS DE ENTRADA
arquivos_csv = list(pasta_entrada.glob("*.csv"))
total_arquivos = len(arquivos_csv)

print(f"\nTotal de arquivos pré-tratados encontrados: {total_arquivos}")


# 5. LISTAS PARA ARMAZENAR RESULTADOS
lista_todos_picos = []
lista_resumo = []


# 6. LOOP PRINCIPAL
for indice_arquivo, arquivo_csv in enumerate(arquivos_csv, start=1):
    nome_arquivo = arquivo_csv.stem

    print(f"\n[{indice_arquivo}/{total_arquivos}] Processando: {nome_arquivo}")

    df = pd.read_csv(arquivo_csv)

    # Garantir que as colunas esperadas existem
    colunas_esperadas = ["frequencia_hz", "magnitude", "fase_graus", "coerencia"]
    if not all(coluna in df.columns for coluna in colunas_esperadas):
        print(f"Arquivo ignorado: colunas incompatíveis em {nome_arquivo}")
        continue

    # Filtro de faixa
    df = df[
        (df["frequencia_hz"] >= frequencia_minima) &
        (df["frequencia_hz"] <= frequencia_maxima)
    ].copy()

    df = df.dropna().reset_index(drop=True)

    if len(df) < 3:
        print(f"Arquivo ignorado: poucos pontos após filtragem em {nome_arquivo}")
        continue

    # Indicadores gerais do arquivo
    coerencia_media = df["coerencia"].mean()
    coerencia_maxima = df["coerencia"].max()
    magnitude_maxima = df["magnitude"].max()

    # Detectar picos
    picos_arquivo = []

    for i in range(1, len(df) - 1):
        freq_atual = df.loc[i, "frequencia_hz"]
        mag_atual = df.loc[i, "magnitude"]
        fase_atual = df.loc[i, "fase_graus"]
        coer_atual = df.loc[i, "coerencia"]

        mag_anterior = df.loc[i - 1, "magnitude"]
        mag_posterior = df.loc[i + 1, "magnitude"]

        eh_pico_local = (mag_atual > mag_anterior) and (mag_atual > mag_posterior)
        passa_coerencia = coer_atual >= coerencia_minima
        passa_magnitude = mag_atual >= magnitude_minima

        if eh_pico_local and passa_coerencia and passa_magnitude:
            picos_arquivo.append({
                "arquivo": nome_arquivo,
                "frequencia_hz": freq_atual,
                "magnitude": mag_atual,
                "coerencia": coer_atual,
                "fase_graus": fase_atual
            })

    df_picos = pd.DataFrame(picos_arquivo)

    # Se não houver picos válidos
    if df_picos.empty:
        lista_resumo.append({
            "arquivo": nome_arquivo,
            "n_picos": 0,
            "primeiro_pico_hz": None,
            "segundo_pico_hz": None,
            "pico_principal_hz": None,
            "mag_primeiro_pico": None,
            "mag_segundo_pico": None,
            "mag_pico_principal": None,
            "coer_primeiro_pico": None,
            "coer_segundo_pico": None,
            "coer_pico_principal": None,
            "fase_primeiro_pico": None,
            "fase_segundo_pico": None,
            "fase_pico_principal": None,
            "coerencia_media_faixa": coerencia_media,
            "coerencia_maxima_faixa": coerencia_maxima,
            "magnitude_maxima_faixa": magnitude_maxima
        })

        print("Nenhum pico válido encontrado com os critérios atuais.")
        continue

    # Ordenação por frequência para identificar primeiro e segundo pico
    df_picos_freq = df_picos.sort_values(by="frequencia_hz").reset_index(drop=True)

    # Ordenação por magnitude para identificar pico principal
    df_picos_mag = df_picos.sort_values(by="magnitude", ascending=False).reset_index(drop=True)

    # Primeiro pico
    primeiro_pico = df_picos_freq.iloc[0]

    # Segundo pico
    if len(df_picos_freq) >= 2:
        segundo_pico = df_picos_freq.iloc[1]
    else:
        segundo_pico = None

    # Pico principal
    pico_principal = df_picos_mag.iloc[0]

    # Salvar todos os picos em lista geral
    for ordem, (_, linha) in enumerate(df_picos_freq.iterrows(), start=1):
        lista_todos_picos.append({
            "arquivo": nome_arquivo,
            "ordem_pico_em_frequencia": ordem,
            "frequencia_hz": linha["frequencia_hz"],
            "magnitude": linha["magnitude"],
            "coerencia": linha["coerencia"],
            "fase_graus": linha["fase_graus"]
        })

    # Montar resumo do arquivo
    lista_resumo.append({
        "arquivo": nome_arquivo,
        "n_picos": len(df_picos_freq),
        "primeiro_pico_hz": primeiro_pico["frequencia_hz"],
        "segundo_pico_hz": segundo_pico["frequencia_hz"] if segundo_pico is not None else None,
        "pico_principal_hz": pico_principal["frequencia_hz"],
        "mag_primeiro_pico": primeiro_pico["magnitude"],
        "mag_segundo_pico": segundo_pico["magnitude"] if segundo_pico is not None else None,
        "mag_pico_principal": pico_principal["magnitude"],
        "coer_primeiro_pico": primeiro_pico["coerencia"],
        "coer_segundo_pico": segundo_pico["coerencia"] if segundo_pico is not None else None,
        "coer_pico_principal": pico_principal["coerencia"],
        "fase_primeiro_pico": primeiro_pico["fase_graus"],
        "fase_segundo_pico": segundo_pico["fase_graus"] if segundo_pico is not None else None,
        "fase_pico_principal": pico_principal["fase_graus"],
        "coerencia_media_faixa": coerencia_media,
        "coerencia_maxima_faixa": coerencia_maxima,
        "magnitude_maxima_faixa": magnitude_maxima
    })

    # Gráfico com picos marcados
    plt.figure(figsize=(12, 6))
    plt.plot(df["frequencia_hz"], df["magnitude"], color="blue", label="Magnitude da FRF")
    plt.scatter(df_picos_freq["frequencia_hz"], df_picos_freq["magnitude"], color="red", label="Picos válidos", zorder=3)

    for _, linha in df_picos_freq.iterrows():
        plt.text(
            linha["frequencia_hz"],
            linha["magnitude"],
            f'{linha["frequencia_hz"]:.2f} Hz',
            fontsize=8,
            ha="left",
            va="bottom"
        )

    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Magnitude")
    plt.title(f"Picos candidatos - {nome_arquivo}")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    caminho_grafico = pasta_graficos_picos / f"{nome_arquivo}_picos.png"
    plt.savefig(caminho_grafico, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Picos válidos encontrados: {len(df_picos_freq)}")


# 7. SALVAR PLANILHAS FINAIS
df_todos_picos = pd.DataFrame(lista_todos_picos)
df_resumo = pd.DataFrame(lista_resumo)

arquivo_todos_picos = pasta_planilhas / "todos_os_picos_araponga.csv"
arquivo_resumo = pasta_planilhas / "resumo_frequencias_principais_araponga.csv"

df_todos_picos.to_csv(arquivo_todos_picos, index=False, encoding="utf-8-sig")
df_resumo.to_csv(arquivo_resumo, index=False, encoding="utf-8-sig")


# 8. MENSAGEM FINAL
print("\nProcessamento concluído com sucesso.")
print(f"Planilha de todos os picos: {arquivo_todos_picos}")
print(f"Planilha resumo: {arquivo_resumo}")
print(f"Gráficos com picos: {pasta_graficos_picos}")