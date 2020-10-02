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

from typing import Optional

from fastapi import FastAPI

from reynir import NounPhrase
from reynir import tokenize, TOK

__version__ = 0.1


app = FastAPI()


def _err(msg):
    return {"err": True, "errmsg": msg}


# @app.get("/")
# def root():
#     return "Welcome to the Greynir API server."


CASES = {"nf": "nominative", "þf": "accusative", "þgf": "dative", "ef": "genitive"}
NUMBERS = frozenset(("et", "ft"))


@app.get("/np")
def np(q: str = None, case: Optional[str] = None, force_number: Optional[str] = None):
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

    resp = {}
    try:
        resp["q"] = q

        n = NounPhrase(q, force_number=force_number)

        cases = dict()
        if case:
            cases[case] = getattr(n, CASES[case])
        else:
            # Default to returning all cases
            cases["nf"] = n.nominative
            cases["þf"] = n.accusative
            cases["þgf"] = n.dative
            cases["ef"] = n.genitive

        resp["cases"] = cases
    except Exception:
        raise

    resp["err"] = False

    return resp


_SKIP_TOKENS = frozenset((TOK.S_BEGIN, TOK.S_END, TOK.PUNCTUATION))
_MAX_LEM_TXT_LEN = 4096


@app.get("/lemmas")
def lemmas(q: str = None):
    """ Lemmatization API. """
    if not q:
        return _err("Missing query parameter")
    if len(q) > _MAX_LEM_TXT_LEN:
        return _err("Param exceeds max length ({_MAX_LEM_TXT_LEN} chars)")

    lem = list()

    # Consume from generator
    for t in tokenize(q):
        if t.kind in _SKIP_TOKENS:
            continue
        if not t.val:
            lem.append(t.txt)
        else:
            m = t.val[0]
            if hasattr(m, "kind"):
                lem.append(m.kind.replace("-", ""))
            elif hasattr(m, "name"):
                lem.append(m.name)
            else:
                lem.append(t.txt)

    resp = dict()
    resp["err"] = False
    resp["q"] = q
    resp["lemmas"] = lem

    return resp
