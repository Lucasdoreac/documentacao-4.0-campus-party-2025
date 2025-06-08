# Documentação 4.0: Guia Prático do Zero ao Avançado
**Por Lucas Dórea Cardoso e Aulus Diniz**

## 🚀 Introdução

Este guia prático foi elaborado para ajudar qualquer pessoa a entender e implementar sistemas de Documentação 4.0 usando LLMs agênticos, mesmo sem conhecimento prévio. Você aprenderá desde a instalação das ferramentas básicas até a criação de sistemas avançados de documentação automatizada.

## 📋 O que é Documentação 4.0?

Documentação 4.0 representa a nova geração de documentação técnica, com as seguintes características:

- **Inteligente**: Compreende contexto e intenção do usuário
- **Automatizada**: Atualiza-se conforme o código evolui
- **Interativa**: Responde a perguntas em linguagem natural
- **Integrada**: Conectada diretamente ao ciclo de desenvolvimento
- **Adaptativa**: Personaliza-se conforme o perfil do usuário

## 🛠️ Instalação das Ferramentas Básicas

### Passo 1: Instalação do Claude Code CLI

O Claude Code CLI (Command Line Interface) é a ferramenta principal para interagir com o modelo Claude para tarefas de documentação.

**Para macOS:**
```bash
# Usando Homebrew
brew install anthropic/tools/claude-code

# Verificando a instalação
claude-code --version
```

**Para Linux:**
```bash
# Baixando o instalador
curl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash

# Verificando a instalação
claude-code --version
```

**Para Windows:**
```bash
# Usando Powershell (execute como administrador)
Set-ExecutionPolicy Bypass -Scope Process -Force
iwr https://raw.githubusercontent.com/anthropic/claude-code/main/install.ps1 -OutFile install.ps1
./install.ps1

# Verificando a instalação
claude-code --version
```

### Passo 2: Configuração da Chave API

Após instalar o Claude Code CLI, você precisa configurar sua chave API:

```bash
# Configurar a chave API
claude-code config set api_key sk_ant_...

# Verificar a configuração
claude-code config get
```

Para obter uma chave API:
1. Acesse https://console.anthropic.com/
2. Crie uma conta ou faça login
3. Navegue até "API Keys"
4. Crie uma nova chave e copie-a

### Passo 3: Instalação de Ferramentas Complementares

Para uma experiência completa, instale estas ferramentas auxiliares:

```bash
# Python (necessário para os scripts de integração)
# macOS/Linux
python3 -m pip install --upgrade pip

# Windows
py -m pip install --upgrade pip

# Bibliotecas necessárias
pip install anthropic python-dotenv requests click rich
```

## 💡 Conceitos Fundamentais

Antes de avançarmos para a implementação, vamos entender alguns conceitos essenciais:

### 1. Agentes LLM vs. RAG Tradicional

| RAG Tradicional | Agentes LLM (Claude Code) |
|-----------------|---------------------------|
| Apenas recupera e gera | Agente autônomo que executa tarefas |
| Requer indexação prévia | Explora código e docs dinamicamente |
| Responde perguntas simples | Executa ações complexas |
| Dificuldade com contexto | Entende contexto amplo do projeto |

### 2. Tipos de Documentação que o Sistema Pode Gerar

- **Documentação de API**: Endpoints, parâmetros, exemplos
- **Documentação de Código**: Classes, métodos, funções
- **Guias Tutoriais**: Passo a passo para usar seu software
- **Notas de Versão**: Mudanças entre versões
- **Docs de Arquitetura**: Visão estrutural do sistema

### 3. O Fluxo de Trabalho da Documentação 4.0

```
Código → Análise Agêntica → Geração de Docs → Validação → Publicação → Manutenção Automática
```

## 🔍 Primeiros Passos: Consultando Documentação

Vamos começar com um exemplo simples: usar o Claude Code para consultar informações em uma base de código.

### Exemplo 1: Consulta Básica

Crie um arquivo chamado `doc40-consulta.py`:

