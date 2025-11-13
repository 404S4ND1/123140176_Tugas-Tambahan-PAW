# Analisis Kode: Basic Web Handling With Views (Pyramid)

## Struktur Kode dan Tujuan

Pada bagian ini, kode difokuskan untuk memisahkan logika **view** dari kode utama aplikasi Pyramid. Pendekatan ini meningkatkan keteraturan dan skalabilitas aplikasi web. Selain itu, penggunaan **decorator `@view_config`** memungkinkan konfigurasi deklaratif yang lebih ringkas dibanding konfigurasi imperatif.

---

## 1. `__init__.py`

```python
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.scan('.views')
    return config.make_wsgi_app()
```

### Analisis:

* `Configurator` digunakan untuk mengatur routing dan inisialisasi aplikasi WSGI.
* `config.add_route` mendefinisikan dua rute: `'home'` dan `'hello'`.
* `config.scan('.views')` mencari dekorator `@view_config` di file `views.py`. Titik (`.`) menunjukkan direktori modul saat ini.
* Pemisahan ini menjadikan file `__init__.py` lebih ringkas, hanya fokus pada setup konfigurasi.

---

## 2. `views.py`

```python
from pyramid.response import Response
from pyramid.view import view_config

@view_config(route_name='home')
def home(request):
    return Response('<body>Visit <a href="/howdy">hello</a></body>')

@view_config(route_name='hello')
def hello(request):
    return Response('<body>Go back <a href="/">home</a></body>')
```

### Analisis:

* Setiap fungsi view dihubungkan ke route tertentu melalui `@view_config(route_name=...)`.
* Fungsi `home()` merespons ke route `'/'` dan memberikan link menuju `/howdy`.
* Fungsi `hello()` merespons ke route `'/howdy'` dan menampilkan link kembali ke halaman utama.
* Pendekatan decorator ini menggantikan cara lama `config.add_view`, membuat kode lebih bersih dan mudah dipindahkan.

---

## 3. `tests.py`

```python
import unittest
from pyramid import testing

class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_home(self):
        from .views import home
        request = testing.DummyRequest()
        response = home(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Visit', response.body)

    def test_hello(self):
        from .views import hello
        request = testing.DummyRequest()
        response = hello(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Go back', response.body)

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<body>Visit', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<body>Go back', res.body)
```

### Analisis:

* Terdapat dua kelas pengujian:

  1. **`TutorialViewTests`** – menguji fungsi view secara langsung menggunakan `DummyRequest()` tanpa menjalankan aplikasi.
  2. **`TutorialFunctionalTests`** – menguji perilaku aplikasi secara penuh menggunakan `WebTest`.
* `assertIn()` digunakan untuk memastikan teks tertentu ada dalam response body, tanpa harus mencocokkan seluruh isi.
* Kedua pendekatan ini (unit dan functional testing) memastikan integritas logika view sekaligus alur HTTP.

---

## Kesimpulan

Kode ini memperkenalkan **pemisahan view dari konfigurasi utama**, serta memperlihatkan **penggunaan decorator `@view_config`** untuk pendekatan deklaratif. Dengan dua view (`home` dan `hello`), pengujian yang komprehensif memastikan bahwa routing, tampilan, dan interaksi antar halaman berjalan sesuai harapan.
