# 🤖 Agente Conversacional com Agno + Gemini

Agente conversacional inteligente usando o framework **Agno** com **Google Gemini 2.0 Flash** e **reasoning** habilitado.

Este projeto demonstra como criar um agente básico para testar o **AgentOS** - o runtime de alta performance para sistemas multi-agente.

## 📚 Documentação Oficial

- [Agno Introduction](https://docs.agno.com/introduction)
- [AgentOS Introduction](https://docs.agno.com/agent-os/introduction)

## 📦 Estrutura do Projeto

```
agno/
├── .env                    # Variáveis de ambiente (API keys)
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Dependências do Python
├── gemini_agent.py       # Agente conversacional principal
└── README.md             # Este arquivo
```

## 🚀 Setup e Instalação

### Pré-requisitos

- Python 3.12 ou superior
- Chave API do Google Gemini ([obtenha aqui](https://aistudio.google.com/apikey))

### Passo 1: Criar Ambiente Virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Passo 2: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 3: Verificar Configuração

O arquivo `.env` já está configurado com a chave API. Caso precise alterar:

```env
GOOGLE_API_KEY=sua_nova_chave_aqui
```

## 🎯 Como Executar

### Iniciar o Servidor

```bash
fastapi dev gemini_agent.py
```

Você verá uma saída similar a:

```
🚀 Inicializando Agente Conversacional com Reasoning...
✅ Agente 'Gemini Assistant' criado com sucesso!

======================================================================
🎯 AGENTE CONVERSACIONAL PRONTO!
======================================================================

INFO:     Uvicorn running on http://localhost:8000
INFO:     Application startup complete.
```

### Acessar a Documentação da API

Abra no navegador: **http://localhost:8000/docs**

Você terá acesso aos endpoints:
- `POST /v1/agents/{agent_id}/run` - Executar o agente
- `GET /v1/agents` - Listar agentes disponíveis
- `GET /v1/agents/{agent_id}/sessions` - Ver sessões do agente
- `GET /v1/health` - Status do sistema

## 🖥️ Conectar ao AgentOS UI

O **AgentOS UI** é uma interface web para gerenciar e interagir com seus agentes.

### Passos:

1. **Acesse:** [https://os.agno.com](https://os.agno.com)
2. **Faça login** (crie uma conta se necessário)
3. **Adicione seu OS local:**
   - Clique em **"Add new OS"**
   - Selecione **"Local"**
   - Configure:
     - **Name:** Dev Environment
     - **URL:** `http://localhost:8000`
   - Clique em **"Connect"**

4. **Comece a conversar:**
   - Vá para a seção **Chat**
   - Selecione seu agente **"Gemini Assistant"**
   - Digite suas perguntas!

✅ Seu agente estará com status **live** (verde).

## 💬 Testando o Agente

### Via Web UI (Recomendado)

Depois de conectar ao AgentOS UI, você pode conversar naturalmente:

**Exemplos:**
- "Olá! Como você funciona?"
- "Explique o que é reasoning"
- "Se eu tenho 10 laranjas e compro o dobro, depois como 5, quantas sobraram?"

### Via API (cURL)

```bash
curl -X POST http://localhost:8000/v1/agents/gemini-assistant/run \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá! Explique como funciona o reasoning.",
    "stream": false
  }'
```

### Via Python

```python
import requests

response = requests.post(
    "http://localhost:8000/v1/agents/gemini-assistant/run",
    json={
        "message": "Qual é a capital do Brasil?",
        "stream": False
    }
)

print(response.json())
```

## 🧠 O que é Reasoning?

**Reasoning** é a capacidade do agente "pensar" antes de responder.

### Como funciona:

1. **Analisa** a pergunta em profundidade
2. **Planeja** a estratégia de resposta
3. **Executa** o raciocínio em etapas
4. **Valida** a lógica
5. **Responde** com precisão

### Exemplo Prático:

**Pergunta:** "Se eu tenho 3 maçãs e compro o dobro, depois dou metade para um amigo, quantas maçãs eu tenho?"

**Com Reasoning:**
- Passo 1: 3 maçãs iniciais
- Passo 2: Compro o dobro = 3 × 2 = 6 maçãs
- Passo 3: Dar metade = 6 ÷ 2 = 3 maçãs restantes
- **Resposta:** "Você tem 3 maçãs"

**Sem Reasoning:**
- Resposta direta (pode errar cálculos)

## 🔧 Características do Agente

| Recurso | Descrição | Status |
|---------|-----------|--------|
| **Modelo** | Gemini 2.0 Flash | ✅ |
| **Reasoning** | Pensamento crítico habilitado | ✅ |
| **Memória** | Persistência em SQLite | ✅ |
| **Contexto** | Últimas 5 mensagens | ✅ |
| **Markdown** | Formatação de texto | ✅ |
| **FastAPI** | Runtime HTTP pronto | ✅ |

## 📊 Monitoramento

### Via AgentOS UI:

- **Sessions:** Visualize todas as conversas
- **Metrics:** Tokens usados, tempo de resposta
- **Debug:** Logs detalhados de execução

### Via Logs do Servidor:

O terminal mostrará todas as requisições em tempo real:

```
INFO:     127.0.0.1:52345 - "POST /v1/agents/gemini-assistant/run HTTP/1.1" 200 OK
```

## 🛠️ Troubleshooting

### Erro: "API key not found"

```bash
# Verifique o arquivo .env
cat .env

# Ou recarregue as variáveis de ambiente:
# Windows
set GOOGLE_API_KEY=sua_chave_aqui

# Mac/Linux
export GOOGLE_API_KEY=sua_chave_aqui
```

### Erro: "Module not found"

```bash
# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Port 8000 already in use"

```bash
# Use uma porta diferente
fastapi dev gemini_agent.py --port 8001
```

### AgentOS UI não conecta

1. Verifique se o servidor está rodando: `http://localhost:8000/v1/health`
2. Confirme que a URL no AgentOS UI está correta
3. Verifique firewall/antivírus
4. Tente desabilitar HTTPS no navegador para localhost

## 📈 Próximos Passos

Depois de testar o agente básico, você pode expandir com:

1. **🔧 Ferramentas (Tools):**
   - Acesso a APIs externas (ViaCEP, etc.)
   - Busca na web (DuckDuckGo)
   - Cálculos matemáticos

2. **🧠 Memória Persistente:**
   - Lembrar preferências do usuário
   - Contexto entre sessões

3. **👥 Multi-Agentes:**
   - Criar equipes de agentes especializados
   - Workflows coordenados

4. **📚 Knowledge Base:**
   - RAG (Retrieval Augmented Generation)
   - Busca vetorial em documentos

## 📚 Recursos Úteis

- [Documentação Completa do Agno](https://docs.agno.com)
- [Modelos Gemini Disponíveis](https://ai.google.dev/gemini-api/docs/models)
- [Exemplos no GitHub](https://github.com/agno-agi/agno/tree/main/cookbook)
- [AgentOS UI](https://os.agno.com)
- [Comunidade Discord](https://discord.gg/agno)

## 🤝 Contribuindo

Encontrou um bug ou tem uma sugestão? Sinta-se à vontade para abrir uma issue ou pull request!

## 📝 Licença

MIT License - use livremente em seus projetos!

---

**Feito com ❤️ usando [Agno Framework](https://docs.agno.com)**