```python
# doc40-consulta.py
import os
import subprocess
import json

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
    # Diretório do projeto (use o diretório atual se não tiver um específico)
    diretorio = os.getcwd()
    
    # Exemplos de perguntas
    perguntas = [
        "Quais são as principais funções neste código?",
        "Explique como funciona o sistema de autenticação",
        "Como são processados os pagamentos neste sistema?"
    ]
    
    # Fazer consultas
    for pergunta in perguntas:
        resposta = consultar_codigo(pergunta, diretorio)
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
```

Para executar:
```bash
python doc40-consulta.py
```

## 📚 Geração de Documentação Automática

Agora vamos criar um script para gerar documentação automaticamente a partir do código.

### Exemplo 2: Gerador de Documentação

Crie um arquivo chamado `doc40-gerador.py`:

```python
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
```

Para executar:
```bash
# Gerar documentação geral
python doc40-gerador.py --dir ./meu-projeto --formato markdown --saida ./documentacao

# Gerar documentação de API
python doc40-gerador.py --dir ./meu-projeto --api
```

## 🤖 Agente de Manutenção de Documentação

Vamos criar um agente que monitora mudanças no código e atualiza a documentação automaticamente.

### Exemplo 3: Agente de Manutenção

Crie um arquivo chamado `doc40-agente.py`:

```python
# doc40-agente.py
import os
import subprocess
import json
import time
import argparse
from datetime import datetime

def verificar_mudancas(diretorio, ultimo_commit=None):
    """Verifica se houve mudanças no repositório."""
    # Mudar para o diretório do projeto
    os.chdir(diretorio)
    
    # Obter o último commit
    comando = ["git", "rev-parse", "HEAD"]
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    if resultado.returncode != 0:
        print(f"❌ Erro ao obter o último commit: {resultado.stderr}")
        return False, None
    
    commit_atual = resultado.stdout.strip()
    
    # Se não temos um commit anterior para comparar, apenas retornar o atual
    if ultimo_commit is None:
        return False, commit_atual
    
    # Se o commit atual é diferente do último, houve mudanças
    if commit_atual != ultimo_commit:
        return True, commit_atual
    
    return False, commit_atual

def atualizar_documentacao(diretorio, commit_id, saida="docs"):
    """Atualiza a documentação com base nas mudanças do commit."""
    print(f"🔄 Atualizando documentação para commit: {commit_id[:8]}")
    
    # Comando para o Claude Code CLI
    comando = [
        "claude-code",
        "update-docs",
        "--directory", diretorio,
        "--commit", commit_id,
        "--output-dir", saida
    ]
    
    # Executar o comando
    resultado = subprocess.run(comando, capture_output=True, text=True)
    
    # Verificar se houve erro
    if resultado.returncode != 0:
        print(f"❌ Erro: {resultado.stderr}")
        return False
    
    # Registrar a atualização
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(os.path.join(saida, "atualizacoes.log"), "a") as f:
        f.write(f"{agora} - Documentação atualizada para commit {commit_id[:8]}\n")
    
    print(f"✅ Documentação atualizada com sucesso em: {saida}")
    return True

def executar_agente(diretorio, saida="docs", intervalo=300):
    """Executa o agente de manutenção de documentação."""
    print(f"🤖 Iniciando agente de manutenção de documentação")
    print(f"📁 Diretório: {diretorio}")
    print(f"📂 Saída: {saida}")
    print(f"⏱️ Intervalo: {intervalo} segundos")
    
    # Criar diretório de saída se não existir
    os.makedirs(saida, exist_ok=True)
    
    # Inicializar o último commit
    _, ultimo_commit = verificar_mudancas(diretorio)
    print(f"📌 Commit inicial: {ultimo_commit[:8]}")
    
    try:
        while True:
            # Verificar mudanças
            houve_mudancas, commit_atual = verificar_mudancas(diretorio, ultimo_commit)
            
            # Se houve mudanças, atualizar a documentação
            if houve_mudancas:
                print(f"🔍 Detectadas mudanças! Novo commit: {commit_atual[:8]}")
                atualizar_documentacao(diretorio, commit_atual, saida)
                ultimo_commit = commit_atual
            
            # Aguardar o próximo ciclo
            time.sleep(intervalo)
    
    except KeyboardInterrupt:
        print("\n⏹️ Agente interrompido pelo usuário")

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Agente de Manutenção de Documentação 4.0")
    parser.add_argument("--dir", default=os.getcwd(), help="Diretório do projeto")
    parser.add_argument("--saida", default="docs", help="Diretório de saída")
    parser.add_argument("--intervalo", type=int, default=300, help="Intervalo entre verificações (segundos)")
    
    args = parser.parse_args()
    
    # Executar o agente
    executar_agente(args.dir, args.saida, args.intervalo)

if __name__ == "__main__":
    main()
```

