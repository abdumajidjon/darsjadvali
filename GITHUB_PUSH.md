# GitHub ga Push Qilish Qo'llanmasi

## Muammo

Agar quyidagi xatolikni ko'rsangiz:
```
remote: Permission to abdumajidjon/darsjadvali.git denied
fatal: unable to access 'https://github.com/abdumajidjon/darsjadvali.git/': The requested URL returned error: 403
```

Bu GitHub ga autentifikatsiya muammosi.

## Yechimlar

### Usul 1: Personal Access Token (Tavsiya etiladi)

1. **GitHub'da Personal Access Token yarating:**
   - GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)
   - "Generate new token (classic)" ni bosing
   - Token nomini kiriting (masalan: "darsjadvali-push")
   - Scopes: `repo` ni belgilang
   - "Generate token" ni bosing
   - **Token ni ko'chirib oling** (faqat bir marta ko'rsatiladi!)

2. **Git remote ni o'zgartirish:**
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/abdumajidjon/darsjadvali.git
```

Yoki:
```bash
git remote remove origin
git remote add origin https://YOUR_TOKEN@github.com/abdumajidjon/darsjadvali.git
```

3. **Push qilish:**
```bash
git push -u origin main
```

### Usul 2: SSH Key (Uzoq muddatli yechim)

1. **SSH key yaratish:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

2. **SSH key ni GitHub ga qo'shish:**
   - `~/.ssh/id_ed25519.pub` faylini oching
   - GitHub > Settings > SSH and GPG keys > New SSH key
   - Key ni qo'shing

3. **Remote ni SSH ga o'zgartirish:**
```bash
git remote set-url origin git@github.com:abdumajidjon/darsjadvali.git
```

4. **Push qilish:**
```bash
git push -u origin main
```

### Usul 3: GitHub CLI

1. **GitHub CLI o'rnatish:**
   - https://cli.github.com/

2. **Login qilish:**
```bash
gh auth login
```

3. **Push qilish:**
```bash
git push -u origin main
```

## Railway PostgreSQL Sozlash

### 1. Railway'da PostgreSQL Ma'lumotlarini Olish

1. Railway dashboard ga kiring
2. PostgreSQL service ni oching
3. **Variables** tab ga kiring
4. Quyidagi ma'lumotlarni ko'rasiz:
   - `PGHOST`
   - `PGPORT`
   - `PGDATABASE`
   - `PGUSER`
   - `PGPASSWORD`

### 2. Connection String Format

Railway PostgreSQL connection string:

```
postgresql+asyncpg://PGUSER:PGPASSWORD@PGHOST:PGPORT/PGDATABASE
```

**Misol:**
```
postgresql+asyncpg://postgres:abc123@containers-us-west-123.railway.app:5432/railway
```

### 3. Railway Environment Variables

Railway'da deploy qilganda, quyidagi variables larni qo'shing:

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

### 4. Local Development

Local development uchun `.env` fayl:

```env
# Railway PostgreSQL
DATABASE_URL=postgresql+asyncpg://postgres:PASSWORD@containers-us-west-123.railway.app:5432/railway
```

## Tekshirish

1. GitHub repository ni oching: https://github.com/abdumajidjon/darsjadvali
2. Barcha fayllar ko'rinishi kerak
3. Railway'da deploy qilish mumkin
