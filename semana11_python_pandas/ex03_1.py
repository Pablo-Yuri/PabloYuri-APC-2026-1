"""Exercicio 3.1 - Bubble Sort por idade, com contagem de trocas."""

from pdad_utils import bubble_sort_items, load_moradores, valid_age_mask


def main():
    moradores = load_moradores()
    validos = moradores[valid_age_mask(moradores)]
    lista = validos[["morador_id", "idade_calculada"]].to_dict("records")

    ordenada, swaps = bubble_sort_items(lista, key=lambda item: item["idade_calculada"], reverse=True)

    print(f"Trocas realizadas: {swaps}")
    print("Moradores ordenados do mais velho ao mais novo:")
    for item in ordenada:
        print(f"  {item['morador_id']}: {item['idade_calculada']} anos")


if __name__ == "__main__":
    main()
