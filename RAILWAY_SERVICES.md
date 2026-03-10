# Railway Services Sozlash

## Services Tahlili

Railway dashboard da 3 ta service ko'rinmoqda:

1. **Postgres** - ✅ Online (Database service)
2. **web** - ❌ Crashed (Asosiy application service)
3. **worker** - ❌ Crashed (Background worker service)

## Environment Variables Qaysi Service ga Qo'shiladi?

### ✅ Web Service (Asosiy)

**Barcha environment variables `web` service ga qo'shiladi:**

1. Railway dashboard > **web** service ni oching
2. **Variables** tab ga kiring
3. Quyidagi variables larni qo'shing:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
BOT_TOKEN=8757340484:AAHeeoxQgj38xFSrLeZEJz6NLBoHe9m6Pgs
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://your-app.railway.app/bot-webhook
ADMIN_API_KEY=your_admin_api_key
ACADEMIC_START_DATE=2024-09-01
```

### ⚠️ Worker Service (Ixtiyoriy)

Agar `worker` service alohida ishlatilsa, faqat Redis URL qo'shish kifoya:

```
REDIS_URL=redis://localhost:6379/0
```

Yoki worker service ni o'chirib tashlash mumkin, chunki worker `web` service ichida ham ishlashi mumkin.

## Qadam-baqadam Sozlash

### 1. Web Service ni Sozlash

1. **web** service ni oching (qizil rangda ko'rsatilgan)
2. **Variables** tab ga kiring
3. **New Variable** tugmasini bosing
4. Quyidagilarni birma-bir qo'shing:

**Variable 1:**
- Name: `DATABASE_URL`
- Value: `${{Postgres.DATABASE_URL}}`

**Variable 2:**
- Name: `BOT_TOKEN`
- Value: `8757340484:AAHeeoxQgj38xFSrLeZEJz6NLBoHe9m6Pgs`

**Variable 3:**
- Name: `REDIS_URL`
- Value: `redis://localhost:6379/0`

**Variable 4:**
- Name: `WEBHOOK_URL`
- Value: `https://your-app.railway.app/bot-webhook`
- **Eslatma:** `your-app.railway.app` ni Railway'ning bergan domain bilan almashtiring

**Variable 5:**
- Name: `ADMIN_API_KEY`
- Value: `your_secure_admin_key_here`

**Variable 6:**
- Name: `ACADEMIC_START_DATE`
- Value: `2024-09-01`

### 2. Web Service ni Restart Qilish

Variables qo'shgandan keyin:
1. **Deployments** tab ga kiring
2. **Redeploy** tugmasini bosing
3. Yoki avtomatik redeploy bo'ladi

### 3. Worker Service (Ixtiyoriy)

Agar worker service alohida ishlatilsa:

1. **worker** service ni oching
2. **Variables** tab
3. Faqat `REDIS_URL` qo'shing:
   - Name: `REDIS_URL`
   - Value: `redis://localhost:6379/0`

**Yoki** worker service ni o'chirib tashlash mumkin va worker ni `web` service ichida ishlatish.

## Xulosa

✅ **Asosiy javob:** Barcha environment variables **`web` service** ga qo'shiladi!

**Qaysi service ga qo'shish kerak:**
- ✅ **web** service - Barcha variables
- ⚠️ **worker** service - Faqat REDIS_URL (agar alohida ishlatilsa)
- ❌ **Postgres** service - Hech qanday variable qo'shish shart emas

## Tezkor Yechim

1. **web** service > **Variables** tab
2. Quyidagilarni qo'shing:

```
DATABASE_URL=${{Postgres.DATABASE_URL}}
BOT_TOKEN=8757340484:AAHeeoxQgj38xFSrLeZEJz6NLBoHe9m6Pgs
REDIS_URL=redis://localhost:6379/0
ADMIN_API_KEY=your_admin_key
ACADEMIC_START_DATE=2024-09-01
```

3. Service avtomatik redeploy bo'ladi va ishga tushadi!
