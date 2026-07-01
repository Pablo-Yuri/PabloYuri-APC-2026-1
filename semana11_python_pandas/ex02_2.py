"""Exercicio 2.2 - Contar moradores por escolaridade."""

from pdad_utils import ESCOLARIDADE_NOMES, load_moradores


def main():
    moradores = load_moradores()

    contagem = {}
    for _, linha in moradores.iterrows():
        nivel = linha["escolaridade"]
        if nivel in ESCOLARIDADE_NOMES:
            contagem[nivel] = contagem.get(nivel, 0) + 1

    print("Escolaridade dos moradores:")
    for nivel, total in sorted(contagem.items()):
        print(f"  {ESCOLARIDADE_NOMES[nivel]}: {total}")

    nivel_mais_comum = max(contagem, key=contagem.get)
    print(f"\nNivel mais comum: {ESCOLARIDADE_NOMES[nivel_mais_comum]}")


if __name__ == "__main__":
    main()
