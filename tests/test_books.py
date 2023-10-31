from flask.testing import FlaskClient
import pytest
from application import app, func

@pytest.fixture
def client():
    return app.app.test_client()

def test_index_online(client: FlaskClient):
    '''GIVEN user requests / route
    WHEN a GET request is made to the root path
    THEN home.html loads'''

    # client makes a GET request to the root path
    resp = client.get('/')

    # checking if there is a response
    assert resp.status_code == 200

def test_build_df():
    '''GIVEN that the df is empty
    WHEN df is built
    THEN the user gets a string answer'''

    books={}

    data = func.build_df(books)

    assert isinstance(data, str)

