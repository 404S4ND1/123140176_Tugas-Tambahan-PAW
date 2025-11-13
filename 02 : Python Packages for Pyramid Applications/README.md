# Analisis Kode: Python Packages for Pyramid Applications

Kode ini merupakan lanjutan dari contoh sebelumnya (Single-File Web Application), namun kali ini aplikasi Pyramid dikemas dalam bentuk **Python package** agar lebih terstruktur dan mudah dikembangkan.

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
)
```

### tutorial/**init**.py

```python
# package
```

### tutorial/app.py

```python
from waitress import serve
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)
```

---

## 1. Struktur Proyek

Proyek ini terdiri dari dua bagian utama:

* **setup.py** → Mengatur metadata dan dependensi proyek.
* **tutorial/** → Direktori yang berfungsi sebagai package Python, berisi file `__init__.py` dan kode aplikasi `app.py`.

Struktur seperti ini memungkinkan aplikasi diinstal secara lokal menggunakan perintah:

```
pip install -e .
```

Perintah ini mengaktifkan *development mode* (editable mode), yang berarti setiap perubahan pada kode akan langsung terlihat tanpa perlu instal ulang.

---

## 2. File setup.py

File ini menggunakan **setuptools** untuk mendefinisikan proyek Python.

* `name='tutorial'` memberi nama pada package.
* `install_requires=requires` menyebutkan dependensi yang akan diinstal otomatis, yaitu `pyramid` dan `waitress`.
* Fungsinya mirip seperti manifest proyek yang menjelaskan bagaimana aplikasi dikemas.

---

## 3. File **init**.py

File kosong `__init__.py` menandakan bahwa direktori `tutorial` adalah **Python package**. Tanpa file ini, Python tidak akan mengenali folder tersebut sebagai package.

---

## 4. File app.py

Kode di `app.py` hampir sama dengan contoh pada single-file sebelumnya:

* Membuat route `/` menggunakan `config.add_route()`.
* Menghubungkannya ke fungsi view `hello_world()` melalui `config.add_view()`.
* Membuat objek aplikasi WSGI dengan `config.make_wsgi_app()`.
* Menjalankan server menggunakan `waitress.serve()`.

Perbedaan utamanya adalah sekarang file ini berada **di dalam package**, bukan di root project.

---

## 5. Analisis Teknis

1. Dengan adanya `setup.py`, proyek ini bisa diinstal dan digunakan di lingkungan Python manapun.
2. Struktur package membuat aplikasi lebih mudah di-*maintain* dan diperluas.
3. Pyramid tetap berjalan dengan prinsip WSGI dan MVC, tetapi sekarang memiliki fondasi proyek yang sesuai standar Python.
4. Menjalankan file `tutorial/app.py` secara langsung tidak umum dalam proyek Python sebenarnya, tetapi berguna dalam konteks pembelajaran untuk memahami urutan eksekusi.

---

## 6. Kesimpulan

* Pendekatan ini memperkenalkan konsep **packaging** dalam pengembangan aplikasi Pyramid.
* Dengan `setup.py`, aplikasi dapat diinstal, dijalankan, dan dikelola seperti proyek Python profesional.
* Secara kode, logika aplikasi tetap sama — hanya struktur dan cara instalasinya yang berubah menjadi lebih rapi dan modular.
