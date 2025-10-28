# Arquivo responsável por baixar os dados do TSE
# O resultado esperado é a criação da pasta dados_tse com os arquivos ZIP baixados
# Você pode setar os anos desejados na lista ANOS

import os
import io
import zipfile
import requests
import pandas as pd
from tqdm import tqdm 

ANOS = [2016, 2018, 2020, 2022, 2024]
BASE_DIR = "dados_tse"
os.makedirs(BASE_DIR, exist_ok=True)

CAMPOS_IMPORTANTES = [
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

def baixar_arquivo_tse(ano):
    """Baixa o ZIP de consulta_cand_ano do TSE com barra de progresso."""
    url_zip = f"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip"
    local_path = os.path.join(BASE_DIR, f"consulta_cand_{ano}.zip")
    print(f"\n⬇️ Baixando {url_zip} ...")

    with requests.get(url_zip, stream=True) as r:
        if r.status_code != 200:
            print(f"❌ Falha ao baixar {ano} ({r.status_code})")
            return None

        total = int(r.headers.get("content-length", 0))
        with open(local_path, "wb") as f, tqdm(
            total=total, unit='B', unit_scale=True, unit_divisor=1024
        ) as bar:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

    print(f"✅ Arquivo salvo: {local_path}")
    return local_path

def extrair_csvs(zip_path):
    """Extrai todos os CSVs do ZIP (um por estado)."""
    dfs = []
    with zipfile.ZipFile(zip_path, "r") as z:
        for nome in z.namelist():
            if nome.lower().endswith(".csv"):
                with z.open(nome) as f:
                    try:
                        df = pd.read_csv(f, sep=";", encoding="latin1", dtype=str)
                        df["ARQUIVO_ORIGEM"] = os.path.basename(zip_path)
                        dfs.append(df)
                    except Exception as e:
                        print(f"Erro ao ler {nome}: {e}")
    return dfs

def consolidar_dados():
    """Baixa, extrai e consolida todos os anos."""
    todos = []
    for ano in ANOS:
        zip_path = baixar_arquivo_tse(ano)
        if zip_path:
            dfs = extrair_csvs(zip_path)
            for df in dfs:
                cols = [c for c in CAMPOS_IMPORTANTES if c in df.columns]
                df = df[cols]
                df["ANO_ELEICAO"] = ano
                todos.append(df)

    if not todos:
        print("Nenhum dado foi carregado.")
        return

    df_final = pd.concat(todos, ignore_index=True)
    out_path = os.path.join(BASE_DIR, "consulta_candidatos_consolidado.csv")
    df_final.to_csv(out_path, index=False, sep=";")
    print(f"\n✅ Base consolidada salva em: {out_path}")
    print(f"Total de registros: {len(df_final):,}")

if __name__ == "__main__":
    consolidar_dados()
