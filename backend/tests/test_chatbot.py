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


def test_root_route_returns_api_message(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'northstar-support-chatbot'
    assert 'api/chat' in data['message']


def test_chat_endpoint_accepts_get_for_local_testing(client):
    response = client.get('/api/chat')
    assert response.status_code == 200
    data = response.get_json()
    assert data['service'] == 'northstar-support-chatbot'
    assert 'POST' in data['message']


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


def test_file_return_for_order_action(client):
    """Test cross-flow: File Return/Refund from Order Status"""
    response = client.post(
        '/api/chat',
        json={'action': 'file_return_for_order', 'order_number': 'NS1025'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'started the return/refund request' in data['body_html']
    assert 'Refund in transit' in data['body_html']
    assert any(opt['label'] == 'Check Refund Status' for opt in data['options'])


def test_check_order_status_for_order_action(client):
    """Test cross-flow: Check Order Status from Returns"""
    response = client.post(
        '/api/chat',
        json={'action': 'check_order_status_for_order', 'order_number': 'NS1025'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'NS1025' in data['body_html']
    assert any(opt['label'] == "Where is my order?" for opt in data['options'])


def test_lookup_order_with_preemptive_order_number(client):
    """Test quick lookup when order number is already known"""
    response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'eligibility', 'order_number': 'NS1025'}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'eligible' in data['body_html'].lower()
    assert 'NS1025' in data['body_html']


def test_ns1025_works_for_both_order_and_return_flows(client):
    """Test that NS1025 is a good test order for both flows"""
    # Check order status
    order_response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'track_order', 'order_number': 'NS1025'}
    )
    order_data = order_response.get_json()
    assert 'In Transit' in order_data['body_html']
    assert any(opt['label'] == 'File Return/Refund' for opt in order_data['options'])

    # Check return eligibility
    return_response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'eligibility', 'order_number': 'NS1025'}
    )
    return_data = return_response.get_json()
    assert 'eligible' in return_data['body_html'].lower()
    assert 'Good news' in return_data['body_html']


def test_order_status_can_check_refund_without_reentering_order_number(client):
    response = client.post(
        '/api/chat',
        json={'action': 'lookup_order', 'intent': 'track_order', 'order_number': 'NS1025'}
    )
    data = response.get_json()
    refund_option = next(opt for opt in data['options'] if opt['label'] == 'Check Refund Status')

    refund_response = client.post(
        '/api/chat',
        json={'action': refund_option['action'], **refund_option['payload']}
    )
    refund_data = refund_response.get_json()

    assert 'NS1025' in refund_data['body_html']
    assert 'Refund in transit' in refund_data['body_html']
