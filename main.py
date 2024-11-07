from flask import Flask, render_template
import os

app = Flask(__name__)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Gerenciamento de Estoque
@app.route('/estoque')
def estoque():
    return render_template('estoque.html')

# Sub-seções de Gerenciamento de Estoque
@app.route('/estoque/compras')
def compras():
    return "<h2>Compras</h2><p>Conteúdo sobre compras.</p>"

@app.route('/estoque/transferencia')
def transferencia():
    return "<h2>Transferência de Estoque</h2><p>Conteúdo sobre transferência de estoque.</p>"

@app.route('/estoque/consignados')
def consignados():
    return "<h2>Consignados</h2><p>Conteúdo sobre consignados.</p>"

# Outras seções (Vendas, Clientes, etc.) continuam como antes
@app.route('/vendas')
def vendas():
    return "<h2>Vendas</h2><p>Conteúdo sobre vendas.</p>"

@app.route('/clientes')
def clientes():
    return "<h2>Clientes</h2><p>Conteúdo sobre clientes.</p>"

@app.route('/fornecedores')
def fornecedores():
    return "<h2>Fornecedores</h2><p>Conteúdo sobre fornecedores.</p>"

@app.route('/colaboradores')
def colaboradores():
    return "<h2>Colaboradores</h2><p>Conteúdo sobre colaboradores.</p>"

@app.route('/relatorios')
def relatorios():
    return "<h2>Relatórios</h2><p>Conteúdo sobre relatórios.</p>"

@app.route('/configuracoes')
def configuracoes():
    return "<h2>Configurações</h2><p>Conteúdo sobre configurações.</p>"

# Executa a aplicação
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
