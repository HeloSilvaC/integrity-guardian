def comparar(referencia, atual):
    """Recebe dois dicionários {caminho: hash} (o cadastrado e o de agora)
    e devolve três listas: modificados, novos e removidos."""
    modificados = []
    novos = []
    removidos = []

    # olha os arquivos de agora
    for caminho in atual:
        if caminho not in referencia:
            # não estava na referência -> é novo
            novos.append(caminho)
        elif atual[caminho] != referencia[caminho]:
            # estava, mas o hash mudou -> foi modificado
            modificados.append(caminho)

    # olha os arquivos da referência
    for caminho in referencia:
        if caminho not in atual:
            # estava na referência e agora não está -> foi removido
            removidos.append(caminho)

    return modificados, novos, removidos
