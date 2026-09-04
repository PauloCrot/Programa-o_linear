import pulp

prob = pulp.LpProblem("Planejamento_de_Estudo", pulp.LpMaximize)

# Variaveis de Decisao
x1 = pulp.LpVariable('Horas_D1', lowBound=10, upBound=20, cat='Continuous')
x2 = pulp.LpVariable('Horas_D2', lowBound=12.5, upBound=25, cat='Continuous')

# Funcao Objetivo: Maximizar a media ponderada das notas
prob += (3 * x1 + 5 * x2) / 8, "MediaPonderada"


prob += x1 + x2 <= 30, "Tempo_Maximo_Estudo"

prob.solve()

print(f"Status da Solucao {pulp.LpStatus[prob.status]}")
print(f"\nPlano de Estudo (Horas):")
for v in prob.variables():
    print(f"- {v.name}: {v.value():.2f}h")

n1 = 5 * x1.value()
n2 = 4 * x2.value()

print(f"\nNotas Finais Estimadas:")
print(f"- Disciplina D1: {n1:.1f} pontos")
print(f"- Disciplina D2: {n2:.1f} pontos")
print(f"\nMedia Ponderada Maxima: {pulp.value(prob.objective)}")