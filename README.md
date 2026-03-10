# Automated Schedule & Substitution Bot

A Telegram bot system for managing class schedules and detecting substitutions automatically.

## Features

- Excel schedule parsing with merged cells support
- Automatic substitution detection
- Targeted broadcast notifications
- Odd/Even week calculation
- Webhook-based Telegram integration
- Background task processing

## Technology Stack

- **Runtime**: Python 3.11
- **Bot Framework**: aiogram 3.x (Webhook mode)
- **Backend API**: FastAPI
- **Database**: PostgreSQL (asyncpg + SQLAlchemy 2.0)
- **Task Queue**: Redis + Taskiq
- **Data Processing**: openpyxl + pandas

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Initialize database:
```bash
alembic upgrade head
```

4. Run the application:
```bash
python main.py
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── bot/
│   │   ├── __init__.py
│   │   ├── handlers.py      # Telegram bot handlers
│   │   └── keyboards.py     # Inline keyboards
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py         # FastAPI routes
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py         # SQLAlchemy models
│   │   └── connection.py     # Database connection
│   ├── services/
│   │   ├── __init__.py
│   │   ├── parser.py         # Excel parsing engine
│   │   ├── diff_engine.py    # Substitution detection
│   │   └── broadcast.py      # Message broadcasting
│   ├── workers/
│   │   ├── __init__.py
│   │   └── tasks.py          # Background tasks
│   └── utils/
│       ├── __init__.py
│       └── week_calculator.py
├── alembic/                  # Database migrations
├── requirements.txt
├── .env.example
└── README.md
```

## API Endpoints

- `POST /bot-webhook` - Telegram webhook endpoint
- `POST /admin/upload-schedule` - Admin schedule upload (requires API key)

## License

MIT
