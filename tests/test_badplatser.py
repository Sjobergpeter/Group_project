import pytest

from application import app, func
from urllib import request


## Mycket enklare att använda pythons modul requests än urllibs request med pytest.
import requests


## Dekorator definierar fixture-funktion
@pytest.fixture

## Denna fixturfunktionen skapar en testklient.
def client():
    return app.app.test_client()


## Dessa testfunktioner kollar om endpointerna ger svar 200 när man gör en get-request.
def test_endpoint_badplatser(client):
    response = client.get('/badplatser')
    assert response.status_code == 200

def test_endpoint_index(client):
    response = client.get('/')
    assert response.status_code == 200

## Denna testfunktion kollar att vi hanterat 404 fel när vi får dem.
def test_catch_404():
    with request.urlopen("http://127.0.0.1:5000/notexisting") as response:
        html = str(response.read())
        assert "404" not in html

## Testar att  funktionen json loads inte returnerar fel.
def test_Func_json_loads_POSITIVE():
    data_url = f"https://apigw.stockholm.se/api/PublicHittaCMS/api/serviceunits?&filter[servicetype.id]=104&page[limit]=1500&page[offset]=0&sort=name"

    assert not isinstance(func.json_loads(data_url), Exception)


## Denna test kollar att url länkarna returnerar svarskod 200. Annars skrivs meddelande ut.
url_list=[]
data_url = f"https://apigw.stockholm.se/api/PublicHittaCMS/api/serviceunits?&filter[servicetype.id]=104&page[limit]=1500&page[offset]=0&sort=name"

def test_url_are_alive():
    for url in url_list + [data_url]:
        response = requests.get(url)
        assert response.status_code == 200, f"URL {url} returnerar följande felkod: {response.status_code}"

## Test för funktionen random beach.
### Testar att den returnerar en sträng samt hanterar inmatning av tom lista.
def test_func_random_beach_string():
    """Skapar testlista för att kolla om resultatet är en sträng"""

    beaches = [{"name": "Baybeach", "url": "http//www.idk.com", "location": "Baylocation"}]
    result = func.random_beach(beaches)
    assert isinstance(result, str)

def test_func_random_beach_empty_list():
    beaches = []

    result = func.random_beach(beaches)
    assert result is None




