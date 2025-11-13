# 08: HTML Generation With Templating — Code Analysis

## Overview

This section introduces **templating** in Pyramid using **pyramid_chameleon**, allowing developers to separate HTML from Python code. Instead of embedding HTML directly into view functions, the code now returns data that templates use for rendering.

---

## Key Code Sections

### **1. setup.py**

```python
requires = [
    'pyramid',
    'pyramid_chameleon',
    'waitress',
]

dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'webtest',
]

setup(
    name='tutorial',
    install_requires=requires,
    extras_require={'dev': dev_requires},
    entry_points={'paste.app_factory': ['main = tutorial:main']},
)
```

**Analysis:**

* Adds **pyramid_chameleon** to enable `.pt` template rendering.
* The `[dev]` extras include testing tools (`pytest`, `webtest`).

---

### **2. tutorial/**init**.py**

```python
from pyramid.config import Configurator

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('home', '/')
    config.add_route('hello', '/howdy')
    config.scan('.views')
    return config.make_wsgi_app()
```

**Analysis:**

* `config.include('pyramid_chameleon')` activates Chameleon integration.
* Routes (`home`, `hello`) are mapped to their respective views.
* `config.scan('.views')` automatically detects `@view_config` decorators.

---

### **3. tutorial/views.py**

```python
from pyramid.view import view_config

@view_config(route_name='home', renderer='home.pt')
def home(request):
    return {'name': 'Home View'}

@view_config(route_name='hello', renderer='home.pt')
def hello(request):
    return {'name': 'Hello View'}
```

**Analysis:**

* Each view returns a **dictionary** of data rather than HTML.
* The `renderer` parameter links the view to `home.pt`.
* Both routes share one template but return different data values.

---

### **4. Template: home.pt**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Quick Tutorial: ${name}</title>
</head>
<body>
<h1>Hi ${name}</h1>
</body>
</html>
```

**Analysis:**

* Uses **Chameleon syntax** `${variable}` for dynamic data injection.
* `name` comes from the dictionary returned by each view.

---

### **5. development.ini**

```ini
pyramid.reload_templates = true
pyramid.includes =
    pyramid_debugtoolbar
```

**Analysis:**

* Enables **auto-reload** for templates during development.
* Includes the **debug toolbar** for easier inspection.

---

### **6. tutorial/tests.py**

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
        self.assertEqual('Home View', response['name'])

    def test_hello(self):
        from .views import hello
        request = testing.DummyRequest()
        response = hello(request)
        self.assertEqual('Hello View', response['name'])

class TutorialFunctionalTests(unittest.TestCase):
    def setUp(self):
        from tutorial import main
        from webtest import TestApp
        app = main({})
        self.testapp = TestApp(app)

    def test_home(self):
        res = self.testapp.get('/', status=200)
        self.assertIn(b'<h1>Hi Home View', res.body)

    def test_hello(self):
        res = self.testapp.get('/howdy', status=200)
        self.assertIn(b'<h1>Hi Hello View', res.body)
```

**Analysis:**

* **Unit tests** validate data returned by each view.
* **Functional tests** verify rendered HTML output via `webtest`.
* This approach cleanly separates logic (Python) and presentation (HTML).

---

## Summary

* **Before:** HTML was embedded in the Python views.
* **After:** HTML moved to external `.pt` templates managed by Chameleon.
* **Benefits:**

  * Easier maintenance and readability.
  * Views return structured data.
  * Templates handle presentation.
  * Testing focuses on logic rather than layout.

---

✅ *This step successfully integrates templating with Pyramid, improving code organization and scalability.*
