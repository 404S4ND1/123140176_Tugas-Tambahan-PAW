# Pyramid Tutorial — Organizing Views With View Classes

## 📘 Analisis Kode

Bagian ini menjelaskan bagaimana kita mengorganisasi *view* dalam bentuk kelas agar kode lebih terstruktur dan efisien.

---

### 1. Struktur Kode Utama (`tutorial/views.py`)

```python
from pyramid.view import (
    view_config,
    view_defaults
    )

@view_defaults(renderer='home.pt')
class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home')
    def home(self):
        return {'name': 'Home View'}

    @view_config(route_name='hello')
    def hello(self):
        return {'name': 'Hello View'}
```

#### 🔍 Penjelasan

* `@view_defaults(renderer='home.pt')` → menentukan konfigurasi umum untuk semua *view method* dalam kelas ini, sehingga tidak perlu mendefinisikan renderer berulang.
* `TutorialViews` → kelas yang menampung dua *view* (`home` dan `hello`).
* `__init__` → menerima `request` agar dapat digunakan oleh seluruh metode.
* `@view_config(route_name='...')` → mendaftarkan setiap metode sebagai *view* dengan rute masing-masing.

Pendekatan ini membuat kode lebih mudah diperluas dan memungkinkan penggunaan state atau fungsi bantu yang sama di beberapa *view*.

---

### 2. Pengujian Unit (`tutorial/tests.py`)

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
        self.assertEqual('Home View', response['name'])

    def test_hello(self):
        from .views import TutorialViews

        request = testing.DummyRequest()
        inst = TutorialViews(request)
        response = inst.hello()
        self.assertEqual('Hello View', response['name'])
```

#### 💡 Penjelasan

* Pengujian diperbarui agar sesuai dengan perubahan ke *class-based views*.
* Sebelum memanggil *view method*, kita harus membuat instance kelas (`inst = TutorialViews(request)`).
* Setiap metode dites secara terpisah dengan `DummyRequest` agar tetap ringan dan cepat.

---

### 3. Pengujian Fungsional

```python
class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hi Home View', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<h1>Hi Hello View', res.body)
```

#### 🧪 Penjelasan

* `TestApp` dari *webtest* digunakan untuk melakukan simulasi permintaan HTTP tanpa server sungguhan.
* Memastikan HTML yang dikembalikan oleh template berisi teks yang diharapkan.

---

### 4. Inti Konsep

| Aspek       | Sebelum (Function View)       | Sesudah (Class View)                    |
| ----------- | ----------------------------- | --------------------------------------- |
| Struktur    | Setiap *view* berdiri sendiri | *View* dikelompokkan dalam satu kelas   |
| Reusability | Konfigurasi diulang           | Bisa dipusatkan dengan `@view_defaults` |
| Testing     | Langsung panggil fungsi       | Harus buat instance kelas dulu          |

---

### 🧭 Kesimpulan

Migrasi dari *function-based views* ke *class-based views* membantu:

* Menyatukan *view* yang terkait dalam satu struktur.
* Mengurangi pengulangan konfigurasi.
* Menyiapkan dasar untuk *stateful views* atau *RESTful controllers*.

---

**Referensi:** [Defining a View Callable as a Class — Pyramid Docs](https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/views.html#view-classes)
