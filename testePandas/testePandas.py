import pandas as pd

# 1. Carregar a base de dados principal. 
# ATENÇÃO: Verifique se o nome do arquivo abaixo é EXATAMENTE o mesmo que está no seu computador.
df = pd.read_excel('domicilios.xlsx', low_memory=False)

# 2. Dicionário de tradução COMPLETO (Incluindo Área Rural e Entorno de Goiás)
dicionario_localidade = {
    5301: "Plano Piloto", 
    5302: "Gama", 
    5303: "Taguatinga", 
    5304: "Brazlândia",
    5305: "Sobradinho", 
    5306: "Planaltina", 
    5307: "Paranoá", 
    5308: "Núcleo Bandeirante",
    5309: "Ceilândia", 
    5310: "Guará", 
    5311: "Cruzeiro", 
    5312: "Samambaia",
    5313: "Santa Maria", 
    5314: "São Sebastião", 
    5315: "Recanto Das Emas", 
    5316: "Lago Sul",
    5317: "Riacho Fundo", 
    5318: "Lago Norte", 
    5319: "Candangolândia", 
    5320: "Águas Claras",
    5321: "Riacho Fundo II", 
    5322: "Sudoeste e Octogonal", 
    5323: "Varjão", 
    5324: "Park Way",
    5325: "SCIA", 
    5326: "Sobradinho II", 
    5327: "Jardim Botânico", 
    5328: "Itapoã",
    5329: "SIA", 
    5330: "Vicente Pires", 
    5331: "Fercal", 
    5332: "Sol Nascente / Pôr do Sol",
    5333: "Arniqueira", 
    5334: "Arapoanga", 
    5335: "Água Quente", 
    5336: "Área Rural",
    5241: "Águas Lindas de Goiás", 
    5242: "Alexânia", 
    5243: "Cidade Ocidental",
    5244: "Cristalina", 
    5245: "Cocalzinho de Goiás", 
    5246: "Formosa",
    5247: "Luziânia", 
    5248: "Novo Gama", 
    5249: "Padre Bernardo",
    5250: "Planaltina de Goiás", 
    5251: "Santo Antônio do Descoberto",
    5252: "Valparaíso de Goiás"
}

# 3. Criar a nova coluna mapeando os nomes
df['nome_localidade'] = df['localidade'].map(dicionario_localidade)

# 4. Traduzir o tipo de domicílio
dicionario_tipo_domicilio = {
    1: "Casa",
    2: "Apartamento",
    3: "Cômodo"
}
df['tipo_domicilio'] = df['B02'].map(dicionario_tipo_domicilio)

# Visualizar o resultado dos primeiros 10 registros (para confirmar que o 5241 funcionou)
print(df[['localidade', 'nome_localidade', 'B02', 'tipo_domicilio']].head(10))