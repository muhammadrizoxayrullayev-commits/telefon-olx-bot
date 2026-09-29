"""
olx_service.py - Resilient & Highly Accurate OLX.uz search and extraction engine
Uses curl_cffi with Chrome 120 browser impersonation to bypass CloudFront WAF.
Includes strict model/chip validation and scoring so incorrect models (e.g. M2 when M3 is selected) are NEVER shown.
"""

import re
import time
import urllib.parse
import logging
from typing import List, Dict, Any, Optional, Set
from curl_cffi.requests import AsyncSession
from config import OLX_API_URL, OLX_REQUEST_TIMEOUT, CHROME_IMPERSONATE

logger = logging.getLogger(__name__)

# In-memory query cache: {cache_key: (timestamp, results)}
_CACHE: Dict[str, tuple[float, List[Dict[str, Any]]]] = {}
CACHE_TTL = 300  # 5 minutes


def extract_battery_info(title: str, description: str) -> Dict[str, Any]:
    """
    Extract battery capacity (yomkist) and cycle count from listing title and description.
    """
    combined = f"{title}\n{description}"
    clean = re.sub(r'<[^>]+>', ' ', combined)
    
    yomkist_val: Optional[int] = None
    cycles_val: Optional[int] = None
    tags: List[str] = []
    
    # 1. Yomkist / Battery percentage search
    p1 = re.findall(r'(?:yomk[io]st|batareya|akkumulyator|battery|ёмкость|емкость)\s*[:=-]?\s*(\d{2,3})\s*%?', clean, re.I)
    if p1:
        try:
            val = int(p1[0])
            if 50 <= val <= 100:
                yomkist_val = val
                tags.append(f"🔋 Yomkist: {val}%")
        except ValueError:
            pass

    # 2. Cycles search: e.g. "26 sikl", "sikl 30", "45 cycles"
    p2 = re.findall(r'(?:sikl|tsikl|cycle|цикл)\s*[:=-]?\s*(\d+)|(\d+)\s*(?:sikl|tsikl|cycle|цикл)', clean, re.I)
    for a, b in p2:
        c = a or b
        try:
            cycles_val = int(c)
            tags.append(f"🔄 {cycles_val} tsikl")
            break
        except ValueError:
            pass

    # 3. Standalone percentage (e.g. "100%", "92%") if not found yet
    if yomkist_val is None:
        p3 = re.findall(r'\b([89]\d|100)%\b', clean)
        if p3:
            try:
                yomkist_val = int(p3[0])
                tags.append(f"🔋 Yomkist: {yomkist_val}%")
            except ValueError:
                pass

    summary = " | ".join(dict.fromkeys(tags)) if tags else "E'londa yozilmagan"
    return {
        "percentage": yomkist_val,
        "cycles": cycles_val,
        "summary": summary
    }


def parse_offer(item: Dict[str, Any]) -> Dict[str, Any]:
    """Parse single OLX offer JSON to clean structured dictionary."""
    offer_id = str(item.get("id", ""))
    title = item.get("title", "Nomlanmagan e'lon").strip()
    url = item.get("url", "")
    description = item.get("description", "")
    
    # Clean HTML tags from description snippet
    clean_desc = re.sub(r'<[^>]+>', ' ', description).strip()
    clean_desc = re.sub(r'\s+', ' ', clean_desc)
    snippet = clean_desc[:240] + "..." if len(clean_desc) > 240 else clean_desc

    # Price & State parameters
    price_label = "Kelishilgan narxda"
    state_label = "Ko'rsatilmagan"
    for param in item.get("params", []):
        if param.get("key") == "price":
            val = param.get("value", {})
            price_label = val.get("label") or f"{val.get('value', '')} {val.get('currency', '')}".strip()
        elif param.get("key") == "state":
            state_label = param.get("value", {}).get("label", state_label)

    # Photos
    photos = []
    for ph in item.get("photos", []):
        link = ph.get("link", "")
        if link:
            formatted_link = link.replace("{width}x{height}", "800x600")
            photos.append(formatted_link)

    # Location
    loc = item.get("location", {})
    city_name = loc.get("city", {}).get("name", "")
    district_name = loc.get("district", {}).get("name", "")
    region_name = loc.get("region", {}).get("name", "")
    
    loc_parts = [p for p in [city_name, district_name] if p]
    if not loc_parts and region_name:
        loc_parts = [region_name]
    location_str = ", ".join(loc_parts) if loc_parts else "O'zbekiston"

    battery_info = extract_battery_info(title, description)

    return {
        "id": offer_id,
        "title": title,
        "url": url,
        "price": price_label,
        "state": state_label,
        "location": location_str,
        "description": snippet,
        "photos": photos,
        "battery": battery_info,
        "created_time": item.get("created_time", "")
    }


