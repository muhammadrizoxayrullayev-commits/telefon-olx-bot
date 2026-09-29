"""
catalog.py - Gadgets and Electronics hierarchical structure
Contains brand, product line, model, specs (RAM, Storage, Battery/Yomkist, GPU) options.
"""

BRANDS = [
    {"id": "apple", "name": "🍏 Apple", "icon": "🍏"},
    {"id": "samsung", "name": "📱 Samsung", "icon": "📱"},
    {"id": "xiaomi", "name": "⚡ Xiaomi / Redmi / POCO", "icon": "⚡"},
    {"id": "windows", "name": "💻 Windows Noutbuklar", "icon": "💻"},
    {"id": "other", "name": "🎮 Boshqa Gadjetlar (PS5, Xbox, Dron)", "icon": "🎮"},
]

# ----------------- APPLE -----------------
APPLE_TYPES = [
    {"id": "macbook", "name": "💻 MacBook (Air / Pro)"},
    {"id": "iphone", "name": "📱 iPhone"},
    {"id": "ipad", "name": "📟 iPad"},
    {"id": "mac_desktop", "name": "🖥️ Mac mini / iMac / Studio"},
    {"id": "apple_watch", "name": "⌚ Apple Watch"},
    {"id": "airpods", "name": "🎧 AirPods"},
]

MACBOOK_MODELS = [
    {"id": "mac_m4_pro_max", "name": "⚡ MacBook Pro M4 / Pro / Max", "query": "MacBook Pro M4"},
    {"id": "mac_m3_pro_max", "name": "⚡ MacBook Pro M3 Pro / Max", "query": "MacBook Pro M3 Pro"},
    {"id": "mac_m3", "name": "⚡ MacBook Pro M3", "query": "MacBook Pro M3"},
    {"id": "mac_m2_pro_max", "name": "⚡ MacBook Pro M2 Pro / Max", "query": "MacBook Pro M2 Pro"},
    {"id": "mac_m2_pro", "name": "⚡ MacBook Pro M2", "query": "MacBook Pro M2"},
    {"id": "mac_m1_pro_max", "name": "⚡ MacBook Pro M1 Pro / Max", "query": "MacBook Pro M1 Pro"},
    {"id": "mac_m1_pro", "name": "⚡ MacBook Pro M1", "query": "MacBook Pro M1"},
    {"id": "mac_air_m3", "name": "🍃 MacBook Air M3", "query": "MacBook Air M3"},
    {"id": "mac_air_m2", "name": "🍃 MacBook Air M2", "query": "MacBook Air M2"},
    {"id": "mac_air_m1", "name": "🍃 MacBook Air M1", "query": "MacBook Air M1"},
    {"id": "mac_intel", "name": "💻 MacBook Pro / Air (Intel)", "query": "MacBook Intel"},
    {"id": "mac_all", "name": "🌟 Barcha MacBooklar", "query": "MacBook"},
]

IPHONE_MODELS = [
    {"id": "ip_16_pm", "name": "🌟 iPhone 16 Pro Max", "query": "iPhone 16 Pro Max"},
    {"id": "ip_16_pro", "name": "🌟 iPhone 16 Pro", "query": "iPhone 16 Pro"},
    {"id": "ip_16_plus", "name": "🌟 iPhone 16 Plus", "query": "iPhone 16 Plus"},
    {"id": "ip_16", "name": "🌟 iPhone 16", "query": "iPhone 16"},
    {"id": "ip_15_pm", "name": "💎 iPhone 15 Pro Max", "query": "iPhone 15 Pro Max"},
    {"id": "ip_15_pro", "name": "💎 iPhone 15 Pro", "query": "iPhone 15 Pro"},
    {"id": "ip_15_plus", "name": "💎 iPhone 15 Plus", "query": "iPhone 15 Plus"},
    {"id": "ip_15", "name": "💎 iPhone 15", "query": "iPhone 15"},
    {"id": "ip_14_pm", "name": "📱 iPhone 14 Pro Max", "query": "iPhone 14 Pro Max"},
    {"id": "ip_14_pro", "name": "📱 iPhone 14 Pro", "query": "iPhone 14 Pro"},
    {"id": "ip_14", "name": "📱 iPhone 14 / 14 Plus", "query": "iPhone 14"},
    {"id": "ip_13_pm", "name": "📱 iPhone 13 Pro Max", "query": "iPhone 13 Pro Max"},
    {"id": "ip_13_pro", "name": "📱 iPhone 13 Pro", "query": "iPhone 13 Pro"},
    {"id": "ip_13", "name": "📱 iPhone 13 / 13 Mini", "query": "iPhone 13"},
    {"id": "ip_12_pm", "name": "📱 iPhone 12 Pro Max", "query": "iPhone 12 Pro Max"},
    {"id": "ip_12_pro", "name": "📱 iPhone 12 Pro", "query": "iPhone 12 Pro"},
    {"id": "ip_12", "name": "📱 iPhone 12 / 12 Mini", "query": "iPhone 12"},
    {"id": "ip_11_pm", "name": "📱 iPhone 11 Pro Max", "query": "iPhone 11 Pro Max"},
    {"id": "ip_11_pro", "name": "📱 iPhone 11 Pro", "query": "iPhone 11 Pro"},
    {"id": "ip_11", "name": "📱 iPhone 11", "query": "iPhone 11"},
    {"id": "ip_older", "name": "📱 iPhone XS / XR / X / SE", "query": "iPhone XS"},
]

