"""
Bu egzersizde bir listede verilmiş sayılar kadar arka arkaya farklı renklerde yağan yağmur animasyonları oluşturacağız.

Kodu test ederken YAGMUR_SAYILARI değişkenini 5 elemandan fazla içermemek üzere değiştireceğiz.
"""
from grafik.canvas import Canvas
import time
import random

KANVAS_EN = 800
KANVAS_BOY = 600

YAZI_Y = 25
YAZI_X = KANVAS_EN - 80
FONT = "Cambria"
FONT_BUYUKLUGU = 14

DAMLA_YARICAP = 3
DAMLA_BASLANGIC_Y = -2 * DAMLA_YARICAP

MIN_BASLANGIC_HIZ = 300
MAX_BASLANGIC_HIZ = 400

YER_CEKIMI = 100
YENILEME_SURESI = 0.01

YAGMUR_SAYILARI = [100, 200, 150 , 300]

MIN_YENI_DAMLA=2
MAX_YENI_DAMLA=5


def renkli_damla_olustur(kanvas, renk):
    """ bu fonksiyon kanvasın üstünde verilen renkte bir damla (oval) oluşturur """
    damla_x = random.randint(-DAMLA_YARICAP, KANVAS_EN - DAMLA_YARICAP)
    damla = kanvas.create_oval(damla_x, DAMLA_BASLANGIC_Y,
                               damla_x + 2 * DAMLA_YARICAP, DAMLA_BASLANGIC_Y + 2 * DAMLA_YARICAP)
    kanvas.set_fill_color(damla, renk)
    return damla

def rastgele_renk_sec():
    """ rastgele bir renk seçer """
    renkler = [Canvas.COLORS.Blue, Canvas.COLORS.Khaki3,
               Canvas.COLORS.Red, Canvas.COLORS.Green2, Canvas.COLORS.Plum1]
    return random.choice(renkler)

def yeni_damlalar_olustur(kanvas, damlalar, hizlar, renk):
    """ MIN_YENI_DAMLA ila MAX_YENI_DAMLA arasında bir sayı seçer, bu sayı kadar damla oluşturur ve damlalar listesine ekler
        her damla için rastgele bir hız seçer ve hızı hizlar listesine ekler """
    yeni_damla_sayisi = random.randint(MIN_YENI_DAMLA, MAX_YENI_DAMLA)
    for i in range(yeni_damla_sayisi):
        damlalar.append(renkli_damla_olustur(kanvas, renk))
        hizlar.append(random.randint(MIN_BASLANGIC_HIZ, MAX_BASLANGIC_HIZ))
        return yeni_damla_sayisi
        
def silinecek_damlalari_sil(kanvas, damlalar, hizlar, silinecek_indexler):
    """ silinecek_indexler listesinde indeksleri verilen damlaları kanvastan kaldırır, hizlar ve damlalar
        listelerini günceller """
    for silinecek_index in silinecek_indexler[::-1]:
        silinecek_damla = damlalar.pop(silinecek_index)
        hizlar.pop(silinecek_index)
        kanvas.delete(silinecek_damla)

def damlalari_hareket_ettir(kanvas, damlalar, hizlar):
    """ y eksenindeki hızları hizlar listesinde verilen damlaları """
    silinecek_indexler = []
    for damla_index in range(len(damlalar)):
        hizlar[damla_index] += YER_CEKIMI * YENILEME_SURESI
        kanvas.move(damlalar[damla_index], 0, hizlar[damla_index] * YENILEME_SURESI)

        if kanvas.get_top_y(damlalar[damla_index]) > KANVAS_BOY:
            silinecek_indexler.append(damla_index)
    return silinecek_indexler
            
def main():
    kanvas = Canvas(KANVAS_EN, KANVAS_BOY)
    kanvas.set_canvas_title("Yağmur")
    #kanvas.set_canvas_background_color(Canvas.COLORS.Black)
    damlalar = []
    hizlar = []
    kullanilmis_renkler = []
    for sayi in YAGMUR_SAYILARI:
        sec_renk = rastgele_renk_sec()
        while sec_renk in kullanilmis_renkler:
        	sec_renk = rastgele_renk_sec()
        kullanilmis_renkler.append(sec_renk)
        kalan_damla = sayi
        while kalan_damla > 0 or damlalar:
            # yeni damlalar olustur
            if kalan_damla > 0:
                yeni_damla = yeni_damlalar_olustur(kanvas, damlalar, hizlar, sec_renk)

            silinecek_indexler = damlalari_hareket_ettir(kanvas, damlalar, hizlar)

            silinecek_damlalari_sil(kanvas, damlalar, hizlar, silinecek_indexler)

            kalan_damla -= yeni_damla
            kanvas.update()  
            time.sleep(YENILEME_SURESI)

if __name__ == "__main__":
    main()