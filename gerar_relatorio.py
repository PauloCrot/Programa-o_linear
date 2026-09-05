import os
import subprocess
import sys

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Relatório - Pesquisa Operacional</title>
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>
  body {
    font-family: "Segoe UI", Arial, sans-serif;
    line-height: 1.6;
    margin: 40px auto;
    max-width: 900px;
    color: #222;
  }
  .capa {
    text-align: center;
    padding: 100px 0;
    page-break-after: always;
  }
  .capa h1 { font-size: 28pt; margin-bottom: 10px; }
  .capa h2 { font-size: 18pt; color: #555; font-weight: normal; }
  .capa .info { margin-top: 150px; font-size: 14pt; line-height: 2; }
  
  .exercicio {
    page-break-after: always;
    padding-top: 20px;
  }
  .exercicio:last-child {
    page-break-after: avoid;
  }
  h1 { color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 8px; }
  h3 { color: #2b6cb0; margin-top: 20px; }
  ul { margin-left: 20px; }
  
  .solver-box {
    background: #f7fafc;
    border: 1px solid #cbd5e0;
    border-left: 5px solid #3182ce;
    padding: 15px;
    border-radius: 4px;
    margin-top: 25px;
  }
  .solver-box h4 {
    margin-top: 0;
    color: #2c5282;
    text-transform: uppercase;
    font-size: 11pt;
    letter-spacing: 0.5px;
  }
  pre {
    background: #edf2f7;
    padding: 12px;
    border-radius: 4px;
    font-family: "Consolas", monospace;
    font-size: 9.5pt;
    white-space: pre-wrap;
    margin: 0;
  }
  @media print {
    body { margin: 0; max-width: 100%; }
    .exercicio { page-break-after: always; }
  }
</style>
</head>
<body>

<div class="capa">
  <h1>Pesquisa Operacional</h1>
  <h2>Modelos Matemáticos e Soluções via Solver (PuLP)</h2>
  <div class="info">
    <p><strong>Universidade Federal de São Paulo (UNIFESP)</strong></p>
    <p>Resolução Computacional dos Exercícios 1 ao 12</p>
  </div>
</div>

{CONTEUDO}

</body>
</html>
"""

def decodificar_saida(bytes_data):
    """Tenta decodificar a saída do Windows com segurança contra erros de acentuação."""
    for enc in ["utf-8", "cp1252", "latin-1"]:
        try:
            return bytes_data.decode(enc)
        except UnicodeDecodeError:
            continue
    return bytes_data.decode("latin-1", errors="replace")

def markdown_simples_para_html(md_text):
    linhas = md_text.split('\n')
    html = []
    in_math_block = False
    in_list = False

    for linha in linhas:
        strip = linha.strip()
        
        if strip.startswith('$$'):
            if in_math_block:
                html.append('$$</div>')
                in_math_block = False
            else:
                html.append('<div style="text-align: center; margin: 15px 0;">$$')
                in_math_block = True
            continue
        elif in_math_block:
            html.append(linha)
            continue
            
        if strip.startswith('# '):
            html.append(f'<h1>{strip[2:]}</h1>')
        elif strip.startswith('### '):
            if in_list:
                html.append('</ul>')
                in_list = False
            html.append(f'<h3>{strip[4:]}</h3>')
        elif strip.startswith('* '):
            if not in_list:
                html.append('<ul>')
                in_list = True
            conteudo = strip[2:]
            conteudo = conteudo.replace('**', '<b>', 1).replace('**', '</b>', 1)
            html.append(f'<li>{conteudo}</li>')
        elif strip == '':
            if in_list:
                html.append('</ul>')
                in_list = False
        else:
            html.append(f'<p>{linha}</p>')

    if in_list:
        html.append('</ul>')
    return '\n'.join(html)

corpo_html = ""

# Força o ambiente Python a usar codificação compatível
env = dict(os.environ)
env["PYTHONIOENCODING"] = "utf-8"

for i in range(1, 13):
    num_str = f"{i:02d}"
    md_path = f"docs/ex{num_str}.md"
    py_path = f"Ex{num_str}.py"
    if not os.path.exists(py_path):
        py_path = f"ex{num_str}.py"

    print(f"Processando Exercício {num_str}...")

    # 1. Lê a modelagem matemática
    md_content = ""
    if os.path.exists(md_path):
        try:
            with open(md_path, "r", encoding="utf-8") as f:
                md_content = f.read()
        except UnicodeDecodeError:
            with open(md_path, "r", encoding="latin-1") as f:
                md_content = f.read()
    else:
        md_content = f"# Exercício {num_str}\nArquivo {md_path} não encontrado."

    html_exercicio = markdown_simples_para_html(md_content)

    # 2. Executa o script capturando bytes brutos para não quebrar no Windows
    saida_solver = ""
    if os.path.exists(py_path):
        try:
            res = subprocess.run([sys.executable, py_path], capture_output=True, env=env)
            texto_saida = decodificar_saida(res.stdout)
            
            linhas_saida = texto_saida.split('\n')
            inicio_util = 0
            for idx, l in enumerate(linhas_saida):
                # Encontra onde começa a resposta útil do script
                if "status" in l.lower() or "plano" in l.lower() or "valor" in l.lower():
                    inicio_util = idx
                    break
            saida_solver = '\n'.join(linhas_saida[inicio_util:]).strip()
        except Exception as e:
            saida_solver = f"Erro ao executar {py_path}: {e}"
    else:
        saida_solver = f"Script {py_path} não encontrado."

    # Junta o exercício no HTML
    bloco = f"""
    <div class="exercicio">
      {html_exercicio}
      <div class="solver-box">
        <h4>Solução Computacional (Solver PuLP)</h4>
        <pre>{saida_solver}</pre>
      </div>
    </div>
    """
    corpo_html += bloco

relatorio_final = HTML_TEMPLATE.replace("{CONTEUDO}", corpo_html)

with open("relatorio_final.html", "w", encoding="utf-8") as f:
    f.write(relatorio_final)

print("\nConcluído com sucesso! Abra o arquivo 'relatorio_final.html' no navegador e imprima como PDF (Ctrl + P).")