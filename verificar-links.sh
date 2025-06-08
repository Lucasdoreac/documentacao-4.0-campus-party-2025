#!/bin/bash

# Script para verificar a disponibilidade de URLs no GitHub Pages
BASE_URL="https://lucasdoreac.github.io/documentacao-4.0-campus-party-2025"

# Lista de URLs para verificar
URLS=(
  "/"
  "/index.html"
  "/doc40-slides-atualizados.html"
  "/doc40-slides-antigos.html"
  "/doc40-guia-pratico.md"
)

echo "Verificando URLs no GitHub Pages..."
echo "============================================"

for url in "${URLS[@]}"; do
  full_url="${BASE_URL}${url}"
  echo -n "Verificando $full_url ... "
  
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$full_url")
  
  if [ "$status_code" == "200" ]; then
    echo "✅ OK (200)"
  else
    echo "❌ ERROR ($status_code)"
  fi
done

echo "============================================"
echo "Verificação concluída!"