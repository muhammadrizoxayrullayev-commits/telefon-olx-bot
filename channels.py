"""
channels.py - Curated database of Uzbekistan's top gadget & electronics Telegram channels,
Malika/Abu Saxiy stores, pricelists, and marketplace communities.
"""

from typing import List, Dict, Any, Optional

CHANNELS_DATA = {
    "apple": [
        {
            "name": "🍏 MacBro — Rasmiy Apple Do'koni",
            "type": "Yirik tarmoq do'koni",
            "channel_username": "@macbro_uz",
            "channel_url": "https://t.me/macbro_uz",
            "location": "📍 Toshkent, Navoiy ko'chasi 33 / Malika A-blok",
            "specs": "MacBook, iPhone, iPad, Watch, AirPods. 1 yil rasmiy kafolat, Trade-in va muddatli to'lov bor.",
            "direct_contact": "@macbro_admin"
        },
        {
            "name": "💎 BroStore — Gadjetlar & Apple",
            "type": "Malika do'koni",
            "channel_username": "@brostore_uz",
            "channel_url": "https://t.me/brostore_uz",
            "location": "📍 Malika savdo markazi, B-blok 27-do'kon",
            "specs": "Eng so'nggi Apple mahsulotlari eng qulay ulgurji narxlarda, original va kafolatli.",
            "direct_contact": "@brostore_sales"
        },
        {
            "name": "✨ iSpace Uzbekistan — Apple Reseller",
            "type": "Rasmiy vakil",
            "channel_username": "@ispace_uzbekistan",
            "channel_url": "https://t.me/ispace_uzbekistan",
            "location": "📍 Toshkent, Amir Temur shox ko'chasi",
            "specs": "Rasmiy sertifikatlangan yangi Apple mahsulotlari.",
            "direct_contact": "@ispace_uz_bot"
        },
        {
            "name": "📲 Mobile Lux — Malika Apple & Gadgets",
            "type": "Malika savdo kanali",
            "channel_username": "@mobile_toshkent",
            "channel_url": "https://t.me/mobile_toshkent",
            "location": "📍 Malika bozori, C-blok",
            "specs": "Har kuni yangilanib turadigan iPhone va MacBook dollar/so'm narxlari (Pricelist).",
            "direct_contact": "@mobilelux_admin"
        },
        {
            "name": "🍎 Apple Bozor Uzbekistan",
            "type": "E'lonlar va savdo kanali",
            "channel_username": "@apple_uzbekistan_bozor",
            "channel_url": "https://t.me/apple_uzbekistan_bozor",
            "location": "📍 Butun O'zbekiston bo'ylab",
            "specs": "Xususiy shaxslar va do'konlarning arzon Apple e'lonlari.",
            "direct_contact": "@apple_bozor_admin"
        }
    ],

    "windows": [
        {
            "name": "💻 Nout.uz — Malika Noutbuklar Markazi",
            "type": "Noutbuklar yetakchi do'koni",
            "channel_username": "@noutuz",
            "channel_url": "https://t.me/noutuz",
            "location": "📍 Malika savdo markazi, A-blok 9-do'kon",
            "specs": "HP Victus 15/16, Lenovo Legion, LOQ, ASUS ROG/TUF, Acer Nitro eng arzon ulgurji narxlarda.",
            "direct_contact": "@nout_uz_menejer"
        },
        {
            "name": "🎮 CompStore.uz — Gaming Noutbuklar",
            "type": "Maxsus Gaming do'koni",
            "channel_username": "@compstore_uz",
            "channel_url": "https://t.me/compstore_uz",
            "location": "📍 Malika A-blok 34-do'kon",
            "specs": "Kuchli RTX 4060, 4070, 4080 noutbuklar va kompyuterlar, professional maslahat.",
            "direct_contact": "@compstore_admin"
        },
        {
            "name": "⚙️ PCMarket.uz — Kompyuter & Noutbuklar",
            "type": "Malika do'koni",
            "channel_username": "@pcmarketuz",
            "channel_url": "https://t.me/pcmarketuz",
            "location": "📍 Malika bozori, A-22 do'kon",
            "specs": "Lenovo, HP, Asus, Dell barcha rusumlari, rasmiy kafolat bilan.",
            "direct_contact": "@pcmarket_manager"
        },
        {
            "name": "📢 Noutbuklar Bozori Uzbekistan",
            "type": "Katta savdo kanali",
            "channel_username": "@noutbuklar_bozori_uz",
            "channel_url": "https://t.me/noutbuklar_bozori_uz",
            "location": "📍 Butun O'zbekiston",
            "specs": "Yangi va ishlatilgan yaxshi holatdagi noutbuklar e'lonlari.",
            "direct_contact": "@noutbuk_bozor_admin"
        }
    ],

    "android": [
        {
            "name": "⚡ Mi Store Uzbekistan",
            "type": "Xiaomi rasmiy kanali",
            "channel_username": "@mistore_uz",
            "channel_url": "https://t.me/mistore_uz",
            "location": "📍 Toshkent, Samarqand, Andijon, Farg'ona filiallari",
            "specs": "Xiaomi 14, Redmi Note 13, POCO F6 Pro, Pad 6 va barcha aqlli gadjetlar.",
            "direct_contact": "@mistore_call"
        },
        {
            "name": "📱 Samsung Malika & Abu Saxiy",
            "type": "Galaxy do'konlari",
            "channel_username": "@samsunguzbekistan",
            "channel_url": "https://t.me/samsunguzbekistan",
            "location": "📍 Abu Saxiy va Malika savdo markazlari",
            "specs": "Galaxy S24 Ultra, Z Fold/Flip 6, Galaxy A55/A35 barcha ranglari bilan.",
            "direct_contact": "@samsung_optom"
        },
        {
            "name": "📦 Abu Saxiy Gadgets & Optom",
            "type": "Ulgurji & Chakana savdo",
            "channel_username": "@abusaxiy_gadgets",
            "channel_url": "https://t.me/abusaxiy_gadgets",
            "location": "📍 Abu Saxiy savdo majmuasi",
            "specs": "Butun O'zbekiston viloyatlariga arzon narxlarda dostavka qilib beradigan yetkazuvchilar.",
            "direct_contact": "@abusaxiy_operator"
        },
        {
            "name": "💎 Radius Mobile",
            "type": "Tarmoq do'koni",
            "channel_username": "@radius_uz",
            "channel_url": "https://t.me/radius_uz",
            "location": "📍 O'zbekiston bo'ylab 15+ do'konlar",
            "specs": "Samsung, Xiaomi, Vivo, Honor telefonlari va aksessuarlari.",
            "direct_contact": "@radius_support"
        }
    ],

    "bazaars": [
        {
            "name": "🏛️ Malika Bozori — Rasmiy E'lonlar Kanali",
            "type": "Bozor kanali (100k+ a'zo)",
            "channel_username": "@malikabozori",
            "channel_url": "https://t.me/malikabozori",
            "location": "📍 Toshkent sh., Malika (Fleshka) bozori",
            "specs": "Malika bozoridagi barcha do'konlarning eng so'nggi e'lonlari va aksiyalari.",
            "direct_contact": "@malikabozor_admin"
        },
        {
            "name": "📱 O'zbekiston Telefonlar Bozori",
            "type": "Respublika savdo kanali",
            "channel_username": "@telefonlar_bozori_uz",
            "channel_url": "https://t.me/telefonlar_bozori_uz",
            "location": "📍 Toshkent va barcha viloyatlar",
            "specs": "Har qanday telefon va smartfonlar oldi-sotdisi.",
            "direct_contact": "@telefonbozor_bot"
        },
        {
            "name": "🎮 Gadgetlar & PlayStation Bozori",
            "type": "O'yin konsollari va aksessuarlar",
            "channel_username": "@gadgets_uz_bozor",
            "channel_url": "https://t.me/gadgets_uz_bozor",
            "location": "📍 Toshkent, Malika",
            "specs": "PS5, PS4 Pro, Xbox Series X, Nintendo Switch va DJI dronlar savdosi.",
            "direct_contact": "@gadget_admin"
        },
        {
            "name": "🛍️ Texnomart & Asaxiy Kanallari",
            "type": "Kafolatlangan yirik marketlar",
            "channel_username": "@asaxiyuz",
            "channel_url": "https://t.me/asaxiyuz",
            "location": "📍 Butun O'zbekiston bo'ylab filiallar",
            "specs": "Rasmiy 1-2 yil kafolat, O'zbekiston bo'yicha bepul yetkazib berish.",
            "direct_contact": "@asaxiybot"
        }
    ]
}


