"""Aplicativo tkinter para o Recorte C da PDAD 2024."""

from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parents[1]
WEEK11_DIR = ROOT_DIR / "semana11_python_pandas"
if str(WEEK11_DIR) not in sys.path:
    sys.path.insert(0, str(WEEK11_DIR))

from pdad_utils import (
    RA_NOMES as NOMES_RA,
    bubble_sort_items as ordenar_bolhas,
    load_moradores as carregar_moradores,
    valid_age_mask as mascara_idade_valida,
    valid_income_mask as mascara_renda_valida,
    filter_by_uf as filtrar_por_uf
)

METRICAS = {
    "Plano de saude (G05)": "G05",
    "Atendimento em saude (G01)": "G01",
}

AGRUPAMENTOS = {
    "Regiao Administrativa": "ra",
    "Faixa etaria": "age",
    "Faixa de renda": "income",
}

LIMITES_IDADE = [0, 17, 29, 44, 59, 120]
ROTULOS_IDADE = ["0-17", "18-29", "30-44", "45-59", "60+"]
LIMITES_RENDA = [0, 900, 1412, 2824, float("inf")]
ROTULOS_RENDA = ["ate 900", "901-1412", "1413-2824", "acima de 2824"]
COLUNAS_EXIBICAO = ["morador_id", "localidade", "idade_calculada", "renda_ind", "G01", "G05", "id_genero", "escolaridade"]


def rotulo_ra(codigo: int | float | str) -> str:
    """Return a readable label for a RA code."""
    try:
        codigo_int = int(codigo)
    except (TypeError, ValueError):
        return str(codigo)
    print(f"rotulo_ra: codigo={codigo}, codigo_int={codigo_int}, nome={NOMES_RA.get(codigo_int, 'RA')}")
    return f"{NOMES_RA.get(codigo_int, 'RA')} ({codigo_int})"


def faixa_idade(serie: pd.Series) -> pd.Series:
    """Classify ages into compact groups."""
    idades = pd.to_numeric(serie, errors="coerce")
    return pd.cut(idades, bins=LIMITES_IDADE, labels=ROTULOS_IDADE, include_lowest=True, right=True)


def faixa_renda(serie: pd.Series) -> pd.Series:
    """Classify incomes into compact groups."""
    rendas = pd.to_numeric(serie, errors="coerce")
    return pd.cut(rendas, bins=LIMITES_RENDA, labels=ROTULOS_RENDA, include_lowest=True, right=True)


def formatar_percentual(valor: float) -> str:
    """Format a proportion as a percentage string."""
    if pd.isna(valor):
        return "0.0%"
    return f"{valor * 100:.1f}%"

