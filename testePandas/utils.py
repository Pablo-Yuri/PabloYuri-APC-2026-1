import pdad_utils as utils

# 1. Carrega e recorta a base
df_moradores = utils.load_moradores()
df_recorte = df_moradores[['localidade', 'idade_calculada', 'renda_ind']].copy()
df_recorte['nome_localidade'] = df_recorte['localidade'].map(utils.LOCALIDADE_NOMES)

print(f"Total de pessoas ANTES da limpeza: {len(df_recorte)}")

# ==============================================================================
# O FILTRO DE LIMPEZA
# Mantemos apenas as linhas onde a idade é DIFERENTE (!=) de 99999 
# e a renda é DIFERENTE (!=) de 99999 e 88888.
# ==============================================================================
df_limpo = df_recorte[
    (df_recorte['idade_calculada'] != 99999) & 
    (df_recorte['renda_ind'] != 99999) &
    (df_recorte['renda_ind'] != 88888) # 88888 significa "Não sabe"
]

print(f"Total de pessoas DEPOIS da limpeza: {len(df_limpo)}")

# Traduzindo as localidades para ficar bonito na tela
df_limpo['nome_localidade'] = df_limpo['localidade'].map(utils.LOCALIDADE_NOMES)

# Imprime o resultado final (apenas as 15 primeiras linhas)
print("\n--- Dados Limpos (Prontos para análise) ---")
print(df_limpo[['nome_localidade', 'idade_calculada', 'renda_ind']].head(15))

print("\n--- Filtro 2: Renda alta em Águas Claras ---")

# Para múltiplas condições, use parênteses () em cada uma e o operador & (E)
filtro_renda = df_recorte[
    (df_recorte['nome_localidade'] == 'Águas Claras') & 
    (df_recorte['renda_ind'] > 1000) &
    (df_recorte['renda_ind'] != 99999)
]

print(filtro_renda.head(10))