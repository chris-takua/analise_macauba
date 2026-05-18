import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# 1. CAMINHO DO ARQUIVO
arquivo = Path(
    r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga\dados\Chris_Araponga\C1P1R1.txt"
)


# 2. LEITURA DO ARQUIVO
df = pd.read_csv(
    arquivo,
    sep="\t",
    decimal=",",
    engine="python"
)


# 3. REMOVER COLUNAS VAZIAS
df = df.dropna(axis=1, how="all")


# 4. RENOMEAR COLUNAS ORIGINAIS
df.columns = [
    "freq_1",
    "magnitude",
    "freq_2",
    "fase_graus",
    "freq_3",
    "coerencia"
]


# 5. CONVERTER TUDO PARA NÚMERO
for coluna in df.columns:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")


# 6. REMOVER LINHAS INVÁLIDAS
df = df.dropna()


# 7. CRIAR DATAFRAME ENXUTO
df = df[["freq_1", "magnitude", "fase_graus", "coerencia"]].copy()
df = df.rename(columns={"freq_1": "frequencia_hz"})


# 8. MOSTRAR PRIMEIRAS LINHAS
print("\nPrimeiras linhas do arquivo:")
print(df.head())

print("\nInformações gerais:")
print(df.info())


# 9. VERIFICAR SE AS FREQUÊNCIAS SÃO IGUAIS
# (opcional, mas útil neste estágio)
# Se quiser, você pode manter esta checagem no script inicial.
df_verificacao = pd.read_csv(
    arquivo,
    sep="\t",
    decimal=",",
    engine="python"
)
df_verificacao = df_verificacao.dropna(axis=1, how="all")
df_verificacao.columns = ["freq_1", "magnitude", "freq_2", "fase_graus", "freq_3", "coerencia"]

for coluna in df_verificacao.columns:
    df_verificacao[coluna] = pd.to_numeric(df_verificacao[coluna], errors="coerce")

df_verificacao = df_verificacao.dropna()

freq_12_iguais = (df_verificacao["freq_1"] == df_verificacao["freq_2"]).all()
freq_13_iguais = (df_verificacao["freq_1"] == df_verificacao["freq_3"]).all()

print("\nVerificação das colunas de frequência:")
print(f"freq_1 == freq_2 -> {freq_12_iguais}")
print(f"freq_1 == freq_3 -> {freq_13_iguais}")


# 10. PLOTAGEM
fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

axs[0].plot(df["frequencia_hz"], df["magnitude"], color="blue")
axs[0].set_ylabel("Magnitude")
axs[0].set_title("FRF - Magnitude")
axs[0].grid(True)

axs[1].plot(df["frequencia_hz"], df["fase_graus"], color="green")
axs[1].set_ylabel("Fase (graus)")
axs[1].set_title("FRF - Fase")
axs[1].grid(True)

axs[2].plot(df["frequencia_hz"], df["coerencia"], color="red")
axs[2].set_ylabel("Coerência")
axs[2].set_xlabel("Frequência (Hz)")
axs[2].set_title("FRF - Coerência")
axs[2].grid(True)

plt.tight_layout()
plt.show()