# Filtros de dados para o Recorte C
# def garantir_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:
def garantir_colunas_numericas(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the fields used in the dashboard."""
    cleaned = df.copy()
    cleaned = df[df["A01uf"] == 53] # filtro por DF
    for column in ["A01uf", "localidade", "idade_calculada", "renda_ind", "G01", "G05"]:
        if column in cleaned.columns: 
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    return cleaned

# print(filtrar_por_uf(carregar_moradores(), 53).head(16))


def montar_linhas_resumo(df: pd.DataFrame, coluna_metrica: str, modo_agrupamento: str) -> list[dict]:
    """Compute grouped coverage rows for the selected metric."""
    working = df.copy()
    working = working[working[coluna_metrica].isin([1, 2])]
    working = working.dropna(subset=[coluna_metrica])

    if modo_agrupamento == "ra":
        working = working.dropna(subset=["localidade"])
        working["grupo"] = working["localidade"].map(rotulo_ra)
    elif modo_agrupamento == "age":
        working = working[mascara_idade_valida(working)]
        working["grupo"] = faixa_idade(working["idade_calculada"])
    else:
        working = working[mascara_renda_valida(working)]
        working["grupo"] = faixa_renda(working["renda_ind"])

    working = working.dropna(subset=["grupo"])
    if working.empty:
        return []

    grouped = (
        working.assign(positivo=(working[coluna_metrica] == 1).astype(int))
        .groupby("grupo", dropna=False)
        .agg(total=(coluna_metrica, "size"), positivo=("positivo", "sum"))
        .reset_index()
    )
    grouped["taxa"] = grouped["positivo"] / grouped["total"]

    registros = grouped.to_dict("records")
    ordenados, _ = ordenar_bolhas(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados


def calcular_estatisticas_metrica(df: pd.DataFrame, coluna_metrica: str) -> dict:
    """Compute the basic statistics for one metric column."""
    validos = df[df[coluna_metrica].isin([1, 2])]
    positivos = int((validos[coluna_metrica] == 1).sum())
    taxa = positivos / len(validos) if len(validos) else 0.0

    idades_validas = df[mascara_idade_valida(df)]
    rendas_validas = df[mascara_renda_valida(df)]

    return {
        "total": len(df),
        "valid_metric": len(validos),
        "yes_count": positivos,
        "rate": taxa,
        "age_mean": idades_validas["idade_calculada"].mean() if not idades_validas.empty else float("nan"),
        "income_mean": rendas_validas["renda_ind"].mean() if not rendas_validas.empty else float("nan"),
    }


def montar_linhas_previa_tabela(df: pd.DataFrame, limite: int = 200) -> list[tuple]:
    """Create a compact preview of filtered rows for the tree view."""
    previa = df.loc[:, [col for col in COLUNAS_EXIBICAO if col in df.columns]].head(limite)
    linhas: list[tuple] = []
    for _, linha in previa.iterrows():
        linhas.append(
            (
                linha.get("morador_id", ""),
                rotulo_ra(linha.get("localidade", "")),
                "" if pd.isna(linha.get("idade_calculada")) else int(linha.get("idade_calculada")),
                "" if pd.isna(linha.get("renda_ind")) else int(linha.get("renda_ind")),
                linha.get("G01", ""),
                linha.get("G05", ""),
            )
        )
    return linhas


def montar_linhas_comparacao_ra(df: pd.DataFrame, coluna_metrica: str, codigos_ra: list[int]) -> list[dict]:
    """Compute side-by-side comparison rows for the selected RAs."""
    if not codigos_ra:
        return []

    working = df[df["localidade"].isin(codigos_ra)].copy()
    working = working[working[coluna_metrica].isin([1, 2])].dropna(subset=["localidade"])
    if working.empty:
        return []

    grouped = (
        working.assign(positivo=(working[coluna_metrica] == 1).astype(int))
        .groupby("localidade", dropna=False)
        .agg(total=(coluna_metrica, "size"), positivo=("positivo", "sum"))
        .reset_index()
    )
    grouped["taxa"] = grouped["positivo"] / grouped["total"]

    medias_idade = working[mascara_idade_valida(working)].groupby("localidade")["idade_calculada"].mean()
    medias_renda = working[mascara_renda_valida(working)].groupby("localidade")["renda_ind"].mean()

    grouped["nome_ra"] = grouped["localidade"].map(rotulo_ra)
    grouped["media_idade"] = grouped["localidade"].map(medias_idade)
    grouped["media_renda"] = grouped["localidade"].map(medias_renda)

    registros = grouped.to_dict("records")
    ordenados, _ = ordenar_bolhas(registros, key=lambda item: item["taxa"], reverse=True)
    return ordenados


def montar_linhas_relatorio(df: pd.DataFrame, coluna_metrica: str, rotulo_metrica: str, rotulo_agrupamento: str, linhas_resumo: list[dict], codigos_ra: list[int]) -> list[str]:
    """Build the lines exported to TXT."""
    estatisticas = calcular_estatisticas_metrica(df, coluna_metrica)
    lines = [
        "PDAD 2024 - Recorte C",
        "Saude e acesso a servicos",
        "",
        f"Filtro RA: {', '.join(rotulo_ra(code) for code in codigos_ra) if codigos_ra else 'Nenhuma RA marcada'}",
        f"Indicador: {rotulo_metrica}",
        f"Agrupamento: {rotulo_agrupamento}",
        "",
        f"Total selecionado: {estatisticas['total']:,}",
        f"Respostas validas: {estatisticas['valid_metric']:,}",
        f"Casos positivos: {estatisticas['yes_count']:,}",
        f"Taxa positiva: {estatisticas['rate'] * 100:.1f}%",
        "",
        "Ranking dos grupos",
        "-" * 60,
    ]
    for item in linhas_resumo:
        lines.append(
            f"{item['grupo']} | total={int(item['total']):,} | positivos={int(item['positivo']):,} | taxa={item['taxa'] * 100:.1f}%"
        )
    return lines

# Inicio - Configuração da janela
class AplicativoRecorteC:
    """Tkinter application for the Recorte C dashboard."""

    def __init__(self, root: tk.Tk) -> None:
        self.janela = root
        self.janela.title("PDAD 2024 - Recorte C: Saude e acesso a servicos")
        self.janela.geometry("1180x760")
        self.janela.minsize(1080, 700)

        self.dados = garantir_colunas_numericas(carregar_moradores())
        self.dados_filtrados = self.dados.copy()
        # print(self.dados_filtrados.head(5))
        self.resumo_atual: list[dict] = []
        # ==================================================================================
        self.variavel_metrica = tk.StringVar(value="Plano de saude (G05)")
        self.variavel_agrupamento = tk.StringVar(value="Regiao Administrativa")
        self.variaveis_ra: dict[int, tk.BooleanVar] = {}
        self.painel_ra_visivel = tk.BooleanVar(value=False)

        self._montar_estilo()
        self._montar_interface()
        self.atualizar_visao()

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
            text=f"Moradores carregados: {len(self.dados):,} | RAs presentes: {self.dados['localidade'].nunique():,}",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        controles = ttk.LabelFrame(self.janela, text="Filtros", padding=12)
        controles.pack(fill="x", padx=16)

        ttk.Label(controles, text="RAs:").grid(row=0, column=0, sticky="nw", padx=(0, 8), pady=4)
        quadro_ra = ttk.Frame(controles)
        quadro_ra.grid(row=0, column=1, rowspan=2, sticky="w", pady=4)

        self.botao_painel_ra = ttk.Button(
            quadro_ra,
            text="Mostrar selecao de RAs",
            command=self.alternar_painel_ra,
        )
        self.botao_painel_ra.pack(anchor="w")

        self.rotulo_status_ra = ttk.Label(quadro_ra, text="Todas as RAs estao selecionadas.")
        self.rotulo_status_ra.pack(anchor="w", pady=(4, 0))

        self.painel_ra = ttk.LabelFrame(quadro_ra, text="Selecionar RAs", padding=8)
        self.painel_ra.pack(anchor="w", fill="both", expand=False, pady=(8, 0))

        corpo_painel_ra = ttk.Frame(self.painel_ra)
        corpo_painel_ra.pack(fill="both", expand=True)

        self.tela_ra = tk.Canvas(corpo_painel_ra, width=280, height=180, highlightthickness=0)
        self.tela_ra.grid(row=0, column=0, sticky="nsew")
        barra_rolagem_ra = ttk.Scrollbar(corpo_painel_ra, orient="vertical", command=self.tela_ra.yview)
        barra_rolagem_ra.grid(row=0, column=1, sticky="ns")
        self.tela_ra.configure(yscrollcommand=barra_rolagem_ra.set)

        conteudo_ra = ttk.Frame(self.tela_ra)
        self.janela_tela_ra = self.tela_ra.create_window((0, 0), window=conteudo_ra, anchor="nw")

        conteudo_ra.bind(
            "<Configure>",
            lambda _event: self.tela_ra.configure(scrollregion=self.tela_ra.bbox("all")),
        )
        self.tela_ra.bind(
            "<Configure>",
            lambda evento: self.tela_ra.itemconfigure(self.janela_tela_ra, width=evento.width),
        )

        for opcao in self._opcoes_ra():
            codigo = self._extrair_codigo_ra(opcao)
            if codigo is None:
                continue
            self.variaveis_ra[codigo] = tk.BooleanVar(value=True)
            ttk.Checkbutton(
                conteudo_ra,
                text=opcao,
                variable=self.variaveis_ra[codigo],
                command=self.atualizar_visao,
            ).pack(anchor="w", pady=1)

        botoes_ra = ttk.Frame(quadro_ra)
        botoes_ra.pack(anchor="w", pady=(8, 0))
        ttk.Button(botoes_ra, text="Marcar todas", command=self.selecionar_todas_ras).pack(side="left")
        ttk.Button(botoes_ra, text="Desmarcar", command=self.limpar_selecao_ra).pack(side="left", padx=6)
        ttk.Button(botoes_ra, text="Ocultar/mostrar", command=self.alternar_painel_ra).pack(side="left")

        self.painel_ra.pack_forget()

        ttk.Label(controles, text="Indicador:").grid(row=0, column=2, sticky="w", padx=(24, 8), pady=4)
        self.combo_metrica = ttk.Combobox(
            controles,
            textvariable=self.variavel_metrica,
            values=list(METRICAS.keys()),
            state="readonly",
            width=28,
        )
        self.combo_metrica.grid(row=0, column=3, sticky="w", pady=4)

        ttk.Label(controles, text="Agrupar por:").grid(row=2, column=0, sticky="w", padx=(0, 8), pady=(12, 4))
        self.combo_agrupamento = ttk.Combobox(
            controles,
            textvariable=self.variavel_agrupamento,
            values=list(AGRUPAMENTOS.keys()),
            state="readonly",
            width=28,
        )
        self.combo_agrupamento.grid(row=2, column=1, sticky="w", pady=(12, 4))

        ttk.Button(controles, text="Atualizar", style="Accent.TButton", command=self.atualizar_visao).grid(
            row=2, column=3, sticky="e", pady=(12, 4)
        )

        self.combo_metrica.bind("<<ComboboxSelected>>", lambda _event: self.atualizar_visao())
        self.combo_agrupamento.bind("<<ComboboxSelected>>", lambda _event: self.atualizar_visao())

        self.caderno = ttk.Notebook(self.janela)
        self.caderno.pack(fill="both", expand=True, padx=16, pady=16)

        self.aba_painel = ttk.Frame(self.caderno, padding=8)
        self.aba_tabela = ttk.Frame(self.caderno, padding=8)
        self.aba_comparacao = ttk.Frame(self.caderno, padding=8)
        self.caderno.add(self.aba_painel, text="Painel")
        self.caderno.add(self.aba_tabela, text="Dados filtrados")
        self.caderno.add(self.aba_comparacao, text="Comparar RAs")

        self._montar_aba_painel()
        self._montar_aba_tabela()
        self._montar_aba_comparacao()

        rodape = ttk.Frame(self.janela, padding=(16, 0, 16, 16))
        rodape.pack(fill="x")
        ttk.Button(rodape, text="Exportar TXT", command=self.exportar_txt).pack(side="left")
        ttk.Button(rodape, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=8)
        ttk.Button(rodape, text="Sair", command=self.janela.destroy).pack(side="right")

    def _montar_aba_painel(self) -> None:
        """Create the statistics panel and chart canvas."""
        coluna_esquerda = ttk.Frame(self.aba_painel)
        coluna_esquerda.pack(side="left", fill="y", padx=(0, 12))

        self.quadro_estatisticas = ttk.LabelFrame(coluna_esquerda, text="Estatisticas", padding=12)
        self.quadro_estatisticas.pack(fill="x", pady=(0, 12))

        self.rotulo_total = ttk.Label(self.quadro_estatisticas, text="Total selecionado: -")
        self.rotulo_validos = ttk.Label(self.quadro_estatisticas, text="Respostas validas: -")
        self.rotulo_positivos = ttk.Label(self.quadro_estatisticas, text="Casos positivos: -")
        self.rotulo_taxa = ttk.Label(self.quadro_estatisticas, text="Taxa: -")
        self.rotulo_idade = ttk.Label(self.quadro_estatisticas, text="Idade media: -")
        self.rotulo_renda = ttk.Label(self.quadro_estatisticas, text="Renda media valida: -")
        for rotulo in [self.rotulo_total, self.rotulo_validos, self.rotulo_positivos, self.rotulo_taxa, self.rotulo_idade, self.rotulo_renda]:
            rotulo.pack(anchor="w", pady=2)

        self.quadro_ranking = ttk.LabelFrame(coluna_esquerda, text="Ranking do grupo", padding=12)
        self.quadro_ranking.pack(fill="both", expand=True)

        self.texto_ranking = tk.Text(self.quadro_ranking, width=44, height=24, wrap="word")
        self.texto_ranking.pack(fill="both", expand=True)
        self.texto_ranking.configure(state="disabled")

        coluna_direita = ttk.Frame(self.aba_painel)
        coluna_direita.pack(side="left", fill="both", expand=True)

        self.figura = Figure(figsize=(7.6, 5.6), dpi=100)
        self.eixo = self.figura.add_subplot(111)
        self.tela_canvas = FigureCanvasTkAgg(self.figura, master=coluna_direita)
        self.tela_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _montar_aba_tabela(self) -> None:
        """Create the filtered data preview area."""
        colunas = ("morador_id", "localidade", "idade_calculada", "renda_ind", "G01", "G05")
        self.arvore = ttk.Treeview(self.aba_tabela, columns=colunas, show="headings", height=18)
        cabecas = {
            "morador_id": "Morador",
            "localidade": "RA",
            "idade_calculada": "Idade",
            "renda_ind": "Renda",
            "G01": "Atendimento",
            "G05": "Plano",
        }
        larguras = {
            "morador_id": 140,
            "localidade": 180,
            "idade_calculada": 90,
            "renda_ind": 110,
            "G01": 110,
            "G05": 90,
        }
        for coluna in colunas:
            self.arvore.heading(coluna, text=cabecas[coluna])
            self.arvore.column(coluna, width=larguras[coluna], anchor="center")
        self.arvore.pack(fill="both", expand=True)

    def _montar_aba_comparacao(self) -> None:
        """Create the comparison panel for selected RAs."""
        cabecalho = ttk.Frame(self.aba_comparacao)
        cabecalho.pack(fill="x", pady=(0, 12))

        ttk.Label(
            cabecalho,
            text="Comparacao de RAs marcadas",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            cabecalho,
            text="Marque duas ou mais RAs no filtro oculto e clique em 'Atualizar comparacao'.",
        ).pack(anchor="w", pady=(4, 0))

        acoes = ttk.Frame(self.aba_comparacao)
        acoes.pack(fill="x", pady=(0, 12))
        ttk.Button(acoes, text="Atualizar comparacao", command=self.abrir_comparacao_ra).pack(side="left")

        corpo = ttk.Frame(self.aba_comparacao)
        corpo.pack(fill="both", expand=True)

        coluna_esquerda = ttk.Frame(corpo)
        coluna_esquerda.pack(side="left", fill="y", padx=(0, 12))

        self.texto_comparacao = tk.Text(coluna_esquerda, width=44, height=26, wrap="word")
        self.texto_comparacao.pack(fill="y", expand=True)
        self.texto_comparacao.insert(tk.END, "A comparacao aparece aqui quando voce marcar duas ou mais RAs.\n")
        self.texto_comparacao.configure(state="disabled")

        coluna_direita = ttk.Frame(corpo)
        coluna_direita.pack(side="left", fill="both", expand=True)

        self.figura_comparacao = Figure(figsize=(6.8, 5.2), dpi=100)
        self.eixo_comparacao = self.figura_comparacao.add_subplot(111)
        self.tela_comparacao = FigureCanvasTkAgg(self.figura_comparacao, master=coluna_direita)
        self.tela_comparacao.get_tk_widget().pack(fill="both", expand=True)

    def _opcoes_ra(self) -> list[str]:
        """Return the RA options shown in the combobox."""
        codigos = sorted(self.dados["localidade"].dropna().astype(int).unique().tolist())
        return [rotulo_ra(codigo) for codigo in codigos]

    def _extrair_codigo_ra(self, rotulo: str) -> int | None:
        """Extract the numeric RA code from the displayed label."""
        if "(" in rotulo and rotulo.endswith(")"):
            try:
                return int(rotulo.rsplit("(", 1)[1].rstrip(")"))
            except ValueError:
                return None
        return None

    def _codigos_ra_selecionados(self) -> list[int]:
        """Translate the checked RA labels into numeric codes."""
        selecionados = [codigo for codigo, variavel in self.variaveis_ra.items() if variavel.get()]
        return sorted(selecionados)

    def alternar_painel_ra(self) -> None:
        """Show or hide the RA checkbox panel."""
        if self.painel_ra_visivel.get():
            self.painel_ra.pack_forget()
            self.painel_ra_visivel.set(False)
            self.botao_painel_ra.config(text="Mostrar selecao de RAs")
        else:
            self.painel_ra.pack(anchor="w", fill="both", expand=False, pady=(8, 0))
            self.painel_ra_visivel.set(True)
            self.botao_painel_ra.config(text="Ocultar selecao de RAs")

    def selecionar_todas_ras(self) -> None:
        """Select all RAs in the filter list."""
        for variavel in self.variaveis_ra.values():
            variavel.set(True)
        self._atualizar_status_ra()
        self.atualizar_visao()

    def limpar_selecao_ra(self) -> None:
        """Clear the RA filter selection."""
        for variavel in self.variaveis_ra.values():
            variavel.set(False)
        self._atualizar_status_ra()
        self.atualizar_visao()

    def _metrica_atual(self) -> str:
        """Return the selected metric column name."""
        return METRICAS[self.variavel_metrica.get()]

    def _agrupamento_atual(self) -> str:
        """Return the selected grouping mode."""
        return AGRUPAMENTOS[self.variavel_agrupamento.get()]

    def _dados_filtrados(self) -> pd.DataFrame:
        """Apply the RA filter chosen by the user."""
        quadro = self.dados.copy()
        codigos_ra = self._codigos_ra_selecionados()
        if codigos_ra:
            quadro = quadro[quadro["localidade"].isin(codigos_ra)]
        return quadro

    def _atualizar_status_ra(self) -> None:
        """Update the helper text that summarizes the RA filter."""
        selecionados = self._codigos_ra_selecionados()
        total = len(self.variaveis_ra)
        if not selecionados:
            texto = "Nenhuma RA marcada; a aba mostrara dados vazios."
        elif len(selecionados) == total:
            texto = "Todas as RAs estao selecionadas."
        else:
            texto = f"{len(selecionados)} de {total} RAs selecionadas."
        self.rotulo_status_ra.config(text=texto)

    def atualizar_visao(self) -> None:
        """Recompute the summary, table preview and chart."""
        self._atualizar_status_ra()
        self.dados_filtrados = self._dados_filtrados()
        coluna_metrica = self._metrica_atual()
        modo_agrupamento = self._agrupamento_atual()
        self.resumo_atual = montar_linhas_resumo(self.dados_filtrados, coluna_metrica, modo_agrupamento)
        self._atualizar_estatisticas(coluna_metrica)
        self._atualizar_texto_ranking(coluna_metrica)
        self._atualizar_grafico()
        self._atualizar_previa_tabela()

    def _atualizar_estatisticas(self, coluna_metrica: str) -> None:
        """Refresh the numeric indicators shown on the left side."""
        estatisticas = calcular_estatisticas_metrica(self.dados_filtrados, coluna_metrica)

        self.rotulo_total.config(text=f"Total selecionado: {estatisticas['total']:,}")
        self.rotulo_validos.config(text=f"Respostas validas: {estatisticas['valid_metric']:,}")
        self.rotulo_positivos.config(text=f"Casos positivos: {estatisticas['yes_count']:,}")
        self.rotulo_taxa.config(text=f"Taxa: {formatar_percentual(estatisticas['rate'])}")
        self.rotulo_idade.config(
            text=f"Idade media: {estatisticas['age_mean']:.1f} anos" if pd.notna(estatisticas["age_mean"]) else "Idade media: -"
        )
        self.rotulo_renda.config(
            text=f"Renda media valida: R$ {estatisticas['income_mean']:,.0f}"
            if pd.notna(estatisticas["income_mean"])
            else "Renda media valida: -"
        )

    def _atualizar_texto_ranking(self, coluna_metrica: str) -> None:
        """Write the grouped ranking as plain text."""
        self.texto_ranking.configure(state="normal")
        self.texto_ranking.delete("1.0", tk.END)

        titulo = f"Indicador: {self.variavel_metrica.get()}\nAgrupado por: {self.variavel_agrupamento.get()}\n\n"
        self.texto_ranking.insert(tk.END, titulo)
        codigos_ra = self._codigos_ra_selecionados()
        if codigos_ra:
            self.texto_ranking.insert(
                tk.END,
                "RAs filtradas: " + ", ".join(rotulo_ra(codigo) for codigo in codigos_ra) + "\n\n",
            )
        if not self.resumo_atual:
            self.texto_ranking.insert(tk.END, "Sem dados suficientes para exibir o ranking.\n")
            self.texto_ranking.configure(state="disabled")
            return

        for indice, item in enumerate(self.resumo_atual, start=1):
            grupo = item["grupo"]
            total = int(item["total"])
            positivos = int(item["positivo"])
            taxa = item["taxa"]
            self.texto_ranking.insert(
                tk.END,
                f"{indice:02d}. {grupo} | total={total:,} | positivos={positivos:,} | taxa={taxa * 100:.1f}%\n",
            )

        self.texto_ranking.configure(state="disabled")

    def _atualizar_grafico(self) -> None:
        """Draw the current summary as a bar chart."""
        self.eixo.clear()
        if not self.resumo_atual:
            self.eixo.set_title("Sem dados para exibir")
            self.tela_canvas.draw()
            return

        itens = self.resumo_atual
        rotulos = [str(item["grupo"]) for item in itens]
        taxas = [item["taxa"] * 100 for item in itens]
        cor = "#2a6f97" if self._metrica_atual() == "G05" else "#9c6644"
        if len(itens) > 14:
            self.eixo.barh(range(len(itens)), taxas, color=cor)
            self.eixo.set_xlim(0, 100)
            self.eixo.set_xlabel("Percentual de respostas positivas")
            self.eixo.set_yticks(range(len(itens)))
            self.eixo.set_yticklabels(rotulos)
            self.eixo.invert_yaxis()
            self.eixo.set_title(f"{self.variavel_metrica.get()} - todas as categorias")
            self.figura.set_size_inches(9.5, max(5.8, len(itens) * 0.32))
            self.eixo.grid(axis="x", alpha=0.25)
        else:
            self.eixo.bar(range(len(itens)), taxas, color=cor)
            self.eixo.set_ylim(0, 100)
            self.eixo.set_ylabel("Percentual de respostas positivas")
            self.eixo.set_title(f"{self.variavel_metrica.get()} - todas as categorias")
            self.eixo.set_xticks(range(len(itens)))
            self.eixo.set_xticklabels(rotulos, rotation=45, ha="right")
            self.eixo.grid(axis="y", alpha=0.25)
        self.figura.tight_layout()
        self.tela_canvas.draw()

    def _atualizar_previa_tabela(self) -> None:
        """Show a compact preview of the filtered records."""
        for item in self.arvore.get_children():
            self.arvore.delete(item)

        linhas_previa = montar_linhas_previa_tabela(self.dados_filtrados, limite=200)
        if not linhas_previa:
            return

        for linha in linhas_previa:
            self.arvore.insert("", tk.END, values=linha)

    def exportar_txt(self) -> None:
        """Export the current summary to a TXT file."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar relatorio em TXT",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt")],
        )
        if not caminho:
            return

        coluna_metrica = self._metrica_atual()
        codigos_ra = self._codigos_ra_selecionados()
        linhas = montar_linhas_relatorio(
            self.dados_filtrados,
            coluna_metrica,
            self.variavel_metrica.get(),
            self.variavel_agrupamento.get(),
            self.resumo_atual,
            codigos_ra,
        )

        with open(caminho, "w", encoding="utf-8") as arquivo:
            for linha in linhas:
                arquivo.write(linha + "\n")

        messagebox.showinfo("Exportacao concluida", f"Arquivo salvo em:\n{caminho}")

    def abrir_comparacao_ra(self) -> None:
        """Refresh the comparison panel for two or more selected RAs."""
        codigos_ra = self._codigos_ra_selecionados()
        if len(codigos_ra) < 2:
            messagebox.showinfo("Comparacao de RAs", "Marque pelo menos duas RAs para comparar.")
            self.caderno.select(self.aba_comparacao)
            self._atualizar_painel_comparacao([])
            return

        coluna_metrica = self._metrica_atual()
        linhas = montar_linhas_comparacao_ra(self.dados_filtrados, coluna_metrica, codigos_ra)
        if not linhas:
            messagebox.showinfo("Comparacao de RAs", "Nao ha dados validos para as RAs marcadas.")
            self.caderno.select(self.aba_comparacao)
            self._atualizar_painel_comparacao([])
            return

        self.caderno.select(self.aba_comparacao)
        self._atualizar_painel_comparacao(linhas)

    def _atualizar_painel_comparacao(self, linhas: list[dict]) -> None:
        """Render the comparison text and chart in the comparison tab."""
        self.texto_comparacao.configure(state="normal")
        self.texto_comparacao.delete("1.0", tk.END)
        self.texto_comparacao.insert(tk.END, "Resumo da comparacao\n\n")

        if not linhas:
            self.texto_comparacao.insert(tk.END, "Marque duas ou mais RAs e clique em 'Atualizar comparacao'.\n")
            self.texto_comparacao.configure(state="disabled")
            self.eixo_comparacao.clear()
            self.eixo_comparacao.set_title("Sem comparacao para exibir")
            self.tela_comparacao.draw()
            return

        for linha in linhas:
            media_idade = f"{linha['media_idade']:.1f}" if pd.notna(linha.get("media_idade")) else "-"
            media_renda = f"R$ {linha['media_renda']:,.0f}" if pd.notna(linha.get("media_renda")) else "-"
            self.texto_comparacao.insert(
                tk.END,
                f"{linha['nome_ra']}\n"
                f"  Total: {int(linha['total']):,}\n"
                f"  Positivos: {int(linha['positivo']):,}\n"
                f"  Taxa: {linha['taxa'] * 100:.1f}%\n"
                f"  Idade media: {media_idade}\n"
                f"  Renda media valida: {media_renda}\n\n",
            )
        self.texto_comparacao.configure(state="disabled")

        self.eixo_comparacao.clear()
        rotulos = [linha["nome_ra"] for linha in linhas]
        taxas = [linha["taxa"] * 100 for linha in linhas]
        if len(linhas) > 8:
            self.eixo_comparacao.barh(range(len(linhas)), taxas, color="#2a6f97")
            self.eixo_comparacao.set_yticks(range(len(linhas)))
            self.eixo_comparacao.set_yticklabels(rotulos)
            self.eixo_comparacao.set_xlim(0, 100)
            self.eixo_comparacao.invert_yaxis()
            self.eixo_comparacao.set_xlabel("Percentual de respostas positivas")
        else:
            self.eixo_comparacao.bar(range(len(linhas)), taxas, color="#2a6f97")
            self.eixo_comparacao.set_ylim(0, 100)
            self.eixo_comparacao.set_xticks(range(len(linhas)))
            self.eixo_comparacao.set_xticklabels(rotulos, rotation=35, ha="right")
            self.eixo_comparacao.set_ylabel("Percentual de respostas positivas")
        self.eixo_comparacao.set_title(f"Comparacao de {self.variavel_metrica.get()}")
        self.eixo_comparacao.grid(axis="y" if len(linhas) <= 8 else "x", alpha=0.25)
        self.figura_comparacao.tight_layout()
        self.tela_comparacao.draw()

    def exportar_csv(self) -> None:
        """Export the current filtered rows to a CSV file."""
        caminho = filedialog.asksaveasfilename(
            title="Salvar dados filtrados em CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
        )
        if not caminho:
            return

        previa = self.dados_filtrados.copy()
        previa = previa.loc[:, [coluna for coluna in COLUNAS_EXIBICAO if coluna in previa.columns]]
        previa.to_csv(caminho, index=False, encoding="utf-8-sig")
        messagebox.showinfo("Exportacao concluida", f"Arquivo salvo em:\n{caminho}")


def principal() -> None:
    """Start the application."""
    try:
        root = tk.Tk()
        AplicativoRecorteC(root)
        root.mainloop()
    except Exception as exc:
        messagebox.showerror("Erro ao iniciar", str(exc))
        raise


if __name__ == "__main__":
    principal()
