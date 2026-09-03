import pulp

prob = pulp.LpProblem("Estrategia_de_Investimento", pulp.LpMaximize)

# Variaveis de investimento em A (anos 1 a 4)
A1 = pulp.LpVariable('A1', lowBound=0, cat='Continuous')
A2 = pulp.LpVariable('A2', lowBound=0, cat='Continuous')
A3 = pulp.LpVariable('A3', lowBound=0, cat='Continuous')
A4 = pulp.LpVariable('A4', lowBound=0, cat='Continuous')

# Variaveis de investimento em B (anos 1 a 3)
B1 = pulp.LpVariable('B1', lowBound=0, cat='Continuous')
B2 = pulp.LpVariable('B2', lowBound=0, cat='Continuous')
B3 = pulp.LpVariable('B3', lowBound=0, cat='Continuous')

# Investimentos especificos em C e D
C2 = pulp.LpVariable('C2', lowBound=0, cat='Continuous')
D5 = pulp.LpVariable('D5', lowBound=0, cat='Continuous')

# Saldos em caixa não investidos (guardados de um ano para o outro)
S1 = pulp.LpVariable('Sobra_Ano1', lowBound=0, cat='Continuous')
S2 = pulp.LpVariable('Sobra_Ano2', lowBound=0, cat='Continuous')
S3 = pulp.LpVariable('Sobra_Ano3', lowBound=0, cat='Continuous')
S4 = pulp.LpVariable('Sobra_Ano4', lowBound=0, cat='Continuous')
S5 = pulp.LpVariable('Sobra_Ano5', lowBound=0, cat='Continuous')

# Funcao Objetivo: Total Acumulado no inicio do ano 6
prob += (
1.40 * A4 + 1.70 * B3 + 2.00 * C2 + 1.30 * D5 + S5
), "Total_Ano_6"

prob += A1 + B1 + S1 == 10000, "Balanco_Ano_1"
prob += A2 + B2 + C2 + S2 - S1 == 0, "Balanco_Ano_2"
prob += A3 + B3 + S3 - S2 - 1.40 * A1 == 0, "Balanco_Ano_3"
prob += A4 + S4 - S3 - 1.40 * A2 - 1.70 * B1 == 0, "Balanco_Ano_4"
prob += D5 + S5 - S4 - 1.40 * A3 - 1.70 * B2 == 0, "Balanco_Ano_5"

prob.solve()

print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nPlano de Investimento:")
for v in prob.variables():
    if v.value() and v.value() > 0:
        print(f"- {v.name}: $ {v.value():,.2f}")

print(f"\nMontante Maximo no Inicio do Ano 6: $ {pulp.value(prob.objective):,.2f}")