# BarberPro - Micro SaaS para Barbearia

Sistema completo de gestao para barbearias com multi-tenant, dashboard, agendamentos, clientes, barbeiros, servicos e pagamentos.

## Tecnologias

- **Backend:** Flask 3 + SQLAlchemy + Flask-Login
- **Frontend:** Jinja2 + TailwindCSS (CDN) + Chart.js
- **Banco:** SQLite (dev) / PostgreSQL (prod)
- **Deploy:** Gunicorn + Docker

## Requisitos

- Python 3.10+
- pip

## Instalacao e Execucao Local

```bash
# 1. Copiar variaveis de ambiente
cp .env.example .env

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Rodar o servidor (SQLite, zero configuracao)
python run.py
```

Abra `http://localhost:5000` no navegador.

## Producao com Docker

```bash
docker compose up -d
```

Disponivel em `http://localhost:8000`

## Producao com Gunicorn (sem Docker)

```bash
cp .env.example .env
# Edite DATABASE_URL para PostgreSQL
FLASK_ENV=production flask db upgrade
gunicorn -c gunicorn.conf.py run:app
```

## Variaveis de Ambiente

| Variavel | Descricao | Default |
|---|---|---|
| SECRET_KEY | Chave secreta para sessoes | (nao use o padrao em prod) |
| DATABASE_URL | URL do banco de dados | sqlite:///barbearia.db |
| FLASK_ENV | Ambiente (development/production) | development |
| SESSION_COOKIE_SECURE | Flag secure nos cookies | False |

## Endpoints da API

| Metodo | Rota | Descricao |
|---|---|---|
| POST | /api/login | Autenticacao |
| GET | /api/appointments | Listar agendamentos |
| POST | /api/appointments | Criar agendamento |
| DELETE | /api/appointments/<id> | Cancelar agendamento |
| GET | /api/clients | Listar clientes |
| POST | /api/clients | Criar cliente |

## Estrutura do Projeto

```
app/
  models/          # SQLAlchemy models
  routes/          # Controllers/blueprints
  services/        # Regras de negocio
  utils/           # Helpers, decorators, seguranca
  templates/       # HTML Jinja2
  config.py        # Configuracoes por ambiente
  extensions.py    # Extensões Flask
  __init__.py      # Factory create_app
run.py             # Entry point
```

## Seguranca

- Senhas com bcrypt (werkzeug)
- Protecao contra brute force (bloqueio apos 5 tentativas)
- Headers de seguranca (CSP, X-Frame, X-XSS, etc.)
- Cookies httpOnly + SameSite
- Isolamento multi-tenant (barber_shop_id em todas as tabelas)
- Validacao de inputs no backend

## Testes

```bash
python -m pytest tests/ -v
# ou
python tests/test_appointments.py
```

## Licenca

MIT
