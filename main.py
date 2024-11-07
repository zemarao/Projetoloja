from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista simples para simular uma base de dados temporária (em desenvolvimento)
produtos = []


@app.route('/')
def index():
    return render_template('index.html', produtos=produtos)


@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form.get('nome')
    preco = request.form.get('preco')
    if nome and preco:
        produtos.append({'nome': nome, 'preco': preco})
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
