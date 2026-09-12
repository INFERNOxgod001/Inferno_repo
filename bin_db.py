"""
Local BIN database — zero HTTP lookups.
Loads data/bins.json.gz once at import; all lookups are instant dict access.
"""
import gzip, json, os, aiohttp

_DB: dict = {}
_DB_PATH = os.path.join(os.path.dirname(__file__), "data", "bins.json.gz")
_HTTP_CACHE: dict = {}

def load_bins() -> int:
    global _DB
    if not os.path.exists(_DB_PATH):
        return 0
    with gzip.open(_DB_PATH, "rt", encoding="utf-8") as f:
        _DB = json.load(f)
    return len(_DB)

def _lookup(bin6: str):
    """Return (brand, type, level, bank, country, flag) or None if not found."""
    entry = _DB.get(bin6) or _DB.get(bin6[:6])
    if entry and isinstance(entry, list) and len(entry) == 6:
        return tuple(entry)
    return None

async def get_bin_info(card_number: str):
    """
    Instant local lookup first; HTTP fallback only for unknown BINs.
    Returns (brand, type, level, bank, country_name, country_flag).
    """
    bin6 = card_number[:6]

    hit = _lookup(bin6)
    if hit:
        return hit

    if bin6 in _HTTP_CACHE:
        return _HTTP_CACHE[bin6]

    try:
        timeout = aiohttp.ClientTimeout(total=6)
        async with aiohttp.ClientSession(timeout=timeout) as s:
            async with s.get(f"https://bins.antipublic.cc/bins/{bin6}") as r:
                if r.status == 200:
                    d = json.loads(await r.text())
                    result = (
                        d.get("brand",        "-") or "-",
                        d.get("type",         "-") or "-",
                        d.get("level",        "-") or "-",
                        d.get("bank",         "-") or "-",
                        d.get("country_name", "-") or "-",
                        d.get("country_flag", "")  or "",
                    )
                    _HTTP_CACHE[bin6] = result
                    if len(_HTTP_CACHE) > 2000:
                        for k in list(_HTTP_CACHE)[:500]:
                            _HTTP_CACHE.pop(k, None)
                    return result
    except Exception:
        pass

    return ("-", "-", "-", "-", "-", "")
