from pathlib import Path
from typing import List
import pandas as pd

# Define o caminho base de forma dinâmica
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

# ==============================================================================
# DICIONÁRIOS DE TRADUÇÃO DAS VARIÁVEIS (PDAD 2024)
# Use o método .map() do Pandas junto a estes dicionários para traduzir as colunas
# Exemplo: df['nome_localidade'] = df['localidade'].map(LOCALIDADE_NOMES)
# ==============================================================================

# Anexo 1: Variável 'localidade' (Engloba DF, Entorno e Área Rural)
LOCALIDADE_NOMES = {
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

# Espécie do domicílio (Coluna 'B01')
ESPECIE_DOMICILIO = {
    1: "Permanente", 
    2: "Improvisado"
}

# Tipo de domicílio (Coluna 'B02')
TIPO_DOMICILIO = {
    1: "Casa", 
    2: "Apartamento", 
    3: "Cômodo"
}

# Situação de posse do domicílio (Coluna 'B03')
SITUACAO_DOMICILIO = {
    1: "Próprio, já pago (quitado)", 
    2: "Próprio, ainda pagando (financiado)"
}

# Nível socioeconômico PED (Coluna 'grupo_ped')
GRUPO_PED = {
    1: "Alta renda", 
    2: "Média-alta renda", 
    3: "Média-baixa renda", 
    4: "Baixa renda"
}

# Unidade de Planejamento Territorial (Coluna 'UPT')
UPT_NOMES = {
    1: "Central", 
    2: "Central Adjacente 1", 
    3: "Central Adjacente 2", 
    4: "Leste", 
    5: "Norte", 
    6: "Oeste", 
    7: "Sul"
}

# Critério de Classificação Econômica Brasil (Coluna 'criterio_brasil')
CRITERIO_BRASIL = {
    1: "Classe A", 
    2: "Classe B1", 
    3: "Classe B2", 
    4: "Classe C1", 
    5: "Classe C2", 
    6: "Classe DE", 
    7: "Sem classificação"
}

# Composição familiar do domicílio (Coluna 'arranjos')
ARRANJOS_FAMILIARES = {
    1: "Unipessoal", 
    2: "Monoparental feminino", 
    3: "Casal com 1 filho", 
    4: "Casal com 2 filhos", 
    5: "Casal com 3 filhos ou mais", 
    6: "Casal sem filhos", 
    7: "Outro perfil"
}

# Identidade de Gênero do Morador (Coluna 'id_genero')
ID_GENERO = {
    1: "Cisgênero", 
    2: "Transgênero", 
    3: "Outro", 
    99999: "Não se aplica"
}

# Nível de Escolaridade (Mantido do arquivo original)
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

# ==============================================================================
# FUNÇÕES DE CARREGAMENTO E TRATAMENTO
# ==============================================================================

def resolve_data_file(candidates: List[str]) -> Path:
    """Procura pelo primeiro arquivo existente em uma lista de candidatos."""
    for name in candidates:
        path = BASE_DIR / name
        if path.exists():
            return path
            
    available = ", ".join(candidates)
    raise FileNotFoundError(f"Nenhum arquivo encontrado em {BASE_DIR} entre: {available}")


def load_moradores() -> pd.DataFrame:
    """Carrega a base de moradores da PDAD."""
    path = resolve_data_file(MORADORES_FILES)
    # low_memory=False evita avisos de dtypes mistos do Pandas
    return pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig", low_memory=False)


def load_domicilios() -> pd.DataFrame:
    """Carrega a base de domicílios da PDAD."""
    path = resolve_data_file(DOMICILIOS_FILES)
    return pd.read_excel(path)


def valid_age_mask(df: pd.DataFrame) -> pd.Series:
    """Retorna uma máscara booleana para idades válidas (exclui o código de 'não informado' 99999)."""
    return df["idade_calculada"].ne(99999)


def valid_income_mask(df: pd.DataFrame) -> pd.Series:
    """Retorna uma máscara booleana para rendas válidas (maior que 0, exclui ignorados 88888 e 99999)."""
    return df["renda_ind"].gt(0) & ~df["renda_ind"].isin([88888, 99999])