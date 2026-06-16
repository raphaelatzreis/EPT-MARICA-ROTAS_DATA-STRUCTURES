class Grafo:
    def __init__(self):
        self.dados = {
            "Maricá": {
                "Flamengo": [
                    {"tempo": 10, "linha": "30"},
                    {"tempo": 10, "linha": "30E"},
                    {"tempo": 10, "linha": "16"},
                    {"tempo": 10, "linha": "24"},
                ],
                "Avenida": [
                    {"tempo": 23, "linha": "30A"},
                    {"tempo": 20, "linha": "24A"},
                ]
            },
            
            "Flamengo": {
                "Maricá": [
                    {"tempo": 10, "linha": "30"},
                    {"tempo": 10, "linha": "30E"},
                    {"tempo": 10, "linha": "16"},
                    {"tempo": 20, "linha": "24"},
                ],
                "Parque Nanci": [
                    {"tempo": 20, "linha": "30"},
                    {"tempo": 15, "linha": "30E"},
                    {"tempo": 20, "linha": "16"},
                    {"tempo": 20, "linha": "24"},
                ]
            },
            
            "Avenida": {
                "Maricá": [
                    {"tempo": 23, "linha": "30A"},
                    {"tempo": 20, "linha": "24A"},
                ],
                "Parque Nanci": [
                    {"tempo": 15, "linha": "30A"},
                    {"tempo": 15, "linha": "24A"},
                ]
            },
            
            "Parque Nanci": {
                "Flamengo": [
                    {"tempo": 20, "linha": "30"},
                    {"tempo": 15, "linha": "30E"},
                    {"tempo": 20, "linha": "16"},
                    {"tempo": 5, "linha": "24"},
                ],
                "Avenida": [
                    {"tempo": 15, "linha": "30A"},
                    {"tempo": 5, "linha": "24A"},
                ],
                "São José": [
                    {"tempo": 10, "linha": "30"},
                    {"tempo": 10, "linha": "30A"},
                    {"tempo": 2, "linha": "16"},
                    {"tempo": 5, "linha": "24A"},
                    {"tempo": 5, "linha": "24"},
                ],
                "Inoã": [
                    {"tempo": 10, "linha": "30E"}
                ]
            },
            
            "São José": {
                "Parque Nanci": [
                    {"tempo": 10, "linha": "30"},
                    {"tempo": 10, "linha": "30A"},
                    {"tempo": 2, "linha": "16"},
                    {"tempo": 5, "linha": "24A"},
                    {"tempo": 5, "linha": "24"},
                ],
                "Inoã": [
                    {"tempo": 5, "linha": "30"},
                    {"tempo": 5, "linha": "30A"},
                    {"tempo": 5, "linha": "24A"},
                    {"tempo": 5, "linha": "24"},
                ]
            },
            
            "Inoã": {
                "Parque Nanci": [
                    {"tempo": 10, "linha": "30E"}
                ],
                "São José": [
                    {"tempo": 5, "linha": "24"},
                    {"tempo": 5, "linha": "24"},
                    {"tempo": 5, "linha": "30"},
                    {"tempo": 5, "linha": "30A"}
                ],
                "Itaipuaçu": [
                    {"tempo": 15, "linha": "30"},
                    {"tempo": 15, "linha": "30A"},
                    {"tempo": 10, "linha": "30E"}
                ],
                "Recanto": [
                    {"tempo": 15, "linha": "21"}
                ]
            },
            
            "Itaipuaçu": {
                "Inoã": [
                    {"tempo": 15, "linha": "30"},
                    {"tempo": 15, "linha": "30A"},
                    {"tempo": 10, "linha": "30E"}
                ],
                "Recanto": [
                    {"tempo": 5, "linha": "30"},
                    {"tempo": 5, "linha": "30A"},
                    {"tempo": 2, "linha": "30E"}
                ]
            },
            
            "Recanto": {
                "Itaipuaçu": [
                    {"tempo": 5, "linha": "30"},
                    {"tempo": 5, "linha": "30A"},
                    {"tempo": 2, "linha": "30E"}
                ],
                "Inoã": [
                    {"tempo": 15, "linha": "21"}
                ]
            }
        }

    def obter_todas_linhas(self):
        linhas = set()
        for u in self.dados:
            for v in self.dados[u]:
                for opcao in self.dados[u][v]:
                    linhas.add(opcao["linha"])
        return linhas
