"""Exercicio 3.2 - Selection Sort por renda, com escolaridade."""

from pdad_utils import ESCOLARIDADE_NOMES, load_moradores, selection_sort_items, valid_income_mask


def main():
    moradores = load_moradores()
    com_renda = moradores[valid_income_mask(moradores)].copy()

    lista = com_renda[["morador_id", "renda_ind", "escolaridade"]].to_dict("records")
    ordenada, comparacoes = selection_sort_items(
        lista,
        key=lambda item: item["renda_ind"],
        reverse=True,
    )

    print(f"Comparacoes realizadas: {comparacoes}")
    print("Moradores ordenados da maior para a menor renda:")
    for item in ordenada:
        escolaridade = ESCOLARIDADE_NOMES.get(item["escolaridade"], "Desconhecida")
        print(f"  {item['morador_id']} - R$ {item['renda_ind']:,.0f} - {escolaridade}")


if __name__ == "__main__":
    main()
