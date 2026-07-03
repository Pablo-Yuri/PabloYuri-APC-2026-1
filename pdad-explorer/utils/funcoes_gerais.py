from logging import root
from pathlib import Path
# import string


import pandas as pd

carrega = Path(__file__).resolve().parent / "utils/carregar.py"
from utils import  (
    carregar_dados
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

def rotulo_ra(codigo: int | float | str) -> str:
    """Return a readable label for a RA code."""
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError):
        return str(codigo)
    # print(f"rotulo_ra: codigo={codigo}, codigo_int={codigo_int}, nome={RA_NOMES.get(codigo_int, 'RA')}")
    return f"{RA_NOMES.get(codigo_int, 'RA')} ({codigo_int})"

def formatar_percentual(valor: float) -> str:
    """Format a proportion as a percentage string."""
    if pd.isna(valor):
        return "0.0%"
    return f"{valor * 100:.1f}%"

# print(filtro_por_UF(carregar_moradores(), 53).head(15))
def garantir_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the fields used in the dashboard."""
    cleaned = df.copy()
    cleaned = df[df["A01uf"] == 53] # filtro por DF
    for column in ["localidade", "idade_calculada", "renda_ind", "G01", "G05"]:
        if column in cleaned.columns: 
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned


def faixa_idade(serie: pd.Series) -> pd.Series:
    """Classify ages into compact groups."""
    idades = pd.to_numeric(serie, errors="coerce")
    print("===============================\nteste faixa_idade: idades=\n", idades)
    print(pd.cut(idades, bins=LIMITES_IDADE, labels=ROTULOS_IDADE, include_lowest=True, right=True))
    return pd.cut(idades, bins=LIMITES_IDADE, labels=ROTULOS_IDADE, include_lowest=True, right=True)

def faixa_renda(serie: pd.Series) -> pd.Series:
    """Classify incomes into compact groups."""
    rendas = pd.to_numeric(serie, errors="coerce")
    return pd.cut(rendas, bins=LIMITES_RENDA, labels=ROTULOS_RENDA, include_lowest=True, right=True)

def mascara_renda_valida(df):
    return df["renda_ind"].gt(0) & df["renda_ind"].ne(99999) & df["renda_ind"].ne(88888)