Para executar:
```bash
# Iniciar o agente com verificação a cada 5 minutos
python doc40-agente.py --dir ./meu-projeto --saida ./documentacao --intervalo 300
```

## 🔄 Sistema Integrado de Documentação 4.0

Agora vamos juntar tudo em um sistema completo e fácil de usar. Este script cria um menu interativo para todas as funcionalidades.

### Sistema Completo: `doc40-sistema.py`

```python
# doc40-sistema.py
import os
import subprocess
import json
import time
import argparse
import threading
from datetime import datetime

class Sistema4Doc:
    def __init__(self, diretorio=None, saida="docs"):
        """Inicializa o sistema de documentação 4.0."""
        self.diretorio = diretorio or os.getcwd()
        self.saida = saida
        self.agente_rodando = False
        self.thread_agente = None
        
        # Criar diretório de saída se não existir
        os.makedirs(saida, exist_ok=True)
        
        print(f"🚀 Sistema de Documentação 4.0 inicializado")
        print(f"📁 Diretório do projeto: {self.diretorio}")
        print(f"📂 Diretório de saída: {self.saida}")
    
    def consultar(self, pergunta):
        """Consulta a documentação/código."""
        print(f"\n📝 Consultando: {pergunta}")
        
        comando = [
            "claude-code",
            "query",
            "--directory", self.diretorio,
            "--query", pergunta,
            "--output", "json"
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"❌ Erro: {resultado.stderr}")
            return
        
        try:
            resposta = json.loads(resultado.stdout)
            
            print("\n" + "="*50)
            print(f"🤖 Resposta para: {pergunta}")
            print("="*50)
            print(resposta.get("response", "Sem resposta"))
            print("="*50)
            print("Fontes:")
            for fonte in resposta.get("sources", []):
                print(f"- {fonte['file']} (relevância: {fonte.get('relevance', 'N/A')})")
            print()
        
        except json.JSONDecodeError:
            print("❌ Erro ao processar a resposta")
    
    def gerar_documentacao(self, formato="markdown"):
        """Gera documentação geral."""
        print(f"\n🚀 Gerando documentação para: {self.diretorio}")
        print(f"📄 Formato: {formato}")
        
        comando = [
            "claude-code",
            "document",
            "--directory", self.diretorio,
            "--format", formato,
            "--output-dir", self.saida
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"❌ Erro: {resultado.stderr}")
            return
        
        print(f"✅ Documentação gerada com sucesso em: {self.saida}")
    
    def gerar_documentacao_api(self):
        """Gera documentação específica para API."""
        print(f"\n🚀 Gerando documentação de API para: {self.diretorio}")
        
        saida_api = os.path.join(self.saida, "api")
        os.makedirs(saida_api, exist_ok=True)
        
        comando = [
            "claude-code",
            "document-api",
            "--directory", self.diretorio,
            "--output-dir", saida_api,
            "--format", "openapi+markdown"
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"❌ Erro: {resultado.stderr}")
            return
        
        print(f"✅ Documentação de API gerada com sucesso em: {saida_api}")
    
    def _loop_agente(self, intervalo):
        """Loop interno do agente de manutenção."""
        # Inicializar o último commit
        ultimo_commit = self._obter_commit_atual()
        print(f"📌 Commit inicial: {ultimo_commit[:8] if ultimo_commit else 'Nenhum'}")
        
        while self.agente_rodando:
            # Obter commit atual
            commit_atual = self._obter_commit_atual()
            
            # Se houve mudanças, atualizar a documentação
            if commit_atual and commit_atual != ultimo_commit:
                print(f"🔍 Detectadas mudanças! Novo commit: {commit_atual[:8]}")
                self._atualizar_documentacao(commit_atual)
                ultimo_commit = commit_atual
            
            # Aguardar o próximo ciclo
            time.sleep(intervalo)
    
    def _obter_commit_atual(self):
        """Obtém o hash do commit atual."""
        try:
            # Mudar para o diretório do projeto
            original_dir = os.getcwd()
            os.chdir(self.diretorio)
            
            # Obter o último commit
            comando = ["git", "rev-parse", "HEAD"]
            resultado = subprocess.run(comando, capture_output=True, text=True)
            
            # Restaurar diretório original
            os.chdir(original_dir)
            
            if resultado.returncode != 0:
                return None
            
            return resultado.stdout.strip()
        
        except Exception as e:
            print(f"❌ Erro ao obter o commit atual: {e}")
            return None
    
    def _atualizar_documentacao(self, commit_id):
        """Atualiza a documentação para um commit específico."""
        print(f"🔄 Atualizando documentação para commit: {commit_id[:8]}")
        
        comando = [
            "claude-code",
            "update-docs",
            "--directory", self.diretorio,
            "--commit", commit_id,
            "--output-dir", self.saida
        ]
        
        resultado = subprocess.run(comando, capture_output=True, text=True)
        
        if resultado.returncode != 0:
            print(f"❌ Erro: {resultado.stderr}")
            return False
        
        # Registrar a atualização
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(os.path.join(self.saida, "atualizacoes.log"), "a") as f:
            f.write(f"{agora} - Documentação atualizada para commit {commit_id[:8]}\n")
        
        print(f"✅ Documentação atualizada com sucesso em: {self.saida}")
        return True
    
    def iniciar_agente(self, intervalo=300):
        """Inicia o agente de manutenção em uma thread separada."""
        if self.agente_rodando:
            print("⚠️ O agente já está em execução")
            return
        
        print(f"\n🤖 Iniciando agente de manutenção de documentação")
        print(f"⏱️ Intervalo: {intervalo} segundos")
        
        self.agente_rodando = True
        self.thread_agente = threading.Thread(target=self._loop_agente, args=(intervalo,))
        self.thread_agente.daemon = True
        self.thread_agente.start()
    
    def parar_agente(self):
        """Para o agente de manutenção."""
        if not self.agente_rodando:
            print("⚠️ O agente não está em execução")
            return
        
        print("\n⏹️ Parando agente de manutenção...")
        self.agente_rodando = False
        self.thread_agente.join(timeout=2)
        print("✅ Agente parado com sucesso")
    
    def menu_interativo(self):
        """Exibe um menu interativo para o usuário."""
        while True:
            print("\n" + "="*50)
            print("📚 SISTEMA DE DOCUMENTAÇÃO 4.0")
            print("="*50)
            print("1. Consultar documentação/código")
            print("2. Gerar documentação geral")
            print("3. Gerar documentação de API")
            print("4. Iniciar agente de manutenção")
            print("5. Parar agente de manutenção")
            print("6. Sair")
            print("="*50)
            
            escolha = input("Escolha uma opção (1-6): ")
            
            if escolha == "1":
                pergunta = input("Digite sua pergunta: ")
                self.consultar(pergunta)
            
            elif escolha == "2":
                formato = input("Formato (markdown, html, pdf) [markdown]: ") or "markdown"
                self.gerar_documentacao(formato)
            
            elif escolha == "3":
                self.gerar_documentacao_api()
            
            elif escolha == "4":
                try:
                    intervalo = int(input("Intervalo em segundos [300]: ") or "300")
                    self.iniciar_agente(intervalo)
                except ValueError:
                    print("❌ Intervalo inválido. Usando o valor padrão de 300 segundos.")
                    self.iniciar_agente()
            
            elif escolha == "5":
                self.parar_agente()
            
            elif escolha == "6":
                if self.agente_rodando:
                    self.parar_agente()
                print("👋 Obrigado por usar o Sistema de Documentação 4.0!")
                break
            
            else:
                print("❌ Opção inválida. Por favor, escolha uma opção de 1 a 6.")

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Sistema de Documentação 4.0")
    parser.add_argument("--dir", default=os.getcwd(), help="Diretório do projeto")
    parser.add_argument("--saida", default="docs", help="Diretório de saída")
    
    args = parser.parse_args()
    
    # Inicializar e executar o sistema
    sistema = Sistema4Doc(args.dir, args.saida)
    sistema.menu_interativo()

if __name__ == "__main__":
    main()
```