IPAD_MODELS = [
    {"id": "ipad_pro_m4", "name": "✨ iPad Pro M4", "query": "iPad Pro M4"},
    {"id": "ipad_pro_m2", "name": "✨ iPad Pro M2", "query": "iPad Pro M2"},
    {"id": "ipad_pro_m1", "name": "✨ iPad Pro M1", "query": "iPad Pro M1"},
    {"id": "ipad_air_m2", "name": "🍃 iPad Air M2", "query": "iPad Air M2"},
    {"id": "ipad_air_5", "name": "🍃 iPad Air 5 (M1)", "query": "iPad Air M1"},
    {"id": "ipad_mini_6_7", "name": "📟 iPad Mini 6 / Mini 7", "query": "iPad Mini"},
    {"id": "ipad_10_gen", "name": "📟 iPad 10-avlod", "query": "iPad 10"},
    {"id": "ipad_9_gen", "name": "📟 iPad 9-avlod", "query": "iPad 9"},
]

MAC_DESKTOP_MODELS = [
    {"id": "mac_mini_m4", "name": "🖥️ Mac mini M4 / M4 Pro", "query": "Mac mini M4"},
    {"id": "mac_mini_m2", "name": "🖥️ Mac mini M2 / M2 Pro", "query": "Mac mini M2"},
    {"id": "mac_mini_m1", "name": "🖥️ Mac mini M1", "query": "Mac mini M1"},
    {"id": "imac_m3", "name": "🖥️ iMac 24\" M3 / M1", "query": "iMac M3"},
    {"id": "mac_studio", "name": "🖥️ Mac Studio (M1/M2 Max/Ultra)", "query": "Mac Studio"},
]

APPLE_WATCH_MODELS = [
    {"id": "aw_ultra_2", "name": "⌚ Apple Watch Ultra 2", "query": "Apple Watch Ultra 2"},
    {"id": "aw_ultra", "name": "⌚ Apple Watch Ultra", "query": "Apple Watch Ultra"},
    {"id": "aw_s10", "name": "⌚ Apple Watch Series 10", "query": "Apple Watch Series 10"},
    {"id": "aw_s9", "name": "⌚ Apple Watch Series 9", "query": "Apple Watch Series 9"},
    {"id": "aw_s8_7", "name": "⌚ Apple Watch Series 8 / 7", "query": "Apple Watch Series 8"},
    {"id": "aw_se_2", "name": "⌚ Apple Watch SE 2", "query": "Apple Watch SE"},
]

AIRPODS_MODELS = [
    {"id": "airpods_max", "name": "🎧 AirPods Max", "query": "AirPods Max"},
    {"id": "airpods_pro_2", "name": "🎧 AirPods Pro 2 (Type-C / Lightning)", "query": "AirPods Pro 2"},
    {"id": "airpods_pro_1", "name": "🎧 AirPods Pro", "query": "AirPods Pro"},
    {"id": "airpods_4", "name": "🎧 AirPods 4 (ANC / Standard)", "query": "AirPods 4"},
    {"id": "airpods_3", "name": "🎧 AirPods 3", "query": "AirPods 3"},
    {"id": "airpods_2", "name": "🎧 AirPods 2", "query": "AirPods 2"},
]

