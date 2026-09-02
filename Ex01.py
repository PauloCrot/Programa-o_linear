import pulp

prob = pulp.LpProblem("Composicao_de_Racao", pulp.LpMinimize)

x1 = pulp.LpVariable('Cevada', lowBound=0, cat='Continuous')
x2 = pulp.LpVariable('Aveia', lowBound=0, cat='Continuous')
x3 = pulp.LpVariable('Soja', lowBound=0, cat='Continuous')
x4 = pulp.LpVariable('Milho', lowBound=0, cat='Continuous')

#Função objetivo
prob += 30 * x1 + 48 * x2 + 44 * x3 + 56 * x4, "Custo_Total"

#Restrições
prob += x1 + x2 + x3 + x4 == 10000, "Peso_total"
prob += (
    6.9 * x1 + 8.5 * x2 + 9.0 * x3 + 27.1 * x4 >= 150000,
    "Proteina_Minima",
) 
prob += (
    6 * x1 + 11 * x2 + 11 * x3 + 14 * x4 >= 80000,
    "Fibra_Minima",
)
prob += (
    1760 * x1 + 1700 * x2 + 1056 * x3 + 1400 * x4 >= 11000000,
    "Calorias_Minimas",
)
prob += (
    1760 * x1 + 1700 * x2 + 1056 * x3 + 1400 * x4 <= 22500000,
    "Calorias_Maximas",
)
prob += x4 >= 2000, "Milho_Minimo"
prob += x3 <= 1200, "Soja_Maxima"

prob.solve()

print(f"Status Da Solução: {pulp.LpStatus[prob.status]}")
print("\nQuantidades ideais")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.2f} kg")

print(f"\nCusto Total Minimo: R$ {pulp.value(prob.objective):.2f}")