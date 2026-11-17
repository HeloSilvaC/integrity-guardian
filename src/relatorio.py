def mostrar_lista(titulo, simbolo, arquivos):
    if len(arquivos) > 0:
        print(f"{titulo}:")
        for caminho in arquivos:
            print(f"  {simbolo} {caminho}")
        print()


def mostrar_relatorio(analisados, modificados, novos, removidos, inacessiveis):
    print("Verificação concluída.")
    print()
    print(f"Arquivos analisados: {analisados}")
    print(f"Arquivos modificados: {len(modificados)}")
    print(f"Arquivos novos: {len(novos)}")
    print(f"Arquivos removidos: {len(removidos)}")
    if len(inacessiveis) > 0:
        print(f"Arquivos inacessíveis: {len(inacessiveis)}")
    print()

    mostrar_lista("Modificados", "~", modificados)
    mostrar_lista("Novos", "+", novos)
    mostrar_lista("Removidos", "-", removidos)
    mostrar_lista("Inacessíveis (não foi possível ler)", "!", inacessiveis)

    total = len(modificados) + len(novos) + len(removidos)
    if total > 0:
        print("Alterações detectadas!")
    elif len(inacessiveis) > 0:
        print("Verificação incompleta: alguns arquivos não puderam ser lidos.")
    else:
        print("Nenhuma alteração detectada.")
