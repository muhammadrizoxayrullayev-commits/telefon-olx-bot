"""
handlers.py - Aiogram 3 routers, handlers, FSM states and rich UI rendering
Handles brand/category navigation, specs selection, OLX search execution, and pagination.
"""

import html
import logging
from typing import Dict, Any, List

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message, CallbackQuery, InputMediaPhoto, BufferedInputFile
)

from catalog import (
    APPLE_TYPES, MACBOOK_MODELS, IPHONE_MODELS, IPAD_MODELS,
    MAC_DESKTOP_MODELS, APPLE_WATCH_MODELS, AIRPODS_MODELS,
    WINDOWS_BRANDS, WINDOWS_MODELS, SAMSUNG_SERIES, SAMSUNG_MODELS,
    XIAOMI_SERIES, XIAOMI_MODELS, OTHER_GADGETS,
    RAM_OPTIONS_MAC, RAM_OPTIONS_WIN, STORAGE_OPTIONS, STORAGE_OPTIONS_PHONE,
    GPU_OPTIONS_WIN, BATTERY_HEALTH_OPTIONS
)
from keyboards import (
    get_main_menu_keyboard, get_apple_types_keyboard,
    get_macbook_models_keyboard, get_iphone_models_keyboard,
    get_ipad_models_keyboard, get_mac_desktop_keyboard,
    get_apple_watch_keyboard, get_airpods_keyboard,
    get_windows_brands_keyboard, get_windows_models_keyboard,
    get_samsung_series_keyboard, get_samsung_models_keyboard,
    get_xiaomi_series_keyboard, get_xiaomi_models_keyboard,
    get_other_gadgets_keyboard, get_ram_keyboard,
    get_storage_keyboard, get_gpu_keyboard, get_battery_keyboard,
    get_result_card_keyboard
)
from olx_service import smart_search, download_image_bytes

logger = logging.getLogger(__name__)
router = Router()


class SearchWizard(StatesGroup):
    choosing_brand = State()
    choosing_category = State()
    choosing_model = State()
    choosing_ram = State()
    choosing_storage = State()
    choosing_gpu = State()
    choosing_battery = State()
    waiting_for_free_text = State()
    browsing_results = State()


