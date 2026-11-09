from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import db
from .models import Cliente, Agendamento
import urllib.parse

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main_bp.route('/dashboard')
def dashboard():
    data = request.args.get('data', '2026-11-20')
    agendamentos = Agendamento.query.filter_by(data_atendimento=data).all()
    total = sum(a.valor_servico for a in agendamentos if a.status in ['AGENDADO', 'CONCLUIDO'])
    return render_template('dashboard.html', data=data, agendamentos=agendamentos, total=total)

@main_bp.route('/api/agendar', methods=['POST'])
def criar_agendamento():
    data = request.json
    nome = data.get('nome')
    telefone = data.get('telefone')
    data_atendimento = data.get('data_atendimento')
    horario = data.get('horario_inicio')
    servico = data.get('servico_nome')
    valor = float(data.get('valor_servico', 0.0))

    # Validacao Anti-Overbooking
    existente = Agendamento.query.filter_by(
        data_atendimento=data_atendimento,
        horario_inicio=horario,
        status='AGENDADO'
    ).first()

    if existente:
        return jsonify({
            'erro': True,
            'mensagem': f'Horário das {horario} já ocupado por {existente.cliente.nome}. Selecione outro horário.'
        }), 400

    cliente = Cliente.query.filter_by(telefone=telefone).first()
    if not cliente:
        cliente = Cliente(nome=nome, telefone=telefone)
        db.session.add(cliente)
        db.session.commit()

    novo_agendamento = Agendamento(
        cliente_id=cliente.id,
        data_atendimento=data_atendimento,
        horario_inicio=horario,
        servico_nome=servico,
        valor_servico=valor
    )
    db.session.add(novo_agendamento)
    db.session.commit()

    # Link wa.me
    msg = f'Olá {nome}, seu agendamento de {servico} no Salão Brilho de Cristal está confirmado para {data_atendimento} às {horario}.'
    link_whatsapp = f'https://wa.me/55{telefone}?text={urllib.parse.quote(msg)}'

    return jsonify({
        'sucesso': True,
        'agendamento_id': novo_agendamento.id,
        'link_whatsapp': link_whatsapp
    }), 201
def gerar_link_whatsapp(telefone, nome, servico, data, hora):
    import urllib.parse
    texto = f'Ola {nome}, seu horario de {servico} no Salao Brilho de Cristal esta confirmado para {data} as {hora}.'
    return f'https://wa.me/55{telefone}?text={urllib.parse.quote(texto)}'
