import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



from utils.exportar import (
    exportar_tabela_csv, 
    salvar_relatorio_txt
)
from utils.calcular import (
    atualizar_grafico_barras,
    atualizar_grafico_dispersao,
    bubble_sort_items
)
from utils.carregar_dados import (
    carregar_moradores_filtados,
    RA_NOMES
)

# REQUISITO 6: valores sentinela já traduzidos para texto pelos dicionários
# de carregar_dados.py; precisam ser excluídos antes de qualquer contagem
# ou percentual, para não distorcer a análise.
SENTINELAS_TEXTO = ["Não sabe", "Não se aplica"]


def criar_dashboard(df_moradores):
    """Inicializa e exibe o painel visual principal (Dashboard)."""
    
    nomes_exibicao = {
        "A01uf": "UF", "localidade": "Localidade / RA", "morador_id": "ID Morador", 
        "idade_calculada": "Idade", "G01": "Atendimento (12m)?", "G02": "Tipo de Consulta", 
        "G03": "Emergência?", "G04": "Local do Atendimento", "G05": "Possui Plano?", 
        "G06": "Já teve filhos?", "G06_1": "Qtd Filhos", "G06_2": "Idade 1º Filho", "renda_ind": "Renda Individual"
    }
    
    opcoes_indicadores = {
        "Precisou Atendimento? (G01)": "G01", "Tipo de Consulta (G02)": "G02",
        "Envolveu Emergência? (G03)": "G03", "Local do Atendimento (G04)": "G04",
        "Possui Plano? (G05)": "G05", "Já teve filhos? (G06)": "G06"
    }
    

    def carregar_tabela(dataframe):
        tree.delete(*tree.get_children())
        df_previa = dataframe.head(200) 
        for row in df_previa.itertuples(index=False):
            valores_linha = [str(val) if pd.notna(val) else "" for val in row]
            tree.insert("", "end", values=valores_linha)

    def acao_exportar_txt():
        texto_relatorio = texto_stats.get("1.0", tk.END).strip()
        salvar_relatorio_txt(texto_relatorio)

    def atualizar_estatisticas_e_grafico(df_filtrado):
        texto_stats.config(state="normal")
        texto_stats.delete("1.0", tk.END)

        total_base = len(df_moradores)
        total_filtro = len(df_filtrado)
        
        # REQUISITO 4: Uso de tk.Label formatado com f-string (Labels estáticos fixos na tela)
        lbl_resumo_estatico.config(text=f"Filtrados: {total_filtro:,} de {total_base:,} moradores")
        
        if df_filtrado.empty:
            texto_stats.insert(tk.END, "Nenhum dado selecionado.")
            texto_stats.config(state="disabled")
            lbl_media_idade.config(text="Média de idade: -")
            lbl_qtd_ras.config(text="RAs no filtro: -")
            lbl_perc_plano.config(text="% com plano de saúde: -")
            atualizar_grafico_barras(eixo, canvas, df_filtrado, "", "")
            return

        nome_amigavel = combo_metrica.get()
        coluna_alvo = opcoes_indicadores[nome_amigavel]
        
        # REQUISITO 6: Filtro explícito de sentinelas antes da média de idade
        df_idade_limpa = df_filtrado[~df_filtrado["idade_calculada"].isin([88888, 99999])]

        # REQUISITO 4: estatísticas numéricas adicionais, exibidas via tk.Label + f-string
        media_idade_geral = df_idade_limpa["idade_calculada"].mean() if not df_idade_limpa.empty else 0
        qtd_ras_no_filtro = df_filtrado["localidade"].nunique()

        # % com plano de saúde (G05 == "Sim"), já excluindo sentinelas ("Não sabe")
        df_g05_valido = df_filtrado[~df_filtrado["G05"].isin(SENTINELAS_TEXTO)]
        perc_plano = (df_g05_valido["G05"] == "Sim").mean() * 100 if not df_g05_valido.empty else 0

        lbl_media_idade.config(text=f"Média de idade: {media_idade_geral:.1f} anos")
        lbl_qtd_ras.config(text=f"RAs no filtro: {qtd_ras_no_filtro}")
        lbl_perc_plano.config(text=f"% com plano de saúde: {perc_plano:.1f}%")

        # Relatório de texto
        texto_stats.insert(tk.END, "RELATÓRIO INDIVIDUAL POR RA\n")
        texto_stats.insert(tk.END, "="*40 + "\n\n")
        
        grupos_ra = df_filtrado.groupby("localidade")
        for ra, df_grupo in grupos_ra:
            total_ra = len(df_grupo)
            df_idade_ra = df_idade_limpa[df_idade_limpa["localidade"] == ra]
            media_idade = df_idade_ra["idade_calculada"].mean() if not df_idade_ra.empty else 0
            
            texto_stats.insert(tk.END, f"RA - {ra}\n")
            texto_stats.insert(tk.END, f"  • Moradores: {total_ra:,} | Média Idade Válida: {media_idade:.1f} anos\n")
            
            # REQUISITO 6: remove sentinelas ("Não sabe" / "Não se aplica")
            # antes de calcular percentuais, para não distorcer a análise
            df_grupo_valido = df_grupo[~df_grupo[coluna_alvo].isin(SENTINELAS_TEXTO)]
            total_valido = len(df_grupo_valido)

            contagem = df_grupo_valido[coluna_alvo].value_counts()
            for valor, quantidade in contagem.items():
                percentual = (quantidade / total_valido) * 100 if total_valido else 0
                texto_stats.insert(tk.END, f"      - {valor}: {quantidade} ({percentual:.1f}%)\n")
            texto_stats.insert(tk.END, "\n" + "-"*30 + "\n")

        texto_stats.config(state="disabled")

        # REQUISITO 6: o gráfico também exclui sentinelas antes de contar
        df_grafico_valido = df_filtrado[~df_filtrado[coluna_alvo].isin(SENTINELAS_TEXTO)]
        atualizar_grafico_barras(eixo, canvas, df_grafico_valido, coluna_alvo, nome_amigavel)

    def aplicar_filtro():
        indices_selecionados = listbox_ras.curselection()
        ras_selecionadas = [listbox_ras.get(i) for i in indices_selecionados]
        
        if not ras_selecionadas:
            df_filtrado = df_moradores.copy()
        else:
            df_filtrado = df_moradores[df_moradores["localidade"].isin(ras_selecionadas)]
            
        carregar_tabela(df_filtrado)
        atualizar_estatisticas_e_grafico(df_filtrado)
        return df_filtrado

    def aplicar_filtro_geral():
        """Filtra por RA (opcional) e redesenha o gráfico de dispersão Idade x Renda."""
        ra_selecionada = combo_ra_geral.get()

        # REQUISITO 6: remove sentinelas de idade e renda antes de plotar
        df_base = df_moradores[~df_moradores["idade_calculada"].isin([88888, 99999])]
        df_base = df_base[df_base["renda_ind"].notna()]

        if ra_selecionada and ra_selecionada != "Todas as RAs":
            df_geral = df_base[df_base["localidade"] == ra_selecionada]
        else:
            df_geral = df_base

        # REQUISITO 4: estatísticas exibidas via tk.Label + f-string
        lbl_pontos_geral.config(text=f"Pontos exibidos: {len(df_geral):,}")

        if len(df_geral) >= 2:
            correlacao = df_geral["idade_calculada"].corr(df_geral["renda_ind"])
            lbl_correlacao_geral.config(text=f"Correlação idade x renda: {correlacao:.2f}")
        else:
            lbl_correlacao_geral.config(text="Correlação idade x renda: -")

        atualizar_grafico_dispersao(eixo_geral, canvas_geral, df_geral, ra_selecionada)

    # --- UI Tkinter ---
    janela = tk.Tk()
    janela.title("Dashboard de Moradores - PDAD 2024")
    janela.geometry("1180x760")
    
    cabecalho = ttk.Frame(janela, padding=16)
    cabecalho.pack(fill="x")
    ttk.Label(cabecalho, text="PDAD 2024 - Recorte C: Saúde e Acesso a Serviços", font=("Arial", 14, "bold")).pack(anchor="w")
    ttk.Label(cabecalho, text="Pablo Yuri - 251027307", font=("Arial", 12, "bold")).pack(anchor="w")
    ttk.Label(cabecalho, text="Projeto final APC (Algoritimos e programação de computadores)", font=("Arial", 10, "bold")).pack(anchor="w")
    ttk.Label(cabecalho, text=f"{len(df_moradores):,} moradores carregados no sistema.", font=("Arial", 10)).pack(anchor="w")
    ttk.Label(cabecalho, text=f"{len(df_moradores['localidade'].unique()):,} RAs representadas.", font=("Arial", 10)).pack(anchor="w")

    controles = ttk.LabelFrame(janela, text="Filtros Interativos", padding=12)
    controles.pack(fill="x", padx=16, pady=5)   
    
    frame_metrica = tk.Frame(controles)
    frame_metrica.pack(fill="x", pady=(0, 10))
    ttk.Label(frame_metrica, text="Indicador do Gráfico: ", font=("Arial", 9, "bold")).pack(side="left")
    combo_metrica = ttk.Combobox(frame_metrica, values=list(opcoes_indicadores.keys()), state="readonly", width=40)
    combo_metrica.current(0) 
    combo_metrica.pack(side="left", padx=5)

    ttk.Label(controles, text="Selecione as RAs desejadas:").pack(anchor="w", pady=(0, 2))
    
    frame_listbox = tk.Frame(controles)
    frame_listbox.pack(fill="x", pady=5)

    ttk.Label(frame_listbox, text="Indicadores do Gráfico:",
            font=("Arial", 9, "bold")).pack(anchor="w")

    scroll_lista = ttk.Scrollbar(frame_listbox, orient="vertical")
    scroll_lista.pack(side="right", fill="y")

    listbox_ras = tk.Listbox(
        frame_listbox,
        selectmode=tk.MULTIPLE,   # Permite múltiplas seleções
        yscrollcommand=scroll_lista.set,
        height=6,
        exportselection=False
    )

    listbox_ras.pack(side="left", fill="both", expand=True)
    scroll_lista.config(command=listbox_ras.yview)

    # DIFERENCIAL D4: Usando o nosso bubble_sort_items ao invés do sorted()
    lista_ras_bruta = df_moradores["localidade"].dropna().astype(str).unique().tolist()
    lista_ras_ordenada = bubble_sort_items(lista_ras_bruta)
    for ra in lista_ras_ordenada:
        listbox_ras.insert(tk.END, ra)

    frame_botoes = tk.Frame(controles)
    frame_botoes.pack(fill="x", pady=5)
    
    ttk.Button(frame_botoes, text="Atualizar Dashboard", command=aplicar_filtro).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Exportar CSV", command=lambda: exportar_tabela_csv(aplicar_filtro())).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Exportar TXT", command=acao_exportar_txt).pack(side="left", padx=5)

    caderno = ttk.Notebook(janela)
    caderno.pack(expand=True, fill="both", padx=16, pady=10)

    aba_graficos = ttk.Frame(caderno, padding=10)
    aba_tabela = ttk.Frame(caderno, padding=10)
    aba_analise = ttk.Frame(caderno, padding=10)
    caderno.add(aba_graficos, text="Estatísticas e Gráficos")
    caderno.add(aba_tabela, text="Visualizar Tabela")
    caderno.add(aba_analise, text="Análise Geral (Idade x Renda)")

    # Aba Gráficos
    frame_stats = ttk.LabelFrame(aba_graficos, text="Estatísticas e Relatório", padding=10)
    frame_stats.pack(side="left", fill="y", padx=(0, 10))
    
    # REQUISITO 4: tk.Label formatados com estatísticas (f-string)
    lbl_resumo_estatico = tk.Label(frame_stats, text="Resumo", font=("Arial", 10, "bold"), fg="blue")
    lbl_resumo_estatico.pack(pady=5)

    lbl_media_idade = tk.Label(frame_stats, text="Média de idade: -", font=("Arial", 9))
    lbl_media_idade.pack(anchor="w")

    lbl_qtd_ras = tk.Label(frame_stats, text="RAs no filtro: -", font=("Arial", 9))
    lbl_qtd_ras.pack(anchor="w")

    lbl_perc_plano = tk.Label(frame_stats, text="% com plano de saúde: -", font=("Arial", 9))
    lbl_perc_plano.pack(anchor="w", pady=(0, 8))
    
    scroll_texto = ttk.Scrollbar(frame_stats, orient="vertical")
    scroll_texto.pack(side="right", fill="y")
    texto_stats = tk.Text(frame_stats, width=42, yscrollcommand=scroll_texto.set, font=("Arial", 10), bg="#f5f5f5")
    texto_stats.pack(side="left", fill="both", expand=True)
    scroll_texto.config(command=texto_stats.yview)

    frame_plot = tk.Frame(aba_graficos)
    frame_plot.pack(side="right", fill="both", expand=True)
    
    figura = Figure(figsize=(5, 4), dpi=100)
    eixo = figura.add_subplot(111)
    canvas = FigureCanvasTkAgg(figura, master=frame_plot)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # Aba Tabela
    scroll_y = ttk.Scrollbar(aba_tabela, orient="vertical")
    scroll_y.pack(side="right", fill="y")
    scroll_x = ttk.Scrollbar(aba_tabela, orient="horizontal")
    scroll_x.pack(side="bottom", fill="x")
    
    colunas = list(df_moradores.columns)
    tree = ttk.Treeview(aba_tabela, columns=colunas, show="headings", yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    for col in colunas:
        tree.heading(col, text=nomes_exibicao.get(col, col))
        tree.column(col, width=120, anchor="center")
    tree.pack(expand=True, fill="both")
    scroll_y.config(command=tree.yview)
    scroll_x.config(command=tree.xview)

    # Aba Análise Geral (Idade x Renda, todas as RAs) — DIFERENCIAL D1: 2º tipo de gráfico (dispersão)
    frame_filtro_geral = ttk.LabelFrame(aba_analise, text="Filtro da Análise Geral", padding=12)
    frame_filtro_geral.pack(fill="x", pady=(0, 10))

    ttk.Label(frame_filtro_geral, text="Filtrar por RA: ", font=("Arial", 9, "bold")).pack(side="left")
    combo_ra_geral = ttk.Combobox(
        frame_filtro_geral,
        values=["Todas as RAs"] + lista_ras_ordenada,
        state="readonly",
        width=30
    )
    combo_ra_geral.current(0)
    combo_ra_geral.pack(side="left", padx=5)

    ttk.Button(
        frame_filtro_geral, text="Montar Gráfico", command=aplicar_filtro_geral
    ).pack(side="left", padx=10)

    frame_stats_geral = ttk.Frame(aba_analise)
    frame_stats_geral.pack(fill="x", pady=(0, 10))

    # REQUISITO 4: estatísticas via tk.Label + f-string
    lbl_pontos_geral = tk.Label(frame_stats_geral, text="Pontos exibidos: -", font=("Arial", 9))
    lbl_pontos_geral.pack(side="left", padx=(0, 20))

    lbl_correlacao_geral = tk.Label(frame_stats_geral, text="Correlação idade x renda: -", font=("Arial", 9))
    lbl_correlacao_geral.pack(side="left")

    frame_plot_geral = tk.Frame(aba_analise)
    frame_plot_geral.pack(fill="both", expand=True)

    figura_geral = Figure(figsize=(5, 4), dpi=100)
    eixo_geral = figura_geral.add_subplot(111)
    canvas_geral = FigureCanvasTkAgg(figura_geral, master=frame_plot_geral)
    canvas_geral.get_tk_widget().pack(fill="both", expand=True)

    carregar_tabela(df_moradores)
    atualizar_estatisticas_e_grafico(df_moradores)
    aplicar_filtro_geral()
    
    janela.mainloop()
    
    
def main():
    """Carrega os dados e inicializa a interface gráfica do sistema."""
    print("A carregar os microdados do PDAD 2024. Aguarde...")
    moradores = carregar_moradores_filtados()
    print("Dados carregados com sucesso! A iniciar a interface...")
    
    criar_dashboard(moradores)

if __name__ == "__main__":
    main()