Para executar o sistema completo:
```bash
python doc40-sistema.py --dir ./meu-projeto --saida ./documentacao
```

## 🔌 Integração com Outras Ferramentas

A Documentação 4.0 pode ser integrada com várias outras ferramentas para ampliar suas capacidades.

### 1. Integração com GitHub Actions

Crie um arquivo `.github/workflows/atualizar-docs.yml`:

```yaml
name: Atualizar Documentação

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  update-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Necessário para acesso ao histórico de commits
      
      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install anthropic python-dotenv requests click rich
      
      - name: Instalar Claude Code CLI
        run: |
          curl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash
      
      - name: Configurar Claude Code
        run: |
          claude-code config set api_key ${{ secrets.CLAUDE_API_KEY }}
      
      - name: Atualizar documentação
        run: |
          # Obter o commit anterior
          PREVIOUS_COMMIT=$(git rev-parse HEAD^)
          CURRENT_COMMIT=$(git rev-parse HEAD)
          
          # Atualizar documentação
          claude-code update-docs --directory . --commit $CURRENT_COMMIT --previous-commit $PREVIOUS_COMMIT --output-dir docs
      
      - name: Commit das alterações de documentação
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add docs/
          git commit -m "📚 Atualização automática da documentação" || echo "Sem alterações para commit"
          git push
```

