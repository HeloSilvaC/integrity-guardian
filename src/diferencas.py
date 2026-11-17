import difflib
import os
import shutil
from datetime import datetime

# só guarda cópia de arquivos de texto até 1 MB
TAMANHO_MAXIMO = 1024 * 1024

# quantas linhas de diferença mostrar no máximo por arquivo
MAXIMO_LINHAS = 20


def data_modificacao(caminho):
    """Devolve a data da última modificação do arquivo como texto."""
    segundos = os.path.getmtime(caminho)
    return datetime.fromtimestamp(segundos).strftime("%d/%m/%Y %H:%M:%S")


def ler_texto(caminho):
    """Devolve a lista de linhas do arquivo se ele for texto.
    Se for binário, muito grande ou não der para ler, devolve None."""
    try:
        if os.path.getsize(caminho) > TAMANHO_MAXIMO:
            return None
        with open(caminho, "r", encoding="utf-8") as f:
            return f.readlines()
    except (UnicodeDecodeError, OSError):
        return None


def guardar_copias(diretorio, caminhos, pasta_copias):
    """Copia os arquivos de texto para a pasta de cópias, para depois
    conseguir mostrar o que mudou neles."""
    # apaga as cópias do cadastro anterior
    if os.path.exists(pasta_copias):
        shutil.rmtree(pasta_copias)

    for relativo in caminhos:
        origem = os.path.join(diretorio, relativo)
        if ler_texto(origem) is not None:
            destino = os.path.join(pasta_copias, relativo)
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            shutil.copyfile(origem, destino)


def descrever_alteracao(diretorio, relativo, info_antiga, pasta_copias):
    """Devolve uma lista de linhas de texto explicando o que mudou no arquivo."""
    linhas = []
    caminho_atual = os.path.join(diretorio, relativo)

    # tamanho e data (antes -> agora)
    if "tamanho" in info_antiga:
        linhas.append(f"tamanho: {info_antiga['tamanho']} -> {os.path.getsize(caminho_atual)} bytes")
    if "modificado_em" in info_antiga:
        linhas.append(f"modificado em: {info_antiga['modificado_em']} -> {data_modificacao(caminho_atual)}")

    # conteúdo (só para arquivo de texto)
    texto_antes = ler_texto(os.path.join(pasta_copias, relativo))
    texto_agora = ler_texto(caminho_atual)

    if texto_antes is None or texto_agora is None:
        linhas.append("(arquivo binário ou grande, não dá para mostrar o conteúdo)")
        return linhas

    diferenca = list(difflib.unified_diff(texto_antes, texto_agora, "antes", "agora", n=1))

    # as duas primeiras linhas são o cabeçalho "--- antes" e "+++ agora", pula elas
    diferenca = diferenca[2:]

    for linha in diferenca[:MAXIMO_LINHAS]:
        linhas.append(linha.rstrip("\n"))

    if len(diferenca) > MAXIMO_LINHAS:
        linhas.append(f"... (mais {len(diferenca) - MAXIMO_LINHAS} linhas)")

    return linhas
