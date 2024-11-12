from flask import Flask, render_template, request, redirect, url_for
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from processa_xml import extrair_informacoes

app = Flask(__name__)

# Configuração do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///produtos.db')
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

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

# Sub-seções de Gerenciamento de Estoque
@app.route('/estoque/compras')
def compras():
    return render_template('compras.html')

# Rota para Enviar XML
@app.route('/estoque/compras/enviar', methods=['GET', 'POST'])
def enviar_xml():
    if request.method == 'POST':
        xml_content = request.form.get('xml_textarea')  # Captura o texto da caixa de texto
        if not xml_content:
            return "Nenhum conteúdo foi enviado para processamento."

        try:
            # Processa o XML usando a função importada
            emitente, produtos = extrair_informacoes(xml_content)

            # Renderiza a página de resultado com as informações
            return render_template('resultado.html', emitente=emitente, produtos=produtos)

        except ValueError as e:
            # Mostra o erro para o usuário
            return f"Erro ao processar o XML: {e}"

    return render_template('enviar_xml.html')


# Outras seções (Clientes, Fornecedores, etc.)
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
