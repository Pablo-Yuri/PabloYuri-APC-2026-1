import tkinter as tk
from tkinter import ttk
import pandas as pd

from carregar_dados import (
    exportar_tabela_csv
    )
from funcoesDash import (
    exportar_tabela_csv,
    alternar_painel_ra
    )



class criar_dashboard():
    
    def __init__(self, root: tk.Tk) -> None:
        self.janela = root
        self.janela.title("PDAD 2024 - Recorte C: Saude e acesso a servicos")
        self.janela.geometry("1180x760")
        self.janela.minsize(1080, 700)

        self.df_moradores = garantir_colunas_numericas(carregar_moradores())
        # self.dados_filtrados = self.df_moradores.copy()
        self.resumo_atual: list[dict] = []
        
        
        # print("=========================================================")
        # print(self.dados_filtrados.head(10))
        
        # ==================================================================================
        self.variavel_metrica = tk.StringVar(value="Plano de saude (G05)")
        self.variavel_agrupamento = tk.StringVar(value="Regiao Administrativa")
        self.variaveis_ra: dict[int, tk.BooleanVar] = {}
        self.painel_ra_visivel = tk.BooleanVar(value=False)
        
        self._montar_estilo()
        self._montar_interface()
        # self.atualizar_visao()

    def _montar_estilo(self) -> None:
        """Configure the visual style of the widgets."""
        style = ttk.Style(self.janela)
        style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 9))
        style.configure("Stat.TLabelframe.Label", font=("Segoe UI", 9, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))

    def _montar_interface(self) -> None:
        """Build the main window, tabs and controls."""
        cabecalho = ttk.Frame(self.janela, padding=16)
        cabecalho.pack(fill="x")

        ttk.Label(cabecalho, text="PDAD 2024 - Recorte C", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            cabecalho,
            text="Saude e acesso a servicos: cobertura de plano, atendimento e comparacoes por grupo.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        ttk.Label(
            cabecalho,
            text=f"Moradores carregados: {len(self.dados_filtrados):,} | RAs presentes: {self.dados_filtrados['localidade'].nunique():,}",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))   
    
    # --- Interface Tkinter ---
    janela = tk.Tk()
    janela.title("Dashboard de Moradores - Dados de Saúde")
    janela.geometry("1180x760") # Ajustei o tamanho para caber os textos maiores
    
    #============================================================================================
    # Cabeçalho 
    cabecalho = ttk.Frame(janela, padding=16)
    cabecalho.pack(fill="x")

    ttk.Label(cabecalho, text="PDAD 2024 - Recorte C", style="Title.TLabel").pack(anchor="w")
    ttk.Label(
        cabecalho,
        text="Saude e acesso a servicos: cobertura de plano, atendimento e comparacoes por grupo.",
        style="Subtitle.TLabel",
    ).pack(anchor="w", pady=(4, 0))

    ttk.Label(
        cabecalho,
        text=f"Moradores carregados: {len(df_moradores):,} | RAs presentes: {df_moradores['localidade'].nunique():,}",
        style="Subtitle.TLabel",
    ).pack(anchor="w", pady=(2, 0))
    #============================================================================================
    
    
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

    # def aplicar_filtro():
    #     termo = entry_filtro.get().strip().lower()
    #     if not termo:
    #         carregar_tabela(df_moradores)
    #         return
    #     df_filtrado = df_moradores[df_moradores["localidade"].astype(str).str.lower().str.contains(termo, na=False)]
    #     carregar_tabela(df_filtrado)
    #     return df_filtrado

    

    
    #============================================================================================
    # Área de Filtro
    
    
    controles = ttk.LabelFrame(janela, text="Filtros", padding=12)
    controles.pack(fill="x", padx=16)

    ttk.Label(controles, text="RAs:").grid(row=0, column=0, sticky="nw", padx=(0, 8), pady=4)
    quadro_ra = ttk.Frame(controles)
    quadro_ra.grid(row=0, column=1, rowspan=2, sticky="w", pady=4)

    # botao_painel_ra = ttk.Button(
    #     quadro_ra,
    #     text="Mostrar selecao de RAs",
    #     command=alternar_painel_ra,
    # )
    # botao_painel_ra.pack(anchor="w")
    
    # controles = ttk.LabelFrame(janela, text="Filtros", padding=12)
    # controles.pack(fill="x", padx=16)
    
    
    # # frame_filtro = tk.Frame(janela)
    # # controle.pack(pady=15, padx=10, fill="x")

    # lbl_filtro = tk.Label(controles, text="Filtrar por Localidade:", font=("Arial", 10, "bold"))
    # lbl_filtro.pack(side="left", padx=5)

    # entry_filtro = tk.Entry(controles, width=30)
    # entry_filtro.pack(side="left", padx=5)

    # btn_filtrar = tk.Button(controles, text="Buscar / Limpar", command=aplicar_filtro)
    # btn_filtrar.pack(side="left", padx=5)
    
    
    # ttk.Button(controles, text="Exportar Tabela CSV", command=lambda: exportar_tabela_csv(aplicar_filtro())).grid(
    # row=4, column=3, sticky="e", pady=(12, 4)
    # )
    #============================================================================================

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