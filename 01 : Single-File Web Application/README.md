# Analisis Kode: Single-File Web Application pada Pyramid

Kode ini merupakan contoh aplikasi web sederhana menggunakan framework **Pyramid** dalam satu file Python. Berikut penjelasan mengenai bagian-bagian penting dari kode tersebut:

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

### 1. Import Library

* `waitress` digunakan sebagai **web server** untuk menjalankan aplikasi.
* `Configurator` berfungsi untuk **mengatur routing dan view**.
* `Response` digunakan untuk membuat **objek respon HTTP** yang dikirim ke browser.

### 2. Fungsi View

```python
def hello_world(request):
    print('Incoming request')
    return Response('<body><h1>Hello World!</h1></body>')
```

Fungsi ini akan dijalankan setiap kali ada request ke URL `/`.

* `print('Incoming request')` menampilkan teks di terminal ketika ada request masuk.
* `Response()` mengembalikan halaman HTML sederhana berisi teks *Hello World!*.

### 3. Bagian Utama Program

```python
if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    serve(app, host='0.0.0.0', port=6543)
```

* `if __name__ == '__main__':` memastikan program hanya dijalankan langsung, bukan diimpor.
* `config.add_route('hello', '/')` membuat rute utama `/` untuk aplikasi.
* `config.add_view(hello_world, route_name='hello')` menghubungkan rute `/` dengan fungsi `hello_world`.
* `make_wsgi_app()` menghasilkan **aplikasi WSGI** siap dijalankan.
* `serve()` menjalankan server lokal di port **6543**.

### 4. Kesimpulan

Kode ini menunjukkan cara kerja dasar framework Pyramid:

* Mengatur rute dan view menggunakan `Configurator`.
* Mengembalikan respon ke client melalui `Response`.
* Menjalankan aplikasi dengan server `waitress`.
