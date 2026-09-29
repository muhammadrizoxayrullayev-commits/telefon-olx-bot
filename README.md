# 🤖 OLX Gadgets & Tech Finder Telegram Bot (@telefonol_bot)

O'zbekiston bo'ylab **OLX.uz** platformasidagi barcha texnika va gadjetlarni (Apple, Samsung, Xiaomi, Windows Gaming va ofis noutbuklari) aniq texnik ko'rsatkichlari bo'yicha saralab topuvchi **24/7 uzluksiz ishlaydigan** Telegram boti.

---

## 🌟 Asosiy Imkoniyatlar

- 🍏 **Apple Mahsulotlari:**
  - **MacBook:** MacBook Pro (M4, M3 Pro/Max, M2, M1, Intel), MacBook Air (M3, M2, M1)
  - **iPhone:** iPhone 16 Pro Max dan tortib iPhone 11, XS, SE gacha barcha modellar
  - **iPad:** iPad Pro M4/M2/M1, iPad Air, iPad Mini, iPad 10/9-avlod
  - **Mac Desktop:** Mac mini M4/M2/M1, iMac, Mac Studio
  - **Apple Watch:** Ultra 2, Series 10, 9, 8, SE 2
  - **AirPods:** Max, Pro 2, 4 ANC, 3, 2

- 💻 **Windows Noutbuklar:**
  - **HP:** HP Victus 16, HP Victus 15, HP Omen, HP Pavilion Gaming, Envy
  - **Lenovo:** Lenovo Legion 5 / 5 Pro, Legion 7, LOQ 15, IdeaPad Gaming, ThinkPad
  - **ASUS:** ROG Strix, Zephyrus, TUF Gaming, ZenBook
  - **Acer:** Nitro 16, Nitro 5, Predator Helios, Aspire
  - **Dell:** Alienware, G15 / G16, XPS
  - **MSI:** Katana, Raider, Thin GF63, Cyborg

- 📱 **Samsung:**
  - Galaxy S24 Ultra, S24+, S24, S23 Ultra, S22...
  - Galaxy Z Fold 6/5, Z Flip 6/5
  - Galaxy A55 5G, A54 5G, A35, A15
  - Galaxy Tab S9/S8 va Galaxy Watch/Buds

- ⚡ **Xiaomi / Redmi / POCO:**
  - Xiaomi 14 Ultra, 14, 13T Pro
  - Redmi Note 13 Pro+, 13 Pro, 13, 12...
  - POCO F6 Pro, X6 Pro, M6 Pro...
  - Xiaomi Pad 6 / 6S Pro

- 🎮 **Boshqa Gadjetlar:**
  - Sony PlayStation 5 (Slim / Disc / Digital), PlayStation 4 Pro
  - Xbox Series X, Xbox Series S
  - Nintendo Switch OLED / V2
  - DJI Dronlar (Mini 4 Pro, Air 3)
  - Smart TV lar

- 🔍 **Erkin Qidiruv (Smart Search):**
  - Foydalanuvchi istalgan gadjet nomini yozsa (masalan: `macbook air m2 16gb 512gb`), bot darhol OLX dan eng mos natijalarni topib beradi.

---

## 🎯 Interaktiv Bosqichma-bosqich Tanlov (Wizard)

1. **Brend tanlash** (Apple, Windows, Samsung, Xiaomi, Boshqa).
2. **Qurilma / Model tanlash** (Masalan: `MacBook Pro M3 Pro`).
3. **RAM (Operativka) tanlash** (8GB, 16GB, 18GB, 24GB, 32GB, 36GB, 64GB yoki `Farqi yo'q`).
4. **Xotira (SSD / ROM) tanlash** (256GB, 512GB, 1TB, 2TB yoki `Farqi yo'q`).
5. **Batareya holati / Yomkist** (100% Yangi/Ideal, 90-99%, 85-89%, 80-84% yoki `Farqi yo'q`).
6. **Natijalar:**
   - 🖼️ E'lon rasmi (OLX dan to'g'ridan-to'g'ri yuklanadi)
   - 📦 Sarlavha
   - 💰 Narxi (so'mda va dollar ekvivalentida)
   - 📍 Joylashuvi (Shahar va tuman)
   - ⚙️ Holati (Yangi / Ishlatilgan)
   - 🔋 Batareya / Yomkist holati va tsikllar soni (tavsifdan avtomatik ajratib olinadi)
   - 🔗 **To'g'ridan-to'g'ri OLX havolasi**
   - ⬅️ Oldingi / Keyingi ➡️ sahifalash tugmalari
   - 📋 Barcha e'lonlar ro'yxatini bir zumda ko'rish

---

## 🛡️ 24/7 Uzluksiz Ishlash va Xavfsizlik

- **CloudFront / WAF Aylanib O'tish:** OLX.uz blokirovkalari va 403 xatoliklarini to'liq bartaraf etuvchi `curl_cffi` (Chrome JA3/HTTP2 impersonation) tizimi.
- **Supervisor Watchdog (`runner.py`):** Bot biron sabab bilan to'xtab qolsa ham, supervisor uni millisekundlar ichida avtomatik qayta ishga tushiradi.
- **Xatoliklarni qamrab olish:** Barcha so'rovlar global try/catch va Telegram xatoliklar filtri bilan himoyalangan.
- **Keshlash:** OLX ga ortiqcha yuk tushmasligi va bot chaqmoqdek tez ishlashi uchun 5 daqiqalik in-memory kesh.

---

## 🚀 Ishga Tushirish

### 1. Talablar:
- Python 3.10+
- Internet aloqasi

### 2. Kutubxonalarni o'rnatish:
```bash
pip install -r requirements.txt
```

### 3. Konfiguratsiya:
`.env` faylida Telegram bot tokeni ko'rsatiladi:
```env
BOT_TOKEN=your_bot_token_here
LOG_LEVEL=INFO
```

### 4. Botni ishga tushirish (Windows 1-click):
Faqatgina `start_bot.bat` fayliga 2 marta bosing yoki terminalda:
```bash
python runner.py
```

Oddiy rejimda:
```bash
python bot.py
```
