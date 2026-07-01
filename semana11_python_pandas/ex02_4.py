"""Exercicio 2.4 - Listar moradores com renda declarada."""

from pdad_utils import load_moradores, valid_income_mask


def main():
    moradores = load_moradores()
    com_renda = moradores[valid_income_mask(moradores)]

    soma = 0
    for renda in com_renda["renda_ind"]:
        soma += renda

    media = soma / len(com_renda)
    print(f"Moradores com renda declarada: {len(com_renda)}")
    for _, linha in com_renda.iterrows():
        print(f"  {linha['morador_id']} - R$ {linha['renda_ind']:,.0f}")

    print(f"\nMedia de renda: R$ {media:,.2f}")


if __name__ == "__main__":
    main()
