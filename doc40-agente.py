#!/usr/bin/env python3
"""
Documentação 4.0 - Agente de Manutenção de Documentação
Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

Este script implementa um agente que monitora mudanças no código-fonte
e atualiza automaticamente a documentação quando detecta alterações.
"""

import os
import sys
import json
import time
import argparse
import subprocess
import threading
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('doc40-agente.log')
    ]
)
logger = logging.getLogger('doc40-agente')

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

def verificar_claude_code() -> bool:
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

def verificar_git(diretorio: str) -> bool:
    """
    Verifica se o diretório é um repositório Git.
    
    Args:
        diretorio: O diretório a verificar
        
    Returns:
        bool: True se for um repositório Git, False caso contrário
    """
    try:
        os.chdir(diretorio)
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception as e:
        logger.error(f"Erro ao verificar repositório Git: {e}")
        return False

def verificar_mudancas(diretorio: str, ultimo_commit: Optional[str] = None) -> Tuple[bool, Optional[str]]:
    """
    Verifica se houve mudanças no repositório desde o último commit.
    
    Args:
        diretorio: O diretório do repositório
        ultimo_commit: O último commit verificado
        
    Returns:
        tuple: (houve_mudancas, commit_atual)
    """
    # Mudar para o diretório do projeto
    os.chdir(diretorio)
    
    # Obter o último commit
    comando = ["git", "rev-parse", "HEAD"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        logger.error(f"Erro ao obter o último commit: {resultado.stderr}")
        return False, None
    
    commit_atual = resultado.stdout.strip()
    
    # Se não temos um commit anterior para comparar, apenas retornar o atual
    if ultimo_commit is None:
        return False, commit_atual
    
    # Se o commit atual é diferente do último, houve mudanças
    return commit_atual != ultimo_commit, commit_atual

def obter_arquivos_alterados(diretorio: str, commit_anterior: str, commit_atual: str) -> List[str]:
    """
    Obtém a lista de arquivos alterados entre dois commits.
    
    Args:
        diretorio: O diretório do repositório
        commit_anterior: O commit anterior
        commit_atual: O commit atual
        
    Returns:
        list: Lista de arquivos alterados
    """
    try:
        os.chdir(diretorio)
        comando = ["git", "diff", "--name-only", commit_anterior, commit_atual]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            logger.error(f"Erro ao obter arquivos alterados: {resultado.stderr}")
            return []
        
        # Filtrar apenas arquivos existentes (pode haver arquivos excluídos)
        arquivos = resultado.stdout.strip().split('\n')
        arquivos_existentes = [f for f in arquivos if f and os.path.exists(os.path.join(diretorio, f))]
        
        return arquivos_existentes
    except Exception as e:
        logger.error(f"Exceção ao obter arquivos alterados: {e}")
        return []

def obter_mensagem_commit(diretorio: str, commit_id: str) -> Optional[str]:
    """
    Obtém a mensagem de um commit.
    
    Args:
        diretorio: O diretório do repositório
        commit_id: O ID do commit
        
    Returns:
        str: A mensagem do commit ou None em caso de erro
    """
    try:
        os.chdir(diretorio)
        comando = ["git", "log", "-1", "--pretty=%B", commit_id]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            logger.error(f"Erro ao obter mensagem do commit: {resultado.stderr}")
            return None
        
        return resultado.stdout.strip()
    except Exception as e:
        logger.error(f"Exceção ao obter mensagem do commit: {e}")
        return None

def atualizar_documentacao(diretorio: str, commit_id: str, saida: str = "docs") -> Dict[str, Any]:
    """
    Atualiza a documentação com base nas mudanças do commit.
    
    Args:
        diretorio: O diretório do repositório
        commit_id: O ID do commit
        saida: O diretório de saída para a documentação atualizada
        
    Returns:
        dict: Resultado da operação
    """
    logger.info(f"Atualizando documentação para commit: {commit_id[:8] if commit_id else 'N/A'}")
    print(f"\n{Colors.BLUE}🔄 Atualizando documentação para commit: {commit_id[:8] if commit_id else 'N/A'}{Colors.ENDC}")
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Obter mensagem do commit para análise de contexto
    mensagem_commit = obter_mensagem_commit(diretorio, commit_id)
    if mensagem_commit:
        logger.info(f"Mensagem do commit: {mensagem_commit}")
        print(f"{Colors.BLUE}📝 Mensagem do commit: {mensagem_commit}{Colors.ENDC}")
    
    # Comando para o Claude Code CLI
    comando = [
        "claude-code",
        "update-docs",
        "--directory", diretorio,
        "--commit", commit_id,
        "--output-dir", saida
    ]
    
    # Registrar início
    inicio = datetime.now()
    
    # Executar o comando
    try:
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        # Registrar fim
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        # Verificar resultado
        if resultado.returncode == 0:
            logger.info(f"Documentação atualizada com sucesso em: {saida}")
            print(f"{Colors.GREEN}✅ Documentação atualizada com sucesso em: {saida}{Colors.ENDC}")
            print(f"{Colors.BLUE}⏱️ Tempo de execução: {duracao:.2f} segundos{Colors.ENDC}")
            
            # Registrar a atualização
            registro_atualizacao(saida, commit_id, mensagem_commit, duracao)
            
            return {
                "success": True,
                "output_dir": saida,
                "commit_id": commit_id,
                "message": mensagem_commit,
                "duration_seconds": duracao
            }
        else:
            logger.error(f"Erro ao atualizar documentação: {resultado.stderr}")
            print(f"{Colors.RED}❌ Erro ao atualizar documentação: {resultado.stderr}{Colors.ENDC}")
            return {
                "success": False,
                "error": "UpdateError",
                "message": resultado.stderr,
                "duration_seconds": duracao
            }
    except Exception as e:
        # Registrar fim em caso de exceção
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        logger.error(f"Exceção ao atualizar documentação: {e}")
        print(f"{Colors.RED}❌ Exceção ao atualizar documentação: {str(e)}{Colors.ENDC}")
        return {
            "success": False,
            "error": "Exception",
            "message": str(e),
            "duration_seconds": duracao
        }

def registro_atualizacao(diretorio_saida: str, commit_id: str, 
                      mensagem_commit: Optional[str], duracao: float) -> None:
    """
    Registra uma atualização de documentação no log.
    
    Args:
        diretorio_saida: O diretório de saída da documentação
        commit_id: O ID do commit
        mensagem_commit: A mensagem do commit
        duracao: A duração da atualização em segundos
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = os.path.join(diretorio_saida, "atualizacoes.log")
    
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - Documentação atualizada para commit {commit_id[:8]}\n")
        if mensagem_commit:
            f.write(f"  Mensagem: {mensagem_commit}\n")
        f.write(f"  Duração: {duracao:.2f} segundos\n")
        f.write("\n")

def configurar_git_hook(diretorio: str) -> bool:
    """
    Configura um hook Git para atualizar a documentação após cada commit.
    
    Args:
        diretorio: O diretório do repositório
        
    Returns:
        bool: True se o hook foi configurado com sucesso, False caso contrário
    """
    try:
        os.chdir(diretorio)
        hooks_dir = os.path.join(diretorio, ".git", "hooks")
        
        # Verificar se o diretório de hooks existe
        if not os.path.isdir(hooks_dir):
            logger.error(f"Diretório de hooks não encontrado: {hooks_dir}")
            print(f"{Colors.RED}❌ Diretório de hooks não encontrado: {hooks_dir}{Colors.ENDC}")
            return False
        
        # Conteúdo do hook post-commit
        hook_content = """#!/bin/bash
# Documentação 4.0 - Post-Commit Hook
# Este hook é executado após cada commit para atualizar a documentação

# Obter diretório raiz do repositório
REPO_ROOT=$(git rev-parse --show-toplevel)

# Executar o script de atualização da documentação
python3 "$REPO_ROOT/doc40-agente.py" atualizar --dir "$REPO_ROOT"

# Ou usar diretamente o Claude Code CLI
# claude-code update-docs --directory "$REPO_ROOT" --commit HEAD --output-dir "$REPO_ROOT/docs"
"""
        
        # Caminho do hook
        hook_path = os.path.join(hooks_dir, "post-commit")
        
        # Gravar o hook
        with open(hook_path, 'w') as f:
            f.write(hook_content)
        
        # Tornar o hook executável
        os.chmod(hook_path, 0o755)
        
        logger.info(f"Hook Git configurado com sucesso: {hook_path}")
        print(f"{Colors.GREEN}✅ Hook Git configurado com sucesso: {hook_path}{Colors.ENDC}")
        
        return True
    except Exception as e:
        logger.error(f"Erro ao configurar hook Git: {e}")
        print(f"{Colors.RED}❌ Erro ao configurar hook Git: {str(e)}{Colors.ENDC}")
        return False

def executar_agente(diretorio: str, saida: str = "docs", intervalo: int = 300) -> None:
    """
    Executa o agente de manutenção de documentação em um loop contínuo.
    
    Args:
        diretorio: O diretório do repositório
        saida: O diretório de saída para a documentação
        intervalo: O intervalo em segundos entre verificações
    """
    logger.info(f"Iniciando agente de manutenção de documentação")
    print(f"\n{Colors.BLUE}🤖 Iniciando agente de manutenção de documentação{Colors.ENDC}")
    print(f"{Colors.BLUE}📁 Diretório: {diretorio}{Colors.ENDC}")
    print(f"{Colors.BLUE}📂 Saída: {saida}{Colors.ENDC}")
    print(f"{Colors.BLUE}⏱️ Intervalo: {intervalo} segundos{Colors.ENDC}")
    
    # Verificar se o diretório é um repositório Git
    if not verificar_git(diretorio):
        logger.error(f"O diretório {diretorio} não é um repositório Git")
        print(f"{Colors.RED}❌ O diretório {diretorio} não é um repositório Git{Colors.ENDC}")
        return
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Inicializar o último commit
    _, ultimo_commit = verificar_mudancas(diretorio)
    logger.info(f"Commit inicial: {ultimo_commit[:8] if ultimo_commit else 'Nenhum'}")
    print(f"{Colors.BLUE}📌 Commit inicial: {ultimo_commit[:8] if ultimo_commit else 'Nenhum'}{Colors.ENDC}")
    
    try:
        # Loop principal do agente
        while True:
            try:
                # Verificar mudanças
                houve_mudancas, commit_atual = verificar_mudancas(diretorio, ultimo_commit)
                
                # Se houve mudanças, atualizar a documentação
                if houve_mudancas:
                    logger.info(f"Detectadas mudanças! Novo commit: {commit_atual[:8]}")
                    print(f"\n{Colors.YELLOW}🔍 Detectadas mudanças! Novo commit: {commit_atual[:8]}{Colors.ENDC}")
                    
                    # Obter arquivos alterados
                    arquivos_alterados = obter_arquivos_alterados(diretorio, ultimo_commit, commit_atual)
                    logger.info(f"Arquivos alterados: {len(arquivos_alterados)}")
                    
                    if arquivos_alterados:
                        print(f"{Colors.BLUE}📄 Arquivos alterados: {len(arquivos_alterados)}{Colors.ENDC}")
                        for arquivo in arquivos_alterados[:5]:  # Mostrar apenas os primeiros 5
                            print(f"  - {arquivo}")
                        if len(arquivos_alterados) > 5:
                            print(f"  ... e mais {len(arquivos_alterados) - 5} arquivo(s)")
                    
                    # Atualizar a documentação
                    atualizar_documentacao(diretorio, commit_atual, saida)
                    ultimo_commit = commit_atual
                
                # Aguardar o próximo ciclo
                time.sleep(intervalo)
                
            except KeyboardInterrupt:
                raise  # Repassar para ser tratado no bloco principal
                
            except Exception as e:
                logger.error(f"Erro no ciclo do agente: {e}")
                print(f"{Colors.RED}❌ Erro no ciclo do agente: {str(e)}{Colors.ENDC}")
                print(f"{Colors.YELLOW}⚠️ Aguardando próximo ciclo...{Colors.ENDC}")
                time.sleep(intervalo)
    
    except KeyboardInterrupt:
        logger.info("Agente interrompido pelo usuário")
        print(f"\n{Colors.YELLOW}⏹️ Agente interrompido pelo usuário{Colors.ENDC}")

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Documentação 4.0 - Agente de Manutenção de Documentação",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando: iniciar (padrão)
    parser_iniciar = subparsers.add_parser("iniciar", help="Iniciar o agente de manutenção")
    parser_iniciar.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                               help="Diretório do projeto (padrão: diretório atual)")
    parser_iniciar.add_argument("--saida", "-o", type=str, default="docs",
                               help="Diretório de saída")
    parser_iniciar.add_argument("--intervalo", "-i", type=int, default=300,
                               help="Intervalo entre verificações em segundos")
    
    # Comando: atualizar
    parser_atualizar = subparsers.add_parser("atualizar", help="Atualizar documentação manualmente")
    parser_atualizar.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                                 help="Diretório do projeto (padrão: diretório atual)")
    parser_atualizar.add_argument("--saida", "-o", type=str, default="docs",
                                 help="Diretório de saída")
    parser_atualizar.add_argument("--commit", "-c", type=str, default="HEAD",
                                 help="ID do commit (padrão: HEAD)")
    
    # Comando: configurar-hook
    parser_hook = subparsers.add_parser("configurar-hook", help="Configurar hook Git para atualização automática")
    parser_hook.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                            help="Diretório do projeto (padrão: diretório atual)")
    
    args = parser.parse_args()
    
    # Verificar se o Claude Code está instalado
    if not verificar_claude_code():
        return 1
    
    # Executar o comando especificado ou o padrão (iniciar)
    if args.command == "atualizar":
        if not verificar_git(args.dir):
            logger.error(f"O diretório {args.dir} não é um repositório Git")
            print(f"{Colors.RED}❌ O diretório {args.dir} não é um repositório Git{Colors.ENDC}")
            return 1
        
        atualizar_documentacao(args.dir, args.commit, args.saida)
    
    elif args.command == "configurar-hook":
        if not verificar_git(args.dir):
            logger.error(f"O diretório {args.dir} não é um repositório Git")
            print(f"{Colors.RED}❌ O diretório {args.dir} não é um repositório Git{Colors.ENDC}")
            return 1
        
        configurar_git_hook(args.dir)
    
    else:  # Padrão: "iniciar" ou nenhum comando
        executar_agente(
            args.dir if hasattr(args, 'dir') else os.getcwd(),
            args.saida if hasattr(args, 'saida') else "docs",
            args.intervalo if hasattr(args, 'intervalo') else 300
        )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())