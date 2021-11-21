import random
import tkinter
import tkinter.font
from .colors import CanvasColors

"""
File: canvas.py
Adapted from the original file by the authors: Chris Piech, Lisa Yan and Nick Troccoli to support Turkish documentation
Authors: Chris Piech, Lisa Yan and Nick Troccoli

Version Date: October 25, 2020
TODO notes:
- support window resizing
- getters for font, outline width, etc.
- mouse dragged
- wait for key press
- rotate resimler
- create polygon
"""


class Canvas(tkinter.Canvas):
    """
    Canvas, grafiksel objelerle işlem yapmayı kolaylaştırmak için Python'ın thinkter kütüphanesindeki Canvas objesi
    üzerine kurulmuş basitleştirilmiş bir arayüzdür. Canvas grafiksel objeleri yaratmak, modifiye etmek ve silmek için
    çeşitli fonksiyonlara sahiptir. Ayrıca kendisi ve üzerinde barındırdığı grafiksel objeler hakkında bilgi almamızı
    sağlayan fonksiyonları da mevcuttur. Canvas 'thinkter.Canvas' ın bir alt sınıfı olduğu için, gerektiğinde thinkter
    fonksiyonları da Canvas'tan erişilebilir.

    """

    DEFAULT_WIDTH = 754
    """Canvas'ın varsayılan genişliği 754 pixeldir."""

    DEFAULT_HEIGHT = 492
    """Canvas'ın varsayılan uzunluğu 492 pixeldir."""

    DEFAULT_TITLE = "Canvas"
    """Varsayılan olarak Canvas penceresi açıldığında başlık kısmında 'Canvas' başlığı gösterilir."""

    COLORS = CanvasColors

    """CanvasColors canvasda kullanabileceğimiz tüm renkleri içeren bir enum sınıfıdır. """

    _colornames = list(COLORS.__members__.keys())
    _colorvalues = list(map(lambda enumcolor : enumcolor.value, list(CanvasColors.__members__.values())))

    LEFT = tkinter.LEFT
    """
    Canvas'ın farklı bölgelerine etkileşim araçları eklemeyi sağlayan yönler.
    LEFT pencerenin sol tarafı için kullanılır.
    """

    BOTTOM = tkinter.BOTTOM
    """
    Canvas'ın farklı bölgelerine etkileşim araçları eklemeyi sağlayan yönler.
    BOTTOM pencerenin alt tarafı için kullanılır.
    """

    RIGHT = tkinter.RIGHT
    """
    Canvas'ın farklı bölgelerine etkileşim araçları eklemeyi sağlayan yönler.
    RIGHT pencerenin sağ tarafı için kullanılır.
    """

    TOP = tkinter.TOP
    """
    Canvas'ın farklı bölgelerine etkileşim araçları eklememizi sağlayan yönler.
    LEFT pencerenin sol tarafı için kullanılır.
    """

    def __init__(self, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        """
        Canvas yaratırken, opsiyonel olarak genişlik ve uzunluğunu belirtilebilir. Eğer genişlik ve uzunluk
        bilgisi sağlanmazsa canvas varsayılan boyutlarda yaratılır.
        Args:
            width: yaratılacak Canvas'ın genişliği (eğer belirtilmemişse, `Canvas.DEFAULT_WIDTH` yani varsayılan genişlik kullanılır)
            height: yaratılacak Canvas'ın uzunluğu (eğer belirtilmemişse, `Canvas.DEFAULT_HEIGHT` yani varsayılan uzunluk kullanılır)
        """

        # Create the main program window
        self.main_window = tkinter.Tk()
        self.main_window.geometry("{}x{}".format(width, height))
        self.main_window.title(self.DEFAULT_TITLE)

        # Create 4 perimeter frames to hold any buttons added later
        self.bottom_frame = tkinter.Frame(self.main_window)
        self.bottom_frame.pack(side=Canvas.BOTTOM)

        self.top_frame = tkinter.Frame(self.main_window)
        self.top_frame.pack(side=Canvas.TOP)

        self.right_frame = tkinter.Frame(self.main_window)
        self.right_frame.pack(side=Canvas.RIGHT)

        self.left_frame = tkinter.Frame(self.main_window)
        self.left_frame.pack(side=Canvas.LEFT)

        # call the tkinter Canvas constructor
        super().__init__(self.main_window, width=width, height=height, bd=0, highlightthickness=0)

        # Optional callbacks the client can specify to be called on each event
        self.on_mouse_pressed = None
        self.on_mouse_released = None
        self.on_key_pressed = None
        self.on_button_clicked = None

        # Tracks whether the mouse is currently on top of the canvas
        self.mouse_on_canvas = False

        # List of presses not handled by a callback
        self.mouse_presses = []

        # List of key presses not handled by a callback
        self.key_presses = []

        # List of button clicks not handled by a callback
        self.button_clicks = []

        # Map of text fields accessible by label name
        self.text_fields = {}

        # These are state variables so wait_for_click knows when to stop waiting and to
        # not call handlers when we are waiting for click
        self.wait_for_click_click_happened = False
        self.currently_waiting_for_click = False

        # bind events
        self.focus_set()
        self.bind("<Button-1>", lambda event: self.__mouse_pressed(event))
        self.bind("<ButtonRelease-1>", lambda event: self.__mouse_released(event))
        self.bind("<Key>", lambda event: self.__key_pressed(event))
        self.bind("<Enter>", lambda event: self.__mouse_entered())
        self.bind("<Leave>", lambda event: self.__mouse_exited())

        self._image_gb_protection = {}
        self.pack()
        self.update()

    def set_canvas_background_color(self, color):
        """
        Canvas'ın arka planını color stringine karşılık gelen renge boyar.
        Args:
            color: canvas'ın arka planını boyamak istediğimiz rengin adı (string).
        """
        self.config(background=color.value)

    def get_canvas_background_color(self):
        """
        Canvas'ın arka plan renginin adını almamızı sağlar.
        Returns:
            canvas'ın arka plan renginin adı (string formatında)
        """
        return self.COLORS(self["background"])

    def get_canvas_width(self):
        """
        Canvas'ın genişliğini almamızı sağlar.
        Returns:
            canvas'ın şu anki genişliği
        """

        return self.winfo_width()

    def get_canvas_height(self):
        """
        Canvas'ın uzunluğunu almamızı sağlar.
        Returns:
            canvas'ın şu anki uzunluğu
        """
        return self.winfo_height()

    def set_canvas_title(self, title):
        """
        Canvas penceresinin başlık kısmındaki texti verilen text ile değiştirir.
        Args:
            title: canvas penceresinin başlık kısmında gösterilecek yeni başlık
        """
        self.main_window.title(title)

    def set_canvas_size(self, width, height):
        """
        Canvas'ı ve onu içeren pencereyi verilen genişlik ve uzunlukta olacak şekilde
        yeniden boyutlandırır.
        Args:
            width: canvas ve onu içeren pencerenin yeni genişliği
            height: canvas ve onu içeren pencerenin yeni uzunluğu
        """
        self.main_window.geometry("{}x{}".format(width, height))
        self.config(width=width, height=height)

    """ EVENT HANDLING """

    def set_on_mouse_pressed(self, callback):
        """
        Fareye her basıldığında verilen fonksiyonun çağrılmasını sağlar. Eğer set_on_mouse_pressed fonksiyonu
        birden çok kez çağrılırsa, en son çağrılışında verilen fonksiyon fareye basıldığında çağrılır. 
        Args:
            callback: fareye her basıldığında çağrılacak fonksiyon. Bu fonksiyon 2 parametre almalı:
            farenin basıldığı noktanın (sırasıyla) x ve y koordinatları. Örneğin, func(x, y). Eğer
            bu parametre None ise, fareye basıldığında hiçbir fonksiyon çağrılmaz.
        """
        self.on_mouse_pressed = callback

    def set_on_mouse_released(self, callback):
        """
        Fare her serbest bırakıldığında verilen fonksiyonun çağrılmasını sağlar. Eğer set_on_mouse_released fonksiyonu
        birden çok kez çağrılırsa, en son çağrılışında verilen fonksiyon fare serbest bırakıldığında çağrılır. 
        Args:
            callback: fare her serbest bırakıldığında çağrılacak fonksiyon. Bu fonksiyon 2 parametre almalı:
            farenin serbest bırakıldığı noktanın (sırasıyla) x ve y koordinatları. Örneğin, func(x, y). Eğer
            bu parametre None ise, fare serbest bırakıldığında hiçbir fonksiyon çağrılmaz.
        """
        self.on_mouse_released = callback

    def set_on_key_pressed(self, callback):
        """
        Her klavyeye basıldığında verilen fonksiyonun çağrılmasını sağlar. Eğer set_on_key_pressed fonksiyonu birden
        çok kez çağrılırsa, en son çağrılışında verilen fonksiyon klavyeye basıldığında çağrılır. 
        Args:
            callback: klavyeye her basıldığında çağrılacak fonksiyon. Bu fonksiyon 1 parametre almalı: 
            klavyede basılan tuşun adı(a tuşu için 'a', b tuşu için 'b', etc.). Örneğin, func(key_char). Eğer bu 
            parametre None ise, klavyeye basıldığında hiçbir fonksiyon çağrılmaz.  
        """
        self.on_key_pressed = callback

    def set_on_button_clicked(self, callback):
        """
        Her butona tıklandığında verilen fonksiyonun çağrılmasını sağlar. Eğer set_on_button_clicked fonksiyonu
        birden çok kez çağrılırsa, en son çağrılışında verilen fonksiyon butona her tıklandığında çağrılır.
        Args:
            callback: butona her tıklandığında çağrılacak fonksiyon. Bu fonksiyon 1 parametre almalı:
            tıklanan butonun adı. Örneğin, func(button_name). Eğer bu parametre None ise, butona tıklandığında
            hiçbir fonksiyon çağrılmaz.
        """
        self.on_button_clicked = callback

    def __button_clicked(self, title):
        """
        Her butona tıklandığında bu fonksiyon çağrılır. Eğer butona atanmış bir tıklanma işleyicisi varsa, bu işleyiciyi
        çağırır. Aksi halde, tıklanmayı daha sonra işlenecek buton tıklanmaları listesini ekler.
        Args:
            title: tıklanan butonun adı
        """
        if self.on_button_clicked:
            self.on_button_clicked(title)
        else:
            self.button_clicks.append(title)

    def get_new_mouse_clicks(self):
        """
        Bu fonksiyonun veya herhangi bir fare işleyicisinin en son çağrılışından beri gerçekleşen fare tıklanmalarının bir
        listesini döndürür.
        Returns:
            bu fonksiyonun veya herhangi bir fare işleyicisinin en son çağrılışından beri gerçekleşen fare tıklanmaları.
            Her tıklanma farenin tıkladığı lokasyonun x ve y koordinatlarını içerir, örneğin
            clicks = canvas.get_new_mouse_clicks(); 
            print(clicks[0].x)
        """
        presses = self.mouse_presses
        self.mouse_presses = []
        return presses

    def get_new_key_presses(self):
        """
        Bu fonksiyonun veya herhangi bir klavye tuşu işleyicisinin en son çağrılışından beri basılan tuşların
        bir listesini döndürür.
        Returns:
            bu fonksiyonun veya herhangi bir klavye tuşu işleyicisinin en son çağrılışından beri basılan tuşların bir listesi.
            Bu listenin herbir elemenaı, basılan tuş için keysym adlı bir özelliğe sahiptir. Örneğin,
            presses = canvas.get_new_key_presses()
            print(presses[0].keysym) 
        """
        presses = self.key_presses
        self.key_presses = []
        return presses

    def get_new_button_clicks(self):
        """
        Bu fonksiyonun veya herhangi bir buton tıklanması işleyicisinin en son çağrılışından beri tıklanan butonların
        bir listesini döndürür.
        Returns:
            bu fonksiyonun veya herhangi bir buton tıklanması işleyicisinin en son çağrılışından beri tıklanan
            butonların bir listesi. Listenin her elemanı o sırada tıklanmış olan butonun adıdır. Örneğin,
            clicks = canvas.get_new_button_clicked()
            print(click[0])
        """
        clicks = self.button_clicks
        self.button_clicks = []
        return clicks

    def __mouse_pressed(self, event):
        """
        Her fareye basıldığında çağrılır. Eğer wait_for_click ile bir fare tıklamasının gerçekleşmesini bekliyorsak,
        hiçbir şey yapmaz. Eğer, farenin basılması olayına ait bir işleyicimiz varsa varsa, onu çağırır.
        Aksi halde, fareye basılma olayını daha sonra işlenecek fare basılmaları listesine ekler.
        Args:
            event: fareye basıldığını gösteren bir obje. Farenin basıldığı noktanın x ve y koordinatlarına
            sahip olduğunu varsayabilirsiniz. 
        """
        if not self.currently_waiting_for_click and self.on_mouse_pressed:
            self.on_mouse_pressed(event.x, event.y)
        elif not self.currently_waiting_for_click:
            self.mouse_presses.append(event)

    def __mouse_released(self, event):
        """
        Fare her serbest bırakıldığında çağrılır. Eğer şu an wait_for_click'i kullanarak bir fare tıklanması için bekliyorsak
        programımızın durumunu tıklama gerçekleşti olarak günceller. Aksi halde, eğer farenin serbest bırakılması olayına
        ait bir işleyicimiz varsa, onu çağırır. 
        Args:
            event: farenin serbest bırakıltığını temsil eden bir obje. Farenin serbest bırakıldığı
            noktanın x ve y koordinatlarına sahip olduğu varsayılabilir. 
        """

        # Do this all in one go to avoid setting click happened to True,
        # then having wait for click set currently waiting to false, then we go
        if self.currently_waiting_for_click:
            self.wait_for_click_click_happened = True
            return

        self.wait_for_click_click_happened = True
        if self.on_mouse_released:
            self.on_mouse_released(event.x, event.y)

    def __key_pressed(self, event):
        """
        Her klavye tuşuna basıldığında çağrılır. Eğer bir klavye tuşu işleyicimiz varsa, onu çağırır. Eğer yoksa, yeni
        basılan klavye tuşunu daha sonra işlenecek klavye tuşları listesine ekler.
        Args:
            event: klavye tuşuna basıldığını temsil eden bir obje, basılan klavye tuşunun adını veren kysym özelliğine sahip olduğunu
            varsayabilirsiniz.
        """
        if self.on_key_pressed:
            self.on_key_pressed(event.keysym)
        else:
            self.key_presses.append(event)

    def __mouse_entered(self):
        """
        Farenin canvas sınırları içerisine her girişinde çağrılır. Farenin şu an canvas sınırları içerisinde olduğu
        kaydedilir.
        """
        self.mouse_on_canvas = True

    def __mouse_exited(self):
        """
        Farenin canvas sınırlarından her çıkışında çağrılır. Farenin şu an canvas sınırları içerisinde
        olmadığı kaydedilir.
        """
        self.mouse_on_canvas = False

    def mouse_is_on_canvas(self):
        """
        Farenin şu an canvas üzerinde olup olmadığını döndürür.
        Returns whether or not the mouse is currently on the canvas.
        Returns:
            eğer fare canvas üzerindeyse True, aksi halde False.
        """
        return self.mouse_on_canvas

    def wait_for_click(self):
        """
        Fareye tıklanana kadar bekler, tıklama gerçekleştiğinde sonlanır.
        """
        self.currently_waiting_for_click = True
        self.wait_for_click_click_happened = False
        while not self.wait_for_click_click_happened:
            self.update()
        self.currently_waiting_for_click = False
        self.wait_for_click_click_happened = False

    def get_mouse_x(self):
        """
        Farenin canvas üzerindeki konumunun x koordinatını verir.
        Returns:
            farenin canvas üzerindeki konumunun x koordinatı
        """
        """
        Note: winfo_pointery farenin ekran üzerindeki mutlak pozisyonudur. (pencere üzerinde değil),
              winfo_rooty farenin pencere üzerindeki mutlak pozisyonudur
        Farenin pencereye göre hareketini önemsediğimiz için, mouse_x'i farenin pencereye göre olan pozisyonuna 
        göre ayarladık.
        """
        return self.winfo_pointerx() - self.winfo_rootx()

    def get_mouse_y(self):
        """
        Farenin canvas üzerindeki konumunun y koordinatını verir.
        Returns:
            farenin canvas üzerindeki konumunun y koordinatı
        """
        """
        Note: winfo_pointery farenin ekran üzerindeki mutlak pozisyonudur. (pencere üzerinde değil),
              winfo_rooty farenin pencere üzerindeki mutlak pozisyonudur
        Farenin pencereye göre hareketini önemsediğimiz için, mouse_y'yi farenin pencereye göre olan pozisyonuna 
        göre ayarladık.
        """
        return self.winfo_pointery() - self.winfo_rooty()

    def __get_frame_and_pack_location_for_location(self, location):
        """
        Canvas'ta verilen konumdaki etkileşim aracı için kullanılması gereken çerçeve ve paket konumunu döndürür.  
        Args:
            location: çerçeve ve paket konumu alınacak bölge (Canvas.TOP/LEFT/BOTTOM/RIGHT)
        Returns:
            verilen etkileşim aracı konumu için sırasıyla çerçeve ve paket lokasyonları.
            Örneğin, üst ve alt bölgeler için, etkileşim araçlarını soldan sağa doğru yerleştirmek için
            paket konumu Canvas.LEFT olmalı.
        """
        frame = self.top_frame
        pack_location = Canvas.LEFT
        if location == Canvas.BOTTOM:
            frame = self.bottom_frame
        elif location == Canvas.LEFT:
            frame = self.left_frame
            pack_location = Canvas.TOP
        elif location == Canvas.RIGHT:
            frame = self.right_frame
            pack_location = Canvas.TOP

        return frame, pack_location

    def create_button(self, title, location, **kwargs):
        """
        Canvas'a verilen başlıkla belirtilen lokasyona bir buton ekler. Butonlar canvas'ın üst ve alt kısımlarında soldan sağa,
        sol ve sağ kısımlarında üstten alta eklenir.
        Args:
            title: buton üzerinde gösterilecek başlık. Diğer buton isimleri içerisinde benzersiz olmalıdır.
            location: canvas üzerinde butonu eklemek istediğimiz bölge (Canvas.TOP/LEFT/BOTTOM/RIGHT)
            kwargs: diğer thinkter keyword argümanları
        Returns:
            belirtilen pozisyona eklenen butona ait bir referans
        """
        frame, pack_location = self.__get_frame_and_pack_location_for_location(location)
        button = tkinter.Button(frame, text=title, command=lambda: self.__button_clicked(title), **kwargs)
        button.pack(side=pack_location)
        self.update()
        return button

    def create_text_field(self, label, location, **kwargs):
        """
        Canvas'ta verilen pozisyona bir text field etiketi ve text field objesi ekler.
        Etkileşim araçları canvas'ın üst ve alt kısmında soldan sağa doğru eklenirken, sol ve sağ kısmında
        yukarıdan aşağıya eklenir. Canvas'ın text field objeleri kayıtlarına oluşturduğu text field objesini de ekler.
        Args:
            label: text field objesinin yanında gösterilecek oaln text, aynı zamanda text field objesinin adı.
                Diğer text field objesi isimleri içerisinde benzersiz olmalıdır.
            location: canvas üzerinde text field etiketini ve objesini eklemek istediğimiz bölge (Canvas.TOP/BOTTOM/LEFT/RIGHT)
            kwargs: text field objeleri için diğer thinkter keyword argümanları
        Returns:
            verilen pozisyona eklenen text field objesine ait bir referans
        """
        frame, pack_location = self.__get_frame_and_pack_location_for_location(location)
        tkinter.Label(frame, text=label).pack(side=pack_location)
        text_field = tkinter.Entry(frame, **kwargs)
        text_field.pack(side=pack_location)
        self.text_fields[label] = text_field
        self.update()
        return text_field

    def get_text_field_text(self, text_field_name):
        """
        Verilen isimdeki text field objesinin güncel içeriğini döndürür.
        Args:
            text_field_name: yaratılmış text field objesinin adı
        Returns:
            verilen isimdeki text field objesinin güncel içeriği, veya bu isimde bir text field yoksa None.
        """
        if text_field_name in self.text_fields:
            return self.text_fields[text_field_name].get()
        else:
            return None

    """ GRAFİKSEL OBJE MANİPÜLASYONU """

    def get_left_x(self, obj):
        """
        Verilen grafiksel objenin sol üst köşesinin x koordinatını döndürür.
        Args:
            obj: sol üst köşesinin x koordinatını almak istediğimiz obje
        Returns:
            verilen objenin sol üst köşesinin x koordinatı
        """
        if self.type(obj) != "text":
            return self.coords(obj)[0]
        else:
            return self.coords(obj)[0] - self.get_width(obj) / 2

    def get_top_y(self, obj):
        """
        Verilen grafiksel objenin sol üst köşesinin y koordinatını döndürür.
        Args:
            obj: sol üst köşesinin y koordinatını almak istediğimiz obje
        Returns:
            verilen objenin sol üst köşesinin y koordinatı
        """
        if self.type(obj) != "text":
            return self.coords(obj)[1]
        else:
            return self.coords(obj)[1] - self.get_height(obj) / 2

    def get_width(self, obj):
        """
        Verilen grafiksel objenin genişliğini döndürür
        Args:
            obj: genişliğini öğrenmek istediğimiz obje
        Returns:
            verilen grafiksel objenin genişliği.
        """
        if len(self.coords(obj)) == 2:  # two-dimensional coords
            return self.bbox(obj)[2] - self.bbox(obj)[0]
        return self.coords(obj)[2] - self.coords(obj)[0]

    def get_height(self, obj):
        """
        Verilen grafiksel objenin yüksekliğini döndürür.
        Args:
            obj: yüksekliğini öğrenmek istediğimiz obje
        Returns:
            verilen grafiksel objenin yüksekliği
        """
        if len(self.coords(obj)) == 2:  # two-dimensional coords
            return self.bbox(obj)[3] - self.bbox(obj)[1]
        return self.coords(obj)[3] - self.coords(obj)[1]

    def move_to(self, obj, new_x, new_y):
        """
        `Canvas.moveto`. ile aynı işlevi görür.
        """
        # Note: Implements manually due to inconsistencies on some machines of bbox vs. coord.
        old_x = self.get_left_x(obj)
        old_y = self.get_top_y(obj)
        self.move(obj, new_x - old_x, new_y - old_y)

    def moveto(self, obj, x='', y=''):
        """
        Verilen grafiksel objeyi belirtilen koordinatlara taşır, objenin sol üst köşesinin koordinatları
        verilen koordinata gelecek şekilde obje canvas'a yerleştirilir.
        Args:
            obj: taşımak istediğimiz obje
            x: objenin sol üst köşesinin yeni x koordinatı 
            y: objenin sol üst köşesinin yeni y koordinatı 
        """
        self.move_to(obj, float(x), float(y))

    def move(self, obj, dx, dy):
        """
        Verilen grafiksel objeyi x ve y eksenlerinde belirtilen miktarlarda taşır.
        Args:
            obj: taşımak istediğimiz obje
            dx: objeyi x ekseninde taşımak istediğimiz miktar
            dy: objeyi y ekseninde taşımak istediğimiz miktar
        """
        super(Canvas, self).move(obj, dx, dy)

    def set_size(self, obj, width, height):
        """
        Verilen grafiksel objenin genişlik ve uzunluğunu değiştirmemize yarar. Resim objelerinin boyutunu
        değiştirmek için kullanılamaz.
        Args:
            obj: boyutlarını değiştirmek istediğimiz obje
            width: objenin yeni genişliği
            height: objenin yeni uzunluğu
        """
        if self.type(obj) == "image":
            assert False, "Image size cannot be changed after creating the image"
        x = self.get_left_x(obj)
        y = self.get_top_y(obj)
        self.coords(obj, x, y, x + width, y + height)

    def delete(self, obj):
        """
        Belirtilen grafiksel objeyi canvas'tan siler.
        Args:
            obj: canvas'tan silmek istediğimiz obje
        """
        super(Canvas, self).delete(obj)

    def delete_all(self):
        """
        Canvas'tan tüm objeleri siler.
        """
        super(Canvas, self).delete('all')

    def set_hidden(self, obj, hidden):
        """
        Verilen grafiksel objenin görünürlüğünü canvas üzerinde değiştirmemize yarar.
        Args:
            obj: canvas üzerinde görünürlüğünü değiştirmek istediğimiz obje.
            hidden: eğer obje görünmez yapılacaksa True, eğer obje görünür yapılacaksa False.
        """
        self.itemconfig(obj, state='hidden' if hidden else 'normal')

    def is_hidden(self, obj):
        """
        Verilen grafiksel objenin canvas'ta görünmez veya görünür olduğunu öğrenmemize yarar.
        Args:
            obj: durumunu öğrenmek istediğimiz grafiksel obje
        Returns:
            eğer grafiksel obje görünmez ise True, diğer türlü False.
        """
        return self.itemcget(obj, "state") == 'hidden'

    def find_element_at(self, x, y):
        """
        Bu koordinatlarla çakışan en üstteki grafiksel objeyi bulur.
        Args:
            x: o noktadaki elemanı bulmak istediğimiz noktanın x koordinatı
            y: o noktadaki elemanı bulmak istediğimiz noktanın y koordinatı
        Returns:
            bu koordinatlarda en üstteki grafiksel obje (eğer böyle bir obje yoksa None)
        """
        closest = self.find_closest(x, y)[0]

        closest_left_x = self.get_left_x(closest)
        closest_right_x = closest_left_x + self.get_width(closest)
        closest_top_y = self.get_top_y(closest)
        closest_bottom_y = closest_top_y + self.get_height(closest)

        # If this object entirely contains this point, then return it.  Otherwise, there is no object here.
        if closest_left_x <= x <= closest_right_x and closest_top_y <= y <= closest_bottom_y:
            return closest

        return None

    def find_overlapping(self, x1, y1, x2, y2):
        """
        Verilen sınırlayıcı kutu ile kesişen grafiksel objelerin bir listesini döndürür.
        Args:
            x1: sınırlayıcı kutunun sol üst köşesinin x koordinatı 
            y1: sınırlayıcı kutunun sol üst köşesinin y koordinatı
            x2: sınırlayıcı kutunun sağ alt köşesinin x koordinatı
            y2: sınırlayıcı kutunun sağ alt köşesinin y koordinatı
        Returns:
            canvas üzerinde verilen sınırlayıcı kutu ile kesişen grafiksel objelerin bir listesi
        """
        return super(Canvas, self).find_overlapping(x1, y1, x2, y2)

    def find_all(self):
        """
        Canvas üzerindeki grafiksel objelerin bir listesini döndürür.
        Returns:
            canvas üzerindeki tüm grafiksel objelerin bir listesi
        """
        return super(Canvas, self).find_all()

    def get_random_color(self):
        """
        Rastgele seçilmiş bir renk döndürür.
        Returns:
            Rastgele seçilmiş bir renk, string formatında.
        """
        return self.COLORS(random.choice(self._colorvalues))

    def set_fill_color(self, obj, fill_color):
        """
        Verilen grafiksel objenin dolgu rengini değiştirmemizi sağlar. Image objeleri gibi doldurulamayan grafiksel
        objelerin rengini değiştirmek için kullanılamaz. thinkter.TclError hatası verir.
        Args:
            obj: dolgu rengini değiştirmek istediğimiz obje
            fill_color: objenin yeni dolgu renginin adı, string formatında. Eğer bu string boşsa
            obje dolgusuz olacak şekilde ayarlanır.
        """
        try:
            self.itemconfig(obj, fill=fill_color.value)
        except tkinter.TclError:
            raise tkinter.TclError("You can't set the fill color on this object")

    def get_fill_color(self, obj):
        """
        Verilen grafiksel objenin dolgu rengini almamızı sağlar. Resim objeleri gibi içi doldurulamayan
        objelerin dolgu rengini almak için kullanılamaz. thinkter.TclError hatası verir.
        Args:
            obj: dolgu rengini öğrenmek istediğimiz obje
        Returns:
            Objenin dolgu rengi, string formatında. Eğer bu boş bir stringse, objenin içi henüz doldurulmamış demektir.
        """
        try:
            return self.COLORS(self.itemcget(obj, 'fill'))
        except tkinter.TclError:
            raise tkinter.TclError("You can't get the fill color of this object")

    def set_outline_color(self, obj, outline_color):
        """
        Verilen grafik objesinin anahat rengini değiştirmemize yarar. Resim ve text objeleri gibi anahattı olmayan
        objelerle birlikte kullanılamaz. thinkter.TclError hatası verir.
        Args:
            obj: anahat rengini değiştirmek istediğimiz obje
            outline_color: objenin anahattının olmasını istediğimiz renk, string formatında. Eğer boş bir string
            verilirse obje anahattı olmayacak şekilde ayarlanır.
        """
        try:
            self.itemconfig(obj, outline=outline_color.value)
        except tkinter.TclError:
            raise tkinter.TclError("You can't set the outline color on this object")

    def get_outline_color(self, obj):
        """
        Verilen grafiksel objenin anahat rengini almamıza yarar. Resim ve text objeleri gibi anahattı olmayan
        grafiksel objelerle kullanılamaz. thinker.TclError hatası verir.
        Args:
            obj: anahat rengini almak istediğimiz obje
        Returns:
            verilen objenin anahat rengi, string formatında. Eğer bu string boşsa, objenin anahattı yok demektir.
        """
        try:
            return self.COLORS(self.itemcget(obj, 'outline'))
        except tkinter.TclError:
            raise tkinter.TclError("You can't get the outline color of this object")

    def set_color(self, obj, color):
        """
        Verilen grafiksel objenin dolgu rengini ve anahat rengini değiştirir. Eğer obje dolgu veya anahatta sahip
        değilse, renk değiştirme işlemi göz ardı edilir.
        Args:
            obj: rengini değiştirmek istediğimiz obje
            color: dolgu ve anahattın olmasını istediğimiz rengin adı, string formatında. Eğer boş string verilirse,
            obje dolgusu ve anahattı olmayacak şekilde ayarlanır.
        """
        try:
            self.set_fill_color(obj, color)
        except tkinter.TclError:
            pass

        try:
            self.set_outline_color(obj, color)
        except tkinter.TclError:
            pass

    def set_outline_width(self, obj, width):
        """
        Verilen grafik objesinin anahattının kalınlığını değiştirir. Anahattı olmayan resim veya text 
        objeleriyle birlikte kullanılamaz.
        Args:
            obj: anahattının kalınlığını değiştirmek istediğimiz obje
            width: anahattın yeni genişliği
        """
        self.itemconfig(obj, width=width)

    def create_line(self, x1, y1, x2, y2, *args, **kwargs):
        """
        Canvas'ta verilen bir noktayla diğer bir nokta arasında çizgi grafiksel objesi yaratır ve döndürür. Çizgi siyah
        anahatla çizilir.
        Args:
            x1: çizginin başlangıç noktasının x koordinatı
            y1: çizginin başlangıç noktasının y koordinatı
            x2: çizginin bitiş noktasının x koordinatı
            y2: çizginin bitiş noktasının y koordinatı
            args: opsiyonel olarak çizgideki veya şekildeki herhangi bir noktanın koordinatlarını belirtebilirsiniz.
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen iki nokta arasında çizilmiş grafiksel çizgi objesi
        """
        return super(Canvas, self).create_line(x1, y1, x2, y2, *args, **kwargs)

    def create_rectangle(self, x1, y1, x2, y2, *args, **kwargs):
        """
        Canvas'ta sol üst köşesi verilen birinci koordinatta ve sağ alt köşesi verilen ikinci koordinatta olan 
        bir dikdörtgen grafiksel objesi yaratır ve döndürür. Rectangle doldurulmamış bir şekilde siyah anahatla çizilir.
        Args:
            x1: dikdörtgenin sol üst köşesinin x koordinatı
            y1: dikdörtgenin sol üst köşesinin y koordinatı
            x2: dikdörtgenin sağ alt köşesinin x koordinatı
            y2: dikdörtgenin sol alt köşesinin y koordinatı
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen pozisyona çizilmiş grafiksel dikdörtgen objesi.
        """
        return super(Canvas, self).create_rectangle(x1, y1, x2, y2, **kwargs)

    def create_oval(self, x1, y1, x2, y2, **kwargs):
        """
        Canvas'ta sol üst köşesi verilen ilk koordinatta, sağ alt köşesi de verilen ikinci koordinatta yer alan 
        sınırlayıcı kutu içerisine sığan en büyük oval grafik objesini yaratır ve döndürür. Oval canvasa içi boş bir şekilde
        siyah bir anahatla çizdirilir.
        Args:
            x1: sınırlayıcı kutunun sol üst köşesinin x koordinatı 
            y1: sınırlayıcı kutunun sol üst köşesinin y koordinatı
            x2: sınırlayıcı kutunun sağ alt köşesinin x koordinatı
            y2: sınırlayıcı kutunun sağ alt köşesinin y koordinatı
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen pozisyona çizilmiş grafiksel oval objesi
        """
        return super(Canvas, self).create_oval(x1, y1, x2, y2, **kwargs)

    def create_text(self, x, y, text, **kwargs):
        """
        Verilen text ile canvas'ta verilen pozisyonda bir text objesi yaratır ve döndürür. Belirtilen x ve y koordinatlarına
        textin merkezini yerleştirir. Text 13 punto boyutunda yaratılır.
        Args:
            x: textin merkezinin olmasını istediğimiz yerin x koordinatı 
            y: textin merkezinin olmasını istediğimiz yerin y koordinatı
            text: canvas'ta verilen pozisyonda gösterilmesi gereken text
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen texti verilen pozisyonda gösteren grafiksel text objesi.
        """
        return super().create_text(x, y, text=text, **kwargs)

    def set_text(self, obj, text):
        """
        Verilen text objesine ait texti değiştirmemize yarar. Text objesi olmayan grafiksel objelerle kullanılamaz.
        Args:
            obj: textini değiştirmek istediğimiz text objesi
            text: grafiksel objenin göstermesini istediğimiz yeni text 
        """
        self.itemconfig(obj, text=text)

    def get_text(self, obj):
        """
        Verilen text objesine ait texti almamızı sağlar. Text objesi olmayan grafiksel objelerle kullanılamaz.
        Args:
            obj: textini almak istediğimiz text objesi
        Returns:
            grafiksel obje üzerinde şu an gösterilmekte olan text
        """
        return self.itemcget(obj, 'text')

    def set_font(self, obj, font, size):
        """
        Verilen text objesi tarafından gösterilen textin yazı stilini ve boyutunu belirler. Text objesi olmayan
        grafiksel objelerle kullanılamaz.
        Args:
            obj: yazı stilini ve boyutunu belirlemek istediğimiz text objesi
            font: yazı stilinin adı, string
            size: yazının boyutu
        """
        self.itemconfig(obj, font=(font, size))

    def raise_to_front(self, obj):
        """
        Verilen objeyi canvas'taki diğer tüm objelerin önüne koyar.
        Args:
            obj: canvas'taki tüm objelerin önüne konulacak obje
        """
        self.raise_in_front_of(obj, 'all')

    def raise_in_front_of(self, obj, above):
        """
        İlk objeyi canvas'ta z ekseninde ikinci objenin önüne yerleştirir. Diğer bir
        deyişle, ilk obje direkt olarak ikinci objenin ve ikinci objenin arkasındaki tüm objelerin önünde görünürken,
        ikinci objenin önünde olan tüm objelerin arkasında görünür. 
        Args:
            obj: ikinci objenin önüne konulacak obje 
            above: ilk objenin önüne konulacağı obje 
        """
        self.tag_raise(obj, above)

    def lower_to_back(self, obj):
        """
        Verilen objeyi canvas'taki diğer tüm objelerin arkasına koyar.
        Args:
            obj: canvas'taki diğer tüm objelerin arkasına konulacak obje
        """
        self.lower_behind(obj, 'all')

    def lower_behind(self, obj, behind):
        """
        İlk objeyi canvas'ta z ekseninde ikinci objenin arkasına yerleştirir. Diğer bir
        deyişle, ilk obje direkt olarak ikinci objenin ve ikinci objenin önündeki tüm objelerin arkasında görünürken,
        ikinci objenin arkasında olan objelerin önünde görünür. 
        Args:
            obj: ikinci objenin önüne konulacak obje
            behind: ilk obje direkt arkasına konulacak olan obje
        """
        self.tag_lower(obj, behind)

    def create_image(self, x, y, file_path, **kwargs):
        """
        Belirtilen dosyadan, canvas'ta belirtilen pozisyonda bir resim yaratır. Resmin boyutu yüklenen resim
        dosyası ile aynı olacaktır.
        Args:
            x: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun x koordinatı
            y: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun y koordinatı
            file_path: canvasa eklemek istediğiniz resim dosyasının yerini belirten path stringi
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen resmi belirtilen pozisyonda gösteren grafiksel resim objesi.
        """
        return self.__create_image_with_optional_size(x, y, file_path, **kwargs)

    def create_image_with_size(self, x, y, width, height, file_path, **kwargs):
        """
        Belirtilen dosyayı kullanarak, canvas'ta verilen pozisyonda  verilen genişlik ve uzunlukta bir resim yaratır.
        Args:
            x: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun x koordinatı
            y: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun y koordinatı
            file_path: canvasa eklemek istediğiniz resim dosyasının yerini belirten path stringi
            width: resmin olmasını istediğiniz genişliği
            height: resmin olmasını istediğiniz uzunluğu
            kwargs: diğer thinkter keyword argümanları
        Returns:
            verilen resmi belirtilen pozisyonda verilen boyutlarda gösteren grafiksel resim objesi.
        """
        return self.__create_image_with_optional_size(x, y, file_path, width=width, height=height, **kwargs)

    def __create_image_with_optional_size(self, x, y, file_path, width=None, height=None, **kwargs):
        """
        Belirtilen dosyadan canvas üzerinde belirtilen pozisyonda bir resim yaratır. Opsiyonel olarak,
        resmi boyutlandırmak istediğiniz genişlik ve uzunluğu da belirtebilirsiniz.
        Args:
            x: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun x koordinatı
            y: canvas üzerinde resmin sol köşesini yerleştirmek istediğiniz pozisyonun y koordinatı
            file_path: canvasa eklemek istediğiniz resim dosyasının yerini belirten path stringi
            width: resmin olmasını istediğiniz genişliği (opsiyonel). Eğer belirtilmemişse resmin orijinal genişliği kullanılır.
            height: resmin olmasını istediğiniz uzunluğu (opsiyonel). Eğer belirtilmemişse resmin orijinal uzunluğu kullanılır.
            kwargs: diğer thinkter keyword argümanları
        Returns:
            belirtilen pozisyonda belirtilen resmi gösteren graphiksel resim objesi
            the graphical image object that is displaying the specified image at the specified location.
        """
        from PIL import ImageTk
        from PIL import Image
        image = Image.open(file_path)

        # Resize the image if another width and height is specified
        if width is not None and height is not None:
            image = image.resize((width, height))

        image = ImageTk.PhotoImage(image)
        img_obj = super().create_image(x, y, anchor="nw", image=image, **kwargs)
        # note: if you don't do this, the image gets garbage collected!!!
        # this introduces a memory leak which can be fixed by overloading delete
        self._image_gb_protection[img_obj] = image
        return img_obj