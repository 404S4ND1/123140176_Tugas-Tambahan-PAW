# Handling Web Requests and Responses

## Ringkasan Kode

Pada tahap ini, aplikasi Pyramid difokuskan untuk menangani *request* dan *response* dengan bantuan library **WebOb**, yang sudah terintegrasi di Pyramid.

### File: `tutorial/__init__.py`

```python
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('plain', '/plain')
    config.scan('.views')
    return config.make_wsgi_app()
```

📌 **Penjelasan:**

* Dua *route* ditambahkan: `/` dan `/plain`.
* `config.scan('.views')` digunakan untuk memindai dekorator `@view_config` di modul views.

---

### File: `tutorial/views.py`

```python
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home')
    def home(self):
        return HTTPFound(location='/plain')

    @view_config(route_name='plain')
    def plain(self):
        name = self.request.params.get('name', 'No Name Provided')
        body = 'URL %s with name: %s' % (self.request.url, name)
        return Response(content_type='text/plain', body=body)
```

📌 **Penjelasan:**

* `home()` mengarahkan pengguna ke `/plain` dengan *redirect* menggunakan `HTTPFound`.
* `plain()` mengambil parameter `name` dari query string, lalu mengembalikan teks sebagai respons.
* `Response` mengatur *content-type* menjadi `text/plain` dan mengirimkan hasil.

---

### File: `tutorial/tests.py`

```python
import unittest
from pyramid import testing

class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import TutorialViews
        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.home()
        self.assertEqual(response.status, '302 Found')

    def test_plain_without_name(self):
        from .views import TutorialViews
        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.plain()
        self.assertIn(b'No Name Provided', response.body)

    def test_plain_with_name(self):
        from .views import TutorialViews
        request = testing.DummyRequest()
        request.GET['name'] = 'Jane Doe'
        inst = TutorialViews(request)
        response = inst.plain()
        self.assertIn(b'Jane Doe', response.body)

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_plain_without_name(self):
        res = self.testapp.get('/plain', status=200)
        self.assertIn(b'No Name Provided', res.body)

    def test_plain_with_name(self):
        res = self.testapp.get('/plain?name=Jane%20Doe', status=200)
        self.assertIn(b'Jane Doe', res.body)
```

📌 **Penjelasan:**

* Unit test memastikan bahwa `home()` benar melakukan *redirect (302)*.
* Fungsi `plain()` diuji untuk dua kasus: tanpa parameter dan dengan parameter `name`.
* Functional test menggunakan **WebTest** untuk mensimulasikan request HTTP sebenarnya.

---

## Analisis Teknis

* **`HTTPFound`**: menghasilkan HTTP 302 Redirect. Dapat dikembalikan langsung atau dilempar dengan `raise` untuk efek serupa.
* **`request.params`**: menggabungkan `GET` dan `POST` parameters menjadi satu dictionary.
* **`Response`**: objek respons yang dikirim ke browser, dapat dikustomisasi pada header, body, dan content type.

### Contoh Alur Aplikasi

1. Akses `/` → diarahkan otomatis ke `/plain`.
2. Akses `/plain` tanpa parameter → teks menampilkan `No Name Provided`.
3. Akses `/plain?name=alice` → teks menampilkan `URL ... with name: alice`.

---

## Insight Tambahan

* `HTTPFound` bisa **dikembalikan** atau **dilempar**. Perbedaannya hanya pada gaya pemrograman, hasil akhirnya sama.
* Library **WebOb** menjadi dasar `request` dan `response` di Pyramid, memastikan kompatibilitas dengan framework Python lain seperti Flask atau Django.

---

✅ **Hasil Pengujian:**

```
$ pytest tutorial/tests.py -q
.....
5 passed in 0.30 seconds
```

---

### Kesimpulan

Modul ini memperkenalkan konsep dasar *HTTP request/response handling* dalam Pyramid, termasuk cara melakukan redirect, membaca parameter query, dan menghasilkan respon teks mentah. Pendekatan ini memudahkan pengelolaan data dari URL dan kontrol penuh terhadap respons web.
