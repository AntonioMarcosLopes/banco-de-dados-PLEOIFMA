from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Itens, Categorias
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///paleoifma.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    itens = Itens.query.all()
    return render_template('home.html', itens=itens)

@app.route('/registrar', methods=['GET', 'POST'])
def registar():
    categorias = Categorias.query.order_by(Categorias.nome).all()
    if request.method == 'POST':
        nome = request.form['nomeForm']
        especificacao = request.form['especificacaoForm']
        categoria_id = request.form['categoria_id']
        novo_item = Itens(
            nome=nome,
            especificacao=especificacao,
            categoria_id=categoria_id
        )
        db.session.add(novo_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('registar.html', categorias=categorias)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    item = Itens.query.get_or_404(id)
    categorias = Categorias.query.order_by(Categorias.nome).all()
    if request.method == 'POST':
        item.nome = request.form['nomeForm']
        item.especificacao = request.form['especificacaoForm']
        item.categoria_id = request.form['categoria_id']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template(
        'editar.html',
        item=item,
        categorias=categorias
    )


@app.route('/deletar/<int:id>')
def deletar(id):
    item = Itens.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Categorias.query.count() == 0:
            categorias = [
                Categorias(nome="Dinossauros"),
                Categorias(nome="Peixes"),
                Categorias(nome="Plantas Fósseis"),
                Categorias(nome="Pterossauros"),
                Categorias(nome="Crocodilomorfos"),
                Categorias(nome="Quelônios"),
                Categorias(nome="Invertebrados"),
                Categorias(nome="Icnofósseis"),
                Categorias(nome="Outros")
            ]
            db.session.add_all(categorias)
            db.session.commit()
    app.run(debug=True)