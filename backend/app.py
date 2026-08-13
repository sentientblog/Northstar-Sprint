import html
import os
import re
from datetime import date, timedelta
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


MOCK_ORDERS = {
    'NS1025': {
        'status': 'In Transit',
        'shipped': True,
        'eta': format_date(3),
        'lastUpdate': f'Departed from Johannesburg hub on {format_date(-2)}'
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

MOCK_RETURNS = {
    'NS1025': {
        'eligible': True,
        'returnWindowDays': 30,
        'refundStatus': 'Processing',
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


@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'service': 'northstar-support-chatbot'})


@app.route('/api/chat', methods=['POST'])
def chat():
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

    return jsonify(build_response(
        "I couldn't find an option that matches your issue.",
        fallback_options()
    ))


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
