import os
import sys


def listar_arquivos(diretorio):
    arquivos = []


    for root, dirs, files in os.walk(diretorio):
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