import tkinter as tk

def atualizar_grafico_barras(eixo, canvas, df_filtrado, coluna_alvo, titulo):
    """Limpa e desenha o gráfico de barras com a métrica selecionada."""
    eixo.clear()
    
    if df_filtrado.empty:
        eixo.set_title("Nenhum dado para exibir")
        canvas.draw()
        return

    contagem_geral = df_filtrado[coluna_alvo].value_counts()
    
    if not contagem_geral.empty:
        eixo.bar(contagem_geral.index.astype(str), contagem_geral.values, color="#0E2F75")
        eixo.set_title(f"Distribuição Geral: {titulo}")
        eixo.set_ylabel("Quantidade")
        eixo.tick_params(axis='x', rotation=15)
    
    eixo.figure.tight_layout()
    canvas.draw()
    
def bubble_sort_items(items):
    """DIFERENCIAL D4: Implementação manual do Bubble Sort para ordenação de listas."""
    ordered = items[:]
    n = len(ordered)
    for i in range(n):
        for j in range(n - i - 1):
            if ordered[j] > ordered[j + 1]:
                ordered[j], ordered[j + 1] = ordered[j + 1], ordered[j]
    return ordered