import html
import json
import os
import re
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from flask import Flask, jsonify, request, send_from_directory, session

app = Flask(__name__, static_folder='.', static_url_path='')
app.secret_key = os.environ.get('SECRET_KEY', 'northstar-dev-secret')


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


def format_date(days_from_today: int) -> str:
    return (date.today() + timedelta(days=days_from_today)).strftime('%b %d, %Y')


FALLBACK_ORDERS = {
    'NS1025': {
        'status': 'Returned - In Transit',
        'shipped': True,
        'eta': f'Expected at warehouse on {format_date(3)}',
        'lastUpdate': f'Return package departed from drop-off hub on {format_date(-2)}'
    },
    'NS1099': {
        'status': 'Processing',
        'shipped': False,
        'eta': 'Not yet dispatched',
        'lastUpdate': 'Order confirmed, awaiting warehouse pickup'
    },
    'NS1250': {
        'status': 'Delivered',
        'shipped': True,
        'eta': f'Delivered on {format_date(-8)}',
        'lastUpdate': 'Package delivered to customer address'
    }
}

FALLBACK_RETURNS = {
    'NS1025': {
        'eligible': True,
        'returnWindowDays': 30,
        'refundStatus': 'Refund in transit',
        'refundEta': '3–5 business days'
    },
    'NS1099': {
        'eligible': False,
        'returnWindowDays': 30,
        'refundStatus': 'Not applicable',
        'refundEta': 'N/A'
    },
    'NS1250': {
        'eligible': True,
        'returnWindowDays': 30,
        'refundStatus': 'Issued',
        'refundEta': 'Refund received'
    }
}


def normalize_order_number(value: Any) -> str:
    return str(value or '').strip().upper()


def humanize_status(value: Any) -> str:
    return str(value or '').replace('_', ' ').strip().title()


def data_path(filename: str) -> Path:
    return Path(__file__).resolve().parents[1] / 'data' / filename


def read_mock_file(filename: str) -> List[Dict[str, Any]]:
    try:
        with data_path(filename).open(encoding='utf-8') as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return []
    return data if isinstance(data, list) else []


def date_from_record(record: Dict[str, Any], offset_key: str, fixed_key: str) -> str:
    if offset_key in record:
        return format_date(int(record[offset_key]))
    return record.get(fixed_key, '')


def load_mock_orders() -> Dict[str, Dict[str, Any]]:
    records: Dict[str, Dict[str, Any]] = {}
    for item in read_mock_file('orders.json'):
        order_number = normalize_order_number(item.get('order_id') or item.get('orderNumber'))
        if not order_number:
            continue

        status = humanize_status(item.get('status'))
        eta = item.get('eta') or date_from_record(item, 'eta_days_from_today', 'estimated_delivery')
        last_update = item.get('lastUpdate') or item.get('last_update')
        last_update_date = date_from_record(item, 'last_update_days_from_today', 'last_update_date')
        if last_update and last_update_date:
            last_update = f'{last_update} on {last_update_date}'

        records[order_number] = {
            'status': status,
            'shipped': bool(item.get('shipped')),
            'eta': eta or 'Not yet available',
            'lastUpdate': last_update or 'No recent tracking update available'
        }
    return records or FALLBACK_ORDERS


def load_mock_returns() -> Dict[str, Dict[str, Any]]:
    records: Dict[str, Dict[str, Any]] = {}
    for item in read_mock_file('returns-refunds.json'):
        order_number = normalize_order_number(item.get('order_id') or item.get('orderNumber'))
        if not order_number:
            continue

        records[order_number] = {
            'eligible': bool(item.get('eligible')),
            'returnWindowDays': item.get('return_window_days') or item.get('returnWindowDays') or 30,
            'refundStatus': item.get('refund_status') or item.get('refundStatus') or 'Not available',
            'refundEta': item.get('refund_eta') or item.get('refundEta') or 'N/A'
        }
    return records or FALLBACK_RETURNS


