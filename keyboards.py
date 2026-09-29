"""
keyboards.py - Inline keyboards and builders for all categories, specs, and result navigation
"""

from typing import List, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from catalog import (
    BRANDS, APPLE_TYPES, MACBOOK_MODELS, IPHONE_MODELS, IPAD_MODELS,
    MAC_DESKTOP_MODELS, APPLE_WATCH_MODELS, AIRPODS_MODELS,
    WINDOWS_BRANDS, WINDOWS_MODELS, SAMSUNG_SERIES, SAMSUNG_MODELS,
    XIAOMI_SERIES, XIAOMI_MODELS, OTHER_GADGETS,
    RAM_OPTIONS_MAC, RAM_OPTIONS_WIN, STORAGE_OPTIONS, STORAGE_OPTIONS_PHONE,
    GPU_OPTIONS_WIN, BATTERY_HEALTH_OPTIONS
)


def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main Category selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🍏 Apple", callback_data="brand:apple")
    builder.button(text="📱 Samsung", callback_data="brand:samsung")
    builder.button(text="⚡ Xiaomi / Redmi", callback_data="brand:xiaomi")
    builder.button(text="💻 Windows Noutbuklar", callback_data="brand:windows")
    builder.button(text="🎮 Boshqa Gadjetlar", callback_data="brand:other")
    builder.button(text="🏬 Do'konlar & Telegram Kanallar", callback_data="nav:channels_menu")
    builder.button(text="📢 Malika & Abu Saxiy Bozorlari", callback_data="channels:bazaars")
    builder.button(text="🔍 Erkin qidiruv (Yozib topish)", callback_data="action:free_search")
    builder.button(text="ℹ️ Bot haqida & Yordam", callback_data="action:help")
    builder.adjust(2, 2, 1, 1, 1, 1, 1)
    return builder.as_markup()


