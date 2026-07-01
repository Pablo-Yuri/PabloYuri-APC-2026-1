"""Exercicio 1.4 - Exibir idades declaradas."""

from pdad_utils import load_moradores, valid_age_mask


def main():
    moradores = load_moradores()
    adultos = moradores[valid_age_mask(moradores)]
    print(adultos[["morador_id", "idade_calculada"]])
    print(f"\nCom idade declarada: {len(adultos)}")
    print(f"Sem idade declarada (99999): {len(moradores) - len(adultos)}")


if __name__ == "__main__":
    main()
