from db import db


class Categorias(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    itens = db.relationship(
        "Itens",
        back_populates="categoria",
        lazy=True
    )

    def __repr__(self):
        return f"<{self.nome}>"


class Itens(db.Model):
    __tablename__ = 'itens'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    especificacao = db.Column(db.String(255), nullable=False)

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id"),
        nullable=False
    )

    categoria = db.relationship(
        "Categorias",
        back_populates="itens"
    )

    def __repr__(self):
        return f"<{self.nome}>"