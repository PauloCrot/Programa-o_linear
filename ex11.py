import pulp

prob = pulp.LpProblem("empreendimento", pulp.LpMinimize)

xI = pulp.LpVariable("programa", lowBound=0, cat='Continuous')
x1 = pulp.LpVariable("divulgacao1", lowBound=0, cat='Continuous')
x2 = pulp.LpVariable("divulgacao2", lowBound=0, cat='Continuous')

prob += xI + x1 + x2, "CustoTotal"

# Restricoes de Meta de vendas
prob += 3 * xI + 4 * x1 >= 30, "MetaVendasP1"
prob += 3 * xI + 10 * x2 >= 30, "MetaVendasP2"

# Restricao de orcamento
prob += xI + x1 + x2 <= 10, "OrcamentoMaximo"

prob.solve()
print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nPlano de Investimento Ideal:")
for v in prob.variables():
    print(f"- {v.name}: $ {v.value() * 1000:,.2f}")

print(f"\nCusto Minimo Total: $ {pulp.value(prob.objective) * 1000:,.2f}")