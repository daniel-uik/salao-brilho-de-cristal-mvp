from . import db
from datetime import datetime

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    observacoes = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    agendamentos = db.relationship('Agendamento', backref='cliente', lazy=True)

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    data_atendimento = db.Column(db.String(10), nullable=False) # AAAA-MM-DD
    horario_inicio = db.Column(db.String(5), nullable=False)   # HH:MM
    servico_nome = db.Column(db.String(60), nullable=False)
    valor_servico = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='AGENDADO')
    lembrete_enviado = db.Column(db.Boolean, default=False)

    __table_args__ = (
        db.UniqueConstraint('data_atendimento', 'horario_inicio', name='uq_data_horario'),
    )