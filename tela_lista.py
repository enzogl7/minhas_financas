# tela_lista.py
# tela para listar, editar e excluir transações.

import ttkbootstrap as ttk
from tkinter import messagebox
import data_manager
import csv
from config import CSV_FILE, CSV_HEADER

# tela popup de edição
class JanelaEdicao(ttk.Toplevel):
    def __init__(self, parent, controller, transacao_original, linha_index):
        super().__init__(parent)
        self.title("Editar Transação")
        self.geometry("350x300")
        
        self.controller = controller
        self.transacao_original = transacao_original
        self.linha_index = linha_index
        
        # campos do formulario (similar a tela de cadastro usando ttk)
        form = ttk.Frame(self, padding=10)
        form.pack(fill="x", expand=True)

        # tipo
        ttk.Label(form, text="Tipo:").grid(row=0, column=0, sticky="w")
        self.tipo = ttk.StringVar(value=transacao_original[0]) # preenche com o valor atual
        tipo_frame = ttk.Frame(form)
        tipo_frame.grid(row=0, column=1, sticky="w", pady=4)
        ttk.Radiobutton(tipo_frame, text="Despesa", variable=self.tipo, value="Despesa").pack(side="left")
        ttk.Radiobutton(tipo_frame, text="Receita", variable=self.tipo, value="Receita").pack(side="left")

        # categoria
        ttk.Label(form, text="Categoria:").grid(row=1, column=0, sticky="w", pady=4)
        self.categoria = ttk.Combobox(form, values=["Alimentação", "Transporte", "Lazer", "Moradia", "Outros"], state="readonly")
        self.categoria.grid(row=1, column=1, sticky="ew", pady=4)
        self.categoria.set(transacao_original[1]) # preenche com o valor atual

        # descricao
        ttk.Label(form, text="Descrição:").grid(row=2, column=0, sticky="w", pady=4)
        self.descricao = ttk.Entry(form)
        self.descricao.grid(row=2, column=1, sticky="ew", pady=4)
        self.descricao.insert(0, transacao_original[2]) # preenche com o valor atual

        # valor
        ttk.Label(form, text="Valor (R$):").grid(row=3, column=0, sticky="w", pady=4)
        self.valor = ttk.Entry(form)
        self.valor.grid(row=3, column=1, sticky="ew", pady=4)
        self.valor.insert(0, transacao_original[3]) # preenche com o valor atual

        # data
        ttk.Label(form, text="Data:").grid(row=4, column=0, sticky="w", pady=4)
        self.data_entry = ttk.DateEntry(form, dateformat="%d/%m/%Y")
        self.data_entry.entry.delete(0, "end")
        self.data_entry.entry.insert(0, transacao_original[4]) # preenche com o valor atual
        self.data_entry.grid(row=4, column=1, sticky="ew", pady=4)

        form.columnconfigure(1, weight=1)

        #  botoa de salvar edição
        btn_salvar = ttk.Button(self, text="Salvar Alterações", command=self.salvar_edicao, bootstyle="success")
        btn_salvar.pack(pady=10)
    
    def salvar_edicao(self):
        # pega tudo que foi inserido nos campos
        dados_novos = [
            self.tipo.get(),
            self.categoria.get(),
            self.descricao.get(),
            self.valor.get(),
            self.data_entry.entry.get()
        ]
        
        # bloco de try catch para tentar salvar a edição
        try:
            # chama a função lá no data_manager
            data_manager.editar_transacao_por_linha(self.linha_index, dados_novos)
            messagebox.showinfo("Sucesso", "Transação atualizada!", parent=self)
            
            # fecha a janela e recarrega a listaa para manter as informações atualizadas
            self.destroy() 
            self.controller.mostrar_tela("TelaLista")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}", parent=self)


# tela de listagem principal
class TelaLista(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # titulo
        ttk.Label(self, text="Todas as Transações", style="Header.TLabel").pack(pady=10)

        # botões de ação em cima da tabela
        action_frame = ttk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(action_frame, text="Recarregar", command=self.carregar_dados, bootstyle="info-outline").pack(side="left", padx=5)
        ttk.Button(action_frame, text="Editar Selecionado", command=self.editar_item, bootstyle="info").pack(side="left", padx=5)
        ttk.Button(action_frame, text="Excluir Selecionado", command=self.excluir_item, bootstyle="danger").pack(side="left", padx=5)
        
        # frame da tabela
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # criação da tabela
        colunas = CSV_HEADER
        self.tree = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=15)
        
        # colunas
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="w")
        
        # barra de rolagem do ttk
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # botão de voltar
        ttk.Button(self, text="Voltar ao Menu", command=lambda: controller.mostrar_tela("TelaMenu")).pack(pady=10)

    def carregar_dados(self):
        # função responsável por ler os dados do csv e então popular a tabela
        
        # limpa a tabela caso tenha algo
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        #  lê todo o csv e insere todos os dados encontrados dentro da tabela
        try:
            transacoes = data_manager.get_todas_transacoes()
            for index, linha in enumerate(transacoes):
                if index == 0 and linha == CSV_HEADER:
                    continue
                self.tree.insert("", "end", iid=index, values=linha)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar os dados: {e}")

    def editar_item(self):
        # função responsável por abrir a janela de edição com o item selecionado
        
        # pega o item selecionado e trata caso nao tenha nenhum selecionado
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um item para editar.")
            return

        # pega os dados do item selecionado e abre a janela
        linha_index = int(item_selecionado)
        dados_da_linha = self.tree.item(item_selecionado)["values"]
        JanelaEdicao(self, self.controller, dados_da_linha, linha_index)

    def excluir_item(self):
        # função responsável por excluir o item selecionado
        
        # pega o item selecionado e trata caso nao tenha nenhum selecionado
        item_selecionado = self.tree.focus()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione um item para excluir.")
            return
            
        # confirmação de exclusão para evitar acidentes
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta transação? Esta ação não pode ser desfeita."):
            return
            
        # pega os dados do item selecionado e tenta excluir chamando a função do data_manager, se der errado aparece a mensagem de erro
        linha_index = int(item_selecionado)
        try:
            data_manager.excluir_transacao_por_linha(linha_index)
            messagebox.showinfo("Sucesso", "Transação excluída.")
            self.carregar_dados()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível excluir: {e}")