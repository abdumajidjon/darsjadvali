# GitHub ga Push Qilish - Qadam-baqadam Qo'llanma

## Muammo

Git'da boshqa GitHub account (`birnimagemini-rgb`) bilan autentifikatsiya qilingan, lekin repository `abdumajidjon/darsjadvali` ga tegishli.

## Yechim

### Usul 1: Personal Access Token (Eng Oson)

1. **GitHub'da Personal Access Token yarating:**
   - GitHub.com ga kiring
   - O'ng yuqori burchakda profile > **Settings**
   - Pastga scroll qiling > **Developer settings**
   - **Personal access tokens** > **Tokens (classic)**
   - **Generate new token (classic)** ni bosing
   - Token nomini kiriting: `darsjadvali-push`
   - **Expiration**: 90 days yoki No expiration
   - **Scopes**: `repo` ni belgilang
   - **Generate token** ni bosing
   - **Token ni ko'chirib oling** (faqat bir marta ko'rsatiladi!)

2. **Git remote ni token bilan yangilang:**

PowerShell'da:
```powershell
$token = "YOUR_TOKEN_HERE"
git remote set-url origin "https://$token@github.com/abdumajidjon/darsjadvali.git"
```

Yoki to'g'ridan-to'g'ri:
```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/abdumajidjon/darsjadvali.git
```

3. **Push qiling:**
```powershell
git push -u origin main
```

### Usul 2: GitHub Desktop

1. GitHub Desktop ni o'rnating: https://desktop.github.com/
2. File > Clone repository > GitHub.com
3. `abdumajidjon/darsjadvali` ni tanlang
4. Clone qiling
5. Publish repository ni bosing

### Usul 3: GitHub CLI

1. GitHub CLI ni o'rnating: https://cli.github.com/
2. Login qiling:
```bash
gh auth login
```
3. Push qiling:
```bash
git push -u origin main
```

### Usul 4: Windows Credential Manager

1. Windows Credential Manager ni oching:
   - Start > Credential Manager
   - Windows Credentials tab
   - `git:https://github.com` ni toping
   - Edit yoki Remove qiling
2. Qayta push qilishda yangi credentials so'raladi

## Tekshirish

Push muvaffaqiyatli bo'lgandan keyin:

1. GitHub repository ni oching: https://github.com/abdumajidjon/darsjadvali
2. Barcha fayllar ko'rinishi kerak
3. Commit history ko'rinishi kerak

## Railway Deployment

Push qilgandan keyin:

1. Railway.app ga kiring
2. **New Project** > **Deploy from GitHub repo**
3. `abdumajidjon/darsjadvali` ni tanlang
4. **Add PostgreSQL** service qo'shing
5. Environment variables ni sozlang (RAILWAY_SETUP.md ga qarang)
