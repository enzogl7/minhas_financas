# **Minhas Finanças**

Aplicação desenvolvida em Python utilizando Tkinter para auxiliar no controle e na análise de finanças pessoais.

Este projeto foi criado como trabalho final da disciplina **Desenvolvimento Rápido de Aplicações em Python - ARA0095**. O objetivo principal é integrar conceitos de interfaces gráficas, persistência de dados e visualização de informações, oferecendo ao usuário uma forma simples de registrar e acompanhar suas movimentações financeiras.

---

## **Funcionalidades**

### Registro de transações

* Cadastro de despesas e receitas
* Campos: tipo, categoria, descrição, valor e data
* Validação dos dados antes do envio

### Visualização e edição

* Exibição de todas as transações em formato de tabela
* Possibilidade de editar ou excluir registros
* Atualização automática das informações

### Análise financeira

* Gráfico de pizza exibindo despesas por categoria
* Gráfico de barras comparando receitas e despesas
* Geração automática dos gráficos a partir do CSV

### Resumo geral

* Total de receitas
* Total de despesas
* Saldo atual do usuário

---

## **Tecnologias Utilizadas**

* Python 3
* Tkinter (interface gráfica)
* CSV para armazenamento de dados
* Matplotlib para geração de gráficos
* Módulos auxiliares: `os`, `datetime`

---

## **Como executar o projeto**

1. Clone este repositório:

   ```bash
   git clone https://github.com/enzogl7/minhas-financas.git
   ```

2. Certifique-se de ter o Python 3 instalado.

3. Instale a dependência necessária:

   ```bash
   pip install matplotlib
   ```

4. Execute o arquivo principal:

   ```bash
   python main.py
   ```

O arquivo `transacoes.csv` será criado automaticamente quando a primeira transação for registrada.

---

## **Estrutura do Projeto**

```
minhas-financas/
│
├── main.py               # Arquivo principal da aplicação
├── transacoes.csv        # Arquivo criado automaticamente com os registros
└── README.md             # Documentação do projeto
```

---

## **Melhorias Futuras**

* Implementação de sistema de login
* Filtros por data e categoria na visualização das transações
* Cadastro de categorias personalizadas
* Substituir o arquivo CSV por um banco de dados
* Exportação de relatórios em PDF

---

## **Autor**

**Enzo Oliveira Galdino Lima**
Projeto desenvolvido como parte da disciplina *Desenvolvimento Rápido de Aplicações em Python* – Universidade Estácio de Sá.