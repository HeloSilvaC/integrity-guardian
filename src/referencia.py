import json
import os

from src.hashing import calcular_hash


def liberar_escrita(arquivo):
    # a referência fica somente leitura, então antes de sobrescrever
    # precisa liberar a escrita de novo
    if os.path.exists(arquivo):
        os.chmod(arquivo, 0o644)


def salvar_referencia(dados, arquivo):
    """Grava os dados da referência em um arquivo JSON e guarda
    o hash da própria referência em outro arquivo (.sha256)."""
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)

    arquivo_hash = arquivo + ".sha256"
    liberar_escrita(arquivo)
    liberar_escrita(arquivo_hash)

    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

    # salva o hash da referência para depois saber se alguém mexeu nela
    with open(arquivo_hash, "w", encoding="utf-8") as f:
        f.write(calcular_hash(arquivo))

    # deixa os dois arquivos somente leitura
    os.chmod(arquivo, 0o444)
    os.chmod(arquivo_hash, 0o444)


def carregar_referencia(arquivo):
    """Lê o arquivo JSON e devolve os dados da referência."""
    with open(arquivo, "r", encoding="utf-8") as f:
        return json.load(f)


def referencia_foi_alterada(arquivo):
    """Confere se o hash atual da referência é igual ao que foi salvo."""
    arquivo_hash = arquivo + ".sha256"

    # se o arquivo do hash sumiu, não dá para confiar na referência
    if not os.path.exists(arquivo_hash):
        return True

    with open(arquivo_hash, "r", encoding="utf-8") as f:
        hash_salvo = f.read().strip()

    return calcular_hash(arquivo) != hash_salvo
