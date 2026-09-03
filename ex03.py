import pulp

prob = pulp.LpProblem("Composicao_de_Producao", pulp.LpMaximize)

x1 = pulp.LpVariable('Produto_1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Produto_2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Produto_3', lowBound=0, cat='Continuous')
x4 = pulp.LpVariable('Produto_4', lowBound=0, cat='Continuous')

# variaveis de decisao
prob += 0 * x1 + 10 * x2 + 0 * x3 - 5 * x4, "Lucro_Total"

# Restriçoes de horas disponiveis nas maquinas
prob += 2 * x1 + 3 * x2 + 4 * x3 + 2 * x4 <= 500, "Horas_M1"
prob += 3 * x1 + 2 * x2 + 1 * x3 + 2 * x4 <= 380, "Horas_M2"

prob.solve()

print(f"Status da Solucão: {pulp.LpStatus[prob.status]}")
print(f"\nPlano de Producao (Unidades):")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.2f}")

print(f"\nLucro Liquido Máximo $ {pulp.value(prob.objective):.2f}")