import math
import tkinter as tk
from tkinter import ttk, messagebox

class CalculadoraAterramento:
    def __init__(self, root):
        self.root = root
        self.root.title("🏗️ Calculadora de Resistência de Aterramento")
        self.root.geometry("750x850")
        self.root.configure(bg='#f0f0f0')
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Variáveis
        self.opcao_var = tk.StringVar()
        self.resistividade_var = tk.StringVar()
        
        # Variáveis para campos dinâmicos
        self.campos_haste_unica = {}
        self.campos_multiplas_hastes = {}
        self.campos_condutor_horizontal = {}
        self.campos_malha = {}
        
        self.criar_interface()
    
    def configurar_estilo(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar fontes
        style.configure('Titulo.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitulo.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Normal.TLabel', font=('Arial', 10))
        style.configure('Grande.TLabel', font=('Arial', 11))
        style.configure('Resultado.TLabel', font=('Arial', 12, 'bold'))
        
        style.configure('TFrame', background='#f0f0f0')
        style.configure('Card.TFrame', background='white', relief='raised', borderwidth=1)
        
        style.configure('Botao.TButton', font=('Arial', 11, 'bold'), padding=(10, 5))
    
    def criar_interface(self):
        # Criar um canvas com scrollbar
        self.main_canvas = tk.Canvas(self.root, bg='#f0f0f0')
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.main_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )
        
        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Frame principal dentro do canvas
        main_frame = ttk.Frame(self.scrollable_frame, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Título principal
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.pack(fill="x", pady=(0, 20))
        
        ttk.Label(titulo_frame, text="🏗️ CALCULADORA DE RESISTÊNCIA DE ATERRAMENTO", 
                 style='Titulo.TLabel').pack(pady=10)
        
        # Frame de seleção
        selecao_frame = ttk.LabelFrame(main_frame, text="🔧 CONFIGURAÇÃO DO ELETRODO", padding="15")
        selecao_frame.pack(fill="x", pady=(0, 15))
        
        # Seleção do tipo de eletrodo
        ttk.Label(selecao_frame, text="Selecione o tipo de eletrodo:", 
                 style='Subtitulo.TLabel').pack(anchor="w", pady=(0, 10))
        
        opcoes = [
            ("📍 Haste vertical única", "1"),
            ("📏 Múltiplas hastes em linha", "2"),
            ("➖ Condutor horizontal enterrado", "3"),
            ("🔲 Aterramento em malha", "4")
        ]
        
        for texto, valor in opcoes:
            rb = ttk.Radiobutton(selecao_frame, text=texto, variable=self.opcao_var, 
                               value=valor, command=self.mostrar_campos, style='Grande.TLabel')
            rb.pack(anchor="w", pady=5)
        
        # Resistividade do solo
        resist_frame = ttk.Frame(selecao_frame)
        resist_frame.pack(fill="x", pady=(15, 0))
        
        ttk.Label(resist_frame, text="Resistividade do solo (Ω.m):", 
                 style='Subtitulo.TLabel').pack(anchor="w")
        
        entry_resist = ttk.Entry(resist_frame, textvariable=self.resistividade_var, 
                 width=15, font=('Arial', 11))
        entry_resist.pack(anchor="w", pady=(5, 0))
        
        ttk.Label(resist_frame, text="Ex: 100 para solo argiloso úmido", 
                 style='Normal.TLabel', foreground='#666').pack(anchor="w", pady=(5, 0))
        
        # Frame para campos dinâmicos
        self.frame_campos = ttk.LabelFrame(main_frame, text="📝 DADOS DO ELETRODO", padding="15")
        self.frame_campos.pack(fill="x", pady=(0, 15))
        
        # Botão calcular
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill="x", pady=10)
        
        self.btn_calcular = ttk.Button(btn_frame, text="🧮 CALCULAR RESISTÊNCIA", 
                  command=self.calcular, style='Botao.TButton')
        self.btn_calcular.pack(pady=10)
        
        # Frame para resultados
        self.frame_resultado = ttk.LabelFrame(main_frame, text="📊 RESULTADO", padding="20")
        self.frame_resultado.pack(fill="x", pady=(10, 0))
        
        # Inicialmente esconder o frame de resultados
        self.frame_resultado.pack_forget()
    
    def mostrar_campos(self):
        # Limpar frame de campos
        for widget in self.frame_campos.winfo_children():
            widget.destroy()
        
        opcao = self.opcao_var.get()
        
        if opcao == "1":
            self.criar_campos_haste_unica()
        elif opcao == "2":
            self.criar_campos_multiplas_hastes()
        elif opcao == "3":
            self.criar_campos_condutor_horizontal()
        elif opcao == "4":
            self.criar_campos_malha()
        
        # Esconder resultados anteriores quando mudar a configuração
        self.frame_resultado.pack_forget()
    
    def criar_campos_haste_unica(self):
        # Frame interno para organização
        inner_frame = ttk.Frame(self.frame_campos)
        inner_frame.pack(fill="x")
        
        ttk.Label(inner_frame, text="Haste Vertical Única", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        campos = [
            ("Comprimento da haste (m):", "comprimento", "Ex: 2.4, 3.0"),
            ("Diâmetro da haste (m):", "diametro", "Ex: 0.016 (16mm)")
        ]
        
        for i, (label, key, exemplo) in enumerate(campos):
            ttk.Label(inner_frame, text=label, style='Grande.TLabel').grid(row=1+i, column=0, sticky="w", pady=8)
            self.campos_haste_unica[key] = ttk.Entry(inner_frame, width=15, font=('Arial', 11))
            self.campos_haste_unica[key].grid(row=1+i, column=1, sticky="w", pady=8, padx=(10, 0))
            
            ttk.Label(inner_frame, text=exemplo, style='Normal.TLabel', 
                     foreground='#666').grid(row=1+i, column=2, sticky="w", padx=(10, 0), pady=8)
    
    def criar_campos_multiplas_hastes(self):
        inner_frame = ttk.Frame(self.frame_campos)
        inner_frame.pack(fill="x")
        
        ttk.Label(inner_frame, text="Múltiplas Hastes em Linha", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        campos = [
            ("Número de hastes:", "n_hastes", "Ex: 4, 6"),
            ("Comprimento de cada haste (m):", "comprimento", "Ex: 2.4, 3.0"),
            ("Diâmetro das hastes (m):", "diametro", "Ex: 0.016 (16mm)"),
            ("Espaçamento entre hastes (m):", "espacamento", "Ex: 2.4, 3.0")
        ]
        
        for i, (label, key, exemplo) in enumerate(campos):
            ttk.Label(inner_frame, text=label, style='Grande.TLabel').grid(row=1+i, column=0, sticky="w", pady=8)
            self.campos_multiplas_hastes[key] = ttk.Entry(inner_frame, width=15, font=('Arial', 11))
            self.campos_multiplas_hastes[key].grid(row=1+i, column=1, sticky="w", pady=8, padx=(10, 0))
            
            ttk.Label(inner_frame, text=exemplo, style='Normal.TLabel', 
                     foreground='#666').grid(row=1+i, column=2, sticky="w", padx=(10, 0), pady=8)
    
    def criar_campos_condutor_horizontal(self):
        inner_frame = ttk.Frame(self.frame_campos)
        inner_frame.pack(fill="x")
        
        ttk.Label(inner_frame, text="Condutor Horizontal Enterrado", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        # Adicionar informação da fórmula
        info_frame = ttk.Frame(inner_frame)
        info_frame.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        ttk.Label(info_frame, text="📐 Fórmula: R = ρ/(2πL) × [ln(2L/d) + ln(L/2h) - 2 + 2h/L]", 
                 style='Normal.TLabel', foreground='#2c3e50', font=('Arial', 9, 'italic')).pack(anchor="w")
        
        campos = [
            ("Comprimento do condutor (m):", "comprimento", "Ex: 15, 20"),
            ("Diâmetro do condutor (m):", "diametro", "Ex: 0.010 (10mm)"),
            ("Profundidade de enterramento (m):", "profundidade", "Ex: 0.6, 0.8")
        ]
        
        for i, (label, key, exemplo) in enumerate(campos):
            ttk.Label(inner_frame, text=label, style='Grande.TLabel').grid(row=2+i, column=0, sticky="w", pady=8)
            self.campos_condutor_horizontal[key] = ttk.Entry(inner_frame, width=15, font=('Arial', 11))
            self.campos_condutor_horizontal[key].grid(row=2+i, column=1, sticky="w", pady=8, padx=(10, 0))
            
            ttk.Label(inner_frame, text=exemplo, style='Normal.TLabel', 
                     foreground='#666').grid(row=2+i, column=2, sticky="w", padx=(10, 0), pady=8)
    
    def criar_campos_malha(self):
        inner_frame = ttk.Frame(self.frame_campos)
        inner_frame.pack(fill="x")
        
        ttk.Label(inner_frame, text="Malha de Aterramento", 
                 style='Subtitulo.TLabel').grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        campos = [
            ("Área da malha (m²):", "area", "Ex: 36 (6x6m), 64 (8x8m)"),
            ("Comprimento total dos condutores (m):", "comprimento_total", "Ex: 24, 32"),
            ("Profundidade da malha (m):", "profundidade", "Ex: 0.5, 0.6")
        ]
        
        for i, (label, key, exemplo) in enumerate(campos):
            ttk.Label(inner_frame, text=label, style='Grande.TLabel').grid(row=1+i, column=0, sticky="w", pady=8)
            self.campos_malha[key] = ttk.Entry(inner_frame, width=15, font=('Arial', 11))
            self.campos_malha[key].grid(row=1+i, column=1, sticky="w", pady=8, padx=(10, 0))
            
            ttk.Label(inner_frame, text=exemplo, style='Normal.TLabel', 
                     foreground='#666').grid(row=1+i, column=2, sticky="w", padx=(10, 0), pady=8)
    
    def obter_valor(self, entry_widget):
        try:
            return float(entry_widget.get())
        except ValueError:
            return None
    
    def calcular(self):
        # Validar resistividade
        try:
            resistividade_solo = float(self.resistividade_var.get())
        except ValueError:
            messagebox.showerror("Erro", "❌ Digite um valor válido para a resistividade do solo!")
            return
        
        opcao = self.opcao_var.get()
        
        if not opcao:
            messagebox.showerror("Erro", "❌ Selecione um tipo de eletrodo!")
            return
        
        try:
            if opcao == "1":
                resultado = self.calcular_haste_unica(resistividade_solo)
            elif opcao == "2":
                resultado = self.calcular_multiplas_hastes(resistividade_solo)
            elif opcao == "3":
                resultado = self.calcular_condutor_horizontal(resistividade_solo)
            elif opcao == "4":
                resultado = self.calcular_malha(resistividade_solo)
            else:
                messagebox.showerror("Erro", "❌ Selecione uma opção válida!")
                return
            
            self.mostrar_resultado(resultado, resistividade_solo)
            
        except ValueError as e:
            messagebox.showerror("Erro", "❌ Digite valores numéricos válidos em todos os campos!")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro inesperado: {e}")
    
    def calcular_haste_unica(self, resistividade_solo):
        comprimento = self.obter_valor(self.campos_haste_unica['comprimento'])
        diametro = self.obter_valor(self.campos_haste_unica['diametro'])
        
        if comprimento is None or diametro is None:
            raise ValueError("Valores inválidos")
        
        R = (resistividade_solo / (2 * math.pi * comprimento)) * (math.log((4 * comprimento) / diametro) - 1)
        
        return {
            'resistencia': R,
            'configuracao': 'Haste vertical única',
            'detalhes': {'comprimento': comprimento, 'diametro': diametro}
        }
    
    def calcular_multiplas_hastes(self, resistividade_solo):
        n_hastes = int(self.obter_valor(self.campos_multiplas_hastes['n_hastes']))
        comprimento = self.obter_valor(self.campos_multiplas_hastes['comprimento'])
        diametro = self.obter_valor(self.campos_multiplas_hastes['diametro'])
        espacamento = self.obter_valor(self.campos_multiplas_hastes['espacamento'])
        
        if any(v is None for v in [n_hastes, comprimento, diametro, espacamento]):
            raise ValueError("Valores inválidos")
        
        # FÓRMULA CORRIGIDA - Múltiplas Hastes em Linha
        R = resistividade_solo / (2 * math.pi * n_hastes * comprimento) * (
            math.log(4 * comprimento / diametro) - 1 + 
            2 * (comprimento / espacamento) * math.log(2 * n_hastes / math.pi)
        )
        
        return {
            'resistencia': R,
            'configuracao': 'Múltiplas hastes em linha',
            'detalhes': {
                'n_hastes': n_hastes, 
                'comprimento': comprimento, 
                'diametro': diametro, 
                'espacamento': espacamento
            }
        }
    
    def calcular_condutor_horizontal(self, resistividade_solo):
        comprimento = self.obter_valor(self.campos_condutor_horizontal['comprimento'])
        diametro = self.obter_valor(self.campos_condutor_horizontal['diametro'])
        profundidade = self.obter_valor(self.campos_condutor_horizontal['profundidade'])
        
        if any(v is None for v in [comprimento, diametro, profundidade]):
            raise ValueError("Valores inválidos")
        
        # FÓRMULA DE DWIGHT PARA CONDUTOR HORIZONTAL - MODIFICADA
        R = (resistividade_solo / (2 * math.pi * comprimento)) * (
            math.log(2 * comprimento / diametro) + 
            math.log(comprimento / (2 * profundidade)) - 
            2 + (2 * profundidade / comprimento)
        )
        
        return {
            'resistencia': R,
            'configuracao': 'Condutor horizontal enterrado',
            'detalhes': {
                'comprimento': comprimento, 
                'diametro': diametro, 
                'profundidade': profundidade,
                'formula': 'Dwight'
            }
        }
    
    def calcular_malha(self, resistividade_solo):
        area = self.obter_valor(self.campos_malha['area'])
        comprimento_total = self.obter_valor(self.campos_malha['comprimento_total'])
        profundidade = self.obter_valor(self.campos_malha['profundidade'])
        
        if any(v is None for v in [area, comprimento_total, profundidade]):
            raise ValueError("Valores inválidos")
        
        R = resistividade_solo * (1/comprimento_total + 1/math.sqrt(20*area)) * (1 + 1/(1 + profundidade * math.sqrt(area/10)))
        
        return {
            'resistencia': R,
            'configuracao': 'Malha de aterramento',
            'detalhes': {'area': area, 'comprimento_total': comprimento_total, 'profundidade': profundidade}
        }
    
    def mostrar_resultado(self, resultado, resistividade_solo):
        # Limpar resultados anteriores
        for widget in self.frame_resultado.winfo_children():
            widget.destroy()
        
        resistencia = resultado['resistencia']
        configuracao = resultado['configuracao']
        detalhes = resultado['detalhes']
        
        # Mostrar o frame de resultados
        self.frame_resultado.pack(fill="x", pady=(10, 0))
        
        # Configuração e resistividade
        ttk.Label(self.frame_resultado, text=f"📋 Configuração: {configuracao}", 
                 style='Subtitulo.TLabel').pack(anchor="w", pady=5)
        
        # Mostrar fórmula específica para condutor horizontal
        if configuracao == 'Condutor horizontal enterrado':
            ttk.Label(self.frame_resultado, text=f"📐 Fórmula aplicada: Dwight para condutor horizontal", 
                     style='Normal.TLabel', foreground='#666', font=('Arial', 10, 'italic')).pack(anchor="w", pady=2)
        
        ttk.Label(self.frame_resultado, text=f"🌱 Resistividade do solo: {resistividade_solo} Ω.m", 
                 style='Grande.TLabel').pack(anchor="w", pady=2)
        
        # Separador
        separator1 = ttk.Separator(self.frame_resultado, orient='horizontal')
        separator1.pack(fill="x", pady=10)
        
        # Resistência calculada
        ttk.Label(self.frame_resultado, text=f"🧮 Resistência de aterramento calculada:", 
                 style='Grande.TLabel').pack(anchor="w", pady=2)
        
        ttk.Label(self.frame_resultado, text=f"{resistencia:.2f} Ω", 
                 font=('Arial', 20, 'bold'), foreground='#2c3e50').pack(anchor="w", pady=(0, 10))
        
        # Separador
        separator2 = ttk.Separator(self.frame_resultado, orient='horizontal')
        separator2.pack(fill="x", pady=10)
        
        # Análise da norma
        ttk.Label(self.frame_resultado, text="📊 ANÁLISE CONFORME NORMAS:", 
                 style='Subtitulo.TLabel').pack(anchor="w", pady=(10, 5))
        
        if resistencia <= 1.0:
            status_text = "✅ EXCELENTE - Atende: Sistemas de equipamentos sensíveis (≤ 1 Ω)"
            cor = '#27ae60'
        elif resistencia <= 5.0:
            status_text = "✅ ÓTIMO - Atende: Sistemas de telecomunicações (≤ 5 Ω)"
            cor = '#2ecc71'
        elif resistencia <= 10.0:
            status_text = "✅ BOM - Atende: Sistemas de potência e para-raios (≤ 10 Ω)"
            cor = '#f39c12'
        else:
            status_text = "❌ PRECISA MELHORAR - Não atende: Resistência acima dos limites normativos (> 10 Ω)"
            cor = '#e74c3c'
        
        status_label = ttk.Label(self.frame_resultado, text=status_text, 
                               font=('Arial', 11, 'bold'), foreground=cor)
        status_label.pack(anchor="w", pady=5)
        
        # Sugestões se não atender
        if resistencia > 10.0:
            separator3 = ttk.Separator(self.frame_resultado, orient='horizontal')
            separator3.pack(fill="x", pady=10)
            
            ttk.Label(self.frame_resultado, text="💡 SUGESTÕES PARA REDUZIR A RESISTÊNCIA:", 
                     style='Subtitulo.TLabel').pack(anchor="w", pady=(15, 10))
            
            sugestoes = self.gerar_sugestoes(configuracao, detalhes, resistencia)
            for sugestao in sugestoes:
                ttk.Label(self.frame_resultado, text=f"• {sugestao}", 
                         style='Grande.TLabel').pack(anchor="w", pady=2)
        
        # Informações adicionais
        separator4 = ttk.Separator(self.frame_resultado, orient='horizontal')
        separator4.pack(fill="x", pady=10)
        
        ttk.Label(self.frame_resultado, text="💡 Observação: Este cálculo é para projeto preliminar. Validação requer medição in loco.", 
                 style='Normal.TLabel', foreground='#666').pack(anchor="w", pady=2)
        
        # Forçar atualização da interface
        self.root.update_idletasks()
    
    def gerar_sugestoes(self, configuracao, detalhes, resistencia):
        sugestoes = []
        
        if configuracao == 'Haste vertical única':
            sugestoes.extend([
                "Adicionar mais hastes em paralelo",
                f"Aumentar comprimento da haste para 4-6m",
                "Usar haste de maior diâmetro (ex: 19mm)"
            ])
        elif configuracao == 'Múltiplas hastes em linha':
            sugestoes.extend([
                f"Aumentar número de hastes",
                f"Aumentar comprimento das hastes para 3-4m",
                f"Reduzir espaçamento entre hastes"
            ])
        elif configuracao == 'Condutor horizontal enterrado':
            sugestoes.extend([
                f"Aumentar comprimento do condutor",
                "Enterrar em maior profundidade (0.8-1.0m)",
                "Adicionar hastes verticais nos extremos",
                "Usar condutor de maior diâmetro"
            ])
        elif configuracao == 'Malha de aterramento':
            sugestoes.extend([
                f"Aumentar área da malha",
                "Aumentar comprimento dos condutores",
                "Adicionar hastes verticais nos cantos da malha"
            ])
        
        sugestoes.extend([
            "Aplicar tratamento químico no solo",
            "Usar aterramento profundo (hastes de 6-12m)",
            "Considerar uso de composto eletrocondutor"
        ])
        
        return sugestoes

# Executar aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraAterramento(root)
    root.mainloop()