import pulp

prob = pulp.LpProblem("Composicao", pulp.LpMinimize)

# Variaveis de decisao
x1 = pulp.LpVariable('Minerio_1', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Minerio_2', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Minerio_3', lowBound=0, cat='Continuous')
x4 = pulp.LpVariable('Minerio_4', lowBound=0, cat='Continuous')
x5 = pulp.LpVariable('Minerio_5', lowBound=0, cat='Continuous')

# Funcao Objetivo
prob += 8.5 * x1 + 6.0 * x2 + 8.9 * x3 + 5.7 * x4 + 8.8 * x5, "CustoTotal"

# Restricoes de composicao da liga

prob += 30 * x1 + 10 * x2 + 50 * x3 + 10 * x4 + 50 * x5 == 30, "Porcentagem_Chumbo"
prob += 60 * x1 + 20 * x2 + 20 * x3 + 10 * x4 + 10 * x5 == 20, "Porcentagem_Zinco"
prob += 10 * x1 + 70 * x2 + 30 * x3 + 80 * x4 + 40 * x5 == 50, "Porcentagem_Estanho"

prob += x1 + x2 + x3 + x4 + x5 == 1, "Soma_Proporcoes"

prob.solve()

print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nProporcoes da mistura:")

for v in prob.variables():
    print(f"- {v.name}: {v.value() * 100:.2f}%")

print(f"\nCusto Minimo: $ {pulp.value(prob.objective):.2f} / kg")