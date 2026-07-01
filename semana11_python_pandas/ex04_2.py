"""Exercicio 4.2 - Menu interativo com opcao de salvar relatorio completo."""

from pathlib import Path

from pdad_utils import ESCOLARIDADE_NOMES, load_domicilios, load_moradores, valid_age_mask


def relatorio_idades_linhas(moradores):
    validos = moradores[valid_age_mask(moradores)]
    idades = validos["idade_calculada"].tolist()
    return [
        f"  Total com idade declarada: {len(idades)}",
        f"  Media: {sum(idades) / len(idades):.1f} anos",
        f"  Minima: {min(idades)} | Maxima: {max(idades)}",
    ]


def relatorio_escolaridade_linhas(moradores):
    contagem = {}
    for _, linha in moradores.iterrows():
        nivel = linha["escolaridade"]
        if nivel in ESCOLARIDADE_NOMES:
            contagem[nivel] = contagem.get(nivel, 0) + 1

    linhas = ["  Escolaridade:"]
    for nivel, total in sorted(contagem.items()):
        linhas.append(f"    {ESCOLARIDADE_NOMES[nivel]}: {total}")
    return linhas


def relatorio_domicilios_linhas(domicilios):
    media_pessoas = sum(domicilios["A01npessoas"]) / len(domicilios)
    return [
        f"  Total de domicilios: {len(domicilios)}",
        f"  Media de moradores por domicilio: {media_pessoas:.1f}",
    ]


def salvar_relatorio_completo(moradores, domicilios):
    linhas = ["RELATORIO COMPLETO PDAD 2024", "=" * 35, ""]
    linhas.append("1. Idades")
    linhas.extend(relatorio_idades_linhas(moradores))
    linhas.append("")
    linhas.append("2. Escolaridade")
    linhas.extend(relatorio_escolaridade_linhas(moradores))
    linhas.append("")
    linhas.append("3. Domicilios")
    linhas.extend(relatorio_domicilios_linhas(domicilios))

    saida = Path(__file__).resolve().parent / "relatorio_completo.txt"
    with open(saida, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")
    print(f"Relatorio salvo em: {saida}")


def main():
    moradores, domicilios = load_moradores(), load_domicilios()

    while True:
        print("\n" + "=" * 40)
        print("  PDAD 2024 - Menu de Relatorios")
        print("=" * 40)
        print("  1. Relatorio de idades")
        print("  2. Relatorio de escolaridade")
        print("  3. Relatorio de domicilios")
        print("  4. Salvar relatorio completo em TXT")
        print("  0. Sair")
        opcao = input("\n  Escolha uma opcao: ").strip()

        if opcao == "1":
            print("\n" + "\n".join(relatorio_idades_linhas(moradores)))
        elif opcao == "2":
            print("\n" + "\n".join(relatorio_escolaridade_linhas(moradores)))
        elif opcao == "3":
            print("\n" + "\n".join(relatorio_domicilios_linhas(domicilios)))
        elif opcao == "4":
            salvar_relatorio_completo(moradores, domicilios)
        elif opcao == "0":
            print("  Ate logo!")
            break
        else:
            print("  Opcao invalida.")


if __name__ == "__main__":
    main()
