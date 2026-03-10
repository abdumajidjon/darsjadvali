# Railway PostgreSQL Sozlash

## Ma'lumotlar

- **Username**: `postgres`
- **Password**: `MiksbWVtNhzVTuziNWqbURZlrnKkjrjj`

## Connection String Format

Railway PostgreSQL connection string format:

```
postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@PGHOST:PGPORT/PGDATABASE
```

## Railway'da Environment Variable

Railway dashboard da:

1. **Service** > **Variables** tab
2. **New Variable** qo'shing:

**Name:** `DATABASE_URL`

**Value:** 
```
postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@PGHOST:PGPORT/PGDATABASE
```

**Yoki Railway'ning o'z formatida:**
```
${{Postgres.DATABASE_URL}}
```

## PostgreSQL Service Ma'lumotlarini Olish

Railway'da PostgreSQL service ni oching va **Variables** tab dan quyidagilarni ko'rasiz:

- `PGHOST` - Host address
- `PGPORT` - Port (odatda 5432)
- `PGDATABASE` - Database name
- `PGUSER` - Username (postgres)
- `PGPASSWORD` - Password

## To'liq Connection String

Agar barcha ma'lumotlarni bilsangiz:

```
postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@containers-us-west-123.railway.app:5432/railway
```

**Misol:** `PGHOST=containers-us-west-123.railway.app`, `PGPORT=5432`, `PGDATABASE=railway` bo'lsa:

```
DATABASE_URL=postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@containers-us-west-123.railway.app:5432/railway
```

## Local Development (.env fayl)

Local development uchun `.env` fayl:

```env
# Railway PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@PGHOST:PGPORT/PGDATABASE

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
BOT_TOKEN=your_bot_token_here
WEBHOOK_URL=
WEBHOOK_SECRET=

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# Admin
ADMIN_API_KEY=your_admin_api_key_here

# Week Calculation
ACADEMIC_START_DATE=2024-09-01
```

**Eslatma:** `PGHOST`, `PGPORT`, `PGDATABASE` ni Railway'dan oling.

## Railway'da Tezkor Sozlash

1. Railway project > **PostgreSQL service** ni oching
2. **Variables** tab dan `PGHOST`, `PGPORT`, `PGDATABASE` ni ko'ring
3. **Web service** > **Variables** tab
4. **New Variable** qo'shing:

```
DATABASE_URL=postgresql+asyncpg://postgres:MiksbWVtNhzVTuziNWqbURZlrnKkjrjj@PGHOST:PGPORT/PGDATABASE
```

Yoki eng oson usul - Railway'ning o'z formatida:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

Bu avtomatik to'g'ri connection string ni beradi.

## Muhim Eslatmalar

⚠️ **Xavfsizlik:**
- Parolni hech kimga ko'rsatmang
- `.env` faylini Git ga commit qilmang
- Railway variables dan foydalaning

✅ **Best Practice:**
- Railway'da `${{Postgres.DATABASE_URL}}` formatidan foydalanish
- Local development uchun `.env` fayl ishlatish
