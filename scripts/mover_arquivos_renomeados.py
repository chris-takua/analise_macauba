from pathlib import Path
import shutil

# 1. CONFIGURAÇÃO DE CAMINHOS
caminho_base = Path(r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga")

# Origem: onde estão os arquivos que você acabou de conferir
pasta_conferencia = caminho_base / "dados" / "conferencia_renomeados"

# Destino Final: sua pasta principal de análise
pasta_destino = caminho_base / "dados" / "Chris_Araponga"

# 2. EXECUÇÃO DA INTEGRAÇÃO
arquivos_para_mover = list(pasta_conferencia.glob("*.txt"))

print(f"Iniciando a integração de {len(arquivos_para_mover)} arquivos...\n")

for arq_origem in arquivos_para_mover:
    # Definimos o caminho de destino final (Pasta Principal + Nome do Arquivo)
    arq_destino = pasta_destino / arq_origem.name
    
    # Verificação de segurança: não sobrescrever se o arquivo já existir no destino
    if not arq_destino.exists():
        shutil.move(arq_origem, arq_destino)
        print(f"✅ Integrado: {arq_origem.name}")
    else:
        print(f"⚠️ Atenção: {arq_origem.name} já existe na pasta de destino. Pulado.")

print(f"\nIntegração concluída. Os arquivos agora estão em: {pasta_destino}")