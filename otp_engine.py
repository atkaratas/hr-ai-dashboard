import random
import time
import json
import os

# OTP kodlarını geçici olarak tutacak dosya (statik site ile bot arasındaki köprü)
OTP_FILE = 'projects/hr_ai_system/data/active_otps.json'

def generate_otp(telegram_id):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + 300 # 5 dakika geçerli
    
    # Mevcut kodları oku
    data = {}
    if os.path.exists(OTP_FILE):
        with open(OTP_FILE, 'r') as f:
            data = json.load(f)
            
    # Yeni kodu ekle
    data[str(telegram_id)] = {"otp": otp, "expires": expiry}
    
    # Dosyayı kaydet
    with open(OTP_FILE, 'w') as f:
        json.dump(data, f)
        
    return otp

def verify_otp(telegram_id, submitted_otp):
    if not os.path.exists(OTP_FILE):
        return False
        
    with open(OTP_FILE, 'r') as f:
        data = json.load(f)
        
    record = data.get(str(telegram_id))
    if record and record['otp'] == submitted_otp and time.time() < record['expires']:
        return True
    return False