# ----------------- WINDOWS LAPTOPS -----------------
WINDOWS_BRANDS = [
    {"id": "hp", "name": "💻 HP (Victus, Omen, Pavilion...)"},
    {"id": "lenovo", "name": "💻 Lenovo (Legion, LOQ, IdeaPad...)"},
    {"id": "asus", "name": "💻 ASUS (ROG, TUF, ZenBook...)"},
    {"id": "acer", "name": "💻 Acer (Nitro 5/16, Predator...)"},
    {"id": "dell", "name": "💻 Dell (Alienware, G15, XPS...)"},
    {"id": "msi", "name": "💻 MSI (Katana, Thin, Raider...)"},
    {"id": "all_win", "name": "🌟 Barcha Windows noutbuklar"},
]

WINDOWS_MODELS = {
    "hp": [
        {"id": "hp_victus_16", "name": "🔥 HP Victus 16", "query": "HP Victus 16"},
        {"id": "hp_victus_15", "name": "🔥 HP Victus 15", "query": "HP Victus 15"},
        {"id": "hp_omen", "name": "⚡ HP Omen 16 / 17", "query": "HP Omen"},
        {"id": "hp_pavilion", "name": "🎮 HP Pavilion Gaming", "query": "HP Pavilion Gaming"},
        {"id": "hp_envy_spectre", "name": "✨ HP Envy / Spectre / EliteBook", "query": "HP Envy"},
        {"id": "hp_all", "name": "🌟 Barcha HP noutbuklar", "query": "HP noutbuk"},
    ],
    "lenovo": [
        {"id": "lenovo_legion_5_pro", "name": "🔥 Lenovo Legion 5 / 5 Pro", "query": "Lenovo Legion 5"},
        {"id": "lenovo_legion_7", "name": "⚡ Lenovo Legion 7 / Slim", "query": "Lenovo Legion 7"},
        {"id": "lenovo_loq", "name": "🔥 Lenovo LOQ 15", "query": "Lenovo LOQ"},
        {"id": "lenovo_ideapad_gaming", "name": "🎮 Lenovo IdeaPad Gaming 3", "query": "IdeaPad Gaming"},
        {"id": "lenovo_thinkpad", "name": "💼 Lenovo ThinkPad", "query": "Lenovo ThinkPad"},
        {"id": "lenovo_all", "name": "🌟 Barcha Lenovo noutbuklar", "query": "Lenovo Legion"},
    ],
    "asus": [
        {"id": "asus_rog_strix", "name": "⚡ ASUS ROG Strix (G15/G16/G17)", "query": "ASUS ROG Strix"},
        {"id": "asus_rog_zephyrus", "name": "✨ ASUS ROG Zephyrus (G14/G16)", "query": "ASUS Zephyrus"},
        {"id": "asus_tuf", "name": "🔥 ASUS TUF Gaming (A15/F15/F16)", "query": "ASUS TUF Gaming"},
        {"id": "asus_zenbook", "name": "💎 ASUS ZenBook / VivoBook", "query": "ASUS ZenBook"},
        {"id": "asus_all", "name": "🌟 Barcha ASUS noutbuklar", "query": "ASUS noutbuk"},
    ],
    "acer": [
        {"id": "acer_nitro_16", "name": "🔥 Acer Nitro 16", "query": "Acer Nitro 16"},
        {"id": "acer_nitro_5", "name": "🔥 Acer Nitro 5", "query": "Acer Nitro 5"},
        {"id": "acer_predator", "name": "⚡ Acer Predator Helios", "query": "Acer Predator"},
        {"id": "acer_aspire", "name": "💼 Acer Aspire / Swift", "query": "Acer Aspire"},
        {"id": "acer_all", "name": "🌟 Barcha Acer noutbuklar", "query": "Acer Nitro"},
    ],
    "dell": [
        {"id": "dell_alienware", "name": "👽 Dell Alienware", "query": "Dell Alienware"},
        {"id": "dell_g15_g16", "name": "🔥 Dell G15 / G16 Gaming", "query": "Dell G15"},
        {"id": "dell_xps", "name": "💎 Dell XPS 13 / 15", "query": "Dell XPS"},
        {"id": "dell_latitude", "name": "💼 Dell Latitude / Inspiron", "query": "Dell noutbuk"},
        {"id": "dell_all", "name": "🌟 Barcha Dell noutbuklar", "query": "Dell noutbuk"},
    ],
    "msi": [
        {"id": "msi_katana", "name": "🗡️ MSI Katana 15 / 17", "query": "MSI Katana"},
        {"id": "msi_raider_stealth", "name": "⚡ MSI Raider / Stealth", "query": "MSI Raider"},
        {"id": "msi_thin", "name": "🔥 MSI Thin GF63 / Cyborg", "query": "MSI Thin GF63"},
        {"id": "msi_modern", "name": "💼 MSI Modern / Prestige", "query": "MSI Modern"},
        {"id": "msi_all", "name": "🌟 Barcha MSI noutbuklar", "query": "MSI noutbuk"},
    ],
    "all_win": [
        {"id": "win_all_gaming", "name": "🎮 Barcha Gaming noutbuklar", "query": "Gaming noutbuk"},
        {"id": "win_all_office", "name": "💼 Barcha Ofis/Ishchi noutbuklar", "query": "noutbuk"},
    ]
}

