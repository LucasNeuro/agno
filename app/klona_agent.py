import os
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.mistral import MistralChat
from agno.os import AgentOS
from agno.tools.api import CustomApiTools
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.vectordb.chroma import ChromaDb
from dotenv import load_dotenv

# Carregar variáveis de ambiente (da pasta raiz)
load_dotenv(dotenv_path='../.env')

# Obter API key das variáveis de ambiente
api_key = os.getenv("MISTRAL_API_KEY")

# Verificar se a API key foi encontrada
if not api_key:
    raise ValueError(
        "MISTRAL_API_KEY não encontrada!\n"
        "Verifique se o arquivo .env existe e contém a chave API do Mistral."
    )

print("Inicializando Assistente Niara com Mistral...")

# ============================================
# CONFIGURAR BASE DE CONHECIMENTO (RAG)
# ============================================

print("📚 Configurando base de conhecimento...")

# Configurar embedder (modelo para gerar vetores)
embedder = SentenceTransformerEmbedder(
    id="all-MiniLM-L6-v2",  # Modelo leve e eficiente
)

# Configurar banco vetorial (ChromaDB)
vector_db = ChromaDb(
    collection="klona_knowledge",
    embedder=embedder,
)

# Criar sistema de conhecimento
knowledge = Knowledge(
    vector_db=vector_db,
)

# PDFs serão processados separadamente
print("📄 PDFs devem ser processados com: python process_pdfs.py")

print("✅ Base de conhecimento configurada!")


mistral_agent = Agent(
    name="Assistente Niara",
    
    # Modelo Mistral
    model=MistralChat(
        id="mistral-large-latest",  
        api_key=api_key,
    ),
    
    # Base de conhecimento integrada (RAG)
    knowledge=knowledge,
    add_knowledge_to_context=True,  # RAG automático
    search_knowledge=True,          # Busca inteligente
    
    # Database SQLite para persistir o histórico
    db=SqliteDb(db_file="mistral_agent.db"),
    
    # Memory habilitada - o agente lembra informações sobre o usuário
    enable_agentic_memory=True,
    add_memories_to_context=True,    # Adiciona memórias ao contexto
    
    # Histórico de conversas - ESSENCIAL para contexto
    add_history_to_context=True,     # Adiciona histórico ao contexto
    num_history_runs=10,             # Últimas 10 execuções
    search_session_history=True,     # Busca em sessões anteriores
    num_history_sessions=5,          # Últimas 5 sessões
    read_chat_history=True,          # Lê histórico de chat
    
    # Reasoning desabilitado - respostas diretas em português
    reasoning=False,
    
    # Ferramentas disponíveis
    tools=[
        CustomApiTools(
            base_url="https://jsonplaceholder.typicode.com",  # API de teste genérica
            headers={"Content-Type": "application/json"},
            timeout=30,
            verify_ssl=True,
            enable_make_request=True
        )
    ],
    
    # Instruções do agente
instructions=[
    "Você é o assistente virtual da NIARA - empresa de tecnologia para turismo.",
    "IMPORTANTE: Sempre responda em PORTUGUÊS BRASILEIRO. Nunca use inglês.",
    "",
    "SOBRE A NIARA:",
    "- Somos uma empresa de tecnologia especializada em soluções para o setor de turismo",
    "- Oferecemos sistemas de gestão, chatbots, e ferramentas digitais para empresas de turismo",
    "- Nossa missão é modernizar e otimizar o atendimento no setor turístico",
    "",
    "SUA BASE DE CONHECIMENTO contém:",
    "- Manual de configuração do Chatbot Asksuite",
    "- Guias de criação e gestão de usuários", 
    "- Configurações de autenticação e segurança (MFA)",
    "- Permissões por tipo de usuário",
    "- Configurações de recebimento e PIX",
    "- Sistema de marcadores",
    "- Módulo de extras e funcionalidades avançadas",
        "",
        "DETECÇÃO DE INTENÇÕES E USO AUTOMÁTICO DE FERRAMENTAS:",
        "",
        "QUANDO USAR make_request (API):",
        "- Palavras-chave: 'usuários', 'posts', 'dados', 'buscar', 'consultar', 'ver', 'listar', 'mostrar'",
        "- Frases: 'Quero ver...', 'Busque...', 'Consulte...', 'Mostre...', 'Liste...'",
        "- Endpoints disponíveis: /users, /posts, /comments, /albums, /photos, /todos",
        "- AÇÃO: Use make_request IMEDIATAMENTE sem pedir permissão!",
        "",
        "QUANDO USAR update_user_memory (MEMÓRIA):",
        "- Palavras-chave: 'meu nome é', 'sou', 'gosto de', 'prefiro', 'trabalho', 'estudo'",
        "- Frases: 'Eu sou...', 'Meu nome...', 'Gosto de...', 'Prefiro...'",
        "- AÇÃO: Salve a informação automaticamente na memória!",
        "",
        "QUANDO USAR BASE DE CONHECIMENTO (RAG):",
        "- Perguntas sobre: políticas, FAQ, problemas técnicos, atendimento, produtos",
        "- Frases: 'Qual a política...', 'Como faço...', 'Problema com...', 'Preciso de ajuda...'",
        "- AÇÃO: SEMPRE consulte sua base de conhecimento antes de responder!",
        "",
"EXEMPLOS PRÁTICOS:",
"Usuário: 'Como configurar o chatbot?' → Você: 'Vou te ajudar com a configuração do Chatbot Asksuite da Niara!' [RAG]",
"Usuário: 'Meu nome é Ana' → Você: 'Prazer, Ana! Vou lembrar disso.' [update_user_memory]",
"Usuário: 'Como criar usuários?' → Você: 'Baseado na nossa documentação, vou te mostrar como criar usuários no sistema.' [RAG]",
"Usuário: 'Como configurar PIX?' → Você: 'Segundo nosso manual, vou te explicar como configurar PIX para recebimento.' [RAG]",
        "",
        "REGRAS IMPORTANTES:",
        "1. NUNCA pergunte se pode usar as ferramentas - USE automaticamente!",
        "2. Seja PROATIVO - detecte a intenção e aja imediatamente",
        "3. SEMPRE consulte sua base de conhecimento para perguntas de atendimento",
        "4. Explique o que está fazendo enquanto executa",
        "5. Use as ferramentas corretas para cada situação",
        "",
"Para tarefas complexas, divida em etapas menores e execute uma por vez.",
"Sempre busque a melhor solução para o usuário da Niara.",
"Use markdown para estruturar suas respostas quando apropriado.",
"Seja amigável, prestativo e represente bem a marca Niara em todas as interações.",
"Quando usar APIs, explique claramente o que está fazendo e os resultados obtidos.",
"Você tem memória avançada (agentic memory) e pode criar, atualizar ou deletar memórias quando relevante.",
"Use sua memória para personalizar respostas e lembrar de conversas anteriores.",
"Para atendimento, SEMPRE baseie suas respostas na base de conhecimento da Niara quando relevante.",
"Lembre-se: você representa a Niara, uma empresa de tecnologia para turismo.",
"Seja especialista em soluções tecnológicas para o setor turístico.",
    ],
    
    # Formato de saída
    markdown=True,
)

