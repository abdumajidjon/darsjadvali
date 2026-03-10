# .env Faylini Yaratish Qo'llanmasi

## Qadam 1: .env Faylini Yaratish

Loyiha ildizida (main.py fayli bor joyda) `.env` nomli yangi fayl yarating.

### Windows PowerShell:
```powershell
New-Item -Path .env -ItemType File
```

### Windows CMD:
```cmd
type nul > .env
```

### Yoki oddiy usul:
1. Notepad yoki boshqa matn muharririni oching
2. Faylni saqlang va nomini `.env` qiling (barcha fayllar ko'rinadigan bo'lishi kerak)

## Qadam 2: .env Faylini To'ldirish

`.env.example` faylini ko'chirib, quyidagi ma'lumotlarni to'ldiring:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/schedule_bot

# Redis
REDIS_URL=redis://localhost:6379/0

# Telegram Bot
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
WEBHOOK_URL=
WEBHOOK_SECRET=

# FastAPI
API_HOST=0.0.0.0
API_PORT=8000

# Admin
ADMIN_API_KEY=your_secure_api_key_here

# Week Calculation
ACADEMIC_START_DATE=2024-09-01
```

## Qadam 3: Ma'lumotlarni To'ldirish

### 1. BOT_TOKEN
- Telegram'da @BotFather ga murojaat qiling
- `/newbot` buyrug'ini yuboring
- Bot nomini va username ni kiriting
- Olingan token ni `BOT_TOKEN=` qatoriga yozing

**Misol:**
```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
```

### 2. DATABASE_URL
PostgreSQL ma'lumotlarini kiriting:

**Format:**
```
postgresql+asyncpg://username:password@host:port/database_name
```

**Misol:**
```env
DATABASE_URL=postgresql+asyncpg://postgres:mypassword@localhost:5432/schedule_bot
```

### 3. REDIS_URL
Redis ma'lumotlarini kiriting:

**Format:**
```
redis://host:port/database_number
```

**Misol:**
```env
REDIS_URL=redis://localhost:6379/0
```

### 4. ADMIN_API_KEY
Xavfsiz API kalit yarating (ixtiyoriy, lekin tavsiya etiladi):

**Misol:**
```env
ADMIN_API_KEY=my_secure_api_key_12345
```

### 5. ACADEMIC_START_DATE
O'quv yili boshlanish sanasini kiriting:

**Format:** YYYY-MM-DD

**Misol:**
```env
ACADEMIC_START_DATE=2024-09-01
```

## Qadam 4: Tekshirish

`.env` fayl to'g'ri yaratilganini tekshirish:

```python
from app.config import settings
print(f"Bot token: {settings.bot_token[:10]}...")
print(f"Database: {settings.database_url}")
```

## Muhim Eslatmalar

⚠️ **Xavfsizlik:**
- `.env` faylini **hech qachon** Git ga commit qilmang
- `.gitignore` faylida `.env` borligini tekshiring
- Bot token va parollarni hech kimga ko'rsatmang

✅ **To'g'ri Format:**
- Har bir o'zgaruvchi `KEY=value` formatida
- Bo'sh joylar bo'lmasligi kerak
- Qo'shtirnoq ishlatilmaydi (faqat qiymatda bo'lsa kerak)
- Izohlar `#` bilan boshlanadi

## Muammo Hal Qilish

**Muammo:** `.env` fayl topilmayapti
**Yechim:** Fayl loyiha ildizida (main.py bilan bir katalogda) bo'lishi kerak

**Muammo:** `BOT_TOKEN` topilmadi
**Yechim:** `.env` faylida `BOT_TOKEN=` qatori mavjudligini tekshiring

**Muammo:** Database ulanish xatosi
**Yechim:** `DATABASE_URL` formatini tekshiring va PostgreSQL ishlayotganini tekshiring