# ----------------- SAMSUNG -----------------
SAMSUNG_SERIES = [
    {"id": "sam_s", "name": "🌟 Galaxy S Seriya (S24, S23, S22...)"},
    {"id": "sam_z", "name": "📱 Galaxy Z Seriya (Z Fold, Z Flip)"},
    {"id": "sam_a", "name": "💎 Galaxy A Seriya (A55, A54, A35...)"},
    {"id": "sam_tab", "name": "📟 Galaxy Tab Planchetlar"},
    {"id": "sam_watch", "name": "⌚ Galaxy Watch & Buds"},
]

SAMSUNG_MODELS = {
    "sam_s": [
        {"id": "s24_ultra", "name": "👑 Galaxy S24 Ultra", "query": "Samsung S24 Ultra"},
        {"id": "s24_plus", "name": "🌟 Galaxy S24+", "query": "Samsung S24 Plus"},
        {"id": "s24", "name": "🌟 Galaxy S24", "query": "Samsung S24"},
        {"id": "s23_ultra", "name": "💎 Galaxy S23 Ultra", "query": "Samsung S23 Ultra"},
        {"id": "s23_plus_base", "name": "💎 Galaxy S23 / S23+", "query": "Samsung S23"},
        {"id": "s22_ultra", "name": "📱 Galaxy S22 Ultra", "query": "Samsung S22 Ultra"},
        {"id": "s22_base", "name": "📱 Galaxy S22 / S22+", "query": "Samsung S22"},
        {"id": "s21_series", "name": "📱 Galaxy S21 Ultra / FE", "query": "Samsung S21"},
    ],
    "sam_z": [
        {"id": "z_fold_6", "name": "📱 Galaxy Z Fold 6", "query": "Samsung Z Fold 6"},
        {"id": "z_flip_6", "name": "✨ Galaxy Z Flip 6", "query": "Samsung Z Flip 6"},
        {"id": "z_fold_5", "name": "📱 Galaxy Z Fold 5", "query": "Samsung Z Fold 5"},
        {"id": "z_flip_5", "name": "✨ Galaxy Z Flip 5", "query": "Samsung Z Flip 5"},
        {"id": "z_fold_4", "name": "📱 Galaxy Z Fold 4 / Flip 4", "query": "Samsung Z Fold 4"},
    ],
    "sam_a": [
        {"id": "a55_5g", "name": "💎 Galaxy A55 5G", "query": "Samsung A55"},
        {"id": "a54_5g", "name": "💎 Galaxy A54 5G", "query": "Samsung A54"},
        {"id": "a35_5g", "name": "📱 Galaxy A35 5G", "query": "Samsung A35"},
        {"id": "a34_5g", "name": "📱 Galaxy A34 5G", "query": "Samsung A34"},
        {"id": "a25_a15", "name": "📱 Galaxy A25 / A15", "query": "Samsung A15"},
    ],
    "sam_tab": [
        {"id": "tab_s9_ultra", "name": "✨ Galaxy Tab S9 Ultra / S9+", "query": "Samsung Tab S9"},
        {"id": "tab_s8", "name": "✨ Galaxy Tab S8 Ultra / S8", "query": "Samsung Tab S8"},
        {"id": "tab_a9", "name": "📟 Galaxy Tab A9 / A9+", "query": "Samsung Tab A9"},
    ],
    "sam_watch": [
        {"id": "watch_ultra", "name": "⌚ Galaxy Watch Ultra", "query": "Galaxy Watch Ultra"},
        {"id": "watch_7_6", "name": "⌚ Galaxy Watch 7 / 6 Classic", "query": "Galaxy Watch 6"},
        {"id": "buds_3_pro", "name": "🎧 Galaxy Buds 3 Pro / Buds 2 Pro", "query": "Galaxy Buds 3 Pro"},
    ]
}

