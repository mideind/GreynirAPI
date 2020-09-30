# GreynirAPI

This web application provides a REST API for the Greynir NLP parser.

Implemented in Python 3.6+ using the [FastAPI](https://fastapi.tiangolo.com/) framework.

Runs via [uvicorn](https://www.uvicorn.org/) or any ASGI-compliant server.


## Setup

Create a Python virtual environment repo root (requires Python 3.6 or later, 
[PyPy](https://pypi.org/) or CPython).

```
$ virtualenv -p /path/to/python venv
```

Activate virtual environment:

```
$ source venv/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```

## Running web application

After activating the virtual environment, run the following command from the repo root:

```
$ uvicorn main:app
```

Defaults to running on `[localhost:8000](http://localhost:8000)`

## API documentation

Visit `/docs` to view the auto-generated API documentation

## License

GreynirAPI is Copyright (C) 2020 [Miðeind ehf.](https://mideind.is)

This set of programs is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any later
version.

This set of programs is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

The full text of the GNU General Public License v3 is
[included here](https://github.com/mideind/Greynir/blob/master/LICENSE.txt)
and also available here: 
[https://www.gnu.org/licenses/gpl-3.0.html](https://www.gnu.org/licenses/gpl-3.0.html).

If you wish to use this set of programs in ways that are not covered under the
GNU GPLv3 license, please contact us at [mideind@mideind.is](mailto:mideind@mideind.is)
to negotiate a custom license. This applies for instance if you want to include or use
this software, in part or in full, in other software that is not licensed under
GNU GPLv3 or other compatible licenses.
