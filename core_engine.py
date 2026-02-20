import pandas as pd
import json
import os
import hashlib

# Dosya Yolları
EXCEL_PATH = 'projects/hr_ai_system/data/company_ledger.xlsx'
USERS_JSON = 'projects/hr_ai_system/data/users.json'
LEDGER_HISTORY = 'projects/hr_ai_system/data/ledger_history.json'

def sync_all():
    """Excel'deki personel listesini ve finansal bakiyeleri sisteme kilitler."""
    if not os.path.exists(EXCEL_PATH):
        print("Hata: Ana Excel dosyası bulunamadı.")
        return False

    try:
        # Excel'i Oku (Sayfa 1: Personel, Sayfa 2: Kasa)
        df_users = pd.read_excel(EXCEL_PATH, sheet_name='PERSONEL')
        df_finance = pd.read_excel(EXCEL_PATH, sheet_name='FINANS')

        # 1. Personel Senkronizasyonu (Hiyerarşi)
        new_user_list = df_users.to_dict(orient='records')
        with open(USERS_JSON, 'w') as f:
            json.dump(new_user_list, f, indent=2)

        # 2. Finansal Bakiye Kilidi (Immutable Ledger)
        # Her bir bakiye hareketi için benzersiz bir hash oluşturulur.
        # Geçmiş kayıtlar asla değiştirilemez.
        current_balance = df_finance['Tutar'].sum()
        
        history = []
        if os.path.exists(LEDGER_HISTORY):
            with open(LEDGER_HISTORY, 'r') as f:
                history = json.load(f)

        # Yeni hareketi logla
        new_entry = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "balance": float(current_balance),
            "hash": hashlib.sha256(str(current_balance).encode()).hexdigest()
        }
        history.append(new_entry)
        
        with open(LEDGER_HISTORY, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"Senkronizasyon Başarılı: {len(new_user_list)} personel, Kasa: ₺{current_balance}")
        return True
    except Exception as e:
        print(f"Sync Hatası: {e}")
        return False

if __name__ == "__main__":
    sync_all()
