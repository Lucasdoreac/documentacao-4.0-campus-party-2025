#!/usr/bin/env python3
"""
Documentação 4.0 - Módulo de Consulta
Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

Este script implementa a funcionalidade de consulta à documentação usando Claude Code,
permitindo que os desenvolvedores façam perguntas em linguagem natural sobre o código.
"""

import os
import sys
import json
import argparse
import subprocess
import logging
from typing import Dict, Any, Optional, List

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('doc40-consulta')

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

def consultar_codigo(pergunta: str, diretorio: str, formato: str = "text", cache: bool = True) -> Dict[str, Any]:
    """
    Consulta o código usando Claude Code com busca agêntica avançada.
    
    Esta função utiliza o Claude Code CLI para fazer uma consulta agêntica sobre o código,
    permitindo perguntas em linguagem natural e recuperando respostas contextuais.
    
    Args:
        pergunta: A pergunta em linguagem natural
        diretorio: O diretório do projeto a ser consultado
        formato: O formato da saída (text, json, markdown)
        cache: Se deve usar cache para consultas (padrão: True)
        
    Returns:
        dict: A resposta processada contendo informações e fontes
    """
    logger.info(f"Consultando: {pergunta}")
    print(f"\n{Colors.BLUE}📝 Consultando: {pergunta}{Colors.ENDC}")
    
    # Validar diretório
    if not os.path.isdir(diretorio):
        logger.error(f"Diretório não encontrado: {diretorio}")
        print(f"{Colors.RED}❌ Diretório não encontrado: {diretorio}{Colors.ENDC}")
        return {"error": "DirectoryNotFound", "message": f"Diretório não encontrado: {diretorio}"}
    
    # Criar diretório de cache se não existir e cache estiver ativado
    cache_dir = os.path.join(diretorio, ".doc40", "cache", "queries")
    cache_file = None
    
    if cache:
        os.makedirs(cache_dir, exist_ok=True)
        # Hash da pergunta para nome do arquivo de cache
        import hashlib
        question_hash = hashlib.md5(pergunta.encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f"{question_hash}.json")
        
        # Verificar se existe cache válido (menos de 24h)
        if os.path.exists(cache_file):
            file_time = os.path.getmtime(cache_file)
            import time
            if time.time() - file_time < 86400:  # 24 horas
                try:
                    with open(cache_file, 'r') as f:
                        response = json.load(f)
                    logger.info(f"Usando resposta em cache para: {pergunta}")
                    print(f"{Colors.GREEN}✓ Usando resposta em cache{Colors.ENDC}")
                    
                    # Exibir a resposta
                    _exibir_resposta(response, pergunta, formato)
                    
                    return response
                except Exception as e:
                    logger.error(f"Erro ao ler cache: {e}")
    
    # Comando para o Claude Code CLI
    command = [
        "claude-code",
        "query",
        "--directory", diretorio,
        "--query", pergunta,
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
                
                # Exibir a resposta
                _exibir_resposta(response, pergunta, formato)
                
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

def _exibir_resposta(response: Dict[str, Any], pergunta: str, formato: str = "text") -> None:
    """
    Exibe a resposta da consulta no formato especificado.
    
    Args:
        response: A resposta da consulta
        pergunta: A pergunta original
        formato: O formato de exibição (text, json, markdown)
    """
    if "error" in response:
        print(f"{Colors.RED}❌ Erro: {response.get('message', 'Erro desconhecido')}{Colors.ENDC}")
        return
    
    if formato == "json":
        print(json.dumps(response, indent=2, ensure_ascii=False))
        return
    
    # Formato texto (padrão) ou markdown
    print("\n" + "="*50)
    print(f"{Colors.GREEN}🤖 Resposta para: {pergunta}{Colors.ENDC}")
    print("="*50)
    print(response.get("response", "Sem resposta"))
    print("="*50)
    print(f"{Colors.BLUE}Fontes:{Colors.ENDC}")
    
    # Ordenar fontes por relevância
    sources = sorted(
        response.get("sources", []),
        key=lambda x: x.get("relevance", 0),
        reverse=True
    )
    
    for fonte in sources:
        relevancia = fonte.get("relevance", "N/A")
        relevancia_formatada = relevancia if isinstance(relevancia, str) else f"{relevancia:.2f}"
        print(f"- {fonte.get('file')} (relevância: {relevancia_formatada})")

def modo_interativo(diretorio: str, formato: str = "text", cache: bool = True) -> None:
    """
    Inicia um modo interativo para consultas contínuas.
    
    Args:
        diretorio: O diretório do projeto
        formato: O formato da saída
        cache: Se deve usar cache
    """
    print(f"\n{Colors.BOLD}=== Modo Interativo de Consulta à Documentação ==={Colors.ENDC}")
    print(f"Digite suas perguntas ou 'sair' para encerrar.")
    print(f"Diretório: {diretorio}")
    
    try:
        while True:
            pergunta = input(f"\n{Colors.BOLD}Pergunta: {Colors.ENDC}")
            if pergunta.lower() in ['sair', 'exit', 'quit', 'q']:
                break
            
            if not pergunta.strip():
                continue
                
            consultar_codigo(pergunta, diretorio, formato, cache)
    except KeyboardInterrupt:
        print("\nModo interativo encerrado.")

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Documentação 4.0 - Consulta Agêntica de Código",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("--query", "-q", type=str,
                        help="Pergunta em linguagem natural sobre o código")
    parser.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                        help="Diretório do projeto (padrão: diretório atual)")
    parser.add_argument("--format", "-f", type=str, choices=["text", "json", "markdown"],
                        default="text", help="Formato da saída")
    parser.add_argument("--no-cache", action="store_true",
                        help="Desativar cache de consultas")
    parser.add_argument("--interactive", "-i", action="store_true",
                        help="Iniciar modo interativo para consultas contínuas")
    
    args = parser.parse_args()
    
    # Verificar se o Claude Code está instalado
    if not verificar_claude_code():
        return 1
    
    # Executar no modo interativo ou com uma única consulta
    if args.interactive:
        modo_interativo(args.dir, args.format, not args.no_cache)
    elif args.query:
        consultar_codigo(args.query, args.dir, args.format, not args.no_cache)
    else:
        parser.print_help()
        print(f"\n{Colors.YELLOW}⚠️ Forneça uma pergunta ou use o modo interativo.{Colors.ENDC}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())