import tkinter as tk
import matplotlib.pyplot as plt

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
        eixo.set_xlabel(titulo)  # REQUISITO 3: rótulo do eixo X exigido pela ementa
        eixo.set_ylabel("Quantidade")
        eixo.tick_params(axis='x', rotation=15)

    eixo.figure.tight_layout()
    canvas.draw()

def atualizar_grafico_dispersao(eixo, canvas, df_filtrado, ra_selecionada):
    """Desenha o gráfico de dispersão Idade x Renda Individual, colorido por RA."""
    eixo.clear()

    if df_filtrado.empty:
        eixo.set_title("Nenhum dado para exibir")
        eixo.set_xlabel("Idade")
        eixo.set_ylabel("Renda Individual (R$)")
        canvas.draw()
        return

    if ra_selecionada and ra_selecionada != "Todas as RAs":
        # Uma única RA selecionada: um único ponto de cor por vez
        eixo.scatter(
            df_filtrado["idade_calculada"], df_filtrado["renda_ind"],
            color="#0E2F75", alpha=0.6, s=18
        )
        eixo.set_title(f"Idade x Renda Individual — {ra_selecionada}")
    else:
        # Todas as RAs: cada RA recebe uma cor diferente, com legenda
        ras_unicas = sorted(df_filtrado["localidade"].dropna().unique())
        paleta = plt.get_cmap("tab20", max(len(ras_unicas), 1))
        for indice, ra in enumerate(ras_unicas):
            df_ra = df_filtrado[df_filtrado["localidade"] == ra]
            eixo.scatter(
                df_ra["idade_calculada"], df_ra["renda_ind"],
                color=paleta(indice), alpha=0.6, s=18, label=str(ra)
            )
        eixo.set_title("Idade x Renda Individual — Todas as RAs")
        if len(ras_unicas) <= 12:
            eixo.legend(fontsize=6, loc="upper right", ncol=1)

    eixo.set_xlabel("Idade")
    eixo.set_ylabel("Renda Individual (R$)")
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