# ----------------- XIAOMI / REDMI / POCO -----------------
XIAOMI_SERIES = [
    {"id": "mi_flagship", "name": "🌟 Xiaomi Flagship (14 Ultra, 14, 13T...)"},
    {"id": "redmi_note", "name": "⚡ Redmi Note Seriya (13 Pro+, 13, 12...)"},
    {"id": "poco_series", "name": "🚀 POCO Seriya (F6 Pro, X6 Pro...)"},
    {"id": "mi_pad", "name": "📟 Xiaomi Pad (Pad 6, 6S Pro...)"},
]

XIAOMI_MODELS = {
    "mi_flagship": [
        {"id": "mi_14_ultra", "name": "👑 Xiaomi 14 Ultra", "query": "Xiaomi 14 Ultra"},
        {"id": "mi_14_pro", "name": "🌟 Xiaomi 14 Pro / 14", "query": "Xiaomi 14"},
        {"id": "mi_13t_pro", "name": "⚡ Xiaomi 13T Pro / 13T", "query": "Xiaomi 13T Pro"},
        {"id": "mi_13_ultra", "name": "💎 Xiaomi 13 Ultra / 13 Pro", "query": "Xiaomi 13 Ultra"},
    ],
    "redmi_note": [
        {"id": "rn_13_pro_plus", "name": "⚡ Redmi Note 13 Pro+ 5G", "query": "Redmi Note 13 Pro+"},
        {"id": "rn_13_pro", "name": "📱 Redmi Note 13 Pro", "query": "Redmi Note 13 Pro"},
        {"id": "rn_13", "name": "📱 Redmi Note 13", "query": "Redmi Note 13"},
        {"id": "rn_12_pro", "name": "📱 Redmi Note 12 Pro+ / 12 Pro", "query": "Redmi Note 12 Pro"},
        {"id": "redmi_13_12", "name": "📱 Redmi 13 / 12 (Oddiy)", "query": "Redmi 13"},
    ],
    "poco_series": [
        {"id": "poco_f6_pro", "name": "🚀 POCO F6 Pro / F6", "query": "POCO F6"},
        {"id": "poco_x6_pro", "name": "⚡ POCO X6 Pro 5G", "query": "POCO X6 Pro"},
        {"id": "poco_x6", "name": "📱 POCO X6 / M6 Pro", "query": "POCO X6"},
        {"id": "poco_f5_pro", "name": "🚀 POCO F5 Pro / F5", "query": "POCO F5"},
    ],
    "mi_pad": [
        {"id": "pad_6s_pro", "name": "✨ Xiaomi Pad 6S Pro", "query": "Xiaomi Pad 6S Pro"},
        {"id": "pad_6", "name": "📟 Xiaomi Pad 6", "query": "Xiaomi Pad 6"},
        {"id": "redmi_pad_pro", "name": "📟 Redmi Pad Pro / SE", "query": "Redmi Pad"},
    ]
}

# ----------------- OTHER GADGETS -----------------
OTHER_GADGETS = [
    {"id": "ps5_disc_digital", "name": "🎮 Sony PlayStation 5 (Slim / Fat)", "query": "PlayStation 5"},
    {"id": "ps4_pro", "name": "🎮 Sony PlayStation 4 Pro / Slim", "query": "PlayStation 4 Pro"},
    {"id": "xbox_series_x", "name": "🎮 Xbox Series X / Series S", "query": "Xbox Series X"},
    {"id": "nintendo_switch", "name": "🕹️ Nintendo Switch (OLED / V2)", "query": "Nintendo Switch OLED"},
    {"id": "dji_drone", "name": "🛸 DJI Dronlar (Mini 4 Pro / Air 3)", "query": "DJI Mini"},
    {"id": "smart_tv", "name": "📺 Smart TV (Samsung / LG / Xiaomi)", "query": "Smart TV"},
]

