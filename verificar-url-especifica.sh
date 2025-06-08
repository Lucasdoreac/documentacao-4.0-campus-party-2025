#!/bin/bash

# Script para verificar uma URL específica no GitHub Pages
check_url() {
  local url="$1"
  echo -n "Verificando $url ... "
  
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  
  if [ "$status_code" == "200" ]; then
    echo "✅ OK (200)"
    return 0
  else
    echo "❌ ERROR ($status_code)"
    return 1
  fi
}

# Se nenhum argumento for fornecido, pedir a URL
if [ $# -eq 0 ]; then
  read -p "Digite a URL completa para verificar: " url
else
  url="$1"
fi

check_url "$url"

# Se for um erro, tentar obter mais informações
if [ $? -ne 0 ]; then
  echo ""
  echo "Obtendo mais informações sobre o erro..."
  echo "============================================"
  curl -s -I "$url"
  echo "============================================"
fi