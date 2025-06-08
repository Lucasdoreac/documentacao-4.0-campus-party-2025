#!/usr/bin/env python3
"""
Documentação 4.0 - Módulo de Geração de Documentação
Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

Este script implementa a funcionalidade de geração automática de documentação
a partir do código-fonte, criando documentação estruturada em vários formatos.
"""

import os
import sys
import json
import argparse
import subprocess
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('doc40-gerador')

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

def gerar_documentacao(diretorio: str, formato: str = "markdown", 
                     saida: str = "docs", escopo: str = "all") -> Dict[str, Any]:
    """
    Gera documentação completa a partir do código-fonte.
    
    Esta função utiliza o Claude Code CLI para analisar o código-fonte e
    gerar documentação estruturada no formato especificado.
    
    Args:
        diretorio: Diretório do projeto
        formato: Formato da documentação (markdown, html, pdf)
        saida: Diretório de saída para a documentação
        escopo: Escopo da documentação (all, api, internal, public)
        
    Returns:
        dict: Resultado da operação com detalhes e estatísticas
    """
    logger.info(f"Gerando documentação para: {diretorio}")
    print(f"\n{Colors.BLUE}🚀 Gerando documentação para: {diretorio}{Colors.ENDC}")
    print(f"{Colors.BLUE}📄 Formato: {formato}{Colors.ENDC}")
    print(f"{Colors.BLUE}📂 Saída: {saida}{Colors.ENDC}")
    
    # Validar diretório
    if not os.path.isdir(diretorio):
        logger.error(f"Diretório não encontrado: {diretorio}")
        print(f"{Colors.RED}❌ Diretório não encontrado: {diretorio}{Colors.ENDC}")
        return {
            "success": False,
            "error": "DirectoryNotFound",
            "message": f"Diretório não encontrado: {diretorio}"
        }
    
    # Validar formato
    formatos_suportados = ["markdown", "html", "pdf", "json", "openapi"]
    if formato not in formatos_suportados:
        logger.error(f"Formato não suportado: {formato}")
        print(f"{Colors.RED}❌ Formato não suportado: {formato}{Colors.ENDC}")
        print(f"{Colors.YELLOW}Formatos suportados: {', '.join(formatos_suportados)}{Colors.ENDC}")
        return {
            "success": False,
            "error": "UnsupportedFormat",
            "message": f"Formato não suportado: {formato}"
        }
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Preparar comando base
    base_command = [
        "claude-code",
        "document",
        "--directory", diretorio,
        "--format", formato,
        "--output-dir", saida
    ]
    
    # Adicionar escopo se especificado
    if escopo != "all":
        base_command.extend(["--scope", escopo])
    
    # Registrar início
    inicio = datetime.now()
    print(f"\n{Colors.BLUE}⏱️ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # Executar o comando
    try:
        print(f"\n{Colors.YELLOW}Analisando o código-fonte...{Colors.ENDC}")
        result = subprocess.run(base_command, capture_output=True, text=True)
        
        # Registrar fim
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        # Verificar resultado
        if result.returncode == 0:
            logger.info(f"Documentação gerada com sucesso em: {saida}")
            print(f"\n{Colors.GREEN}✅ Documentação gerada com sucesso em: {saida}{Colors.ENDC}")
            print(f"{Colors.BLUE}⏱️ Tempo de execução: {duracao:.2f} segundos{Colors.ENDC}")
            
            # Listar arquivos gerados
            arquivos_gerados = []
            for root, _, files in os.walk(saida):
                for file in files:
                    if file.endswith(('.md', '.html', '.pdf', '.json')):
                        caminho_relativo = os.path.relpath(os.path.join(root, file), saida)
                        arquivos_gerados.append(caminho_relativo)
            
            print(f"\n{Colors.BLUE}📄 Arquivos gerados:{Colors.ENDC}")
            for arquivo in sorted(arquivos_gerados):
                print(f"  - {arquivo}")
            
            # Registrar a geração no log
            log_file = os.path.join(saida, "geracoes.log")
            with open(log_file, "a") as f:
                f.write(f"{inicio.strftime('%Y-%m-%d %H:%M:%S')} - Geração de documentação em formato {formato}\n")
                f.write(f"  Duração: {duracao:.2f} segundos\n")
                f.write(f"  Arquivos gerados: {len(arquivos_gerados)}\n")
                f.write("\n")
            
            return {
                "success": True,
                "output_dir": saida,
                "format": formato,
                "duration_seconds": duracao,
                "files_generated": len(arquivos_gerados),
                "file_list": arquivos_gerados
            }
        else:
            logger.error(f"Erro ao gerar documentação: {result.stderr}")
            print(f"\n{Colors.RED}❌ Erro ao gerar documentação:{Colors.ENDC}")
            print(result.stderr)
            return {
                "success": False,
                "error": "GenerationError",
                "message": result.stderr,
                "duration_seconds": duracao
            }
    except Exception as e:
        # Registrar fim em caso de exceção
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        logger.error(f"Exceção ao gerar documentação: {e}")
        print(f"\n{Colors.RED}❌ Exceção ao gerar documentação: {str(e)}{Colors.ENDC}")
        return {
            "success": False,
            "error": "Exception",
            "message": str(e),
            "duration_seconds": duracao
        }

def gerar_documentacao_api(diretorio: str, formato: str = "openapi", 
                        saida: str = "docs/api") -> Dict[str, Any]:
    """
    Gera documentação específica para APIs.
    
    Esta função foca na geração de documentação para APIs,
    utilizando formatos como OpenAPI (Swagger).
    
    Args:
        diretorio: Diretório do projeto
        formato: Formato da documentação (openapi, markdown, html)
        saida: Diretório de saída para a documentação
        
    Returns:
        dict: Resultado da operação com detalhes e estatísticas
    """
    logger.info(f"Gerando documentação de API para: {diretorio}")
    print(f"\n{Colors.BLUE}🚀 Gerando documentação de API para: {diretorio}{Colors.ENDC}")
    print(f"{Colors.BLUE}📄 Formato: {formato}{Colors.ENDC}")
    print(f"{Colors.BLUE}📂 Saída: {saida}{Colors.ENDC}")
    
    # Validar diretório
    if not os.path.isdir(diretorio):
        logger.error(f"Diretório não encontrado: {diretorio}")
        print(f"{Colors.RED}❌ Diretório não encontrado: {diretorio}{Colors.ENDC}")
        return {
            "success": False,
            "error": "DirectoryNotFound",
            "message": f"Diretório não encontrado: {diretorio}"
        }
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Comando para o Claude Code CLI
    command = [
        "claude-code",
        "document-api",  # Comando específico para documentação de API
        "--directory", diretorio,
        "--format", formato,
        "--output-dir", saida
    ]
    
    # Registrar início
    inicio = datetime.now()
    print(f"\n{Colors.BLUE}⏱️ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}")
    
    # Executar o comando
    try:
        print(f"\n{Colors.YELLOW}Analisando APIs e endpoints...{Colors.ENDC}")
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Registrar fim
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        # Verificar resultado
        if result.returncode == 0:
            logger.info(f"Documentação de API gerada com sucesso em: {saida}")
            print(f"\n{Colors.GREEN}✅ Documentação de API gerada com sucesso em: {saida}{Colors.ENDC}")
            print(f"{Colors.BLUE}⏱️ Tempo de execução: {duracao:.2f} segundos{Colors.ENDC}")
            
            # Listar arquivos gerados
            arquivos_gerados = []
            for root, _, files in os.walk(saida):
                for file in files:
                    if file.endswith(('.json', '.yaml', '.md', '.html')):
                        caminho_relativo = os.path.relpath(os.path.join(root, file), saida)
                        arquivos_gerados.append(caminho_relativo)
            
            print(f"\n{Colors.BLUE}📄 Arquivos gerados:{Colors.ENDC}")
            for arquivo in sorted(arquivos_gerados):
                print(f"  - {arquivo}")
            
            # Detectar arquivo principal OpenAPI
            arquivo_openapi = None
            for arquivo in arquivos_gerados:
                if arquivo.endswith(('openapi.json', 'openapi.yaml', 'swagger.json', 'swagger.yaml')):
                    arquivo_openapi = arquivo
                    break
            
            if arquivo_openapi:
                print(f"\n{Colors.GREEN}📄 Arquivo principal OpenAPI: {arquivo_openapi}{Colors.ENDC}")
            
            return {
                "success": True,
                "output_dir": saida,
                "format": formato,
                "duration_seconds": duracao,
                "files_generated": len(arquivos_gerados),
                "file_list": arquivos_gerados,
                "openapi_file": arquivo_openapi
            }
        else:
            logger.error(f"Erro ao gerar documentação de API: {result.stderr}")
            print(f"\n{Colors.RED}❌ Erro ao gerar documentação de API:{Colors.ENDC}")
            print(result.stderr)
            return {
                "success": False,
                "error": "APIDocGenerationError",
                "message": result.stderr,
                "duration_seconds": duracao
            }
    except Exception as e:
        # Registrar fim em caso de exceção
        fim = datetime.now()
        duracao = (fim - inicio).total_seconds()
        
        logger.error(f"Exceção ao gerar documentação de API: {e}")
        print(f"\n{Colors.RED}❌ Exceção ao gerar documentação de API: {str(e)}{Colors.ENDC}")
        return {
            "success": False,
            "error": "Exception",
            "message": str(e),
            "duration_seconds": duracao
        }

def main():
    """Função principal do script."""
    parser = argparse.ArgumentParser(
        description="Documentação 4.0 - Geração Automática de Documentação",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando: geral (padrão)
    parser_geral = subparsers.add_parser("geral", help="Gerar documentação geral do projeto")
    parser_geral.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                             help="Diretório do projeto (padrão: diretório atual)")
    parser_geral.add_argument("--formato", "-f", type=str, default="markdown",
                             choices=["markdown", "html", "pdf"],
                             help="Formato da documentação")
    parser_geral.add_argument("--saida", "-o", type=str, default="docs",
                             help="Diretório de saída")
    parser_geral.add_argument("--escopo", "-s", type=str, default="all",
                             choices=["all", "api", "internal", "public"],
                             help="Escopo da documentação")
    
    # Comando: api
    parser_api = subparsers.add_parser("api", help="Gerar documentação específica para APIs")
    parser_api.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                           help="Diretório do projeto (padrão: diretório atual)")
    parser_api.add_argument("--formato", "-f", type=str, default="openapi",
                           choices=["openapi", "markdown", "html"],
                           help="Formato da documentação de API")
    parser_api.add_argument("--saida", "-o", type=str, default="docs/api",
                           help="Diretório de saída")
    
    # Comando: tudo
    parser_tudo = subparsers.add_parser("tudo", help="Gerar toda a documentação (geral + API)")
    parser_tudo.add_argument("--dir", "-d", type=str, default=os.getcwd(),
                            help="Diretório do projeto (padrão: diretório atual)")
    parser_tudo.add_argument("--saida", "-o", type=str, default="docs",
                            help="Diretório de saída base")
    
    args = parser.parse_args()
    
    # Verificar se o Claude Code está instalado
    if not verificar_claude_code():
        return 1
    
    # Executar o comando especificado ou o padrão (geral)
    if args.command == "api":
        gerar_documentacao_api(args.dir, args.formato, args.saida)
    elif args.command == "tudo":
        # Gerar documentação geral
        print(f"{Colors.BOLD}=== Gerando Documentação Geral ==={Colors.ENDC}")
        geral_result = gerar_documentacao(args.dir, "markdown", args.saida)
        
        # Gerar documentação de API
        print(f"\n{Colors.BOLD}=== Gerando Documentação de API ==={Colors.ENDC}")
        api_result = gerar_documentacao_api(args.dir, "openapi", os.path.join(args.saida, "api"))
        
        # Resumo
        print(f"\n{Colors.BOLD}=== Resumo da Geração ==={Colors.ENDC}")
        print(f"Documentação Geral: {'✅ Sucesso' if geral_result.get('success') else '❌ Falha'}")
        print(f"Documentação API: {'✅ Sucesso' if api_result.get('success') else '❌ Falha'}")
    else:  # Padrão: "geral" ou nenhum comando
        gerar_documentacao(
            args.dir if hasattr(args, 'dir') else os.getcwd(),
            args.formato if hasattr(args, 'formato') else "markdown",
            args.saida if hasattr(args, 'saida') else "docs",
            args.escopo if hasattr(args, 'escopo') else "all"
        )
    
    return 0

if __name__ == "__main__":
    sys.exit(main())