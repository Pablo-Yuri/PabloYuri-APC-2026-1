from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent / "Base_dados"

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

ESCOLARIDADE_NOMES = {
    1: "Sem instrução",
    2: "Fundamental incompleto",
    3: "Fundamental completo",
    4: "Médio incompleto",
    5: "Médio completo",
    6: "Superior incompleto",
    7: "Superior completo",
    8: "Pós-graduação",
}


def resolve_data_file(candidates):
    for name in candidates:
        path = BASE_DIR / name
        if path.exists():
            return path
    available = ", ".join(candidates)
    raise FileNotFoundError(f"Nenhum arquivo encontrado em {BASE_DIR} entre: {available}")


def load_moradores():
    path = resolve_data_file(MORADORES_FILES)
    # df = :
    return pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig")


def load_domicilios():
    path = resolve_data_file(DOMICILIOS_FILES)
    return pd.read_excel(path)


def valid_age_mask(df):
    return df["idade_calculada"].ne(99999)


def valid_income_mask(df):
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


def selection_sort_items(items, key, reverse=False):
    ordered = items[:]
    n = len(ordered)
    comparisons = 0
    for i in range(n):
        idx_best = i
        for j in range(i + 1, n):
            comparisons += 1
            left = key(ordered[j])
            best = key(ordered[idx_best])
            if (left > best and reverse) or (left < best and not reverse):
                idx_best = j
        ordered[i], ordered[idx_best] = ordered[idx_best], ordered[i]
    return ordered, comparisons


def insertion_sort_items(items, key, reverse=False):
    ordered = items[:]
    comparisons = 0
    for i in range(1, len(ordered)):
        current = ordered[i]
        current_key = key(current)
        j = i - 1
        while j >= 0:
            comparisons += 1
            left_key = key(ordered[j])
            should_move = left_key < current_key if reverse else left_key > current_key
            if not should_move:
                break
            ordered[j + 1] = ordered[j]
            j -= 1
        ordered[j + 1] = current
    return ordered, comparisons

def filter_by_uf(df, uf_codigo):
    """Filtra o DataFrame para incluir apenas registros de uma UF específica."""
    return df[df["A01uf"] == uf_codigo]