def get_apple_types_keyboard() -> InlineKeyboardMarkup:
    """Apple subcategories keyboard"""
    builder = InlineKeyboardBuilder()
    for item in APPLE_TYPES:
        builder.button(text=item["name"], callback_data=f"apple_type:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup()


def get_macbook_models_keyboard() -> InlineKeyboardMarkup:
    """MacBook models list"""
    builder = InlineKeyboardBuilder()
    for item in MACBOOK_MODELS:
        builder.button(text=item["name"], callback_data=f"mac_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2)
    return builder.as_markup()


def get_iphone_models_keyboard() -> InlineKeyboardMarkup:
    """iPhone models list"""
    builder = InlineKeyboardBuilder()
    for item in IPHONE_MODELS:
        builder.button(text=item["name"], callback_data=f"iph_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2)
    return builder.as_markup()


def get_ipad_models_keyboard() -> InlineKeyboardMarkup:
    """iPad models list"""
    builder = InlineKeyboardBuilder()
    for item in IPAD_MODELS:
        builder.button(text=item["name"], callback_data=f"ipad_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2)
    return builder.as_markup()


def get_mac_desktop_keyboard() -> InlineKeyboardMarkup:
    """Mac mini / iMac / Studio list"""
    builder = InlineKeyboardBuilder()
    for item in MAC_DESKTOP_MODELS:
        builder.button(text=item["name"], callback_data=f"macdesk_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 2)
    return builder.as_markup()


def get_apple_watch_keyboard() -> InlineKeyboardMarkup:
    """Apple Watch models"""
    builder = InlineKeyboardBuilder()
    for item in APPLE_WATCH_MODELS:
        builder.button(text=item["name"], callback_data=f"aw_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup()


def get_airpods_keyboard() -> InlineKeyboardMarkup:
    """AirPods models"""
    builder = InlineKeyboardBuilder()
    for item in AIRPODS_MODELS:
        builder.button(text=item["name"], callback_data=f"airp_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:apple")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 1, 2)
    return builder.as_markup()


# ----------------- WINDOWS LAPTOPS KEYBOARDS -----------------

def get_windows_brands_keyboard() -> InlineKeyboardMarkup:
    """Windows laptop brands"""
    builder = InlineKeyboardBuilder()
    for item in WINDOWS_BRANDS:
        builder.button(text=item["name"], callback_data=f"win_brand:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 1, 2)
    return builder.as_markup()


def get_windows_models_keyboard(brand_id: str) -> InlineKeyboardMarkup:
    """Models for chosen Windows laptop brand (Victus, Legion, TUF, etc.)"""
    models = WINDOWS_MODELS.get(brand_id, WINDOWS_MODELS["all_win"])
    builder = InlineKeyboardBuilder()
    for item in models:
        builder.button(text=item["name"], callback_data=f"win_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:windows")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 1, 2)
    return builder.as_markup()


# ----------------- SAMSUNG KEYBOARDS -----------------

def get_samsung_series_keyboard() -> InlineKeyboardMarkup:
    """Samsung series list"""
    builder = InlineKeyboardBuilder()
    for item in SAMSUNG_SERIES:
        builder.button(text=item["name"], callback_data=f"sam_ser:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 2)
    return builder.as_markup()


def get_samsung_models_keyboard(series_id: str) -> InlineKeyboardMarkup:
    """Samsung models for selected series"""
    models = SAMSUNG_MODELS.get(series_id, [])
    builder = InlineKeyboardBuilder()
    for item in models:
        builder.button(text=item["name"], callback_data=f"sam_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:samsung")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2)
    return builder.as_markup()


# ----------------- XIAOMI KEYBOARDS -----------------

def get_xiaomi_series_keyboard() -> InlineKeyboardMarkup:
    """Xiaomi series list"""
    builder = InlineKeyboardBuilder()
    for item in XIAOMI_SERIES:
        builder.button(text=item["name"], callback_data=f"mi_ser:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()


def get_xiaomi_models_keyboard(series_id: str) -> InlineKeyboardMarkup:
    """Xiaomi models for selected series"""
    models = XIAOMI_MODELS.get(series_id, [])
    builder = InlineKeyboardBuilder()
    for item in models:
        builder.button(text=item["name"], callback_data=f"mi_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="brand:xiaomi")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2)
    return builder.as_markup()


# ----------------- OTHER GADGETS KEYBOARD -----------------

def get_other_gadgets_keyboard() -> InlineKeyboardMarkup:
    """Other gadgets (PlayStation, Xbox, Drones)"""
    builder = InlineKeyboardBuilder()
    for item in OTHER_GADGETS:
        builder.button(text=item["name"], callback_data=f"oth_mod:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 1, 1, 2)
    return builder.as_markup()


# ----------------- SPECS KEYBOARDS -----------------

def get_ram_keyboard(device_category: str = "mac", back_cb: str = "nav:main_menu") -> InlineKeyboardMarkup:
    """RAM selection buttons"""
    options = RAM_OPTIONS_MAC if device_category == "mac" else RAM_OPTIONS_WIN
    builder = InlineKeyboardBuilder()
    for item in options:
        builder.button(text=item["label"], callback_data=f"spec_ram:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data=back_cb)
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2)
    return builder.as_markup()


def get_storage_keyboard(is_phone: bool = False, back_cb: str = "nav:main_menu") -> InlineKeyboardMarkup:
    """SSD / ROM storage options"""
    options = STORAGE_OPTIONS_PHONE if is_phone else STORAGE_OPTIONS
    builder = InlineKeyboardBuilder()
    for item in options:
        builder.button(text=item["label"], callback_data=f"spec_ssd:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data=back_cb)
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2)
    return builder.as_markup()


def get_gpu_keyboard(back_cb: str = "nav:main_menu") -> InlineKeyboardMarkup:
    """GPU options for Windows laptops"""
    builder = InlineKeyboardBuilder()
    for item in GPU_OPTIONS_WIN:
        builder.button(text=item["label"], callback_data=f"spec_gpu:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data=back_cb)
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 2, 2, 2)
    return builder.as_markup()


def get_battery_keyboard(back_cb: str = "nav:main_menu") -> InlineKeyboardMarkup:
    """Battery Health (Yomkist) buttons"""
    builder = InlineKeyboardBuilder()
    for item in BATTERY_HEALTH_OPTIONS:
        builder.button(text=item["label"], callback_data=f"spec_bat:{item['id']}")
    builder.button(text="🔙 Orqaga", callback_data=back_cb)
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(2, 2, 1, 2)
    return builder.as_markup()


def get_channels_menu_keyboard() -> InlineKeyboardMarkup:
    """Channels & Stores category selection keyboard"""
    builder = InlineKeyboardBuilder()
    builder.button(text="🍏 Apple Do'konlari (MacBro, BroStore...)", callback_data="channels:apple")
    builder.button(text="💻 Noutbuklar & Gaming (Nout.uz, CompStore...)", callback_data="channels:windows")
    builder.button(text="📱 Samsung & Xiaomi (Mi Store, Abu Saxiy...)", callback_data="channels:android")
    builder.button(text="🏛️ Malika & Bozorlar (Malika Bozori, Optom)", callback_data="channels:bazaars")
    builder.button(text="🔙 Orqaga", callback_data="nav:main_menu")
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    builder.adjust(1, 1, 1, 1, 2)
    return builder.as_markup()


# ----------------- RESULT NAVIGATION KEYBOARD -----------------

def get_result_card_keyboard(
    current_index: int,
    total_count: int,
    offer_url: str,
    back_cb: str = "nav:main_menu"
) -> InlineKeyboardMarkup:
    """Navigation for browsing found OLX offers"""
    builder = InlineKeyboardBuilder()
    
    # Prev / Next pagination buttons
    prev_cb = f"res_page:{current_index - 1}" if current_index > 0 else "noop"
    next_cb = f"res_page:{current_index + 1}" if current_index < total_count - 1 else "noop"
    
    prev_text = "⬅️ Oldingi" if current_index > 0 else "⛔ Boshida"
    next_text = "Keyingi ➡️" if current_index < total_count - 1 else "⛔ Oxirida"
    counter_text = f"📍 {current_index + 1}/{total_count}"

    builder.button(text=prev_text, callback_data=prev_cb)
    builder.button(text=counter_text, callback_data="noop")
    builder.button(text=next_text, callback_data=next_cb)

    # Direct Web link to OLX
    if offer_url and offer_url.startswith("http"):
        builder.button(text="🌐 OLX da ko'rish (Havola)", url=offer_url)

    # Direct access to stores & channels for this device
    builder.button(text="🏬 Do'konlar & Kanallardagi narxlar", callback_data="action:related_channels")

    # Actions: List view & Repeat
    builder.button(text="📋 Barcha e'lonlar ro'yxati", callback_data="action:list_view")
    builder.button(text="🔄 Qayta qidirish", callback_data=back_cb)

    # Navigation
    builder.button(text="🔙 Orqaga", callback_data=back_cb)
    builder.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")

    builder.adjust(3, 1, 1, 2, 2)
    return builder.as_markup()
