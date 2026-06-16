import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import networkx as nx

class InterfaceEPT:
    def __init__(self, roteador):
        self.roteador = roteador
        
        self.texto_origem = ""
        self.texto_destino = ""
        self.texto_linha = ""

        self.fig, self.ax_main = plt.subplots(figsize=(10, 8), facecolor="#F4F6F9")
        plt.subplots_adjust(bottom=0.35, top=0.85, left=0.05, right=0.95)

        self.ax_log = plt.axes([0.65, 0.06, 0.30, 0.24], facecolor="#FFFFFF")
        self.ax_log.axis("off")

        self.configurar_widgets()
        self.atualizar_plot()
        self.atualizar_log("Olá! Bem-vindo ao sistema de rotas.\n\nUse os controles ao lado para simular\ne gerenciar o tráfego.")

    def atualizar_log(self, texto):
        self.ax_log.clear()
        self.ax_log.axis("off")
        
        import textwrap
        linhas_wrapped = []
        for linha in texto.split("\n"):
            if linha.strip():
                linhas_wrapped.append(textwrap.fill(linha, width=42))
            else:
                linhas_wrapped.append("")
        texto_wrapped = "\n".join(linhas_wrapped)
        
        self.ax_log.text(0.05, 0.95, "DETALHES DA OPERAÇÃO:", fontsize=10, fontweight="bold", color="#E30613", va="top")
        self.ax_log.text(0.05, 0.82, texto_wrapped, fontsize=9.5, color="#333333", va="top")
        self.fig.canvas.draw_idle()

    def atualizar_plot(self, caminho_destacado=None):
        self.ax_main.clear()
        self.ax_main.set_title("SISTEMA DE TRANSPORTE EPT - MARICÁ", fontsize=15, fontweight="bold", color="#CC0000", pad=20)
        
        dados_grafo = self.roteador.grafo_obj.dados
        linhas_off = self.roteador.linhas_desativadas
        
        G = nx.Graph()
        for u in dados_grafo:
            for v in dados_grafo[u]:
                G.add_edge(u, v)
                
        posicoes_base = {
            "Maricá": (0, 0),
            "Avenida": (1.5, 1.5),
            "Flamengo": (1.5, -1.5),
            "Parque Nanci": (3.5, 0),
            "São José": (6.0, 1.5),
            "Inoã": (11.0, 1.5),
            "Itaipuaçu": (11.0, -3.0),
            "Recanto": (13.5, -3.0)
        }
        
        pos_fixas = {no: coords for no, coords in posicoes_base.items() if no in G.nodes()}
        if len(pos_fixas) == len(G.nodes()):
            pos = pos_fixas
        else:
            pos = nx.spring_layout(G, pos=pos_fixas, fixed=pos_fixas.keys(), seed=42)
        
        pos_labels = {}
        for no, coords in pos.items():
            pos_labels[no] = (coords[0], coords[1] + 0.4)
            
        nos = nx.draw_networkx_nodes(G, pos, ax=self.ax_main, node_size=600, node_color="#E30613", edgecolors="white", linewidths=2)
        nos.set_zorder(3)
        
        fundo_cidades = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#DDDDDD", alpha=0.9)
        labels_cidades = nx.draw_networkx_labels(G, pos_labels, ax=self.ax_main, font_size=9, font_weight="bold", font_family="sans-serif", verticalalignment="bottom", bbox=fundo_cidades)
        
        for texto in labels_cidades.values():
            texto.set_color("#2C3E50")
            texto.set_zorder(4)
        
        edges_normais, edges_desativados, edges_caminho = [], [], []
        
        for u, v in G.edges():
            opcoes = dados_grafo[u][v]
            todas_desativadas = all(op["linha"] in linhas_off for op in opcoes)
            no_caminho = False
            
            if caminho_destacado:
                for i in range(len(caminho_destacado) - 1):
                    if (caminho_destacado[i] == u and caminho_destacado[i+1] == v) or (caminho_destacado[i] == v and caminho_destacado[i+1] == u):
                        no_caminho = True
                        break
                        
            if no_caminho:
                edges_caminho.append((u, v))
            elif todas_desativadas:
                edges_desativados.append((u, v))
            else:
                edges_normais.append((u, v))
                
        linhas_n = nx.draw_networkx_edges(G, pos, edgelist=edges_normais, ax=self.ax_main, width=2, edge_color="#BDC3C7", style="solid")
        if linhas_n: linhas_n.set_zorder(1)
            
        linhas_d = nx.draw_networkx_edges(G, pos, edgelist=edges_desativados, ax=self.ax_main, width=2, edge_color="#7F8C8D", style="dashed")
        if linhas_d: linhas_d.set_zorder(1)
            
        if edges_caminho:
            linhas_c = nx.draw_networkx_edges(G, pos, edgelist=edges_caminho, ax=self.ax_main, width=4.5, edge_color="#27AE60", style="solid")
            if linhas_c: linhas_c.set_zorder(2)
            
        midpoint_groups = {}
        for u, v in G.edges():
            pu, pv = pos[u], pos[v]
            mx, my = round((pu[0] + pv[0]) / 2, 2), round((pu[1] + pv[1]) / 2, 2)
            key = (mx, my)
            if key not in midpoint_groups:
                midpoint_groups[key] = []
            midpoint_groups[key].append((u, v))
            
        caixa_texto = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#EEEEEE", alpha=0.9)

        for key, edges in midpoint_groups.items():
            if len(edges) == 1:
                u, v = edges[0]
                opcoes = dados_grafo[u][v]
                linhas_por_tempo = {}
                for op in opcoes:
                    t = op["tempo"]
                    l = op["linha"]
                    status = f"{l}" + ("(OFF)" if l in linhas_off else "")
                    if t not in linhas_por_tempo:
                        linhas_por_tempo[t] = []
                    linhas_por_tempo[t].append(status)
                
                linhas_label = []
                for t, lst in linhas_por_tempo.items():
                    if len(lst) >= 2:
                        linhas_label.append(f"({ ' / '.join(lst) }) ({t}m)")
                    else:
                        linhas_label.append(f"{lst[0]} ({t}m)")
                lbl_str = "\n".join(linhas_label)
                lbl = {(u, v): lbl_str}
                
                nx.draw_networkx_edge_labels(G, pos, edge_labels=lbl, ax=self.ax_main, 
                font_size=7, font_color="#555555", label_pos=0.5, 
                rotate=False, bbox=caixa_texto)
            else:
                num_edges = len(edges)
                for i, (u, v) in enumerate(edges):
                    pos_val = 0.3 if num_edges == 2 and i == 0 else (0.7 if num_edges == 2 else 0.2 + (0.6 * i / (num_edges - 1)))
                    opcoes = dados_grafo[u][v]
                    linhas_por_tempo = {}
                    for op in opcoes:
                        t = op["tempo"]
                        l = op["linha"]
                        status = f"{l}" + ("(OFF)" if l in linhas_off else "")
                        if t not in linhas_por_tempo:
                            linhas_por_tempo[t] = []
                        linhas_por_tempo[t].append(status)
                    
                    linhas_label = []
                    for t, lst in linhas_por_tempo.items():
                        if len(lst) >= 2:
                            linhas_label.append(f"({ ' / '.join(lst) }) ({t}m)")
                        else:
                            linhas_label.append(f"{lst[0]} ({t}m)")
                    lbl_str = "\n".join(linhas_label)
                    lbl = {(u, v): lbl_str}
                    
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=lbl, ax=self.ax_main, 
                    font_size=7, font_color="#555555", label_pos=pos_val, 
                    rotate=False, bbox=caixa_texto)
        
        for text in self.ax_main.texts:
            if text.get_zorder() == 1:
                text.set_zorder(2)

        self.ax_main.margins(x=0.15, y=0.25)
        self.ax_main.axis("off")
        self.fig.canvas.draw_idle()

    def txt_origem_changed(self, val): self.texto_origem = val.strip()
    def txt_destino_changed(self, val): self.texto_destino = val.strip()
    def txt_linha_changed(self, val): self.texto_linha = val.strip()

    def buscar_caminho_click(self, event):
        try:
            if not self.texto_origem or not self.texto_destino:
                self.atualizar_log("[ERRO]\nPreencha os campos de\nOrigem e Destino!")
                return
                
            inicio, fim = self.texto_origem.title(), self.texto_destino.title()
            
            if inicio not in self.roteador.grafo_obj.dados:
                self.atualizar_log("Parada não encontrada no sistema EPT.")
                return
                
            tempo, caminho, lines = self.roteador.calcular_caminho(inicio, fim)
            
            if caminho:
                dados_grafo = self.roteador.grafo_obj.dados
                linhas_off = self.roteador.linhas_desativadas
                step_descriptions = []
                
                for i in range(len(caminho) - 1):
                    u, v = caminho[i], caminho[i+1]
                    opcoes = dados_grafo[u][v]
                    
                    opcoes_ativas = [op for op in opcoes if op["linha"] not in linhas_off]
                    if opcoes_ativas:
                        min_t = min(op["tempo"] for op in opcoes_ativas)
                        linhas_mesmo_tempo = [op["linha"] for op in opcoes_ativas if op["tempo"] == min_t]
                        
                        if len(linhas_mesmo_tempo) >= 2:
                            linha_str = f"({ ' / '.join(linhas_mesmo_tempo) })"
                        else:
                            linha_str = linhas_mesmo_tempo[0]
                        step_descriptions.append(f"{linha_str} [{u}]")
                
                caminho_str = " -> ".join(f"Pt {n}" for n in caminho)
                linhas_str = " -> ".join(step_descriptions)
                info = f"Rota encontrada!\n\nTrajeto:\n{caminho_str}\n\nTempo: {tempo} min\n\nÔnibus: {linhas_str}"
                self.atualizar_log(info)
                self.atualizar_plot(caminho_destacado=caminho)
            else:
                self.atualizar_log("[ALERTA]\nNão há conexão ativa disponível\nentre esses dois pontos!")
                self.atualizar_plot()
        except ValueError:
            self.atualizar_log("[ERRO]\nDigite os nomes corretamente!")

    def toggle_linha_click(self, event):
        if not self.texto_linha:
            self.atualizar_log("[ERRO]\nDigite o número da linha!")
            return
            
        linha = self.texto_linha.upper()
        linhas_existentes = self.roteador.grafo_obj.obter_todas_linhas()
        
        if linha not in linhas_existentes:
            self.atualizar_log(f"[ERRO]\nA Linha {linha} não\nexiste no sistema!")
            return
            
        reativada = self.roteador.alternar_linha(linha)
        
        if reativada:
            self.atualizar_log(f"LINHA REATIVADA:\n\nA Linha {linha} está ativa\ne operando normalmente!")
        else:
            self.atualizar_log(f"FORA DE SERVIÇO:\n\nA Linha {linha} foi desativada.\nO sistema calculará rotas\nalternativas.")
            
        self.atualizar_plot()


    def configurar_widgets(self):
        self.ax_txt_origem = plt.axes([0.10, 0.25, 0.10, 0.04])
        self.box_origem = widgets.TextBox(self.ax_txt_origem, 'Partida: ', initial='')
        self.box_origem.on_text_change(self.txt_origem_changed)

        self.ax_txt_destino = plt.axes([0.30, 0.25, 0.10, 0.04])
        self.box_destino = widgets.TextBox(self.ax_txt_destino, 'Destino: ', initial='')
        self.box_destino.on_text_change(self.txt_destino_changed)

        self.ax_btn_buscar = plt.axes([0.42, 0.25, 0.12, 0.04])
        self.btn_buscar = widgets.Button(self.ax_btn_buscar, 'Achar Rota', color="#27AE60", hovercolor="#229954")
        self.btn_buscar.label.set_color("white")
        self.btn_buscar.label.set_fontweight("bold")
        self.btn_buscar.on_clicked(self.buscar_caminho_click)

        self.ax_txt_linha = plt.axes([0.10, 0.18, 0.10, 0.04])
        self.box_linha = widgets.TextBox(self.ax_txt_linha, 'Linha: ', initial='')
        self.box_linha.on_text_change(self.txt_linha_changed)

        self.ax_btn_toggle = plt.axes([0.22, 0.18, 0.12, 0.04])
        self.btn_toggle = widgets.Button(self.ax_btn_toggle, 'Alternar', color="#F39C12", hovercolor="#D68910")
        self.btn_toggle.label.set_color("white")
        self.btn_toggle.label.set_fontweight("bold")
        self.btn_toggle.on_clicked(self.toggle_linha_click)


    def iniciar(self):
        plt.show()
