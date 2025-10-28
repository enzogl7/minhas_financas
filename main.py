# main.py
# arquivo de execução da aplicação, chamando outras classes principais

from app import App
from data_manager import garantir_csv

if __name__ == "__main__":
    # garante que o csv exista ou esteja no formato correto de leitura antes de rodar a aplicação
    garantir_csv() 
    
    # executa o app
    app = App()
    app.mainloop()