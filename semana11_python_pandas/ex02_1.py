"""Exercicio 2.1 - Calcular idade media manualmente."""

from pdad_utils import load_moradores, valid_age_mask


def main():
    moradores = load_moradores()
    idades = moradores.loc[valid_age_mask(moradores), "idade_calculada"].tolist()

    soma = 0
    for idade in idades:
        soma += idade

    media = soma / len(idades)
    mais_velho = max(idades)
    mais_novo = min(idade for idade in idades if idade > 0)

    print(f"Total com idade declarada: {len(idades)}")
    print(f"Soma das idades: {soma}")
    print(f"Media de idade: {media:.1f} anos")
    print(f"Morador mais velho: {mais_velho} anos")
    print(f"Morador mais novo com idade > 0: {mais_novo} anos")


if __name__ == "__main__":
    main()