### 2. Integração com VSCode

Crie uma extensão VSCode ou use snippets para integrar a Documentação 4.0 no seu editor. Aqui está um exemplo de configuração de snippet:

```json
{
  "Doc 4.0 - Comentário de Função": {
    "prefix": "doc4",
    "body": [
      "/**",
      " * ${1:Nome da função}",
      " * ",
      " * ${2:Descrição da função}",
      " * ",
      " * @param {${3:tipo}} ${4:nome_param} - ${5:Descrição do parâmetro}",
      " * @returns {${6:tipo_retorno}} ${7:Descrição do retorno}",
      " * @throws {${8:tipo_erro}} ${9:Descrição da exceção}",
      " * ",
      " * @example",
      " * ```javascript",
      " * ${10:// Exemplo de uso}",
      " * ```",
      " */",
      "$0"
    ],
    "description": "Cria um comentário de função no padrão da Documentação 4.0"
  }
}
```

## 📊 Métricas e Monitoramento

É importante medir a eficácia da sua documentação. Aqui está um script para coletar métricas:

### Monitoramento de Documentação: `doc40-metricas.py`

```python
# doc40-metricas.py
import os
import json
import argparse
import datetime
import matplotlib.pyplot as plt

class MetricasDocumentacao:
    def __init__(self, diretorio_docs):
        """Inicializa o monitor de métricas de documentação."""
        self.diretorio_docs = diretorio_docs
        self.arquivo_metricas = os.path.join(diretorio_docs, "metricas.json")
        self.metricas = self._carregar_metricas()
    
    def _carregar_metricas(self):
        """Carrega métricas existentes ou cria um novo arquivo."""
        if os.path.exists(self.arquivo_metricas):
            try:
                with open(self.arquivo_metricas, "r") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"❌ Erro ao carregar métricas. Criando novo arquivo.")
        
        # Estrutura inicial das métricas
        return {
            "consultas": [],
            "atualizacoes": [],
            "cobertura": []
        }
    
    def _salvar_metricas(self):
        """Salva as métricas no arquivo JSON."""
        with open(self.arquivo_metricas, "w") as f:
            json.dump(self.metricas, f, indent=2)
    
    def registrar_consulta(self, pergunta, sucesso):
        """Registra uma consulta à documentação."""
        agora = datetime.datetime.now().isoformat()
        
        self.metricas["consultas"].append({
            "timestamp": agora,
            "pergunta": pergunta,
            "sucesso": sucesso
        })
        
        self._salvar_metricas()
    
    def registrar_atualizacao(self, commit_id, arquivos_alterados):
        """Registra uma atualização de documentação."""
        agora = datetime.datetime.now().isoformat()
        
        self.metricas["atualizacoes"].append({
            "timestamp": agora,
            "commit_id": commit_id,
            "arquivos_alterados": arquivos_alterados
        })
        
        self._salvar_metricas()
    
    def calcular_cobertura(self):
        """Calcula a cobertura de documentação."""
        # Esta é uma implementação simplificada. Na prática, você faria uma
        # análise mais complexa do código e da documentação.
        
        # Contar arquivos de código
        codigo_total = 0
        for root, _, files in os.walk(os.path.dirname(self.diretorio_docs)):
            if self.diretorio_docs in root:  # Pular o diretório de docs
                continue
            
            for file in files:
                if file.endswith((".py", ".js", ".java", ".cpp", ".ts")):
                    codigo_total += 1
        
        # Contar arquivos de documentação
        docs_total = 0
        for root, _, files in os.walk(self.diretorio_docs):
            for file in files:
                if file.endswith((".md", ".html", ".json")) and file != "metricas.json":
                    docs_total += 1
        
        # Calcular cobertura (simplificado)
        cobertura = (docs_total / max(1, codigo_total)) * 100 if codigo_total > 0 else 0
        
        # Registrar
        agora = datetime.datetime.now().isoformat()
        self.metricas["cobertura"].append({
            "timestamp": agora,
            "codigo_total": codigo_total,
            "docs_total": docs_total,
            "cobertura_percentual": cobertura
        })
        
        self._salvar_metricas()
        return cobertura
    
    def gerar_relatorio(self):
        """Gera um relatório completo de métricas."""
        # Total de consultas
        total_consultas = len(self.metricas["consultas"])
        consultas_sucesso = sum(1 for c in self.metricas["consultas"] if c["sucesso"])
        taxa_sucesso = (consultas_sucesso / max(1, total_consultas)) * 100
        
        # Total de atualizações
        total_atualizacoes = len(self.metricas["atualizacoes"])
        arquivos_atualizados = sum(len(a["arquivos_alterados"]) for a in self.metricas["atualizacoes"])
        
        # Cobertura atual
        cobertura_atual = self.metricas["cobertura"][-1]["cobertura_percentual"] if self.metricas["cobertura"] else 0
        
        # Exibir relatório
        print("\n" + "="*50)
        print("📊 RELATÓRIO DE MÉTRICAS DE DOCUMENTAÇÃO")
        print("="*50)
        print(f"📅 Data: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Diretório: {self.diretorio_docs}")
        print("\n📈 ESTATÍSTICAS:")
        print(f"- Total de consultas: {total_consultas}")
        print(f"- Taxa de sucesso das consultas: {taxa_sucesso:.1f}%")
        print(f"- Total de atualizações: {total_atualizacoes}")
        print(f"- Arquivos atualizados: {arquivos_atualizados}")
        print(f"- Cobertura atual: {cobertura_atual:.1f}%")
        print("="*50)
    
    def gerar_graficos(self):
        """Gera gráficos das métricas."""
        # Converter timestamps para objetos datetime
        datas_consultas = [datetime.datetime.fromisoformat(c["timestamp"]) for c in self.metricas["consultas"]]
        datas_atualizacoes = [datetime.datetime.fromisoformat(a["timestamp"]) for a in self.metricas["atualizacoes"]]
        datas_cobertura = [datetime.datetime.fromisoformat(c["timestamp"]) for c in self.metricas["cobertura"]]
        
        # Valores de cobertura
        valores_cobertura = [c["cobertura_percentual"] for c in self.metricas["cobertura"]]
        
        # Configurar a figura
        plt.figure(figsize=(12, 8))
        
        # Gráfico de consultas
        plt.subplot(2, 1, 1)
        plt.hist(datas_consultas, bins=20, alpha=0.7, color='blue')
        plt.title('Histórico de Consultas à Documentação')
        plt.xlabel('Data')
        plt.ylabel('Número de Consultas')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Gráfico de cobertura
        plt.subplot(2, 1, 2)
        plt.plot(datas_cobertura, valores_cobertura, 'g-', marker='o')
        plt.title('Evolução da Cobertura de Documentação')
        plt.xlabel('Data')
        plt.ylabel('Cobertura (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Ajustar layout e salvar
        plt.tight_layout()
        grafico_path = os.path.join(self.diretorio_docs, "metricas_grafico.png")
        plt.savefig(grafico_path)
        plt.close()
        
        print(f"✅ Gráfico salvo em: {grafico_path}")
        return grafico_path

def main():
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description="Métricas de Documentação 4.0")
    parser.add_argument("--dir", default="docs", help="Diretório de documentação")
    parser.add_argument("--relatorio", action="store_true", help="Gerar relatório")
    parser.add_argument("--grafico", action="store_true", help="Gerar gráfico")
    parser.add_argument("--cobertura", action="store_true", help="Calcular cobertura")
    
    args = parser.parse_args()
    
    # Inicializar monitor de métricas
    metricas = MetricasDocumentacao(args.dir)
    
    # Executar ações solicitadas
    if args.cobertura:
        cobertura = metricas.calcular_cobertura()
        print(f"📊 Cobertura atual: {cobertura:.1f}%")
    
    if args.relatorio:
        metricas.gerar_relatorio()
    
    if args.grafico:
        metricas.gerar_graficos()
    
    # Se nenhuma ação foi especificada, mostrar ajuda
    if not (args.cobertura or args.relatorio or args.grafico):
        print("⚠️ Nenhuma ação especificada. Use --relatorio, --grafico ou --cobertura.")
        parser.print_help()

