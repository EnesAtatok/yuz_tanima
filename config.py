"""Projenin tüm ayarları burada. Değiştirmek istediğiniz sayıları buradan değiştirin."""
from pathlib import Path

KOK = Path(__file__).resolve().parent
VERI_KLASORU = KOK / "veri" / "yuzler"        # her kişi için bir alt klasör
MODEL_YOLU = KOK / "model" / "yuz_modeli.xml"  # eğitilmiş model (eski projedeki yuz.xml gibi)
ETIKET_YOLU = KOK / "model" / "etiketler.json"  # 0 -> "Ali", 1 -> "Ayşe" ...
CASCADE_YOLU = KOK / "cascade" / "haarcascade_frontalface_default.xml"  # yüz bulma dosyası

KAMERA_NO = 0            # bilgisayarın kamerası genelde 0'dır, çalışmazsa 1 deneyin
YUZ_BOYUTU = (100, 100)  # tüm yüzler bu boyuta getirilir (Fisherface için şart)
FOTO_SAYISI = 30         # bir kişi için kaç fotoğraf çekilecek

# "fisher" -> eski projedeki gibi Fisherface (en az 2 kişi gerekir)
# "lbph"   -> tek kişiyle de çalışır, ışık değişimine daha dayanıklı
ALGORITMA = "fisher"

# Uzaklık bu değerden BÜYÜKSE "Bilinmiyor" denir. Küçük olması = daha emin demek.
# Ekranda görünen sayıya bakarak kendi ortamınıza göre ayarlayın.
ESIK = {
    "lbph": 115,   # 70-80 ise 115-120 yapın
    "eigen": 5000,
    "fisher": 500
}
