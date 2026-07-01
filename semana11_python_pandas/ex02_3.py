"""Exercicio 2.3 - Filtrar moradores por RA."""

from pdad_utils import RA_NOMES, load_moradores


def main():
    moradores = load_moradores()
    ra_alvo = 5320

    filtro = moradores[moradores["localidade"] == ra_alvo]

    print(f"Moradores da RA {ra_alvo} - {RA_NOMES.get(ra_alvo, 'RA desconhecida')}: ")
    for _, linha in filtro.iterrows():
        print(
            f"  {linha['morador_id']} - {linha['idade_calculada']} anos - "
            f"escolaridade: {linha['escolaridade']}"
        )

    print(f"\nTotal: {len(filtro)} moradores")


if __name__ == "__main__":
    main()
