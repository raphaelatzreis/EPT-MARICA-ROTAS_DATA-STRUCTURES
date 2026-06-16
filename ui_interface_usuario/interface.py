# interface.py
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import networkx as nx

class InterfaceEPT:
    def __init__(self, roteador):
        self.roteador = roteador
        
        self.texto_origem = ""
        self.texto_destino = ""
        self.texto_linha = ""
        # REMOVIDO: self.texto_add (funcionalidade de adicionar rota removida)

        # DESIGN: Fundo da janela cinza claro moderno
        self.fig, self.ax_main = plt.subplots(figsize=(10, 8), facecolor="#F4F6F9")
        # Ajuste de layout mantido para acomodar o restante dos elementos
        plt.subplots_adjust(bottom=0.35, top=0.85, left=0.05, right=0.95)

        # Configuração do painel de log com fundo branco e borda suave
        self.ax_log = plt.axes([0.65, 0.10, 0.30, 0.20], facecolor="#FFFFFF")
        self.ax_log.axis("off")

        self.configurar_widgets()
        self.atualizar_plot()
        self.atualizar_log("Olá! Bem-vindo ao sistema de rotas.\n\nUse os controles ao lado para simular\ne gerenciar o tráfego.")

    def atualizar_log(self, texto):
        self.ax_log.clear()
        self.ax_log.axis("off")
        # DESIGN: Título do log em vermelho EPT
        self.ax_log.text(0.05, 0.95, "DETALHES DA OPERAÇÃO:", fontsize=10, fontweight="bold", color="#E30613", va="top")
        self.ax_log.text(0.05, 0.75, texto, fontsize=9.5, color="#333333", va="top")
        self.fig.canvas.draw_idle()

    def atualizar_plot(self, caminho_destacado=None):
        self.ax_main.clear()
        # DESIGN: Título com cor da marca
        self.ax_main.set_title("SISTEMA DE TRANSPORTE EPT - MARICÁ", fontsize=15, fontweight="bold", color="#CC0000", pad=20)
        
        dados_grafo = self.roteador.grafo_obj.dados
        linhas_off = self.roteador.linhas_desativadas
        
        G = nx.Graph()
        for u in dados_grafo:
            for v in dados_grafo[u]:
                G.add_edge(u, v)
                
        posicoes_base = {
            "Terminal Centro": (0, 0),
            "Araçatiba": (-0.5, -2.5), 
            "Jacaroá": (3, -1.5),
            "São José": (-4.5, 0.5),
            "Inoã": (-7, 1.5),
            "Maricá": (-2.5, -1.8),
            "Retiro": (-1.5, 3.5),
            "Espraiado": (4, 3.5),
            "Itaipuaçu": (-9, -1),
            "Recanto": (-11, -1.5),
            "Cajueiros": (-7.5, -3.5),
            "Guaratiba": (4.5, -3),
            "Ponta Negra": (8, -1),
            "Cordeirinho": (7, -3.5),
            "Jaconé": (10.5, -1)
        }
        
        pos_fixas = {no: coords for no, coords in posicoes_base.items() if no in G.nodes()}
        if len(pos_fixas) == len(G.nodes()):
            pos = pos_fixas
        else:
            pos = nx.spring_layout(G, pos=pos_fixas, fixed=pos_fixas.keys(), seed=42)
        
        pos_labels = {}
        for no, coords in pos.items():
            pos_labels[no] = (coords[0], coords[1] + 0.4)
            
        # DESIGN: Nós agora são vermelhos com borda branca, imitando os "Vermelhinhos"
        nos = nx.draw_networkx_nodes(G, pos, ax=self.ax_main, node_size=600, node_color="#E30613", edgecolors="white", linewidths=2)
        nos.set_zorder(3)
        
        fundo_cidades = dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="#DDDDDD", alpha=0.9)
        labels_cidades = nx.draw_networkx_labels(G, pos_labels, ax=self.ax_main, font_size=9, font_weight="bold", font_family="sans-serif", verticalalignment="bottom", bbox=fundo_cidades)
        
        for texto in labels_cidades.values():
            texto.set_color("#2C3E50") # Fonte dos bairros um pouco mais suave que preto absoluto
            texto.set_zorder(4)
        
        edges_normais, edges_desativados, edges_caminho = [], [], []
        
        for u, v in G.edges():
            linha = dados_grafo[u][v]["linha"]
            no_caminho = False
            
            if caminho_destacado:
                for i in range(len(caminho_destacado) - 1):
                    if (caminho_destacado[i] == u and caminho_destacado[i+1] == v) or (caminho_destacado[i] == v and caminho_destacado[i+1] == u):
                        no_caminho = True
                        break
                        
            if no_caminho:
                edges_caminho.append((u, v))
            elif linha in linhas_off:
                edges_desativados.append((u, v))
            else:
                edges_normais.append((u, v))
                
        # DESIGN: Linhas normais cinzas, desativadas cinza escuro
        linhas_n = nx.draw_networkx_edges(G, pos, edgelist=edges_normais, ax=self.ax_main, width=2, edge_color="#BDC3C7", style="solid")
        if linhas_n: linhas_n.set_zorder(1)
            
        linhas_d = nx.draw_networkx_edges(G, pos, edgelist=edges_desativados, ax=self.ax_main, width=2, edge_color="#7F8C8D", style="dashed")
        if linhas_d: linhas_d.set_zorder(1)
            
        # DESIGN: Caminho destacado em Verde vibrante
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
                dados = dados_grafo[u][v]
                linha, tempo = dados["linha"], dados["tempo"]
                status = " [OFF]" if linha in linhas_off else ""
                lbl = {(u, v): f"L:{linha} ({tempo}m){status}"}
                
                nx.draw_networkx_edge_labels(G, pos, edge_labels=lbl, ax=self.ax_main, 
                font_size=7, font_color="#555555", label_pos=0.5, 
                rotate=False, bbox=caixa_texto)
            else:
                num_edges = len(edges)
                for i, (u, v) in enumerate(edges):
                    pos_val = 0.3 if num_edges == 2 and i == 0 else (0.7 if num_edges == 2 else 0.2 + (0.6 * i / (num_edges - 1)))
                    dados = dados_grafo[u][v]
                    linha, tempo = dados["linha"], dados["tempo"]
                    status = " [OFF]" if linha in linhas_off else ""
                    lbl = {(u, v): f"L:{linha} ({tempo}m){status}"}
                    
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=lbl, ax=self.ax_main, 
                    font_size=7, font_color="#555555", label_pos=pos_val, 
                    rotate=False, bbox=caixa_texto)
        
        for text in self.ax_main.texts:
            if text.get_zorder() == 1:
                text.set_zorder(2)

        self.ax_main.axis("off")
        self.fig.canvas.draw_idle()

    def txt_origem_changed(self, val): self.texto_origem = val.strip()
    def txt_destino_changed(self, val): self.texto_destino = val.strip()
    def txt_linha_changed(self, val): self.texto_linha = val.strip()
    # REMOVIDO: Método txt_add_changed

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
                caminho_str = " -> ".join(f"Pt {n}" for n in caminho)
                linhas_str = ", ".join(f"Linha(s): {l}" for l in lines)
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

    # REMOVIDO: Método adicionar_rota_click

    def configurar_widgets(self):
        self.ax_txt_origem = plt.axes([0.10, 0.25, 0.10, 0.04])
        self.box_origem = widgets.TextBox(self.ax_txt_origem, 'Partida: ', initial='')
        self.box_origem.on_text_change(self.txt_origem_changed)

        self.ax_txt_destino = plt.axes([0.30, 0.25, 0.10, 0.04])
        self.box_destino = widgets.TextBox(self.ax_txt_destino, 'Destino: ', initial='')
        self.box_destino.on_text_change(self.txt_destino_changed)

        # DESIGN: Botão de busca Verde (Sucesso)
        self.ax_btn_buscar = plt.axes([0.42, 0.25, 0.12, 0.04])
        self.btn_buscar = widgets.Button(self.ax_btn_buscar, 'Achar Rota', color="#27AE60", hovercolor="#229954")
        self.btn_buscar.label.set_color("white")
        self.btn_buscar.label.set_fontweight("bold")
        self.btn_buscar.on_clicked(self.buscar_caminho_click)

        self.ax_txt_linha = plt.axes([0.10, 0.18, 0.10, 0.04])
        self.box_linha = widgets.TextBox(self.ax_txt_linha, 'Linha: ', initial='')
        self.box_linha.on_text_change(self.txt_linha_changed)

        # DESIGN: Botão de alternar Laranja (Alerta)
        self.ax_btn_toggle = plt.axes([0.22, 0.18, 0.12, 0.04])
        self.btn_toggle = widgets.Button(self.ax_btn_toggle, 'Alternar', color="#F39C12", hovercolor="#D68910")
        self.btn_toggle.label.set_color("white")
        self.btn_toggle.label.set_fontweight("bold")
        self.btn_toggle.on_clicked(self.toggle_linha_click)

        # REMOVIDO: Widgets ax_txt_add, box_add, ax_btn_add e btn_add

    def iniciar(self):
        plt.show()