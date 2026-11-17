import os
import sys

# pasta onde o guardião guarda a referência e o log (não deve ser monitorada)
PASTA_IGNORADA = ".guardiao"


def avisar_erro(erro):
    # o os.walk chama essa função quando não consegue abrir uma pasta
    print(f"Aviso: não foi possível abrir a pasta {erro.filename}")


def listar_arquivos(diretorio):
    arquivos = []

    for root, dirs, files in os.walk(diretorio, onerror=avisar_erro):
        # tira a pasta do guardião da lista para o os.walk não entrar nela
        if PASTA_IGNORADA in dirs:
            dirs.remove(PASTA_IGNORADA)

        for nome in files:
            caminho = os.path.join(root, nome)
            arquivos.append(caminho)

    return sorted(arquivos)


def main():
    diretorio = sys.argv[1]

    for caminho in listar_arquivos(diretorio):
        print(caminho)


if __name__ == "__main__":
    main()