def get_channels_by_category(category: str) -> List[Dict[str, Any]]:
    """Return relevant channels based on gadget category"""
    cat = category.lower()
    if any(k in cat for k in ["macbook", "iphone", "ipad", "apple", "airpods"]):
        return CHANNELS_DATA["apple"]
    elif any(k in cat for k in ["windows", "noutbuk", "laptop", "victus", "legion", "asus", "hp", "acer", "dell", "msi"]):
        return CHANNELS_DATA["windows"]
    elif any(k in cat for k in ["samsung", "xiaomi", "redmi", "poco", "android"]):
        return CHANNELS_DATA["android"]
    return CHANNELS_DATA["bazaars"]


def format_channels_message(channels: List[Dict[str, Any]], category_title: str) -> str:
    """Formats channels and stores into a rich Telegram message"""
    lines = [
        f"🏬 <b>O'zbekistondagi Eng Yirik Do'konlar & Telegram Kanallari:</b>",
        f"🎯 <i>Kategoriya: {category_title}</i>\n",
        "Bu yerda siz Malika, Abu Saxiy va O'zbekiston bo'ylab ishonchli do'konlar narxlarini solishtirishingiz va sotuvchilar bilan to'g'ridan-to'g'ri bog'lanishingiz mumkin:\n"
    ]

    for i, ch in enumerate(channels, 1):
        lines.append(
            f"<b>{i}. {ch['name']}</b> ({ch['type']})\n"
            f"   {ch['location']}\n"
            f"   ℹ️ <i>{ch['specs']}</i>\n"
            f"   📢 Kanal: <a href='{ch['channel_url']}'>{ch['channel_username']}</a>\n"
            f"   👤 Aloqa: {ch['direct_contact']}\n"
        )

    lines.append(
        "💡 <i>Kanal havolasini bosib, to'g'ridan-to'g'ri ularning so'nggi narxnomalarini (Pricelist) ko'rishingiz mumkin!</i>"
    )
    return "\n".join(lines)
