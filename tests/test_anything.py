import pytest

def test_anything_view_returns_200_ok(client):
    response = client.get('/anything')
    assert response.status_code == 200

