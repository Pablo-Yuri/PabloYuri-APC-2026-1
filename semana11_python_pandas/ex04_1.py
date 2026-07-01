"""Exercicio 4.1 - Gerar relatorio TXT por linha de comando."""

import sys

from pdad_utils import RA_NOMES, insertion_sort_items, load_moradores, valid_age_mask


def linhas_relatorio(moradores):
    validos = moradores[valid_age_mask(moradores)]
    idades = validos["idade_calculada"].tolist()

    linhas = []
    linhas.append("=" * 50)
    linhas.append("RELATORIO PDAD 2024 - MORADORES")
    linhas.append("=" * 50)
    linhas.append(f"Total de moradores na amostra : {len(moradores)}")
    linhas.append(f"Com idade declarada           : {len(validos)}")
    linhas.append(f"Media de idade                : {sum(idades) / len(idades):.1f} anos")
    linhas.append(f"Idade minima                  : {min(idades)} anos")
    linhas.append(f"Idade maxima                  : {max(idades)} anos")
    linhas.append("")

    ras = []
    for codigo, grupo in moradores.groupby("localidade"):
        validos_ra = grupo[valid_age_mask(grupo)]
        idades_ra = validos_ra["idade_calculada"].tolist()
        ras.append(
            {
                "codigo": codigo,
                "nome": RA_NOMES.get(codigo, f"RA-{codigo}"),
                "total": len(grupo),
                "media": sum(idades_ra) / len(idades_ra) if idades_ra else 0,
            }
        )

    ras_ordenadas, _ = insertion_sort_items(ras, key=lambda item: item["nome"])
    linhas.append("Moradores por RA:")
    for ra in ras_ordenadas:
        linhas.append(
            f"  {ra['nome']} (cod. {ra['codigo']}): {ra['total']} moradores, media de idade {ra['media']:.1f} anos"
        )

    return linhas


def main():
    if len(sys.argv) < 2:
        print("Uso: python ex13.py <nome_do_arquivo.txt>")
        sys.exit(1)

    arquivo_saida = sys.argv[1]
    moradores = load_moradores()
    linhas = linhas_relatorio(moradores)

    with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")

    print(f"Relatorio salvo em: {arquivo_saida}")


if __name__ == "__main__":
    main()
