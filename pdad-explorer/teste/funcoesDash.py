import tkinter as tk
from tkinter import ttk
import pandas as pd


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