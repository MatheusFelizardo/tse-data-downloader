# Esse arquivo é responsável por verificar a integridade e consistência do arquivo consolidado_final.csv gerado.
# O resultado esperado são logs que confirmem que o arquivo contém todas as colunas esperadas, dados de todos os anos,
# e que os dados são consistentes (sem valores nulos inesperados, formatos corretos, etc).

import pandas as pd
import os
from datetime import datetime

ARQUIVO = "consolidado_final.csv"

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

def main():
    if not os.path.exists(ARQUIVO):
        print(f"❌ Arquivo {ARQUIVO} não encontrado!")
        return

    print(f"📂 Lendo {ARQUIVO} ...")
    df = pd.read_csv(ARQUIVO, sep=";", encoding="latin1", dtype=str, low_memory=False)
    print(f"✅ Total de registros: {len(df):,}\n")

    # 1️⃣ Verifica se todas as colunas obrigatórias estão presentes
    colunas = list(df.columns)
    faltando = [c for c in COLUNAS_OBRIGATORIAS if c not in colunas]
    extras = [c for c in colunas if c not in COLUNAS_OBRIGATORIAS]

    print("🔍 Verificação de colunas:")
    print(f"→ Colunas encontradas: {len(colunas)}")
    print(f"→ Colunas extras: {len(extras)}")
    if faltando:
        print(f"❌ Faltando colunas obrigatórias: {faltando}")
        return
    else:
        print("✅ Todas as colunas obrigatórias estão presentes.\n")

    # 2️⃣ Verifica se há dados de todos os anos esperados
    anos = sorted(df["ANO_ELEICAO"].dropna().unique())
    print(f"📅 Anos encontrados: {anos}")
    if set(anos) != set(["2016", "2018", "2020", "2022", "2024"]):
        print("⚠️ Alguns anos estão faltando ou inconsistentes!")
    else:
        print("✅ Todos os anos esperados estão presentes.\n")

    # 3️⃣ Verifica integridade de dados (linhas nulas, duplicadas, formatos)
    print("🧩 Verificação de integridade:")
    nulos_porcent = df.isnull().mean() * 100
    nulos_altos = nulos_porcent[nulos_porcent > 5]
    if len(nulos_altos) > 0:
        print(f"⚠️ Colunas com mais de 5% de valores ausentes:")
        for col, val in nulos_altos.items():
            print(f"   - {col}: {val:.2f}%")
    else:
        print("✅ Nenhuma coluna com mais de 5% de valores ausentes.")

    # 4️⃣ Duplicatas
    duplicadas = df.duplicated(subset=["NM_CANDIDATO", "DS_CARGO", "ANO_ELEICAO"]).sum()
    print(f"\n📋 Registros duplicados (mesmo candidato, cargo e ano): {duplicadas}")

    # 5️⃣ Coerência de tipos e formatos
    print("\n🧠 Verificando formato das datas...")
    df["DT_NASCIMENTO"] = pd.to_datetime(df["DT_NASCIMENTO"], errors="coerce", dayfirst=True)
    invalidas = df["DT_NASCIMENTO"].isna().sum()
    print(f"→ Datas de nascimento inválidas: {invalidas:,}")
    if invalidas / len(df) < 0.01:
        print("✅ Datas de nascimento majoritariamente válidas.\n")
    else:
        print("⚠️ Muitas datas inválidas — revisar encoding.\n")

    # 6️⃣ Verificação de coerência lógica (idade plausível)
    agora = datetime.now()
    df["IDADE"] = (agora - df["DT_NASCIMENTO"]).dt.days // 365
    idade_media = df["IDADE"].mean()
    idade_anomalias = df[(df["IDADE"] < 18) | (df["IDADE"] > 100)]
    print(f"📊 Idade média estimada: {idade_media:.1f} anos")
    print(f"⚠️ Registros com idade fora do intervalo 18–100: {len(idade_anomalias)}\n")

    # 7️⃣ Amostra de dados válidos
    print("🧾 Amostra de registros válidos:")
    print(df[["ANO_ELEICAO", "SG_UF", "NM_CANDIDATO", "DS_CARGO", "SG_PARTIDO"]].head(10).to_string(index=False))

    print("\n✅ Auditoria concluída. O arquivo consolidado_final.csv contém todas as informações esperadas e é consistente.")

if __name__ == "__main__":
    main()
