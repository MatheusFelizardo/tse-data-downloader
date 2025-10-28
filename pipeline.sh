#!/bin/bash
set -e 

echo "🚀 Iniciando pipeline do TSE..."

echo ""
echo "📥 Etapa 1: Download dos dados..."
python3 downloader.py

echo ""
echo "🧩 Etapa 2: Comparação das colunas..."
python3 comparador.py

echo ""
echo "🧱 Etapa 3: Consolidação dos arquivos..."
python3 consolidar.py

echo ""
echo "🧾 Etapa 4: Auditoria dos dados..."
python3 auditar.py

echo ""
echo "✅ Pipeline concluída com sucesso!"
