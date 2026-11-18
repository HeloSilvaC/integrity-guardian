#!/bin/bash
# Demonstração do guardião.
# Uso: ./testes/demo.sh            -> para entre as etapas (Enter para seguir)
#      ./testes/demo.sh --direto   -> roda tudo direto
# Usa uma cópia de testes/arquivos em /tmp/guardiao-demo.

PROJETO=$(cd "$(dirname "$0")/.." && pwd)
DEMO="/tmp/guardiao-demo"
ORIGEM="$PROJETO/testes/arquivos"
LOG="$PROJETO/.guardiao/guardiao.log"

PAUSAR=1
if [ "$1" = "--direto" ]; then
    PAUSAR=0
fi

# cores (só se estiver no terminal)

if [ -t 1 ]; then
    NEGRITO=$'\e[1m'
    FRACO=$'\e[2m'
    NORMAL=$'\e[0m'
    AZUL=$'\e[34m'
    CIANO=$'\e[36m'
    VERDE=$'\e[32m'
    AMARELO=$'\e[33m'
    VERMELHO=$'\e[31m'
else
    NEGRITO="" FRACO="" NORMAL="" AZUL="" CIANO="" VERDE="" AMARELO="" VERMELHO=""
fi

# título da etapa e o resultado esperado
etapa() {
    echo
    echo
    printf "%s▶ %s%s\n" "$NEGRITO$AZUL" "$1" "$NORMAL"
    if [ -n "$2" ]; then
        printf "  %sesperado: %s%s\n" "$FRACO" "$2" "$NORMAL"
    fi
}

# texto explicativo
info() {
    printf "\n  %s\n" "$1"
}

# só mostra o comando
comando() {
    printf "\n%s\$ %s%s\n" "$CIANO" "$1" "$NORMAL"
}

pausa() {
    if [ "$PAUSAR" -eq 1 ]; then
        echo
        read -r -p "${FRACO}  [Enter para continuar]${NORMAL}" _
    fi
}

# mostra o comando, roda e mostra o código de saída
rodar() {
    comando "$*"
    echo
    "$@"
    codigo=$?
    case "$codigo" in
        0) cor="$VERDE";    texto="ok" ;;
        1) cor="$AMARELO";  texto="alterações detectadas" ;;
        *) cor="$VERMELHO"; texto="erro" ;;
    esac
    printf "\n%s● código de saída: %s (%s)%s\n" "$NEGRITO$cor" "$codigo" "$texto" "$NORMAL"
    return $codigo
}

# ---- roteiro ----

cd "$PROJETO" || exit 2

echo
printf "%s🛡  Guardião de Integridade — demonstração%s\n" "$NEGRITO" "$NORMAL"
printf "%s   Códigos de saída: 0 = ok · 1 = alterações detectadas · 2 = erro%s\n" "$FRACO" "$NORMAL"

etapa "0. Preparando uma cópia dos arquivos de teste" "$DEMO"
chmod -R u+rwX "$DEMO" 2>/dev/null
rm -rf "$DEMO"
cp -r "$ORIGEM" "$DEMO"
echo
(cd "$DEMO" && find . \( -type f -o -type l \) | sort | sed 's/^\.\//  · /')
pausa

etapa "1. Cadastrando a referência inicial" "código 0"
rodar ./guardiao.sh cadastrar "$DEMO" --forcar
pausa

etapa "2. Verificando sem mudar nada" "código 0, nenhuma alteração"
rodar ./guardiao.sh "$DEMO"
pausa

etapa "3. Modificando um arquivo" "código 1, 1 modificado"
comando "echo \"linha nova\" >> $DEMO/documentos/notas.txt"
echo "linha nova" >> "$DEMO/documentos/notas.txt"
rodar ./guardiao.sh "$DEMO"
pausa

etapa "4. Criando um arquivo novo" "código 1, + 1 novo"
comando "echo \"sou novo\" > $DEMO/novo.txt"
echo "sou novo" > "$DEMO/novo.txt"
rodar ./guardiao.sh "$DEMO"
pausa

etapa "5. Removendo um arquivo" "código 1, + 1 removido"
comando "rm $DEMO/vazio.txt"
rm "$DEMO/vazio.txt"
rodar ./guardiao.sh "$DEMO"
pausa

etapa "6. Erro: diretório que não existe" "código 2"
rodar ./guardiao.sh /tmp/pasta_que_nao_existe
pausa

etapa "7. Erro: arquivo sem permissão de leitura" "código 2"
if [ "$(id -u)" -eq 0 ]; then
    info "Rodando como root: o root lê qualquer arquivo, então esse teste não"
    info "funciona. Rode o demo como usuário comum para ver esse erro."
else
    # recadastra para não aparecer as alterações de antes
    info "Recadastrando para começar de um estado limpo:"
    rodar ./guardiao cadastrar "$DEMO" --forcar
    comando "chmod 000 $DEMO/dados/vendas.csv"
    chmod 000 "$DEMO/dados/vendas.csv"
    rodar ./guardiao verificar "$DEMO"
    chmod 644 "$DEMO/dados/vendas.csv"
fi
pausa

etapa "8. Erro: referência adulterada" "código 2"
info "Simulando alguém que mexeu na referência sem recalcular o hash dela:"
comando "chmod u+w .guardiao/referencia.json && echo ' ' >> .guardiao/referencia.json"
chmod u+w .guardiao/referencia.json
echo " " >> .guardiao/referencia.json
rodar ./guardiao.sh "$DEMO"
pausa

etapa "9. Log das execuções (últimas 10 linhas)"
comando "tail -n 10 .guardiao/guardiao.log"
echo
tail -n 10 "$LOG"

echo
echo
printf "%s✔ Fim da demonstração%s\n" "$NEGRITO$VERDE" "$NORMAL"
printf "%s  Para deixar o guardião pronto de novo: ./guardiao.sh cadastrar <diretorio> --forcar%s\n" "$FRACO" "$NORMAL"
echo