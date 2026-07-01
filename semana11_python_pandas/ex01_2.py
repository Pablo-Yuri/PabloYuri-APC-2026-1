"""Exercicio 1.2 - Selecionar colunas relevantes."""

from pdad_utils import load_moradores


def main():
    moradores = load_moradores()
    colunas = [
        "morador_id",
        "localidade",
        "idade_calculada",
        "id_genero",
        "escolaridade",
        "renda_ind",
        "peso_mor",
    ]
    print(moradores[colunas])


if __name__ == "__main__":
    main()
