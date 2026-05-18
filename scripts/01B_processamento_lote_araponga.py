# O script varre a pasta de dados brutos automaticamente.
# Ele aplica a limpeza de colunas redundantes em cada um.
# Salva os r resultados organizados nas pastas pretratados_araponga e graficos_araponga.
# Você terá  um histórico visual (PNG) e um banco de dados limpo (CSV) para cada ensai

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# 1. CONFIGURAÇÃO DE CAMINHOS
caminho_base = Path(r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga")
pasta_entrada = caminho_base / "dados" / "Chris_Araponga"
pasta_pretratados = caminho_base / "dados" / "pretratados_araponga"
pasta_graficos = caminho_base / "resultados" / "graficos_araponga"

# 2. CRIAR PASTAS DE SAÍDA
pasta_pretratados.mkdir(parents=True, exist_ok=True)
pasta_graficos.mkdir(parents=True, exist_ok=True)

# 3. LISTAR TODOS OS ARQUIVOS .TXT NA PASTA
arquivos_txt = list(pasta_entrada.glob("*.txt"))
total = len(arquivos_txt)

print(f"Encontrados {total} arquivos para processamento.\n")

# 4. LOOP DE PROCESSAMENTO
for i, arquivo_path in enumerate(arquivos_txt, 1):
    nome_base = arquivo_path.stem
    print(f"[{i}/{total}] Processando: {nome_base}...", end=" ")

    try:
        # Leitura
        df = pd.read_csv(arquivo_path, sep="\t", decimal=",", engine="python")
        
        # Limpeza e Renomeação
        df = df.dropna(axis=1, how="all")
        df.columns = ["freq_1", "magnitude", "freq_2", "fase_graus", "freq_3", "coerencia"]
        
        for coluna in df.columns:
            df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        
        df = df.dropna()
        
        # Enxugando colunas (mantendo apenas uma frequência)
        df_limpo = df[["freq_1", "magnitude", "fase_graus", "coerencia"]].copy()
        df_limpo = df_limpo.rename(columns={"freq_1": "frequencia_hz"})

        # Salvando CSV
        caminho_csv = pasta_pretratados / f"{nome_base}_pretratado.csv"
        df_limpo.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

        # Gerando e Salvando Gráfico (sem abrir janela para não travar o loop)
        fig, axs = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
        
        axs[0].plot(df_limpo["frequencia_hz"], df_limpo["magnitude"], color="blue")
        axs[0].set_ylabel("Magnitude")
        axs[0].set_title(f"FRF - {nome_base} (Magnitude)")
        axs[0].grid(True)

        axs[1].plot(df_limpo["frequencia_hz"], df_limpo["fase_graus"], color="green")
        axs[1].set_ylabel("Fase (graus)")
        axs[1].grid(True)

        axs[2].plot(df_limpo["frequencia_hz"], df_limpo["coerencia"], color="red")
        axs[2].set_ylabel("Coerência")
        axs[2].set_xlabel("Frequência (Hz)")
        axs[2].grid(True)

        plt.tight_layout()
        caminho_png = pasta_graficos / f"{nome_base}_grafico.png"
        plt.savefig(caminho_png, dpi=150) # DPI menor para processar mais rápido no lote
        plt.close(fig) # IMPORTANTE: fecha o gráfico da memória

        print("✅ OK")

    except Exception as e:
        print(f"❌ ERRO: {e}")

print("\n🚀 Processamento concluído!")