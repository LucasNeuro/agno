#!/usr/bin/env python3
"""
Script de Deploy para Render - Assistente Niara
"""

import os
import sys
import subprocess
from pathlib import Path

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
    """Verificar arquivos necessários"""
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

def check_env_example():
    """Verificar se existe exemplo de .env"""
    env_example = Path("env_example.txt")
    if env_example.exists():
        print("✅ Exemplo de .env encontrado")
        return True
    else:
        print("⚠️ Exemplo de .env não encontrado")
        return False

def prepare_deploy():
    """Preparar arquivos para deploy"""
    print("📦 Preparando arquivos para deploy...")
    
    # Copiar docs se necessário
    docs_source = Path("../docs")
    docs_target = Path("docs")
    
    if docs_source.exists() and not docs_target.exists():
        import shutil
        shutil.copytree(docs_source, docs_target)
        print("✅ Pasta docs copiada")
    
    # Verificar se todos os arquivos estão prontos
    return check_files()

def git_commands():
    """Executar comandos Git"""
    print("📝 Executando comandos Git...")
    
    try:
        # Adicionar todos os arquivos
        subprocess.run(["git", "add", "."], check=True)
        print("✅ Arquivos adicionados ao Git")
        
        # Commit
        subprocess.run([
            "git", "commit", "-m", 
            "Deploy Assistente Niara para Render"
        ], check=True)
        print("✅ Commit realizado")
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Push realizado")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no Git: {e}")
        return False

def show_next_steps():
    """Mostrar próximos passos"""
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASSOS PARA DEPLOY NO RENDER")
    print("="*60)
    
    print("\n1. 🌐 Acesse: https://dashboard.render.com")
    print("2. ➕ Clique em 'New +' → 'Web Service'")
    print("3. 🔗 Conecte seu repositório GitHub")
    print("4. ⚙️ Configure o serviço:")
    print("   • Name: assistente-niara")
    print("   • Environment: Python 3")
    print("   • Build Command: pip install -r requirements.txt")
    print("   • Start Command: python klona_agent.py")
    
    print("\n5. 🔑 Adicione variáveis de ambiente:")
    print("   • MISTRAL_API_KEY = sua_chave_api")
    print("   • PORT = 8000")
    print("   • HOST = 0.0.0.0")
    print("   • DEBUG = false")
    
    print("\n6. 🚀 Clique em 'Create Web Service'")
    print("7. ⏳ Aguarde o deploy (5-10 minutos)")
    print("8. 🎉 Acesse: https://seu-app.onrender.com")
    
    print("\n📚 Documentação completa: RENDER_DEPLOY.md")

def main():
    print("🚀 Deploy Assistente Niara para Render")
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
    check_env_example()
    
    print("\n📋 Verificações concluídas!")
    
    # Preparar deploy
    if not prepare_deploy():
        print("\n❌ Erro ao preparar deploy!")
        return
    
    # Confirmar deploy
    print("\n🤔 Deseja fazer push para GitHub?")
    choice = input("Isso irá fazer commit e push dos arquivos (s/n): ").lower()
    
    if choice == 's':
        if git_commands():
            print("\n✅ Push realizado com sucesso!")
            show_next_steps()
        else:
            print("\n❌ Erro no push!")
    else:
        print("\n📝 Arquivos preparados, mas não foi feito push")
        print("Execute manualmente:")
        print("git add .")
        print("git commit -m 'Deploy Assistente Niara para Render'")
        print("git push origin main")
        show_next_steps()

if __name__ == "__main__":
    main()
