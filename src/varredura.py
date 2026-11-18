import os
import sys

# pasta onde o guardião guarda a referência e o log (não deve ser monitorada)
PASTA_IGNORADA = ".guardiao"


def listar_arquivos(diretorio):
    """Percorre o diretório recursivamente e devolve duas listas:
    os arquivos encontrados e as pastas que não deu para abrir."""
    arquivos = []
    pastas_com_erro = []

    def guardar_erro(erro):
        # o os.walk chama essa função quando não consegue abrir uma pasta
        # (sem permissão, por exemplo). Guardamos para avisar depois,
        # senão os arquivos dela iam parecer "removidos".
        print(f"Aviso: não foi possível abrir a pasta {erro.filename}", file=sys.stderr)
        pastas_com_erro.append(erro.filename)

    for root, dirs, files in os.walk(diretorio, onerror=guardar_erro):
        # tira a pasta do guardião da lista para o os.walk não entrar nela
        if PASTA_IGNORADA in dirs:
            dirs.remove(PASTA_IGNORADA)

        for nome in files:
            caminho = os.path.join(root, nome)
            arquivos.append(caminho)

    return sorted(arquivos), sorted(pastas_com_erro)


def main():
    diretorio = sys.argv[1]

    arquivos, pastas_com_erro = listar_arquivos(diretorio)
    for caminho in arquivos:
        print(caminho)
    for pasta in pastas_com_erro:
        print(f"(não foi possível abrir: {pasta})")


if __name__ == "__main__":
    main()