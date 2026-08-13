import sys
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'


def test_start_action_returns_main_options(client):
    response = client.post('/api/chat', json={'action': 'start'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'Order Status' in data['body_html'] or data['options'][0]['label'] == 'Order Status'
    assert len(data['options']) >= 3


def test_valid_order_status_lookup(client):
    response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'track_order', 'order_number': 'NS1025'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'In Transit' in data['body_html']
    assert 'NS1025' in data['body_html']


def test_invalid_order_number_is_handled(client):
    response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'track_order', 'order_number': 'BAD'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'valid order number' in data['body_html'].lower() or 'try again' in data['body_html'].lower()


def test_order_dates_are_current_and_realistic(client):
    response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'track_order', 'order_number': 'NS1025'}
    )
    assert response.status_code == 200
    data = response.get_json()
    current_year = str(date.today().year)
    assert current_year in data['body_html']
    assert '2024' not in data['body_html']