MOCK_ORDERS = load_mock_orders()
MOCK_RETURNS = load_mock_returns()


def build_response(body_html: str, options: Optional[List[Dict[str, Any]]] = None,
                   input_mode: Optional[Dict[str, Any]] = None):
    return {
        'body_html': body_html,
        'options': options or [],
        'input_mode': input_mode
    }


def option(label: str, action: str, payload: Optional[Dict[str, Any]] = None):
    entry = {'label': label, 'action': action}
    if payload:
        entry['payload'] = payload
    return entry


def root_options():
    return [
        option('Order Status', 'order_status_root'),
        option('Returns & Refunds', 'returns_root'),
        option('Something else', 'fallback')
    ]


def order_status_options():
    return [
        option('Where is my order?', 'ask_order_number', {'intent': 'track_order'}),
        option('Has my order shipped?', 'ask_order_number', {'intent': 'shipped_check'}),
        option("My order hasn't arrived", 'ask_order_number', {'intent': 'not_arrived'}),
        option('Something else', 'fallback')
    ]


def returns_options():
    return [
        option('How do I return an item?', 'return_instructions'),
        option('Is my item eligible for return?', 'ask_order_number', {'intent': 'eligibility'}),
        option('When will I receive my refund?', 'ask_order_number', {'intent': 'refund_status'}),
        option("My refund hasn't arrived", 'ask_order_number', {'intent': 'refund_not_arrived'}),
        option('Something else', 'fallback')
    ]


def contact_support_options():
    return [option('Start Over', 'start')]


def fallback_options():
    return [
        option('Contact Support', 'contact_support'),
        option('Start Over', 'start')
    ]


def get_order_detail(order_number: str):
    return MOCK_ORDERS.get(order_number)


def get_return_detail(order_number: str):
    return MOCK_RETURNS.get(order_number)


def order_result(intent: str, order_number: str, record: Dict[str, Any]):
    body = ''
    clean_number = html.escape(order_number)
    if intent == 'track_order':
        body = (
            f"Here's the latest update for order <b>{clean_number}</b>:"
            f"<ul>"
            f"<li>🚚 <span><b>Status:</b> {record['status']}</span></li>"
            f"<li>📅 <span><b>Estimated Delivery:</b> {record['eta']}</span></li>"
            f"<li>📍 <span><b>Last Update:</b> {record['lastUpdate']}</span></li>"
            f"</ul>"
        )
    elif intent == 'shipped_check':
        if record['shipped']:
            body = (
                f"Yes — order <b>{clean_number}</b> has shipped. {record['lastUpdate']}, "
                f"with delivery estimated {record['eta']}."
            )
        else:
            body = (
                f"Not yet — order <b>{clean_number}</b> is still being processed. "
                f"Current status: {record['status']}."
            )
    elif intent == 'not_arrived':
        body = (
            f"Sorry about that. Order <b>{clean_number}</b> currently shows: "
            f"<b>{record['status']}</b>, last update: {record['lastUpdate']}. "
            f"If the estimated delivery date ({record['eta']}) has already passed, "
            f"I'd recommend contacting support so we can look into it."
        )
    else:
        body = f"I found information for order <b>{clean_number}</b>. Current status: {record['status']}."
    return build_response(body + '<br><br>Is there anything else I can help you with?', [
        option('File Return/Refund', 'file_return_for_order', {'order_number': order_number}),
        option('Check Refund Status', 'lookup_order', {'intent': 'refund_status', 'order_number': order_number}),
        option('Start Over', 'start'),
        option('Contact Support', 'contact_support')
    ])