async def fetch_olx_offers(query: str, limit: int = 30) -> List[Dict[str, Any]]:
    """
    Fetch offers from OLX.uz API with impersonation and caching.
    """
    cache_key = f"{query.lower().strip()}_{limit}"
    now = time.time()
    if cache_key in _CACHE:
        timestamp, cached_data = _CACHE[cache_key]
        if now - timestamp < CACHE_TTL:
            return cached_data

    encoded_query = urllib.parse.quote_plus(query.strip())
    url = f"{OLX_API_URL}?query={encoded_query}&limit={limit}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "uz-UZ,uz;q=0.9,ru;q=0.8,en;q=0.7",
        "Referer": "https://www.olx.uz/",
    }

    try:
        async with AsyncSession(impersonate=CHROME_IMPERSONATE, timeout=OLX_REQUEST_TIMEOUT) as session:
            response = await session.get(url, headers=headers)
            if response.status_code != 200:
                logger.error(f"OLX API returned HTTP {response.status_code}: {response.text[:200]}")
                return []
            
            data = response.json()
            raw_items = data.get("data", [])
            parsed_items = [parse_offer(item) for item in raw_items]
            
            _CACHE[cache_key] = (now, parsed_items)
            return parsed_items

    except Exception as e:
        logger.exception(f"Error fetching OLX data for query '{query}': {e}")
        return []


async def download_image_bytes(image_url: str) -> Optional[bytes]:
    """Download image binary content with browser headers to avoid CDN blocks."""
    if not image_url:
        return None
    try:
        async with AsyncSession(impersonate=CHROME_IMPERSONATE, timeout=10) as session:
            res = await session.get(image_url)
            if res.status_code == 200 and len(res.content) > 100:
                return res.content
    except Exception as e:
        logger.warning(f"Failed to download image {image_url}: {e}")
    return None


def normalize_text(text: str) -> str:
    """Normalize text for consistent chip and model extraction"""
    t = text.lower()
    # Separate joined chip words like m3pro -> m3 pro, m2max -> m2 max
    t = re.sub(r'(\bm[1-5])(pro|max)', r'\1 \2', t)
    # Normalize Cyrillic lookalikes
    t = t.replace('м1', 'm1').replace('м2', 'm2').replace('м3', 'm3').replace('м4', 'm4').replace('м5', 'm5')
    return t


