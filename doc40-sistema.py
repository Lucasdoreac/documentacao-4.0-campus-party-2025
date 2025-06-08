#!/usr/bin/env python3
"""
Documentação 4.0 - Sistema Completo com Interface Interativa
Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

Este script integra todas as funcionalidades do sistema Documentação 4.0
em uma interface interativa de linha de comando, permitindo consulta,
geração, manutenção e visualização da documentação.
"""

import os
import sys
import json
import time
import argparse
import subprocess
import threading
import http.server
import socketserver
import webbrowser
import logging
import signal
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime

# Importar módulos do sistema Documentação 4.0
# Você pode usar importação direta se os módulos estiverem instalados
# como pacotes, ou usar importação relativa se estiverem no mesmo diretório.
try:
    # Se eles forem módulos locais no mesmo diretório
    # Esta é a abordagem que estamos usando para o sistema Documentação 4.0
    from doc40_consulta import consultar_codigo, verificar_claude_code as verificar_consulta
    from doc40_gerador import gerar_documentacao, gerar_documentacao_api
    from doc40_agente import atualizar_documentacao, verificar_git, executar_agente as executar_agente_thread
except ImportError:
    # Implementação inline para quando os módulos não estão disponíveis como imports
    # Isso torna o script completamente independente
    
    def verificar_claude_code():
        """Verifica se o Claude Code CLI está instalado."""
        try:
            result = subprocess.run(
                ["claude-code", "--version"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
            
    def consultar_codigo(pergunta, diretorio, formato="text", cache=True):
        """Consulta o código usando Claude Code."""
        if not verificar_claude_code():
            return {"error": "ClaudeCodeNotFound"}
            
        command = [
            "claude-code",
            "query",
            "--directory", diretorio,
            "--query", pergunta,
            "--output", "json"
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return {"error": "CommandError", "message": result.stderr}
        except Exception as e:
            return {"error": "Exception", "message": str(e)}
    
    def gerar_documentacao(diretorio, formato="markdown", saida="docs", escopo="all"):
        """Gera documentação a partir do código."""
        if not verificar_claude_code():
            return {"success": False, "error": "ClaudeCodeNotFound"}
            
        os.makedirs(saida, exist_ok=True)
        
        command = [
            "claude-code",
            "document",
            "--directory", diretorio,
            "--format", formato,
            "--output-dir", saida
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "output_dir": saida}
            return {"success": False, "error": "CommandError", "message": result.stderr}
        except Exception as e:
            return {"success": False, "error": "Exception", "message": str(e)}
    
    def gerar_documentacao_api(diretorio, formato="openapi", saida="docs/api"):
        """Gera documentação de API."""
        if not verificar_claude_code():
            return {"success": False, "error": "ClaudeCodeNotFound"}
            
        os.makedirs(saida, exist_ok=True)
        
        command = [
            "claude-code",
            "document-api",
            "--directory", diretorio,
            "--format", formato,
            "--output-dir", saida
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "output_dir": saida}
            return {"success": False, "error": "CommandError", "message": result.stderr}
        except Exception as e:
            return {"success": False, "error": "Exception", "message": str(e)}
    
    def verificar_git(diretorio):
        """Verifica se o diretório é um repositório Git."""
        try:
            os.chdir(diretorio)
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0 and result.stdout.strip() == "true"
        except Exception:
            return False
    
    def atualizar_documentacao(diretorio, commit_id, saida="docs"):
        """Atualiza documentação com base nas mudanças do commit."""
        if not verificar_claude_code():
            return {"success": False, "error": "ClaudeCodeNotFound"}
            
        os.makedirs(saida, exist_ok=True)
        
        command = [
            "claude-code",
            "update-docs",
            "--directory", diretorio,
            "--commit", commit_id,
            "--output-dir", saida
        ]
        
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                return {"success": True, "output_dir": saida}
            return {"success": False, "error": "CommandError", "message": result.stderr}
        except Exception as e:
            return {"success": False, "error": "Exception", "message": str(e)}
    
    def executar_agente_thread(diretorio, saida="docs", intervalo=300):
        """Executa o agente de manutenção em uma thread separada."""
        def verificar_mudancas(dir, ultimo_commit=None):
            os.chdir(dir)
            cmd = ["git", "rev-parse", "HEAD"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return False, None
                
            commit_atual = result.stdout.strip()
            if ultimo_commit is None:
                return False, commit_atual
                
            return commit_atual != ultimo_commit, commit_atual
        
        def thread_func():
            if not verificar_git(diretorio):
                return
                
            os.makedirs(saida, exist_ok=True)
            _, ultimo_commit = verificar_mudancas(diretorio)
            
            while True:
                try:
                    houve_mudancas, commit_atual = verificar_mudancas(diretorio, ultimo_commit)
                    
                    if houve_mudancas:
                        atualizar_documentacao(diretorio, commit_atual, saida)
                        ultimo_commit = commit_atual
                    
                    time.sleep(intervalo)
                except Exception:
                    time.sleep(intervalo)
        
        thread = threading.Thread(target=thread_func, daemon=True)
        thread.start()
        return thread

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('doc40-sistema.log')
    ]
)
logger = logging.getLogger('doc40-sistema')

# Cores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DocumentationServer:
    """Servidor HTTP simples para visualizar a documentação gerada."""
    
    def __init__(self, docs_dir: str, port: int = 8000):
        """
        Inicializa o servidor de documentação.
        
        Args:
            docs_dir: O diretório da documentação
            port: A porta para o servidor (padrão: 8000)
        """
        self.docs_dir = os.path.abspath(docs_dir)
        self.port = port
        self.server = None
        self.server_thread = None
        self.running = False
    
    def start(self) -> bool:
        """
        Inicia o servidor HTTP.
        
        Returns:
            bool: True se o servidor iniciou com sucesso, False caso contrário
        """
        if self.running:
            logger.warning("Servidor já está em execução")
            print(f"{Colors.YELLOW}⚠️ Servidor já está em execução{Colors.ENDC}")
            return False
        
        try:
            if not os.path.isdir(self.docs_dir):
                logger.error(f"Diretório de documentação não encontrado: {self.docs_dir}")
                print(f"{Colors.RED}❌ Diretório de documentação não encontrado: {self.docs_dir}{Colors.ENDC}")
                return False
            
            os.chdir(self.docs_dir)
            
            # Criar um arquivo index.html se não existir
            index_path = os.path.join(self.docs_dir, "index.html")
            if not os.path.exists(index_path):
                self._create_index_html()
            
            # Iniciar o servidor em uma thread separada
            handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.running = True
            
            logger.info(f"Servidor iniciado em http://localhost:{self.port}")
            print(f"{Colors.GREEN}✅ Servidor iniciado em http://localhost:{self.port}{Colors.ENDC}")
            
            # Abrir o navegador
            webbrowser.open(f"http://localhost:{self.port}")
            
            return True
        except Exception as e:
            logger.error(f"Erro ao iniciar servidor: {e}")
            print(f"{Colors.RED}❌ Erro ao iniciar servidor: {e}{Colors.ENDC}")
            return False
    
    def stop(self) -> bool:
        """
        Para o servidor HTTP.
        
        Returns:
            bool: True se o servidor parou com sucesso, False caso contrário
        """
        if not self.running:
            logger.warning("Servidor não está em execução")
            print(f"{Colors.YELLOW}⚠️ Servidor não está em execução{Colors.ENDC}")
            return False
        
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                self.running = False
                logger.info("Servidor parado")
                print(f"{Colors.YELLOW}ℹ️ Servidor parado{Colors.ENDC}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao parar servidor: {e}")
            print(f"{Colors.RED}❌ Erro ao parar servidor: {e}{Colors.ENDC}")
            return False
    
    def _run_server(self) -> None:
        """Função interna para executar o servidor em uma thread."""
        try:
            self.server.serve_forever()
        except Exception as e:
            logger.error(f"Erro no servidor: {e}")
    
    def _create_index_html(self) -> None:
        """Cria um arquivo index.html para navegar pela documentação."""
        # Listar arquivos de documentação
        md_files = [f for f in os.listdir(self.docs_dir) if f.endswith('.md')]
        html_files = [f for f in os.listdir(self.docs_dir) if f.endswith('.html') and f != "index.html"]
        other_files = [f for f in os.listdir(self.docs_dir) if not f.endswith(('.md', '.html', '.log'))]
        
        # Criar HTML
        html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação 4.0</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f5f7;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2a67c2;
            border-bottom: 2px solid #eaecef;
            padding-bottom: 10px;
        }
        h2 {
            color: #2a67c2;
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
            padding: 5px 10px;
            background-color: #f6f8fa;
            border-radius: 3px;
        }
        a {
            color: #2a67c2;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        footer {
            margin-top: 30px;
            font-size: 0.8em;
            color: #6a737d;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Documentação 4.0</h1>
        <p>Documentação gerada automaticamente pelo sistema Documentação 4.0.</p>
"""
        
        # Adicionar seção de arquivos Markdown
        if md_files:
            html_content += """
        <h2>Documentação Markdown</h2>
        <ul>
"""
            for file in sorted(md_files):
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar seção de arquivos HTML
        if html_files:
            html_content += """
        <h2>Documentação HTML</h2>
        <ul>
"""
            for file in sorted(html_files):
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar seção de outros arquivos
        if other_files:
            html_content += """
        <h2>Outros Arquivos</h2>
        <ul>
"""
            for file in sorted(other_files):
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar rodapé
        html_content += """
        <footer>
            <p>Gerado por Documentação 4.0 - Campus Party 2025</p>
            <p>Lucas Dórea Cardoso e Aulus Diniz</p>
        </footer>
    </div>
</body>
</html>
"""
        
        # Salvar o arquivo
        with open(os.path.join(self.docs_dir, "index.html"), 'w') as f:
            f.write(html_content)
        
        logger.info(f"Arquivo index.html criado em {self.docs_dir}")

class DocumentationSystem:
    """Sistema completo de Documentação 4.0."""
    
    def __init__(self):
        """Inicializa o sistema de documentação."""
        # Estado do sistema
        self.diretorio = os.getcwd()
        self.saida = os.path.join(self.diretorio, "docs")
        self.formato = "markdown"
        self.intervalo = 300  # 5 minutos
        self.porta = 8000
        
        # Componentes
        self.agente_thread = None
        self.agente_rodando = False
        self.servidor = None
        self.servidor_rodando = False
        
        # Verificar o ambiente
        self.verificar_ambiente()
    
    def verificar_ambiente(self) -> Dict[str, bool]:
        """
        Verifica o ambiente de execução.
        
        Returns:
            dict: Resultado das verificações
        """
        results = {
            "claude_code": verificar_claude_code(),
            "git": verificar_git(self.diretorio) if os.path.isdir(self.diretorio) else False
        }
        
        return results
    
    def mostrar_menu(self) -> None:
        """Mostra o menu principal do sistema."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}{'=' * 49}{Colors.ENDC}")
        print(f"{Colors.BOLD}📚 SISTEMA DE DOCUMENTAÇÃO 4.0{Colors.ENDC}")
        print(f"{Colors.BOLD}{'=' * 49}{Colors.ENDC}")
        print(f"1. Consultar documentação/código")
        print(f"2. Gerar documentação geral")
        print(f"3. Gerar documentação de API")
        print(f"4. Iniciar agente de manutenção")
        print(f"5. Parar agente de manutenção")
        print(f"6. Iniciar servidor de documentação")
        print(f"7. Parar servidor de documentação")
        print(f"8. Configurações")
        print(f"9. Sair")
        print(f"{Colors.BOLD}{'=' * 49}{Colors.ENDC}")
        
        # Mostrar estado atual
        print(f"\n{Colors.BLUE}Estado atual:{Colors.ENDC}")
        print(f"- Diretório: {self.diretorio}")
        print(f"- Saída: {self.saida}")
        print(f"- Formato: {self.formato}")
        print(f"- Agente: {'🟢 Rodando' if self.agente_rodando else '🔴 Parado'}")
        print(f"- Servidor: {'🟢 Rodando em http://localhost:' + str(self.porta) if self.servidor_rodando else '🔴 Parado'}")
        
        # Mostrar ambiente
        ambiente = self.verificar_ambiente()
        print(f"\n{Colors.BLUE}Ambiente:{Colors.ENDC}")
        print(f"- Claude Code: {'✅ Instalado' if ambiente['claude_code'] else '❌ Não encontrado'}")
        print(f"- Git: {'✅ Repositório válido' if ambiente['git'] else '❌ Não é um repositório Git'}")
    
    def opcao_consultar(self) -> None:
        """Opção para consultar documentação/código."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}📝 Consulta à Documentação/Código{Colors.ENDC}")
        print(f"{Colors.BLUE}Diretório: {self.diretorio}{Colors.ENDC}")
        print(f"\nDigite sua pergunta (ou 'voltar' para retornar ao menu):")
        
        try:
            while True:
                pergunta = input(f"\n{Colors.BOLD}Pergunta: {Colors.ENDC}")
                if pergunta.lower() in ['voltar', 'back', 'exit', 'sair', 'q']:
                    break
                
                if not pergunta.strip():
                    continue
                
                resultado = consultar_codigo(pergunta, self.diretorio)
                
                if "error" in resultado:
                    print(f"\n{Colors.RED}❌ Erro: {resultado.get('message', 'Erro desconhecido')}{Colors.ENDC}")
                else:
                    print("\n" + "="*50)
                    print(f"{Colors.GREEN}🤖 Resposta para: {pergunta}{Colors.ENDC}")
                    print("="*50)
                    print(resultado.get("response", "Sem resposta"))
                    print("="*50)
                    print(f"{Colors.BLUE}Fontes:{Colors.ENDC}")
                    
                    for fonte in resultado.get("sources", []):
                        relevancia = fonte.get("relevance", "N/A")
                        relevancia_formatada = relevancia if isinstance(relevancia, str) else f"{relevancia:.2f}"
                        print(f"- {fonte.get('file')} (relevância: {relevancia_formatada})")
                
                print("\nDigite outra pergunta ou 'voltar' para retornar ao menu:")
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Consulta interrompida{Colors.ENDC}")
    
    def opcao_gerar_documentacao(self) -> None:
        """Opção para gerar documentação geral."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}📄 Geração de Documentação Geral{Colors.ENDC}")
        print(f"{Colors.BLUE}Diretório: {self.diretorio}{Colors.ENDC}")
        print(f"{Colors.BLUE}Saída: {self.saida}{Colors.ENDC}")
        print(f"{Colors.BLUE}Formato: {self.formato}{Colors.ENDC}")
        
        confirmar = input(f"\nGerar documentação com estas configurações? (s/N): ")
        if confirmar.lower() != 's':
            print(f"{Colors.YELLOW}ℹ️ Operação cancelada{Colors.ENDC}")
            input("\nPressione Enter para continuar...")
            return
        
        resultado = gerar_documentacao(self.diretorio, self.formato, self.saida)
        
        if resultado.get("success"):
            print(f"\n{Colors.GREEN}✅ Documentação gerada com sucesso em: {self.saida}{Colors.ENDC}")
            
            # Perguntar se deseja abrir a documentação
            abrir = input(f"\nDeseja abrir a documentação no navegador? (s/N): ")
            if abrir.lower() == 's':
                self.iniciar_servidor()
        else:
            print(f"\n{Colors.RED}❌ Erro ao gerar documentação: {resultado.get('message', 'Erro desconhecido')}{Colors.ENDC}")
        
        input("\nPressione Enter para continuar...")
    
    def opcao_gerar_documentacao_api(self) -> None:
        """Opção para gerar documentação de API."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}📄 Geração de Documentação de API{Colors.ENDC}")
        print(f"{Colors.BLUE}Diretório: {self.diretorio}{Colors.ENDC}")
        print(f"{Colors.BLUE}Saída: {os.path.join(self.saida, 'api')}{Colors.ENDC}")
        print(f"{Colors.BLUE}Formato: openapi{Colors.ENDC}")
        
        confirmar = input(f"\nGerar documentação de API com estas configurações? (s/N): ")
        if confirmar.lower() != 's':
            print(f"{Colors.YELLOW}ℹ️ Operação cancelada{Colors.ENDC}")
            input("\nPressione Enter para continuar...")
            return
        
        resultado = gerar_documentacao_api(self.diretorio, "openapi", os.path.join(self.saida, "api"))
        
        if resultado.get("success"):
            print(f"\n{Colors.GREEN}✅ Documentação de API gerada com sucesso em: {os.path.join(self.saida, 'api')}{Colors.ENDC}")
            
            # Perguntar se deseja abrir a documentação
            abrir = input(f"\nDeseja abrir a documentação no navegador? (s/N): ")
            if abrir.lower() == 's':
                self.iniciar_servidor()
        else:
            print(f"\n{Colors.RED}❌ Erro ao gerar documentação de API: {resultado.get('message', 'Erro desconhecido')}{Colors.ENDC}")
        
        input("\nPressione Enter para continuar...")
    
    def iniciar_agente(self) -> None:
        """Inicia o agente de manutenção de documentação."""
        if self.agente_rodando:
            print(f"{Colors.YELLOW}⚠️ O agente já está em execução{Colors.ENDC}")
            return
        
        ambiente = self.verificar_ambiente()
        if not ambiente["claude_code"]:
            print(f"{Colors.RED}❌ Claude Code CLI não encontrado{Colors.ENDC}")
            return
        
        if not ambiente["git"]:
            print(f"{Colors.RED}❌ O diretório {self.diretorio} não é um repositório Git{Colors.ENDC}")
            return
        
        try:
            self.agente_thread = executar_agente_thread(self.diretorio, self.saida, self.intervalo)
            self.agente_rodando = True
            print(f"{Colors.GREEN}✅ Agente iniciado com sucesso{Colors.ENDC}")
            print(f"{Colors.BLUE}📁 Monitorando: {self.diretorio}{Colors.ENDC}")
            print(f"{Colors.BLUE}📂 Saída: {self.saida}{Colors.ENDC}")
            print(f"{Colors.BLUE}⏱️ Intervalo: {self.intervalo} segundos{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Erro ao iniciar agente: {str(e)}{Colors.ENDC}")
    
    def parar_agente(self) -> None:
        """Para o agente de manutenção de documentação."""
        if not self.agente_rodando:
            print(f"{Colors.YELLOW}⚠️ O agente não está em execução{Colors.ENDC}")
            return
        
        try:
            # Como a thread é daemon, basta marcar como não rodando
            self.agente_rodando = False
            print(f"{Colors.YELLOW}ℹ️ Agente parado{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Erro ao parar agente: {str(e)}{Colors.ENDC}")
    
    def iniciar_servidor(self) -> None:
        """Inicia o servidor de documentação."""
        if self.servidor_rodando:
            print(f"{Colors.YELLOW}⚠️ O servidor já está em execução{Colors.ENDC}")
            print(f"{Colors.BLUE}🌐 Acesse: http://localhost:{self.porta}{Colors.ENDC}")
            return
        
        if not os.path.isdir(self.saida):
            print(f"{Colors.YELLOW}⚠️ Diretório de documentação não encontrado: {self.saida}{Colors.ENDC}")
            print(f"{Colors.YELLOW}ℹ️ Criando diretório...{Colors.ENDC}")
            os.makedirs(self.saida, exist_ok=True)
        
        try:
            self.servidor = DocumentationServer(self.saida, self.porta)
            if self.servidor.start():
                self.servidor_rodando = True
                print(f"{Colors.GREEN}✅ Servidor iniciado com sucesso{Colors.ENDC}")
                print(f"{Colors.BLUE}🌐 Acesse: http://localhost:{self.porta}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Erro ao iniciar servidor: {str(e)}{Colors.ENDC}")
    
    def parar_servidor(self) -> None:
        """Para o servidor de documentação."""
        if not self.servidor_rodando:
            print(f"{Colors.YELLOW}⚠️ O servidor não está em execução{Colors.ENDC}")
            return
        
        try:
            if self.servidor and self.servidor.stop():
                self.servidor_rodando = False
                print(f"{Colors.YELLOW}ℹ️ Servidor parado{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}❌ Erro ao parar servidor: {str(e)}{Colors.ENDC}")
    
    def opcao_configuracoes(self) -> None:
        """Opção para configurar o sistema."""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Colors.BOLD}⚙️ Configurações{Colors.ENDC}")
        
        # Mostrar configurações atuais
        print(f"\n{Colors.BLUE}Configurações atuais:{Colors.ENDC}")
        print(f"1. Diretório: {self.diretorio}")
        print(f"2. Saída: {self.saida}")
        print(f"3. Formato: {self.formato}")
        print(f"4. Intervalo do agente: {self.intervalo} segundos")
        print(f"5. Porta do servidor: {self.porta}")
        print(f"6. Voltar ao menu principal")
        
        # Pedir opção
        try:
            opcao = input(f"\nEscolha uma opção (1-6): ")
            
            if opcao == "1":
                novo_diretorio = input(f"Novo diretório (Enter para manter atual): ")
                if novo_diretorio and os.path.isdir(novo_diretorio):
                    self.diretorio = os.path.abspath(novo_diretorio)
                    print(f"{Colors.GREEN}✅ Diretório atualizado: {self.diretorio}{Colors.ENDC}")
                elif novo_diretorio:
                    print(f"{Colors.RED}❌ Diretório não encontrado: {novo_diretorio}{Colors.ENDC}")
            
            elif opcao == "2":
                nova_saida = input(f"Novo diretório de saída (Enter para manter atual): ")
                if nova_saida:
                    self.saida = os.path.abspath(nova_saida)
                    os.makedirs(self.saida, exist_ok=True)
                    print(f"{Colors.GREEN}✅ Diretório de saída atualizado: {self.saida}{Colors.ENDC}")
            
            elif opcao == "3":
                print(f"\nFormatos disponíveis: markdown, html, pdf")
                novo_formato = input(f"Novo formato (Enter para manter atual): ")
                if novo_formato in ["markdown", "html", "pdf"]:
                    self.formato = novo_formato
                    print(f"{Colors.GREEN}✅ Formato atualizado: {self.formato}{Colors.ENDC}")
                elif novo_formato:
                    print(f"{Colors.RED}❌ Formato não suportado: {novo_formato}{Colors.ENDC}")
            
            elif opcao == "4":
                novo_intervalo = input(f"Novo intervalo em segundos (Enter para manter atual): ")
                if novo_intervalo and novo_intervalo.isdigit() and int(novo_intervalo) > 0:
                    self.intervalo = int(novo_intervalo)
                    print(f"{Colors.GREEN}✅ Intervalo atualizado: {self.intervalo} segundos{Colors.ENDC}")
                elif novo_intervalo:
                    print(f"{Colors.RED}❌ Intervalo inválido: {novo_intervalo}{Colors.ENDC}")
            
            elif opcao == "5":
                nova_porta = input(f"Nova porta (Enter para manter atual): ")
                if nova_porta and nova_porta.isdigit() and 1024 <= int(nova_porta) <= 65535:
                    self.porta = int(nova_porta)
                    print(f"{Colors.GREEN}✅ Porta atualizada: {self.porta}{Colors.ENDC}")
                elif nova_porta:
                    print(f"{Colors.RED}❌ Porta inválida: {nova_porta}{Colors.ENDC}")
        
        except Exception as e:
            print(f"{Colors.RED}❌ Erro ao atualizar configurações: {str(e)}{Colors.ENDC}")
        
        input("\nPressione Enter para continuar...")
    
    def executar(self) -> None:
        """Executa o loop principal do sistema."""
        # Configurar manipulador de sinais para encerramento limpo
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)
        
        while True:
            try:
                self.mostrar_menu()
                
                opcao = input(f"\nEscolha uma opção (1-9): ")
                
                if opcao == "1":
                    self.opcao_consultar()
                elif opcao == "2":
                    self.opcao_gerar_documentacao()
                elif opcao == "3":
                    self.opcao_gerar_documentacao_api()
                elif opcao == "4":
                    self.iniciar_agente()
                    input("\nPressione Enter para continuar...")
                elif opcao == "5":
                    self.parar_agente()
                    input("\nPressione Enter para continuar...")
                elif opcao == "6":
                    self.iniciar_servidor()
                    input("\nPressione Enter para continuar...")
                elif opcao == "7":
                    self.parar_servidor()
                    input("\nPressione Enter para continuar...")
                elif opcao == "8":
                    self.opcao_configuracoes()
                elif opcao == "9":
                    self._encerrar()
                    break
            
            except KeyboardInterrupt:
                if input(f"\n{Colors.YELLOW}Deseja sair? (s/N): {Colors.ENDC}").lower() == 's':
                    self._encerrar()
                    break
            
            except Exception as e:
                logger.error(f"Erro no loop principal: {e}")
                print(f"\n{Colors.RED}❌ Erro: {str(e)}{Colors.ENDC}")
                input("\nPressione Enter para continuar...")
    
    def _handle_signal(self, signum, frame) -> None:
        """Manipulador de sinais para encerramento limpo."""
        print(f"\n{Colors.YELLOW}Sinal recebido, encerrando...{Colors.ENDC}")
        self._encerrar()
        sys.exit(0)
    
    def _encerrar(self) -> None:
        """Encerra todos os componentes do sistema."""
        print(f"\n{Colors.YELLOW}Encerrando sistema...{Colors.ENDC}")
        
        if self.agente_rodando:
            self.parar_agente()
        
        if self.servidor_rodando:
            self.parar_servidor()
        
        print(f"{Colors.GREEN}✅ Sistema encerrado com sucesso{Colors.ENDC}")

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Documentação 4.0 - Sistema Completo",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                       help="Diretório do projeto (padrão: diretório atual)")
    parser.add_argument("--output", "-o", type=str, default=None,
                       help="Diretório de saída (padrão: ./docs)")
    parser.add_argument("--format", "-f", type=str, choices=["markdown", "html", "pdf"],
                       default="markdown", help="Formato da documentação")
    parser.add_argument("--interval", "-i", type=int, default=300,
                       help="Intervalo entre verificações do agente em segundos")
    parser.add_argument("--port", "-p", type=int, default=8000,
                       help="Porta para o servidor de documentação")
    parser.add_argument("--auto-start", "-a", action="store_true",
                       help="Iniciar automaticamente o agente e o servidor")
    
    args = parser.parse_args()
    
    # Inicializar o sistema
    sistema = DocumentationSystem()
    
    # Aplicar configurações da linha de comando
    sistema.diretorio = os.path.abspath(args.dir)
    if args.output:
        sistema.saida = os.path.abspath(args.output)
    else:
        sistema.saida = os.path.join(sistema.diretorio, "docs")
    sistema.formato = args.format
    sistema.intervalo = args.interval
    sistema.porta = args.port
    
    # Iniciar componentes se solicitado
    if args.auto_start:
        print(f"{Colors.BLUE}Iniciando componentes automaticamente...{Colors.ENDC}")
        sistema.iniciar_agente()
        sistema.iniciar_servidor()
    
    # Executar o sistema
    sistema.executar()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())