import hashlib
import sys

TAMANHO_BLOCO = 4096


def calcular_hash(caminho):
    """Recebe o caminho de um arquivo e devolve o SHA-256
    em hexadecimal (string de 64 caracteres)."""
    # criar um objeto sha256 novo (um por arquivo)
    h = hashlib.sha256()

    # abrir o arquivo em modo binário
    with open(caminho, "rb") as f:
        # repetir até o arquivo acabar
        while True:
            # ler um bloco
            bloco = f.read(TAMANHO_BLOCO)
            # se veio vazio (b''), o arquivo acabou
            if not bloco:
                break
            # entregar o bloco ao update
            h.update(bloco)

    # devolver o hexdigest
    return h.hexdigest()


if __name__ == "__main__":
    caminho = sys.argv[1]
    print(calcular_hash(caminho))