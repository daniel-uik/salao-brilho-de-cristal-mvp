import pytest
from app import create_app, db
from app.models import Cliente, Agendamento

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_criar_cliente_e_agendamento(app):
    with app.app_context():
        c = Cliente(nome='Carla Souza', telefone='11999998888')
        db.session.add(c)
        db.session.commit()

        a = Agendamento(
            cliente_id=c.id,
            data_atendimento='2026-11-20',
            horario_inicio='09:00',
            servico_nome='Corte & Escova',
            valor_servico=60.0
        )
        db.session.add(a)
        db.session.commit()

        assert a.id is not None
        assert a.cliente.nome == 'Carla Souza'
        assert a.status == 'AGENDADO'