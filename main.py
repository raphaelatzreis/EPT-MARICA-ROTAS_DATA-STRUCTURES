# main.py
import matplotlib.pyplot as plt

# Imports conforme o seu projeto (ajuste o nome das pastas se necessário)
from regras_e_logica.grafo import Grafo
from regras_e_logica.roteador import Roteador
from ui_interface_usuario.interface import InterfaceEPT

def main():
    # 1. Cria os dados
    meu_grafo = Grafo()
    
    # 2. Cria o processador (injetando os dados)
    meu_roteador = Roteador(meu_grafo)
    
    # 3. Cria a interface (injetando o processador)
    app = InterfaceEPT(meu_roteador)
    
    # 4. Inicia a janela
    app.iniciar()

if __name__ == "__main__":
    main()