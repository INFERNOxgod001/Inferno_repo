from config import OWNER_NAME, OWNER_USERNAME
from emojis import SEP, pe


def _result_header(status: str) -> tuple[str, str]:
    if status == 'Charged':  return ("⚡  CHARGED  —  Hit Confirmed",  "Charged 💎")
    if status == 'Approved': return ("✅  APPROVED  —  Auth Detected",  "Approved ✅")
    if status == 'OTP':      return ("🔔  OTP REQUIRED",                "OTP 🔔")
    return ("❌  DECLINED", "Declined ❌")


def _clean_response(msg: str) -> str:
    m = msg.lower()
    if 'payment captured' in m or 'payment was successful' in m or 'captured successfully' in m:
        return 'Payment captured ✅'
    if 'auth' in m and ('approved' in m or 'success' in m):
        return 'Auth approved ✅'
    if 'approved' in m and '3ds not required' in m:
        return 'Approved — no 3DS ✅'
    if 'approved' in m and '3ds' not in m:
        return 'Card approved ✅'
    if 'insufficient funds' in m:
        return 'Insufficient funds 💸'
    if 'do not honor' in m or 'do not honour' in m:
        return 'Do not honor ❌'
    if 'card was declined' in m or 'card has been declined' in m or 'transaction declined' in m:
        return 'Card declined ❌'
    if 'declined' in m:
        return 'Declined ❌'
    if '3d secure' in m or '3ds' in m or 'authentication required' in m:
        return '3DS required ⚠️'
    if 'invalid card' in m or 'invalid number' in m:
        return 'Invalid card ❌'
    if 'expired' in m:
        return 'Card expired ❌'
    if 'incorrect cvc' in m or 'invalid cvc' in m or 'security code' in m:
        return 'Invalid CVV ❌'
    if 'lost' in m:
        return 'Card reported lost ❌'
    if 'stolen' in m:
        return 'Card reported stolen ❌'
    if 'pickup' in m:
        return 'Card pickup required ❌'
    if 'limit' in m or 'exceeded' in m:
        return 'Limit exceeded ❌'
    return msg[:60] if len(msg) > 60 else msg


def checker_line(uid: int, display_name: str) -> str:
    return f'👤 <b>By</b>  »  <a href="tg://user?id={uid}">{display_name}</a>'


def build_result_card(result: dict, bin_info: tuple, uid: int, cname: str) -> str:
    brand, btype, level, bank, country, flag = bin_info
    header, status_label = _result_header(result['status'])
    gate        = result.get('gateway', 'Shopify Payments')
    price       = result.get('price', '-')
    receipt_url = result.get('receipt_url', '') or ''
    _p          = str(price).replace('$', '').strip()
    price_str   = f'${_p} USD' if _p not in ('-', '', 'None', '0', '0.00', '0.0') else '—'
    t           = result.get('time')
    time_str    = f'{t}s' if t is not None else '—'
    dev_link    = f'<a href="https://t.me/Inferno_XR">𝙄𝙉𝙁𝙀𝙍𝙉𝙊_𝙓𝙍</a>'

    receipt_line = (
        f"🔗 <b>Receipt</b>    »  <a href=\"{receipt_url}\">View Receipt</a>\n"
        if result['status'] == 'Charged' and receipt_url else ""
    )

    bin_parts = " · ".join(p for p in [brand, btype, level] if p and p != '-')

    return pe(
        f"<b>{header}</b>\n"
        f"<b>{SEP}</b>\n"
        f"🃏 <b>Card</b>       »  <tg-spoiler>{result['card']}</tg-spoiler>\n"
        f"✨ <b>Status</b>     »  {status_label}\n"
        f"🖥 <b>Response</b>   »  {_clean_response(result['message'])}\n"
        f"🌐 <b>Gateway</b>    »  {gate}\n"
        f"⏱️ <b>Time</b>      »  {time_str}\n"
        + receipt_line
        + f"<b>{SEP}</b>\n"
        f"<blockquote>"
        f"💳 {bin_parts}\n"
        f"🏦 <b>Bank</b>       »  {bank}\n"
        f"🌍 <b>Country</b>    »  {country} {flag}\n"
        f"💵 <b>Amount</b>     »  {price_str}"
        f"</blockquote>\n"
        f"<b>{SEP}</b>\n"
        f"{checker_line(uid, cname)}\n"
        f"💻 <b>Dev</b>  »  {dev_link}"
    )
