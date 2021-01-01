import os
import tempfile
import pytest
from chordService import main
import json


@pytest.fixture
def client():
    """ Create a test client with Flask so that we dont
        have to send requests using Postman
    """

    db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
    main.app.config['TESTING'] = True

    with main.app.test_client() as client:
        with main.app.app_context():
            pass
        yield client

    os.close(db_fd)
    os.unlink(main.app.config['DATABASE'])


def test_get_valid_json_generate_progression(client):
    """ Given a root and a scale, generate a random progression """

    response = client.get('/chords')
    assert json.loads(response.data)
