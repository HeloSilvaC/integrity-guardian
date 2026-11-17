#!/bin/bash

# 1. se não veio argumento → mostrar como usar e sair com erro (exit 2)
if [ $# -eq 0 ]; then
    echo "Uso: $0 <diretorio>"
    exit 2
fi

# 2. se o diretório não existe → avisar e sair com erro (exit 2)
if [ ! -d "$1" ]; then
    echo "Erro: diretório '$1' não encontrado."
    exit 2
fi

# 3. mostrar "Iniciando..."
echo "Iniciando verificação de integridade em '$1'..."

# 4. chamar o guardiao repassando o diretório
python3 guardiao "$1"