# 💰 "Hisobchi" Telegram Boti

Ovozli va matnli xabarlarni sun'iy intellekt (Google Gemini Flash) yordamida avtomatik tahlil qilib, xarajatlar, qarzlar va eslatmalarni hisobga oluvchi ko'p tilli (O'zbek lotin/kirill, Rus) Telegram bot.

---

## 🛠 Texnologiyalar to'plami
- **Til:** Python 3.12+
- **Bot freymvorki:** [Aiogram 3.x](https://docs.aiogram.dev/) (to'liq asinxron)
- **Ma'lumotlar bazasi:** SQLite + [SQLAlchemy 2.0 (Async)](https://docs.sqlalchemy.org/) + `aiosqlite`
- **Rejalashtiruvchi:** [APScheduler](https://apscheduler.readthedocs.io/) (eslatmalar, qarz muddatlari va oylik hisobotlar)
- **Sun'iy Intellekt:** [Google Gemini API](https://ai.google.dev/) (`gemini-1.5-flash` orqali audio va matnni to'g'ridan-to'g'ri JSON formatga o'girish)
- **Xalqaro interfeys (i18n):** O'zbekcha (Lotin), Ўзбекча (Кирилл), Русский

---

## 📂 Loyiha tuzilishi

```text
d:/Telegram bot 1/
│
├── bot/
│   ├── handlers/          # Buyruqlar va xabarlar ishlovchilari
│   │   ├── __init__.py    # Routerlar agregatori
│   │   ├── start.py       # /start va /til buyruqlari
│   │   ├── expenses.py    # Xarajatlarni tasdiqlash va saqlash
│   │   ├── debts.py       # /qarzlar va qarzni "To'landi" qilish
│   │   ├── reports.py     # /bugun, /hafta, /oy hisobotlari
│   │   ├── voice.py       # Ovozli xabarlarni Gemini orqali tahlil qilish
│   │   └── text.py        # Erkin matnli xabarlarni tahlil qilish
│   │
│   ├── models/            # SQLAlchemy ORM modellari
│   │   ├── base.py        # DeclarativeBase va TimestampMixin
│   │   ├── user.py        # users jadvali
│   │   ├── expense.py     # expenses jadvali
│   │   ├── debt.py        # debts jadvali
│   │   └── reminder.py    # reminders jadvali
│   │
│   ├── middlewares/       # Aiogram middlewarelari
│   │   └── i18n.py        # Foydalanuvchini DB dan olish va tilni inyeksiya qilish
│   │
│   ├── keyboards/         # Inline tugmalar
│   │   └── inline.py      # Tasdiqlash, qarzlar va til menyulari
│   │
│   ├── services/          # Biznes mantiq xizmatlari
│   │   ├── db.py          # Asinxron sessiya va DB initsializatsiyasi
│   │   ├── gemini.py      # Gemini 1.5 Flash STT + JSON ekstraksiya
│   │   ├── scheduler.py   # APScheduler foniy vazifalari
│   │   └── pending.py     # Tasdiqlash kutayotgan operatsiyalar keshi
│   │
│   ├── utils/
│   │   ├── i18n.py        # 3 tildagi lug'at va formatlovchi
│   │   └── parser.py      # Regex / evristik zaxira tahlilchi
│   │
│   ├── config.py          # .env sozlamalari
│   └── main.py            # Botni ishga tushiruvchi asosiy modul
│
├── tests/                 # Pytest testlari
│   ├── test_parser.py     # Regex va mantiqiy tahlil testlari
│   └── test_models.py     # Baza va modellar integratsiya testi
│
├── run.py                 # Loyihani ishga tushiruvchi yagona fayl
├── requirements.txt       # Kerakli Python kutubxonalari
├── .env                   # Muhit parametrlari (Maxfiy tokenlar)
├── .env.example           # Muhit namunalari
├── Dockerfile             # Docker konteyner fayli
├── docker-compose.yml     # Docker Compose fayli
└── hisobchi.service       # Linux systemd xizmati
```

---

## 🚀 O'rnatish va Mahalliy Ishga Tushirish

### 1. Virtual muhitni faollashtirish va kutubxonalarni o'rnatish
```bash
# Virtual muhit yaratish (agar yaratilmagan bo'lsa)
python -m venv .venv

# Windows uchun faollashtirish
.\.venv\Scripts\activate

# Kutubxonalarni o'rnatish
pip install -r requirements.txt
```

### 2. .env faylini sozlash
`.env` faylida sizning Telegram Bot tokeningiz allaqachon sozlangan:
```env
BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=sizning_gemini_api_kalitingiz  # (Ovoz va matnni chuqur tahlil qilish uchun)
DB_URL=sqlite+aiosqlite:///hisobchi.db
DEFAULT_LANG=uz_lat
TIMEZONE=Asia/Tashkent
```

> **Eslatma:** Agar `GEMINI_API_KEY` kiritilmasa ham, bot o'zining ichki aqlli regex va evristik tahlilchisi orqali xarajat va qarzlarni muvaffaqiyatli aniqlay oladi! Gemini kalitini qo'shsangiz ovozli xabarlar va murakkab matnlar to'liq sun'iy intellekt quvvatida ishlaydi.

### 3. Botni ishga tushirish
```bash
python run.py
```

---

## 🤖 Bot Funksiyalari va Buyruqlari

### Asosiy Buyruqlar:
- `/start` - Botni ishga tushirish va qo'llanma
- `/til` yoki `/lang` - Bot tilini almashtirish (O'zbek lotin, kirill yoki rus)
- `/qarzlar` - Hozirgi barcha faol (yopilmagan) qarzlar ro'yxati va **"To'landi"** tugmasi
- `/bugun` - Bugungi barcha xarajatlar va kategoriyalar bo'yicha yig'indi
- `/hafta` - So'nggi 7 kunlik moliyaviy hisobot
- `/oy` - Ushbu oydagi barcha xarajatlar xulosasi

### Avtomatik Funksiyalar:
1. **Ovozli xabar yuborish:**
   - Foydalanuvchi ovozli xabar jo'natadi (masalan: *"Ali'ga 200 ming qarz berdim, 5-noyabrgacha qaytaradi"* yoki *"Taksiga 25000 to'ladim"*).
   - Bot ovozni tinglaydi, ma'lumotni chiqarib oladi va tasdiqlash uchun tugma chiqaradi: `[✅ Tasdiqlash] [❌ Bekor qilish]`.
2. **Xarajat toifasini avtomatik belgilash:**
   - *Oziq-ovqat, Transport, Kafe, Kommunal, Aloqa, Salomatlik, Kiyim, Boshqa*.
3. **Eslatmalar:**
   - Qarz muddati tugashidan 1 kun oldin va qarz to'lash kuni bot foydalanuvchiga eslatma jo'natadi.
   - Uchrashuv va eslatmalar belgilangan vaqtida bot orqali yetkaziladi.
4. **Oylik xulosa:**
   - Har oyning 1-sanasida soat 10:00 da bot barcha faol foydalanuvchilarga o'tgan oy sarf-xarajatlari bo'yicha hisobot taqdim etadi.

---

## 🧪 Testlarni Tekshirish (Test Check-list)

Loyihada barcha asosiy modellar va tahlil mexanizmlari bo'yicha testlar mavjud. Testlarni yurgizish uchun:

```bash
pytest -v
```

Natija:
- `test_create_and_read_user_expense` - Asinxron SQLite bazasi va modellarning to'g'ri ishlashi.
- `test_parse_amount` - 200 ming, 1.5 mln, 50k va so'm summalarining to'g'ri hisoblanishi.
- `test_detect_category` - Kalit so'zlar bo'yicha toifalarni aniqlash.
- `test_fallback_parse_debt` - Qarz va shaxs ismini to'g'ri ajratib olish.
- `test_fallback_parse_expense` - Xarajatlarni tahlil qilish.

---

## 🌐 VPS Serverga Joylashtirish (Deployment)

### Variant 1: Systemd orqali (Tavsiya etiladi)

1. Serverga Python va Git o'rnating:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git
   ```
2. Loyihani serverga nusxalang (masalan `/var/www/hisobchi` papkasiga).
3. Virtual muhit va bog'liqliklarni o'rnating:
   ```bash
   cd /var/www/hisobchi
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. `.env` faylini to'ldiring:
   ```bash
   nano .env
   ```
5. Systemd xizmatini yoqing:
   ```bash
   sudo cp hisobchi.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable hisobchi
   sudo systemctl start hisobchi
   sudo systemctl status hisobchi
   ```

### Variant 2: Docker orqali
```bash
docker-compose up -d --build
```
Jurnallarni kuzatish:
```bash
docker-compose logs -f
```
