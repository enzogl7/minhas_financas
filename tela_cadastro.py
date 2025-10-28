# tela_cadastro.py
# classe da tela de cadastro

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
from datetime import date
import data_manager

class TelaCadastro(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Adicionar Transação", style="Header.TLabel").pack(pady=10)

        form = ttk.Frame(self, padding=10)
        form.pack(fill="x")

        # tipo de cadastro (receita ou despesa)
        ttk.Label(form, text="Tipo:").grid(row=0, column=0, sticky="w")
        self.tipo = tk.StringVar(value="Despesa")
        tipo_frame = ttk.Frame(form)
        tipo_frame.grid(row=0, column=1, sticky="w", pady=4)
        ttk.Radiobutton(tipo_frame, text="Despesa", variable=self.tipo, value="Despesa").pack(side="left", padx=(0,8))
        ttk.Radiobutton(tipo_frame, text="Receita", variable=self.tipo, value="Receita").pack(side="left")

        # categoria
        ttk.Label(form, text="Categoria:").grid(row=1, column=0, sticky="w", pady=(8,0))
        self.categoria = ttk.Combobox(form, values=["Alimentação", "Transporte", "Lazer", "Moradia", "Outros"], state="readonly")
        self.categoria.grid(row=1, column=1, sticky="ew", pady=(8,0))

        # descrição
        ttk.Label(form, text="Descrição:").grid(row=2, column=0, sticky="w", pady=(8,0))
        self.descricao = ttk.Entry(form)
        self.descricao.grid(row=2, column=1, sticky="ew", pady=(8,0))

        # valor
        ttk.Label(form, text="Valor (R$):").grid(row=3, column=0, sticky="w", pady=(8,0))
        self.valor = ttk.Entry(form)
        self.valor.grid(row=3, column=1, sticky="ew", pady=(8,0))

        # data com seletor de data em calendário
        ttk.Label(form, text="Data:").grid(row=4, column=0, sticky="w", pady=(8,0))
        self.data_entry = ttk.DateEntry(form, dateformat="%d/%m/%Y")
        self.data_entry.grid(row=4, column=1, sticky="ew", pady=(8,0))
        
        form.columnconfigure(1, weight=1)

        # botões de ação (voltar e salvar)
        btns = ttk.Frame(self)
        btns.pack(pady=12)
        ttk.Button(btns, text="Salvar", command=self.salvar).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Voltar", command=lambda: controller.mostrar_tela("TelaMenu")).grid(row=0, column=1, padx=6)
        
        # faz com que seja possível salvar apertando enter
        self.bind_all("<Return>", self._on_enter)

    def _on_enter(self, event):
        widget = self.focus_get()
        if isinstance(widget, ttk.Entry) or isinstance(widget, tk.Entry):
            self.salvar()

    def salvar(self):
        # salva a transação pegando os dados inseridos e enviando para o csv
        try:
            data_str = self.data_entry.entry.get() 
            
            data_manager.salvar_transacao(
                tipo=self.tipo.get(),
                categoria=self.categoria.get(),
                descricao=self.descricao.get(),
                valor_str=self.valor.get(),
                data_str=data_str
            )
            
            messagebox.showinfo("Sucesso", "Transação salva com sucesso!")
            self._limpar_campos()
            self.controller.mostrar_tela("TelaMenu")

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except:
            messagebox.showerror("Erro", "Ocorreu um erro inesperado.")

    def _limpar_campos(self):
        # após salvar, limpa os campos para caso o usuário queira cadastrar outra transação
        self.descricao.delete(0, tk.END)
        self.valor.delete(0, tk.END)
        
        # limpa o seletor de data por calendário
        self.data_entry.entry.delete(0, tk.END)
        self.data_entry.entry.insert(0, date.today().strftime("%d/%m/%Y"))
        
        self.categoria.set('')
        self.tipo.set('Despesa')