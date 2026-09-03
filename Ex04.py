import pulp

prob = pulp.LpProblem("Compra_de_Avioes", pulp.LpMaximize)

x1 = pulp.LpVariable('PequenoCurso', lowBound=0, cat='Integer')
x2 = pulp.LpVariable('MedioCurso', lowBound=0, cat='Integer')
x3 = pulp.LpVariable('LongoCurso', lowBound=0, cat='Integer')

prob += 0.23 * x1 + 0.30 * x2 + 0.42 * x3, "LucroTotal"

prob += 3.5 * x1 + 5.0 * x2 + 6.7 * x3 <= 150, "Orcamento_Maximo"
prob += x1 + x2 + x3 <= 30, "Capacidade_piloto"
prob += 3 * x1 + 4 * x2 + 5 * x3 <= 120, "Capacidade_Manutencao"

prob.solve()

print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nPlano de Compra (Quantidade de Avioes):")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.0f}")

print(f"\nLucro TotalAnual Maximo: $ {pulp.value(prob.objective):.2f} Milhoes")