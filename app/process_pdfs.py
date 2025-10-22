import os
import sys
import glob
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv(dotenv_path='../.env')

print("📚 Processando PDFs da pasta docs...")

# Configurar embedder
embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",
)

# Configurar banco vetorial
vector_db = ChromaDb(
    collection="klona_knowledge",
    embedder=embedder,
)

# Criar sistema de conhecimento
knowledge = Knowledge(
    vector_db=vector_db,
)

# Caminho para a pasta docs
docs_path = Path("../docs")

# Verificar se a pasta docs existe
if not docs_path.exists():
    print("❌ Pasta 'docs' não encontrada!")
    print("Crie a pasta 'docs' na raiz do projeto e coloque seus PDFs lá.")
    sys.exit(1)

# Buscar todos os PDFs na pasta docs
pdf_files = list(docs_path.glob("*.pdf"))

if not pdf_files:
    print("❌ Nenhum arquivo PDF encontrado na pasta 'docs'!")
    print("Coloque seus arquivos PDF na pasta 'docs' e execute novamente.")
    sys.exit(1)

print(f"📄 Encontrados {len(pdf_files)} arquivos PDF:")
for pdf in pdf_files:
    print(f"   • {pdf.name}")

print("\n🔄 Processando PDFs...")

# Processar cada PDF
for i, pdf_file in enumerate(pdf_files, 1):
    print(f"\n📄 Processando {i}/{len(pdf_files)}: {pdf_file.name}")
    
    try:
        # Extrair nome do arquivo sem extensão para usar como nome
        file_name = pdf_file.stem
        
        # Adicionar PDF à base de conhecimento
        knowledge.add_content(
            path=str(pdf_file),
            name=file_name,
            description=f"Documento PDF: {file_name}",
            metadata={
                "tipo": "pdf",
                "categoria": "documento",
                "arquivo": pdf_file.name,
                "processado": "sim"
            }
        )
        
        print(f"✅ {pdf_file.name} processado com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao processar {pdf_file.name}: {e}")
        continue

print(f"\n🎯 Processamento concluído!")
print(f"📚 Total de PDFs processados: {len(pdf_files)}")
print("\n🚀 Próximos passos:")
print("1. Reinicie o agente para carregar os novos documentos")
print("2. Faça perguntas sobre o conteúdo dos PDFs")
print("3. O agente usará automaticamente a base de conhecimento!")

print(f"\n📋 PDFs processados:")
for pdf in pdf_files:
    print(f"   • {pdf.name}")
