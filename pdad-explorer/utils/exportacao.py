
from logging import root
from pathlib import Path
# import string


import pandas as pd

carrega = Path(__file__).resolve().parent / "utils/carregar.py"
from utils import  (
    carregar_dados,
    funcoes_gerais,
    estatisticas
)

from utils.funcoes_gerais import (
    rotulo_ra,
    formatar_percentual,
    garantir_colunas_numericas,
    faixa_idade,
    faixa_renda,
    mascara_renda_valida
)

from utils.estatisticas import (
    calcular_estatisticas_metrica,
    montar_linhas_resumo
)



def montar_linhas_relatorio(df: pd.DataFrame, coluna_metrica: str, rotulo_metrica: str, rotulo_agrupamento: str, linhas_resumo: list[dict], codigos_ra: list[int]) -> list[str]:
    """Build the lines exported to TXT."""
    estatisticas = calcular_estatisticas_metrica(df, coluna_metrica)
    lines = [
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
        lines.append(
            f"{item['grupo']} | total={int(item['total']):,} | positivos={int(item['positivo']):,} | taxa={item['taxa'] * 100:.1f}%"
        )
    return lines

def exportar_csv(df: pd.DataFrame, nome_arquivo: str) -> None:
    """Export the DataFrame to a CSV file."""
    df.to_csv(nome_arquivo, index=False)

# exportar_txt()