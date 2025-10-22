#!/usr/bin/env python3
"""
Webhook Server para Assistente Niara
Versão simplificada - sempre envia respostas para webhook específico
"""

import os
import sys
import json
import requests
from flask import Flask, request, jsonify
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Webhook fixo para respostas
RESPONSE_WEBHOOK_URL = "https://webhook.fiqon.app/webhook/a02bb210-fabb-4bcf-9976-601014ae05af/05e23f61-0a62-48da-b7c1-a31507aab6a2"

class NiaraWebhookServer:
    def __init__(self):
        self.niara_api = os.getenv("NIARA_API_URL", "https://assistente-niara.onrender.com")
        self.agent_name = "assistente-niara"
        
    def send_to_niara(self, message, user_id=None, metadata=None):
        """Enviar mensagem para o Assistente Niara"""
        try:
            payload = {
                "message": message,
                "stream": False,
                "webhook_url": RESPONSE_WEBHOOK_URL  # Sempre usar o webhook fixo
            }
            
            if user_id:
                payload["user_id"] = user_id
            
            if metadata:
                payload["metadata"] = metadata
            
            response = requests.post(
                f"{self.niara_api}/agents/{self.agent_name}/run",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Erro HTTP {response.status_code}: {response.text}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Timeout ao conectar com Niara"}
        except requests.exceptions.ConnectionError:
            return {"error": "Erro de conexão com Niara"}
        except Exception as e:
            return {"error": f"Erro inesperado: {str(e)}"}
    
    def send_webhook_response(self, webhook_url, data):
        """Enviar resposta para webhook externo"""
        try:
            response = requests.post(
                webhook_url,
                json=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Erro ao enviar webhook: {e}")
            return False

# Instanciar o servidor
server = NiaraWebhookServer()

@app.route("/", methods=["GET"])
def home():
    """Página inicial"""
    return jsonify({
        "service": "Niara Webhook Server",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "webhook": "/webhook",
            "send": "/send",
            "health": "/health"
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({
        "status": "ok",
        "service": "Niara Webhook Server",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    """Receber mensagens via webhook"""
    try:
        # Obter dados da requisição
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extrair informações
        message = data.get("message", "")
        user_id = data.get("user_id", "webhook_user")
        metadata = data.get("metadata", {})
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        print(f"📨 Mensagem recebida de {user_id}: {message}")
        
        # Enviar para o Assistente Niara
        niara_response = server.send_to_niara(message, user_id, metadata)
        
        # Preparar resposta
        response_data = {
            "success": "error" not in niara_response,
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "response_webhook": RESPONSE_WEBHOOK_URL
        }
        
        # Se houver erro, incluir na resposta
        if "error" in niara_response:
            response_data["error"] = niara_response["error"]
            print(f"❌ Erro do Niara: {niara_response['error']}")
        else:
            print(f"✅ Mensagem enviada para Niara, resposta será enviada para: {RESPONSE_WEBHOOK_URL}")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/send", methods=["POST"])
def send_message():
    """Enviar mensagem diretamente (sem webhook de resposta)"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")
        metadata = data.get("metadata", {})
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        print(f"📤 Enviando mensagem para Niara: {message}")
        
        # Enviar para o Assistente Niara
        niara_response = server.send_to_niara(message, user_id, metadata)
        
        response_data = {
            "success": "error" not in niara_response,
            "user_id": user_id,
            "message": message,
            "response": niara_response.get("content", "Erro ao processar mensagem"),
            "timestamp": datetime.now().isoformat()
        }
        
        if "error" in niara_response:
            response_data["error"] = niara_response["error"]
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/test", methods=["GET"])
def test():
    """Endpoint de teste"""
    test_message = "Olá, como configurar o chatbot Asksuite?"
    
    print(f"🧪 Testando com mensagem: {test_message}")
    
    niara_response = server.send_to_niara(test_message, "test_user")
    
    return jsonify({
        "test": True,
        "message": test_message,
        "niara_response": niara_response,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    print("🤖 Niara Webhook Server iniciando...")
    print("📡 Webhook simples para Assistente Niara")
    print("🌐 Servidor rodando em http://localhost:5000")
    print(f"📤 Respostas serão enviadas para: {RESPONSE_WEBHOOK_URL}")
    print("\n📋 Endpoints disponíveis:")
    print("   • GET  / - Informações do serviço")
    print("   • GET  /health - Health check")
    print("   • POST /webhook - Receber mensagens")
    print("   • POST /send - Enviar mensagens")
    print("   • GET  /test - Teste de conectividade")
    print("\n🔧 Configurações:")
    print(f"   • Niara API: {server.niara_api}")
    print(f"   • Agent: {server.agent_name}")
    print(f"   • Response Webhook: {RESPONSE_WEBHOOK_URL}")
    
    app.run(host="0.0.0.0", port=5000, debug=True)
