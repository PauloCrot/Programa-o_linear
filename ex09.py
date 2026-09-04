import pulp

prob = pulp.LpProblem("Escala_funcionarios", pulp.LpMinimize)

x1 = pulp.LpVariable('Turno_02_06', lowBound=0, cat='Integer')
x2 = pulp.LpVariable('Turno_06_10', lowBound=0, cat='Integer')
x3 = pulp.LpVariable('Turno_10_14', lowBound=0, cat='Integer')
x4 = pulp.LpVariable('Turno_14_18', lowBound=0, cat='Integer')
x5 = pulp.LpVariable('Turno_18_22', lowBound=0, cat='Integer')
x6 = pulp.LpVariable('Turno_22_02', lowBound=0, cat='Integer')

# Funcao Objetivo: Minimizar o total de funcionarios
prob += x1 + x2 + x3 + x4 + x5 + x6, "Total_Funcionarios"

# Restricoes: A soma dos funcionarios que iniciaram no turno atual
# com os que iniciaram no turno anterior deve atender à demanda mínima

prob += x6 + x1 >= 4, "Demanda_02_06"
prob += x1 + x2 >= 8, "Demanda_06_10"
prob += x2 + x3 >= 10, "Demanda_10_14"
prob += x3 + x4 >= 7,  "Demanda_14_18"
prob += x4 + x5 >= 12, "Demanda_18_22"
prob += x5 + x6 >= 4,  "Demanda_22_02"

# Executa o solver
prob.solve()

# Exibe os resultados
print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print("\nEscala de Trabalho (Funcionarios iniciando o turno):")
for v in prob.variables():
    print(f"- {v.name}: {int(v.value())}")

print(f"\nTotal Minimo de Funcionarios: {int(pulp.value(prob.objective))}")