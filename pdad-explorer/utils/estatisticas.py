from logging import root
from pathlib import Path
# import string


import pandas as pd

carrega = Path(__file__).resolve().parent / "utils/carregar.py"
from utils import  (
    carregar_dados,
    funcoes_gerais
)
from utils.carregar_dados import (
    AGRUPAMENTOS,
    METRICAS,
    LIMITES_IDADE,
    ROTULOS_IDADE,
    LIMITES_RENDA,
    ROTULOS_RENDA,
    COLUNAS_EXIBICAO,
    RA_NOMES,
    carregar_moradores,
    filtro_por_UF,
    carregar_domicilios,
    mascara_idade_valida,
    bubble_sort_items
)

from utils.funcoes_gerais import (
    rotulo_ra,
    formatar_percentual,
    garantir_colunas_numericas,
    faixa_idade,
    faixa_renda,
    mascara_renda_valida
)


def montar_linhas_resumo(df: pd.DataFrame, coluna_metrica: str, modo_agrupamento: str) -> list[dict]:
    """Compute grouped coverage rows for the selected metric."""
    working = df.copy()
    working = working[working[coluna_metrica].isin([1, 2])]
    working = working.dropna(subset=[coluna_metrica])

    if modo_agrupamento == "ra":
        working = working.dropna(subset=["localidade"])
        working["grupo"] = working["localidade"].map(rotulo_ra)
    elif modo_agrupamento == "age":
        working = working[mascara_idade_valida(working)]
        working["grupo"] = faixa_idade(working["idade_calculada"])
    else:
        working = working[mascara_renda_valida(working)]
        working["grupo"] = faixa_renda(working["renda_ind"])

    working = working.dropna(subset=["grupo"])
    if working.empty:
        return []

    grouped = (
        working.assign(positivo=(working[coluna_metrica] == 1).astype(int))
        .groupby("grupo", dropna=False)
        .agg(total=(coluna_metrica, "size"), positivo=("positivo", "sum"))
        .reset_index()
    )
    grouped["taxa"] = grouped["positivo"] / grouped["total"]

    registros = grouped.to_dict("records")
    ordenados, _ = bubble_sort_items(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados

def calcular_estatisticas_metrica(df: pd.DataFrame, coluna_metrica: str) -> dict:
    """Compute the basic statistics for one metric column."""
    validos = df[df[coluna_metrica].isin([1, 2])]
    positivos = int((validos[coluna_metrica] == 1).sum())
    taxa = positivos / len(validos) if len(validos) else 0.0

    idades_validas = df[mascara_idade_valida(df)]
    rendas_validas = df[mascara_renda_valida(df)]

    return {
        "total": len(df),
        "valid_metric": len(validos),
        "yes_count": positivos,
        "rate": taxa,
        "age_mean": idades_validas["idade_calculada"].mean() if not idades_validas.empty else float("nan"),
        "income_mean": rendas_validas["renda_ind"].mean() if not rendas_validas.empty else float("nan"),
    }

def montar_linhas_previa_tabela(df: pd.DataFrame, limite: int = 200) -> list[tuple]:
    """Create a compact preview of filtered rows for the tree view."""
    previa = df.loc[:, [col for col in COLUNAS_EXIBICAO if col in df.columns]].head(limite)
    linhas: list[tuple] = []
    for _, linha in previa.iterrows():
        linhas.append(
            (
                linha.get("morador_id", ""),
                rotulo_ra(linha.get("localidade", "")),
                "" if pd.isna(linha.get("idade_calculada")) else int(linha.get("idade_calculada")),
                "" if pd.isna(linha.get("renda_ind")) else int(linha.get("renda_ind")),
                linha.get("G01", ""),
                linha.get("G05", ""),
            )
        )
    return linhas

def montar_linhas_comparacao_ra(df: pd.DataFrame, coluna_metrica: str, codigos_ra: list[int]) -> list[dict]:
    """Compute side-by-side comparison rows for the selected RAs."""
    if not codigos_ra:
        return []

    working = df[df["localidade"].isin(codigos_ra)].copy()
    working = working[working[coluna_metrica].isin([1, 2])].dropna(subset=["localidade"])
    if working.empty:
        return []

    grouped = (
        working.assign(positivo=(working[coluna_metrica] == 1).astype(int))
        .groupby("localidade", dropna=False)
        .agg(total=(coluna_metrica, "size"), positivo=("positivo", "sum"))
        .reset_index()
    )
    grouped["taxa"] = grouped["positivo"] / grouped["total"]

    medias_idade = working[mascara_idade_valida(working)].groupby("localidade")["idade_calculada"].mean()
    medias_renda = working[mascara_renda_valida(working)].groupby("localidade")["renda_ind"].mean()

    grouped["nome_ra"] = grouped["localidade"].map(rotulo_ra)
    grouped["media_idade"] = grouped["localidade"].map(medias_idade)
    grouped["media_renda"] = grouped["localidade"].map(medias_renda)

    registros = grouped.to_dict("records")
    ordenados, _ = bubble_sort_items(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados