# 🗳️ TSE Data Downloader

Pipeline automatizado em **Python** para baixar, validar, consolidar e auditar os dados públicos de **candidatos** disponibilizados pelo **Tribunal Superior Eleitoral (TSE)**.  
O projeto foi criado para gerar uma **base única, limpa e confiável**, reunindo as informações das últimas eleições.

## ⚙️ Estrutura do Projeto

```
├── ⚙️ .gitignore
├── 🐍 downloader.py      → Baixa e extrai os arquivos oficiais do TSE (.zip)
├── 🐍 comparador.py      → Compara as colunas entre anos e valida a consistência dos CSVs
├── 🐍 consolidar.py      → Gera os arquivos consolidados por ano e o consolidado final
├── 🐍 auditar.py         → Audita o resultado final (duplicatas, consistência, estatísticas)
└── 📄 pipeline.sh        → Executa todas as etapas automaticamente
```

## 🚀 Como Funciona

1. **Baixar dados:**  
   O script `downloader.py` baixa automaticamente os arquivos `.zip` de cada eleição disponíveis no portal de dados do TSE.

2. **Comparar colunas:**  
   `comparador.py` analisa e garante que todos os arquivos têm o mesmo conjunto mínimo de colunas essenciais (como nome, partido, cargo, etc.).

3. **Consolidar dados:**  
   `consolidar.py` extrai apenas as colunas relevantes, remove duplicatas idênticas e gera um arquivo final único (`consolidado_final.csv`).

4. **Auditar e validar:**  
   `auditar.py` realiza verificações de integridade, busca por duplicações e confirma a padronização da base consolidada.

## 🧠 Objetivo

Criar uma base de dados simplificada e fidedigna com:

- Lista dos **partidos políticos** participantes nas últimas eleições.
- Lista completa de **candidatos**, com dados pessoais públicos, cargos, partidos e situação eleitoral.

## 🧩 Execução da Pipeline Completa

Basta rodar o script bash:

```bash
chmod +x pipeline.sh
./pipeline.sh
```

Isso executará, em sequência:

- `downloader.py`
- `comparador.py`
- `consolidar.py`
- `auditar.py`

## 🧹 Resultado Final

O pipeline gera o arquivo:

```
📦 consolidado_final.csv
```

Com as colunas padronizadas:

- ANO_ELEICAO
- SG_UF
- NM_CANDIDATO
- NM_URNA_CANDIDATO
- DS_CARGO
- SG_PARTIDO
- NR_PARTIDO
- NM_PARTIDO
- DS_OCUPACAO
- DS_SIT_TOT_TURNO
- DT_NASCIMENTO
- DS_GRAU_INSTRUCAO
- DS_ESTADO_CIVIL
- DT_GERACAO
- HH_GERACAO

## 🧾 Licença

Este projeto utiliza apenas **dados públicos do TSE**, disponíveis sob acesso aberto em:
[https://dadosabertos.tse.jus.br](https://dadosabertos.tse.jus.br)

O código deste repositório é distribuído sob a **licença MIT** — uso livre, com citação.

## 👨‍💻 Autor

**Matheus Felizardo**  
Criação e desenvolvimento da pipeline de consolidação de dados eleitorais.  
📅 Última atualização: **28 de outubro de 2025**
🤖 Scripts criados com auxílio de IA (OpenAI)

> “Transparência e dados abertos são pilares da democracia.”
