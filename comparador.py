# Arquivo responsável por verificar se dentro dos ZIPs baixados existem os arquivos _BRASIL
# e se estes arquivos possuem todas as colunas obrigatórias setadas em COLUNAS_OBRIGATORIAS.
# O resultado esperado é a extração dos arquivos _BRASIL para a pasta consolidados_tse.

import os
import zipfile
import pandas as pd
from pathlib import Path

BASE_DIR = "dados_tse"
DESTINO_DIR = "consolidados_tse"
ANOS = [2016, 2018, 2020, 2022, 2024]

COLUNAS_OBRIGATORIAS = [
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

Path(DESTINO_DIR).mkdir(exist_ok=True)

def verificar_e_extrair(ano):
    zip_path = os.path.join(BASE_DIR, f"consulta_cand_{ano}.zip")
    if not os.path.exists(zip_path):
        print(f"❌ {ano}: arquivo ZIP não encontrado.")
        return False

    with zipfile.ZipFile(zip_path, "r") as z:
        arquivos = [n for n in z.namelist() if "_BRASIL" in n and n.lower().endswith(".csv")]
        if not arquivos:
            print(f"⚠️  {ano}: não há arquivo _BRASIL no ZIP.")
            return False

        nome_arquivo = arquivos[0]
        print(f"\n📘 {ano}: verificando {nome_arquivo}")

        with z.open(nome_arquivo) as f:
            df = pd.read_csv(f, sep=";", encoding="latin1", nrows=1, dtype=str)

        colunas = set(df.columns)
        faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in colunas]

        if faltando:
            print(f"❌ {ano}: faltam colunas obrigatórias → {faltando}")
            return False

        print(f"✅ {ano}: o arquivo possui todas as colunas obrigatórias.")

        destino_csv = os.path.join(DESTINO_DIR, f"consulta_cand_{ano}_BRASIL.csv")
        with z.open(nome_arquivo) as f_in, open(destino_csv, "wb") as f_out:
            f_out.write(f_in.read())
        print(f"📦 Extraído para {destino_csv}")

    return True

if __name__ == "__main__":
    for ano in ANOS:
        sucesso = verificar_e_extrair(ano)
        if not sucesso:
            print(f"\n⛔ Interrompendo execução — erro encontrado no ano {ano}.")
            break
    else:
        print("\n✅ Todos os arquivos _BRASIL foram verificados e extraídos com sucesso!")
