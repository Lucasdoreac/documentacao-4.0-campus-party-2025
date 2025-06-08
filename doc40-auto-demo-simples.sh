#!/bin/bash
# Script de Demonstração Automática - Documentação 4.0 com Claude Code
# Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

# Definir cores para melhor visualização
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Função para exibir cabeçalho
mostrar_cabecalho() {
    # Abrir a apresentação HTML
    echo "Abrindo apresentação de slides..."
    open_presentation
    sleep 1

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
    echo "A demonstração é totalmente automática. Sente-se e aproveite!"
    echo "A apresentação foi aberta no seu navegador."
    echo ""
    echo -e "${YELLOW}A demonstração começará em 5 segundos...${NC}"
    sleep 5
}

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

# Função para simular digitação
simular_digitacao() {
    local texto="$1"
    local velocidade=${2:-0.03}
    
    for (( i=0; i<${#texto}; i++ )); do
        echo -n "${texto:$i:1}"
        sleep $velocidade
    done
    echo ""
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
    local tempo_espera=${3:-1}
    
    echo -e "${YELLOW}$> ${GREEN}${comando}${NC}"
    sleep $tempo_espera
    echo -e "$resultado"
    sleep 1
}

# Função para limpar a tela e esperar
limpar_e_esperar() {
    local tempo=${1:-3}
    sleep $tempo
    clear
}

# Função para demo de consulta de documentação
demo_consulta() {
    mostrar_secao "DEMO 1: CONSULTA À DOCUMENTAÇÃO"
    
    simular_digitacao "Primeiro, vamos ver como consultar documentação usando busca agêntica."
    simular_digitacao "A busca agêntica permite fazer perguntas em linguagem natural sobre o código."
    echo ""
    
    # Simular uma consulta
    simular_digitacao "Vamos perguntar: Como funciona o sistema de autenticação?" 0.05
    sleep 1
    
    # Simular execução do comando
    simular_comando "claude-code query --directory $DEMO_PROJECT_DIR --query \"Como funciona a autenticação neste sistema?\"" "
🔍 Explorando o repositório...
📂 Analisando arquivos relevantes...
💡 Processando informações...

🤖 RESPOSTA:
O sistema de autenticação usa tokens JWT para autenticar usuários. O fluxo funciona da seguinte forma:

1. O usuário fornece suas credenciais através da função 'authenticate' em auth.py
2. A função verifica se a API key tem pelo menos 10 caracteres
3. Se válida, gera um token no formato 'Bearer {api_key[:5]}...{api_key[-5:]}'
4. Este token deve ser incluído em todas as requisições subsequentes
5. O token é verificado antes de permitir acesso às operações protegidas

Para uma API key como 'abcdefghijklmnopqrst', o token gerado seria 'Bearer abcde...pqrst'.

FONTES:
- src/api/auth.py (relevância: 0.95)
- api_module.py (relevância: 0.82)
"
    
    simular_digitacao "O sistema encontrou as informações relevantes na base de código!" 0.03
    simular_digitacao "Note como ele explorou o repositório e forneceu detalhes precisos." 0.03
    simular_digitacao "Agora, vamos fazer outra pergunta..." 0.03
    sleep 1
    
    # Simular outra consulta
    simular_digitacao "Vamos perguntar: Como faço para processar um pagamento?" 0.05
    sleep 1
    
    # Simular execução do segundo comando
    simular_comando "claude-code query --directory $DEMO_PROJECT_DIR --query \"Como faço para processar um pagamento?\"" "
🔍 Explorando o repositório...
📂 Analisando arquivos relevantes...
💡 Processando informações...

🤖 RESPOSTA:
Para processar um pagamento, você deve usar a classe PaymentProcessor da seguinte forma:

1. Primeiro, inicialize o processador com sua API key:
   processor = PaymentProcessor(api_key=\"sua_api_key\")

2. Em seguida, chame o método process_payment com os parâmetros necessários:
   result = processor.process_payment(
       amount=100.50,             # Valor da transação (obrigatório)
       payment_method=\"credit_card\", # Método de pagamento (obrigatório)
       customer_id=\"cus_123456\",     # ID do cliente (obrigatório)
       currency=\"USD\",              # Moeda (opcional, padrão: USD)
       metadata={\"invoice_id\": \"inv_987\"} # Dados adicionais (opcional)
   )

3. O resultado será um dicionário com os detalhes da transação:
   {
       \"transaction_id\": \"tr_123456\",
       \"status\": \"success\",
       \"amount\": 100.50,
       \"currency\": \"USD\",
       \"risk_score\": 0.15,
       ...
   }

Para pagamentos com PIX, use payment_method=\"pix\" e você receberá um QR code na resposta.

FONTES:
- src/api/payment_processor.py (relevância: 0.98)
- api_module.py (relevância: 0.94)
"
    
    simular_digitacao "Impressionante! O sistema não só encontrou como processar um pagamento," 0.03
    simular_digitacao "mas também forneceu exemplos de código prontos para uso!" 0.03
    simular_digitacao "Isso economiza muito tempo de desenvolvimento e consulta à documentação." 0.03
    
    limpar_e_esperar 4
}

# Função para demo de geração de documentação
demo_geracao() {
    mostrar_secao "DEMO 2: GERAÇÃO DE DOCUMENTAÇÃO"
    
    simular_digitacao "Agora, vamos ver como gerar documentação automaticamente a partir do código."
    simular_digitacao "Este processo analisa o código-fonte e gera documentação completa e estruturada."
    echo ""
    
    # Simular geração de documentação
    simular_digitacao "Vamos gerar documentação para nosso projeto de demonstração:" 0.05
    sleep 1
    
    # Simular execução do comando
    simular_comando "claude-code document --directory $DEMO_PROJECT_DIR --format markdown --output-dir $DEMO_PROJECT_DIR/docs" "
📝 Analisando o código-fonte...
🔍 Extraindo classes e métodos...
📊 Identificando parâmetros e tipos de retorno...
📚 Gerando exemplos de uso...
🧪 Verificando e validando exemplos...
📄 Formatando documentação em markdown...

✅ Documentação gerada com sucesso em $DEMO_PROJECT_DIR/docs/api_module.md!
"
    
    # Mostrar exemplo de documentação gerada
    simular_digitacao "Vamos ver um trecho da documentação gerada:" 0.03
    sleep 1
    
    simular_comando "head -n 30 $DEMO_PROJECT_DIR/docs/api_module.md" "
# API de Pagamentos - Documentação

*Gerado automaticamente em: $(date +"%Y-%m-%d %H:%M:%S")*
*Autores: Lucas Dórea Cardoso, Aulus Diniz*

## Visão Geral

Este módulo implementa um processador de pagamentos com validação avançada e documentação integrada.

## Classes

### PaymentProcessor

Processador de pagamentos com validação avançada e documentação automática.

Este processador implementa várias formas de pagamento e gera documentação SOTA automaticamente para cada método.

#### Inicialização

processor = PaymentProcessor(api_key=\"seu_api_key\")

#### Parâmetros do Construtor

| Parâmetro   | Tipo  | Descrição                                  | Padrão        |
|-------------|-------|--------------------------------------------| --------------|
| api_key     | str   | Chave de API para autenticação             | Obrigatório   |
| environment | str   | Ambiente ('production', 'sandbox', 'test') | \"production\"  |
"
    
    simular_digitacao "A documentação inclui tudo: parâmetros, tipos, exemplos, e muito mais!" 0.03
    simular_digitacao "Tudo isso foi gerado automaticamente a partir do código-fonte." 0.03
    
    # Mostrar geração de documentação de API
    simular_digitacao "Também podemos gerar documentação específica para APIs:" 0.03
    sleep 1
    
    simular_comando "claude-code document-api --directory $DEMO_PROJECT_DIR --format openapi --output-dir $DEMO_PROJECT_DIR/docs/api" "
📝 Analisando APIs e endpoints...
🔍 Extraindo parâmetros e respostas...
📊 Detectando esquemas e tipos de dados...
📚 Criando especificação OpenAPI...
🧪 Validando especificação...
📄 Salvando documentação...

✅ Documentação de API gerada com sucesso!
✅ Arquivo OpenAPI: $DEMO_PROJECT_DIR/docs/api/openapi.json
"
    
    simular_digitacao "A especificação OpenAPI pode ser usada em ferramentas como Swagger UI," 0.03
    simular_digitacao "permitindo que desenvolvedores testem e explorem sua API facilmente!" 0.03
    
    limpar_e_esperar 4
}

# Função para demo de agente de manutenção
demo_agente() {
    mostrar_secao "DEMO 3: AGENTE DE MANUTENÇÃO DE DOCUMENTAÇÃO"
    
    simular_digitacao "Vamos ver como o agente de manutenção de documentação funciona."
    simular_digitacao "Este agente monitora mudanças no código e atualiza a documentação automaticamente."
    echo ""
    
    # Simular detecção de mudanças
    simular_digitacao "Simulando uma mudança no código (adição de um novo parâmetro):" 0.05
    sleep 1
    
    # Simular commit
    simular_comando "git commit -m \"feat: Adicionar parâmetro timeout ao processo de pagamento\"" "
[main a1b2c3d] feat: Adicionar parâmetro timeout ao processo de pagamento
 1 file changed, 5 insertions(+), 1 deletion(-)
"
    
    # Simular detecção pelo agente
    simular_digitacao "O agente de manutenção detectou a mudança e está atualizando a documentação:" 0.03
    sleep 1
    
    simular_comando "claude-code update-docs --directory $DEMO_PROJECT_DIR --commit a1b2c3d" "
🔍 Analisando alterações no commit a1b2c3d...
📂 Verificando arquivos modificados...
📝 Identificando alterações na API...
🔄 Atualizando documentação afetada...

Alterações detectadas:
- Adicionado parâmetro 'timeout' ao método 'process_payment'
- Atualizada descrição do parâmetro
- Adicionado exemplo de uso com timeout

✅ Documentação atualizada com sucesso!
✅ Arquivos atualizados:
   - $DEMO_PROJECT_DIR/docs/api_module.md
   - $DEMO_PROJECT_DIR/docs/api/openapi.json
"
    
    # Mostrar trechos da documentação atualizada
    simular_digitacao "Vamos ver como a documentação foi atualizada automaticamente:" 0.03
    sleep 1
    
    simular_comando "grep -A 5 timeout $DEMO_PROJECT_DIR/docs/api_module.md" "
| timeout       | float  | Tempo limite em segundos para a transação | 30.0         |

#### Exemplo com timeout personalizado

result = processor.process_payment(
    amount=100.50,
"
    
    simular_digitacao "A documentação foi atualizada automaticamente!" 0.03
    simular_digitacao "O agente detectou a adição do parâmetro timeout e atualizou toda a documentação," 0.03
    simular_digitacao "incluindo tabelas de parâmetros, exemplos, e especificação OpenAPI." 0.03
    
    limpar_e_esperar 4
}

# Função para demo de geração de código com documentação
demo_geracao_codigo() {
    mostrar_secao "DEMO 4: GERAÇÃO DE CÓDIGO COM DOCUMENTAÇÃO INTEGRADA"
    
    simular_digitacao "Por fim, vamos ver como gerar código com documentação SOTA integrada."
    simular_digitacao "Este é o auge da Documentação 4.0: código e documentação nascem juntos!"
    echo ""
    
    # Simular geração de código
    simular_digitacao "Vamos gerar um novo módulo para processamento de reembolsos:" 0.05
    sleep 1
    
    # Simular execução do comando
    simular_comando "claude-code generate --prompt \"Crie um módulo Python para processamento de reembolsos com documentação SOTA integrada\" --output $DEMO_PROJECT_DIR/src/api/refunds.py" "
🧠 Pensando...
📝 Gerando código com documentação integrada...
⚙️ Otimizando estrutura e padrões...
📚 Incorporando melhores práticas de documentação...
✅ Adicionando docstrings completos...
🧪 Incluindo exemplos testáveis...

✅ Código gerado com sucesso em $DEMO_PROJECT_DIR/src/api/refunds.py!
"
    
    # Mostrar trecho do código gerado
    simular_digitacao "Vamos ver um trecho do código gerado:" 0.03
    sleep 1
    
    simular_comando "head -n 40 $DEMO_PROJECT_DIR/src/api/refunds.py" "
\"\"\"
Módulo de Processamento de Reembolsos

Este módulo implementa um sistema completo para processamento de reembolsos
relacionados a transações de pagamento. Suporta reembolsos totais e parciais,
com validação e rastreamento completo.

Autores: Lucas Dórea Cardoso, Aulus Diniz
Data: $(date +\"%Y-%m-%d\")
\"\"\"

import datetime
import uuid
from typing import Dict, Any, Optional, List, Union, Tuple

class RefundProcessor:
    \"\"\"
    Processador de reembolsos com documentação SOTA integrada.
    
    Esta classe gerencia todas as operações relacionadas a reembolsos,
    incluindo validação, processamento e geração de comprovantes.
    
    Exemplos:
        # Inicializar o processador
        refund_processor = RefundProcessor(api_key=\"sk_test_123456\")
        
        # Processar um reembolso total
        result = refund_processor.process_refund(
            transaction_id=\"tr_123456\"
        )
        
        # Processar um reembolso parcial
        result = refund_processor.process_refund(
            transaction_id=\"tr_123456\",
            amount=50.25,
            reason=\"partial_dissatisfaction\"
        )
    \"\"\"
"
    
    simular_digitacao "O código gerado já vem com documentação completa integrada!" 0.03
    simular_digitacao "Docstrings, exemplos, tipos, tudo seguindo as melhores práticas." 0.03
    simular_digitacao "Isso garante que a documentação nasça junto com o código, sempre atualizada." 0.03
    
    limpar_e_esperar 4
}

# Função para mostrar resumo e conclusão
mostrar_conclusao() {
    mostrar_secao "CONCLUSÃO: DOCUMENTAÇÃO 4.0 COM CLAUDE CODE"
    
    simular_digitacao "Vimos como a Documentação 4.0 com Claude Code transforma completamente"
    simular_digitacao "a forma como criamos e mantemos documentação técnica:"
    echo ""
    
    sleep 1
    echo -e "${GREEN}✅ Busca Agêntica${NC}: Consultas em linguagem natural sobre o código"
    sleep 0.5
    echo -e "${GREEN}✅ Geração Automática${NC}: Documentação completa gerada a partir do código"
    sleep 0.5
    echo -e "${GREEN}✅ Manutenção Automática${NC}: Atualização da documentação ao mudar o código"
    sleep 0.5
    echo -e "${GREEN}✅ Geração de Código${NC}: Código e documentação nascem juntos"
    sleep 0.5
    echo -e "${GREEN}✅ Integração Contínua${NC}: Tudo integrado ao fluxo de desenvolvimento"
    echo ""
    
    sleep 1
    simular_digitacao "A Documentação 4.0 transforma documentação de um fardo em um ativo estratégico"
    simular_digitacao "que evolui automaticamente com seu código."
    echo ""
    
    sleep 1
    echo -e "${BLUE}Para saber mais:${NC}"
    echo -e "1. Consulte o guia prático: ${YELLOW}doc40-guia-pratico.md${NC}"
    echo -e "2. Veja a apresentação completa: ${YELLOW}doc40-slides-atualizados.html${NC}"
    echo -e "3. Explore os scripts de exemplo: ${YELLOW}doc40-*.py${NC}"
    echo ""
    
    sleep 1
    echo -e "${BLUE}${BOLD}OBRIGADO POR ASSISTIR À DEMONSTRAÇÃO!${NC}"
    echo -e "${BLUE}Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz${NC}"
}

# Execução principal
mostrar_cabecalho
demo_consulta
demo_geracao
demo_agente
demo_geracao_codigo
mostrar_conclusao