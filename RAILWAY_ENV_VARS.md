# Railway Environment Variables Sozlash

## Muammo

Railway'da deploy qilganda quyidagi xatolik:
```
pydantic_core._pydantic_core.ValidationError: 5 validation errors for Settings
database_url - Field required
redis_url - Field required
bot_token - Field required
admin_api_key - Field required
academic_start_date - Field required
```

Bu degani, Railway'da environment variables sozlanmagan.

## Yechim: Railway'da Environment Variables Qo'shish

### 1. Railway Dashboard ga Kiring

1. Railway.app ga kiring
2. Project ni oching
3. Service ni tanlang (web service)

### 2. Variables Tab ga Kiring

1. Service settings da **Variables** tab ni oching
2. **New Variable** tugmasini bosing

### 3. Quyidagi Variables larni Qo'shing

#### Database (PostgreSQL)

Agar PostgreSQL service qo'shgan bo'lsangiz:

**Usul 1: Railway'ning o'z formatida**
```
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

**Usul 2: To'g'ridan-to'g'ri**
PostgreSQL service > Variables tab dan:
- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

Keyin format:
```
DATABASE_URL=postgresql+asyncpg://PGUSER:PGPASSWORD@PGHOST:PGPORT/PGDATABASE
```

**Misol:**
```
DATABASE_URL=postgresql+asyncpg://postgres:abc123@containers-us-west-123.railway.app:5432/railway
```

#### Telegram Bot

```
BOT_TOKEN=your_bot_token_here
```

Bot token olish:
1. Telegram'da @BotFather ga murojaat qiling
2. `/newbot` yoki `/mybots` > Bot ni tanlang > API Token

#### Redis (Ixtiyoriy)

Agar Redis service qo'shgan bo'lsangiz:
```
REDIS_URL=${{Redis.REDIS_URL}}
```

Yoki:
```
REDIS_URL=redis://localhost:6379/0
```

#### Webhook

```
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
WEBHOOK_SECRET=your_webhook_secret_here
```

**Eslatma:** `WEBHOOK_URL` ni Railway'ning bergan domain bilan almashtiring.

#### Admin API Key

```
ADMIN_API_KEY=your_secure_api_key_here
```

Xavfsiz kalit yarating (masalan: `railway_admin_2024_secure_key`)

#### Academic Start Date

```
ACADEMIC_START_DATE=2024-09-01
```

Format: `YYYY-MM-DD`

### 4. To'liq Variables Ro'yxati

Railway'da quyidagi barcha variables larni qo'shing:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
BOT_TOKEN=your_bot_token_here
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
WEBHOOK_SECRET=your_webhook_secret
ADMIN_API_KEY=your_admin_api_key
ACADEMIC_START_DATE=2024-09-01
API_HOST=0.0.0.0
API_PORT=${{PORT}}
```

**Muhim:** Railway avtomatik `PORT` environment variable ni beradi, shuning uchun `API_PORT=${{PORT}}` ishlatish mumkin.

### 5. Tekshirish

Variables qo'shgandan keyin:

1. **Redeploy** qiling (yoki avtomatik redeploy bo'ladi)
2. **Logs** ni tekshiring
3. Agar hali ham xatolik bo'lsa, har bir variable to'g'riligini tekshiring

### 6. PostgreSQL Service Qo'shish

Agar PostgreSQL service qo'shmagan bo'lsangiz:

1. Railway project da **New** > **Database** > **Add PostgreSQL**
2. PostgreSQL service yaratiladi
3. `DATABASE_URL=${{Postgres.DATABASE_URL}}` ni ishlatishingiz mumkin

## Muammo Hal Qilish

**Muammo:** `DATABASE_URL` topilmayapti
**Yechim:** PostgreSQL service qo'shing va `DATABASE_URL=${{Postgres.DATABASE_URL}}` ni qo'shing

**Muammo:** `BOT_TOKEN` topilmayapti
**Yechim:** Bot token ni @BotFather dan oling va Railway variables ga qo'shing

**Muammo:** `academic_start_date` format xatosi
**Yechim:** Format `YYYY-MM-DD` bo'lishi kerak (masalan: `2024-09-01`)

## Tezkor Yechim

Agar barcha variables ni bir vaqtda qo'shmoqchi bo'lsangiz:

1. Railway service > **Variables** tab
2. **Raw Editor** ni oching (agar mavjud bo'lsa)
3. Quyidagilarni yozing:

```env
DATABASE_URL=${{Postgres.DATABASE_URL}}
BOT_TOKEN=your_bot_token
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
ADMIN_API_KEY=your_admin_key
ACADEMIC_START_DATE=2024-09-01
```

4. **Save** ni bosing
5. Service avtomatik redeploy bo'ladi
