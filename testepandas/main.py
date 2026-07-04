import pandas as pd

from carregar_dados import (
    carregar_moradores,
    RA_NOMES,
    UF_NOMES
)

from dash import  (    
    criar_dashboard
)


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



def main():
    moradores = carregar_moradores()
    
    colunas = [
        "A01uf", "localidade", "morador_id",
        "idade_calculada", "G01", "G02", "G03", "G04", "G05", "G06",
        "G06_1", "G06_2", "renda_ind"
    ]
    
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

    # Agora, se você imprimir, verá as strings (Ex: "Sim", "Não sabe") em vez dos códigos
    # print(moradores[["G01", "G02", "G06_1", "G06_2"]])
    filtro = moradores[colunas].copy()
    # filtroUF = filtro[filtro["A01uf"] == 53]
    # print(filtro[filtro["A01uf"] == "Distrito Federal"])
    # print(filtro)
    # df_filtro = pd.DataFrame(filtro)
    criar_dashboard(filtro)


if __name__ == "__main__":
    main()