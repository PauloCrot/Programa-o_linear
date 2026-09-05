import pulp

prob = pulp.LpProblem("ComposicaoProdutosAgricolas", pulp.LpMinimize)

# Lista de indices
ingredientes = ['Milho', 'Calcario', 'Soja', 'Farinha']
produtos = ['Gado', 'Ovelhas', 'Galinhas']

# custos por kg
custos = {'Milho': 0.20, 'Calcario': 0.12, 'Soja': 0.24, 'Farinha': 0.12}

# Disponibilidade de ingredientes (kg)
disp = {'Milho': 6000, 'Calcario': 10000, 'Soja': 4000, 'Farinha': 5000}

# Demanda de Producao
demanda = {'Gado': 10000, 'Ovelhas': 6000, 'Galinhas': 8000}

# Composicao Nutricional

nutrientes = {
    'Milho': {'Vit': 8, 'Prot': 10, 'Calc': 6, 'Gord': 8},
    'Calcario': {'Vit': 6, 'Prot': 5, 'Calc': 10, 'Gord': 6},
    'Soja': {'Vit': 10, 'Prot': 12, 'Calc': 6, 'Gord': 6},
    'Farinha': {'Vit': 4, 'Prot': 8, 'Calc': 6, 'Gord': 9}
}

# Restricoes de Nutrientes por kg de Produto

reqs = {
    'Gado':     {'Vit': (6, None), 'Prot': (6, None), 'Calc': (7, None), 'Gord': (4, 8)},
    'Ovelhas': {'Vit': (6, None), 'Prot': (6, None), 'Calc': (6, None), 'Gord': (4, 8)},
    'Galinhas': {'Vit': (4, 6),    'Prot': (6, None), 'Calc': (6, None), 'Gord': (4, 8)} 
}

x = pulp.LpVariable.dicts("X", (ingredientes, produtos), lowBound=0, cat='Continuous')

# Funcao Objetivo: Minimizar o custo total
prob += pulp.lpSum([custos[i] *  x[i][j] for i in ingredientes for j in produtos]), "Custo_Total"

# 1. Restricoes de demanda de producao
for j in produtos:
    prob += pulp.lpSum([x[i][j] for i in ingredientes]) == demanda[j], f"Demanda_{j}"

# 2. Restrições de Disponibilidade de Matéria-prima
for i in ingredientes:
    prob += pulp.lpSum([x[i][j] for j in produtos]) <= disp[i], f"Disponibilidade_{i}"

# Restricoes nutricionais
for j in produtos: 
    for n in ['Vit', 'Prot', 'Calc', 'Gord']: 
        min_req, max_req = reqs[j][n]
        if min_req is not None:
            prob += pulp.lpSum ([x[i][j] * nutrientes[i][n]for i in ingredientes]) >= min_req * demanda[j], f"Min_{n}{j}"
        if max_req is not None:
            prob += pulp.lpSum([x[i][j] * nutrientes[i][n] for i in ingredientes]) <= max_req * demanda[j], f"Max_{n}_{j}"

prob.solve()

# Exibição
print(f"Status da Solucao: {pulp.LpStatus[prob.status]}")
print(f"Custo Minimo Total: $ {pulp.value(prob.objective):,.2f}\n")

print("Matriz de Receitas (kg do Ingrediente no Produto):")
for j in produtos:
    print(f"\nRação para {j}:")
    for i in ingredientes:
        val = pulp.value(x[i][j])
        if val > 0:
            print(f"- {i}: {val:,.2f} kg")