import pulp

prob = pulp.LpProblem("Plano_de_Abastecimento", pulp.LpMinimize)

# Variaveis de decisao
x_BH_RJ = pulp.LpVariable('BH_para_RJ', lowBound=0, cat='Continuous')
x_BH_SP = pulp.LpVariable('BH_para_SP', lowBound=0, cat='Continuous')
x_RP_RJ = pulp.LpVariable('RP_para_RJ', lowBound=0, cat='Continuous')
x_RP_SP = pulp.LpVariable('RP_para_SP', lowBound=0, cat='Continuous')
x_SJC_RJ = pulp.LpVariable('SJC_para_RJ', lowBound=0, cat='Continuous')
x_SJC_SP = pulp.LpVariable('SJC_para_SP', lowBound=0, cat='Continuous')

# Funcao Objetivo
prob += (
    13 * x_BH_RJ + 25 * x_BH_SP +
    25 * x_RP_RJ + 16 * x_RP_SP +
    15 * x_SJC_RJ + 40 * x_SJC_SP
), "Custo_Total_Transporte"

# Restricoes de Capacidade / Oferta
prob += x_BH_RJ + x_BH_SP <= 70, "Oferta_Maxima_BH"
prob += x_RP_RJ + x_RP_SP <= 130, "Oferta_Maxima_RP" 
prob += x_SJC_RJ + x_SJC_SP <= 120, "Oferta_Maxima_SJC"

# Restricoes de Consumo / Demanda

prob += x_BH_RJ + x_RP_RJ + x_SJC_RJ == 180, "Demanda_RJ"
prob += x_BH_SP + x_RP_SP + x_SJC_SP == 140, "Demanda_SP"

prob.solve()

print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nPlano de Transporte (Toneladas):")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.0f} ton")

print(f"\nCusto Total Minimo: $ {pulp.value(prob.objective):.2f}")