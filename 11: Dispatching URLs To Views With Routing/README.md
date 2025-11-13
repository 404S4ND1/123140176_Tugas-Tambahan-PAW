# Dispatching URLs to Views with Routing (Pyramid Tutorial Step 11)

Tutorial ini menjelaskan cara **memetakan URL ke view menggunakan routing** di framework Pyramid.  
Kita membuat route dengan parameter dinamis (`{first}` dan `{last}`) dan menampilkannya di template.

---

## 📁 Struktur Folder

```
routing/
├── tutorial/
│   ├── __init__.py
│   ├── views.py
│   ├── home.pt
│   └── tests.py
└── setup.py
```

---

## ⚙️ Konfigurasi Route (`__init__.py`)

```python
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/howdy/{first}/{last}')
    config.scan('.views')
    return config.make_wsgi_app()
```

Kode di atas membuat route `/howdy/{first}/{last}` yang mengekstrak bagian URL ke `request.matchdict`.

---

## 👀 View (`views.py`)

```python
from pyramid.view import view_config, view_defaults

@view_defaults(renderer='home.pt')
class TutorialViews:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='home')
    def home(self):
        first = self.request.matchdict['first']
        last = self.request.matchdict['last']
        return {
            'name': 'Home View',
            'first': first,
            'last': last
        }
```

View ini menerima data dari URL dan mengirimkannya ke template.

---

## 🥉 Template (`home.pt`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${name}</title>
</head>
<body>
<h1>${name}</h1>
<p>First: ${first}, Last: ${last}</p>
</body>
</html>
```

Template menggunakan Chameleon untuk menampilkan data dari view.

---

## 🥉 Testing (`tests.py`)

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
        request.matchdict['first'] = 'First'
        request.matchdict['last'] = 'Last'
        inst = TutorialViews(request)
        response = inst.home()
        self.assertEqual(response['first'], 'First')
        self.assertEqual(response['last'], 'Last')

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        from webtest import TestApp
        app = main({})
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/howdy/Jane/Doe', status=200)
        self.assertIn(b'Jane', res.body)
        self.assertIn(b'Doe', res.body)
```

---

## ▶️ Menjalankan Aplikasi

```bash
$VENV/bin/pserve development.ini --reload
```

Lalu buka di browser:
```
http://localhost:6543/howdy/amy/smith
```

---

## 📚 Penjelasan Singkat

- `config.add_route('home', '/howdy/{first}/{last}')`: menambahkan route dinamis.
- `request.matchdict`: berisi data hasil ekstraksi dari URL.
- Test unit dan functional memastikan route dan view berjalan sesuai harapan.

---

## ✅ Hasil Akhir

URL `/howdy/amy/smith` akan menampilkan halaman dengan teks:

```
First: amy, Last: smith
```

---

## 🔗 Referensi

- [Pyramid Web Framework](https://trypyramid.com/)
- [Tutorial Resmi di GitHub](https://github.com/Pylons/pyramid_tutorials)
