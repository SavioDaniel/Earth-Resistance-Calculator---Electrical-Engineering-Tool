import math

print("=" * 50)
print("CALCULADORA DE RESISTÊNCIA DE ATERRAMENTO")
print("=" * 50)

print("\nSelecione o tipo de eletrodo de aterramento:")
print("1 - Haste vertical única")
print("2 - Múltiplas hastes em linha")
print("3 - Condutor horizontal enterrado")
print("4 - Aterramento em malha")

opcao = input("\nDigite o número da opção desejada: ")

# Constante - Resistividade do solo (Ω.m)
resistividade_solo = float(input("\nDigite a resistividade do solo (Ω.m): "))

def haste_vertical_unica():
    print("\n--- Haste Vertical Única ---")
    comprimento = float(input("Comprimento da haste (m): "))
    diametro = float(input("Diâmetro da haste (m): "))
    
    # Fórmula CORRETA para haste vertical (IEEE Std 142)
    R = (resistividade_solo / (2 * math.pi * comprimento)) * (math.log((4 * comprimento) / diametro) - 1)
    
    return R, comprimento, diametro

def multiplas_hastes_linha():
    print("\n--- Múltiplas Hastes em Linha ---")
    n_hastes = int(input("Número de hastes: "))
    comprimento = float(input("Comprimento de cada haste (m): "))
    diametro = float(input("Diâmetro das hastes (m): "))
    espacamento = float(input("Espaçamento entre hastes (m): "))
    
    # Resistência de uma haste isolada
    R_uma_haste = (resistividade_solo / (2 * math.pi * comprimento)) * (math.log((4 * comprimento) / diametro) - 1)
    
    # Fator de utilização mais preciso
    if n_hastes == 2:
        fator_utilizacao = 0.85
    elif n_hastes == 3:
        fator_utilizacao = 0.75
    elif n_hastes == 4:
        fator_utilizacao = 0.65
    elif n_hastes == 5:
        fator_utilizacao = 0.60
    elif n_hastes == 6:
        fator_utilizacao = 0.55
    elif n_hastes == 8:
        fator_utilizacao = 0.50
    elif n_hastes == 10:
        fator_utilizacao = 0.45
    else:
        fator_utilizacao = 0.40
    
    R_total = R_uma_haste / (n_hastes * fator_utilizacao)
    
    return R_total, n_hastes, comprimento, diametro, espacamento, R_uma_haste, fator_utilizacao

def condutor_horizontal():
    print("\n--- Condutor Horizontal ---")
    comprimento = float(input("Comprimento do condutor (m): "))
    diametro = float(input("Diâmetro do condutor (m): "))
    profundidade = float(input("Profundidade de enterramento (m): "))
    
    # Fórmula de Laurent para condutor horizontal
    R = (resistividade_solo / (math.pi * comprimento)) * (
        math.log((2 * comprimento) / math.sqrt(diametro * profundidade)) + 0.5
    )
    
    return R, comprimento, diametro, profundidade

def malha_aterramento():
    print("\n--- Malha de Aterramento ---")
    area = float(input("Área da malha (m²): "))
    comprimento_total = float(input("Comprimento total dos condutores (m): "))
    profundidade = float(input("Profundidade da malha (m): "))
    
    # Fórmula de Schwarz para malha
    R = resistividade_solo * (1/comprimento_total + 1/math.sqrt(20*area)) * (1 + 1/(1 + profundidade * math.sqrt(area/10)))
    
    return R, area, comprimento_total, profundidade

