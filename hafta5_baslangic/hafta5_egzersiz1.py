"""
    Bir markette barkod okuyucu sistem bozulmuştur. Bu yüzden kasiyerler her ürün için fiyatlara bakıp
    hesap makinesiyle fiş tutarını hesaplamaktadirlar. Bizden de onlara yardımcı olmak için fiş yazdıran
    ve toplam tutar hesaplayan bir program yazacağız.

    Marketle ilgili bilmemiz gerekenler şunlar:
    Markette iki çeşit ürün var: Biri kg olarak satılan ürünler diğeri de paket olarak satılan ürünler.
    İşimizi kolaylaştırmak için market çalışanları bu ürünleri ve ürünleri fiyatlarını listelediler.

    kg_urun_listesi=["elma","portakal","muz", "domates","kabak","marul"]
    kg_urun_fiyat_listesi=[2.25, 4.50, 10.0, 8.75, 8.50, 10.10]

    Buradan da anlaşılacağı gibi; elmanın 1 kg'lık için fiyatı 2.25, portakalın 1 kg'lık fiyatı 4.50...

    Gelen her müşteri için hangi ürünü aldıkları, aldıkları kg cinsinden satılan bir ürün ise kaç kg aldığı,
    paket cinsindense kaç paket aldığını soracağız ve bir ürün için ödemesi gereken fiyati, ürünün adını listelere
    kaydedeceğiz.

    Sonrasında bu listeler üzerinde gezinip fişi bastıracağız.

    # Örnek Çalışma Şekli
    Merhabalar, toplam fiyatı öğrenmek için ürünleri ve fiyatları girmeye başlayabilirsiniz!
    > Ürün adını giriniz: konserve
    > Kaç paket konserve aldınız?: 3
    > Ürün adını giriniz: portakal
    > Kaç kg portakal aldınız?: 1.5
    > Ürün adını giriniz: marul
    > Kaç kg marul aldınız?: 0.5
    > Ürün adını giriniz: çikolata
    > Kaç paket çikolata aldınız?: 3
    > Ürün adını giriniz: bitti

    > konserve  -> 60.0
    > portakal  -> 6.75
    > marul  -> 5.05
    > çikolata  -> 21.75
    > Toplam fiyat: 93.55

"""

kg_urun_listesi=["elma","portakal","muz", "domates","kabak","marul"]
kg_urun_fiyat_listesi=[2.25, 4.50, 10.0, 8.75, 8.50, 10.10]
paket_urun_listesi=["cips","çikolata", "kuruyemiş", "konserve"]
paket_urun_fiyat_listesi=[4.50, 7.25, 15.25, 20.0]



def fis_yazdir(urun_listesi, fiyat_listesi):
    pass


def main():
    print("Merhabalar, toplam fiyatı öğrenmek için ürünleri ve fiyatları girmeye başlayabilirsiniz!")
    urun_listesi = []
    fiyat_listesi = []


if __name__ == "__main__":
    main()