def return_result(intent: str, order_number: str, record: Dict[str, Any]):
    body = ''
    clean_number = html.escape(order_number)
    if intent == 'eligibility':
        if record['eligible']:
            body = (
                f"Good news — order <b>{clean_number}</b> is eligible for return within our "
                f"{record['returnWindowDays']}-day window."
            )
        else:
            body = (
                f"Order <b>{clean_number}</b> is outside our {record['returnWindowDays']}-day return "
                f"window, so it isn't eligible for a standard return."
            )
    elif intent in {'refund_status', 'refund_not_arrived'}:
        body = (
            f"Refund status for order <b>{clean_number}</b>: <b>{record['refundStatus']}</b>. "
            f"Estimated time to reach you: {record['refundEta']}."
        )
        if intent == 'refund_not_arrived':
            body += ' If that window has already passed, I recommend contacting support so we can check with the payment provider.'
    else:
        body = f"I found return details for order <b>{clean_number}</b>."
    return build_response(body + '<br><br>Is there anything else I can help you with?', [
        option('File Return/Refund', 'file_return_for_order', {'order_number': order_number}),
        option('Check Order Status', 'check_order_status_for_order', {'order_number': order_number}),
        option('Start Over', 'start'),
        option('Contact Support', 'contact_support')
    ])


def ask_for_order_number(intent: str):
    session['pending_text_intent'] = intent
    return build_response(
        'Sure — could you share your order number so I can look that up?',
        [],
        {'intent': intent, 'placeholder': 'Enter your order number (e.g. NS1025)'}
    )


def validate_order_number(value: str):
    if not value or not value.strip():
        return False, 'Please enter your order number first.'
    normalized = normalize_order_number(value)
    if not re.fullmatch(r'NS\d{4,6}', normalized):
        return False, f"I couldn't find a valid order number matching <b>{html.escape(value)}</b>."
    return True, normalized


def order_not_found(intent: str, order_number: str):
    clean_number = html.escape(order_number)
    return build_response(
        f"I couldn't find an order matching <b>{clean_number}</b>. Could you double-check the number, or would you like a hand from a person instead?",
        [
            option('Try again', 'ask_order_number', {'intent': intent}),
            option('Contact Support', 'contact_support')
        ]
    )


def return_not_found(intent: str, order_number: str):
    clean_number = html.escape(order_number)
    return build_response(
        f"I couldn't find return details for <b>{clean_number}</b>. Please double-check the order number or contact support.",
        [
            option('Try again', 'ask_order_number', {'intent': intent}),
            option('Contact Support', 'contact_support')
        ]
    )


def file_return_for_order_handler(order_number: str):
    clean_number = html.escape(order_number)
    record = get_return_detail(order_number)
    if not record:
        return return_not_found('eligibility', order_number)

    if not record['eligible']:
        return build_response(
            f"Order <b>{clean_number}</b> is not eligible for a standard return/refund request right now.",
            [
                option('Check Order Status', 'check_order_status_for_order', {'order_number': order_number}),
                option('Contact Support', 'contact_support'),
                option('Start Over', 'start')
            ]
        )

    return build_response(
        (
            f"Done — I've started the return/refund request for order <b>{clean_number}</b>. "
            f"Current refund status: <b>{record['refundStatus']}</b>. "
            f"Estimated time to reach you: {record['refundEta']}."
        ),
        [
            option('Check Refund Status', 'lookup_order', {'intent': 'refund_status', 'order_number': order_number}),
            option('Check Order Status', 'check_order_status_for_order', {'order_number': order_number}),
            option('Contact Support', 'contact_support'),
            option('Start Over', 'start')
        ]
    )


def check_order_status_for_order_handler(order_number: str):
    """Show order status options for a specific order"""
    clean_number = html.escape(order_number)
    return build_response(
        f'<b>What would you like to know about {clean_number}?</b>',
        [
            option('Where is my order?', 'lookup_order', {'intent': 'track_order', 'order_number': order_number}),
            option('Has my order shipped?', 'lookup_order', {'intent': 'shipped_check', 'order_number': order_number}),
            option("My order hasn't arrived", 'lookup_order', {'intent': 'not_arrived', 'order_number': order_number}),
            option('File Return/Refund', 'file_return_for_order', {'order_number': order_number}),
            option('Start Over', 'start')
        ]
    )


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'northstar-support-chatbot'})


