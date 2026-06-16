# grafo.py
class Grafo:
    def __init__(self):
        # Dados estruturados do sistema EPT
        self.dados = {
            "Terminal Centro": {
                "Ponta Negra": {"tempo": 50, "linha": "E01"},
                "São José": {"tempo": 20, "linha": "E24"},
                "Araçatiba": {"tempo": 15, "linha": "E05"},
                "Retiro": {"tempo": 25, "linha": "E15"},
                "Jacaroá": {"tempo": 20, "linha": "E08"},
                "Guaratiba": {"tempo": 30, "linha": "E09"},
                "Espraiado": {"tempo": 45, "linha": "E14"}
            },
            "Ponta Negra": {
                "Terminal Centro": {"tempo": 50, "linha": "E01"},
                "Cordeirinho": {"tempo": 20, "linha": "E02"},
                "Jaconé": {"tempo": 15, "linha": "E01A"}
            },
            "São José": {
                "Terminal Centro": {"tempo": 20, "linha": "E24"},
                "Inoã": {"tempo": 20, "linha": "E24"}
            },
            "Inoã": {
                "São José": {"tempo": 20, "linha": "E24"},
                "Itaipuaçu": {"tempo": 30, "linha": "E26"},
                "Maricá": {"tempo": 35, "linha": "E11"}
            },
            "Itaipuaçu": {
                "Inoã": {"tempo": 30, "linha": "E26"},
                "Recanto": {"tempo": 15, "linha": "E30"},
                "Cajueiros": {"tempo": 20, "linha": "E32"}
            },
            "Cordeirinho": {"Ponta Negra": {"tempo": 20, "linha": "E02"}},
            "Recanto": {"Itaipuaçu": {"tempo": 15, "linha": "E30"}},
            "Araçatiba": {"Terminal Centro": {"tempo": 15, "linha": "E05"}},
            "Maricá": {"Inoã": {"tempo": 35, "linha": "E11"}},
            "Retiro": {"Terminal Centro": {"tempo": 25, "linha": "E15"}},
            "Jacaroá": {"Terminal Centro": {"tempo": 20, "linha": "E08"}},
            "Guaratiba": {"Terminal Centro": {"tempo": 30, "linha": "E09"}},
            "Espraiado": {"Terminal Centro": {"tempo": 45, "linha": "E14"}},
            "Cajueiros": {"Itaipuaçu": {"tempo": 20, "linha": "E32"}},
            "Jaconé": {"Ponta Negra": {"tempo": 15, "linha": "E01A"}}
        }

    def obter_todas_linhas(self):
        linhas = set()
        for u in self.dados:
            for v in self.dados[u]:
                linhas.add(self.dados[u][v]["linha"])
        return linhas