#!/usr/bin/env python3
"""
Script para preparar commit do Assistente Niara
"""

import os
import sys
import subprocess
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def check_git():
    """Verificar se é um repositório Git"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Repositório Git encontrado")
            return True
        else:
            print("❌ Não é um repositório Git")
            return False
    except FileNotFoundError:
        print("❌ Git não instalado")
        return False

def check_files():
    """Verificar arquivos necessários para deploy"""
    required_files = [
        "klona_agent.py",
        "requirements.txt",
        "Dockerfile",
        "render.yaml"
    ]
    
    missing_files = []
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Arquivos faltando: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Todos os arquivos necessários encontrados")
        return True

def check_docs():
    """Verificar pasta docs"""
    docs_path = Path("../docs")
    if docs_path.exists():
        pdf_count = len(list(docs_path.glob("*.pdf")))
        print(f"✅ Pasta docs encontrada com {pdf_count} PDFs")
        return True
    else:
        print("⚠️ Pasta docs não encontrada")
        return False

def create_gitignore():
    """Criar .gitignore se não existir"""
    gitignore_path = Path(".gitignore")
    
    if not gitignore_path.exists():
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Environment variables
.env
.env.local
.env.production

# Database
*.db
*.sqlite3

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Render
.render/
"""
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        print("✅ .gitignore criado")
    else:
        print("✅ .gitignore já existe")

def prepare_commit():
    """Preparar arquivos para commit"""
    print("📦 Preparando arquivos para commit...")
    
    # Copiar docs se necessário
    docs_source = Path("../docs")
    docs_target = Path("docs")
    
    if docs_source.exists() and not docs_target.exists():
        import shutil
        shutil.copytree(docs_source, docs_target)
        print("✅ Pasta docs copiada")
    
    return True

def show_commit_commands():
    """Mostrar comandos para commit"""
    print("\n" + "="*60)
    print("📝 COMANDOS PARA COMMIT E PUSH")
    print("="*60)
    
    print("\n1. 📁 Adicionar arquivos:")
    print("   git add .")
    
    print("\n2. 💾 Fazer commit:")
    print('   git commit -m "Deploy Assistente Niara para Render"')
    
    print("\n3. 🚀 Fazer push:")
    print("   git push origin main")
    
    print("\n4. 🌐 Deploy no Render:")
    print("   • Acesse: https://dashboard.render.com")
    print("   • New + → Web Service")
    print("   • Conecte seu repositório")
    print("   • Configure variáveis de ambiente")
    print("   • Deploy automático")

def main():
    print("🤖 Preparando Assistente Niara para Deploy")
    print("="*50)
    
    # Verificações
    if not check_git():
        print("\n❌ Configure o Git primeiro:")
        print("git init")
        print("git remote add origin https://github.com/seu-usuario/seu-repo.git")
        return
    
    if not check_files():
        print("\n❌ Arquivos necessários não encontrados!")
        return
    
    check_docs()
    create_gitignore()
    
    print("\n📋 Verificações concluídas!")
    
    # Preparar commit
    if not prepare_commit():
        print("\n❌ Erro ao preparar commit!")
        return
    
    print("\n✅ Arquivos preparados para commit!")
    show_commit_commands()

if __name__ == "__main__":
    main()
