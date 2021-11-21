"""
Bu egzersizde bir listede verilmiş sayılar kadar arka arkaya farklı renklerde yağan yağmur animasyonları oluşturacağız.

Kodu test ederken YAGMUR_SAYİLARİ değişkenini 5 elemandan fazla içermemek üzere değiştireceğiz.
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

MAX_YENI_DAMLA = 5
MIN_YENI_DAMLA = 2

YAGMUR_SAYILARI = [100, 200, 150, 300]

MIN_YENI_DAMLA = 2
MAX_YENI_DAMLA = 5


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


def main():
    kanvas = Canvas(KANVAS_EN, KANVAS_BOY)
    kanvas.set_canvas_title("Yağmur")

    # animasyonu yazdıktan sonra bu satırı silebilirsin
    Canvas.wait_for_click()


if __name__ == "__main__":
    main()
