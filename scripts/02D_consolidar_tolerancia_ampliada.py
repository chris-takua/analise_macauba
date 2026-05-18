import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. CAMINHOS
caminho_base = Path(r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga")
arquivo_picos = caminho_base / "resultados" / "planilhas_araponga" / "todos_os_picos_araponga.csv"
pasta_saida = caminho_base / "resultados" / "planilhas_araponga"
pasta_graficos = caminho_base / "resultados" / "picos_araponga"

# 2. PARÂMETROS (AJUSTE D: MAIOR TOLERÂNCIA PARA VARIABILIDADE)
tolerancia_hz = 2.0    # Aumentamos para unir modos próximos
ocorrencia_minima = 6 

# 3. LEITURA E AGRUPAMENTO
df = pd.read_csv(arquivo_picos).sort_values("frequencia_hz").reset_index(drop=True)
grupos = []
grupo_atual = []

for _, linha in df.iterrows():
    frequencia = linha["frequencia_hz"]
    if not grupo_atual:
        grupo_atual.append(linha.to_dict())
    else:
        centro_grupo = sum([item["frequencia_hz"] for item in grupo_atual]) / len(grupo_atual)
        if abs(frequencia - centro_grupo) <= tolerancia_hz:
            grupo_atual.append(linha.to_dict())
        else:
            grupos.append(grupo_atual)
            grupo_atual = [linha.to_dict()]
if grupo_atual: grupos.append(grupo_atual)

# 4. PROCESSAMENTO DOS GRUPOS
lista_grupos = []
for i, grupo in enumerate(grupos, 1):
    dg = pd.DataFrame(grupo)
    lista_grupos.append({
        "grupo_modal": i,
        "freq_media": dg["frequencia_hz"].mean(),
        "n_ocorrencias": len(dg),
        "coerencia_media": dg["coerencia"].mean()
    })
df_grupos = pd.DataFrame(lista_grupos)
df_relevantes = df_grupos[df_grupos["n_ocorrencias"] >= ocorrencia_minima].copy()

# 5. SALVAMENTO (Versão D)
df_relevantes.to_csv(pasta_saida / "grupos_relevantes_AJUSTE_D.csv", index=False, encoding="utf-8-sig")

# 6. GRÁFICO OTIMIZADO
if not df_relevantes.empty:
    df_plot = df_relevantes.nlargest(15, 'n_ocorrencias').sort_values('freq_media')
    plt.figure(figsize=(12, 6))
    barras = plt.bar(df_plot["freq_media"].round(2).astype(str), df_plot["n_ocorrencias"], color="darkorange")
    plt.bar_label(barras, padding=3)
    plt.xticks(rotation=45, ha='right')
    plt.title(f"Ajuste D: Tolerância Ampliada {tolerancia_hz}Hz (Mínimo {ocorrencia_minima})")
    plt.ylabel("Nº de Arquivos")
    plt.tight_layout()
    plt.savefig(pasta_graficos / "recorrencia_AJUSTE_D.png", dpi=300)
    plt.show()