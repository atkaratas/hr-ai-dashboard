import random
import time
import json
import os

OTP_FILE = 'projects/hr_ai_system/data/active_otps.json'

def generate_otp(telegram_id):
    otp = str(random.randint(100000, 999999))
    expiry = time.time() + 300 # 5 dakika geçerli
    
    data = {}
    if os.path.exists(OTP_FILE):
        with open(OTP_FILE, 'r') as f:
            try:
                data = json.load(f)
            except:
                data = {}
            
    data[str(telegram_id)] = {"otp": otp, "expires": expiry, "used": False}
    
    with open(OTP_FILE, 'w') as f:
        json.dump(data, f)
        
    return otp

def verify_and_burn_otp(telegram_id, submitted_otp):
    """Kodu doğrular ve anında imha eder (One-Time Only)."""
    if not os.path.exists(OTP_FILE):
        return False
        
    with open(OTP_FILE, 'r') as f:
        data = json.load(f)
        
    record = data.get(str(telegram_id))
    if record and record['otp'] == submitted_otp and not record.get('used') and time.time() < record['expires']:
        # Kodu kullanıldı olarak işaretle (Burn)
        data[str(telegram_id)]['used'] = True
        with open(OTP_FILE, 'w') as f:
            json.dump(data, f)
        return True
    return False
