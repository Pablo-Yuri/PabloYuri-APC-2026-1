import pandas as pd

from carregar_dados import (
    carregar_moradores,
    RA_NOMES,
    UF_NOMES,
    COLUNAS_EXIBICAO,
    carregar_moradores_filtados,
)

from dash import  (    
    criar_dashboard
)

def main():
    moradores = carregar_moradores_filtados()
    criar_dashboard(moradores)


if __name__ == "__main__":
    main()