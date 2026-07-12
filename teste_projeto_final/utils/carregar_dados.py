from pathlib import Path
import pandas as pd

# Dicionários de Nomes
UF_NOMES = {52: "Goiás", 53: "Distrito Federal"}

RA_NOMES = {
    5301: "Plano Piloto", 5302: "Gama", 5303: "Taguatinga", 5304: "Brazlândia",
    5305: "Sobradinho", 5306: "Planaltina", 5307: "Paranoá", 5308: "Núcleo Bandeirante",
    5309: "Ceilândia", 5310: "Guará", 5311: "Cruzeiro", 5312: "Samambaia",
    5313: "Santa Maria", 5314: "São Sebastião", 5315: "Recanto Das Emas", 5316: "Lago Sul",
    5317: "Riacho Fundo", 5318: "Lago Norte", 5319: "Candangolândia", 5320: "Águas Claras",
    5321: "Riacho Fundo II", 5322: "Sudoeste e Octogonal", 5323: "Varjão", 5324: "Park Way",
    5325: "SCIA", 5326: "Sobradinho II", 5327: "Jardim Botânico", 5328: "Itapoã",
    5329: "SIA", 5330: "Vicente Pires", 5331: "Fercal", 5332: "Sol Nascente / Pôr do Sol",
    5333: "Arniqueira", 5334: "Arapoanga", 5335: "Água Quente", 5336: "Área Rural"
}

# Dicionários de Saúde (G01 a G06)
G01 = {1: "Sim", 2: "Não", 88888: "Não sabe"}
G02 = {1: "Sim, rede pública", 2: "Sim, rede privada", 3: "Sim, ambas", 4: "Não", 88888: "Não sabe", 99999: "Não se aplica"}
G03 = {1: "Sim, rede pública", 2: "Sim, rede privada", 3: "Sim, ambas", 4: "Não", 88888: "Não sabe", 99999: "Não se aplica"}
G04 = {
    0: "Na Região Administrativa", 40: "No município", 1: "Plano Piloto", 2: "Gama",
    3: "Taguatinga", 9: "Ceilândia", 54: "No domicílio", 55: "Telemedicina", 
    56: "Outros locais", 88888: "Não sabe", 99999: "Não se aplica"
}
G05 = {1: "Sim", 2: "Não", 88888: "Não sabe"}
G06 = {1: "Sim", 2: "Não", 88888: "Não sabe", 99999: "Não se aplica"}
G06_1 = {"numero": int, 88888: "Não sabe", 99999: "Não se aplica"}
G06_2 = {"numero": int, 88888: "Não sabe", 99999: "Não se aplica"}
renda_ind = {"numero": float, 88888: "Não sabe", 99999: "Não se aplica"}

COLUNAS_EXIBICAO = [
    "A01uf", "localidade", "morador_id",
    "idade_calculada", "G01", "G02", "G03", "G04", "G05", "G06",
    "G06_1", "G06_2", "renda_ind"
]

BASE_DIR = Path(__file__).resolve().parent / ".." / "dados"

def carregar_moradores():
    """Lê o arquivo CSV bruto da pasta dados."""
    path = BASE_DIR / "moradores.csv"
    return pd.read_csv(path, sep=";", decimal=",", encoding="utf-8-sig")

def mapear_coluna(df, nome_coluna, dicionario):
    """Substitui valores numéricos de uma coluna pelas strings correspondentes."""
    dict_limpo = {k: v for k, v in dicionario.items() if isinstance(k, (int, float))}
    df[nome_coluna] = df[nome_coluna].replace(dict_limpo)
    return df

def qtd_RAs(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the fields used in the dashboard."""
    cleaned = df.copy()
    cleaned = df[df["A01uf"] == 53] # filtro por DF
    for column in ["A01uf", "localidade", "idade_calculada", "renda_ind", "G01", "G05"]:
        if column in cleaned.columns: 
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned

def carregar_moradores_filtados():
    """Carrega os dados e aplica as traduções usando os dicionários."""
    moradores = carregar_moradores()
    
    mapeamentos = {
        "A01uf": UF_NOMES, "localidade": RA_NOMES, "G01": G01, "G02": G02,
        "G03": G03, "G04": G04, "G05": G05, "G06": G06, "G06_1": G06_1,
        "G06_2": G06_2, "renda_ind": renda_ind
    }

    for coluna, dicionario in mapeamentos.items():
        if coluna in moradores.columns:
            moradores = mapear_coluna(moradores, coluna, dicionario)

    moradores_filtrados = moradores[COLUNAS_EXIBICAO].copy()
    # Filtra apenas o Distrito Federal
    return moradores_filtrados[moradores_filtrados["A01uf"] == "Distrito Federal"]

