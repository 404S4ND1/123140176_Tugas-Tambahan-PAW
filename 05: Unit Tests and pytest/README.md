# Unit Tests and pytest — README

## Deskripsi

Pada tahap ini, kita menambahkan **unit testing** menggunakan **pytest** untuk memastikan fungsi aplikasi Pyramid berjalan dengan benar. Pendekatan ini membantu mendeteksi error lebih awal tanpa perlu selalu membuka browser untuk menguji secara manual.

---

## Struktur Proyek

```
unit_testing/
│
├── setup.py
├── development.ini
└── tutorial/
    ├── __init__.py
    └── tests.py
```

---

## setup.py

Tambahkan `pytest` ke dalam daftar dependensi pengembangan (`dev_requires`) agar dapat dijalankan saat testing.

```python
from setuptools import setup

requires = [
    'pyramid',
    'waitress',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
]

setup(
    name='tutorial',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'main = tutorial:main'
        ],
    },
)
```

### Instalasi Dependensi

Jalankan perintah berikut untuk menginstal proyek beserta dependensi pengembangannya:

```bash
$VENV/bin/pip install -e ".[dev]"
```

---

## tests.py

Buat file `tutorial/tests.py` untuk menulis unit test sederhana terhadap fungsi `hello_world`:

```python
import unittest
from pyramid import testing


class TutorialViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_hello_world(self):
        from tutorial import hello_world

        request = testing.DummyRequest()
        response = hello_world(request)
        self.assertEqual(response.status_code, 200)
```

### Menjalankan Test

Gunakan perintah berikut untuk menjalankan semua unit test:

```bash
$VENV/bin/pytest tutorial/tests.py -q
```

Hasil yang diharapkan:

```
.
1 passed in 0.14 seconds
```

---

## Analisis

* **Tujuan**: Memastikan fungsi view `hello_world` mengembalikan status HTTP yang benar (200 OK).
* **`testing.setUp()` dan `tearDown()`**: Menyediakan lingkungan konfigurasi Pyramid untuk setiap test case.
* **Isolasi test**: Fungsi `hello_world` diimpor di dalam metode test, bukan di awal file, agar efek samping dari import tidak mengganggu test lain.

### Kenapa Menggunakan pytest?

* Lebih ringkas dan cepat dibanding `unittest` bawaan Python.
* Menyediakan laporan error yang lebih informatif.
* Mudah diperluas dengan plugin seperti `pytest-cov` untuk coverage testing.

---

## Kesimpulan

Langkah ini memperkenalkan dasar pengujian unit menggunakan **pytest** dalam proyek Pyramid. Dengan pengujian otomatis, kamu bisa memeriksa fungsi view tanpa menjalankan aplikasi secara manual, meningkatkan efisiensi dan keandalan kode.

---

**Next Step:** Lanjutkan ke bab berikutnya — *Functional Testing with WebTest* untuk menguji alur aplikasi secara menyeluruh.

