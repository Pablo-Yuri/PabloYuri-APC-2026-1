import tkinter as tk
from tkinter import filedialog, messagebox
from utils.carregar_dados import COLUNAS_EXIBICAO

def salvar_relatorio_txt(texto_relatorio: str):
    """Abre janela para o utilizador guardar o relatório num .txt."""
    if not texto_relatorio:
        messagebox.showwarning("Aviso", "Não há dados para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        title="Salvar Relatório TXT", defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")]
    )
    if caminho:
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(texto_relatorio)
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{caminho}")
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível salvar:\n{erro}")

def exportar_tabela_csv(df) -> None:
    """Exporta as linhas filtradas atuais para um ficheiro CSV."""
    caminho = filedialog.asksaveasfilename(
        title="Salvar dados filtrados em CSV", defaultextension=".csv", filetypes=[("CSV", "*.csv")]
    )
    if not caminho:
        return
    
    previa = df.copy()
    colunas_presentes = [coluna for coluna in COLUNAS_EXIBICAO if coluna in previa.columns]
    previa = previa.loc[:, colunas_presentes]
    
    nomes_exibicao = {
        "A01uf": "UF", "localidade": "Localidade / RA", "morador_id": "ID Morador",
        "idade_calculada": "Idade", "G01": "Atendimento? (12m)", "G02": "Tipo Consulta",
        "G03": "Emergência?", "G04": "Local", "G05": "Tem Plano?", "G06": "Filhos?",
        "G06_1": "Qtd Filhos", "G06_2": "Idade 1º Filho", "renda_ind": "Renda Ind."
    }
    
    previa.rename(columns=nomes_exibicao, inplace=True)
    previa.to_csv(caminho, index=False, encoding="utf-8-sig")
    messagebox.showinfo("Sucesso", f"Arquivo CSV guardado em:\n{caminho}")