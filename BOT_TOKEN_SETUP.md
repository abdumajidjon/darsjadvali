# Bot Token Sozlash Qo'llanmasi

## Bot Token Qayerdan Olinadi?

1. **Telegram'da @BotFather ga murojaat qiling**
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting
4. Bot username ni kiriting (oxirida `bot` bo'lishi kerak, masalan: `my_schedule_bot`)
5. BotFather sizga **BOT_TOKEN** beradi

**Misol:**
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
```

## Bot Token Qayerga Joylashtiriladi?

Bot token `.env` faylida `BOT_TOKEN` o'zgaruvchisiga yoziladi:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
```

## Bot Token Qayerda Ishlatiladi?

### 1. `app/config.py` - Konfiguratsiya
```python
class Settings(BaseSettings):
    bot_token: str = Field(..., env="BOT_TOKEN")
```

Bot token `.env` faylidan o'qiladi va `settings.bot_token` orqali ishlatiladi.

### 2. `app/bot/dispatcher.py` - Bot Dispatcher
```python
def get_bot() -> Bot:
    _bot = Bot(token=settings.bot_token)
    return _bot
```

Bot yaratilganda token ishlatiladi.

### 3. `app/services/broadcast.py` - Xabar Yuborish
```python
bot = Bot(token=settings.bot_token)
broadcast_service = BroadcastService(bot, session)
```

Xabarlarni yuborish uchun bot instance yaratiladi.

### 4. `app/workers/tasks.py` - Background Tasks
```python
bot = Bot(token=settings.bot_token)
```

Background tasklarda ham bot token ishlatiladi.

## .env Faylini To'ldirish

1. `.env` faylini oching
2. `BOT_TOKEN=your_bot_token_here` qatorini toping
3. `your_bot_token_here` o'rniga haqiqiy token ni yozing:

```env
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
```

## Muhim Eslatmalar

⚠️ **Xavfsizlik:**
- `.env` faylini **hech qachon** Git ga commit qilmang
- `.gitignore` faylida `.env` borligini tekshiring
- Bot token ni hech kimga ko'rsatmang

✅ **To'g'ri Format:**
- Token format: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890`
- Bo'sh joylar bo'lmasligi kerak
- Qo'shtirnoq ishlatilmaydi

## Tekshirish

Bot token to'g'ri sozlanganini tekshirish:

```python
from app.config import settings
print(f"Bot token uzunligi: {len(settings.bot_token)}")
# 45-50 belgi bo'lishi kerak
```

## Muammo Hal Qilish

**Muammo:** `BOT_TOKEN` topilmadi
**Yechim:** `.env` faylida `BOT_TOKEN` mavjudligini tekshiring

**Muammo:** Bot ishlamayapti
**Yechim:** Token to'g'riligini @BotFather dan tekshiring
