#!/bin/bash
# Instalação Rápida - Documentação 4.0 com Claude Code
# Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

# Cores para o terminal
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para exibir cabeçalho
mostrar_cabecalho() {
    echo -e "${BLUE}"
    echo "============================================================"
    echo "    🚀 INSTALAÇÃO RÁPIDA - DOCUMENTAÇÃO 4.0 COM CLAUDE CODE"
    echo "    Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz"
    echo "============================================================"
    echo -e "${NC}"
}

# Função para verificar requisitos
verificar_requisitos() {
    echo -e "\n${YELLOW}Verificando requisitos...${NC}"
    
    # Verificar Python
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✓ Python3 instalado${NC}"
        PYTHON_VERSION=$(python3 --version)
        echo -e "  ${BLUE}$PYTHON_VERSION${NC}"
    else
        echo -e "${RED}✗ Python3 não encontrado${NC}"
        echo -e "  Por favor, instale Python 3.8 ou superior: https://www.python.org/downloads/"
        exit 1
    fi
    
    # Verificar Git
    if command -v git &> /dev/null; then
        echo -e "${GREEN}✓ Git instalado${NC}"
        GIT_VERSION=$(git --version)
        echo -e "  ${BLUE}$GIT_VERSION${NC}"
    else
        echo -e "${RED}✗ Git não encontrado${NC}"
        echo -e "  Por favor, instale Git: https://git-scm.com/downloads"
        exit 1
    fi
    
    # Verificar curl
    if command -v curl &> /dev/null; then
        echo -e "${GREEN}✓ curl instalado${NC}"
    else
        echo -e "${RED}✗ curl não encontrado${NC}"
        echo -e "  Por favor, instale curl para baixar o Claude Code CLI"
        exit 1
    fi
}

# Função para instalar Claude Code CLI
instalar_claude_code() {
    echo -e "\n${YELLOW}Instalando Claude Code CLI...${NC}"
    
    if command -v claude-code &> /dev/null; then
        echo -e "${GREEN}✓ Claude Code CLI já está instalado${NC}"
        CLAUDE_VERSION=$(claude-code --version)
        echo -e "  ${BLUE}$CLAUDE_VERSION${NC}"
    else
        echo -e "${BLUE}Baixando e instalando Claude Code CLI...${NC}"
        
        # Determinar sistema operacional
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            echo -e "${BLUE}Sistema detectado: macOS${NC}"
            curl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            echo -e "${BLUE}Sistema detectado: Linux${NC}"
            curl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash
        elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
            # Windows
            echo -e "${BLUE}Sistema detectado: Windows${NC}"
            echo -e "${YELLOW}Execute o seguinte comando no PowerShell como administrador:${NC}"
            echo -e "iwr https://raw.githubusercontent.com/anthropic/claude-code/main/install.ps1 -OutFile install.ps1; ./install.ps1"
            exit 1
        else
            echo -e "${RED}Sistema operacional não suportado: $OSTYPE${NC}"
            exit 1
        fi
        
        # Verificar se a instalação foi bem-sucedida
        if command -v claude-code &> /dev/null; then
            echo -e "${GREEN}✓ Claude Code CLI instalado com sucesso${NC}"
            CLAUDE_VERSION=$(claude-code --version)
            echo -e "  ${BLUE}$CLAUDE_VERSION${NC}"
        else
            echo -e "${RED}✗ Falha ao instalar Claude Code CLI${NC}"
            exit 1
        fi
    fi
}

# Função para configurar a API key
configurar_api_key() {
    echo -e "\n${YELLOW}Configurando a API key do Claude...${NC}"
    
    read -p "Você já tem uma API key da Anthropic? (s/n): " tem_api_key
    
    if [[ $tem_api_key == "s" ]] || [[ $tem_api_key == "S" ]]; then
        read -p "Digite sua API key (sk_ant_...): " api_key
        
        if [[ $api_key == sk_ant_* ]]; then
            echo -e "${BLUE}Configurando API key...${NC}"
            claude-code config set api_key "$api_key"
            echo -e "${GREEN}✓ API key configurada com sucesso${NC}"
        else
            echo -e "${RED}✗ API key inválida. Deve começar com 'sk_ant_'${NC}"
            echo -e "${YELLOW}Você pode configurar manualmente mais tarde com:${NC}"
            echo -e "  claude-code config set api_key SUA_API_KEY"
        fi
    else
        echo -e "${YELLOW}Para obter uma API key:${NC}"
        echo -e "1. Acesse https://console.anthropic.com/"
        echo -e "2. Crie uma conta ou faça login"
        echo -e "3. Navegue até 'API Keys'"
        echo -e "4. Crie uma nova chave e copie-a"
        echo -e "5. Configure com: claude-code config set api_key SUA_API_KEY"
    fi
}

# Função para instalar dependências Python
instalar_dependencias() {
    echo -e "\n${YELLOW}Instalando dependências Python...${NC}"
    
    python3 -m pip install --upgrade pip
    
    echo -e "${BLUE}Instalando bibliotecas necessárias...${NC}"
    python3 -m pip install anthropic python-dotenv requests click rich
    
    echo -e "${GREEN}✓ Dependências instaladas com sucesso${NC}"
}

