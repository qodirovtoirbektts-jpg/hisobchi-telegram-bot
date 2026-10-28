"""Inline keyboard builders for bot interactions."""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.i18n import t

def get_language_keyboard() -> InlineKeyboardMarkup:
    """Build language selection keyboard."""
    buttons = [
        [
            InlineKeyboardButton(text="🇺🇿 O'zbekcha (Lotin)", callback_data="set_lang:uz_lat"),
        ],
        [
            InlineKeyboardButton(text="🇺🇿 Ўзбекча (Кирилл)", callback_data="set_lang:uz_cyr"),
        ],
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_confirm_keyboard(action_type: str, item_id: str, lang: str = "uz_lat") -> InlineKeyboardMarkup:
    """Build confirmation inline keyboard for saving expense or debt."""
    buttons = [
        [
            InlineKeyboardButton(text=t("btn_confirm", lang), callback_data=f"confirm:{action_type}:{item_id}"),
            InlineKeyboardButton(text=t("btn_cancel", lang), callback_data=f"cancel:{action_type}:{item_id}"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_debts_keyboard(debts: list, lang: str = "uz_lat") -> InlineKeyboardMarkup:
    """Build keyboard to close debts."""
    buttons = []
    for d in debts:
        btn_text = t("btn_close_debt", lang, person=d.person_name, amount=d.amount)
        buttons.append([InlineKeyboardButton(text=btn_text, callback_data=f"close_debt:{d.id}")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
