"""

    GreynirAPI: Web application that exposes the Greynir API

    Tests for web application

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

"""

from typing import Dict

import os
import sys
from urllib.parse import urlencode
from fastapi.testclient import TestClient

# Hack to make this Python program executable from the tests subdirectory
basepath, _ = os.path.split(os.path.realpath(__file__))
if basepath.endswith("/tests") or basepath.endswith("\\tests"):
    basepath = basepath[0:-6]
    sys.path.append(basepath)

from main import app


client = TestClient(app)


def test_np_api() -> None:
    """ Test noun phrase API ("/np" route). """

    # Test without params
    response = client.get("/np")  # type: ignore
    assert response.status_code == 422

    # Test w. just noun phrase param
    n = "Maðurinn með hattinn"

    response = client.get(f"/np?{urlencode(dict(q=n))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == n
    assert json["cases"]["þf"] == "Manninn með hattinn"
    assert json["cases"]["þgf"] == "Manninum með hattinn"
    assert json["cases"]["ef"] == "Mannsins með hattinn"

    # Test w. case param
    response = client.get(f"/np?{urlencode(dict(q=n, case='ef'))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert "nf" not in json["cases"]
    assert "þf" not in json["cases"]
    assert "þgf" not in json["cases"]
    assert json["cases"]["ef"] == "Mannsins með hattinn"

    # Test w. just noun phrase param
    n = "Laugavegur 22"

    response = client.get(f"/np?{urlencode(dict(q=n))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == n
    assert json["cases"]["þf"] == "Laugaveg 22"
    assert json["cases"]["þgf"] == "Laugavegi 22"
    assert json["cases"]["ef"] == "Laugavegar 22"

    # Test w. just noun phrase param
    n = "Húsið norðanmegin við bensínstöðina ofarlega í bænum"

    response = client.get(f"/np?{urlencode(dict(q=n))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == n
    assert json["cases"]["þf"] == n
    assert json["cases"]["þgf"] == "Húsinu norðanmegin við bensínstöðina ofarlega í bænum"
    assert json["cases"]["ef"] == "Hússins norðanmegin við bensínstöðina ofarlega í bænum"

    # Test w. number param and ambiguous word ("fata" can be sing. nom. or pl. gen. of "föt")
    response = client.get(f"/np?{urlencode(dict(q='fata', force_number='et'))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == "fata"
    assert json["cases"]["þf"] == "fötu"
    assert json["cases"]["þgf"] == "fötu"
    assert json["cases"]["ef"] == "fötu"

    response = client.get(f"/np?{urlencode(dict(q='fata', force_number='ft'))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] in {"föt", "fötur"}
    assert json["cases"]["þf"] in {"föt", "fötur"}
    assert json["cases"]["þgf"] == "fötum"
    assert json["cases"]["ef"] in {"fata", "fatna"}

    # Test w. both case and number params
    response = client.get(f"/np?{urlencode(dict(q='fata', case='þgf', force_number='ft'))}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["þgf"] == "fötum"


def test_lemma_api() -> None:
    """ Test lemmatization API ("/lemmas" route). """

    # Test call with no params
    response = client.get("/lemmas")  # type: ignore
    assert response.status_code == 422

    d: Dict[str, str] = dict(q='hamborgari með frönskum og kokteilsósu')
    response = client.get(f"/lemmas?{urlencode(d)}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json.get("errmsg", "") == ""
    assert json["err"] is False
    assert "lemmas" in json
    assert json["lemmas"] == [
        ["hamborgari", "kk"],
        ["með", "fs"],
        ["franska", "kvk"],
        ["og", "st"],
        ["kokteilsósa", "kvk"],
    ]

    # Test compound words that are not in BÍN
    d = dict(q='svakahamborgari með saltfrönskum og slummukokteilsósu')
    response = client.get(f"/lemmas?{urlencode(d)}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "lemmas" in json
    assert json["lemmas"] == [
        ["svakahamborgari", "kk"],
        ["með", "fs"],
        ["saltfranska", "kvk"],
        ["og", "st"],
        ["slummukokteilsósa", "kvk"],
    ]

    d = dict(q='Hamborgari MEÐ frönskum Og kokteilsósu')
    response = client.get(f"/lemmas?{urlencode(d)}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "lemmas" in json
    assert json["lemmas"] == [
        ["hamborgari", "kk"],
        ["með", "fs"],
        ["franska", "kvk"],
        ["og", "st"],
        ["kokteilsósa", "kvk"],
    ]

    d = dict(q='skýrslu um Jón Sigurðsson, 1900-2000')
    response = client.get(f"/lemmas?{urlencode(d)}")  # type: ignore
    assert response.status_code == 200
    json = response.json()  # type: ignore
    assert json["err"] is False
    assert "lemmas" in json
    assert json["lemmas"] == [
        ["skýrsla", "kvk"],
        ["um", "fs"],
        ["Jón Sigurðsson", "person_kk"],
    ]