def is_strict_match(title: str, base_model: str, device_category: str = "") -> bool:
    """
    STRICT FILTER: Rejects listings where the seller spammed other models in description.
    Checks the TITLE to verify that the item is indeed the requested model/chip.
    """
    t = normalize_text(title)
    bm = normalize_text(base_model)

    # 1. APPLE MACBOOK
    if "macbook" in bm or device_category in ["macbook", "mac_desktop"]:
        # Check chip (m1, m2, m3, m4, m5, intel)
        chip_match = re.search(r'\b(m[1-5]|intel)\b', bm)
        if chip_match:
            req_chip = chip_match.group(1)
            other_chips = {"m1", "m2", "m3", "m4", "m5", "intel"} - {req_chip}
            has_req_chip = bool(re.search(rf'\b{req_chip}\b', t))
            has_other_chip = any(re.search(rf'\b{c}\b', t) for c in other_chips)
            
            # If title clearly states another chip and NOT the required chip -> REJECT
            if has_other_chip and not has_req_chip:
                return False
            # If title has neither, but requested a specific chip -> REJECT
            if not has_req_chip:
                return False

        # Pro vs Air distinction
        if "pro" in bm and not "air" in bm:
            if re.search(r'\bair\b', t):
                return False
        elif "air" in bm and not "pro" in bm:
            if re.search(r'\bpro\b', t) and not re.search(r'\bair\b', t):
                return False

        return True

    # 2. APPLE IPHONE
    if "iphone" in bm or device_category == "iphone":
        # Extract generation e.g. 16, 15, 14, 13, 12, 11, xs, xr, x, se
        gen_match = re.search(r'\biphone\s*(\d{1,2}|xs|xr|x|se)\b', bm)
        if gen_match:
            req_gen = gen_match.group(1)
            all_gens = {"16", "15", "14", "13", "12", "11", "xs", "xr", "x", "se"}
            other_gens = all_gens - {req_gen}
            
            # Check what generation is in title
            has_req = bool(re.search(rf'\b(?:iphone|айфон)?\s*{req_gen}\b', t))
            has_other = any(re.search(rf'\b(?:iphone|айфон)\s*{g}\b', t) for g in other_gens)
            
            if has_other and not has_req:
                return False
            if not has_req:
                return False

            # Pro Max check
            if "pro max" in bm:
                if not re.search(r'\b(?:pro\s*max|promax|max)\b', t):
                    return False
            elif "pro" in bm and "max" not in bm:
                if re.search(r'\b(?:pro\s*max|promax|max)\b', t):
                    # Pro Max is acceptable if Pro was asked, but keep in mind
                    pass
        return True

    # 3. WINDOWS LAPTOPS
    laptop_keywords = [
        ("victus", ["pavilion", "omen", "legion", "loq", "tuf", "nitro"]),
        ("omen", ["victus", "pavilion", "legion", "nitro"]),
        ("legion", ["ideapad", "thinkpad", "loq", "victus", "nitro"]),
        ("loq", ["legion", "ideapad", "victus", "nitro"]),
        ("tuf", ["rog", "strix", "zephyrus", "victus", "nitro"]),
        ("strix", ["tuf", "zephyrus", "victus"]),
        ("zephyrus", ["tuf", "strix", "victus"]),
        ("nitro", ["predator", "aspire", "victus", "legion"]),
        ("predator", ["nitro", "aspire", "victus"]),
        ("alienware", ["g15", "g16", "latitude", "xps"]),
        ("katana", ["thin", "gf63", "raider", "cyborg"])
    ]
    for target_kw, conflicts in laptop_keywords:
        if target_kw in bm:
            if target_kw not in t:
                return False
            # Check conflict
            if any(c in t for c in conflicts if c not in bm):
                return False
            return True

    # 4. SAMSUNG
    if "samsung" in bm or device_category == "samsung":
        for mod in ["s24", "s23", "s22", "s21", "z fold 6", "z fold 5", "z flip 6", "z flip 5", "a55", "a54", "a35"]:
            if mod in bm:
                other_mods = [m for m in ["s24", "s23", "s22", "s21", "fold 6", "fold 5", "flip 6", "flip 5", "a55", "a54"] if m != mod]
                has_other = any(re.search(rf'\b{m}\b', t) for m in other_mods)
                has_req = bool(re.search(rf'\b{mod}\b', t))
                if has_other and not has_req:
                    return False
                if not has_req:
                    return False
                if "ultra" in bm and not re.search(r'\bultra\b', t):
                    return False

    return True


def calculate_offer_score(
    offer: Dict[str, Any],
    base_model: str,
    ram: str,
    storage: str,
    gpu: str,
    battery_min: int
) -> int:
    """
    Ranks offers so that listings with exact RAM, Storage, and Battery appear FIRST.
    """
    score = 100
    t = normalize_text(offer.get("title", ""))
    d = normalize_text(offer.get("description", ""))
    
    # 1. Base model matches in title
    bm = normalize_text(base_model)
    for word in bm.split():
        if word in t:
            score += 40

    # 2. Exact RAM match
    if ram:
        ram_num = re.sub(r'[^0-9]', '', ram)
        if ram_num:
            # e.g. "18gb", "18 gb", "18/1tb", "18 гб"
            ram_pattern = rf'\b{ram_num}\s*(?:gb|гб|g)?\b|/{ram_num}\b|\b{ram_num}/'
            if re.search(ram_pattern, t):
                score += 250  # Huge boost if exact RAM is in title!
            elif re.search(ram_pattern, d):
                score += 80   # Boost if in description

    # 3. Exact Storage match
    if storage:
        st = storage.lower()
        if "1tb" in st or "1 tb" in st:
            st_pattern = r'\b(?:1tb|1\s*tb|1024|1\s*terabayt|1\s*тб)\b|/1tb\b|\b1tb/'
            if re.search(st_pattern, t):
                score += 250  # Huge boost for exact 1TB!
            elif re.search(st_pattern, d):
                score += 80
        elif "512" in st:
            st_pattern = r'\b512\s*(?:gb|гб|ssd)?\b|/512\b|\b512/'
            if re.search(st_pattern, t):
                score += 250
            elif re.search(st_pattern, d):
                score += 80
        elif "256" in st:
            st_pattern = r'\b256\s*(?:gb|гб|ssd)?\b|/256\b|\b256/'
            if re.search(st_pattern, t):
                score += 250
            elif re.search(st_pattern, d):
                score += 80

    # 4. GPU match
    if gpu:
        gpu_clean = gpu.lower().replace("rtx", "").strip()
        if gpu_clean:
            if re.search(rf'\b(?:rtx\s*)?{gpu_clean}\b', t):
                score += 200
            elif re.search(rf'\b(?:rtx\s*)?{gpu_clean}\b', d):
                score += 80

    # 5. Battery match
    perc = offer.get("battery", {}).get("percentage")
    if battery_min > 0:
        if perc and perc >= battery_min:
            score += 150
        elif perc and perc < battery_min:
            score -= 50

    return score


