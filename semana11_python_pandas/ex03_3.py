"""Exercicio 3.3 - Ordenar RAs por nome e calcular media de idade."""

from pdad_utils import insertion_sort_items, load_moradores, valid_age_mask


def main():
    moradores = load_moradores()
    codigos = moradores["localidade"].dropna().unique().tolist()

    ras = []
    for codigo in codigos:
        grupo = moradores[moradores["localidade"] == codigo]
        validos = grupo[valid_age_mask(grupo)]
        idades = validos["idade_calculada"].tolist()
        media = sum(idades) / len(idades) if idades else 0
        ras.append(
            {
                "codigo": codigo,
                "nome": f"RA-{codigo}",
                "qtd": len(grupo),
                "media_idade": media,
            }
        )

    ras_ordenadas, _ = insertion_sort_items(ras, key=lambda item: item["nome"])

    print("Regioes Administrativas ordenadas por nome:")
    for ra in ras_ordenadas:
        print(
            f"  {ra['nome']} (cod. {ra['codigo']}): {ra['qtd']} moradores, "
            f"media de idade {ra['media_idade']:.1f}"
        )


if __name__ == "__main__":
    main()
