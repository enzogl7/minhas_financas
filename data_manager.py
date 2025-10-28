# data_manager.py
# lógicas de leitura e escritas de dados em csv

import os
import csv
import pandas as pd
from datetime import datetime
from config import CSV_FILE, CSV_HEADER

def garantir_csv():
    # garante que o csv tenha o cabeçalho correto e exista para leitura que o código faz
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(CSV_HEADER)

def salvar_transacao(tipo, categoria, descricao, valor_str, data_str):
    # salva novos registros no arquivo csv
    if not (categoria and descricao and valor_str and data_str):
        raise ValueError("Preencha todos os campos!")

    # trata o valor para preço numérico
    try:
        valor_clean = float(valor_str.replace(",", "."))
    except:
        raise ValueError("O valor deve ser numérico! Use ponto ou vírgula.")
        
    # trata a data para formato correto
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
    except:
        raise ValueError("Data deve estar no formato DD/MM/AAAA.")

    # por fim salva no csv
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([tipo, categoria, descricao, valor_clean, data_str])

def get_resumo():
    # lê o csv e retorna os valores de receitas, despesas e saldo
    try:
        df = pd.read_csv(CSV_FILE, names=CSV_HEADER, skiprows=1)
        if df.empty:
            return 0.0, 0.0, 0.0
            
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0)
        total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
        saldo = total_receitas - total_despesas
        return total_receitas, total_despesas, saldo
        
    except:
        return 0.0, 0.0, 0.0

def get_dados_grafico_despesas():
    # gráfico de despesas por categoria feito pelo panda em formato de pizza
    try:
        df = pd.read_csv(CSV_FILE, names=CSV_HEADER, skiprows=1)
        despesas = df[df["Tipo"] == "Despesa"].copy()
        if despesas.empty:
            return None
        despesas["Valor"] = pd.to_numeric(despesas["Valor"], errors="coerce").fillna(0.0)
        por_cat = despesas.groupby("Categoria")["Valor"].sum()
        return por_cat
    except:
        return None

def get_dados_grafico_saldo():
    # grafico em barra de receitas x despesas
    try:
        df = pd.read_csv(CSV_FILE, names=CSV_HEADER, skiprows=1)
        df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce").fillna(0.0)
        total_receitas = df[df["Tipo"] == "Receita"]["Valor"].sum()
        total_despesas = df[df["Tipo"] == "Despesa"]["Valor"].sum()
        return total_receitas, total_despesas
    except:
        return 0.0, 0.0

# -- funções responsáveis pela listagem, exclusão e edição de transações existentes
def get_todas_transacoes():
    # lê todo o csv e devolve todas as transações criadas
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader) 
            dados = list(reader)
            return dados
    except FileNotFoundError:
        return [] # retorna sem nada se nao encontrar o arquivo csv
    except Exception as e:
        print(f"Erro ao ler CSV: {e}")
        return []

def _reescrever_csv_completo(dados_com_cabecalho):
    # reescreve o csv caso tenha alguma alteração p/ exibir tudo atualizado
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(dados_com_cabecalho)
    except Exception as e:
        raise Exception(f"Erro ao reescrever o arquivo CSV: {e}")

def editar_transacao_por_linha(index_alvo, novos_dados):
    # edita uma transação específica

    # le o arquivo todo
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        todas_as_linhas = list(reader)
        
    # pega os dados separadamente
    cabecalho = todas_as_linhas[0]
    dados = todas_as_linhas[1:]

    # modifica a linha selecionada
    if 0 <= index_alvo < len(dados):
        try:
            float(novos_dados[3].replace(",", "."))
        except ValueError:
            raise ValueError("Valor inválido. Use apenas números.")
        dados[index_alvo] = novos_dados
    else:
        raise IndexError("Índice da transação não encontrado.")
        
    # reescreve as informações no csv e salva
    novos_dados_completos = [cabecalho] + dados
    _reescrever_csv_completo(novos_dados_completos)

def excluir_transacao_por_linha(index_alvo):
    # exclui uma transação especifica seguindo a memsa lógica da função de editar

    # le todo o arquivo
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        todas_as_linhas = list(reader)
        
    cabecalho = todas_as_linhas[0]
    dados = todas_as_linhas[1:]
    
    # remove a linha selecionada usando o pop
    if 0 <= index_alvo < len(dados):
        dados.pop(index_alvo)
    else:
        raise IndexError("Índice da transação não encontrado.")
        
    # reescreve todo o arquivo com as informações atualizadas
    novos_dados_completos = [cabecalho] + dados
    _reescrever_csv_completo(novos_dados_completos)