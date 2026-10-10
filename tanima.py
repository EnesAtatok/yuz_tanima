"""3. ADIM: Kameradaki yüzleri eğitilmiş modelle tanır, duygu analizi ve sesli bildirim yapar."""
import json
import threading
import time
from pathlib import Path
import cv2
import numpy as np

import config
from egitim import tanimlayici_olustur
from yardimci import ascii_yap, cikis_istendi, model_yukle
from yuz_bulucu import kamera_ac, yuzleri_bul, yuzu_hazirla

PENCERE = "Yuz Tanima (cikis: q veya ESC)"

# Duygu Etiketleri (ONNX FER+)
DUYGU_LISTESI = [
    "Notr",
    "Mutlu",
    "Saskin",
    "Uzgun",
    "Sinirli",
    "Igrenmis",
    "Korkmus",
    "Kucumseme"
]

son_konusma_zamanlari = {}


def seslendir(metin: str):
    """Windows COM motorunu başlatarak sesi arka planda güvenle çalar."""
    def _konus():
        try:
            import pythoncom
            pythoncom.CoInitialize()  # Windows thread ses motoru başlatıcısı
            import pyttsx3
            motor = pyttsx3.init()
            motor.setProperty("rate", 140)  # Konuşma hızı
            motor.say(metin)
            motor.runAndWait()
        except Exception as e:
            print("Seslendirme Hatası:", e)

    threading.Thread(target=_konus, daemon=True).start()


def tani():
    """Kamerayı açıp yüzleri tanır ve duygu durumunu gösterir. Çıkmak için 'q'."""
    if not config.MODEL_YOLU.exists():
        raise FileNotFoundError("Model bulunamadı. Önce 'Modeli Eğit' düğmesine basın.")

    tanimlayici = tanimlayici_olustur()
    model_yukle(tanimlayici, config.MODEL_YOLU)
    with open(config.ETIKET_YOLU, encoding="utf-8") as f:
        isimler = json.load(f)
    esik = config.ESIK[config.ALGORITMA]

    # Varsa duygu modelini hazırla
    duygu_agi = None
    duygu_yolu = Path("duygu_modeli.onnx")
    if duygu_yolu.exists():
        try:
            duygu_agi = cv2.dnn.readNetFromONNX(str(duygu_yolu))
        except Exception:
            duygu_agi = None

    kamera = kamera_ac()
    kare_sayaci = 0
    son_duygu = "Notr"

    while True:
        basarili, kare = kamera.read()
        if not basarili:
            break
        kare_sayaci += 1
        gri = cv2.cvtColor(kare, cv2.COLOR_BGR2GRAY)
        simdi = time.time()

        for kutu in yuzleri_bul(gri):
            x, y, w, h = kutu
            etiket, uzaklik = tanimlayici.predict(yuzu_hazirla(gri, kutu))

            # Duygu Analizi (Model mevcutsa her 3 karede bir hesapla)
            if duygu_agi is not None and kare_sayaci % 3 == 0 and w > 40 and h > 40:
                try:
                    yuz_yeniden = cv2.resize(gri[y:y+h, x:x+w], (64, 64))
                    blob = cv2.dnn.blobFromImage(yuz_yeniden, 1.0, (64, 64), (0,), False, False)
                    duygu_agi.setInput(blob)
                    ciktilar = duygu_agi.forward()
                    son_duygu = DUYGU_LISTESI[int(np.argmax(ciktilar[0]))]
                except Exception:
                    pass

            # Orijinal Tanıma Kararı
            if uzaklik < esik:
                kisi_adi = ascii_yap(isimler[str(etiket)] if str(etiket) in isimler else isimler[etiket])
                yazi, renk = f"{kisi_adi} ({uzaklik:.0f})", (0, 255, 0)

                # Sesli anons
                if kisi_adi not in son_konusma_zamanlari or (simdi - son_konusma_zamanlari[kisi_adi] > 8):
                    son_konusma_zamanlari[kisi_adi] = simdi
                    seslendir(f"Hos geldin {kisi_adi}")
            else:
                yazi, renk = f"Bilinmiyor ({uzaklik:.0f})", (0, 0, 255)
                if "bilinmiyor" not in son_konusma_zamanlari or (simdi - son_konusma_zamanlari["bilinmiyor"] > 6):
                    son_konusma_zamanlari["bilinmiyor"] = simdi
                    seslendir("Dikkat yetkisiz kisi algilandi")

            # Kutu ve Bilgi Çizimi
            cv2.rectangle(kare, (x, y), (x + w, y + h), renk, 2)
            cv2.putText(kare, yazi, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, renk, 2)
            
            # Duygu durumunu yüzün altına yaz
            if duygu_agi is not None:
                cv2.putText(kare, f"Duygu: {son_duygu}", (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)

        cv2.imshow(PENCERE, kare)
        if cikis_istendi(PENCERE):
            break

    kamera.release()
    cv2.destroyAllWindows()