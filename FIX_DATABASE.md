# Database Ulanish Muammosini Hal Qilish

## Muammo

`.env` faylda default qiymatlar qoldirilgan:
```
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/schedule_bot
```

Bu noto'g'ri! Haqiqiy PostgreSQL username va password kerak.

## Yechim

### 1. PostgreSQL Username va Password ni Topish

PostgreSQL'da odatda:
- **Username**: `postgres` (default)
- **Password**: PostgreSQL o'rnatish paytida belgilangan parol

Agar parolni bilmasangiz, quyidagilarni bajarishingiz mumkin:

#### Usul 1: pgAdmin orqali
1. pgAdmin ni oching
2. Server Properties ga kiring
3. Connection tab da username va password ni ko'ring

#### Usul 2: PostgreSQL terminal orqali
```sql
-- PostgreSQL terminal (psql) orqali
-- Windows: Start Menu > PostgreSQL > SQL Shell (psql)
```

### 2. .env Faylini To'g'rilash

`.env` faylini oching va quyidagilarni o'zgartiring:

**ESKI (noto'g'ri):**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/schedule_bot
```

**YANGI (to'g'ri):**
```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5432/schedule_bot
```

**Misol:**
```env
DATABASE_URL=postgresql+asyncpg://postgres:mypassword123@localhost:5432/schedule_bot
```

### 3. Portni Tekshirish

Sizda 2 ta PostgreSQL versiyasi ishlayapti:
- PostgreSQL 15 (port 5432)
- PostgreSQL 18 (port 5433)

Agar PostgreSQL 18 dan foydalanmoqchi bo'lsangiz:
```env
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_PASSWORD@localhost:5433/schedule_bot
```

### 4. Database Yaratish

Database mavjud emas bo'lishi mumkin. Yaratish:

```sql
-- PostgreSQL terminal (psql) orqali
CREATE DATABASE schedule_bot;
```

Yoki `setup_database.py` script ishlatish:
```bash
py -3.11 setup_database.py
```

### 5. Tekshirish

`.env` faylni to'g'rilagach, qayta tekshiring:

```bash
py -3.11 setup_database.py
```

Agar "[OK] Connection successful!" ko'rsangiz, hammasi yaxshi!

## Tezkor Yechim (Development uchun SQLite)

Agar PostgreSQL sozlash qiyin bo'lsa, development uchun SQLite ishlatishingiz mumkin:

1. **aiosqlite o'rnatish:**
```bash
py -3.11 -m pip install aiosqlite
```

2. **.env faylini o'zgartirish:**
```env
DATABASE_URL=sqlite+aiosqlite:///./schedule_bot.db
```

3. **Application ni ishga tushirish:**
```bash
py -3.11 main.py
```

**Eslatma:** SQLite faqat development uchun. Production uchun PostgreSQL tavsiya etiladi.
