import os
from datetime import datetime


def registrar_log(arquivo_log, comando, diretorio, resultado):
    """Escreve uma linha no log com data, horário, comando e resultado."""
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{agora}] {comando} {diretorio} -> {resultado}\n"

    try:
        os.makedirs(os.path.dirname(arquivo_log), exist_ok=True)
        # "a" = append, adiciona no final sem apagar o que já tinha
        with open(arquivo_log, "a", encoding="utf-8") as f:
            f.write(linha)
    except OSError:
        # se não conseguir escrever o log, só avisa (não para o programa)
        print(f"Aviso: não foi possível escrever no log {arquivo_log}")
