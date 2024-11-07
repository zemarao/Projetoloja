from flask import Flask, render_template, request, redirect, url_for
import os
import xmltodict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ['DATABASE_URL']  # Heroku define esta variável automaticamente
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Modelo de Produto
class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    quantidade = Column(Integer)
    preco = Column(String)

# Cria a tabela se não existir
Base.metadata.create_all(engine)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Gerenciamento de Estoque
@app.route('/estoque')
def estoque():
    return render_template('estoque.html')

# Upload e processamento de XML para a seção Compras
@app.route('/estoque/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        # Verifica se um arquivo foi enviado
        if 'file' not in request.files:
            return "Nenhum arquivo enviado."
        file = request.files['file']

        # Processa o arquivo XML
        if file.filename.endswith('.xml'):
            data = xmltodict.parse(file.read())
            produtos = data['produtos']['produto']

            # Insere os produtos no banco de dados
            for p in produtos:
                produto = Produto(
                    nome=p['nome'],
                    quantidade=int(p['quantidade']),
                    preco=p['preco']
                )
                session.add(produto)
            session.commit()
            return "Produtos adicionados com sucesso ao estoque!"
        else:
            return "Formato de arquivo não suportado. Envie um arquivo XML."

    return render_template('compras.html')

# Sub-seções de Gerenciamento de Estoque
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
