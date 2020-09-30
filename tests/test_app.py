"""

    GreynirAPI: Web application that exposes the Greynir API

    Tests for web application

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

from urllib.parse import urlencode
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_np_api():
    """ Test noun phrase API ("/np" route). """

    # Test without params
    response = client.get("/np")
    assert response.status_code == 200
    json = response.json()
    assert json["err"] is True
    assert json["errmsg"]

    # Test w. just noun phrase param
    n = "Maðurinn með hattinn"

    response = client.get(f"/np?{urlencode(dict(q=n))}")
    assert response.status_code == 200
    json = response.json()
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == n
    assert json["cases"]["þf"] == "Manninn með hattinn"
    assert json["cases"]["þgf"] == "Manninum með hattinn"
    assert json["cases"]["ef"] == "Mannsins með hattinn"

    # Test w. case param
    response = client.get(f"/np?{urlencode(dict(q=n, case='ef'))}")
    assert response.status_code == 200
    json = response.json()
    assert json["err"] is False
    assert "cases" in json
    assert "nf" not in json["cases"]
    assert "þf" not in json["cases"]
    assert "þgf" not in json["cases"]
    assert json["cases"]["ef"] == "Mannsins með hattinn"

    # Test w. number param and ambiguous word ("fata" can be sing. nom. or pl. gen. of "föt")
    response = client.get(f"/np?{urlencode(dict(q='fata', number='et'))}")
    assert response.status_code == 200
    json = response.json()
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["nf"] == "fata"
    assert json["cases"]["þf"] == "fötu"
    assert json["cases"]["þgf"] == "fötu"
    assert json["cases"]["ef"] == "fötu"

    # response = client.get(f"/np?{urlencode(dict(q='fata', number='ft'))}")
    # assert response.status_code == 200
    # json = response.json()
    # assert json["err"] is False
    # assert "cases" in json
    # assert json["cases"]["nf"] == "föt"
    # assert json["cases"]["þf"] == "föt"
    # assert json["cases"]["þgf"] == "fötum"
    # assert json["cases"]["ef"] == "fata"

    # Test w. both case and number params
    response = client.get(f"/np?{urlencode(dict(q='fata', case='þgf', number='ft'))}")
    assert response.status_code == 200
    json = response.json()
    assert json["err"] is False
    assert "cases" in json
    assert json["cases"]["þgf"] == "fötum"


def test_lemma_api():
    pass
