import tkinter as tk
from tkinter import ttk
import pandas as pd

def criar_dashboard(df_moradores):
    """
    Função que inicializa e exibe o painel visual (Dashboard) 
    com nomes de colunas personalizados.
    """
    
    # Dicionário de tradução para os cabeçalhos da tabela
    nomes_exibicao = {
        "A01uf": "UF",
        "localidade": "Localidade / RA",
        "setor_distrito": "Setor",
        "morador_id": "ID Morador",
        "index": "Nº Registo",
        "idade_calculada": "Idade",
        "G01": "Precisou Atendimento? (12m)",
        "G02": "Tipo de Consulta",
        "G03": "Envolveu Emergência?",
        "G04": "Local do Atendimento",
        "G05": "Possui Plano?",
        "G06": "Já teve filhos?",
        "G06_1": "Qtd Filhos",
        "G06_2": "Idade 1º Filho",
        "renda_ind": "Renda Individual"
    }
    
    # --- Funções de Lógica Internas ---
    def carregar_tabela(dataframe):
        for item in tree.get_children():
            tree.delete(item)
        for _, row in dataframe.iterrows():
            valores_linha = [str(val) if pd.notna(val) else "" for val in row]
            tree.insert("", "end", values=valores_linha)

    def aplicar_filtro():
        termo = entry_filtro.get().strip().lower()
        if not termo:
            carregar_tabela(df_moradores)
            return
        df_filtrado = df_moradores[df_moradores["localidade"].astype(str).str.lower().str.contains(termo, na=False)]
        carregar_tabela(df_filtrado)

    # --- Interface Tkinter ---
    janela = tk.Tk()
    janela.title("Dashboard de Moradores - Dados de Saúde")
    janela.geometry("1000x550") # Ajustei o tamanho para caber os textos maiores

    # Área de Filtro
    frame_filtro = tk.Frame(janela)
    frame_filtro.pack(pady=15, padx=10, fill="x")

    lbl_filtro = tk.Label(frame_filtro, text="Filtrar por Localidade:", font=("Arial", 10, "bold"))
    lbl_filtro.pack(side="left", padx=5)

    entry_filtro = tk.Entry(frame_filtro, width=30)
    entry_filtro.pack(side="left", padx=5)

    btn_filtrar = tk.Button(frame_filtro, text="Buscar / Limpar", command=aplicar_filtro)
    btn_filtrar.pack(side="left", padx=5)

    # Área da Tabela
    frame_tabela = tk.Frame(janela)
    frame_tabela.pack(expand=True, fill="both", padx=10, pady=10)

    scroll_y = ttk.Scrollbar(frame_tabela, orient="vertical")
    scroll_y.pack(side="right", fill="y")
    
    scroll_x = ttk.Scrollbar(frame_tabela, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")

    colunas = list(df_moradores.columns)
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # --- O SEGREDO ESTÁ AQUI ---
    for col in colunas:
        # Se a coluna existir no dicionário, usa o nome bonito. Se não, usa o original (ex: 'G01')
        nome_bonito = nomes_exibicao.get(col, col)
        
        tree.heading(col, text=nome_bonito)
        
        # Podes aumentar a largura (width) das colunas que têm textos maiores
        largura = 180 if "G" in col or col == "localidade" else 100
        tree.column(col, width=largura, anchor="center")

    tree.pack(expand=True, fill="both")
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    carregar_tabela(df_moradores)
    janela.mainloop()