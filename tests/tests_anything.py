import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_random_anything(client):
    response = client.get('/anything')
    assert response.status_code == 200

    data = response.get_data(as_text=True)
    assert "Hämta något" in data  # Ändra detta till den exakta texten du förväntar dig i din template
