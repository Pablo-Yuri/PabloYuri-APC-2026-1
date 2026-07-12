import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Importando do seu arquivo original
from exportar import exportar_tabela_csv

# Importando do novo arquivo que criamos
from grafico import atualizar_grafico_barras

def criar_dashboard(df_moradores):
    """
    Função que inicializa e exibe o painel visual (Dashboard).
    """
    nomes_exibicao = {
        "A01uf": "UF", "localidade": "Localidade / RA", "setor_distrito": "Setor",
        "morador_id": "ID Morador", "index": "Nº Registo", "idade_calculada": "Idade",
        "G01": "Atendimento (12m)?", "G02": "Tipo de Consulta", "G03": "Emergência?",
        "G04": "Local do Atendimento", "G05": "Possui Plano?", "G06": "Já teve filhos?",
        "G06_1": "Qtd Filhos", "G06_2": "Idade 1º Filho", "renda_ind": "Renda Individual"
    }

    opcoes_indicadores = {
        "Precisou Atendimento? (G01)": "G01",
        "Tipo de Consulta (G02)": "G02",
        "Envolveu Emergência? (G03)": "G03",
        "Local do Atendimento (G04)": "G04",
        "Possui Plano? (G05)": "G05",
        "Já teve filhos? (G06)": "G06"
    }
    
    # --- Funções de Lógica Internas ---
    
    def carregar_tabela(dataframe):
        """Limpa a tabela atual e recarrega com uma prévia rápida (Otimizado)."""
        tree.delete(*tree.get_children())
        df_previa = dataframe.head(200) # Mostra apenas as primeiras 200 linhas
        
        for row in df_previa.itertuples(index=False):
            valores_linha = [str(val) if pd.notna(val) else "" for val in row]
            tree.insert("", "end", values=valores_linha)

    def acao_exportar_txt():
        """Pega o texto da tela e manda para o módulo externo salvar."""
        from exportar import salvar_relatorio_txt # Importação local para evitar erro cíclico
        texto_relatorio = texto_stats.get("1.0", tk.END).strip()
        salvar_relatorio_txt(texto_relatorio)

    def atualizar_estatisticas_e_grafico(df_filtrado):
        """Gera o relatório em texto e aciona o módulo externo para desenhar o gráfico."""
        texto_stats.config(state="normal")
        texto_stats.delete("1.0", tk.END)

        # === NOVIDADE: CABEÇALHO DO RELATÓRIO ===
        # Adicionamos o resumo da base total e do que está filtrado
        total_base_moradores = len(df_moradores)
        total_base_ras = df_moradores['localidade'].nunique()
        total_filtro_moradores = len(df_filtrado)
        total_filtro_ras = df_filtrado['localidade'].nunique()

        texto_stats.insert(tk.END, "📊 RESUMO GERAL DO SISTEMA\n")
        texto_stats.insert(tk.END, f"  • Total na Base: {total_base_moradores:,} moradores em {total_base_ras} RAs\n")
        texto_stats.insert(tk.END, f"  • Exibindo Agora: {total_filtro_moradores:,} moradores em {total_filtro_ras} RAs\n")
        texto_stats.insert(tk.END, "="*40 + "\n\n")
        # =========================================

        if df_filtrado.empty:
            texto_stats.insert(tk.END, "Nenhum dado selecionado.")
            texto_stats.config(state="disabled")
            atualizar_grafico_barras(eixo, canvas, df_filtrado, "", "")
            return

        nome_amigavel = combo_metrica.get()
        coluna_alvo = opcoes_indicadores[nome_amigavel]
        
        # Tratamento de valores sentinela
        df_idade_limpa = df_filtrado[~df_filtrado["idade_calculada"].isin([88888, 99999])]
        
        grupos_ra = df_filtrado.groupby("localidade")
        
        for ra, df_grupo in grupos_ra:
            total_ra = len(df_grupo)
            df_idade_ra = df_idade_limpa[df_idade_limpa["localidade"] == ra]
            media_idade = df_idade_ra["idade_calculada"].mean() if not df_idade_ra.empty else 0
            
            texto_stats.insert(tk.END, f"📍 {ra}\n")
            texto_stats.insert(tk.END, f"  • Total de Registros: {total_ra:,}\n")
            texto_stats.insert(tk.END, f"  • Média de Idade Válida: {media_idade:.1f} anos\n")
            
            contagem = df_grupo[coluna_alvo].value_counts()
            texto_stats.insert(tk.END, f"  • Distribuição de '{coluna_alvo}':\n")
            
            for valor, quantidade in contagem.items():
                percentual = (quantidade / total_ra) * 100
                texto_stats.insert(tk.END, f"      - {valor}: {quantidade} ({percentual:.1f}%)\n")
            
            texto_stats.insert(tk.END, "\n" + "-"*30 + "\n\n")

        texto_stats.config(state="disabled") 

        # Chama a função do arquivo externo para cuidar da plotagem
        atualizar_grafico_barras(eixo, canvas, df_filtrado, coluna_alvo, nome_amigavel)

    def aplicar_filtro():
        """Acionado pelo botão 'Atualizar Dashboard'"""
        indices_selecionados = listbox_ras.curselection()
        ras_selecionadas = [listbox_ras.get(i) for i in indices_selecionados]
        
        if not ras_selecionadas:
            df_filtrado = df_moradores.copy()
        else:
            df_filtrado = df_moradores[df_moradores["localidade"].isin(ras_selecionadas)]
            
        carregar_tabela(df_filtrado)
        atualizar_estatisticas_e_grafico(df_filtrado)
        return df_filtrado
        
    def abrir_janela_metodologia():
        """Abre uma janela secundária (Toplevel) com detalhes sobre o projeto."""
        janela_sobre = tk.Toplevel(janela)
        janela_sobre.title("Sobre o Recorte C - Saúde")
        janela_sobre.geometry("500x300")
        janela_sobre.grab_set() 
        
        ttk.Label(janela_sobre, text="Recorte C: Saúde e Acesso a Serviços", font=("Arial", 12, "bold")).pack(pady=10)
        
        descricao = (
            "Este painel explora os microdados do PDAD 2024 referentes à saúde.\n\n"
            "Pergunta central:\n"
            "Qual é a cobertura de plano de saúde e o uso de serviços\n"
            "de saúde no Distrito Federal?\n\n"
            "Variáveis utilizadas:\n"
            "• G01: Necessidade de atendimento nos últimos 12 meses\n"
            "• G02 e G03: Tipo de atendimento e se envolveu emergência\n"
            "• G04: Localidade procurada para atendimento\n"
            "• G05: Posse de plano de saúde particular\n"
            "• Idade e Renda para contextualização demográfica."
        )
        
        lbl_descricao = tk.Label(janela_sobre, text=descricao, justify="left", font=("Arial", 10))
        lbl_descricao.pack(padx=20, pady=10, fill="both")
        ttk.Button(janela_sobre, text="Fechar", command=janela_sobre.destroy).pack(pady=10)

    # --- Interface Tkinter Principal ---
    janela = tk.Tk()
    janela.title("Dashboard de Moradores - PDAD 2024")
    janela.geometry("1180x760")
    
    # Cabeçalho
    cabecalho = ttk.Frame(janela, padding=16)
    cabecalho.pack(fill="x")
    ttk.Label(cabecalho, text="PDAD 2024 - Recorte C: Saúde e Acesso a Serviços", font=("Arial", 14, "bold")).pack(anchor="w")
    ttk.Label(cabecalho, text=f"Moradores carregados: {len(df_moradores):,} | RAs únicas: {df_moradores['localidade'].nunique()}", font=("Arial", 10)).pack(anchor="w", pady=(2, 0))

    # Área de Filtros Interativos
    controles = ttk.LabelFrame(janela, text="Filtros e Configurações (Requisito 2)", padding=12)
    controles.pack(fill="x", padx=16, pady=5)   
    
    frame_metrica = tk.Frame(controles)
    frame_metrica.pack(fill="x", pady=(0, 10))
    ttk.Label(frame_metrica, text="Indicador para o Gráfico e Relatório: ", font=("Arial", 9, "bold")).pack(side="left")
    combo_metrica = ttk.Combobox(frame_metrica, values=list(opcoes_indicadores.keys()), state="readonly", width=40)
    combo_metrica.current(0) 
    combo_metrica.pack(side="left", padx=5)

    ttk.Label(controles, text="Selecione as RAs desejadas (Lista Múltipla):").pack(anchor="w", pady=(0, 2))

    frame_listbox = tk.Frame(controles)
    frame_listbox.pack(fill="x", pady=5)
    scroll_lista = ttk.Scrollbar(frame_listbox, orient="vertical")
    scroll_lista.pack(side="right", fill="y")
    listbox_ras = tk.Listbox(frame_listbox, selectmode=tk.MULTIPLE, yscrollcommand=scroll_lista.set, height=4, exportselection=False)
    listbox_ras.pack(side="left", fill="both", expand=True)
    scroll_lista.config(command=listbox_ras.yview)

    lista_ras_unicas = sorted(df_moradores["localidade"].dropna().astype(str).unique().tolist())
    for ra in lista_ras_unicas:
        listbox_ras.insert(tk.END, ra)

    # Botões de Ação
    frame_botoes = tk.Frame(controles)
    frame_botoes.pack(fill="x", pady=5)
    
    ttk.Button(frame_botoes, text="Atualizar Dashboard", command=aplicar_filtro).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Exportar Tabela CSV", command=lambda: exportar_tabela_csv(aplicar_filtro())).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Exportar Relatório TXT", command=acao_exportar_txt).pack(side="left", padx=5)
    ttk.Button(frame_botoes, text="Metodologia (Sobre)", command=abrir_janela_metodologia).pack(side="right", padx=5)

    # Abas (Notebook)
    caderno = ttk.Notebook(janela)
    caderno.pack(expand=True, fill="both", padx=16, pady=10)

    aba_graficos = ttk.Frame(caderno, padding=10)
    aba_tabela = ttk.Frame(caderno, padding=10)
    caderno.add(aba_graficos, text="Estatísticas e Gráficos")
    caderno.add(aba_tabela, text="Visualizar Tabela")

    # Aba Gráficos e Relatório
    frame_stats = ttk.LabelFrame(aba_graficos, text="Estatísticas por RA (Requisito 4)", padding=10)
    frame_stats.pack(side="left", fill="y", padx=(0, 10))
    
    scroll_texto = ttk.Scrollbar(frame_stats, orient="vertical")
    scroll_texto.pack(side="right", fill="y")
    texto_stats = tk.Text(frame_stats, width=45, yscrollcommand=scroll_texto.set, font=("Arial", 10), bg="#f5f5f5")
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

    # Inicializa as telas
    carregar_tabela(df_moradores)
    atualizar_estatisticas_e_grafico(df_moradores)
    
    janela.mainloop()