# Função para baixar scripts
baixar_scripts() {
    echo -e "\n${YELLOW}Baixando scripts de exemplo...${NC}"
    
    DIR_DESTINO="./doc40-scripts"
    mkdir -p "$DIR_DESTINO"
    
    cat > "$DIR_DESTINO/doc40-consulta.py" << 'EOF'
# doc40-consulta.py
import os
import subprocess
import json
import argparse

def consultar_codigo(pergunta, diretorio):
    """Consulta o código usando Claude Code."""
    print(f"📝 Consultando: {pergunta}")
    
    # Comando para o Claude Code CLI
    comando = [
        "claude-code",
        "query",
        "--directory", diretorio,
        "--query", pergunta,
        "--output", "json"
    ]
    
    # Executar o comando
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Verificar se houve erro
    if resultado.returncode != 0:
        print(f"❌ Erro: {resultado.stderr}")
        return None
    
    # Processar o resultado
    try:
        resposta = json.loads(resultado.stdout)
        return resposta
    except json.JSONDecodeError:
        print("❌ Erro ao processar a resposta")
        return None

def main():
    # Configurar argumentos
    parser = argparse.ArgumentParser(description="Consulta de Documentação 4.0")
    parser.add_argument("--dir", default=os.getcwd(), help="Diretório do projeto")
    parser.add_argument("--pergunta", help="Pergunta a ser feita (opcional)")
    
    args = parser.parse_args()
    
    # Se não foi fornecida uma pergunta, perguntar interativamente
    if args.pergunta:
        pergunta = args.pergunta
    else:
        print("\n" + "="*50)
        print("📚 CONSULTA DE DOCUMENTAÇÃO 4.0")
        print("="*50)
        print("Digite 'sair' para encerrar")
        print("="*50)
        
        while True:
            pergunta = input("\nSua pergunta: ")
            
            if pergunta.lower() == "sair":
                print("👋 Até logo!")
                break
            
            resposta = consultar_codigo(pergunta, args.dir)
            if resposta:
                print("\n" + "="*50)
                print(f"🤖 Resposta para: {pergunta}")
                print("="*50)
                print(resposta.get("response", "Sem resposta"))
                print("="*50)
                print("Fontes:")
                for fonte in resposta.get("sources", []):
                    print(f"- {fonte['file']} (relevância: {fonte.get('relevance', 'N/A')})")
                print()

if __name__ == "__main__":
    main()
EOF
    
    cat > "$DIR_DESTINO/doc40-gerador.py" << 'EOF'
# doc40-gerador.py
import os
import subprocess
import json
import argparse

def gerar_documentacao(diretorio, formato="markdown", saida="docs"):
    """Gera documentação automaticamente a partir do código."""
    print(f"🚀 Gerando documentação para: {diretorio}")
    print(f"📄 Formato: {formato}")
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Comando para o Claude Code CLI
    comando = [
        "claude-code",
        "document",
        "--directory", diretorio,
        "--format", formato,
        "--output-dir", saida
    ]
    
    # Executar o comando
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Verificar se houve erro
    if resultado.returncode != 0:
        print(f"❌ Erro: {resultado.stderr}")
        return False
    
    print(f"✅ Documentação gerada com sucesso em: {saida}")
    return True

def gerar_documentacao_api(diretorio, saida="docs/api"):
    """Gera documentação específica para API."""
    print(f"🚀 Gerando documentação de API para: {diretorio}")
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Comando para o Claude Code CLI
    comando = [
        "claude-code",
        "document-api",
        "--directory", diretorio,
        "--output-dir", saida,
        "--format", "openapi+markdown"  # Gera tanto OpenAPI quanto Markdown
    ]
    
    # Executar o comando
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Verificar se houve erro
    if resultado.returncode != 0:
        print(f"❌ Erro: {resultado.stderr}")
        return False
    
    print(f"✅ Documentação de API gerada com sucesso em: {saida}")
    return True

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Gerador de Documentação 4.0")
    parser.add_argument("--dir", default=os.getcwd(), help="Diretório do projeto")
    parser.add_argument("--formato", default="markdown", choices=["markdown", "html", "pdf"], help="Formato de saída")
    parser.add_argument("--saida", default="docs", help="Diretório de saída")
    parser.add_argument("--api", action="store_true", help="Gerar documentação de API")
    
    args = parser.parse_args()
    
    # Gerar documentação
    if args.api:
        gerar_documentacao_api(args.dir, os.path.join(args.saida, "api"))
    else:
        gerar_documentacao(args.dir, args.formato, args.saida)

if __name__ == "__main__":
    main()
EOF
    
    echo -e "${GREEN}✓ Scripts baixados para $DIR_DESTINO${NC}"
    echo -e "${BLUE}Scripts disponíveis:${NC}"
    echo -e "  - $DIR_DESTINO/doc40-consulta.py"
    echo -e "  - $DIR_DESTINO/doc40-gerador.py"
}

# Função para exibir instruções finais
exibir_instrucoes() {
    echo -e "\n${GREEN}🎉 Instalação concluída com sucesso!${NC}"
    echo -e "\n${YELLOW}Próximos passos:${NC}"
    echo -e "1. Configure sua API key (se ainda não o fez):"
    echo -e "   ${BLUE}claude-code config set api_key SUA_API_KEY${NC}"
    echo -e "2. Execute a consulta à documentação:"
    echo -e "   ${BLUE}python3 doc40-scripts/doc40-consulta.py --dir ./seu-projeto${NC}"
    echo -e "3. Gere documentação automática:"
    echo -e "   ${BLUE}python3 doc40-scripts/doc40-gerador.py --dir ./seu-projeto --formato markdown${NC}"
    echo -e "4. Para obter o guia completo, acesse:"
    echo -e "   ${BLUE}https://github.com/Lucasdoreac/doc40-campus-party${NC}"
    echo -e "\n${GREEN}Obrigado por usar o Instalador da Documentação 4.0!${NC}"
}

# Execução principal
mostrar_cabecalho
verificar_requisitos
instalar_claude_code
configurar_api_key
instalar_dependencias
baixar_scripts
exibir_instrucoes