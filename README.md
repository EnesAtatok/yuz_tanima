# Yüz Tanıma (Python)

C# / Emgu.CV ile yazılmış eski "YüzTanıma" projesinin Python + OpenCV karşılığı.
Kameradan yüz toplar, Fisherface ile eğitir, canlı olarak kimin olduğunu bulur.

## Kurulum (VS Code)

1. Python 3.10+ kurulu olsun.
2. Klasör Türkçe harf içermeyen bir yolda olursa en sorunsuzu (ör. `C:\projeler\yuz_tanima`), ama kod Türkçe harfli yollarda da çalışacak şekilde yazıldı.
   OpenCV, model dosyasını `ü`, `ı`, `ş` gibi harfler içeren yollara kaydedemeyebilir.
3. VS Code'da `File > Open Folder` ile klasörü açın.
4. Terminal açın (`Ctrl + ö` veya `Terminal > New Terminal`) ve sırayla:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

(Mac/Linux'ta ikinci satır: `source .venv/bin/activate`)

VS Code sağ altta interpreter sorarsa `.venv` seçin. `F5` ile de çalıştırabilirsiniz.

## Kullanım

1. **Kişinin adını** yazıp **Yüz Ekle**'ye basın. Kameraya bakın, 30 fotoğraf otomatik çekilir
   (ışığı ve yüz açısını biraz değiştirin). Çıkmak için `q` veya `ESC`.
2. Her kişi için tekrarlayın. **Fisherface için en az 2 kişi gerekir.**
3. **Modeli Eğit**'e basın.
4. **Yüz Tanımayı Başlat**'a basın. Yeşil kutu = tanındı, kırmızı = Bilinmiyor. Çıkış: `q` veya `ESC` (önce kamera penceresine bir kez tıklayın).

## Dosyalar

| Dosya | Görevi |
|---|---|
| `main.py` | tkinter menü penceresi (eski Form1.cs) |
| `config.py` | Tüm ayarlar (kamera no, foto sayısı, eşik, algoritma) |
| `yuz_bulucu.py` | Görüntüde yüz bulma, yüzü hazırlama |
| `cascade/` | Yüz bulma için hazır OpenCV dosyası (dokunmayın) |
| `veri_toplama.py` | Kameradan foto toplama |
| `egitim.py` | Model eğitimi (eski Classifier_Train.cs) |
| `tanima.py` | Canlı tanıma (eski FisherFaceRecognizer.cs / BusinessRecognition.cs) |
| `yardimci.py` | Türkçe harf / dosya okuma yardımcıları |
| `veri/yuzler/` | Kişi başına bir klasör, içinde fotoğraflar |
| `model/` | Eğitilmiş model (eski `yuz.xml`) |

## Sık sorunlar

- **Kamera açılmıyor:** `config.py` içinde `KAMERA_NO = 1` deneyin.
- **Herkes "Bilinmiyor" çıkıyor veya yanlış kişiyi buluyor:** Ekranda parantez içinde görünen sayı
  uzaklıktır (küçük = emin). Tanınan yüzlerde kaç çıktığına bakıp `config.py` içindeki `ESIK` değerini ayarlayın.
- **Tek kişiyle denemek istiyorum:** `ALGORITMA = "lbph"` yapın, modeli yeniden eğitin.
- **Sonuçlar kötü:** Her kişi için farklı ışık ve açılarla daha fazla fotoğraf toplayın.

## Not

`veri/` ve `model/` içeriği `.gitignore`'dadır; yüz fotoğrafları GitHub'a yüklenmesin.
Başkalarının yüzünü kaydederken izinlerini alın.