# ----------------- SPECS DEFINITIONS -----------------

# RAM Options
RAM_OPTIONS_MAC = [
    {"id": "ram_8", "label": "8 GB", "val": "8gb"},
    {"id": "ram_16", "label": "16 GB", "val": "16gb"},
    {"id": "ram_18", "label": "18 GB", "val": "18gb"},
    {"id": "ram_24", "label": "24 GB", "val": "24gb"},
    {"id": "ram_32", "label": "32 GB", "val": "32gb"},
    {"id": "ram_36", "label": "36 GB", "val": "36gb"},
    {"id": "ram_48_64", "label": "48/64 GB", "val": "64gb"},
    {"id": "ram_any", "label": "🤷‍♂️ Farqi yo'q", "val": ""},
]

RAM_OPTIONS_WIN = [
    {"id": "ram_8", "label": "8 GB", "val": "8gb"},
    {"id": "ram_16", "label": "16 GB", "val": "16gb"},
    {"id": "ram_24", "label": "24 GB", "val": "24gb"},
    {"id": "ram_32", "label": "32 GB", "val": "32gb"},
    {"id": "ram_64", "label": "64 GB", "val": "64gb"},
    {"id": "ram_any", "label": "🤷‍♂️ Farqi yo'q", "val": ""},
]

# Storage (SSD / ROM) Options
STORAGE_OPTIONS = [
    {"id": "ssd_128", "label": "128 GB", "val": "128gb"},
    {"id": "ssd_256", "label": "256 GB", "val": "256gb"},
    {"id": "ssd_512", "label": "512 GB", "val": "512gb"},
    {"id": "ssd_1tb", "label": "1 TB", "val": "1tb"},
    {"id": "ssd_2tb", "label": "2 TB", "val": "2tb"},
    {"id": "ssd_any", "label": "🤷‍♂️ Farqi yo'q", "val": ""},
]

STORAGE_OPTIONS_PHONE = [
    {"id": "rom_64", "label": "64 GB", "val": "64gb"},
    {"id": "rom_128", "label": "128 GB", "val": "128gb"},
    {"id": "rom_256", "label": "256 GB", "val": "256gb"},
    {"id": "rom_512", "label": "512 GB", "val": "512gb"},
    {"id": "rom_1tb", "label": "1 TB", "val": "1tb"},
    {"id": "rom_any", "label": "🤷‍♂️ Farqi yo'q", "val": ""},
]

# GPU Options for Windows Laptops
GPU_OPTIONS_WIN = [
    {"id": "gpu_rtx_4080_4090", "label": "🚀 RTX 4080 / 4090", "val": "rtx 4080"},
    {"id": "gpu_rtx_4070", "label": "⚡ RTX 4070", "val": "rtx 4070"},
    {"id": "gpu_rtx_4060", "label": "🔥 RTX 4060", "val": "rtx 4060"},
    {"id": "gpu_rtx_4050", "label": "🎮 RTX 4050", "val": "rtx 4050"},
    {"id": "gpu_rtx_3060_3070", "label": "🎯 RTX 3060 / 3070", "val": "rtx 3060"},
    {"id": "gpu_rtx_3050_2050", "label": "🎮 RTX 3050 / 2050", "val": "rtx 3050"},
    {"id": "gpu_gtx_1650", "label": "🕹️ GTX 1650 / 1660", "val": "gtx 1650"},
    {"id": "gpu_any", "label": "🤷‍♂️ Farqi yo'q", "val": ""},
]

# Battery Health (Yomkist) Options
BATTERY_HEALTH_OPTIONS = [
    {"id": "bat_100", "label": "🔋 100% (Yangi / Ideal)", "val": "100%", "min": 100},
    {"id": "bat_90_99", "label": "🔋 90% - 99%", "val": "90%", "min": 90},
    {"id": "bat_85_89", "label": "🔋 85% - 89%", "val": "85%", "min": 85},
    {"id": "bat_80_84", "label": "🔋 80% - 84%", "val": "80%", "min": 80},
    {"id": "bat_any", "label": "🤷‍♂️ Farqi yo'q", "val": "", "min": 0},
]
