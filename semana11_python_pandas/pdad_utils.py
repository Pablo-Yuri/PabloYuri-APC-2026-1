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
    5249: "Arniqueira",
    5301: "Brasília",
    5303: "Taguatinga",
    5305: "Sobradinho",
    5311: "Cruzeiro",
    5313: "Ceilândia",
    5314: "Sobradinho II",
    5315: "Jardim Botânico",
    5319: "Lago Sul",
    5320: "Gama",
    5326: "Samambaia",
    5328: "Santa Maria",
    5330: "São Sebastião",
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
