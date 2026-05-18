import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. ARQUIVO DE ENTRADA
arquivo_entrada = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga\dados\Chris_Araponga\c1p1r1.txt"
)


# 2. PASTAS DE SAÍDA
pasta_pretratados_araponga = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga\dados\pretratados_araponga"
)

pasta_graficos_araponga = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga\resultados\graficos_araponga"
)


# 3. CRIAR PASTAS, SE NECESSÁRIO
pasta_pretratados_araponga.mkdir(parents=True, exist_ok=True)
pasta_graficos_araponga.mkdir(parents=True, exist_ok=True)


# 4. LER O ARQUIVO BRUTO
df = pd.read_csv(
    arquivo_entrada,
    sep="\t",
    decimal=",",
    engine="python"
)


# 5. REMOVER COLUNAS VAZIAS
df = df.dropna(axis=1, how="all")


# 6. RENOMEAR COLUNAS
df.columns = [
    "freq_1",
    "magnitude",
    "freq_2",
    "fase_graus",
    "freq_3",
    "coerencia"
]


# 7. CONVERTER PARA NÚMERO
for coluna in df.columns:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")


# 8. REMOVER LINHAS INVÁLIDAS
df = df.dropna()


# 9. VERIFICAR SE AS COLUNAS DE FREQUÊNCIA SÃO IGUAIS
freq_12_iguais = (df["freq_1"] == df["freq_2"]).all()
freq_13_iguais = (df["freq_1"] == df["freq_3"]).all()

print("\nVerificação das frequências redundantes:")
print(f"freq_1 == freq_2 -> {freq_12_iguais}")
print(f"freq_1 == freq_3 -> {freq_13_iguais}")


# 10. MANTER APENAS AS COLUNAS ÚTEIS
df_limpo = df[["freq_1", "magnitude", "fase_graus", "coerencia"]].copy()
df_limpo = df_limpo.rename(columns={"freq_1": "frequencia_hz"})


# 11. MOSTRAR AMOSTRA NO TERMINAL
print("\nPrimeiras linhas do arquivo pré-tratado:")
print(df_limpo.head())

print("\nInformações gerais:")
print(df_limpo.info())


# 12. DEFINIR NOMES DE SAÍDA
nome_base = arquivo_entrada.stem

arquivo_csv_saida = pasta_pretratados_araponga / f"{nome_base}_pretratado.csv"
arquivo_png_saida = pasta_graficos_araponga / f"{nome_base}_frf.png"

print("\nDiagnóstico de caminhos:")
print(f"Arquivo de entrada existe? {arquivo_entrada.exists()}")
print(f"Pasta pretratados: {pasta_pretratados_araponga}")
print(f"Pasta pretratados existe? {pasta_pretratados_araponga.exists()}")
print(f"Pasta gráficos: {pasta_graficos_araponga}")
print(f"Pasta gráficos existe? {pasta_graficos_araponga.exists()}")
print(f"Caminho final do CSV: {arquivo_csv_saida}")
print(f"Caminho final do PNG: {arquivo_png_saida}")

# 13. SALVAR CSV PRÉ-TRATADO
df_limpo.to_csv(arquivo_csv_saida, index=False, encoding="utf-8-sig")

print(f"CSV existe após salvar? {arquivo_csv_saida.exists()}")

# 14. GERAR E SALVAR GRÁFICO
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axs[0].plot(df_limpo["frequencia_hz"], df_limpo["magnitude"], color="blue")
axs[0].set_ylabel("Magnitude")
axs[0].set_title("FRF - Magnitude")
axs[0].grid(True)

axs[1].plot(df_limpo["frequencia_hz"], df_limpo["fase_graus"], color="green")
axs[1].set_ylabel("Fase (graus)")
axs[1].set_title("FRF - Fase")
axs[1].grid(True)

axs[2].plot(df_limpo["frequencia_hz"], df_limpo["coerencia"], color="red")
axs[2].set_ylabel("Coerência")
axs[2].set_xlabel("Frequência (Hz)")
axs[2].set_title("FRF - Coerência")
axs[2].grid(True)

plt.tight_layout()
plt.savefig(arquivo_png_saida, dpi=300, bbox_inches="tight")
plt.show()


# 15. CONFIRMAÇÃO FINAL
print("\nArquivos gerados com sucesso:")
print(f"CSV pré-tratado: {arquivo_csv_saida}")
print(f"Gráfico salvo: {arquivo_png_saida}")