# Execução do cálculo baseado na opção escolhida
try:
    resistencia = 0
    config = ""
    detalhes = {}
    
    if opcao == "1":
        resistencia, comprimento, diametro = haste_vertical_unica()
        config = "Haste vertical única"
        detalhes = {"comprimento": comprimento, "diametro": diametro}
    elif opcao == "2":
        resistencia, n_hastes, comprimento, diametro, espacamento, R_uma_haste, fator_utilizacao = multiplas_hastes_linha()
        config = "Múltiplas hastes em linha"
        detalhes = {"n_hastes": n_hastes, "comprimento": comprimento, "diametro": diametro, "espacamento": espacamento, "R_uma_haste": R_uma_haste, "fator_utilizacao": fator_utilizacao}
    elif opcao == "3":
        resistencia, comprimento, diametro, profundidade = condutor_horizontal()
        config = "Condutor horizontal"
        detalhes = {"comprimento": comprimento, "diametro": diametro, "profundidade": profundidade}
    elif opcao == "4":
        resistencia, area, comprimento_total, profundidade = malha_aterramento()
        config = "Malha de aterramento"
        detalhes = {"area": area, "comprimento_total": comprimento_total, "profundidade": profundidade}
    else:
        print("Opção inválida!")
        exit()
    
    print("\n" + "=" * 50)
    print("RESULTADO DO CÁLCULO")
    print("=" * 50)
    print(f"Configuração: {config}")
    print(f"Resistividade do solo: {resistividade_solo} Ω.m")
    print(f"Resistência de aterramento calculada: {resistencia:.2f} Ω")
    
    # Verificação conforme norma
    print(f"\n--- ANÁLISE CONFORME NORMAS ---")
    
    if resistencia <= 1.0:
        print("✅ ATENDE: Sistemas de equipamentos sensíveis (≤ 1 Ω)")
        status = "ATENDE"
    elif resistencia <= 5.0:
        print("✅ ATENDE: Sistemas de telecomunicações (≤ 5 Ω)")
        status = "ATENDE"
    elif resistencia <= 10.0:
        print("✅ ATENDE: Sistemas de potência e para-raios (≤ 10 Ω)")
        status = "ATENDE"
    else:
        print("❌ NÃO ATENDE: Resistência acima dos limites normativos (> 10 Ω)")
        status = "NÃO ATENDE"
    
    # Mostrar cálculo detalhado
    print(f"\n--- DETALHES DO CÁLCULO ---")
    if opcao == "1":
        L = detalhes["comprimento"]
        d = detalhes["diametro"]
        parte1 = resistividade_solo / (2 * math.pi * L)
        parte2 = math.log((4 * L) / d) - 1
        print(f"Fórmula: R = (ρ / (2πL)) × [ln(4L/d) - 1]")
        print(f"R = ({resistividade_solo} / (2×π×{L})) × [ln(4×{L}/{d}) - 1]")
        print(f"R = ({resistividade_solo} / {2*math.pi*L:.2f}) × [ln({4*L/d:.1f}) - 1]")
        print(f"R = {parte1:.2f} × [{math.log(4*L/d):.2f} - 1]")
        print(f"R = {parte1:.2f} × {parte2:.2f}")
        print(f"R = {resistencia:.2f} Ω")
    
    elif opcao == "2":
        L = detalhes["comprimento"]
        d = detalhes["diametro"]
        n = detalhes["n_hastes"]
        R_uma = detalhes["R_uma_haste"]
        fator = detalhes["fator_utilizacao"]
        
        print(f"1. Resistência de UMA haste:")
        print(f"   R_uma = (ρ / (2πL)) × [ln(4L/d) - 1]")
        print(f"   R_uma = ({resistividade_solo} / (2×π×{L})) × [ln(4×{L}/{d}) - 1]")
        print(f"   R_uma = {R_uma:.2f} Ω")
        
        print(f"\n2. Fator de utilização para {n} hastes: η = {fator}")
        
        print(f"\n3. Resistência TOTAL:")
        print(f"   R_total = R_uma / (n × η)")
        print(f"   R_total = {R_uma:.2f} / ({n} × {fator})")
        print(f"   R_total = {R_uma:.2f} / {n * fator:.2f}")
        print(f"   R_total = {resistencia:.2f} Ω")
    
    # Sugestões de melhoria
    if resistencia > 10.0:
        print(f"\n--- SUGESTÕES PARA REDUZIR A RESISTÊNCIA ---")
        if opcao == "1":
            print(f"• Adicionar mais hastes em paralelo")
            print(f"• Aumentar comprimento da haste para 4-6m")
            print(f"• Usar haste de maior diâmetro")
        elif opcao == "2":
            print(f"• Aumentar número de hastes para {detalhes['n_hastes'] + 2}")
            print(f"• Aumentar comprimento das hastes para 3-4m")
            print(f"• Reduzir espaçamento entre hastes para 2.0m")
        elif opcao == "3":
            print(f"• Aumentar comprimento do condutor para {detalhes['comprimento'] * 1.5:.1f}m")
            print(f"• Enterrar em maior profundidade (0.8-1.0m)")
            print(f"• Adicionar hastes verticais nos extremos")
        elif opcao == "4":
            print(f"• Aumentar área da malha para {detalhes['area'] * 1.5:.1f}m²")
            print(f"• Aumentar comprimento dos condutores")
            print(f"• Adicionar hastes verticais nos cantos")
        
        print(f"• Aplicar tratamento químico no solo (eletrodos químicos)")
        print(f"• Usar aterramento profundo (hastes de 6-12m)")
        print(f"• Considerar uso de composto eletrocondutor")
    
    # Mostrar próximo passo para atingir ≤ 10 Ω
    if resistencia > 10.0 and opcao == "2":
        n_minimo = math.ceil(detalhes['R_uma_haste'] / (10 * detalhes['fator_utilizacao']))
        print(f"\n--- PARA ATINGIR ≤ 10 Ω ---")
        print(f"Número mínimo de hastes necessárias: {n_minimo}")
        print(f"Resistência estimada com {n_minimo} hastes: {detalhes['R_uma_haste']/(n_minimo * detalhes['fator_utilizacao']):.2f} Ω")
    
except ValueError:
    print("Erro: Digite valores numéricos válidos!")
except Exception as e:
    print(f"Erro inesperado: {e}")

'''print("\n" + "=" * 50)
print("Observações importantes:")
print("- Cálculo para projeto preliminar")
print("- Validação requer medição in loco")
print("- Consulte NBR 5419 e IEEE Std 80")
print("=" * 50)'''