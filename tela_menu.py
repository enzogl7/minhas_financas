# tela_menu.py
# classe da tela principal (menu)

import tkinter as tk
from tkinter import ttk
import data_manager

class TelaMenu(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # cabeçalho com nome do app
        header = ttk.Frame(self)
        header.pack(fill="x", pady=(6, 12))
        title = ttk.Label(header, text="💰 Minhas Finanças", style="Header.TLabel", anchor="center")
        title.pack()

        # resumo financeiro com o quanto o usuário tem de receitas, despesas e saldo
        resumo_frame = ttk.Frame(self, padding=12)
        resumo_frame.pack(fill="x", pady=(0, 12))

        self.lbl_receitas = ttk.Label(resumo_frame, text="Receitas: R$ 0.00", style="Small.TLabel")
        self.lbl_receitas.grid(row=0, column=0, sticky="w", padx=6)
        self.lbl_despesas = ttk.Label(resumo_frame, text="Despesas: R$ 0.00", style="Small.TLabel")
        self.lbl_despesas.grid(row=0, column=1, sticky="w", padx=6)
        self.lbl_saldo = ttk.Label(resumo_frame, text="Saldo: R$ 0.00", style="Small.TLabel")
        self.lbl_saldo.grid(row=0, column=2, sticky="w", padx=6)

        # botoes de menu principais que levam para outras telas
        buttons = ttk.Frame(self)
        buttons.pack(pady=20)

        ttk.Button(buttons, text="➕ Adicionar Transação", width=25, command=lambda: controller.mostrar_tela("TelaCadastro")).grid(row=0, column=0, pady=6)
        ttk.Button(buttons, text="Ver/Editar Transações", width=25, command=lambda: controller.mostrar_tela("TelaLista")).grid(row=1, column=0, pady=6)
        ttk.Button(buttons, text="📊 Análise Financeira", width=25, command=lambda: controller.mostrar_tela("TelaAnalise")).grid(row=2, column=0, pady=6)
        ttk.Button(buttons, text="Sair", width=25, command=controller.destroy).grid(row=3, column=0, pady=6)

    def atualizar_resumo(self):
        # busca os dados de receitas, despesas e saldo no csv para atualizar as labels do resumo financeiro
        try:
            total_receitas, total_despesas, saldo = data_manager.get_resumo()
            
            self.lbl_receitas.config(text=f"Receitas: R$ {total_receitas:,.2f}")
            self.lbl_despesas.config(text=f"Despesas: R$ {total_despesas:,.2f}")
            
            color = "green" if saldo >= 0 else "red"
            self.lbl_saldo.config(text=f"Saldo: R$ {saldo:,.2f}", foreground=color)
            
        except:
            # se der erro no csv:
            self.lbl_saldo.config(text="Erro ao ler dados", foreground="red")