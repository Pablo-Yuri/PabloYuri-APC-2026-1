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

# G01	Nos últimos 12 meses precisou/realizou de atendimento em saúde?	1	Sim
                                                                # 		2	Não
                                                                # 		88888	Não sabe
                                                                
G01 = {
    # Atendimento de saúde nos últimos 12 meses
    1: "Sim",
    2: "Não",
    88888: "Não sabe"
}

                                                                
# G02	Os atendimentos de [Nome do morador] envolveram consulta/prevenção em geral?	1	Sim, na rede pública
                                                                                # 		2	Sim, na rede privada
                                                                                # 		3	Sim, na rede pública e privada
                                                                                # 		4	Não
                                                                                # 		88888	Não sabe
                                                                                # 		99999	Não se aplica
G02 = {
    # Consulta/prevenção em geral
    1: "Sim, na rede pública",
    2: "Sim, na rede privada",
    3: "Sim, na rede pública e privada",
    4: "Não",
    88888: "Não sabe",
    99999: "Não se aplica"
}

                                                                                
# G03	Os atendimentos de [Nome do morador] envolveram emergência?	1	Sim, na rede pública
                                                            # 		2	Sim, na rede privada
                                                            # 		3	Sim, na rede  pública e privada
                                                            # 		4	Não
                                                            # 		88888	Não sabe
                                                            # 		99999	Não se aplica
                          
G03 = {
    # Emergência
    1: "Sim, na rede pública",
    2: "Sim, na rede privada",
    3: "Sim, na rede pública e privada",
    4: "Não",
    88888: "Não sabe",
    99999: "Não se aplica"
}               
                   
# G04	Última localidade procurada para o atendimento em saúde	-	Ver Anexo 9

G04 ={
    # Última localidade procurada para o atendimento em saúde
    0:	"Na Região Adminstrativa",
    40: "No município",
    1: "Plano Piloto",
    2: "Gama",
    3: "Taguatinga",
    4: "Brazlândia",
    5: "Sobradinho",
    6: "Planaltina",
    7: "Paranoá",
    8: "Núcleo Bandeirante",
    9: "Ceilândia",
    10: "Guará",
    11: "Cruzeiro",
    12: "Samambaia",
    13: "Santa Maria",
    14: "São Sebastião",
    15: "Recanto Das Emas",
    16: "Lago Sul",
    17: "Riacho Fundo",
    18: "Lago Norte",
    19: "Candangolândia",
    20: "Águas Claras",
    21: "Riacho Fundo II",
    22: "Sudoeste e Octogonal",
    23: "Varjão",
    24: "Park Way",
    25: "SCIA",
    26: "Sobradinho II",
    27: "Jardim Botânico",
    28: "Itapoã",
    29: "SIA",
    30: "Vicente Pires",
    31: "Fercal",
    32: "Sol Nascente / Pôr do Sol",
    33: "Arniqueira",
    34: "Arapoanga",
    35: "Água Quente",
    41: "Águas Lindas de Goiás",
    42: "Alexânia",
    43: "Cidade Ocidental",
    44: "Cristalina",
    45: "Cocalzinho de Goiás",
    46: "Formosa",
    47: "Luziânia",
    48: "Novo Gama",
    49: "Padre Bernardo",
    50: "Planaltina de Goiás",
    51: "Santo Antônio do Descoberto",
    52: "Valparaíso de Goiás",
    53: "Outros municípios de Goiás",
    54: "No domicílio",
    55: "Pela internet (Telemedicina)",
    56: "Outros locais",
    88888: "Não sabe",
    99999: "Não se aplica"

}

# G05	Possui plano de saúde	1	Sim
                        # 		2	Não
                        # 		88888	Não sabe
                        
G05 = {
    # Possui plano de saúde
    1: "Sim",
    2: "Não",
    88888: "Não sabe"
}
                        
# G06	A [Nome da moradora] já teve algum filho?	1	Sim
                                            # 		2	Não
                                            # 		88888	Não sabe
                                            # 		99999	Não se aplica

G06 = {
    # Já teve algum filho?
    1: "Sim",
    2: "Não",
    88888: "Não sabe",
    99999: "Não se aplica"
}
                                            
# G06_1	Quantos filhos [Nome da moradora] teve?	Númerico	
                                        # 		88888	Não sabe
                                        # 		99999	Não se aplica

G06_1 = {
    # Quantos filhos teve?
    "numero": int,
    88888: "Não sabe",
    99999: "Não se aplica"
}

# G06_2	Quantos anos [Nome da moradora] tinha quando teve o primeiro filho?	Númerico	
                                                            # 		88888	Não sabe
                                                            # 		99999	Não se aplica

G06_2 = {
    # Quantos anos tinha quando teve o primeiro filho?
    "numero": int,
    88888: "Não sabe",
    99999: "Não se aplica"
}

renda_ind = {
    "numero": float,
    88888: "Não sabe",
    99999: "Não se aplica"
}

LIMITES_IDADE = [0, 17, 29, 44, 59, 120]
ROTULOS_IDADE = ["0-17", "18-29", "30-44", "45-59", "60+"]
LIMITES_RENDA = [0, 900, 1412, 2824, float("inf")]
ROTULOS_RENDA = ["ate 900", "901-1412", "1413-2824", "acima de 2824"]
COLUNAS_EXIBICAO = [
        "A01uf", "localidade", "morador_id",
        "idade_calculada", "G01", "G02", "G03", "G04", "G05", "G06",
        "G06_1", "G06_2", "renda_ind"
    ]


BASE_DIR = Path(__file__).resolve().parent / "Base_dados"

def carregar_moradores():
    path = BASE_DIR / "moradores.csv"
    # df = :
    return pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig")

def mapear_coluna(df, nome_coluna, dicionario):
    """
    Substitui os valores numéricos de uma coluna do DataFrame
    pelas strings correspondentes do dicionário.
    """
    # Remove chaves genéricas de tipagem dos dicionários antes de mapear, 
    # como a chave "numero" em G06_1 e G06_2, para evitar erros no Pandas.
    dict_limpo = {k: v for k, v in dicionario.items() if isinstance(k, (int, float))}
    
    # O inplace=False garante que vamos retornar a coluna modificada 
    # sem alterar silenciosamente o dataframe original de forma inesperada.
    df[nome_coluna] = df[nome_coluna].replace(dict_limpo)
    
    return df

def carregar_moradores_filtados():
    moradores = carregar_moradores()
    
    # colunas = [
    #     "A01uf", "localidade", "morador_id",
    #     "idade_calculada", "G01", "G02", "G03", "G04", "G05", "G06",
    #     "G06_1", "G06_2", "renda_ind"
    # ]
    
    # Dicionário organizando qual coluna usa qual mapeamento
    mapeamentos = {
        "A01uf": UF_NOMES,
        "localidade": RA_NOMES,
        "G01": G01,
        "G02": G02,
        "G03": G03,
        "G04": G04,
        "G05": G05,
        "G06": G06,
        "G06_1": G06_1,
        "G06_2": G06_2,
        "renda_ind": renda_ind
    }

    # Aplica a função de mapeamento para cada coluna definida acima
    for coluna, dicionario in mapeamentos.items():
        if coluna in moradores.columns: # Boa prática de segurança para evitar KeyError
            moradores = mapear_coluna(moradores, coluna, dicionario)

    moradores_filtrados = moradores[COLUNAS_EXIBICAO].copy()
    return moradores_filtrados[moradores_filtrados["A01uf"] == "Distrito Federal"]  # Filtra apenas Distrito Federal (UF=53)


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
