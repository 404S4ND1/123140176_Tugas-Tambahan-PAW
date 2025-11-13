# Functional Testing with WebTest — README.md

## Analisis Kode

Kode pada langkah ini memperkenalkan **pengujian fungsional (functional testing)** menggunakan pustaka **WebTest**. Tujuan utamanya adalah melakukan pengujian menyeluruh terhadap aplikasi Pyramid, bukan hanya bagian tertentu seperti pada unit test.

---

### 1. **Penambahan Dependensi WebTest**

```python
requires = [
    'pyramid',
    'waitress',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]
```

Bagian ini menambahkan **webtest** ke dalam daftar `dev_requires`. Artinya, library ini hanya digunakan saat pengembangan dan pengujian, bukan pada deployment produksi.

Perintah instalasi:

```bash
$VENV/bin/pip install -e ".[dev]"
```

Perintah tersebut menginstal semua dependensi utama dan tambahan yang dibutuhkan untuk testing.

---

### 2. **Unit Test (Pengujian Komponen Terisolasi)**

```python
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

Bagian ini masih sama seperti tahap sebelumnya, berfungsi untuk menguji **fungsi view** secara langsung tanpa melibatkan server HTTP. `DummyRequest()` digunakan untuk mensimulasikan permintaan HTTP tanpa benar-benar menjalankan aplikasi.

---

### 3. **Functional Test (Pengujian End-to-End)**

```python
class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        app = main({})
        from webtest import TestApp

        self.testapp = TestApp(app)

    def test_hello_world(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hello World!</h1>', res.body)
```

Di sini dilakukan pengujian penuh terhadap aplikasi Pyramid:

* `main({})` memanggil fungsi utama aplikasi yang mengembalikan objek WSGI.
* `TestApp(app)` membuat objek pengujian dari WebTest untuk mensimulasikan permintaan HTTP nyata.
* `get('/', status=200)` menguji endpoint root `/` dan memeriksa apakah status kode HTTP yang dikembalikan adalah **200 (OK)**.
* `assertIn(b'<h1>Hello World!</h1>', res.body)` memastikan bahwa HTML yang dikembalikan mengandung teks **Hello World!**. Huruf **b** menandakan bahwa isi respons dibaca dalam format **byte string**, bukan teks biasa.

---

### 4. **Menjalankan Pengujian**

```bash
$VENV/bin/pytest tutorial/tests.py -q
..
2 passed in 0.25 seconds
```

Tanda `..` berarti dua pengujian berhasil dijalankan dan lulus. Ini menunjukkan bahwa baik pengujian unit maupun pengujian fungsional berjalan dengan benar.

---

### 5. **Kesimpulan**

Dengan menambahkan WebTest, kini pengujian mencakup seluruh lapisan aplikasi dari request hingga response tanpa harus menjalankan server HTTP sungguhan. Hal ini membuat proses pengujian lebih cepat dan efisien, serta meningkatkan jaminan bahwa aplikasi berfungsi sesuai harapan.

**Perbedaan utama:**

| Jenis Tes       | Fokus                                      | Kecepatan    | Cakupan  |
| --------------- | ------------------------------------------ | ------------ | -------- |
| Unit Test       | Menguji fungsi/view secara terpisah        | Sangat cepat | Terbatas |
| Functional Test | Menguji seluruh aplikasi secara end-to-end | Cepat        | Luas     |

---

### 6. **Catatan Tambahan**

* Huruf **b** di `b'<h1>Hello World!</h1>'` digunakan karena `res.body` mengembalikan data dalam format **byte**, bukan string.
* Pengujian fungsional ini bisa dikembangkan untuk menguji banyak route, status code, atau isi HTML lain yang dihasilkan aplikasi.