async def smart_search(
    base_model: str,
    ram: str = "",
    storage: str = "",
    gpu: str = "",
    battery_min: int = 0,
    free_query: str = "",
    device_category: str = ""
) -> tuple[List[Dict[str, Any]], bool, str]:
    """
    Executes smart multi-query search with STRICT post-filtering and scoring:
    1. Gathers candidate queries
    2. Fetches offers in parallel
    3. Strictly filters out false matches (wrong chips/models spamming descriptions)
    4. Ranks listings with exact specs at the top
    """
    if free_query:
        query = free_query.strip()
        items = await fetch_olx_offers(query, limit=30)
        return items, False, query

    # Build primary query and candidate queries
    parts = [base_model]
    if gpu:
        parts.append(gpu)
    if ram:
        parts.append(ram)
    if storage:
        parts.append(storage)

    primary_query = " ".join([p for p in parts if p]).strip()
    
    # Generate candidate variations for broader recall before strict filtering
    candidate_queries = [primary_query]
    
    # Variant with just model + RAM (if storage was specified)
    if ram and storage:
        candidate_queries.append(f"{base_model} {ram}")
    
    # Variant with base model (e.g. "MacBook Pro M3 Pro")
    candidate_queries.append(base_model)
    
    # If base model has "Pro" or "Air", also search shorthand e.g. "MacBook Pro M3"
    if "m3 pro" in base_model.lower():
        candidate_queries.append("MacBook Pro M3 Pro")
        candidate_queries.append("MacBook Pro M3")

    logger.info(f"Smart search executing candidates: {candidate_queries}")
    
    all_offers_map: Dict[str, Dict[str, Any]] = {}
    for q in candidate_queries:
        fetched = await fetch_olx_offers(q, limit=25)
        for item in fetched:
            if item["id"] not in all_offers_map:
                all_offers_map[item["id"]] = item
        # If we already have 20+ candidates, stop query loop
        if len(all_offers_map) >= 40:
            break

    logger.info(f"Total raw offers retrieved from OLX: {len(all_offers_map)}")

    # Apply STRICT validation: Eliminate any listing with the wrong chip or model in title!
    strictly_valid_offers: List[tuple[int, Dict[str, Any]]] = []
    for item in all_offers_map.values():
        title = item.get("title", "")
        if is_strict_match(title, base_model=base_model, device_category=device_category):
            score = calculate_offer_score(
                offer=item,
                base_model=base_model,
                ram=ram,
                storage=storage,
                gpu=gpu,
                battery_min=battery_min
            )
            strictly_valid_offers.append((score, item))
        else:
            logger.debug(f"Filtered out mismatch: '{title}' for request '{base_model}'")

    logger.info(f"Offers passing strict filter: {len(strictly_valid_offers)}")

    # Sort descending by score
    strictly_valid_offers.sort(key=lambda x: x[0], reverse=True)
    results = [item for _, item in strictly_valid_offers]

    if results:
        # Check if the top result matched all exact specs
        is_relaxed = False
        top_score = strictly_valid_offers[0][0]
        # If score is lower, it means exact RAM/storage wasn't found in top results, but chip is 100% correct
        if (ram or storage) and top_score < 300:
            is_relaxed = True
        return results, is_relaxed, primary_query

    # Fallback: if strict filter produced 0 items, search base_model directly
    base_raw = await fetch_olx_offers(base_model, limit=30)
    fallback_strictly_valid = []
    for item in base_raw:
        if is_strict_match(item.get("title", ""), base_model=base_model, device_category=device_category):
            fallback_strictly_valid.append(item)

    if fallback_strictly_valid:
        return fallback_strictly_valid, True, base_model

    return [], False, primary_query
