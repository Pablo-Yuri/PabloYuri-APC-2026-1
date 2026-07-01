"""Exercicio 1.1 - Ler os dados de moradores."""

from pdad_utils import load_moradores


def main():
    moradores = load_moradores()
    print(moradores.head())
    print(f"\nshape = {moradores.shape}")


if __name__ == "__main__":
    main()
