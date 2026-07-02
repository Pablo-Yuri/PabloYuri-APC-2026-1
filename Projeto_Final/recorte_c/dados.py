"""Camada de dados do Recorte C."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
WEEK11_DIR = ROOT_DIR.parent / "semana11_python_pandas"
if str(WEEK11_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK11_DIR))

from pdad_utils import load_moradores

COLUNAS_NUMERICAS = ["localidade", "idade_calculada", "renda_ind", "G01", "G05"]
COLUNAS_EXIBICAO = [
    "morador_id",
    "localidade",
    "idade_calculada",
    "renda_ind",
    "G01",
    "G05",
    "id_genero",
    "escolaridade",
]


def garantir_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Converte as colunas usadas na analise para formato numerico."""
    convertido = df.copy()
    for coluna in COLUNAS_NUMERICAS:
        if coluna in convertido.columns:
            convertido[coluna] = pd.to_numeric(convertido[coluna], errors="coerce")
    return convertido


def carregar_dados_moradores() -> pd.DataFrame:
    """Carrega a base de moradores usada no sistema."""
    return garantir_colunas_numericas(load_moradores())


def selecionar_colunas_exibicao(df: pd.DataFrame, limite: int = 200) -> pd.DataFrame:
    """Retorna uma amostra das colunas exibidas na tabela da interface."""
    colunas = [coluna for coluna in COLUNAS_EXIBICAO if coluna in df.columns]
    return df.loc[:, colunas].head(limite)
