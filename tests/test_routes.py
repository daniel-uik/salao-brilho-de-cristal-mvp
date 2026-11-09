import pytest
from app import create_app, db

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

def test_anti_overbooking_bloqueio(client, app):
    payload = {
        'nome': 'Carla Souza',
        'telefone': '11999998888',
        'data_atendimento': '2026-11-20',
        'horario_inicio': '09:00',
        'servico_nome': 'Corte',
        'valor_servico': 50.0
    }
    # Primeiro agendamento -> sucesso
    res1 = client.post('/api/agendar', json=payload)
    assert res1.status_code == 201

    # Segundo agendamento no mesmo horario -> bloqueio 400
    res2 = client.post('/api/agendar', json=payload)
    assert res2.status_code == 400
    assert 'já ocupado' in res2.get_json()['mensagem']