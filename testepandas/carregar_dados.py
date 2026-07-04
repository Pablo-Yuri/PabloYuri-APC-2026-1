from pathlib import Path

import pandas as pd



MORADORES_FILES = [
    "moradores.csv",
    "moradores_parcial.csv",
    "PDAD_2024-Moradores.csv",
]

DOMICILIOS_FILES = [
    "domicilios.xlsx",
    "domicilios_parcial.xlsx",
    "PDAD_2024-Domicilios.xlsx",
]

RA_NOMES = {
    5301: "Plano Piloto", 5302: "Gama", 5303: "Taguatinga", 5304: "Brazlândia",
    5305: "Sobradinho", 5306: "Planaltina", 5307: "Paranoá", 5308: "Núcleo Bandeirante",
    5309: "Ceilândia", 5310: "Guará", 5311: "Cruzeiro", 5312: "Samambaia",
    5313: "Santa Maria", 5314: "São Sebastião", 5315: "Recanto Das Emas", 5316: "Lago Sul",
    5317: "Riacho Fundo", 5318: "Lago Norte", 5319: "Candangolândia", 5320: "Águas Claras",
    5321: "Riacho Fundo II", 5322: "Sudoeste e Octogonal", 5323: "Varjão", 5324: "Park Way",
    5325: "SCIA", 5326: "Sobradinho II", 5327: "Jardim Botânico", 5328: "Itapoã",
    5329: "SIA", 5330: "Vicente Pires", 5331: "Fercal", 5332: "Sol Nascente / Pôr do Sol",
    5333: "Arniqueira", 5334: "Arapoanga", 5335: "Água Quente", 5336: "Área Rural",
    5241: "Águas Lindas de Goiás", 5242: "Alexânia", 5243: "Cidade Ocidental",
    5244: "Cristalina", 5245: "Cocalzinho de Goiás", 5246: "Formosa",
    5247: "Luziânia", 5248: "Novo Gama", 5249: "Padre Bernardo",
    5250: "Planaltina de Goiás", 5251: "Santo Antônio do Descoberto",
    5252: "Valparaíso de Goiás"
}

# Unidade da Federação (Coluna 'A01uf')
UF_NOMES = {
    52: "Goiás", 
    53: "Distrito Federal"
}

METRICAS = {
    "Plano de saude (G05)": "G05",
    "Atendimento de saude nos ultimos 12 meses (G01)": "G01",
}

AGRUPAMENTOS = {
    "Regiao Administrativa": "ra",
    "Faixa etaria": "age",
    "Faixa de renda": "income",
}

LIMITES_IDADE = [0, 17, 29, 44, 59, 120]
ROTULOS_IDADE = ["0-17", "18-29", "30-44", "45-59", "60+"]
LIMITES_RENDA = [0, 900, 1412, 2824, float("inf")]
ROTULOS_RENDA = ["ate 900", "901-1412", "1413-2824", "acima de 2824"]
COLUNAS_EXIBICAO = ["morador_id", "localidade", "idade_calculada", "renda_ind", "G01", "G05", "id_genero", "escolaridade"]


BASE_DIR = Path(__file__).resolve().parent / "Base_dados"

def carregar_moradores():
    path = BASE_DIR / "moradores.csv"
    # df = :
    return pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig")

# print(carregar_moradores().head(5))


def carregar_domicilios():
    path = BASE_DIR / "domicilios.xlsx"
    return pd.read_excel(path)


def mascara_idade_valida(df):
    return df["idade_calculada"].ne(99999)


def mascara_renda_valida(df):
    return df["renda_ind"].gt(0) & df["renda_ind"].ne(99999) & df["renda_ind"].ne(88888)


def bubble_sort_items(items, key, reverse=False):
    ordered = items[:]
    n = len(ordered)
    swaps = 0
    for i in range(n):
        for j in range(n - i - 1):
            left = key(ordered[j])
            right = key(ordered[j + 1])
            should_swap = left < right if reverse else left > right
            if should_swap:
                ordered[j], ordered[j + 1] = ordered[j + 1], ordered[j]
                swaps += 1
    return ordered, swaps


# def selection_sort_items(items, key, reverse=False):
#     ordered = items[:]
#     n = len(ordered)
#     comparisons = 0
#     for i in range(n):
#         idx_best = i
#         for j in range(i + 1, n):
#             comparisons += 1
#             left = key(ordered[j])
#             best = key(ordered[idx_best])
#             if (left > best and reverse) or (left < best and not reverse):
#                 idx_best = j
#         ordered[i], ordered[idx_best] = ordered[idx_best], ordered[i]
#     return ordered, comparisons


# def insertion_sort_items(items, key, reverse=False):
#     ordered = items[:]
#     comparisons = 0
#     for i in range(1, len(ordered)):
#         current = ordered[i]
#         current_key = key(current)
#         j = i - 1
#         while j >= 0:
#             comparisons += 1
#             left_key = key(ordered[j])
#             should_move = left_key < current_key if reverse else left_key > current_key
#             if not should_move:
#                 break
#             ordered[j + 1] = ordered[j]
#             j -= 1
#         ordered[j + 1] = current
#     return ordered, comparisons

def filtro_por_UF(df, uf_codigo):
    """Filtra o DataFrame para incluir apenas registros de uma UF específica."""
    return df[df["A01uf"] == uf_codigo]
