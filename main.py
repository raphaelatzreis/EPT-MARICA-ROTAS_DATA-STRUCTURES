import matplotlib.pyplot as plt

from regras_e_logica.grafo import Grafo  
from regras_e_logica.roteador import Roteador  
from ui_interface_usuario.interface import InterfaceEPT  


def main():
    meu_grafo = Grafo()  
    
    meu_roteador = Roteador(meu_grafo)  
    
    app = InterfaceEPT(meu_roteador)  
    
    app.iniciar()  

if __name__ == "__main__":
    main()  
