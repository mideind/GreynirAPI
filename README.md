
<img src="static/logo.png" alt="Greynir" width="200" height="200" align="right" style="margin-left:20px; margin-bottom: 20px;">

# GreynirAPI

This web application provides a REST API for the [Greynir](https://github.com/mideind/Greynir) Icelandic natural language processing engine.

The API is implemented in Python 3.6+ using the [FastAPI](https://fastapi.tiangolo.com/) framework.

It runs via [uvicorn](https://www.uvicorn.org/) or any ASGI-compliant server.

## Setup

Create a Python virtual environment in the repository root (requires
Python 3.6 or later, either [PyPy](https://pypi.org/) or CPython).

```
$ virtualenv -p /path/to/python3 venv
```

Activate the virtual environment:

```
$ source venv/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Install ASGI-compliant server (`uvicorn` is recommended):

```
$ pip install uvicorn
```

## Running web application

After activating the virtual environment, run the following command from the repository root:

```
$ uvicorn main:app
```

or if in development mode:

```
$ uvicorn main:app --reload
```

Defaults to running on [localhost:8000](http://localhost:8000)

## Docker deployment

TBD

## API documentation

Visit `/docs` to view the auto-generated API documentation

## License

GreynirAPI is copyright © 2021 [Miðeind ehf.](https://mideind.is)

This software is licensed under the *MIT License*:

   *Permission is hereby granted, free of charge, to any person
   obtaining a copy of this software and associated documentation
   files (the "Software"), to deal in the Software without restriction,
   including without limitation the rights to use, copy, modify, merge,
   publish, distribute, sublicense, and/or sell copies of the Software,
   and to permit persons to whom the Software is furnished to do so,
   subject to the following conditions:*

   *The above copyright notice and this permission notice shall be
   included in all copies or substantial portions of the Software.*

   *THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
   EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.*