if __name__ == "__main__":
    main()
```

Para executar:
```bash
# Calcular a cobertura de documentação
python doc40-metricas.py --dir ./documentacao --cobertura

# Gerar relatório completo
python doc40-metricas.py --dir ./documentacao --relatorio

# Gerar gráficos
python doc40-metricas.py --dir ./documentacao --grafico
```

## 🎓 Melhores Práticas

Para obter os melhores resultados com a Documentação 4.0, siga estas práticas:

### 1. Estrutura de Código Consistente

Mantenha uma estrutura de código consistente, com nomes de arquivos, classes e funções significativos. Isso ajuda o Claude Code a entender melhor seu código.

### 2. Comentários Estratégicos

Adicione comentários em pontos estratégicos do código, especialmente para explicar a lógica de negócios complexa. O Claude Code usará esses comentários para gerar documentação mais precisa.

### 3. Integração com o Fluxo de Trabalho

Integre a Documentação 4.0 com seu fluxo de trabalho de desenvolvimento:
- Execute o agente de manutenção no ambiente de CI/CD
- Faça verificações de documentação parte do processo de revisão de código
- Inclua métricas de documentação em seus relatórios regulares

### 4. Feedback dos Usuários

Colete feedback dos usuários da sua documentação para identificar áreas de melhoria. O Claude Code pode adaptar a documentação com base nesse feedback.

## 🌟 Conclusão

Parabéns! Você aprendeu como implementar um sistema completo de Documentação 4.0 usando Claude Code e outras ferramentas agênticas. Este guia abrangeu desde a instalação básica até a configuração de um sistema de documentação automatizado e monitorado.

A Documentação 4.0 representa uma mudança fundamental na forma como criamos e mantemos documentação técnica, transformando-a de um processo manual e tedioso em um sistema inteligente e automatizado que evolui com seu código.

## 📞 Suporte e Recursos

Para obter mais informações ou suporte:

- **Documentação Oficial**: [docs.anthropic.com/claude-code](https://docs.anthropic.com/claude-code)
- **GitHub do Projeto**: [github.com/anthropic/claude-code](https://github.com/anthropic/claude-code)
- **Comunidade**: [community.anthropic.com](https://community.anthropic.com)

---

Criado por Lucas Dórea Cardoso e Aulus Diniz para a Campus Party 2025  
Este guia é parte da apresentação "Documentação 4.0 na Era IA"

---

**Nota**: Os comandos e APIs específicos do Claude Code neste documento são ilustrativos. Para a implementação real, consulte a documentação oficial mais recente.