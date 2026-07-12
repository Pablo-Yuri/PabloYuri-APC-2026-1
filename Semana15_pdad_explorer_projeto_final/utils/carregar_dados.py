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

# Códigos especiais de G04 que NÃO são RAs (locais fora do sistema de RAs)
G04_ESPECIAIS = {
    0: "Na Região Administrativa",
    40: "No município",
    54: "No domicílio",
    55: "Telemedicina",
    56: "Outros locais",
    88888: "Não sabe",
    99999: "Não se aplica",
}

def montar_dicionario_G04():
    """Monta o dicionário de G04 reaproveitando os códigos de RA (sem prefixo 53)."""
    codigos_ra_sem_prefixo = {codigo - 5300: nome for codigo, nome in RA_NOMES.items()}
    dicionario = dict(codigos_ra_sem_prefixo)
    dicionario.update(G04_ESPECIAIS)
    return dicionario

G04 = montar_dicionario_G04()

G05 = {1: "Sim", 2: "Não", 88888: "Não sabe"}
G06 = {1: "Sim", 2: "Não", 88888: "Não sabe", 99999: "Não se aplica"}
G06_1 = {"numero": int, 88888: "Não sabe", 99999: "Não se aplica"}
G06_2 = {"numero": int, 88888: "Não sabe", 99999: "Não se aplica"}

# REQUISITO 6: renda_ind é tratada separadamente (sempre numérica), não traduzida
# para texto, para evitar misturar tipos (float + str) na mesma coluna.
RENDA_SENTINELAS = [88888, 99999]

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

def contar_ras(df: pd.DataFrame) -> int:
    """Retorna a quantidade de RAs distintas presentes no DataFrame."""
    return df["localidade"].nunique()

def carregar_moradores_filtados():
    """Carrega os dados e aplica as traduções usando os dicionários."""
    moradores = carregar_moradores()

    mapeamentos = {
        "A01uf": UF_NOMES, "localidade": RA_NOMES, "G01": G01, "G02": G02,
        "G03": G03, "G04": G04, "G05": G05, "G06": G06, "G06_1": G06_1,
        "G06_2": G06_2
        # renda_ind não entra aqui: é tratada abaixo, mantendo-a numérica
    }

    for coluna, dicionario in mapeamentos.items():
        if coluna in moradores.columns:
            moradores = mapear_coluna(moradores, coluna, dicionario)

    # REQUISITO 6: renda_ind permanece numérica; sentinelas viram NaN
    # (em vez de virarem texto, o que impediria cálculos futuros de média/mediana)
    if "renda_ind" in moradores.columns:
        moradores["renda_ind"] = pd.to_numeric(moradores["renda_ind"], errors="coerce")
        moradores.loc[moradores["renda_ind"].isin(RENDA_SENTINELAS), "renda_ind"] = pd.NA

    moradores_filtrados = moradores[COLUNAS_EXIBICAO].copy()
    # Filtra apenas o Distrito Federal
    return moradores_filtrados[moradores_filtrados["A01uf"] == "Distrito Federal"]
