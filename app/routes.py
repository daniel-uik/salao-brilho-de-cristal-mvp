from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import db
from .models import Cliente, Agendamento
import urllib.parse

main_bp = Blueprint('main', __name__)

DURACOES_SERVICOS = {
    'Corte': '30 min',
    'Escova': '40 min',
    'Manicure': '45 min',
    'Luzes': '2h 30 min',
    'Selagem': '2h 00 min'
}

def gerar_link_whatsapp(telefone, nome, servico, data, hora):
    msg = (
        f'Oi {nome}, tudo bem? Passando pra confirmar seu horário de {servico} '
        f'amanhã ({data}) às {hora} aqui no Salão Brilho de Cristal! '
        f'Se precisar remarcar, só me avisar por aqui. Até amanhã! - Maria'
    )
    return f'https://wa.me/55{telefone}?text={urllib.parse.quote(msg)}'

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
    telefone = ''.join(filter(str.isdigit, data.get('telefone', '')))
    data_atendimento = data.get('data_atendimento')
    horario = data.get('horario_inicio')
    servico = data.get('servico_nome')
    valor = float(data.get('valor_servico', 0.0))

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

    link_whatsapp = gerar_link_whatsapp(telefone, nome, servico, data_atendimento, horario)

    return jsonify({
        'sucesso': True,
        'agendamento_id': novo_agendamento.id,
        'link_whatsapp': link_whatsapp
    }), 201