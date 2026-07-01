"""Exercicio 1.3 - Mostrar moradores por domicilio."""

from pdad_utils import load_domicilios


def main():
    domicilios = load_domicilios()
    for _, linha in domicilios.iterrows():
        print(
            f"Domicilio {linha['A01nficha']}: {linha['A01npessoas']} moradores, "
            f"{linha['A01ncriancas']} criancas"
        )

    idx_pessoas = domicilios["A01npessoas"].idxmax()
    idx_criancas = domicilios["A01ncriancas"].idxmax()
    maior_pessoas = domicilios.loc[idx_pessoas]
    maior_criancas = domicilios.loc[idx_criancas]

    print("\nMaior quantidade de moradores:")
    print(f"  ficha {maior_pessoas['A01nficha']} -> {maior_pessoas['A01npessoas']}")
    print("Maior quantidade de criancas:")
    print(f"  ficha {maior_criancas['A01nficha']} -> {maior_criancas['A01ncriancas']}")


if __name__ == "__main__":
    main()
