import tkinter as tk
from tkinter import filedialog, messagebox

# def salvar_relatorio_txt(texto_relatorio: str):
#     """
#     Recebe uma string com o texto do relatório e abre a janela 
#     para o usuário escolher onde salvar o arquivo .txt.
#     """
#     if not texto_relatorio:
#         messagebox.showwarning("Aviso", "Não há dados para exportar.")
#         return

#     caminho = filedialog.asksaveasfilename(
#         title="Salvar Relatório TXT",
#         defaultextension=".txt",
#         filetypes=[("Arquivo de Texto", "*.txt")]
#     )
    
#     if caminho:
#         try:
#             with open(caminho, "w", encoding="utf-8") as arquivo:
#                 arquivo.write("RELATÓRIO DESCRITIVO PDAD 2024\n")
#                 arquivo.write("=" * 40 + "\n\n")
#                 arquivo.write(texto_relatorio)
#             messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{caminho}")
#         except Exception as erro:
#             messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{erro}")


def atualizar_grafico_barras(eixo, canvas, df_filtrado, coluna_alvo, titulo):
    """
    Limpa o gráfico atual e desenha um novo gráfico de barras 
    baseado na coluna selecionada do DataFrame.
    """
    eixo.clear()
    
    if df_filtrado.empty:
        eixo.set_title("Nenhum dado para exibir")
        canvas.draw()
        return

    # Calcula a distribuição
    contagem_geral = df_filtrado[coluna_alvo].value_counts()
    
    if not contagem_geral.empty:
        eixo.bar(contagem_geral.index.astype(str), contagem_geral.values, color="#4CAF50")
        eixo.set_title(f"Distribuição Geral: {titulo}")
        eixo.set_ylabel("Quantidade")
        eixo.tick_params(axis='x', rotation=15)
    
    # tight_layout evita que os textos das bordas sejam cortados
    eixo.figure.tight_layout()
    canvas.draw()