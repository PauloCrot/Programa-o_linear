import pulp

prob = pulp.LpProblem("Uso_Capacidade_Ociosa", pulp.LpMaximize)

x1G = pulp.LpVariable('F1_Grande', lowBound=0, cat='Continuous')
x1M = pulp.LpVariable('F1_Medio', lowBound=0, cat='Continuous')
x1P = pulp.LpVariable('F1_pequeno', lowBound=0, cat='Continuous')

x2G = pulp.LpVariable('F2_Grande', lowBound=0, cat='Continuous')
x2M = pulp.LpVariable('F2_Medio', lowBound=0, cat='Continuous')
x2P = pulp.LpVariable('F2_Pequeno', lowBound=0, cat='Continuous')

x3G = pulp.LpVariable('F3_Grande', lowBound=0, cat='Continuous')
x3M = pulp.LpVariable('F3_Medio', lowBound=0, cat='Continuous')
x3P = pulp.LpVariable('F3_Pequeno', lowBound=0, cat='Continuous')

# Função Objetivo (Maximizar lucro)
prob += 12 * (x1G + x2G + x3G) + 10 * (x1M + x2M + x3M) + 9 * (x1P + x2P + x3P), "Lucro_total"
# Restricoes de capacidade de producao
prob += x1G + x1M + x1P <= 500, "Capacidade_Prod_F1"
prob += x2G + x2M + x2P <= 600, "Capacidade_Prod_F2"
prob += x3G + x3M + x3P <= 300, "Capacidade_Prod_F3"

# Restricoes de Area de estocagem
prob += 20 * x1G + 15 * x1M + 12 * x1P <= 9000, "Estocagem_F1"
prob += 20 * x2G + 15 * x2M + 12 * x2P <= 8000, "Estocagem_F2"
prob += 20 * x3G + 15 * x3M + 12 * x3P <= 3500, "Estocagem_F3"

# Restricoes de Demanda
prob += x1G + x2G + x3G <= 600, "Demanda_Grande"
prob += x1M + x2M + x3M <= 800, "Demanda_Media"
prob += x1P + x2P + x3P <= 500, "Demanda_pequena"

# Restricoes de Uniformidade

prob += 6 * (x1G + x1M + x1P) - 5 * (x2G + x2M + x2P) == 0, "Uniformidade_F1_F2"
prob += 1 * (x2G + x2M + x2P) - 2 * (x3G + x3M + x3P) == 0, "Uniformidade_F2_F3"

prob.solve()

print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nPlano de Producao (Unidades):")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.2f}")

print(f"\nLucro Maximo: $ {pulp.value(prob.objective):.2f}")