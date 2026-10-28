"""Heuristic regex-based parser as fallback for Gemini API."""
import re
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

CATEGORIES = {
    "oziq-ovqat": ["ovqat", "non", "gosht", "go'sht", "bozor", "supermarket", "lavash", "osh", "tushlik", "choy", "suv", "yegulik", "еда", "продукты", "обед"],
    "transport": ["taksi", "taxi", "yandex", "metro", "avtobus", "benzin", "yo'lkira", "yolkira", "проезд", "такси", "бензин"],
    "kafe": ["restoran", "qahva", "kofe", "coffee", "kafe", "choyxona", "кафе", "ресторан"],
    "kommunal": ["svet", "gaz", "suv", "arenda", "ijara", "kvartira", "kommunal", "коммуналка", "аренда"],
    "aloqa": ["internet", "telefon", "payme", "click", "tarif", "связь", "интернет"],
    "salomatlik": ["dori", "apteka", "shifokor", "doktor", "klinika", "apteka", "лекарства", "аптека"],
    "kiyim": ["kiyim", "shim", "ko'ylak", "koylak", "oyoqkiyim", "etik", "odejda", "одежда"],
}

def parse_amount(text: str) -> Optional[float]:
    """Extract numeric amount considering 'ming', 'mln', 'k' multipliers."""
    # Match patterns like: 200 ming, 200k, 1.5 mln, 200000, 200 000
    cleaned = text.lower().replace(" ", "").replace(",", ".")
    
    # Check for ming / k
    ming_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:ming|k|тыс)", text, re.IGNORECASE)
    if ming_match:
        return float(ming_match.group(1)) * 1000

    # Check for mln
    mln_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:mln|million|миллион|млн)", text, re.IGNORECASE)
    if mln_match:
        return float(mln_match.group(1)) * 1000000

    # Plain digits
    digits_match = re.search(r"(\d{3,}(?:\.\d+)?)", text)
    if digits_match:
        return float(digits_match.group(1))

    return None

def detect_category(text: str) -> str:
    """Detect category from text keywords."""
    lowered = text.lower()
    for category, keywords in CATEGORIES.items():
        for kw in keywords:
            if kw in lowered:
                return category
    return "boshqa"

def fallback_parse_text(text: str) -> Dict[str, Any]:
    """Parse text using regex when Gemini is unavailable."""
    lowered = text.lower()
    amount = parse_amount(text)

    # Debt check
    if any(w in lowered for w in ["qarz", "qarzga", "долг", "карз", "қарз", "berdim", "oldim"]):
        debt_type = "taken" if any(w in lowered for w in ["oldim", "vzyal", "взял"]) else "given"
        # Try extracting person name
        # e.g. "Ali'ga 200 ming" or "Aliga 200 ming" or "Ali dan 200 ming"
        person_match = re.search(r"([A-ZА-ЯЁa-zа-яё\']+?)(?:['’`]?ga|['’`]?dan|['’`]?га|['’`]?дан)?\s+\d+", text, re.IGNORECASE)
        person_name = person_match.group(1).replace("'", "").replace("’", "").strip().capitalize() if person_match else "Noma'lum shaxs"
        
        return {
            "type": "debt",
            "data": {
                "person_name": person_name,
                "amount": amount or 0.0,
                "debt_type": debt_type,
                "due_date": None,
                "description": text
            },
            "raw_text": text
        }

    # Reminder check
    if any(w in lowered for w in ["eslat", "eslatma", "uchrashuv", "soat", "napomni", "напомни", "эслат"]):
        remind_time = datetime.now() + timedelta(hours=1)
        return {
            "type": "reminder",
            "data": {
                "title": text,
                "remind_at": remind_time.strftime("%Y-%m-%d %H:%M:%S"),
                "reminder_type": "meeting" if any(w in lowered for w in ["uchrashuv", "vstrecha", "встреча"]) else "general"
            },
            "raw_text": text
        }

    # Expense check (default if amount is present)
    if amount:
        category = detect_category(text)
        return {
            "type": "expense",
            "data": {
                "amount": amount,
                "category": category,
                "description": text
            },
            "raw_text": text
        }

    return {
        "type": "unknown",
        "data": {},
        "raw_text": text
    }
