import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider, Button, RadioButtons

class DemonstracaoAterramentoSeparada:
    def __init__(self):
        # Valores iniciais
        self.rho = 100  # Ω·m
        self.L = 2.4    # m
        self.d = 0.015  # m
        
        # Tipos de solo pré-definidos
        self.tipos_solo = {
            "Argila úmida": 50,
            "Terra agricultável": 150,
            "Areia úmida": 1000,
            "Rocha": 5000
        }
        
        # Criar figura principal para controles
        self.fig_controles = plt.figure(figsize=(10, 6))
        self.fig_controles.suptitle('🎮 CONTROLES - SISTEMA DE ATERRAMENTO', 
                                  fontsize=16, fontweight='bold')
        
        self.setup_ui()
        self.criar_visualizacao_principal()
        
    def formula_dwight(self, rho, L, d):
        """Fórmula de Dwight para hastes verticais"""
        if L <= 0 or d <= 0:
            return float('inf')
        return (rho / (2 * math.pi * L)) * math.log(4 * L / d)
    
    def setup_ui(self):
        """Configura a interface de controles"""
        plt.subplots_adjust(bottom=0.4, top=0.9)
        
        # Área de informações
        ax_info = plt.axes([0.1, 0.75, 0.8, 0.15])
        ax_info.axis('off')
        self.texto_info = ax_info.text(0.02, 0.8, '', transform=ax_info.transAxes, 
                                      fontsize=11, verticalalignment='top', fontfamily='monospace')
        
        # Slider para resistividade
        ax_rho = plt.axes([0.25, 0.6, 0.6, 0.03])
        self.slider_rho = Slider(
            ax=ax_rho,
            label='Resistividade do Solo (ρ) - Ω·m',
            valmin=10,
            valmax=10000,
            valinit=self.rho,
            valfmt='%0.0f Ω·m',
            color='#2E8B57'
        )
        
        # Slider para comprimento
        ax_L = plt.axes([0.25, 0.55, 0.6, 0.03])
        self.slider_L = Slider(
            ax=ax_L,
            label='Comprimento da Haste (L) - metros',
            valmin=0.5,
            valmax=10,
            valinit=self.L,
            valfmt='%0.1f m',
            color='#1E90FF'
        )
        
        # Slider para diâmetro
        ax_d = plt.axes([0.25, 0.5, 0.6, 0.03])
        self.slider_d = Slider(
            ax=ax_d,
            label='Diâmetro da Haste (d) - milímetros',
            valmin=5,
            valmax=50,
            valinit=self.d * 1000,
            valfmt='%0.0f mm',
            color='#FF8C00'
        )
        
        # Botões para tipos de solo
        ax_tipos_label = plt.axes([0.1, 0.35, 0.3, 0.1])
        ax_tipos_label.axis('off')
        ax_tipos_label.set_title('📊 TIPOS DE SOLO', fontweight='bold')
        
        self.radio_tipos = RadioButtons(
            plt.axes([0.1, 0.2, 0.2, 0.15]),
            list(self.tipos_solo.keys()),
            active=1
        )
        
        # Botões de ação
        ax_reset = plt.axes([0.7, 0.25, 0.2, 0.05])
        self.button_reset = Button(ax_reset, '🔄 Reset', color='#F0F0F0')
        
        ax_visualizar = plt.axes([0.7, 0.15, 0.2, 0.05])
        self.button_visualizar = Button(ax_visualizar, '📈 Ver Gráficos', color='#90EE90')
        
        # Conectar eventos
        self.slider_rho.on_changed(self.atualizar_valores)
        self.slider_L.on_changed(self.atualizar_valores)
        self.slider_d.on_changed(self.atualizar_valores)
        self.radio_tipos.on_clicked(self.selecionar_tipo_solo)
        self.button_reset.on_clicked(self.resetar)
        self.button_visualizar.on_clicked(self.mostrar_graficos)
        
        self.atualizar_informacoes()
    
    def selecionar_tipo_solo(self, label):
        """Atualiza para um tipo de solo pré-definido"""
        self.rho = self.tipos_solo[label]
        self.slider_rho.set_val(self.rho)
        self.atualizar_informacoes()
    
    def atualizar_valores(self, val):
        """Atualiza os valores quando os sliders mudam"""
        self.rho = self.slider_rho.val
        self.L = self.slider_L.val
        self.d = self.slider_d.val / 1000
        self.atualizar_informacoes()
    
    def resetar(self, event):
        """Reseta para valores padrão"""
        self.rho = 100
        self.L = 2.4
        self.d = 0.015
        self.slider_rho.set_val(self.rho)
        self.slider_L.set_val(self.L)
        self.slider_d.set_val(self.d * 1000)
        self.atualizar_informacoes()
    
    def atualizar_informacoes(self):
        """Atualiza o painel de informações"""
        R = self.formula_dwight(self.rho, self.L, self.d)
        tipo_solo = self.obter_tipo_solo(self.rho)
        
        info_text = f"""⚡ PARÂMETROS ATUAIS:

• Resistividade (ρ): {self.rho:>6.0f} Ω·m
• Comprimento (L):   {self.L:>6.1f} m
• Diâmetro (d):      {self.d*1000:>6.0f} mm
• Tipo de solo:      {tipo_solo:>15}
• Resistência (R):   {R:>6.1f} Ω

🎯 CLASSIFICAÇÃO: {self.classificar_resistencia(R)}"""
        
        self.texto_info.set_text(info_text)
        plt.draw()
    
    def obter_tipo_solo(self, rho):
        """Classifica o tipo de solo baseado na resistividade"""
        if rho <= 100: return "Argila úmida"
        elif rho <= 500: return "Terra agricultável"
        elif rho <= 2000: return "Areia úmida"
        else: return "Rocha"
    
    def classificar_resistencia(self, R):
        """Classifica a qualidade da resistência"""
        if R <= 10: return "⭐ EXCELENTE"
        elif R <= 25: return "✅ BOA"
        elif R <= 50: return "⚠️  ACEITÁVEL"
        else: return "❌ PRECISA MELHORAR"
    
    def criar_visualizacao_principal(self):
        """Cria a visualização principal do sistema"""
        self.fig_principal = plt.figure(figsize=(8, 8))
        self.fig_principal.suptitle('🏗️ VISUALIZAÇÃO DO SISTEMA DE ATERRAMENTO', 
                                  fontsize=16, fontweight='bold')
        
        self.ax_principal = plt.axes([0.1, 0.1, 0.8, 0.8])
        self.atualizar_visualizacao_principal()
    
    def atualizar_visualizacao_principal(self):
        """Atualiza a visualização principal"""
        self.ax_principal.clear()
        
        R = self.formula_dwight(self.rho, self.L, self.d)
        tipo_solo = self.obter_tipo_solo(self.rho)
        cor_solo = self.obter_cor_solo(self.rho)
        
        # Desenhar solo
        solo_depth = self.L + 2
        self.ax_principal.add_patch(Rectangle((-1, 0), 2, solo_depth, 
                                            facecolor=cor_solo, alpha=0.8))
        
        # Desenhar haste
        self.ax_principal.add_patch(Rectangle((-self.d/2, 0), self.d, self.L, 
                                            facecolor='#696969', edgecolor='black', linewidth=2))
        
        # Superfície
        self.ax_principal.axhline(y=0, color='#8B4513', linewidth=4)
        
        # Textos
        self.ax_principal.text(0, solo_depth - 0.5, f'TIPO: {tipo_solo.upper()}', 
                              ha='center', va='center', fontweight='bold', fontsize=12,
                              bbox=dict(boxstyle="round,pad=0.5", facecolor="white"))
        
        self.ax_principal.text(0, self.L/2, f'HASTE\n{self.L:.1f}m\n⌀{self.d*1000:.0f}mm', 
                              ha='center', va='center', color='white', fontweight='bold',
                              bbox=dict(boxstyle="round,pad=0.3", facecolor="black", alpha=0.7))
        
        self.ax_principal.text(0, -0.8, f'RESISTÊNCIA DE ATERRAMENTO: {R:.1f} Ω', 
                              ha='center', va='top', fontsize=14, fontweight='bold',
                              bbox=dict(boxstyle="round,pad=0.8", facecolor="yellow"))
        
        self.ax_principal.set_xlim(-1, 1)
        self.ax_principal.set_ylim(-1, solo_depth)
        self.ax_principal.set_aspect('equal')
        self.ax_principal.set_xlabel('Largura (m)', fontweight='bold')
        self.ax_principal.set_ylabel('Profundidade (m)', fontweight='bold')
        self.ax_principal.grid(True, alpha=0.3)
        
        plt.draw()
    
    def obter_cor_solo(self, rho):
        """Retorna cor baseada na resistividade"""
        if rho <= 100: return '#2E8B57'
        elif rho <= 500: return '#90EE90'
        elif rho <= 2000: return '#FFD700'
        else: return '#FF8C00'
    
    def mostrar_graficos(self, event):
        """Mostra gráficos separados em janelas individuais"""
        self.criar_grafico_comprimento()
        self.criar_grafico_diametro()
        self.criar_grafico_comparacao()
        self.atualizar_visualizacao_principal()
    
    def criar_grafico_comprimento(self):
        """Cria gráfico do efeito do comprimento"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        comprimentos = np.linspace(0.5, 10, 100)
        resistencias = [self.formula_dwight(self.rho, L, self.d) for L in comprimentos]
        
        ax.plot(comprimentos, resistencias, 'b-', linewidth=3, label='R = f(L)')
        
        R_atual = self.formula_dwight(self.rho, self.L, self.d)
        ax.plot(self.L, R_atual, 'ro', markersize=10, label=f'Atual: L={self.L:.1f}m, R={R_atual:.1f}Ω')
        
        ax.set_xlabel('Comprimento da Haste (m)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Resistência (Ω)', fontweight='bold', fontsize=12)
        ax.set_title('📏 EFEITO DO COMPRIMENTO DA HASTE NA RESISTÊNCIA', 
                    fontweight='bold', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
        
        ax.text(0.02, 0.98, f'ρ = {self.rho} Ω·m | d = {self.d*1000:.0f} mm', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))
        
        plt.tight_layout()
        plt.show(block=False)
    
    def criar_grafico_diametro(self):
        """Cria gráfico do efeito do diâmetro"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        diametros = np.linspace(0.005, 0.05, 100)
        resistencias = [self.formula_dwight(self.rho, self.L, d) for d in diametros]
        
        ax.plot([d * 1000 for d in diametros], resistencias, 'g-', linewidth=3, label='R = f(d)')
        
        R_atual = self.formula_dwight(self.rho, self.L, self.d)
        ax.plot(self.d * 1000, R_atual, 'ro', markersize=10, 
                label=f'Atual: d={self.d*1000:.0f}mm, R={R_atual:.1f}Ω')
        
        ax.set_xlabel('Diâmetro da Haste (mm)', fontweight='bold', fontsize=12)
        ax.set_ylabel('Resistência (Ω)', fontweight='bold', fontsize=12)
        ax.set_title('📐 EFEITO DO DIÂMETRO DA HASTE NA RESISTÊNCIA', 
                    fontweight='bold', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(bottom=0)
        
        ax.text(0.02, 0.98, f'ρ = {self.rho} Ω·m | L = {self.L:.1f} m', 
                transform=ax.transAxes, fontsize=10, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgreen"))
        
        plt.tight_layout()
        plt.show(block=False)
    
    def criar_grafico_comparacao(self):
        """Cria gráfico de comparação com solos típicos"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        solos = list(self.tipos_solo.keys())
        resistencias = []
        cores = ['#2E8B57', '#90EE90', '#FFD700', '#FF8C00']
        
        for i, solo in enumerate(solos):
            rho = self.tipos_solo[solo]
            R = self.formula_dwight(rho, self.L, self.d)
            resistencias.append(R)
        
        # Adicionar caso atual
        solos.append("SEU CASO")
        resistencias.append(self.formula_dwight(self.rho, self.L, self.d))
        cores.append('#FF4444')
        
        bars = ax.bar(solos, resistencias, color=cores, alpha=0.8, edgecolor='black')
        
        # Valores nas barras
        for bar, valor in zip(bars, resistencias):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(resistencias)*0.01,
                   f'{valor:.1f} Ω', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Resistência de Aterramento (Ω)', fontweight='bold', fontsize=12)
        ax.set_title('🏆 COMPARAÇÃO DA RESISTÊNCIA ENTRE DIFERENTES SOLOS', 
                    fontweight='bold', fontsize=14)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')
        
        ax.text(0.02, 0.98, f'L = {self.L:.1f} m | d = {self.d*1000:.0f} mm', 
                transform=ax.transAxes, fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))
        
        plt.tight_layout()
        plt.show(block=False)
    
    def mostrar(self):
        """Mostra todas as janelas"""
        plt.show()

# Executar a demonstração
if __name__ == "__main__":
    print("🎤 DEMONSTRAÇÃO INTERATIVA DE ATERRAMENTO - JANELAS SEPARADAS")
    print("=" * 70)
    print("\n🎯 COMO USAR:")
    print("1. Ajuste os parâmetros na janela 'CONTROLES'")
    print("2. Clique em '📈 Ver Gráficos' para abrir as visualizações")
    print("3. Cada gráfico abrirá em uma janela separada")
    print("4. Você pode mover e redimensionar as janelas livremente")
    print("\n📊 GRÁFICOS DISPONÍVEIS:")
    print("   • Visualização do sistema de aterramento")
    print("   • Efeito do comprimento da haste")
    print("   • Efeito do diâmetro da haste") 
    print("   • Comparação com solos típicos")
    print("\n" + "=" * 70)
    
    demo = DemonstracaoAterramentoSeparada()
    demo.mostrar()