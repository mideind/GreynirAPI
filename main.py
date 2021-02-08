#!/usr/bin/env python
"""

    GreynirAPI: Web application that exposes the Greynir API

    Copyright (C) 2021 Miðeind ehf.

    This software is licensed under the MIT License:

        Permission is hereby granted, free of charge, to any person
        obtaining a copy of this software and associated documentation
        files (the "Software"), to deal in the Software without restriction,
        including without limitation the rights to use, copy, modify, merge,
        publish, distribute, sublicense, and/or sell copies of the Software,
        and to permit persons to whom the Software is furnished to do so,
        subject to the following conditions:

        The above copyright notice and this permission notice shall be
        included in all copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
        EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
        MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
        CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
        TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
        SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    Main web application module

"""

from typing import Dict, List, Union, Optional, Any

from fastapi import FastAPI
from fastapi.responses import Response, JSONResponse, HTMLResponse

from reynir import Greynir, NounPhrase


__version__ = 0.1


app = FastAPI()
greynir: Optional[Greynir] = None


def _err(msg: str) -> JSONResponse:
    return JSONResponse(content={"err": True, "errmsg": msg})


@app.get("/", response_class=HTMLResponse)  # type: ignore
def root() -> str:
    return """
<html>
    <head><title>Greynir API Server v{0}</title></head>
    <body>
        <h1>Greynir API Server v{0}</h1>
        <ul><li><a href="/docs">Documentation</a></li></ul>
    </body>
</html>
""".format(
        __version__
    )


CASES = {"nf": "nominative", "þf": "accusative", "þgf": "dative", "ef": "genitive"}
SING_OR_PLUR = frozenset(("et", "ft", "singular", "plural"))


@app.get("/np")  # type: ignore
def np(
    q: str,
    case: Optional[str] = None,
    force_number: Optional[str] = None,
) -> Response:
    """ Noun phrase declension API """
    if not q:
        return _err("Missing query parameter")

    if case and case not in CASES.keys():
        return _err(f"Invalid case: '{case}'. Valid cases are: {', '.join(CASES.keys())}")

    if force_number and force_number not in SING_OR_PLUR:
        return _err(
            f"Invalid force_number parameter: '{force_number}'. Valid numbers are: {', '.join(SING_OR_PLUR)}"
        )

    resp: Dict[str, Union[str, bool, Dict[str, str]]] = dict(q=q)

    kwargs: Dict[str, Any] = dict()
    if force_number:
        kwargs["force_number"] = force_number

    try:
        n = NounPhrase(q, **kwargs)

        cases: Dict[str, str] = dict()
        if case:
            cases[case] = getattr(n, CASES[case])
        else:
            # Default to returning all cases
            c: Optional[str] = n.nominative
            if c is not None:
                cases["nf"] = c
            c = n.accusative
            if c is not None:
                cases["þf"] = c
            c = n.dative
            if c is not None:
                cases["þgf"] = c
            c = n.genitive
            if c is not None:
                cases["ef"] = c

        resp["cases"] = cases
        resp["err"] = False
    except Exception as _:
        raise
        #return _err(f"Villa kom upp við fallbeygingu nafnliðar: '{e}'")

    return JSONResponse(content=resp)


_MAX_LEMMAS_TXT_LEN = 8192


@app.get("/lemmas")  # type: ignore
def lemmas(q: str, all_lemmas: bool = False) -> Response:
    """ Lemmatization API. """
    if not q:
        return _err("Missing query parameter")
    if len(q) > _MAX_LEMMAS_TXT_LEN:
        return _err(f"Param exceeds max length ({_MAX_LEMMAS_TXT_LEN} chars)")

    # Lazy-load Greynir engine
    global greynir
    if greynir is None:
        greynir = Greynir()

    resp: Dict[str, Any] = dict(q=q)
    try:
        lem: List[Any] = []
        for m in greynir.lemmatize(q, all_lemmas=all_lemmas):
            # TODO: postprocess in some way?
            lem.append(m)
        resp["err"] = False
        resp["lemmas"] = lem
    except Exception as e:
        return _err(f"Villa kom upp við lemmun texta: '{e}'");

    return JSONResponse(content=resp)
