import pulp

prob = pulp.LpProblem("Composicao_Producao", pulp.LpMaximize)

# Variaveis de decisao
x1 = pulp.LpVariable('Produto_1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Produto_2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Produto_3', lowBound=0, upBound=20, cat='Continuous')

# Funcao objetivo
prob += 30 * x1 + 12 * x2 + 15 * x3, "Lucro_total"

# Restricoes de capacidade das maquinas
prob += x1 * 9 + x2 * 3 + x3 * 5 <= 500, "Capacidade_maquina_A"
prob += x1 * 5 + x2 * 4 <= 350, "Capacidade_maquina_B"
prob += x1 * 3 + x3 * 2 <= 150, "Capacidade_maquina_C"

prob.solve()

print(f"Status da solucao: {pulp.LpStatus[prob.status]}")
print(f"\nPlano de Producao (Unidades/semana):")

for v in prob.variables():
    print(f"- {v.name}: {v.value():.2f}")

print(f"\nLucro Maximo $ {pulp.value(prob.objective):.2f}")