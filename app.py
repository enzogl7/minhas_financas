# app.py

import tkinter as tk
import ttkbootstrap as ttk

from tela_menu import TelaMenu
from tela_cadastro import TelaCadastro
from tela_analise import TelaAnalise
from tela_lista import TelaLista

class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="flatly") 
        self.title("Minhas Finanças")
        self.geometry("720x520")
        self.resizable(False, False)

        # estilização com ttkbootstrap
        style = ttk.Style() 
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("TLabel") 
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("Small.TLabel", font=("Segoe UI", 10))

        # criação do container
        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=12, pady=12)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        
        # cria os frames dentro do container
        for F in (TelaMenu, TelaCadastro, TelaAnalise, TelaLista): 
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.mostrar_tela("TelaMenu")

    def mostrar_tela(self, nome_tela_str):
        # traz a tela solicitada pra frente
        frame = self.frames[nome_tela_str]
        
        # se for de volta pro menu, atualiza o resumo financeiro
        if isinstance(frame, TelaMenu):
            frame.atualizar_resumo()
            
        # se for pra tela de listagem, recarrega os dados atualizados
        if isinstance(frame, TelaLista):
            frame.carregar_dados() 
            
        frame.tkraise()