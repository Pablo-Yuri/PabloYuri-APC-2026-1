import tkinter as tk
from tkinter import filedialog, messagebox

from carregar_dados import COLUNAS_EXIBICAO


def salvar_relatorio_txt(texto_relatorio: str):
    """
    Recebe uma string com o texto do relatório e abre a janela 
    para o usuário escolher onde salvar o arquivo .txt.
    """
    if not texto_relatorio:
        messagebox.showwarning("Aviso", "Não há dados para exportar.")
        return

    caminho = filedialog.asksaveasfilename(
        title="Salvar Relatório TXT",
        defaultextension=".txt",
        filetypes=[("Arquivo de Texto", "*.txt")]
    )
    
    if caminho:
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("RELATÓRIO DESCRITIVO PDAD 2024\n")
                arquivo.write("=" * 40 + "\n\n")
                arquivo.write(texto_relatorio)
            messagebox.showinfo("Sucesso", f"Relatório salvo em:\n{caminho}")
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível salvar o arquivo:\n{erro}")
            
            
def exportar_tabela_csv(df) -> None:
    """Export the current filtered rows to a CSV file with renamed columns."""
    caminho = filedialog.asksaveasfilename(
        title="Salvar dados filtrados em CSV",
        defaultextension=".csv",
        filetypes=[("CSV", "*.csv")],
    )
    if not caminho:
        return
    
    # 1. Faz uma cópia para NÃO alterar os dados do painel original
    previa = df.copy()
    
    # 2. Filtra as colunas desejadas PRIMEIRO (usando os nomes originais)
    colunas_presentes = [coluna for coluna in COLUNAS_EXIBICAO if coluna in previa.columns]
    previa = previa.loc[:, colunas_presentes]
    
    # 3. Dicionário de tradução
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
    
    # 4. Renomeia as colunas de uma vez só no DataFrame da exportação
    previa.rename(columns=nomes_exibicao, inplace=True)
    
    # 5. Imprime e Exporta
    print(previa.head(5))
    previa.to_csv(caminho, index=False, encoding="utf-8-sig")
    print(f"Exportação concluída: {caminho}")
    messagebox.showinfo("Exportação concluída", f"Arquivo salvo em:\n{caminho}")