# Railway Deployment Qo'llanmasi

## Railway PostgreSQL Sozlash

### 1. Railway'da PostgreSQL Yaratish

1. [Railway.app](https://railway.app) ga kiring
2. New Project > Add Database > PostgreSQL
3. PostgreSQL service yaratiladi

### 2. PostgreSQL Ma'lumotlarini Olish

Railway dashboard da:
1. PostgreSQL service ni oching
2. **Variables** tab ga kiring
3. Quyidagi ma'lumotlarni ko'rasiz:
   - `PGHOST`
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`

### 3. .env Faylini Sozlash

Railway PostgreSQL ma'lumotlarini `.env` faylga qo'shing:

```env
# Railway PostgreSQL
DATABASE_URL=postgresql+asyncpg://PGUSER:PGPASSWORD@PGHOST:PGPORT/PGDATABASE
```

**Misol:**
```env
DATABASE_URL=postgresql+asyncpg://postgres:abc123@containers-us-west-123.railway.app:5432/railway
```

### 4. Railway Environment Variables

Railway'da application deploy qilganda, environment variables ni sozlang:

1. Railway project da **New Service** > **GitHub Repo** tanlang
2. **Variables** tab ga kiring
3. Quyidagi variables larni qo'shing:

```
BOT_TOKEN=your_bot_token_here
DATABASE_URL=${{Postgres.DATABASE_URL}}
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
WEBHOOK_SECRET=your_webhook_secret
ADMIN_API_KEY=your_admin_api_key
ACADEMIC_START_DATE=2024-09-01
```

**Muhim:** Railway PostgreSQL uchun `DATABASE_URL` ni `${{Postgres.DATABASE_URL}}` formatida ishlatish mumkin.

### 5. Railway PostgreSQL Connection String Format

Railway PostgreSQL connection string format:

```
postgresql+asyncpg://postgres:PASSWORD@HOST:PORT/railway
```

Yoki Railway'ning o'z formatida:

```
postgresql+asyncpg://${{Postgres.PGHOST}}:${{Postgres.PGPORT}}/${{Postgres.PGDATABASE}}?user=${{Postgres.PGUSER}}&password=${{Postgres.PGPASSWORD}}
```

### 6. Local Development

Local development uchun `.env` fayl:

```env
# Railway PostgreSQL (local development uchun)
DATABASE_URL=postgresql+asyncpg://postgres:PASSWORD@containers-us-west-123.railway.app:5432/railway

# Yoki local PostgreSQL
# DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/schedule_bot
```

### 7. Database Migrations

Railway'da deploy qilganda, migrations ni ishga tushirish:

**Railway'da startup command:**
```bash
alembic upgrade head && python main.py
```

Yoki **railway.json** yoki **Procfile** yaratish:

**Procfile:**
```
web: alembic upgrade head && python main.py
```

### 8. Redis (Ixtiyoriy)

Agar Redis kerak bo'lsa:
1. Railway'da **New Service** > **Redis** qo'shing
2. `REDIS_URL` ni environment variable sifatida qo'shing

## GitHub Actions (CI/CD)

Agar GitHub Actions ishlatmoqchi bo'lsangiz, `.github/workflows/deploy.yml` yarating.

## Tekshirish

Deploy qilgandan keyin:

1. Railway logs ni tekshiring
2. Database connection muvaffaqiyatli bo'lishi kerak
3. Application `https://your-app.railway.app` da ishlashi kerak

## Muhim Eslatmalar

⚠️ **Xavfsizlik:**
- `.env` faylini Git ga commit qilmang
- Railway environment variables dan foydalaning
- Bot token va parollarni hech kimga ko'rsatmang

✅ **Best Practices:**
- Production uchun Railway PostgreSQL ishlatish
- Environment variables ni Railway'da sozlash
- Database migrations ni avtomatik ishga tushirish
