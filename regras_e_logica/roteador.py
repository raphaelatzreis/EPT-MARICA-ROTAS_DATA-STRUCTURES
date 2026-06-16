import heapq

class Roteador:
    def __init__(self, grafo_obj):
        self.grafo_obj = grafo_obj  
        self.linhas_desativadas = set()  

    def calcular_caminho(self, inicio, fim):
        fila = [(0, inicio, [inicio], [])]  
        visitados = {}  
        
        while fila:
            tempo, atual, caminho, linhas = heapq.heappop(fila)  
            
            if atual == fim:
                return tempo, caminho, list(linhas)  
                
            if atual in visitados and visitados[atual] <= tempo:  
                continue
            visitados[atual] = tempo  
            
            vizinhos = self.grafo_obj.dados.get(atual, {})  
            for vizinho, opcoes in vizinhos.items():
                for opcao in opcoes:
                    linha = opcao["linha"]
                    
                    if linha in self.linhas_desativadas:  
                        continue
                        
                    tempo_aresta = opcao["tempo"]
                    heapq.heappush(fila, (tempo + tempo_aresta, vizinho, caminho + [vizinho], linhas + [linha]))  
                    
        return None, [], []


    def alternar_linha(self, linha):
        if linha in self.linhas_desativadas:
            self.linhas_desativadas.remove(linha)
            return True
        else:
            self.linhas_desativadas.add(linha)
            return False
