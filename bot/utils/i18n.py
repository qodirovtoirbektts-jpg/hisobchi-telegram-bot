"""Internationalization (i18n) dictionary and helper functions."""
from typing import Dict, Any

MESSAGES: Dict[str, Dict[str, str]] = {
    "uz_lat": {
        "welcome": (
            "Assalomu alaykum, <b>{name}</b>!\n\n"
            "Men <b>\"Hisobchi\"</b> botiman. Siz menga matn yoki ovozli xabar yuborishingiz mumkin.\n"
            "Men avtomatik ravishda:\n"
            "💸 <b>Xarajatlarni</b> toifalarga ajrataman\n"
            "🤝 <b>Qarzlarni</b> hisobga olaman\n"
            "⏰ <b>Eslatmalar</b> o'rnataman\n\n"
            "Buyruqlar:\n"
            "/start - Botni qayta ishga tushirish\n"
            "/qarzlar - Qarzlar ro'yxati\n"
            "/bugun - Bugungi hisobot\n"
            "/hafta - Haftalik hisobot\n"
            "/oy - Oylik hisobot\n"
            "/til - Tilni o'zgartirish"
        ),
        "choose_language": "Tilni tanlang / Выберите язык / Тилни танланг:",
        "lang_changed": "Muvaffaqiyatli o'zbek tiliga o'tkazildi (Lotin).",
        "confirm_expense": (
            "💸 <b>Xarajat aniqlandi:</b>\n\n"
            "💵 Miqdor: <b>{amount:,.0f} so'm</b>\n"
            "📁 Kategoriya: <b>{category}</b>\n"
            "📝 Izoh: <i>{description}</i>\n\n"
            "Saqlashni tasdiqlaysizmi?"
        ),
        "expense_saved": "✅ Xarajat muvaffaqiyatli saqlandi!",
        "cancelled": "❌ Bekor qilindi.",
        "confirm_debt": (
            "🤝 <b>Qarz ma'lumoti:</b>\n\n"
            "👤 Shaxs: <b>{person}</b>\n"
            "💵 Miqdor: <b>{amount:,.0f} so'm</b>\n"
            "🔄 Turi: <b>{debt_type}</b>\n"
            "📅 Muddat: <b>{due_date}</b>\n\n"
            "Saqlashni tasdiqlaysizmi?"
        ),
        "debt_saved": "✅ Qarz ma'lumoti saqlandi!",
        "debt_given": "Berilgan qarz",
        "debt_taken": "Olingan qarz",
        "no_due_date": "Belgilanmagan",
        "reminder_saved": "⏰ Eslatma saqlandi:\n<b>{title}</b>\n📅 Vaqt: <b>{time}</b>",
        "unknown_format": "Kechirasiz, xabaringizdan xarajat yoki qarz ma'lumotini aniqlab bo'lmadi. Iltimos, aniqroq yozing yoki ovoz yuboring.",
        "debts_empty": "Sizda faol qarzlar yo'q.",
        "debts_title": "📋 <b>Faol qarzlar ro'yxati:</b>\n\n",
        "debt_item": "{index}. {type_icon} <b>{person}</b>: {amount:,.0f} so'm (Muddati: {due_date})\n",
        "btn_close_debt": "✅ {person} ({amount:,.0f}) - To'landi",
        "debt_closed": "🎉 Qarz yopildi!",
        "report_title": "📊 <b>{period} bo'yicha hisobot:</b>\n\n",
        "report_total": "Jami xarajat: <b>{total:,.0f} so'm</b>\n\n",
        "report_by_category": "📂 <b>Kategoriyalar bo'yicha:</b>\n",
        "report_item": "• {category}: <b>{amount:,.0f} so'm</b>\n",
        "report_empty": "Ushbu davr uchun hech qanday xarajat topilmadi.",
        "btn_confirm": "✅ Tasdiqlash",
        "btn_cancel": "❌ Bekor qilish",
        "reminder_alert": "⏰ <b>Eslatma!</b>\n\n{title}",
        "debt_reminder_alert": "⚠️ <b>Qarz eslatmasi!</b>\n\n{person} bilan bog'liq {amount:,.0f} so'm qarzingiz muddati {due_text}!",
        "error_occurred": "Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring."
    },
    "uz_cyr": {
        "welcome": (
            "Ассалому алайкум, <b>{name}</b>!\n\n"
            "Мен <b>\"Ҳисобчи\"</b> ботиман. Сиз менга матн ёки овозли хабар юборишингиз мумкин.\n"
            "Мен автоматик равишда:\n"
            "💸 <b>Харажатларни</b> тоифаларга ажратаман\n"
            "🤝 <b>Қарзларни</b> ҳисобга оламан\n"
            "⏰ <b>Эслатмалар</b> ўрнатаман\n\n"
            "Буйруқлар:\n"
            "/start - Ботни қайта ишга тушириш\n"
            "/qarzlar - Қарзлар рўйхати\n"
            "/bugun - Бугунги ҳисобот\n"
            "/hafta - Ҳафталик ҳисобот\n"
            "/oy - Ойлик ҳисобот\n"
            "/til - Тилни ўзгартириш"
        ),
        "choose_language": "Тилни танланг / Выберите язык / Tilni tanlang:",
        "lang_changed": "Муваффақиятли ўзбек тилига ўтказилди (Кирилл).",
        "confirm_expense": (
            "💸 <b>Харажат аниқланди:</b>\n\n"
            "💵 Миқдор: <b>{amount:,.0f} сўм</b>\n"
            "📁 Категория: <b>{category}</b>\n"
            "📝 Изоҳ: <i>{description}</i>\n\n"
            "Сақлашни тасдиқлайсизми?"
        ),
        "expense_saved": "✅ Харажат муваффақиятли сақланди!",
        "cancelled": "❌ Бекор қилинди.",
        "confirm_debt": (
            "🤝 <b>Қарз маълумоти:</b>\n\n"
            "👤 Шахс: <b>{person}</b>\n"
            "💵 Миқдор: <b>{amount:,.0f} сўм</b>\n"
            "🔄 Тури: <b>{debt_type}</b>\n"
            "📅 Муддат: <b>{due_date}</b>\n\n"
            "Сақлашни тасдиқлайсизми?"
        ),
        "debt_saved": "✅ Қарз маълумоти сақланди!",
        "debt_given": "Берилган қарз",
        "debt_taken": "Олинган қарз",
        "no_due_date": "Белгиланмаган",
        "reminder_saved": "⏰ Эслатма сақланди:\n<b>{title}</b>\n📅 Вақт: <b>{time}</b>",
        "unknown_format": "Кечирасиз, хабарингиздан харажат ёки қарз маълумотини аниқлаб бўлмади. Илтимос, аниқроқ ёзинг ёки овоз юборинг.",
        "debts_empty": "Сизда фаол қарзлар йўқ.",
        "debts_title": "📋 <b>Фаол қарзлар рўйхати:</b>\n\n",
        "debt_item": "{index}. {type_icon} <b>{person}</b>: {amount:,.0f} сўм (Муддати: {due_date})\n",
        "btn_close_debt": "✅ {person} ({amount:,.0f}) - Тўланди",
        "debt_closed": "🎉 Қарз ёпилди!",
        "report_title": "📊 <b>{period} бўйича ҳисобот:</b>\n\n",
        "report_total": "Жами харажат: <b>{total:,.0f} сўм</b>\n\n",
        "report_by_category": "📂 <b>Категориялар бўйича:</b>\n",
        "report_item": "• {category}: <b>{amount:,.0f} сўм</b>\n",
        "report_empty": "Ушбу давр учун ҳеч қандай харажат топилмади.",
        "btn_confirm": "✅ Тасдиқлаш",
        "btn_cancel": "❌ Бекор қилиш",
        "reminder_alert": "⏰ <b>Эслатма!</b>\n\n{title}",
        "debt_reminder_alert": "⚠️ <b>Қарз эслатмаси!</b>\n\n{person} билан боғлиқ {amount:,.0f} сўм қарзингиз муддати {due_text}!",
        "error_occurred": "Хатолик юз берди. Илтимос, кейинроқ қайта уриниб кўринг."
    },
    "ru": {
        "welcome": (
            "Здравствуйте, <b>{name}</b>!\n\n"
            "Я бот <b>«Бухгалтер» (Hisobchi)</b>. Вы можете отправлять мне текстовые или голосовые сообщения.\n"
            "Я автоматически:\n"
            "💸 Распределяю <b>расходы</b> по категориям\n"
            "🤝 Веду учет <b>долгов</b>\n"
            "⏰ Устанавливаю <b>напоминания</b>\n\n"
            "Команды:\n"
            "/start - Перезапуск бота\n"
            "/qarzlar - Список долгов\n"
            "/bugun - Отчет за сегодня\n"
            "/hafta - Отчет за неделю\n"
            "/oy - Отчет за месяц\n"
            "/til - Сменить язык"
        ),
        "choose_language": "Выберите язык / Tilni tanlang / Тилни танланг:",
        "lang_changed": "Язык успешно изменен на русский.",
        "confirm_expense": (
            "💸 <b>Расход распознан:</b>\n\n"
            "💵 Сумма: <b>{amount:,.0f} сум</b>\n"
            "📁 Категория: <b>{category}</b>\n"
            "📝 Описание: <i>{description}</i>\n\n"
            "Подтверждаете сохранение?"
        ),
        "expense_saved": "✅ Расход успешно сохранен!",
        "cancelled": "❌ Отменено.",
        "confirm_debt": (
            "🤝 <b>Запись о долге:</b>\n\n"
            "👤 Лицо: <b>{person}</b>\n"
            "💵 Сумма: <b>{amount:,.0f} сум</b>\n"
            "🔄 Тип: <b>{debt_type}</b>\n"
            "📅 Срок: <b>{due_date}</b>\n\n"
            "Подтверждаете сохранение?"
        ),
        "debt_saved": "✅ Запись о долге сохранена!",
        "debt_given": "Дал в долг",
        "debt_taken": "Взял в долг",
        "no_due_date": "Не указан",
        "reminder_saved": "⏰ Напоминание сохранено:\n<b>{title}</b>\n📅 Время: <b>{time}</b>",
        "unknown_format": "Извините, не удалось распознать расход или долг. Попробуйте уточнить или отправить голосовое сообщение.",
        "debts_empty": "У вас нет активных долгов.",
        "debts_title": "📋 <b>Список активных долгов:</b>\n\n",
        "debt_item": "{index}. {type_icon} <b>{person}</b>: {amount:,.0f} сум (Срок: {due_date})\n",
        "btn_close_debt": "✅ {person} ({amount:,.0f}) - Закрыть",
        "debt_closed": "🎉 Долг закрыт!",
        "report_title": "📊 <b>Отчет за {period}:</b>\n\n",
        "report_total": "Всего расходов: <b>{total:,.0f} сум</b>\n\n",
        "report_by_category": "📂 <b>По категориям:</b>\n",
        "report_item": "• {category}: <b>{amount:,.0f} сум</b>\n",
        "report_empty": "За данный период расходов не найдено.",
        "btn_confirm": "✅ Подтвердить",
        "btn_cancel": "❌ Отмена",
        "reminder_alert": "⏰ <b>Напоминание!</b>\n\n{title}",
        "debt_reminder_alert": "⚠️ <b>Напоминание о долге!</b>\n\nСрок долга {person} на сумму {amount:,.0f} сум {due_text}!",
        "error_occurred": "Произошла ошибка. Пожалуйста, попробуйте позже."
    }
}

def t(key: str, lang: str = "uz_lat", **kwargs: Any) -> str:
    """Get localized string by key and format parameters."""
    if lang not in MESSAGES:
        lang = "uz_lat"
    text = MESSAGES[lang].get(key, MESSAGES["uz_lat"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
