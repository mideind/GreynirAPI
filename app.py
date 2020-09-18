#!/usr/bin/env python
"""

    GreynirAPI: Web application that exposes the Greynir API

    Main web application module

    Copyright (C) 2020 Miðeind ehf.

       This program is free software: you can redistribute it and/or modify
       it under the terms of the GNU General Public License as published by
       the Free Software Foundation, either version 3 of the License, or
       (at your option) any later version.
       This program is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
       GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see http://www.gnu.org/licenses/.


"""

import json
from aiohttp import web

from reynir import NounPhrase

routes = web.RouteTableDef()


@routes.get("/np")
async def np(request):
    resp = {}
    try:
        pass
    except Exception:
        pass
    return web.Response(text=json.dumps(resp))


@routes.get("/lemmatize")
async def lemmatize(request):
    resp = {}
    try:
        pass
    except Exception:
        pass
    return web.Response(text=json.dumps(resp))


@routes.get("/")
async def hello(request):
    return web.Response(
        text="<html><center><h1>Greynir API Server</h1></center></html>",
        content_type="text/html",
    )


app = web.Application()
app.add_routes(routes)
web.run_app(app)
