from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255))
    funcao = db.Column(db.String(255))


class User(BaseModel):
    username: str
    password: str

class ArduinoData(BaseModel):
    timestamp: datetime
    value: float


class Dado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date)
    hora = db.Column(db.Time)
    intervalo = db.Column(db.Integer)
    dados_json = db.Column(db.Text)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref='dados')

