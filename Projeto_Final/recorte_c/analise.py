"""Camada de analise do Recorte C."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
WEEK11_DIR = ROOT_DIR.parent / "semana11_python_pandas"
if str(WEEK11_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK11_DIR))

from pdad_utils import (
    RA_NOMES as NOMES_RA,
    bubble_sort_items as ordenar_bolhas,
    valid_age_mask as mascara_idade_valida,
    valid_income_mask as mascara_renda_valida,
)

LIMITES_IDADE = [0, 17, 29, 44, 59, 120]
ROTULOS_IDADE = ["0-17", "18-29", "30-44", "45-59", "60+"]
LIMITES_RENDA = [0, 900, 1412, 2824, float("inf")]
ROTULOS_RENDA = ["ate 900", "901-1412", "1413-2824", "acima de 2824"]


def rotulo_ra(codigo: int | float | str) -> str:
    """Converte o codigo da RA em um nome legivel."""
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError):
        return str(codigo)
    return f"{NOMES_RA.get(codigo_int, 'RA')} ({codigo_int})"


def faixa_idade(serie: pd.Series) -> pd.Series:
    """Agrupa idades em faixas menores."""
    idades = pd.to_numeric(serie, errors="coerce")
    return pd.cut(idades, bins=LIMITES_IDADE, labels=ROTULOS_IDADE, include_lowest=True, right=True)


def faixa_renda(serie: pd.Series) -> pd.Series:
    """Agrupa rendas em faixas menores."""
    rendas = pd.to_numeric(serie, errors="coerce")
    return pd.cut(rendas, bins=LIMITES_RENDA, labels=ROTULOS_RENDA, include_lowest=True, right=True)


def formatar_percentual(valor: float) -> str:
    """Formata um valor decimal como percentual."""
    if pd.isna(valor):
        return "0.0%"
    return f"{valor * 100:.1f}%"


def montar_linhas_resumo(df: pd.DataFrame, coluna_metrica: str, modo_agrupamento: str) -> list[dict]:
    """Monta o ranking de grupos usado no painel e no relatorio."""
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
    ordenados, _ = ordenar_bolhas(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados


def calcular_estatisticas_metrica(df: pd.DataFrame, coluna_metrica: str) -> dict:
    """Calcula as estatisticas basicas de uma metrica."""
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


def montar_linhas_comparacao_ra(df: pd.DataFrame, coluna_metrica: str, codigos_ra: list[int]) -> list[dict]:
    """Monta a comparacao entre duas ou mais RAs."""
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
    ordenados, _ = ordenar_bolhas(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados


def montar_linhas_relatorio(
    df: pd.DataFrame,
    coluna_metrica: str,
    rotulo_metrica: str,
    rotulo_agrupamento: str,
    linhas_resumo: list[dict],
    codigos_ra: list[int],
) -> list[str]:
    """Monta o conteudo textual do relatorio exportado."""
    estatisticas = calcular_estatisticas_metrica(df, coluna_metrica)
    linhas = [
        "PDAD 2024 - Recorte C",
        "Saude e acesso a servicos",
        "",
        f"Filtro RA: {', '.join(rotulo_ra(code) for code in codigos_ra) if codigos_ra else 'Nenhuma RA marcada'}",
        f"Indicador: {rotulo_metrica}",
        f"Agrupamento: {rotulo_agrupamento}",
        "",
        f"Total selecionado: {estatisticas['total']:,}",
        f"Respostas validas: {estatisticas['valid_metric']:,}",
        f"Casos positivos: {estatisticas['yes_count']:,}",
        f"Taxa positiva: {estatisticas['rate'] * 100:.1f}%",
        "",
        "Ranking dos grupos",
        "-" * 60,
    ]
    for item in linhas_resumo:
        linhas.append(
            f"{item['grupo']} | total={int(item['total']):,} | positivos={int(item['positivo']):,} | taxa={item['taxa'] * 100:.1f}%"
        )
    return linhas
