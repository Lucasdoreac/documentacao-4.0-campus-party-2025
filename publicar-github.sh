#!/bin/bash
# Script para publicar o projeto no GitHub
# Campus Party 2025 - Lucas Dórea Cardoso e Aulus Diniz

echo "🚀 Preparando repositório para publicação no GitHub..."

# Verificar se git está instalado
if ! command -v git &> /dev/null; then
    echo "❌ Git não encontrado. Por favor, instale o Git para continuar."
    exit 1
fi

# Diretório base
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$BASE_DIR"

# Verificar se já existe um repositório git
if [ ! -d ".git" ]; then
    echo "📦 Inicializando novo repositório Git..."
    git init
fi

# Verificar se o usuário já tem um nome de usuário do GitHub configurado
echo "🔍 Verificando configurações do Git..."
GIT_USER=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_USER" ] || [ -z "$GIT_EMAIL" ]; then
    echo "⚠️ Configuração do Git incompleta."
    
    if [ -z "$GIT_USER" ]; then
        read -p "Digite seu nome de usuário do Git: " GIT_USER
        git config --global user.name "$GIT_USER"
    fi
    
    if [ -z "$GIT_EMAIL" ]; then
        read -p "Digite seu email do Git: " GIT_EMAIL
        git config --global user.email "$GIT_EMAIL"
    fi
fi

# Adicionar arquivos essenciais ao staging
echo "📋 Adicionando arquivos ao repositório..."
git add README.md LICENSE .gitignore doc40-*.* publicar-github.sh demo-project/

# Criar commit inicial
echo "💾 Criando commit inicial..."
git commit -m "Documentação 4.0 na Era IA - Campus Party 2025"

# Perguntar sobre o repositório remoto
echo ""
echo "🌐 Para publicar no GitHub, você precisa criar um repositório em https://github.com/new"
echo "   Use o nome 'documentacao-4.0-campus-party-2025' ou outro de sua preferência."
echo ""
read -p "Digite o URL do seu repositório GitHub (ex: https://github.com/seunome/documentacao-4.0-campus-party-2025): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ URL do repositório não fornecido. Você pode adicionar manualmente depois com:"
    echo "   git remote add origin SEU_URL_GITHUB"
    echo "   git push -u origin main"
else
    # Extrair apenas a parte do URL que o git precisa
    if [[ $REPO_URL == *"github.com"* ]]; then
        # Se é um URL completo, converter para formato git
        REPO_URL=$(echo $REPO_URL | sed 's|https://github.com/|git@github.com:|')
        if [[ $REPO_URL != *".git"* ]]; then
            REPO_URL="${REPO_URL}.git"
        fi
    fi
    
    echo "🔗 Adicionando repositório remoto: $REPO_URL"
    git remote add origin "$REPO_URL"
    
    echo "⬆️ Enviando código para o GitHub..."
    git push -u origin main
    
    echo ""
    echo "✅ Projeto publicado com sucesso no GitHub!"
    echo "   Acesse seu repositório em: $REPO_URL"
fi

echo ""
echo "🎉 Processo de publicação finalizado!"
echo "   Seus arquivos estão prontos para compartilhamento."