#!/bin/bash
# Script de Demonstração Automática - Documentação 4.0 com Claude Code
# Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz
# Versão rápida para testes

# Definir cores para melhor visualização
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Caminho base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
DEMO_PROJECT_DIR="$BASE_DIR/demo-project"

# Abrir apresentação HTML
open_presentation() {
    if [ "$(uname)" == "Darwin" ]; then
        # macOS
        open "$BASE_DIR/doc40-slides-atualizados.html"
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Linux
        if command -v xdg-open > /dev/null; then
            xdg-open "$BASE_DIR/doc40-slides-atualizados.html"
        elif command -v firefox > /dev/null; then
            firefox "$BASE_DIR/doc40-slides-atualizados.html"
        elif command -v google-chrome > /dev/null; then
            google-chrome "$BASE_DIR/doc40-slides-atualizados.html"
        else
            echo "Não foi possível abrir o navegador automaticamente."
            echo "Por favor, abra manualmente o arquivo: $BASE_DIR/doc40-slides-atualizados.html"
        fi
    elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ] || [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
        # Windows
        start "$BASE_DIR/doc40-slides-atualizados.html"
    else
        echo "Não foi possível detectar o sistema operacional."
        echo "Por favor, abra manualmente o arquivo: $BASE_DIR/doc40-slides-atualizados.html"
    fi
}

# Função para mostrar título de seção
mostrar_secao() {
    local titulo="$1"
    echo ""
    echo -e "${BLUE}${BOLD}## $titulo ##${NC}"
    echo -e "${BLUE}${BOLD}$(printf '=%.0s' $(seq 1 $((${#titulo} + 6))))${NC}"
    echo ""
}

# Função para simular comando e resultado
simular_comando() {
    local comando="$1"
    local resultado="$2"
    
    echo -e "${YELLOW}$> ${GREEN}${comando}${NC}"
    echo -e "$resultado"
}

# Abrir a apresentação HTML
echo "Abrindo apresentação de slides..."
open_presentation

# Mostrar cabeçalho
clear
echo -e "${BLUE}${BOLD}"
echo "============================================================"
echo "    🚀 DEMONSTRAÇÃO AUTOMÁTICA - DOCUMENTAÇÃO 4.0"
echo "    Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz"
echo "============================================================"
echo -e "${NC}"
echo "Esta demonstração mostrará como funciona um sistema completo"
echo "de Documentação 4.0 usando Claude Code e técnicas de IA."
echo ""
echo "Versão rápida para testes - sem delays"
echo "A apresentação foi aberta no seu navegador"
echo ""

# Demo 1: Consulta à documentação
mostrar_secao "DEMO 1: CONSULTA À DOCUMENTAÇÃO"
echo "A busca agêntica permite fazer perguntas em linguagem natural sobre o código."
echo ""

simular_comando "claude-code query --directory $DEMO_PROJECT_DIR --query \"Como funciona a autenticação?\"" "
🔍 Explorando o repositório...
🤖 RESPOSTA:
O sistema de autenticação usa tokens JWT para autenticar usuários. 
O token é gerado no formato 'Bearer {api_key[:5]}...{api_key[-5:]}'

FONTES:
- src/api/auth.py (relevância: 0.95)
- api_module.py (relevância: 0.82)
"

# Demo 2: Geração de documentação
mostrar_secao "DEMO 2: GERAÇÃO DE DOCUMENTAÇÃO"
echo "Este processo analisa o código-fonte e gera documentação completa e estruturada."
echo ""

simular_comando "claude-code document --directory $DEMO_PROJECT_DIR --format markdown" "
📝 Analisando o código-fonte...
✅ Documentação gerada com sucesso em $DEMO_PROJECT_DIR/docs/api_module.md!
"

simular_comando "head -n 10 $DEMO_PROJECT_DIR/docs/api_module.md" "
# API de Pagamentos - Documentação

*Gerado automaticamente em: $(date +"%Y-%m-%d %H:%M:%S")*
*Autores: Lucas Dórea Cardoso, Aulus Diniz*

## Visão Geral

Este módulo implementa um processador de pagamentos com validação avançada e documentação integrada.
"

# Demo 3: Agente de manutenção
mostrar_secao "DEMO 3: AGENTE DE MANUTENÇÃO DE DOCUMENTAÇÃO"
echo "Este agente monitora mudanças no código e atualiza a documentação automaticamente."
echo ""

simular_comando "git commit -m \"feat: Adicionar parâmetro timeout\"" "
[main a1b2c3d] feat: Adicionar parâmetro timeout
 1 file changed, 5 insertions(+), 1 deletion(-)
"

simular_comando "claude-code update-docs --directory $DEMO_PROJECT_DIR --commit a1b2c3d" "
🔍 Analisando alterações no commit a1b2c3d...
✅ Documentação atualizada com sucesso!
✅ Arquivos atualizados:
   - $DEMO_PROJECT_DIR/docs/api_module.md
   - $DEMO_PROJECT_DIR/docs/api/openapi.json
"

# Demo 4: Geração de código com documentação
mostrar_secao "DEMO 4: GERAÇÃO DE CÓDIGO COM DOCUMENTAÇÃO INTEGRADA"
echo "Este é o auge da Documentação 4.0: código e documentação nascem juntos!"
echo ""

simular_comando "claude-code generate --prompt \"Crie um módulo para reembolsos\"" "
🧠 Pensando...
✅ Código gerado com sucesso em $DEMO_PROJECT_DIR/src/api/refunds.py!
"

simular_comando "head -n 15 $DEMO_PROJECT_DIR/src/api/refunds.py" "
\"\"\"
Módulo de Processamento de Reembolsos

Este módulo implementa um sistema completo para processamento de reembolsos
com validação e rastreamento completo.

Autores: Lucas Dórea Cardoso, Aulus Diniz
Data: $(date +\"%Y-%m-%d\")
\"\"\"

import datetime
import uuid
from typing import Dict, Any, Optional
\"\"\"
"

# Conclusão
mostrar_secao "CONCLUSÃO: DOCUMENTAÇÃO 4.0 COM CLAUDE CODE"

echo -e "${GREEN}✅ Busca Agêntica${NC}: Consultas em linguagem natural sobre o código"
echo -e "${GREEN}✅ Geração Automática${NC}: Documentação completa gerada a partir do código"
echo -e "${GREEN}✅ Manutenção Automática${NC}: Atualização da documentação ao mudar o código"
echo -e "${GREEN}✅ Geração de Código${NC}: Código e documentação nascem juntos"
echo -e "${GREEN}✅ Integração Contínua${NC}: Tudo integrado ao fluxo de desenvolvimento"
echo ""

echo "A Documentação 4.0 transforma documentação de um fardo em um ativo estratégico"
echo "que evolui automaticamente com seu código."
echo ""

echo -e "${BLUE}Para saber mais:${NC}"
echo -e "1. Consulte o guia prático: ${YELLOW}doc40-guia-pratico.md${NC}"
echo -e "2. Veja a apresentação completa: ${YELLOW}doc40-slides-atualizados.html${NC}"
echo -e "3. Explore os scripts de exemplo: ${YELLOW}doc40-*.py${NC}"
echo ""

echo -e "${BLUE}${BOLD}OBRIGADO POR ASSISTIR À DEMONSTRAÇÃO!${NC}"
echo -e "${BLUE}Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz${NC}"