# Automated Schedule & Substitution Bot

Telegram bot system for managing class schedules and detecting substitutions automatically.

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

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/abdumajidjon/darsjadvali.git
cd darsjadvali
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```env
# Database (Railway PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com/bot-webhook
WEBHOOK_SECRET=your_webhook_secret

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# Admin
ADMIN_API_KEY=your_admin_api_key

# Week Calculation
ACADEMIC_START_DATE=2024-09-01
```

### 4. Initialize Database

```bash
alembic upgrade head
```

### 5. Run Application

```bash
python main.py
```

## Railway Deployment

### 1. Connect GitHub Repository

1. Railway dashboard > New Project > Deploy from GitHub repo
2. Select `abdumajidjon/darsjadvali`

### 2. Add PostgreSQL

1. New > Add Database > PostgreSQL
2. Railway automatically provides connection string

### 3. Set Environment Variables

In Railway project settings, add:

```
BOT_TOKEN=your_bot_token
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
ADMIN_API_KEY=your_admin_api_key
ACADEMIC_START_DATE=2024-09-01
```

### 4. Deploy

Railway automatically deploys on push to main branch.

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── bot/                 # Telegram bot handlers
│   ├── api/                 # FastAPI routes
│   ├── database/            # Models & connection
│   ├── services/            # Business logic
│   ├── workers/            # Background tasks
│   └── utils/               # Utilities
├── alembic/                 # Database migrations
├── main.py                 # Entry point
├── worker.py               # Worker entry point
└── requirements.txt
```

## API Endpoints

- `POST /bot-webhook` - Telegram webhook endpoint
- `POST /admin/upload-schedule` - Admin schedule upload (requires API key)
- `GET /health` - Health check

## Bot Commands

- `/start` - Start the bot and register user
- `/schedule` - View current week schedule
- `/setgroup <group_name>` - Set user's group

## Documentation

- [Setup Guide](SETUP.md)
- [Database Setup](DATABASE_SETUP.md)
- [Railway Setup](RAILWAY_SETUP.md)
- [Bot Token Setup](BOT_TOKEN_SETUP.md)

## License

MIT
