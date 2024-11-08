from flask import Flask, render_template, request, redirect, url_for
import os
import xmltodict
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# Função para processar o XML
def processar_xml(xml_data):
    data = xmltodict.parse(xml_data)

    # Extraindo informações do destinatário
    nome_destinatario = data['nfeProc']['NFe']['infNFe']['dest']['xNome']

    # Extraindo informações dos produtos
    produtos = []
    itens = data['nfeProc']['NFe']['infNFe']['det']
    if isinstance(itens, list):  # Vários produtos
        for item in itens:
            produtos.append(extrair_detalhes_produto(item))
    else:  # Apenas um produto
        produtos.append(extrair_detalhes_produto(itens))

    return nome_destinatario, produtos

# Função para extrair detalhes de um produto
def extrair_detalhes_produto(item):
    produto = item['prod']
    return {
        'Código do Produto': produto['cProd'],
        'Código EAN': produto['cEAN'],
        'Descrição do Produto': produto['xProd'],
        'Unidade Comercial': produto['uCom'],
        'Quantidade Comercial': produto['qCom'],
        'Valor Unitário Comercial': produto['vUnCom'],
        'Valor Total do Produto': produto['vProd'],
        'Valor do Desconto': produto.get('vDesc', '0.00'),
        'Indicador de Total': produto['indTot']
    }

# Rota para upload do XML e exibição de resultados
@app.route('/estoque/compras', methods=['GET', 'POST'])
def compras():
    if request.method == 'POST':
        # Verifica se um arquivo foi enviado
        if 'file' not in request.files or request.files['file'].filename == '':
            return "Nenhum arquivo enviado."

        file = request.files['file']
        if file.filename.endswith('.xml'):
            # Processa o XML enviado
            nome_destinatario, produtos = processar_xml(file.read())
            return render_template('compras.html', nome_destinatario=nome_destinatario, produtos=produtos)
        else:
            return "Formato de arquivo não suportado. Envie um arquivo XML."

    return render_template('compras.html', nome_destinatario=None, produtos=None)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
