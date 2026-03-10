# Database Sozlash Qo'llanmasi

## Muammo

Agar quyidagi xatolikni ko'rsangiz:

```
asyncpg.exceptions.ConnectionDoesNotExistError: connection was closed in the middle of operation
```

Bu PostgreSQL database ga ulanishda muammo borligini anglatadi.

## Yechimlar

### 1. PostgreSQL O'rnatish va Ishga Tushirish

#### Windows:
1. PostgreSQL ni o'rnating: https://www.postgresql.org/download/windows/
2. PostgreSQL xizmatini ishga tushiring:
   ```powershell
   # Xizmatni tekshirish
   Get-Service -Name postgresql*
   
   # Xizmatni ishga tushirish (agar to'xtatilgan bo'lsa)
   Start-Service -Name postgresql*
   ```

#### Linux/Mac:
```bash
# PostgreSQL ni ishga tushirish
sudo systemctl start postgresql
# yoki
sudo service postgresql start
```

### 2. Database Yaratish

PostgreSQL'ga ulaning va database yarating:

```sql
-- PostgreSQL terminal yoki pgAdmin orqali
CREATE DATABASE schedule_bot;
```

### 3. .env Faylini To'g'rilash

`.env` faylida `DATABASE_URL` ni to'g'ri sozlang:

```env
# Format: postgresql+asyncpg://username:password@host:port/database_name

# Misol 1: Default sozlamalar
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5432/schedule_bot

# Misol 2: Boshqa port
DATABASE_URL=postgresql+asyncpg://postgres:your_password@localhost:5433/schedule_bot

# Misol 3: Remote server
DATABASE_URL=postgresql+asyncpg://user:pass@192.168.1.100:5432/schedule_bot
```

### 4. PostgreSQL Parolini O'zgartirish

Agar parolni bilmasangiz:

```sql
-- PostgreSQL terminal orqali
ALTER USER postgres WITH PASSWORD 'yangi_parol';
```

### 5. Ulanishni Tekshirish

Python orqali tekshirish:

```python
import asyncio
import asyncpg

async def test_connection():
    try:
        conn = await asyncpg.connect(
            'postgresql://postgres:your_password@localhost:5432/schedule_bot'
        )
        print("✅ Database connection successful!")
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

asyncio.run(test_connection())
```

## Alternativ: SQLite (Development uchun)

Agar PostgreSQL o'rnatish qiyin bo'lsa, development uchun SQLite ishlatishingiz mumkin:

### 1. .env Faylini O'zgartirish

```env
DATABASE_URL=sqlite+aiosqlite:///./schedule_bot.db
```

### 2. Aiosqlite Kutubxonasini O'rnatish

```bash
py -3.11 -m pip install aiosqlite
```

### 3. requirements.txt ga Qo'shish

```txt
aiosqlite==0.19.0
```

**Eslatma:** SQLite production uchun tavsiya etilmaydi. Faqat development/test uchun.

## Tekshirish

Database to'g'ri sozlanganini tekshirish:

```bash
# Application ni ishga tushirish
py -3.11 main.py

# Agar "✅ Database initialized successfully" ko'rsangiz, hammasi yaxshi!
```

## Muammo Hal Qilish

**Muammo:** `connection was closed in the middle of operation`
**Yechim:** PostgreSQL ishlayotganini tekshiring va `.env` fayldagi `DATABASE_URL` ni to'g'rilang

**Muammo:** `password authentication failed`
**Yechim:** `.env` fayldagi parol to'g'riligini tekshiring

**Muammo:** `database "schedule_bot" does not exist`
**Yechim:** Database yaratish kerak (yuqoridagi qadam 2 ni bajarish)

**Muammo:** `could not connect to server`
**Yechim:** PostgreSQL xizmati ishlayotganini tekshiring
