#!/usr/bin/env python3
"""
Documentação 4.0 - Sistema Completo (LocalFirst)
Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

Este script implementa um sistema completo de Documentação 4.0 com abordagem LocalFirst,
incluindo consulta agêntica, geração de documentação, agente de manutenção e
integração com CI/CD, tudo em um único arquivo para facilitar o uso e distribuição.
"""

import os
import sys
import json
import time
import argparse
import subprocess
import threading
import logging
import re
import shutil
from datetime import datetime
from pathlib import Path
import http.server
import socketserver
import webbrowser
from typing import Dict, List, Optional, Tuple, Union, Any

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('doc40.log')
    ]
)
logger = logging.getLogger('doc40')

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

# Versão do script
VERSION = "1.0.0"

class ClaudeCodeIntegration:
    """Classe para integração com Claude Code CLI."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa a integração com Claude Code.
        
        Args:
            config: Configuração opcional
        """
        self.config = config or {}
        self.check_installation()
        
    def check_installation(self) -> bool:
        """
        Verifica se o Claude Code CLI está instalado.
        
        Returns:
            bool: True se estiver instalado, False caso contrário
        """
        try:
            result = subprocess.run(
                ["claude-code", "--version"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"Claude Code instalado: {version}")
                return True
            else:
                logger.warning("Claude Code instalado, mas não foi possível obter a versão")
                return True
        except Exception as e:
            logger.error(f"Claude Code não está instalado ou não está no PATH: {e}")
            print(f"\n{Colors.RED}Claude Code CLI não encontrado. Por favor, instale:"+
                  f"\n\ncurl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash{Colors.ENDC}\n")
            return False
            
    def check_api_key(self) -> bool:
        """
        Verifica se a API key está configurada.
        
        Returns:
            bool: True se a API key estiver configurada, False caso contrário
        """
        try:
            result = subprocess.run(
                ["claude-code", "config", "get", "api_key"], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0 and "api_key" in result.stdout:
                logger.info("API key configurada corretamente")
                return True
            else:
                logger.warning("API key não está configurada")
                print(f"\n{Colors.YELLOW}API key não configurada. Por favor, configure:"+
                      f"\n\nclaude-code config set api_key sk_ant_your_key_here{Colors.ENDC}\n")
                return False
        except Exception as e:
            logger.error(f"Erro ao verificar API key: {e}")
            return False
    
    def query(self, question: str, directory: str, cache: bool = True) -> Dict[str, Any]:
        """
        Consulta o código usando Claude Code.
        
        Args:
            question: A pergunta a ser feita
            directory: O diretório do projeto
            cache: Se deve usar cache (padrão: True)
            
        Returns:
            dict: A resposta processada
        """
        logger.info(f"Consultando: {question}")
        print(f"\n{Colors.BLUE}📝 Consultando: {question}{Colors.ENDC}")
        
        # Criar diretório de cache se não existir e cache estiver ativado
        cache_dir = os.path.join(directory, ".doc40", "cache", "queries")
        cache_file = None
        
        if cache:
            os.makedirs(cache_dir, exist_ok=True)
            # Hash da pergunta para nome do arquivo de cache
            import hashlib
            question_hash = hashlib.md5(question.encode()).hexdigest()
            cache_file = os.path.join(cache_dir, f"{question_hash}.json")
            
            # Verificar se existe cache válido (menos de 24h)
            if os.path.exists(cache_file):
                file_time = os.path.getmtime(cache_file)
                if time.time() - file_time < 86400:  # 24 horas
                    try:
                        with open(cache_file, 'r') as f:
                            response = json.load(f)
                        logger.info(f"Usando resposta em cache para: {question}")
                        print(f"{Colors.GREEN}✓ Usando resposta em cache{Colors.ENDC}")
                        return response
                    except Exception as e:
                        logger.error(f"Erro ao ler cache: {e}")
        
        # Comando para o Claude Code CLI
        command = [
            "claude-code",
            "query",
            "--directory", directory,
            "--query", question,
            "--output", "json"
        ]
        
        # Executar o comando
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Processar a resposta
            if result.returncode == 0:
                try:
                    response = json.loads(result.stdout)
                    
                    # Salvar no cache se ativado
                    if cache and cache_file:
                        with open(cache_file, 'w') as f:
                            json.dump(response, f)
                    
                    return response
                except json.JSONDecodeError as e:
                    logger.error(f"Erro ao processar resposta JSON: {e}")
                    print(f"{Colors.RED}❌ Erro ao processar a resposta{Colors.ENDC}")
                    return {"error": "JSONDecodeError", "message": str(e)}
            else:
                logger.error(f"Erro ao executar consulta: {result.stderr}")
                print(f"{Colors.RED}❌ Erro: {result.stderr}{Colors.ENDC}")
                return {"error": "CommandError", "message": result.stderr}
        except Exception as e:
            logger.error(f"Exceção ao executar consulta: {e}")
            print(f"{Colors.RED}❌ Exceção: {str(e)}{Colors.ENDC}")
            return {"error": "Exception", "message": str(e)}
    
    def generate_documentation(self, directory: str, format: str = "markdown", 
                              output_dir: str = "docs") -> Dict[str, Any]:
        """
        Gera documentação automaticamente a partir do código.
        
        Args:
            directory: O diretório do projeto
            format: O formato da documentação (markdown, html)
            output_dir: O diretório de saída
            
        Returns:
            dict: Resultado da operação
        """
        logger.info(f"Gerando documentação para: {directory}")
        print(f"\n{Colors.BLUE}🚀 Gerando documentação para: {directory}{Colors.ENDC}")
        print(f"{Colors.BLUE}📄 Formato: {format}{Colors.ENDC}")
        
        # Criar diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Comando para o Claude Code CLI
        command = [
            "claude-code",
            "document",
            "--directory", directory,
            "--format", format,
            "--output-dir", output_dir
        ]
        
        # Executar o comando
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Documentação gerada com sucesso em: {output_dir}")
                print(f"{Colors.GREEN}✅ Documentação gerada com sucesso em: {output_dir}{Colors.ENDC}")
                
                # Registrar a geração
                self._log_documentation_update(output_dir, "Geração inicial")
                
                return {
                    "success": True, 
                    "output_dir": output_dir,
                    "format": format
                }
            else:
                logger.error(f"Erro ao gerar documentação: {result.stderr}")
                print(f"{Colors.RED}❌ Erro: {result.stderr}{Colors.ENDC}")
                return {
                    "success": False, 
                    "error": result.stderr
                }
        except Exception as e:
            logger.error(f"Exceção ao gerar documentação: {e}")
            print(f"{Colors.RED}❌ Exceção: {str(e)}{Colors.ENDC}")
            return {
                "success": False, 
                "error": str(e)
            }
    
    def update_documentation(self, directory: str, commit_id: str, 
                           output_dir: str = "docs") -> Dict[str, Any]:
        """
        Atualiza a documentação com base nas mudanças do commit.
        
        Args:
            directory: O diretório do projeto
            commit_id: O ID do commit
            output_dir: O diretório de saída
            
        Returns:
            dict: Resultado da operação
        """
        logger.info(f"Atualizando documentação para commit: {commit_id[:8] if commit_id else 'N/A'}")
        print(f"\n{Colors.BLUE}🔄 Atualizando documentação para commit: {commit_id[:8] if commit_id else 'N/A'}{Colors.ENDC}")
        
        # Criar diretório de saída se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Comando para o Claude Code CLI
        command = [
            "claude-code",
            "update-docs",
            "--directory", directory,
            "--commit", commit_id,
            "--output-dir", output_dir
        ]
        
        # Executar o comando
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Documentação atualizada com sucesso em: {output_dir}")
                print(f"{Colors.GREEN}✅ Documentação atualizada com sucesso em: {output_dir}{Colors.ENDC}")
                
                # Registrar a atualização
                self._log_documentation_update(output_dir, f"Atualização para commit {commit_id[:8]}")
                
                return {
                    "success": True, 
                    "output_dir": output_dir,
                    "commit_id": commit_id
                }
            else:
                logger.error(f"Erro ao atualizar documentação: {result.stderr}")
                print(f"{Colors.RED}❌ Erro: {result.stderr}{Colors.ENDC}")
                return {
                    "success": False, 
                    "error": result.stderr
                }
        except Exception as e:
            logger.error(f"Exceção ao atualizar documentação: {e}")
            print(f"{Colors.RED}❌ Exceção: {str(e)}{Colors.ENDC}")
            return {
                "success": False, 
                "error": str(e)
            }
    
    def generate_code_with_docs(self, prompt: str, output_file: str, language: str = "python") -> Dict[str, Any]:
        """
        Gera código com documentação integrada.
        
        Args:
            prompt: O prompt para geração
            output_file: O arquivo de saída
            language: A linguagem de programação
            
        Returns:
            dict: Resultado da operação
        """
        logger.info(f"Gerando código para: {prompt}")
        print(f"\n{Colors.BLUE}🧠 Gerando código com documentação para: {prompt}{Colors.ENDC}")
        
        # Criar diretório de saída se não existir
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        
        # Adicionar contexto sobre documentação SOTA ao prompt
        enhanced_prompt = f"""
        {prompt}
        
        IMPORTANTE:
        1. O código deve seguir as melhores práticas de Documentação 4.0, incluindo:
           - Docstrings completos para classes, métodos e funções
           - Anotações de tipo (type hints) para todos os parâmetros e retornos
           - Exemplos de uso embutidos na documentação
           - Explicações claras do propósito e comportamento
        2. O código deve ser bem estruturado e seguir princípios SOLID
        3. Inclua validação robusta de entradas e tratamento de erros
        4. A linguagem é {language}
        """
        
        # Comando para o Claude Code CLI
        command = [
            "claude-code",
            "generate",
            "--prompt", enhanced_prompt,
            "--output", output_file
        ]
        
        # Executar o comando
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Código gerado com sucesso em: {output_file}")
                print(f"{Colors.GREEN}✅ Código gerado com sucesso em: {output_file}{Colors.ENDC}")
                
                # Ler o arquivo gerado para retornar seu conteúdo
                with open(output_file, 'r') as f:
                    content = f.read()
                
                return {
                    "success": True, 
                    "output_file": output_file,
                    "content": content
                }
            else:
                logger.error(f"Erro ao gerar código: {result.stderr}")
                print(f"{Colors.RED}❌ Erro: {result.stderr}{Colors.ENDC}")
                return {
                    "success": False, 
                    "error": result.stderr
                }
        except Exception as e:
            logger.error(f"Exceção ao gerar código: {e}")
            print(f"{Colors.RED}❌ Exceção: {str(e)}{Colors.ENDC}")
            return {
                "success": False, 
                "error": str(e)
            }
    
    def _log_documentation_update(self, output_dir: str, description: str) -> None:
        """
        Registra uma atualização de documentação no log.
        
        Args:
            output_dir: O diretório de saída
            description: Descrição da atualização
        """
        log_file = os.path.join(output_dir, "updates.log")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a') as f:
            f.write(f"{timestamp} - {description}\n")


class GitIntegration:
    """Classe para integração com Git."""
    
    def __init__(self, directory: str):
        """
        Inicializa a integração com Git.
        
        Args:
            directory: O diretório do repositório Git
        """
        self.directory = directory
        self.is_git_repo = self._check_git_repo()
    
    def _check_git_repo(self) -> bool:
        """
        Verifica se o diretório é um repositório Git.
        
        Returns:
            bool: True se for um repositório Git, False caso contrário
        """
        try:
            os.chdir(self.directory)
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"], 
                capture_output=True, 
                text=True
            )
            return result.returncode == 0 and result.stdout.strip() == "true"
        except Exception as e:
            logger.error(f"Erro ao verificar repositório Git: {e}")
            return False
    
    def get_current_commit(self) -> Optional[str]:
        """
        Obtém o commit atual.
        
        Returns:
            str: O ID do commit atual ou None se ocorrer um erro
        """
        if not self.is_git_repo:
            logger.warning(f"O diretório {self.directory} não é um repositório Git")
            return None
        
        try:
            os.chdir(self.directory)
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Erro ao obter commit atual: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Exceção ao obter commit atual: {e}")
            return None
    
    def get_changed_files(self, from_commit: str, to_commit: str = "HEAD") -> List[str]:
        """
        Obtém os arquivos alterados entre dois commits.
        
        Args:
            from_commit: O commit de origem
            to_commit: O commit de destino (padrão: HEAD)
            
        Returns:
            list: Lista de arquivos alterados
        """
        if not self.is_git_repo:
            logger.warning(f"O diretório {self.directory} não é um repositório Git")
            return []
        
        try:
            os.chdir(self.directory)
            result = subprocess.run(
                ["git", "diff", "--name-only", from_commit, to_commit], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                return [f.strip() for f in result.stdout.splitlines() if f.strip()]
            else:
                logger.error(f"Erro ao obter arquivos alterados: {result.stderr}")
                return []
        except Exception as e:
            logger.error(f"Exceção ao obter arquivos alterados: {e}")
            return []
    
    def get_commit_message(self, commit_id: str = "HEAD") -> Optional[str]:
        """
        Obtém a mensagem de um commit.
        
        Args:
            commit_id: O ID do commit (padrão: HEAD)
            
        Returns:
            str: A mensagem do commit ou None se ocorrer um erro
        """
        if not self.is_git_repo:
            logger.warning(f"O diretório {self.directory} não é um repositório Git")
            return None
        
        try:
            os.chdir(self.directory)
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=%B", commit_id], 
                capture_output=True, 
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.error(f"Erro ao obter mensagem do commit: {result.stderr}")
                return None
        except Exception as e:
            logger.error(f"Exceção ao obter mensagem do commit: {e}")
            return None
    
    def setup_git_hooks(self, hooks_dir: str = None) -> bool:
        """
        Configura hooks Git para integração com o sistema de documentação.
        
        Args:
            hooks_dir: Diretório para os hooks
            
        Returns:
            bool: True se os hooks foram configurados com sucesso, False caso contrário
        """
        if not self.is_git_repo:
            logger.warning(f"O diretório {self.directory} não é um repositório Git")
            return False
        
        try:
            os.chdir(self.directory)
            git_hooks_dir = os.path.join(self.directory, ".git", "hooks")
            
            # Conteúdo do hook post-commit
            post_commit_hook = """#!/bin/bash
# Documentação 4.0 - Post-Commit Hook
# Este hook é executado após cada commit para atualizar a documentação

# Caminho para o script doc40-completo.py
DOC40_SCRIPT="$(git rev-parse --show-toplevel)/doc40-completo.py"

if [ -f "$DOC40_SCRIPT" ]; then
    echo "Atualizando documentação após commit..."
    python3 "$DOC40_SCRIPT" update-docs
else
    echo "Script doc40-completo.py não encontrado em $DOC40_SCRIPT"
    exit 1
fi
"""
            
            # Gravar o hook
            post_commit_path = os.path.join(git_hooks_dir, "post-commit")
            with open(post_commit_path, 'w') as f:
                f.write(post_commit_hook)
            
            # Tornar o hook executável
            os.chmod(post_commit_path, 0o755)
            
            logger.info(f"Hooks Git configurados com sucesso em {git_hooks_dir}")
            print(f"{Colors.GREEN}✅ Hooks Git configurados com sucesso{Colors.ENDC}")
            return True
        except Exception as e:
            logger.error(f"Erro ao configurar hooks Git: {e}")
            print(f"{Colors.RED}❌ Erro ao configurar hooks Git: {e}{Colors.ENDC}")
            return False


class DocumentationServer:
    """Servidor HTTP simples para visualizar a documentação gerada."""
    
    def __init__(self, docs_dir: str, port: int = 8000):
        """
        Inicializa o servidor de documentação.
        
        Args:
            docs_dir: O diretório da documentação
            port: A porta para o servidor (padrão: 8000)
        """
        self.docs_dir = docs_dir
        self.port = port
        self.server = None
        self.server_thread = None
    
    def start(self) -> bool:
        """
        Inicia o servidor HTTP.
        
        Returns:
            bool: True se o servidor iniciou com sucesso, False caso contrário
        """
        try:
            os.chdir(self.docs_dir)
            
            # Criar um arquivo index.html se não existir
            index_path = os.path.join(self.docs_dir, "index.html")
            if not os.path.exists(index_path):
                self._create_index_html()
            
            # Iniciar o servidor em uma thread separada
            handler = http.server.SimpleHTTPRequestHandler
            self.server = socketserver.TCPServer(("", self.port), handler)
            
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            
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
        try:
            if self.server:
                self.server.shutdown()
                self.server.server_close()
                logger.info("Servidor parado")
                print(f"{Colors.YELLOW}ℹ️ Servidor parado{Colors.ENDC}")
                return True
            return False
        except Exception as e:
            logger.error(f"Erro ao parar servidor: {e}")
            print(f"{Colors.RED}❌ Erro ao parar servidor: {e}{Colors.ENDC}")
            return False
    
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
            for file in md_files:
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar seção de arquivos HTML
        if html_files:
            html_content += """
        <h2>Documentação HTML</h2>
        <ul>
"""
            for file in html_files:
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar seção de outros arquivos
        if other_files:
            html_content += """
        <h2>Outros Arquivos</h2>
        <ul>
"""
            for file in other_files:
                html_content += f'            <li><a href="{file}">{file}</a></li>\n'
            html_content += "        </ul>\n"
        
        # Adicionar rodapé
        html_content += """
        <footer>
            <p>Gerado por Documentação 4.0 - Campus Party 2025</p>
        </footer>
    </div>
</body>
</html>
"""
        
        # Salvar o arquivo
        with open(os.path.join(self.docs_dir, "index.html"), 'w') as f:
            f.write(html_content)


class DocumentationAgent:
    """Agente de monitoramento e manutenção de documentação."""
    
    def __init__(self, directory: str, output_dir: str = "docs", 
                 interval: int = 300, claude: ClaudeCodeIntegration = None):
        """
        Inicializa o agente de documentação.
        
        Args:
            directory: O diretório do projeto
            output_dir: O diretório de saída
            interval: O intervalo de verificação em segundos
            claude: Instância de ClaudeCodeIntegration
        """
        self.directory = directory
        self.output_dir = output_dir
        self.interval = interval
        self.claude = claude or ClaudeCodeIntegration()
        self.git = GitIntegration(directory)
        self.running = False
        self.agent_thread = None
        self.last_commit = self.git.get_current_commit()
    
    def start(self) -> bool:
        """
        Inicia o agente de documentação.
        
        Returns:
            bool: True se o agente iniciou com sucesso, False caso contrário
        """
        if not self.git.is_git_repo:
            logger.error(f"O diretório {self.directory} não é um repositório Git")
            print(f"{Colors.RED}❌ O diretório {self.directory} não é um repositório Git{Colors.ENDC}")
            return False
        
        if self.running:
            logger.warning("O agente já está em execução")
            print(f"{Colors.YELLOW}⚠️ O agente já está em execução{Colors.ENDC}")
            return False
        
        self.running = True
        self.agent_thread = threading.Thread(target=self._run)
        self.agent_thread.daemon = True
        self.agent_thread.start()
        
        logger.info(f"Agente iniciado com intervalo de {self.interval} segundos")
        print(f"{Colors.GREEN}✅ Agente iniciado com intervalo de {self.interval} segundos{Colors.ENDC}")
        
        return True
    
    def stop(self) -> bool:
        """
        Para o agente de documentação.
        
        Returns:
            bool: True se o agente parou com sucesso, False caso contrário
        """
        if not self.running:
            logger.warning("O agente não está em execução")
            print(f"{Colors.YELLOW}⚠️ O agente não está em execução{Colors.ENDC}")
            return False
        
        self.running = False
        self.agent_thread.join(timeout=2.0)
        
        logger.info("Agente parado")
        print(f"{Colors.YELLOW}ℹ️ Agente parado{Colors.ENDC}")
        
        return True
    
    def _run(self) -> None:
        """Loop principal do agente."""
        while self.running:
            try:
                # Obter o commit atual
                current_commit = self.git.get_current_commit()
                
                # Se houve mudança no commit
                if current_commit and current_commit != self.last_commit:
                    logger.info(f"Detectada mudança de commit: {self.last_commit[:8] if self.last_commit else 'Nenhum'} -> {current_commit[:8]}")
                    print(f"{Colors.BLUE}🔍 Detectada mudança de commit: {self.last_commit[:8] if self.last_commit else 'Nenhum'} -> {current_commit[:8]}{Colors.ENDC}")
                    
                    # Obter arquivos alterados
                    changed_files = self.git.get_changed_files(
                        self.last_commit if self.last_commit else current_commit + "^", 
                        current_commit
                    )
                    
                    # Obter mensagem do commit
                    commit_message = self.git.get_commit_message(current_commit)
                    
                    print(f"{Colors.BLUE}📄 Arquivos alterados: {len(changed_files)}{Colors.ENDC}")
                    print(f"{Colors.BLUE}📝 Mensagem do commit: {commit_message}{Colors.ENDC}")
                    
                    # Atualizar a documentação
                    self.claude.update_documentation(
                        self.directory, 
                        current_commit,
                        self.output_dir
                    )
                    
                    # Atualizar o último commit
                    self.last_commit = current_commit
                
                # Aguardar o próximo ciclo
                for _ in range(self.interval):
                    if not self.running:
                        break
                    time.sleep(1)
            
            except Exception as e:
                logger.error(f"Erro no agente: {e}")
                print(f"{Colors.RED}❌ Erro no agente: {e}{Colors.ENDC}")
                time.sleep(10)  # Esperar um pouco antes de tentar novamente


class DocumentationSystem:
    """Sistema completo de Documentação 4.0."""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa o sistema de documentação.
        
        Args:
            config: Configuração opcional
        """
        self.config = config or {}
        self.directory = self.config.get('directory', os.getcwd())
        self.output_dir = self.config.get('output_dir', os.path.join(self.directory, "docs"))
        self.interval = self.config.get('interval', 300)
        self.format = self.config.get('format', "markdown")
        self.port = self.config.get('port', 8000)
        
        # Criar diretório de saída se não existir
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Componentes do sistema
        self.claude = ClaudeCodeIntegration(self.config)
        self.git = GitIntegration(self.directory)
        self.agent = DocumentationAgent(
            self.directory, 
            self.output_dir,
            self.interval,
            self.claude
        )
        self.server = DocumentationServer(self.output_dir, self.port)
    
    def check_environment(self) -> Dict[str, bool]:
        """
        Verifica o ambiente de execução.
        
        Returns:
            dict: Resultado das verificações
        """
        logger.info("Verificando ambiente de execução")
        print(f"\n{Colors.BLUE}🔍 Verificando ambiente de execução{Colors.ENDC}")
        
        results = {
            "claude_code_installed": self.claude.check_installation(),
            "api_key_configured": self.claude.check_api_key(),
            "is_git_repo": self.git.is_git_repo
        }
        
        if all(results.values()):
            print(f"{Colors.GREEN}✅ Ambiente configurado corretamente{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}⚠️ Algumas verificações falharam. Consulte os logs para mais detalhes.{Colors.ENDC}")
        
        return results
    
    def generate_initial_documentation(self) -> Dict[str, Any]:
        """
        Gera a documentação inicial.
        
        Returns:
            dict: Resultado da operação
        """
        logger.info(f"Gerando documentação inicial para {self.directory}")
        print(f"\n{Colors.BLUE}🚀 Gerando documentação inicial para {self.directory}{Colors.ENDC}")
        
        result = self.claude.generate_documentation(
            self.directory,
            self.format,
            self.output_dir
        )
        
        return result
    
    def start_agent(self) -> bool:
        """
        Inicia o agente de manutenção.
        
        Returns:
            bool: True se o agente iniciou com sucesso, False caso contrário
        """
        return self.agent.start()
    
    def stop_agent(self) -> bool:
        """
        Para o agente de manutenção.
        
        Returns:
            bool: True se o agente parou com sucesso, False caso contrário
        """
        return self.agent.stop()
    
    def start_server(self) -> bool:
        """
        Inicia o servidor de documentação.
        
        Returns:
            bool: True se o servidor iniciou com sucesso, False caso contrário
        """
        return self.server.start()
    
    def stop_server(self) -> bool:
        """
        Para o servidor de documentação.
        
        Returns:
            bool: True se o servidor parou com sucesso, False caso contrário
        """
        return self.server.stop()
    
    def setup_git_hooks(self) -> bool:
        """
        Configura hooks Git.
        
        Returns:
            bool: True se os hooks foram configurados com sucesso, False caso contrário
        """
        return self.git.setup_git_hooks()
    
    def generate_code(self, prompt: str, output_file: str, language: str = "python") -> Dict[str, Any]:
        """
        Gera código com documentação integrada.
        
        Args:
            prompt: O prompt para geração
            output_file: O arquivo de saída
            language: A linguagem de programação
            
        Returns:
            dict: Resultado da operação
        """
        return self.claude.generate_code_with_docs(prompt, output_file, language)
    
    def search_documentation(self, query: str) -> Dict[str, Any]:
        """
        Pesquisa na documentação.
        
        Args:
            query: A consulta de pesquisa
            
        Returns:
            dict: Resultado da pesquisa
        """
        return self.claude.query(query, self.directory)
    
    def shutdown(self) -> None:
        """Encerra todos os componentes do sistema."""
        logger.info("Encerrando sistema de documentação")
        print(f"\n{Colors.YELLOW}🛑 Encerrando sistema de documentação{Colors.ENDC}")
        
        self.stop_agent()
        self.stop_server()


def print_welcome():
    """Exibe mensagem de boas-vindas."""
    print(f"""
{Colors.BLUE}{Colors.BOLD}======================================================{Colors.ENDC}
{Colors.BLUE}{Colors.BOLD}    Documentação 4.0 - Sistema Completo v{VERSION}{Colors.ENDC}
{Colors.BLUE}{Colors.BOLD}    Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz{Colors.ENDC}
{Colors.BLUE}{Colors.BOLD}======================================================{Colors.ENDC}

Este script implementa um sistema completo de Documentação 4.0,
incluindo consulta agêntica, geração de documentação, agente de 
manutenção e integração com CI/CD.

{Colors.YELLOW}Para ajuda:{Colors.ENDC} python doc40-completo.py --help
""")


def print_help():
    """Exibe ajuda detalhada."""
    print(f"""
{Colors.BLUE}{Colors.BOLD}DOCUMENTAÇÃO 4.0 - AJUDA DETALHADA{Colors.ENDC}

{Colors.YELLOW}Comandos disponíveis:{Colors.ENDC}

  {Colors.GREEN}init{Colors.ENDC}                  Inicializa o sistema e gera documentação inicial
    --dir DIR               Diretório do projeto (padrão: diretório atual)
    --output OUTPUT         Diretório de saída (padrão: ./docs)
    --format FORMAT         Formato da documentação (markdown, html)
    
  {Colors.GREEN}start-agent{Colors.ENDC}           Inicia o agente de manutenção de documentação
    --dir DIR               Diretório do projeto (padrão: diretório atual)
    --output OUTPUT         Diretório de saída (padrão: ./docs)
    --interval INTERVAL     Intervalo de verificação em segundos (padrão: 300)
    
  {Colors.GREEN}stop-agent{Colors.ENDC}            Para o agente de manutenção de documentação
    
  {Colors.GREEN}start-server{Colors.ENDC}          Inicia o servidor para visualizar a documentação
    --output OUTPUT         Diretório da documentação (padrão: ./docs)
    --port PORT             Porta do servidor (padrão: 8000)
    
  {Colors.GREEN}stop-server{Colors.ENDC}           Para o servidor de documentação
    
  {Colors.GREEN}update-docs{Colors.ENDC}           Atualiza a documentação manualmente
    --dir DIR               Diretório do projeto (padrão: diretório atual)
    --output OUTPUT         Diretório de saída (padrão: ./docs)
    
  {Colors.GREEN}setup-hooks{Colors.ENDC}           Configura hooks Git para atualização automática
    --dir DIR               Diretório do projeto (padrão: diretório atual)
    
  {Colors.GREEN}generate-code{Colors.ENDC}         Gera código com documentação integrada
    --prompt PROMPT         Prompt para geração de código
    --output OUTPUT         Arquivo de saída
    --language LANGUAGE     Linguagem de programação (padrão: python)
    
  {Colors.GREEN}search{Colors.ENDC}                Pesquisa na documentação
    --query QUERY           Consulta de pesquisa
    --dir DIR               Diretório do projeto (padrão: diretório atual)

{Colors.YELLOW}Exemplos:{Colors.ENDC}

  # Inicializar o sistema e gerar documentação inicial
  python doc40-completo.py init --dir ./meu-projeto --output ./docs
  
  # Iniciar o agente de manutenção
  python doc40-completo.py start-agent --interval 600
  
  # Iniciar o servidor de documentação
  python doc40-completo.py start-server --port 8080
  
  # Pesquisar na documentação
  python doc40-completo.py search --query "Como funciona a autenticação?"
  
  # Gerar código com documentação
  python doc40-completo.py generate-code --prompt "Crie uma classe para processamento de pagamentos" --output payment.py
""")


def parse_args():
    """
    Processa os argumentos de linha de comando.
    
    Returns:
        argparse.Namespace: Os argumentos processados
    """
    parser = argparse.ArgumentParser(
        description="Documentação 4.0 - Sistema Completo",
        add_help=False
    )
    
    # Argumentos gerais
    parser.add_argument('--help', '-h', action='store_true', 
                        help='Exibe ajuda detalhada')
    parser.add_argument('--version', '-v', action='store_true',
                        help='Exibe a versão do script')
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest='command')
    
    # Comando: init
    init_parser = subparsers.add_parser('init', 
                                        help='Inicializa o sistema e gera documentação inicial')
    init_parser.add_argument('--dir', default=os.getcwd(),
                            help='Diretório do projeto (padrão: diretório atual)')
    init_parser.add_argument('--output', default='docs',
                            help='Diretório de saída (padrão: ./docs)')
    init_parser.add_argument('--format', default='markdown', choices=['markdown', 'html'],
                            help='Formato da documentação (padrão: markdown)')
    
    # Comando: start-agent
    agent_parser = subparsers.add_parser('start-agent',
                                         help='Inicia o agente de manutenção de documentação')
    agent_parser.add_argument('--dir', default=os.getcwd(),
                             help='Diretório do projeto (padrão: diretório atual)')
    agent_parser.add_argument('--output', default='docs',
                             help='Diretório de saída (padrão: ./docs)')
    agent_parser.add_argument('--interval', type=int, default=300,
                             help='Intervalo de verificação em segundos (padrão: 300)')
    
    # Comando: stop-agent
    subparsers.add_parser('stop-agent',
                          help='Para o agente de manutenção de documentação')
    
    # Comando: start-server
    server_parser = subparsers.add_parser('start-server',
                                          help='Inicia o servidor para visualizar a documentação')
    server_parser.add_argument('--output', default='docs',
                              help='Diretório da documentação (padrão: ./docs)')
    server_parser.add_argument('--port', type=int, default=8000,
                              help='Porta do servidor (padrão: 8000)')
    
    # Comando: stop-server
    subparsers.add_parser('stop-server',
                          help='Para o servidor de documentação')
    
    # Comando: update-docs
    update_parser = subparsers.add_parser('update-docs',
                                          help='Atualiza a documentação manualmente')
    update_parser.add_argument('--dir', default=os.getcwd(),
                              help='Diretório do projeto (padrão: diretório atual)')
    update_parser.add_argument('--output', default='docs',
                              help='Diretório de saída (padrão: ./docs)')
    
    # Comando: setup-hooks
    hooks_parser = subparsers.add_parser('setup-hooks',
                                         help='Configura hooks Git para atualização automática')
    hooks_parser.add_argument('--dir', default=os.getcwd(),
                             help='Diretório do projeto (padrão: diretório atual)')
    
    # Comando: generate-code
    generate_parser = subparsers.add_parser('generate-code',
                                            help='Gera código com documentação integrada')
    generate_parser.add_argument('--prompt', required=True,
                                help='Prompt para geração de código')
    generate_parser.add_argument('--output', required=True,
                                help='Arquivo de saída')
    generate_parser.add_argument('--language', default='python',
                                help='Linguagem de programação (padrão: python)')
    
    # Comando: search
    search_parser = subparsers.add_parser('search',
                                          help='Pesquisa na documentação')
    search_parser.add_argument('--query', required=True,
                              help='Consulta de pesquisa')
    search_parser.add_argument('--dir', default=os.getcwd(),
                              help='Diretório do projeto (padrão: diretório atual)')
    
    return parser.parse_args()


def main():
    """Função principal."""
    args = parse_args()
    
    # Exibir versão
    if args.version:
        print(f"Documentação 4.0 - Sistema Completo v{VERSION}")
        return 0
    
    # Exibir ajuda detalhada
    if args.help:
        print_help()
        return 0
    
    # Exibir mensagem de boas-vindas
    print_welcome()
    
    # Sistema global
    system = None
    
    try:
        # Processamento de comandos
        if args.command == 'init':
            # Configurar o sistema
            config = {
                'directory': args.dir,
                'output_dir': os.path.join(args.dir, args.output),
                'format': args.format
            }
            system = DocumentationSystem(config)
            
            # Verificar ambiente
            system.check_environment()
            
            # Gerar documentação inicial
            system.generate_initial_documentation()
            
            # Iniciar servidor automaticamente
            if system.start_server():
                print(f"{Colors.GREEN}✓ Acesse a documentação em http://localhost:{system.port}{Colors.ENDC}")
            
            # Perguntar se deseja configurar hooks Git
            setup_hooks = input(f"\n{Colors.YELLOW}Deseja configurar hooks Git para atualização automática? (s/N): {Colors.ENDC}")
            if setup_hooks.lower() == 's':
                system.setup_git_hooks()
            
            # Perguntar se deseja iniciar o agente
            start_agent = input(f"\n{Colors.YELLOW}Deseja iniciar o agente de manutenção de documentação? (s/N): {Colors.ENDC}")
            if start_agent.lower() == 's':
                system.start_agent()
        
        elif args.command == 'start-agent':
            # Configurar o sistema
            config = {
                'directory': args.dir,
                'output_dir': os.path.join(args.dir, args.output),
                'interval': args.interval
            }
            system = DocumentationSystem(config)
            
            # Verificar ambiente
            system.check_environment()
            
            # Iniciar o agente
            system.start_agent()
        
        elif args.command == 'stop-agent':
            # Configurar o sistema
            system = DocumentationSystem()
            
            # Parar o agente
            system.stop_agent()
        
        elif args.command == 'start-server':
            # Configurar o sistema
            config = {
                'output_dir': args.output,
                'port': args.port
            }
            system = DocumentationSystem(config)
            
            # Iniciar o servidor
            if system.start_server():
                print(f"{Colors.GREEN}✓ Acesse a documentação em http://localhost:{args.port}{Colors.ENDC}")
                
                # Manter o script em execução
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print(f"\n{Colors.YELLOW}Servidor interrompido pelo usuário{Colors.ENDC}")
                    system.stop_server()
        
        elif args.command == 'stop-server':
            # Configurar o sistema
            system = DocumentationSystem()
            
            # Parar o servidor
            system.stop_server()
        
        elif args.command == 'update-docs':
            # Configurar o sistema
            config = {
                'directory': args.dir,
                'output_dir': os.path.join(args.dir, args.output)
            }
            system = DocumentationSystem(config)
            
            # Verificar ambiente
            system.check_environment()
            
            # Gerar documentação inicial
            system.generate_initial_documentation()
        
        elif args.command == 'setup-hooks':
            # Configurar o sistema
            config = {
                'directory': args.dir
            }
            system = DocumentationSystem(config)
            
            # Verificar ambiente
            system.check_environment()
            
            # Configurar hooks Git
            system.setup_git_hooks()
        
        elif args.command == 'generate-code':
            # Configurar o sistema
            system = DocumentationSystem()
            
            # Verificar ambiente
            system.check_environment()
            
            # Gerar código
            result = system.generate_code(args.prompt, args.output, args.language)
            
            if result.get('success'):
                print(f"{Colors.GREEN}✓ Código gerado com sucesso em {args.output}{Colors.ENDC}")
                
                # Exibir o começo do código gerado
                lines = result.get('content', '').split('\n')
                preview = '\n'.join(lines[:15])
                print(f"\n{Colors.BLUE}Primeiras linhas do código gerado:{Colors.ENDC}")
                print(f"{preview}\n...")
        
        elif args.command == 'search':
            # Configurar o sistema
            config = {
                'directory': args.dir
            }
            system = DocumentationSystem(config)
            
            # Verificar ambiente
            system.check_environment()
            
            # Pesquisar na documentação
            result = system.search_documentation(args.query)
            
            if 'error' not in result:
                print(f"\n{Colors.GREEN}=== Resposta para: {args.query} ==={Colors.ENDC}")
                print(result.get("response", "Sem resposta"))
                print(f"\n{Colors.BLUE}Fontes:{Colors.ENDC}")
                for source in result.get("sources", []):
                    print(f"- {source.get('file')} (relevância: {source.get('relevance', 'N/A')})")
        
        else:
            # Comando não especificado, mostrar ajuda resumida
            print(f"{Colors.YELLOW}Nenhum comando especificado. Use --help para ver os comandos disponíveis.{Colors.ENDC}")
            print("\nComandos básicos:")
            print(f"  {Colors.GREEN}init{Colors.ENDC}           Inicializa o sistema e gera documentação inicial")
            print(f"  {Colors.GREEN}start-agent{Colors.ENDC}    Inicia o agente de manutenção de documentação")
            print(f"  {Colors.GREEN}start-server{Colors.ENDC}   Inicia o servidor para visualizar a documentação")
            print(f"  {Colors.GREEN}search{Colors.ENDC}         Pesquisa na documentação")
    
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operação interrompida pelo usuário{Colors.ENDC}")
    
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        print(f"\n{Colors.RED}Erro inesperado: {e}{Colors.ENDC}")
    
    finally:
        # Encerrar o sistema se estiver inicializado
        if system:
            system.shutdown()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())