# ----------------- /start and /help -----------------

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Start command handler"""
    await state.clear()
    welcome_text = (
        "👋 <b>Assalomu alaykum!</b>\n\n"
        "🤖 <b>OLX Gadgets & Telefon Qidiruvchi Botiga xush kelibsiz!</b>\n\n"
        "Bu bot orqali siz O'zbekiston bo'ylab <b>OLX.uz</b> platformasidagi eng so'nggi va qulay e'lonlarni "
        "aniq texnik ko'rsatkichlari (RAM, Xotira, Yomkist / Batareya, GPU) bo'yicha saralab topishingiz mumkin.\n\n"
        "👇 <b>Quyidagi bo'limlardan birini tanlang:</b>"
    )
    await message.answer(welcome_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Help command handler"""
    help_text = (
        "📖 <b>Botdan foydalanish qo'llanmasi:</b>\n\n"
        "1️⃣ <b>Brend yoki Bo'limni tanlang:</b> Apple, Samsung, Xiaomi, Windows Noutbuklar yoki Boshqa gadjetlar.\n"
        "2️⃣ <b>Kerakli modelni tanlang:</b> Masalan, MacBook Pro M3 Pro, HP Victus 16 yoki iPhone 15 Pro.\n"
        "3️⃣ <b>Xarakteristikalarni belgilang:</b> RAM (operativka), SSD/ROM va Yomkist (batareya salomatligi).\n"
        "4️⃣ Bot siz uchun OLX dan barcha e'lonlarni rasmlari, narxi, manzili, yomkisti va to'g'ridan-to'g'ri havolasi bilan topib beradi!\n\n"
        "💡 <i>Shuningdek, istalgan vaqtda botga to'g'ridan-to'g'ri matn yuborishingiz mumkin (Masalan: 'hp victus rtx 4060' yoki 'macbook m3 pro 18gb').</i>"
    )
    await message.answer(help_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")


# ----------------- MAIN NAVIGATION -----------------

@router.callback_query(F.data == "nav:main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    """Return to main menu"""
    await state.clear()
    text = (
        "🏠 <b>Bosh menyu</b>\n\n"
        "Qaysi brend yoki gadjet turini qidirmoqchisiz? Quyidagilardan birini tanlang:"
    )
    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
        else:
            await call.message.edit_text(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    await call.answer()


@router.callback_query(F.data == "action:help")
async def cb_help(call: CallbackQuery):
    await call.answer()
    help_text = (
        "ℹ️ <b>OLX Gadgets Bot haqida:</b>\n\n"
        "• <b>24/7 Rejim:</b> Bot uzluksiz ishlaydi va OLX dagi eng yangi takliflarni saralaydi.\n"
        "• <b>Aniq filtrlar:</b> Model, RAM, Doimiy xotira (SSD/ROM), Batareya (Yomkist) foizi va Video karta.\n"
        "• <b>Smart Search:</b> Agar juda kamyob parametr tanlasangiz ham, bot sizni bo'sh qoldirmaydi va eng yaqin mos takliflarni ko'rsatadi.\n\n"
        "Qidiruvni boshlash uchun quyidagi tugmalardan birini bosing:"
    )
    try:
        await call.message.edit_text(help_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
    except Exception:
        await call.message.answer(help_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")


@router.callback_query(F.data == "action:free_search")
async def cb_free_search_prompt(call: CallbackQuery, state: FSMContext):
    """Prompt user to type a free-text search"""
    await state.set_state(SearchWizard.waiting_for_free_text)
    text = (
        "🔍 <b>Erkin qidiruv rejimi:</b>\n\n"
        "Qidirayotgan gadjetingiz nomini matn orqali yozib yuboring.\n"
        "<i>Masalan:</i>\n"
        "• <code>Macbook Air M2 16gb</code>\n"
        "• <code>HP Victus 16 RTX 4060</code>\n"
        "• <code>iPhone 15 Pro Max 256gb yomkist 100</code>\n"
        "• <code>PlayStation 5 Slim</code>\n\n"
        "✍️ <i>Xabaringizni yozing:</i>"
    )
    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, parse_mode="HTML")
        else:
            await call.message.edit_text(text, parse_mode="HTML")
    except Exception:
        await call.message.answer(text, parse_mode="HTML")
    await call.answer()


# ----------------- BRAND SELECTION -----------------

@router.callback_query(F.data.startswith("brand:"))
async def cb_brand_selected(call: CallbackQuery, state: FSMContext):
    brand_id = call.data.split(":")[1]
    await state.update_data(brand=brand_id)
    await call.answer()

    if brand_id == "apple":
        text = "🍏 <b>Apple bo'limi:</b>\nQaysi mahsulot turini qidirmoqchisiz?"
        reply_markup = get_apple_types_keyboard()
    elif brand_id == "windows":
        text = "💻 <b>Windows Noutbuklar:</b>\nQaysi brenddagi noutbuk qiziqtiryapti?"
        reply_markup = get_windows_brands_keyboard()
    elif brand_id == "samsung":
        text = "📱 <b>Samsung bo'limi:</b>\nQaysi seriyadagi qurilma kerak?"
        reply_markup = get_samsung_series_keyboard()
    elif brand_id == "xiaomi":
        text = "⚡ <b>Xiaomi / Redmi / POCO bo'limi:</b>\nQaysi seriyani tanlaysiz?"
        reply_markup = get_xiaomi_series_keyboard()
    elif brand_id == "other":
        text = "🎮 <b>Boshqa Gadjetlar:</b>\nQaysi qurilma bo'yicha e'lonlar kerak?"
        reply_markup = get_other_gadgets_keyboard()
    else:
        text = "Qurilma turini tanlang:"
        reply_markup = get_main_menu_keyboard()

    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")
        else:
            await call.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")
    except Exception:
        await call.message.answer(text, reply_markup=reply_markup, parse_mode="HTML")


# ----------------- APPLE FLOW -----------------

@router.callback_query(F.data.startswith("apple_type:"))
async def cb_apple_type_selected(call: CallbackQuery, state: FSMContext):
    apple_type = call.data.split(":")[1]
    await state.update_data(device_category=apple_type)
    await call.answer()

    if apple_type == "macbook":
        text = "💻 <b>MacBook modelini / chipini tanlang:</b>"
        kb = get_macbook_models_keyboard()
    elif apple_type == "iphone":
        text = "📱 <b>iPhone rusumini tanlang:</b>"
        kb = get_iphone_models_keyboard()
    elif apple_type == "ipad":
        text = "📟 <b>iPad modelini tanlang:</b>"
        kb = get_ipad_models_keyboard()
    elif apple_type == "mac_desktop":
        text = "🖥️ <b>Mac Desktop modelini tanlang:</b>"
        kb = get_mac_desktop_keyboard()
    elif apple_type == "apple_watch":
        text = "⌚ <b>Apple Watch modelini tanlang:</b>"
        kb = get_apple_watch_keyboard()
    elif apple_type == "airpods":
        text = "🎧 <b>AirPods modelini tanlang:</b>"
        kb = get_airpods_keyboard()
    else:
        text = "Modelni tanlang:"
        kb = get_main_menu_keyboard()

    await call.message.edit_text(text, reply_markup=kb, parse_mode="HTML")


# MacBook Model Selected -> Ask RAM
@router.callback_query(F.data.startswith("mac_mod:"))
async def cb_mac_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in MACBOOK_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "MacBook"
    model_name = target["name"] if target else "MacBook"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="macbook"
    )
    await call.answer()

    text = (
        f"Selected: <b>{model_name}</b>\n\n"
        f"🧠 <b>RAM (Operativ xotira) hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_ram_keyboard("mac", back_cb=f"apple_type:macbook"),
        parse_mode="HTML"
    )


# iPhone Model Selected -> Ask Storage
@router.callback_query(F.data.startswith("iph_mod:"))
async def cb_iphone_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in IPHONE_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "iPhone"
    model_name = target["name"] if target else "iPhone"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="iphone"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"💾 <b>Xotira (ROM) hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_storage_keyboard(is_phone=True, back_cb="apple_type:iphone"),
        parse_mode="HTML"
    )


# iPad Model Selected -> Ask Storage
@router.callback_query(F.data.startswith("ipad_mod:"))
async def cb_ipad_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in IPAD_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "iPad"
    model_name = target["name"] if target else "iPad"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="ipad"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"💾 <b>Xotira hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_storage_keyboard(is_phone=True, back_cb="apple_type:ipad"),
        parse_mode="HTML"
    )


# Mac Desktop Selected -> Ask RAM
@router.callback_query(F.data.startswith("macdesk_mod:"))
async def cb_macdesk_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in MAC_DESKTOP_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "Mac mini"
    model_name = target["name"] if target else "Mac Desktop"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="mac_desktop"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"🧠 <b>RAM (Operativ xotira) hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_ram_keyboard("mac", back_cb="apple_type:mac_desktop"),
        parse_mode="HTML"
    )


# Apple Watch Selected -> Ask Battery
@router.callback_query(F.data.startswith("aw_mod:"))
async def cb_apple_watch_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in APPLE_WATCH_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "Apple Watch"
    model_name = target["name"] if target else "Apple Watch"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="apple_watch"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"🔋 <b>Batareya salomatligi (Yomkist) qanday bo'lsin?</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_battery_keyboard(back_cb="apple_type:apple_watch"),
        parse_mode="HTML"
    )


# AirPods Selected -> Execute Direct Search
@router.callback_query(F.data.startswith("airp_mod:"))
async def cb_airpods_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((m for m in AIRPODS_MODELS if m["id"] == mod_id), None)
    base_query = target["query"] if target else "AirPods"
    model_name = target["name"] if target else "AirPods"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        ram="",
        storage="",
        gpu="",
        battery_min=0,
        battery_label="Farqi yo'q"
    )
    await call.answer()
    await execute_and_display_search(call, state)


# ----------------- WINDOWS LAPTOPS FLOW -----------------

@router.callback_query(F.data.startswith("win_brand:"))
async def cb_win_brand_selected(call: CallbackQuery, state: FSMContext):
    brand_id = call.data.split(":")[1]
    await state.update_data(win_brand=brand_id, device_category="windows")
    await call.answer()

    target = next((b for b in WINDOWS_BRANDS if b["id"] == brand_id), None)
    brand_name = target["name"] if target else "Windows Noutbuklar"

    text = f"💻 <b>{brand_name}:</b>\nKerakli modelni tanlang:"
    await call.message.edit_text(
        text,
        reply_markup=get_windows_models_keyboard(brand_id),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("win_mod:"))
async def cb_win_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    data = await state.get_data()
    brand_id = data.get("win_brand", "all_win")
    models = WINDOWS_MODELS.get(brand_id, WINDOWS_MODELS["all_win"])
    target = next((m for m in models if m["id"] == mod_id), None)

    base_query = target["query"] if target else "Gaming noutbuk"
    model_name = target["name"] if target else "Windows Noutbuk"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="windows"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"🎮 <b>Video karta (GPU) turini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_gpu_keyboard(back_cb=f"win_brand:{brand_id}"),
        parse_mode="HTML"
    )


# GPU Selected -> Ask RAM
@router.callback_query(F.data.startswith("spec_gpu:"))
async def cb_gpu_selected(call: CallbackQuery, state: FSMContext):
    gpu_id = call.data.split(":")[1]
    target = next((g for g in GPU_OPTIONS_WIN if g["id"] == gpu_id), None)
    gpu_val = target["val"] if target else ""

    await state.update_data(gpu=gpu_val)
    await call.answer()

    data = await state.get_data()
    model_name = data.get("model_name", "Noutbuk")

    text = (
        f"Model: <b>{model_name}</b>\n"
        f"GPU: <b>{target['label'] if target else 'Barchasi'}</b>\n\n"
        f"🧠 <b>RAM (Operativ xotira) hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_ram_keyboard("win", back_cb="brand:windows"),
        parse_mode="HTML"
    )


# ----------------- SAMSUNG FLOW -----------------

@router.callback_query(F.data.startswith("sam_ser:"))
async def cb_samsung_series_selected(call: CallbackQuery, state: FSMContext):
    series_id = call.data.split(":")[1]
    await state.update_data(sam_series=series_id, device_category="samsung")
    await call.answer()

    text = "📱 <b>Samsung modelini tanlang:</b>"
    await call.message.edit_text(
        text,
        reply_markup=get_samsung_models_keyboard(series_id),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("sam_mod:"))
async def cb_samsung_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    data = await state.get_data()
    series_id = data.get("sam_series", "sam_s")
    models = SAMSUNG_MODELS.get(series_id, [])
    target = next((m for m in models if m["id"] == mod_id), None)

    base_query = target["query"] if target else "Samsung Galaxy"
    model_name = target["name"] if target else "Samsung Galaxy"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="samsung"
    )
    await call.answer()

    if series_id == "sam_watch":
        # Direct search for watches & buds
        await state.update_data(ram="", storage="", gpu="", battery_min=0)
        await execute_and_display_search(call, state)
    else:
        text = (
            f"Tanlandi: <b>{model_name}</b>\n\n"
            f"💾 <b>Xotira hajmini tanlang:</b>"
        )
        await call.message.edit_text(
            text,
            reply_markup=get_storage_keyboard(is_phone=True, back_cb=f"sam_ser:{series_id}"),
            parse_mode="HTML"
        )


# ----------------- XIAOMI FLOW -----------------

@router.callback_query(F.data.startswith("mi_ser:"))
async def cb_xiaomi_series_selected(call: CallbackQuery, state: FSMContext):
    series_id = call.data.split(":")[1]
    await state.update_data(mi_series=series_id, device_category="xiaomi")
    await call.answer()

    text = "⚡ <b>Modelni tanlang:</b>"
    await call.message.edit_text(
        text,
        reply_markup=get_xiaomi_models_keyboard(series_id),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("mi_mod:"))
async def cb_xiaomi_model_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    data = await state.get_data()
    series_id = data.get("mi_series", "mi_flagship")
    models = XIAOMI_MODELS.get(series_id, [])
    target = next((m for m in models if m["id"] == mod_id), None)

    base_query = target["query"] if target else "Xiaomi"
    model_name = target["name"] if target else "Xiaomi"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        device_category="xiaomi"
    )
    await call.answer()

    text = (
        f"Tanlandi: <b>{model_name}</b>\n\n"
        f"💾 <b>Xotira hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_storage_keyboard(is_phone=True, back_cb=f"mi_ser:{series_id}"),
        parse_mode="HTML"
    )


# ----------------- OTHER GADGETS FLOW -----------------

@router.callback_query(F.data.startswith("oth_mod:"))
async def cb_other_mod_selected(call: CallbackQuery, state: FSMContext):
    mod_id = call.data.split(":")[1]
    target = next((g for g in OTHER_GADGETS if g["id"] == mod_id), None)
    base_query = target["query"] if target else "Gadjet"
    model_name = target["name"] if target else "Gadjet"

    await state.update_data(
        model_name=model_name,
        base_query=base_query,
        ram="",
        storage="",
        gpu="",
        battery_min=0,
        battery_label="Farqi yo'q"
    )
    await call.answer()
    await execute_and_display_search(call, state)


# ----------------- SPECS SELECTION STEPS -----------------

# RAM Selected -> Ask Storage
@router.callback_query(F.data.startswith("spec_ram:"))
async def cb_ram_selected(call: CallbackQuery, state: FSMContext):
    ram_id = call.data.split(":")[1]
    data = await state.get_data()
    dev_cat = data.get("device_category", "mac")
    options = RAM_OPTIONS_MAC if dev_cat in ["macbook", "mac_desktop"] else RAM_OPTIONS_WIN

    target = next((r for r in options if r["id"] == ram_id), None)
    ram_val = target["val"] if target else ""
    ram_label = target["label"] if target else "Farqi yo'q"

    await state.update_data(ram=ram_val, ram_label=ram_label)
    await call.answer()

    model_name = data.get("model_name", "Qurilma")
    text = (
        f"Model: <b>{model_name}</b>\n"
        f"RAM: <b>{ram_label}</b>\n\n"
        f"💾 <b>SSD (Doimiy xotira) hajmini tanlang:</b>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_storage_keyboard(is_phone=False, back_cb="brand:apple" if "mac" in dev_cat else "brand:windows"),
        parse_mode="HTML"
    )


# Storage Selected -> Ask Battery
@router.callback_query(F.data.startswith("spec_ssd:"))
async def cb_storage_selected(call: CallbackQuery, state: FSMContext):
    ssd_id = call.data.split(":")[1]
    data = await state.get_data()
    is_phone = data.get("device_category") in ["iphone", "ipad", "samsung", "xiaomi"]
    options = STORAGE_OPTIONS_PHONE if is_phone else STORAGE_OPTIONS

    target = next((s for s in options if s["id"] == ssd_id), None)
    ssd_val = target["val"] if target else ""
    ssd_label = target["label"] if target else "Farqi yo'q"

    await state.update_data(storage=ssd_val, storage_label=ssd_label)
    await call.answer()

    model_name = data.get("model_name", "Qurilma")
    text = (
        f"Model: <b>{model_name}</b>\n"
        f"Xotira: <b>{ssd_label}</b>\n\n"
        f"🔋 <b>Batareya holati (Yomkist) qanday bo'lsin?</b>\n"
        f"<i>(O'zingizga mos talabni yoki 'Farqi yo'q' tugmasini tanlang)</i>"
    )
    await call.message.edit_text(
        text,
        reply_markup=get_battery_keyboard(back_cb="nav:main_menu"),
        parse_mode="HTML"
    )


# Battery Selected -> Execute Search!
@router.callback_query(F.data.startswith("spec_bat:"))
async def cb_battery_selected(call: CallbackQuery, state: FSMContext):
    bat_id = call.data.split(":")[1]
    target = next((b for b in BATTERY_HEALTH_OPTIONS if b["id"] == bat_id), None)
    bat_min = target["min"] if target else 0
    bat_label = target["label"] if target else "Farqi yo'q"

    await state.update_data(battery_min=bat_min, battery_label=bat_label)
    await call.answer()
    await execute_and_display_search(call, state)


# ----------------- EXECUTE SEARCH & RENDER CARD -----------------

async def execute_and_display_search(call: CallbackQuery, state: FSMContext):
    """Fetches offers from OLX and presents the first result card."""
    data = await state.get_data()
    base_model = data.get("base_query", "MacBook")
    ram = data.get("ram", "")
    storage = data.get("storage", "")
    gpu = data.get("gpu", "")
    battery_min = data.get("battery_min", 0)

    # Status message
    status_msg = await call.message.edit_text(
        f"⏳ <b>OLX.uz bo'yicha eng sara e'lonlar qidirilmoqda...</b>\n"
        f"🔍 <i>{html.escape(base_model)} {html.escape(ram)} {html.escape(storage)}</i>\n\n"
        f"Biroz kuting...",
        parse_mode="HTML"
    )

    device_category = data.get("device_category", "")

    results, is_relaxed, actual_query = await smart_search(
        base_model=base_model,
        ram=ram,
        storage=storage,
        gpu=gpu,
        battery_min=battery_min,
        device_category=device_category
    )

    if not results:
        empty_text = (
            f"😕 <b>Afsuski, hozirda OLX da ushbu parametrlar bo'yicha faol e'lon topilmadi:</b>\n"
            f"🔍 <i>{html.escape(actual_query)}</i>\n\n"
            f"💡 <b>Tavsiya:</b> Parametrlarni (RAM yoki SSD) kengroq qilib, 'Farqi yo'q' variantini tanlab ko'ring "
            f"yoki to'g'ridan-to'g'ri matn orqali erkin qidiruvdan foydalaning."
        )
        await status_msg.edit_text(empty_text, reply_markup=get_main_menu_keyboard(), parse_mode="HTML")
        return

    # Store search results in FSM context
    await state.update_data(
        results=results,
        current_index=0,
        is_relaxed=is_relaxed,
        actual_query=actual_query
    )

    # Render card
    await render_offer_card(call.message, state, index=0, is_new_message=True)


async def render_offer_card(message: Message, state: FSMContext, index: int, is_new_message: bool = False):
    """
    Renders single OLX offer card with photo (if available), formatted details and pagination.
    """
    data = await state.get_data()
    results: List[Dict[str, Any]] = data.get("results", [])
    if not results or index < 0 or index >= len(results):
        return

    offer = results[index]
    total = len(results)
    is_relaxed = data.get("is_relaxed", False)
    actual_query = data.get("actual_query", "")

    relaxed_banner = ""
    if is_relaxed:
        relaxed_banner = (
            "ℹ️ <i>Aniq kombinatsiya bo'yicha kam e'lon topilgani sababli, "
            "sizga eng yaqin mos keluvchi saralangan e'lonlar ko'rsatilmoqda.</i>\n\n"
        )

    title_safe = html.escape(offer.get("title", ""))
    price_safe = html.escape(offer.get("price", "Kelishilgan"))
    location_safe = html.escape(offer.get("location", "O'zbekiston"))
    state_safe = html.escape(offer.get("state", "Ko'rsatilmagan"))
    battery_safe = html.escape(offer.get("battery", {}).get("summary", "E'londa yozilmagan"))
    desc_safe = html.escape(offer.get("description", ""))
    url_safe = offer.get("url", "")

    card_text = (
        f"🔎 <b>OLX Qidiruvi:</b> <code>{html.escape(actual_query)}</code>\n"
        f"{relaxed_banner}"
        f"📦 <b>{title_safe}</b>\n\n"
        f"💰 <b>Narxi:</b> {price_safe}\n"
        f"📍 <b>Manzil:</b> {location_safe}\n"
        f"⚙️ <b>Holati:</b> {state_safe}\n"
        f"🔋 <b>Batareya / Yomkist:</b> {battery_safe}\n\n"
        f"📝 <b>Tavsif:</b>\n<i>{desc_safe}</i>\n\n"
        f"🔗 <a href='{url_safe}'>OLX da e'lonni to'liq ko'rish</a>"
    )

    kb = get_result_card_keyboard(
        current_index=index,
        total_count=total,
        offer_url=url_safe,
        back_cb="nav:main_menu"
    )

    photos = offer.get("photos", [])
    first_photo = photos[0] if photos else None

    # Handle media sending or editing
    if first_photo:
        try:
            # Attempt to download image directly into buffer for 100% bypass of Telegram CDN restrictions
            img_bytes = await download_image_bytes(first_photo)
            if img_bytes:
                photo_input = BufferedInputFile(img_bytes, filename=f"olx_{offer['id']}.jpg")
                if is_new_message:
                    await message.delete()
                    await message.answer_photo(
                        photo=photo_input,
                        caption=card_text,
                        reply_markup=kb,
                        parse_mode="HTML"
                    )
                else:
                    await message.edit_media(
                        media=InputMediaPhoto(media=photo_input, caption=card_text, parse_mode="HTML"),
                        reply_markup=kb
                    )
                return
        except Exception as e:
            logger.warning(f"Error rendering image card: {e}")

    # Fallback to text card if photo failed or does not exist
    try:
        if is_new_message:
            await message.delete()
            await message.answer(card_text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=False)
        else:
            if message.photo:
                await message.delete()
                await message.answer(card_text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=False)
            else:
                await message.edit_text(card_text, reply_markup=kb, parse_mode="HTML", disable_web_page_preview=False)
    except Exception as e:
        logger.error(f"Error rendering text card: {e}")
        await message.answer(card_text, reply_markup=kb, parse_mode="HTML")


# ----------------- PAGINATION & LIST VIEW -----------------

@router.callback_query(F.data.startswith("res_page:"))
async def cb_pagination(call: CallbackQuery, state: FSMContext):
    """Handle Prev / Next page clicks"""
    target_idx = int(call.data.split(":")[1])
    await state.update_data(current_index=target_idx)
    await call.answer()
    await render_offer_card(call.message, state, index=target_idx, is_new_message=False)


@router.callback_query(F.data == "noop")
async def cb_noop(call: CallbackQuery):
    await call.answer()


@router.callback_query(F.data == "action:list_view")
async def cb_list_view(call: CallbackQuery, state: FSMContext):
    """Shows compact scrollable list of all found offers with direct links"""
    data = await state.get_data()
    results: List[Dict[str, Any]] = data.get("results", [])
    if not results:
        await call.answer("E'lonlar topilmadi", show_alert=True)
        return

    actual_query = data.get("actual_query", "")
    lines = [
        f"📋 <b>Topilgan barcha e'lonlar ({len(results)} ta):</b>",
        f"🔍 <i>{html.escape(actual_query)}</i>\n"
    ]

    for i, it in enumerate(results[:15], 1):
        t = html.escape(it['title'][:55])
        p = html.escape(it['price'])
        loc = html.escape(it['location'].split(',')[0])
        u = it['url']
        lines.append(f"{i}. <a href='{u}'><b>{t}</b></a>\n   💰 {p} | 📍 {loc}")

    lines.append("\n👇 <i>Kartochkalar ko'rinishiga qaytish uchun 'Orqaga' tugmasini bosing:</i>")
    text = "\n".join(lines)

    from aiogram.utils.keyboard import InlineKeyboardBuilder
    b = InlineKeyboardBuilder()
    b.button(text="🔙 Kartochkaga qaytish", callback_data=f"res_page:{data.get('current_index', 0)}")
    b.button(text="🏠 Bosh menyu", callback_data="nav:main_menu")
    b.adjust(1, 1)

    try:
        if call.message.photo:
            await call.message.delete()
            await call.message.answer(text, reply_markup=b.as_markup(), parse_mode="HTML", disable_web_page_preview=True)
        else:
            await call.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="HTML", disable_web_page_preview=True)
    except Exception:
        await call.message.answer(text, reply_markup=b.as_markup(), parse_mode="HTML", disable_web_page_preview=True)
    await call.answer()


# ----------------- FREE-TEXT SEARCH HANDLER -----------------

@router.message(F.text)
async def handle_free_text_search(message: Message, state: FSMContext):
    """
    Handles any custom search text sent by user.
    Executes instant OLX search and displays interactive result cards.
    """
    query = message.text.strip()
    if not query:
        return

    status = await message.answer(
        f"🔍 <b>OLX.uz dan qidirilmoqda:</b> <code>{html.escape(query)}</code>\n"
        f"Biroz kuting...",
        parse_mode="HTML"
    )

    results, is_relaxed, actual_query = await smart_search(base_model="", free_query=query)

    if not results:
        await status.edit_text(
            f"😕 <b>'{html.escape(query)}' bo'yicha OLX da e'lon topilmadi.</b>\n\n"
            f"Qidiruv so'zini o'zgartirib ko'ring yoki bosh menyudan brend tanlang:",
            reply_markup=get_main_menu_keyboard(),
            parse_mode="HTML"
        )
        return

    await state.clear()
    await state.update_data(
        results=results,
        current_index=0,
        is_relaxed=is_relaxed,
        actual_query=actual_query
    )

    await render_offer_card(status, state, index=0, is_new_message=True)