@app.route('/api/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return jsonify({
            'service': 'northstar-support-chatbot',
            'status': 'ok',
            'message': 'This endpoint expects POST requests from the frontend chat client. Use /api/health for status checks.'
        })

    payload = request.get_json(silent=True) or {}
    action = payload.get('action')

    if not action:
        return jsonify(build_response(
            "I couldn't find an option that matches your issue.",
            fallback_options()
        ))

    if action == 'start':
        session.pop('pending_text_intent', None)
        return jsonify(build_response(
            'Hello! 👋<br>Welcome to Northstar Support.<br>I\'m here to help you with your order, returns and refunds.<br><br><b>How can we help you?</b>',
            root_options()
        ))

    if action == 'order_status_root':
        return jsonify(build_response('<b>What would you like to know?</b>', order_status_options()))

    if action == 'returns_root':
        return jsonify(build_response('<b>What would you like to know?</b>', returns_options()))

    if action == 'return_instructions':
        return jsonify(build_response(
            'To return an item:<ul><li>📦 <span>Repack the item in its original packaging, if possible</span></li><li>🏷️ <span>Attach the return label from your order confirmation email</span></li><li>🚚 <span>Drop it off at any Northstar collection point within 30 days</span></li></ul><br>Is there anything else I can help you with?',
            [
                option('Start Over', 'start'),
                option('Contact Support', 'contact_support')
            ]
        ))

    if action == 'ask_order_number':
        intent = payload.get('intent')
        if not intent:
            return jsonify(build_response(
                'I need to know what you want to check before I can look up your order.',
                fallback_options()
            ))
        return jsonify(ask_for_order_number(intent))

    if action == 'lookup_order':
        intent = payload.get('intent')
        order_number = payload.get('order_number')
        if not intent:
            return jsonify(build_response(
                'I’m not sure which order check you selected. Please choose a supported option.',
                fallback_options()
            ))

        if not order_number:
            return jsonify(build_response(
                'I need your order number before I can check that for you.',
                [],
                {'intent': intent, 'placeholder': 'Enter your order number (e.g. NS1025)'}
            ))

        valid, normalized = validate_order_number(order_number)
        if not valid:
            return jsonify(build_response(
                normalized,
                [
                    option('Try again', 'ask_order_number', {'intent': intent}),
                    option('Contact Support', 'contact_support')
                ]
            ))

        if intent in {'eligibility', 'refund_status', 'refund_not_arrived'}:
            record = get_return_detail(normalized)
            if not record:
                return jsonify(return_not_found(intent, normalized))
            return jsonify(return_result(intent, normalized, record))

        record = get_order_detail(normalized)
        if not record:
            return jsonify(order_not_found(intent, normalized))
        return jsonify(order_result(intent, normalized, record))

    if action == 'fallback':
        return jsonify(build_response(
            "I couldn't find an option that matches your issue.",
            fallback_options()
        ))

    if action == 'contact_support':
        return jsonify(build_response(
            'No problem — I\'ll route this to a member of our support team. They typically respond within our business hours (Mon–Fri 08:00–20:00, Sat–Sun 09:00–17:00).',
            contact_support_options()
        ))

    if action == 'file_return_for_order':
        valid, order_number = validate_order_number(payload.get('order_number'))
        if not valid:
            return jsonify(build_response('I need an order number to proceed.', fallback_options()))
        return jsonify(file_return_for_order_handler(order_number))

    if action == 'check_order_status_for_order':
        valid, order_number = validate_order_number(payload.get('order_number'))
        if not valid:
            return jsonify(build_response('I need an order number to proceed.', fallback_options()))
        return jsonify(check_order_status_for_order_handler(order_number))

    return jsonify(build_response(
        "I couldn't find an option that matches your issue.",
        fallback_options()
    ))


@app.route('/')
def serve_root():
    return jsonify({
        'service': 'northstar-support-chatbot',
        'status': 'ok',
        'message': 'Northstar Support API is running. Use /api/health for status and /api/chat for chatbot requests.'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
