# tela_analise.py
# classe da tela de gráficos

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data_manager

class TelaAnalise(ttk.Frame):
    # exibe o menu de seleção de gráficos a serem exibidos + botão de voltar
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Análise Financeira", style="Header.TLabel").pack(pady=10)

        controls = ttk.Frame(self)
        controls.pack(fill="x", padx=12)

        ttk.Button(controls, text="Despesas por Categoria", command=self.grafico_despesas).grid(row=0, column=0, padx=6, pady=6)
        ttk.Button(controls, text="Receitas x Despesas", command=self.grafico_saldo).grid(row=0, column=1, padx=6, pady=6)
        ttk.Button(controls, text="Voltar", command=lambda: controller.mostrar_tela("TelaMenu")).grid(row=0, column=2, padx=6, pady=6)

        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.pack(fill="both", expand=True, padx=12, pady=8)

        self.current_canvas = None
        self.current_fig = None

    # limpa o espaço do gráfico anterior para exibir o novo
    def _limpar_canvas(self):
        # se existir um canvas, limpa ele para que exiba o novo
        if self.current_canvas:
            self.current_canvas.get_tk_widget().destroy()
            plt.close(self.current_fig)
            self.current_canvas = None
            self.current_fig = None

    # cria o gráfico de pizza de despesas por categoria
    def grafico_despesas(self):
        self._limpar_canvas()
        por_cat = data_manager.get_dados_grafico_despesas()
        if por_cat is None or por_cat.empty:
            messagebox.showinfo("Aviso", "Nenhuma despesa registrada!")
            return

        fig, ax = plt.subplots(figsize=(5,4))
        por_cat.plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
        ax.set_title("Despesas por Categoria")
        fig.tight_layout()

        self._desenhar_grafico(fig)

    # cria o gráfico de receita x despesas em barra
    def grafico_saldo(self):
        self._limpar_canvas()
        total_receitas, total_despesas = data_manager.get_dados_grafico_saldo()

        fig, ax = plt.subplots(figsize=(5,4))
        ax.bar(["Receitas", "Despesas"], [total_receitas, total_despesas], color=["#4CAF50", "#F44336"])
        ax.set_ylabel("Valor (R$)")
        ax.set_title("Receitas x Despesas")
        for i, v in enumerate([total_receitas, total_despesas]):
            ax.text(i, v + max(1.0, v*0.01), f"R$ {v:,.2f}", ha="center")
        fig.tight_layout()

        self._desenhar_grafico(fig)

    def _desenhar_grafico(self, fig):
        # função para desenhar o gráfico com o matplotlib + tkinter
        self.current_fig = fig
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.current_canvas = canvas