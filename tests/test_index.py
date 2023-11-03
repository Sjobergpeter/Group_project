import pytest

from application import app, func
from urllib import request

def test_anything_view_returns_200_ok(client):
    response = client.get('/')
    assert response.status_code == 200

def test_Func_json_Loads_ipinfo():
    data_url = f"http://ipinfo.io/json"

    assert not isinstance(func.json_loads(data_url), Exception)

def test_Func_json_Loads_weather():
    data_url = f"https://api.open-meteo.com/v1/forecast?latitude=00.00&longitude=00.00&current=rain,snowfall,cloudcover"

    assert not isinstance(func.json_loads(data_url), Exception)