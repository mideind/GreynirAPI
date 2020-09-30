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


__version__ = 0.1


app = FastAPI()


@app.get("/")
def root():
    return "Welcome to the Greynir API server."


CASES = {"nf": "nominative", "þf": "accusative", "þgf": "dative", "ef": "genitive"}
NUMBERS = frozenset(("et", "ft"))


@app.get("/np")
def np(q: str = None, case: Optional[str] = None, number: Optional[str] = None):
    if not q:
        return {"err": True, "errmsg": "Missing query parameter"}

    ckeys = CASES.keys()
    if case and case not in ckeys:
        return {
            "err": True,
            "errmsg": f"Invalid case: '{case}'. Valid cases are: {', '.join(ckeys)}",
        }

    if number and number not in NUMBERS:
        return {
            "err": True,
            "errmsg": f"Invalid number: '{number}'. Valid numbers are: {', '.join(NUMBERS)}",
        }

    resp = {}
    try:
        resp["q"] = q

        n = NounPhrase(q, force_number=number)

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


@app.get("/lemmas")
def lemmas():
    pass
