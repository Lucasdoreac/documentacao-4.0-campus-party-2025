#!/bin/bash

# Script para atualizar o GitHub Pages com os slides atualizados
echo "Atualizando GitHub Pages para usar os slides atualizados..."

# Verificar se estamos em um repositório git
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Erro: Este diretório não é um repositório Git."
  exit 1
fi

# Obter o nome do repositório e usuário do remote origin
REMOTE_URL=$(git config --get remote.origin.url)
if [[ -z "$REMOTE_URL" ]]; then
  echo "Erro: Não foi possível encontrar a URL do repositório remoto."
  exit 1
fi

# Extrair nome de usuário e repositório
if [[ $REMOTE_URL == *"github.com"* ]]; then
  if [[ $REMOTE_URL == *"github.com:"* ]]; then
    # SSH URL format: git@github.com:username/repo.git
    USER_REPO=$(echo $REMOTE_URL | sed -E 's/.*github.com:([^/]+)\/([^.]+).*/\1\/\2/')
  else
    # HTTPS URL format: https://github.com/username/repo.git
    USER_REPO=$(echo $REMOTE_URL | sed -E 's/.*github.com\/([^/]+)\/([^.]+).*/\1\/\2/')
  fi
else
  echo "Erro: A URL remota não parece ser do GitHub."
  exit 1
fi

USERNAME=$(echo $USER_REPO | cut -d'/' -f1)
REPO=$(echo $USER_REPO | cut -d'/' -f2)

echo "Usuário GitHub: $USERNAME"
echo "Repositório: $REPO"

# Criar ou modificar o arquivo index.html para a página principal do GitHub Pages
cat > index.html << EOF
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentação 4.0 na Era IA</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        a {
            color: #3498db;
            text-decoration: none;
            transition: color 0.3s;
        }
        a:hover {
            color: #2980b9;
            text-decoration: underline;
        }
        .card {
            background: #f9f9f9;
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 16px;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .button {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
            font-weight: bold;
        }
        .button:hover {
            background: #2980b9;
            text-decoration: none;
            color: white;
        }
        footer {
            margin-top: 40px;
            font-size: 0.9em;
            color: #7f8c8d;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Documentação 4.0 na Era IA</h1>
    <p>Materiais da apresentação para a Campus Party 2025 sobre as novas abordagens de documentação técnica potencializadas pela IA.</p>
    
    <div class="card">
        <h2>Apresentação de Slides</h2>
        <p>Versão atualizada da apresentação com códigos maiores e links diretos para implementações.</p>
        <a href="doc40-slides-atualizados.html" class="button">Ver Apresentação</a>
    </div>
    
    <div class="card">
        <h2>Implementações Completas</h2>
        <p>Acesse as implementações completas de todos os componentes do sistema de Documentação 4.0:</p>
        <ul>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-consulta.py">Módulo de Consulta</a></li>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-gerador.py">Gerador de Documentação</a></li>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-agente.py">Agente de Manutenção</a></li>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-sistema.py">Sistema Completo</a></li>
        </ul>
    </div>
    
    <div class="card">
        <h2>Guia Prático</h2>
        <p>Um guia passo a passo para implementar Documentação 4.0 em seu projeto.</p>
        <a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-guia-pratico.md" class="button">Acessar Guia</a>
    </div>
    
    <div class="card">
        <h2>Demonstração Automática</h2>
        <p>Scripts para demonstração automática das funcionalidades:</p>
        <ul>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-auto-demo-rapido.sh">Versão Rápida</a></li>
            <li><a href="https://github.com/${USERNAME}/${REPO}/blob/main/doc40-auto-demo-simples.sh">Versão Simples</a></li>
        </ul>
    </div>
    
    <footer>
        <p>Material desenvolvido para Campus Party 2025 | <a href="https://github.com/${USERNAME}/${REPO}">Repositório no GitHub</a></p>
    </footer>
</body>
</html>
EOF

echo "Arquivo index.html criado com sucesso!"

# Adicionar o arquivo ao repositório git
git add index.html

# Verificar se há alterações para comitar
if ! git diff --cached --quiet; then
  git commit -m "Atualizar página principal do GitHub Pages para usar slides atualizados"
  echo "Comitado com sucesso!"
  
  # Perguntar se deseja fazer push
  echo "Deseja fazer push das alterações para o GitHub? (s/n)"
  read RESPOSTA
  if [[ $RESPOSTA == "s" || $RESPOSTA == "S" ]]; then
    git push origin main
    echo "Push realizado com sucesso!"
    echo "Página GitHub Pages atualizada: https://${USERNAME}.github.io/${REPO}"
  else
    echo "Push não realizado. Execute 'git push origin main' quando estiver pronto."
  fi
else
  echo "Não há alterações para comitar."
fi

echo "Processo concluído!"