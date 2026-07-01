"""Exercicio 4.3 - Analise completa por RA, com opcao --todas."""

import sys
from pathlib import Path

from pdad_utils import (
    ESCOLARIDADE_NOMES,
    RA_NOMES,
    insertion_sort_items,
    load_moradores,
    valid_age_mask,
)


def bubble_sort_por_idade(lista):
    n = len(lista)
    for i in range(n):
        for j in range(n - i - 1):
            if lista[j]["idade"] > lista[j + 1]["idade"]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def distribuicao_escolaridade(grupo):
    contagem = {}
    for _, linha in grupo.iterrows():
        nivel = linha["escolaridade"]
        if nivel in ESCOLARIDADE_NOMES:
            contagem[nivel] = contagem.get(nivel, 0) + 1

    itens = [
        {"nivel": nivel, "nome": ESCOLARIDADE_NOMES[nivel], "total": total}
        for nivel, total in contagem.items()
    ]
    itens, _ = insertion_sort_items(itens, key=lambda item: item["nome"])
    return itens


def gerar_relatorio(ra_codigo):
    moradores = load_moradores()
    filtro = moradores[moradores["localidade"] == ra_codigo]

    if filtro.empty:
        raise ValueError(f"Nenhum dado encontrado para a RA {ra_codigo}.")

    ra_nome = RA_NOMES.get(ra_codigo, f"RA-{ra_codigo}")
    validos = filtro[valid_age_mask(filtro)]
    idades = validos["idade_calculada"].tolist()

    lista_moradores = []
    for _, linha in validos.iterrows():
        lista_moradores.append(
            {
                "id": linha["morador_id"],
                "idade": linha["idade_calculada"],
                "escolaridade": ESCOLARIDADE_NOMES.get(linha["escolaridade"], "Desconhecida"),
                "renda": linha["renda_ind"] if linha["renda_ind"] not in (99999, 88888) else None,
            }
        )
    lista_moradores = bubble_sort_por_idade(lista_moradores)

    linhas = []
    linhas.append("=" * 55)
    linhas.append(f"  PDAD 2024 - Analise da RA: {ra_nome} (cod. {ra_codigo})")
    linhas.append("=" * 55)
    linhas.append(f"  Total de moradores na amostra : {len(filtro)}")
    linhas.append(f"  Com idade declarada           : {len(validos)}")
    if idades:
        linhas.append(f"  Media de idade                : {sum(idades) / len(idades):.1f} anos")
        linhas.append(f"  Faixa etaria                  : {min(idades)} a {max(idades)} anos")
    linhas.append("")
    linhas.append("  Distribuicao de escolaridade:")
    for item in distribuicao_escolaridade(filtro):
        linhas.append(f"    {item['nome']}: {item['total']}")
    linhas.append("")
    linhas.append("  Moradores (ordenados por idade):")
    linhas.append("  " + "-" * 50)
    for m in lista_moradores:
        renda_str = f"R$ {m['renda']:,.0f}" if m["renda"] else "nao declarada"
        linhas.append(f"  {m['id']:12s} | {m['idade']:3d} anos | {m['escolaridade']:25s} | {renda_str}")
    linhas.append("")
    return linhas, ra_nome


def salvar_relatorio(linhas, destino):
    with open(destino, "w", encoding="utf-8") as arquivo:
        for linha in linhas:
            arquivo.write(linha + "\n")


def main():
    if len(sys.argv) < 2:
        print("Uso: python ex15.py <codigo_ra> [arquivo_saida.txt]")
        print("Uso: python ex15.py --todas [diretorio_saida]")
        sys.exit(1)

    if sys.argv[1] == "--todas":
        destino_base = Path(sys.argv[2]) if len(sys.argv) >= 3 else Path(__file__).resolve().parent / "relatorios_ra"
        destino_base.mkdir(parents=True, exist_ok=True)

        moradores = load_moradores()
        codigos = sorted(moradores["localidade"].dropna().unique().tolist())
        for codigo in codigos:
            try:
                linhas, nome = gerar_relatorio(int(codigo))
            except ValueError:
                continue
            arquivo_saida = destino_base / f"relatorio_{codigo}_{nome.replace(' ', '_')}.txt"
            salvar_relatorio(linhas, arquivo_saida)
            print(f"Salvo: {arquivo_saida}")
        return

    ra = int(sys.argv[1])
    linhas, nome = gerar_relatorio(ra)

    for linha in linhas:
        print(linha)

    if len(sys.argv) >= 3:
        arquivo_saida = Path(sys.argv[2])
        salvar_relatorio(linhas, arquivo_saida)
        print(f"\n  Relatorio salvo em: {arquivo_saida}")


if __name__ == "__main__":
    main()
