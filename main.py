#!/usr/bin/env python
"""

    GreynirAPI: Web application that exposes the Greynir API

    Copyright (C) 2021 Miðeind ehf.

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


    Main web application module

"""

from typing import List, Dict, Union, Optional

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from reynir import Greynir, NounPhrase, tokenize, TOK


__version__ = 0.1


app = FastAPI()
greynir: Greynir = None


def _err(msg: str) -> Dict[str, Union[str, bool]]:
    return {"err": True, "errmsg": msg}


@app.get("/", response_class=HTMLResponse)
def root():
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
NUMBERS = frozenset(("et", "ft"))


@app.get("/np")
def np(
    q: Optional[str] = None,
    case: Optional[str] = None,
    force_number: Optional[str] = None,
):
    """ Noun phrase declension API. """
    if not q:
        return _err("Missing query parameter")

    ckeys = CASES.keys()
    if case and case not in ckeys:
        return _err(f"Invalid case: '{case}'. Valid cases are: {', '.join(ckeys)}")

    if force_number and force_number not in NUMBERS:
        return _err(
            f"Invalid force_number param: '{force_number}'. Valid numbers are: {', '.join(NUMBERS)}"
        )

    resp: Dict[str, Union[str, bool, Dict[str, str]]] = dict(q=q)

    try:
        n = NounPhrase(q, force_number=force_number)

        cases: Dict[str, str] = dict()
        if case:
            cases[case] = getattr(n, CASES[case])
        else:
            # Default to returning all cases
            cases["nf"] = n.nominative
            cases["þf"] = n.accusative
            cases["þgf"] = n.dative
            cases["ef"] = n.genitive

        resp["cases"] = cases
        resp["err"] = False
    except Exception as e:
        return _err(f"Villa kom upp við fallbeygingu nafnliðs: '{e}'")

    return resp


_SKIP_TOKENS = frozenset((TOK.S_BEGIN, TOK.S_END, TOK.PUNCTUATION))
_MAX_LEM_TXT_LEN = 4096


@app.get("/lemmas")
def lemmas(q: Optional[str] = None, multiple: Optional[bool] = False):
    """ Lemmatization API. """
    if not q:
        return _err("Missing query parameter")
    if len(q) > _MAX_LEM_TXT_LEN:
        return _err(f"Param exceeds max length ({_MAX_LEM_TXT_LEN} chars)")
    print(multiple)


    # Lazy-load Greynir engine
    global greynir
    if not greynir:
        greynir = Greynir()

    resp: Dict[str, List] = dict(q=q)
    try:
        lem = list()
        for m in greynir.lemmatize(q, multiple=multiple):
            # TODO: postprocess in some way?
            lem.append(m)

        resp["err"] = False
        resp["lemmas"] = lem
    except Exception as e:
        return _err(f"Villa kom upp við lemmun texta: '{e}'");

    return resp
