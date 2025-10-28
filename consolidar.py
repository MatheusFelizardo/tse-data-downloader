# Esse arquivo é responsável por consolidar os arquivos CSV baixados e normalizados em um único arquivo final.
# O resultado esperado é a criação do arquivo 'consolidado_final.csv' contendo todos os dados consolidados e sem duplicatas.

import os
import pandas as pd
from pathlib import Path

# Pastas
CONSOLIDADOS_DIR = "consolidados_tse"
ARQUIVO_FINAL = "consolidado_final.csv"

COLUNAS_PADRAO = [
    "ANO_ELEICAO",
    "SG_UF",
    "NM_CANDIDATO",
    "NM_URNA_CANDIDATO",
    "DS_CARGO",
    "SG_PARTIDO",
    "NR_PARTIDO",
    "NM_PARTIDO",
    "DS_OCUPACAO",
    "DS_SIT_TOT_TURNO",
    "DT_NASCIMENTO",
    "DS_GRAU_INSTRUCAO",
    "DS_ESTADO_CIVIL",
    "DT_GERACAO",
    "HH_GERACAO"
]

Path(CONSOLIDADOS_DIR).mkdir(exist_ok=True)

def carregar_e_normalizar(caminho_csv):
    """Carrega o CSV, mantém apenas colunas padrão, remove duplicatas e garante consistência."""
    try:
        df = pd.read_csv(caminho_csv, sep=";", encoding="latin1", dtype=str, low_memory=False)
    except Exception as e:
        print(f"❌ Erro ao ler {caminho_csv}: {e}")
        return None

    # Normaliza colunas: garante que todas existam
    for col in COLUNAS_PADRAO:
        if col not in df.columns:
            df[col] = None

    df = df[COLUNAS_PADRAO]

    # Remove duplicatas 100% idênticas
    linhas_antes = len(df)
    df = df.drop_duplicates(subset=df.columns.tolist(), keep="first")
    removidas = linhas_antes - len(df)
    if removidas > 0:
        print(f"⚠️  {removidas:,} duplicatas removidas em {os.path.basename(caminho_csv)}")

    return df

def main():
    arquivos = [f for f in os.listdir(CONSOLIDADOS_DIR) if f.endswith("_BRASIL.csv")]
    if not arquivos:
        print(f"❌ Nenhum arquivo encontrado em {CONSOLIDADOS_DIR}.")
        return

    todos_dfs = []
    total_removidas = 0
    total_linhas = 0

    for nome in sorted(arquivos):
        caminho = os.path.join(CONSOLIDADOS_DIR, nome)
        print(f"📥 Lendo {nome}...")
        df = carregar_e_normalizar(caminho)
        if df is not None:
            total_linhas += len(df)
            todos_dfs.append(df)
            print(f"✅ {len(df):,} linhas adicionadas.\n")

    if not todos_dfs:
        print("❌ Nenhum dado foi carregado com sucesso.")
        return

    consolidado = pd.concat(todos_dfs, ignore_index=True)

    # Verificação final: remover duplicatas globais (entre anos)
    linhas_antes = len(consolidado)
    consolidado = consolidado.drop_duplicates(subset=COLUNAS_PADRAO, keep="first")
    total_removidas = linhas_antes - len(consolidado)

    consolidado.to_csv(ARQUIVO_FINAL, sep=";", index=False, encoding="latin1")

    print("\n✅ Consolidação concluída com sucesso!")
    print(f"📦 Arquivo final salvo em: {ARQUIVO_FINAL}")
    print(f"📊 Total de registros: {len(consolidado):,}")
    print(f"🧹 Duplicatas globais removidas: {total_removidas:,}")

if __name__ == "__main__":
    main()
