# SSH Key Sozlash Qo'llanmasi

## SSH Key Yaratish va GitHub ga Qo'shish

### 1. SSH Key Yaratish

PowerShell'da quyidagi buyruqni ishlating:

```powershell
ssh-keygen -t ed25519 -C "your_email@example.com"
```

**Misol:**
```powershell
ssh-keygen -t ed25519 -C "abdumajidjon@example.com"
```

**Eslatma:**
- Enter ni bosganda default fayl nomi taklif qilinadi: `C:\Users\texnoexpert\.ssh\id_ed25519`
- Parol kiritish ixtiyoriy (Enter ni bosib o'tib ketishingiz mumkin)
- Parol kiritilsa, har safar SSH ishlatganda so'raladi

### 2. SSH Key ni Ko'rish

Yaratilgan SSH public key ni ko'rish:

```powershell
Get-Content ~/.ssh/id_ed25519.pub
```

Yoki:

```powershell
cat C:\Users\texnoexpert\.ssh\id_ed25519.pub
```

### 3. GitHub ga SSH Key Qo'shish

1. **SSH key ni ko'chirib oling:**
   - Yuqoridagi buyruq natijasini ko'chirib oling
   - Format: `ssh-ed25519 AAAA... your_email@example.com`

2. **GitHub'da SSH key qo'shing:**
   - GitHub.com > Settings > SSH and GPG keys
   - **New SSH key** tugmasini bosing
   - **Title**: `darsjadvali-laptop` (yoki istalgan nom)
   - **Key**: Ko'chirib olgan SSH key ni yozing
   - **Add SSH key** ni bosing

### 4. Git Remote ni SSH ga O'zgartirish

HTTPS o'rniga SSH ishlatish:

```powershell
git remote set-url origin git@github.com:abdumajidjon/darsjadvali.git
```

### 5. SSH Ulanishini Tekshirish

```powershell
ssh -T git@github.com
```

Agar muvaffaqiyatli bo'lsa, quyidagi xabar ko'rinadi:
```
Hi abdumajidjon! You've successfully authenticated, but GitHub does not provide shell access.
```

### 6. Push Qilish

Endi push qilish mumkin:

```powershell
git push -u origin main
```

## Alternativ: Personal Access Token (Tezkor Yechim)

Agar SSH key yaratish qiyin bo'lsa, Personal Access Token ishlatishingiz mumkin:

1. **GitHub > Settings > Developer settings > Personal access tokens > Tokens (classic)**
2. **Generate new token (classic)**
3. Token ni yarating va ko'chirib oling
4. **Git remote ni yangilang:**

```powershell
git remote set-url origin https://YOUR_TOKEN@github.com/abdumajidjon/darsjadvali.git
```

5. **Push qiling:**

```powershell
git push -u origin main
```

## Qaysi Usulni Tanlash?

- **SSH Key**: Uzoq muddatli, xavfsiz, har safar parol kiritish shart emas
- **Personal Access Token**: Tezkor, oson, lekin token ni saqlash kerak

Ikkalasi ham ishlaydi!
