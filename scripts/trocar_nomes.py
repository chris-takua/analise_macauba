from pathlib import Path
import re
import shutil  # Biblioteca para copiar arquivos

# 1. CONFIGURAÇÃO DE CAMINHOS
caminho_base = Path(r"C:\Users\Chris\Dropbox\Doutorado\modal_cachos\analise_modal_araponga")

# Origem: pasta com nomes em MAIÚSCULO
pasta_origem = caminho_base / "dados" / "experimento_analise_modal_26022026"

# Destino: Nova pasta apenas para conferência (será criada pelo script)
pasta_conferencia = caminho_base / "dados" / "conferencia_renomeados"
pasta_conferencia.mkdir(parents=True, exist_ok=True)

# 2. PARÂMETROS DE RENOMEAÇÃO
offset_c = 15  # Começa do 16 (15 já existentes + 1)

# Padrao para identificar CxPyRz (independente de ser maiúsculo ou minúsculo)
padrao = re.compile(r'^(c)(\d+)(p)(\d+)(r)(\d+)(.*)$', re.IGNORECASE)

# 3. PROCESSAMENTO
arquivos = list(pasta_origem.glob("*.txt"))
print(f"Processando {len(arquivos)} arquivos...\n")

for arq_path in arquivos:
    nome_original = arq_path.name
    match = padrao.match(nome_original)
    
    if match:
        # Extração dos números originais
        c_num = int(match.group(2))
        p_num = int(match.group(4))
        r_num = int(match.group(6))
        extensao = match.group(7)
        
        # Cálculo do novo nome (Ex: C1 -> c16)
        novo_nome = f"c{c_num + offset_c}p{p_num}r{r_num}{extensao}".lower()
        
        # Caminho completo de onde o novo arquivo será salvo
        caminho_destino = pasta_conferencia / novo_nome
        
        # Executa a cópia
        shutil.copy2(arq_path, caminho_destino)
        print(f"Copiado: {nome_original} -> {novo_nome}")
    else:
        print(f"⚠️ Ignorado (fora do padrão): {nome_original}")

print(f"\n✅ Concluído! Verifique os arquivos em: {pasta_conferencia}")