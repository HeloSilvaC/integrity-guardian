#!/bin/bash
# Script de automação do guardião.
# Uso: ./guardiao.sh <diretorio>             -> verifica
#      ./guardiao.sh cadastrar <diretorio>   -> cadastra a referência

# pasta onde está este script (para achar o guardiao de qualquer lugar)
PASTA=$(dirname "$0")

# 1. ver o que foi pedido
if [ $# -eq 1 ]; then
    comando="verificar"
    diretorio="$1"
elif [ $# -eq 2 ]; then
    comando="$1"
    diretorio="$2"
else
    echo "Uso: $0 <diretorio>"
    echo "     $0 cadastrar <diretorio>"
    exit 2
fi

# 2. se o diretório não existe -> avisar e sair com erro
if [ ! -d "$diretorio" ]; then
    echo "Erro: diretório '$diretorio' não encontrado."
    exit 2
fi

# 3. chamar o guardião
if [ "$comando" = "cadastrar" ]; then
    echo "Cadastrando referência de '$diretorio'..."
else
    echo "Iniciando verificação de integridade em '$diretorio'..."
fi
echo

python3 "$PASTA/guardiao" "$comando" "$diretorio"
resultado=$?

echo

# 4. mostrar a mensagem de acordo com o código de saída (ver src/codigos.py)
case "$resultado" in
    0)
        if [ "$comando" = "cadastrar" ]; then
            echo "OK: referência cadastrada."
        else
            echo "OK: nenhuma alteração detectada."
        fi
        ;;
    1)
        echo "Atenção: alterações detectadas!"
        ;;
    *)
        echo "Erro durante a execução (código $resultado)."
        exit 2
        ;;
esac

exit $resultado
