# ✂️ Salão Brilho de Cristal - Sistema de Gestão e Agendamento (MVP)

> **Projeto de Software – Experiência Prática III**  
> Desenvolvido para o parceiro comunitário **Salão Brilho de Cristal (MEI)**, localizado no bairro de Cidade Tiradentes, São Paulo/SP.  
> Alinhado ao **ODS 8 da ONU (Trabalho Decente e Crescimento Econômico - Meta 8.3)**.

---

## 📌 1. Visão Geral do Produto
O **Salão Brilho de Cristal** é uma aplicação web responsiva (PWA Mobile-First) construída com **Python, Flask e SQLAlchemy**, projetada sob medida para a gestora **Maria**. O sistema substitui o caderno analógico de agendamentos por uma grade diária digital intuitiva, resolvendo dois gargalos centrais:
1. **Validação Anti-Overbooking:** Bloqueio técnico contra agendamentos duplos no mesmo horário.
2. **Disparo de Confirmação via WhatsApp:** Botão de um toque que aciona o protocolo `wa.me` com mensagens de véspera personalizadas a custo zero, erradicando os *no-shows* (faltas sem aviso prévio).

---

## 🛠️ 2. Arquitetura e Pilha Tecnológica
- **Linguagem Principal:** Python 3.12 LTS
- **Padrão Arquitetural:** Model-View-Controller (MVC) em 3 Camadas
- **Microframework Web:** Flask 3.0.3
- **ORM / Persistência:** SQLAlchemy 2.0 (SQLite local / PostgreSQL em produção)
- **Front-end:** HTML5 semântico, CSS3 e Bootstrap 5 (área de toque mínima de 48px e alto contraste WCAG 2.1 AA)
- **Testes Automatizados:** Pytest (Unitários e de Integração)
- **Integração Contínua (CI):** GitHub Actions

---

## 🧪 3. Como Executar os Testes Automatizados
`ash
# Instalar dependências
pip install -r requirements.txt

# Executar suite completa de testes
pytest -v
`

---

## 🚀 4. Como Executar a Aplicação Localmente
`ash
python run.py
`
Acesse a aplicação no navegador móvel em: `http://localhost:5000`