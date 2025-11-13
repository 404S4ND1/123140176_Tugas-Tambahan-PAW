# Analisis Kode: Application Configuration with .ini Files (Pyramid)

Kode ini melanjutkan pengembangan aplikasi Pyramid sebelumnya dengan menambahkan **konfigurasi berbasis file `.ini`** dan menjalankan aplikasi menggunakan perintah **`pserve`** bawaan Pyramid.

Berikut potongan kode utama yang dianalisis:

### setup.py

```python
from setuptools import setup

requires = [
    'pyramid',
    'waitress',
]

setup(
    name='tutorial',
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = tutorial:main'
        ],
    },
)
```

### development.ini

```ini
[app:main]
use = egg:tutorial

[server:main]
use = egg:waitress#main
listen = localhost:6543
```

### tutorial/**init**.py

```python
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('<body><h1>Hello World!</h1></body>')


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    return config.make_wsgi_app()
```

---

## 1. Entry Point pada setup.py

Bagian penting dari file `setup.py` adalah konfigurasi **entry point**:

```python
entry_points={
    'paste.app_factory': [
        'main = tutorial:main'
    ],
},
```

Bagian ini memberi tahu Pyramid (melalui *PasteDeploy*) di mana fungsi utama aplikasi berada — dalam hal ini `main()` di modul `tutorial`.

Ketika `pserve` dijalankan, ia membaca `development.ini`, menemukan `use = egg:tutorial`, lalu mencari entry point `tutorial:main` dari `setup.py`. Dari situ, fungsi `main()` akan dieksekusi untuk membangun aplikasi WSGI.

---

## 2. File development.ini

File `.ini` berfungsi sebagai **file konfigurasi** aplikasi.

* `[app:main]` menunjuk ke aplikasi utama yang didefinisikan dalam entry point `tutorial:main`.
* `[server:main]` menentukan server yang digunakan (`waitress`) dan alamatnya (`localhost:6543`).

Dengan pendekatan ini, pengaturan aplikasi (seperti port, logging, dll.) tidak perlu ditulis di kode Python — semuanya bisa dikelola dari file konfigurasi.

---

## 3. File **init**.py

Fungsi `main()` pada `__init__.py` menggantikan peran `app.py` dari langkah sebelumnya. Ia bertugas membuat objek WSGI aplikasi berdasarkan pengaturan dari `.ini`.

* `global_config` berisi konfigurasi global dari file `.ini`.
* `**settings` menangkap pasangan *key-value* dari konfigurasi aplikasi.
* `config = Configurator(settings=settings)` membuat objek konfigurasi Pyramid.
* Route dan view ditambahkan seperti sebelumnya, lalu aplikasi dikembalikan dengan `make_wsgi_app()`.

---

## 4. Proses Eksekusi Aplikasi

Urutan kerja Pyramid dengan konfigurasi `.ini` adalah:

1. Perintah `pserve development.ini --reload` dijalankan.
2. `pserve` membaca bagian `[app:main]` dari `development.ini`.
3. `use = egg:tutorial` mengarah ke entry point di `setup.py`.
4. Fungsi `main()` pada `tutorial/__init__.py` dipanggil untuk membuat WSGI app.
5. Server `waitress` dijalankan sesuai pengaturan `[server:main]`.

Opsi `--reload` membuat Pyramid otomatis me-*reload* aplikasi setiap kali ada perubahan pada kode atau file `.ini` — sangat berguna saat pengembangan.

---

## 5. Analisis Teknis

* Dengan pendekatan `.ini`, Pyramid memisahkan **konfigurasi dari kode** untuk fleksibilitas dan kemudahan pengelolaan.
* Entry point `paste.app_factory` memanfaatkan fitur dari **Setuptools** dan **PasteDeploy**.
* `development.ini` dapat diperluas untuk menambahkan pengaturan logging, database, atau middleware lain.
* Struktur ini membuat aplikasi Pyramid lebih mudah di-deploy dan diatur di berbagai lingkungan (development, staging, production).

---

## 6. Kesimpulan

* Pyramid dapat dijalankan menggunakan konfigurasi `.ini` melalui `pserve` untuk pengelolaan aplikasi yang lebih terstruktur.
* Entry point di `setup.py` menghubungkan aplikasi dengan konfigurasi `.ini`.
* File `__init__.py` kini menjadi pusat inisialisasi aplikasi.
* Pendekatan ini memisahkan logika aplikasi dari konfigurasi server dan pengaturan, membuatnya lebih profesional dan mudah dikelola.