print(f"Agente '{mistral_agent.name}' criado com sucesso!")

# ============================================
# CRIAR AGENTOS (Runtime FastAPI)
# ============================================
agent_os = AgentOS(
    agents=[mistral_agent],
)

# Obter a aplicação FastAPI do AgentOS
app = agent_os.get_app()

print("\n" + "="*70)
print("🤖 ASSISTENTE NIARA COM RAG PRONTO!")
print("="*70)
print("\nConfigurações:")
print(f"   • Nome do Agente: {mistral_agent.name}")
print(f"   • Modelo: Mistral Large Latest")
print(f"   • Tipo: Assistente Niara - Tecnologia para Turismo")
print(f"   • Reasoning: Desabilitado (respostas diretas em português)")
print(f"   • Memory: Agentic Memory (controle total)")
print(f"   • Histórico: Últimas 10 execuções + 5 sessões")
print(f"   • Contexto: Memórias + Histórico de chat")
print(f"   • Inteligência: Detecção automática de intenções")
print(f"   • Ferramentas: Uso automático sem permissão")
print(f"   • Database: mistral_agent.db")
print(f"   • Ferramentas: CustomApiTools (HTTP Requests)")
print(f"   • API Base: https://jsonplaceholder.typicode.com")
print(f"   • 🆕 Base de Conhecimento: Pronta para documentos")
print(f"   • 🆕 RAG: Habilitado (busca automática)")
print(f"   • 🆕 Banco Vetorial: ChromaDB")
print(f"   • 🆕 Embedder: all-MiniLM-L6-v2")
print("\nPara iniciar o servidor:")
print("   cd app && python klona_agent.py")
print("\nEndpoints disponíveis:")
print("   • API Documentation: http://localhost:8000/docs")
print("   • Health Check: http://localhost:8000/health")
print("\nConectar ao AgentOS UI:")
print("   1. Acesse: https://os.agno.com")
print("   2. Faça login")
print("   3. Clique em 'Add new OS' → 'Local'")
print("   4. Configure URL: http://localhost:8000")
print("   5. Clique em 'Connect'")
print("="*70 + "\n")

# ============================================
# SERVIR O AGENTOS (Método Oficial)
# ============================================
if __name__ == "__main__":
    # Usar o método oficial do AgentOS para servir
    agent_os.serve(
        app="klona_agent:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )