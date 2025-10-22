#!/usr/bin/env python3
"""
Script Simples de Deploy - Assistente Niara
Baseado na documentação oficial do AgnoOS
"""

import os
import sys
import subprocess
from pathlib import Path

def check_agno_cli():
    """Verificar se o Agno CLI está instalado"""
    try:
        result = subprocess.run(["ag", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Agno CLI encontrado: {result.stdout.strip()}")
            return True
        else:
            print("❌ Agno CLI não encontrado")
            return False
    except FileNotFoundError:
        print("❌ Agno CLI não instalado")
        return False

def install_agno_cli():
    """Instalar Agno CLI"""
    print("📦 Instalando Agno CLI...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "agno"], check=True)
        print("✅ Agno CLI instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar Agno CLI")
        return False

def create_infrastructure():
    """Criar infraestrutura usando template oficial"""
    print("🏗️ Criando infraestrutura...")
    
    # Verificar se já existe
    if Path("assistente-niara-prod").exists():
        print("⚠️ Pasta 'assistente-niara-prod' já existe!")
        choice = input("Deseja continuar? (s/n): ").lower()
        if choice != 's':
            return False
    
    try:
        # Executar comando do Agno
        result = subprocess.run([
            "ag", "infra", "create"
        ], input="assistente-niara-prod\n1\n", text=True, check=True)
        
        print("✅ Infraestrutura criada com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar infraestrutura: {e}")
        return False

def copy_files():
    """Copiar arquivos do projeto para a infraestrutura"""
    print("📁 Copiando arquivos...")
    
    source_dir = Path(".")
    target_dir = Path("../assistente-niara-prod")
    
    if not target_dir.exists():
        print("❌ Pasta de infraestrutura não encontrada!")
        return False
    
    # Arquivos para copiar
    files_to_copy = [
        "klona_agent.py",
        "requirements.txt",
        "mistral_agent.db"
    ]
    
    # Copiar arquivos
    for file_name in files_to_copy:
        source_file = source_dir / file_name
        target_file = target_dir / file_name
        
        if source_file.exists():
            import shutil
            shutil.copy2(source_file, target_file)
            print(f"✅ Copiado: {file_name}")
        else:
            print(f"⚠️ Arquivo não encontrado: {file_name}")
    
    # Copiar pasta docs
    docs_source = Path("../docs")
    docs_target = target_dir / "docs"
    
    if docs_source.exists():
        import shutil
        if docs_target.exists():
            shutil.rmtree(docs_target)
        shutil.copytree(docs_source, docs_target)
        print("✅ Copiado: pasta docs")
    
    return True

def setup_environment():
    """Configurar variáveis de ambiente"""
    print("🔧 Configurando ambiente...")
    
    env_file = Path("../assistente-niara-prod/.env")
    
    # Verificar se .env já existe
    if env_file.exists():
        print("⚠️ Arquivo .env já existe!")
        choice = input("Deseja sobrescrever? (s/n): ").lower()
        if choice != 's':
            return True
    
    # Solicitar chave API
    api_key = input("Digite sua MISTRAL_API_KEY: ").strip()
    
    if not api_key:
        print("❌ Chave API é obrigatória!")
        return False
    
    # Criar arquivo .env
    env_content = f"""# Configurações do Assistente Niara
MISTRAL_API_KEY={api_key}

# Configurações de Produção
DATABASE_URL=postgresql://postgres:password@db:5432/agno
PORT=8000
HOST=0.0.0.0
DEBUG=False
LOG_LEVEL=INFO
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print("✅ Arquivo .env criado!")
    return True

def deploy_local():
    """Deploy local com Docker"""
    print("🐳 Fazendo deploy local...")
    
    target_dir = Path("../assistente-niara-prod")
    
    if not target_dir.exists():
        print("❌ Pasta de infraestrutura não encontrada!")
        return False
    
    try:
        # Mudar para diretório da infraestrutura
        os.chdir(target_dir)
        
        # Executar deploy local
        result = subprocess.run(["ag", "infra", "up"], check=True)
        
        print("✅ Deploy local realizado com sucesso!")
        print("🌐 Acesse: http://localhost:8000")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no deploy local: {e}")
        return False

def main():
    print("🤖 Assistente Niara - Deploy Simples")
    print("=" * 50)
    
    # Verificar Agno CLI
    if not check_agno_cli():
        if not install_agno_cli():
            print("❌ Não foi possível instalar o Agno CLI")
            return
    
    print("\n📋 Opções de Deploy:")
    print("1. Criar infraestrutura completa")
    print("2. Deploy local apenas")
    print("3. Sair")
    
    choice = input("\nEscolha uma opção (1-3): ").strip()
    
    if choice == "1":
        # Criar infraestrutura completa
        if create_infrastructure():
            if copy_files():
                if setup_environment():
                    print("\n🎯 Infraestrutura criada com sucesso!")
                    print("📁 Pasta: assistente-niara-prod")
                    print("🔧 Configure o .env com suas chaves")
                    print("🐳 Execute: cd assistente-niara-prod && ag infra up")
    
    elif choice == "2":
        # Deploy local apenas
        if deploy_local():
            print("\n🎉 Deploy local concluído!")
    
    elif choice == "3":
        print("👋 Até logo!")
    
    else:
        print("❌ Opção inválida!")

if __name__ == "__main__":
    main()
