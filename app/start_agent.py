#!/usr/bin/env python3
"""
Script de inicialização do Assistente Niara
Versão simplificada para deploy
"""

import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Importar e executar o agente
if __name__ == "__main__":
    print("🤖 Iniciando Assistente Niara...")
    print("📚 Base de conhecimento será carregada automaticamente")
    print("🌐 Servidor iniciando...")
    
    # Executar o agente principal
    exec(open('klona_agent.py').read())
