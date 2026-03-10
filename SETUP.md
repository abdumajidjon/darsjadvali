# Setup Guide

## Prerequisites

- Python 3.11+
- PostgreSQL database
- Redis server
- Telegram Bot Token (from @BotFather)

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/schedule_bot

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=https://your-domain.com/bot-webhook
WEBHOOK_SECRET=your_webhook_secret_here

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# Admin
ADMIN_API_KEY=your_admin_api_key_here

# Week Calculation
ACADEMIC_START_DATE=2024-09-01
```

### 3. Initialize Database

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Start Services

#### Terminal 1: FastAPI Application
```bash
python main.py
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Terminal 2: Taskiq Worker
```bash
python worker.py
# or
taskiq worker app.workers.tasks.broker
```

### 5. Set Webhook (Optional)

If using webhook mode, the webhook will be automatically set on startup if `WEBHOOK_URL` is configured.

For polling mode (development), you can use:
```python
from app.bot.dispatcher import get_dispatcher, get_bot
import asyncio

async def main():
    bot = get_bot()
    dp = get_dispatcher()
    await dp.start_polling(bot)

asyncio.run(main())
```

## Usage

### Upload Schedule

```bash
curl -X POST "http://localhost:8000/admin/upload-schedule" \
  -H "X-API-Key: your_admin_api_key_here" \
  -F "file=@schedule.xlsx" \
  -F "target_date=2024-09-15"
```

### Telegram Bot Commands

- `/start` - Start the bot and register user
- `/schedule` - View current week schedule
- `/setgroup <group_name>` - Set user's group

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── config.py            # Configuration
│   ├── bot/
│   │   ├── handlers.py      # Bot command handlers
│   │   ├── keyboards.py     # Inline keyboards
│   │   └── dispatcher.py    # Bot setup
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── database/
│   │   ├── models.py        # SQLAlchemy models
│   │   └── connection.py    # DB connection
│   ├── services/
│   │   ├── parser.py        # Excel parser
│   │   ├── diff_engine.py  # Substitution detection
│   │   └── broadcast.py     # Message broadcasting
│   ├── workers/
│   │   └── tasks.py         # Background tasks
│   └── utils/
│       └── week_calculator.py
├── alembic/                 # Database migrations
├── main.py                 # Entry point
├── worker.py               # Worker entry point
├── requirements.txt
└── README.md
```

## Excel File Format

The parser expects Excel files with the following structure:

- **Columns**: Day, Pair, Time, Subject, Teacher, Room
- **Merged cells**: Supported (automatically unmerged)
- **Week splits**: Use `/` or newline to separate odd/even weeks
- **Group identification**: First column typically contains group name

Example:
```
Group    | Day      | Pair | Time      | Subject | Teacher | Room
---------|----------|------|------------|---------|---------|-----
Group-1  | Monday   | I    | 08:00-09:30| Math    | John    | 101
         |          | II   | 10:00-11:30| Physics | Jane    | 102
```

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running
- Check DATABASE_URL format: `postgresql+asyncpg://user:pass@host:port/dbname`

### Redis Connection Issues
- Verify Redis is running: `redis-cli ping`
- Check REDIS_URL format: `redis://localhost:6379/0`

### Bot Not Responding
- Verify BOT_TOKEN is correct
- Check webhook status: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- For development, use polling mode instead of webhook

### Parsing Errors
- Ensure Excel file follows expected format
- Check column headers match expected names (case-insensitive)
- Verify merged cells are properly formatted
