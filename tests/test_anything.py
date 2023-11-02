# from application import app
# import pytest

# @pytest.fixture
# def client():
#     app.config['TESTING'] = True
#     with app.test_client() as client:
#         yield client

# def test_anything_view(client):
#     response = client.get('/anything')
#     assert response.status_code == 200
#     assert b"Random Activity" in response.data
#     assert b"Here's a random activity you can try:" in response.data
#     # Här kan du lägga till fler assertions för att kontrollera innehållet på sidan

#     # Exempel: Kontrollera att knappen finns
#     assert b"Next Random Activity" in response.data
