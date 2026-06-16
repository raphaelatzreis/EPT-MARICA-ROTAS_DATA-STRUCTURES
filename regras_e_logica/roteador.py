# roteador.py
import heapq

class Roteador:
    def __init__(self, grafo_obj):
        # COMENTÁRIO OO: Injeção de dependência. O roteador "conhece" o grafo.
        self.grafo_obj = grafo_obj
        # COMENTÁRIO OO: A variável global 'linhas_desativadas' virou atributo
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
            
            # Pega as conexões diretamente do objeto grafo
            vizinhos = self.grafo_obj.dados.get(atual, {})
            for vizinho, dados in vizinhos.items():
                linha = dados["linha"]
                
                # Respeita o estado das linhas dentro do próprio objeto
                if linha in self.linhas_desativadas:
                    continue
                    
                tempo_aresta = dados["tempo"]
                heapq.heappush(fila, (tempo + tempo_aresta, vizinho, caminho + [vizinho], linhas + [linha]))
                
        return None, [], []

    # COMENTÁRIO OO: Método para lidar com a ativação/desativação
    def alternar_linha(self, linha):
        if linha in self.linhas_desativadas:
            self.linhas_desativadas.remove(linha)
            return True # Retorna True indicando que foi ativada
        else:
            self.linhas_desativadas.add(linha)
            return False # Retorna False indicando que foi desativada