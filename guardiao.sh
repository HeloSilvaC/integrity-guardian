#!/bin/bash
# Script de automação do guardião.
# Uso: ./guardiao.sh <diretorio>                       -> verifica
#      ./guardiao.sh verificar <diretorio>             -> verifica
#      ./guardiao.sh cadastrar <diretorio> [--forcar]  -> cadastra a referência

# pasta onde está este script (para achar o guardiao de qualquer lugar)
PASTA=$(dirname "$0")

uso() {
    echo "Uso: $0 <diretorio>" >&2
    echo "     $0 verificar <diretorio>" >&2
    echo "     $0 cadastrar <diretorio> [--forcar]" >&2
}

# 1. ver o que foi pedido
if [ "$1" = "cadastrar" ] || [ "$1" = "verificar" ]; then
    comando="$1"
    diretorio="$2"
    shift 2 2>/dev/null || shift $#
    extras=("$@")            # opções que vão direto para o guardiao (ex.: --forcar)
elif [ $# -eq 1 ]; then
    comando="verificar"
    diretorio="$1"
    extras=()
else
    uso
    exit 2
fi

if [ -z "$diretorio" ]; then
    uso
    exit 2
fi

# 2. se o diretório não existe -> avisar e sair com erro
if [ ! -d "$diretorio" ]; then
    echo "Erro: diretório '$diretorio' não encontrado." >&2
    exit 2
fi

# 3. chamar o guardião
if [ "$comando" = "cadastrar" ]; then
    echo "Cadastrando referência de '$diretorio'..."
else
    echo "Iniciando verificação de integridade em '$diretorio'..."
fi
echo

python3 "$PASTA/guardiao" "$comando" "$diretorio" "${extras[@]}"
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
        echo "Erro durante a execução (código $resultado)." >&2
        exit 2
        ;;
esac

exit $resultado