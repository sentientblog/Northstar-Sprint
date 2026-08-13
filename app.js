

document.addEventListener('DOMContentLoaded', () => {

    /* ==========================================================
       MOCK DATA LAYER — placeholder for NS-06 / NS-07 / NS-08 / NS-09
       Replace lookupOrder() / lookupReturn() with real backend calls.
       ========================================================== */
    const MOCK_ORDERS = {
        NS1025: {
            status: 'In Transit',
            shipped: true,
            eta: 'May 16, 2024',
            lastUpdate: 'Departed from Johannesburg hub'
        },
        NS1099: {
            status: 'Processing',
            shipped: false,
            eta: 'Not yet dispatched',
            lastUpdate: 'Order confirmed, awaiting warehouse pickup'
        }
    };

    const MOCK_RETURNS = {
        NS1025: {
            eligible: true,
            returnWindowDays: 30,
            refundStatus: 'Processing',
            refundEta: '3\u20135 business days'
        },
        NS1099: {
            eligible: false,
            returnWindowDays: 30,
            refundStatus: 'Not applicable',
            refundEta: 'N/A'
        }
    };

    function lookupOrder(orderNumber) {
        return MOCK_ORDERS[orderNumber.trim().toUpperCase()] || null;
    }

    function lookupReturn(orderNumber) {
        return MOCK_RETURNS[orderNumber.trim().toUpperCase()] || null;
    }

    /* ==========================================================
       DOM refs
       ========================================================== */
    const chatScroll = document.getElementById('chatScroll');
    const hero = document.getElementById('hero');
    const input = document.getElementById('msgInput');
    const sendBtn = document.getElementById('sendBtn');
    const composerInner = document.querySelector('.composer-inner');
    const backBtn = document.getElementById('backBtn');

    // Tracks what the text input is currently being used for, if anything.
    // null = input disabled (guided-options only, per charter).
    let pendingTextIntent = null;

    /* ==========================================================
       Rendering helpers
       ========================================================== */
    function nowTime() {
        const d = new Date();
        let h = d.getHours();
        let m = d.getMinutes();
        const ampm = h >= 12 ? 'PM' : 'AM';
        h = h % 12; h = h ? h : 12;
        m = m < 10 ? '0' + m : m;
        return h + ':' + m + ' ' + ampm;
    }

    function hideHero() {
        if (hero) hero.style.display = 'none';
    }

    function scrollToBottom() {
        chatScroll.scrollTop = chatScroll.scrollHeight;
    }

    function addUserBubble(text) {
        hideHero();
        const row = document.createElement('div');
        row.className = 'msg-row user';
        row.innerHTML = `
      <div class="msg-col">
        <div class="bubble user"></div>
        <div class="msg-meta">${nowTime()} <span class="check">\u2713\u2713</span></div>
      </div>`;
        row.querySelector('.bubble').textContent = text;
        chatScroll.appendChild(row);
        scrollToBottom();
    }

    function showTyping() {
        const row = document.createElement('div');
        row.className = 'msg-row bot typing-row';
        row.id = 'typingRow';
        row.innerHTML = `
      <div class="orb"></div>
      <div class="typing-dots"><span></span><span></span><span></span></div>`;
        chatScroll.appendChild(row);
        scrollToBottom();
    }

    function removeTyping() {
        const el = document.getElementById('typingRow');
        if (el) el.remove();
    }

    function addBotTurn(bodyHtml, options) {
        hideHero();
        showTyping();

        setTimeout(() => {
            removeTyping();

            const row = document.createElement('div');
            row.className = 'msg-row bot';

            const chipsId = 'chips-' + Math.random().toString(36).slice(2, 9);
            const chipsHtml = options && options.length
                ? `<div class="option-chips" id="${chipsId}">` +
                options.map((opt, i) =>
                    `<button class="option-chip" data-idx="${i}">
               <span>${opt.label}</span>
               <span class="arrow">\u203a</span>
             </button>`
                ).join('') +
                `</div>`
                : '';

            row.innerHTML = `
        <div class="orb"></div>
        <div class="msg-col">
          <div class="bubble bot">${bodyHtml}${chipsHtml}</div>
          <div class="msg-meta">${nowTime()}</div>
        </div>`;
            chatScroll.appendChild(row);
            scrollToBottom();

            if (options && options.length) {
                const chipsEl = document.getElementById(chipsId);
                chipsEl.querySelectorAll('.option-chip').forEach((btn) => {
                    btn.addEventListener('click', () => {
                        const idx = Number(btn.getAttribute('data-idx'));
                        const chosen = options[idx];
                        // Disable the whole set so this state can't be re-answered.
                        chipsEl.querySelectorAll('.option-chip').forEach((b) => (b.disabled = true));
                        addUserBubble(chosen.label);
                        setTimeout(() => chosen.onClick(), 300);
                    });
                });
            }
        }, 550);
    }

    function setTextInputMode(intent, placeholder) {
        pendingTextIntent = intent;
        input.disabled = false;
        input.placeholder = placeholder;
        composerInner.classList.remove('disabled');
        input.focus();
    }

    function clearTextInputMode() {
        pendingTextIntent = null;
        input.disabled = true;
        input.placeholder = 'Select an option above';
        input.value = '';
        composerInner.classList.add('disabled');
    }

    /* ==========================================================
       Conversation flow — mirrors Team Charter \u00a72 and \u00a75 exactly
       ========================================================== */

    function goRoot() {
        addBotTurn(
            `Hello! \ud83d\udc4b<br>Welcome to Northstar Support.<br>I'm here to help you with your order, returns and refunds.<br><br><b>How can we help you?</b>`,
            [
                { label: 'Order Status', onClick: goOrderStatusRoot },
                { label: 'Returns & Refunds', onClick: goReturnsRoot },
                { label: 'Something else', onClick: goFallback }
            ]
        );
    }

    function goOrderStatusRoot() {
        addBotTurn(
            `<b>What would you like to know?</b>`,
            [
                { label: 'Where is my order?', onClick: () => goAskOrderNumber('trackOrder') },
                { label: 'Has my order shipped?', onClick: () => goAskOrderNumber('shippedCheck') },
                { label: "My order hasn't arrived", onClick: () => goAskOrderNumber('notArrived') },
                { label: 'Something else', onClick: goFallback }
            ]
        );
    }

    function goReturnsRoot() {
        addBotTurn(
            `<b>What would you like to know?</b>`,
            [
                { label: 'How do I return an item?', onClick: goHowToReturn },
                { label: 'Is my item eligible for return?', onClick: () => goAskOrderNumber('eligibility') },
                { label: 'When will I receive my refund?', onClick: () => goAskOrderNumber('refundStatus') },
                { label: "My refund hasn't arrived", onClick: () => goAskOrderNumber('refundNotArrived') },
                { label: 'Something else', onClick: goFallback }
            ]
        );
    }

    function goHowToReturn() {
        addBotTurn(
            `To return an item:
       <ul>
         <li>\ud83d\udce6 <span>Repack the item in its original packaging, if possible</span></li>
         <li>\ud83c\udff7\ufe0f <span>Attach the return label from your order confirmation email</span></li>
         <li>\ud83d\ude9a <span>Drop it off at any Northstar collection point within 30 days</span></li>
       </ul>
       <br>Is there anything else I can help you with?`,
            [
                { label: 'Start Over', onClick: goRoot },
                { label: 'Contact Support', onClick: goContactSupport }
            ]
        );
    }

    function goAskOrderNumber(intent) {
        addBotTurn(`Sure \u2014 could you share your order number so I can look that up?`, null);
        setTextInputMode(intent, 'Enter your order number (e.g. NS1025)');
    }

    function handleOrderNumberSubmit(orderNumber) {
        const intent = pendingTextIntent;
        clearTextInputMode();
        addUserBubble(orderNumber);

        if (intent === 'eligibility' || intent === 'refundStatus' || intent === 'refundNotArrived') {
            const record = lookupReturn(orderNumber);
            if (!record) return goOrderNotFound(intent, orderNumber);
            return goReturnsResult(intent, orderNumber, record);
        }

        const record = lookupOrder(orderNumber);
        if (!record) return goOrderNotFound(intent, orderNumber);
        return goOrderResult(intent, orderNumber, record);
    }

    function goOrderNotFound(intent, orderNumber) {
        addBotTurn(
            `I couldn't find an order matching <b>${escapeHtml(orderNumber)}</b>. Could you double-check the number, or would you like a hand from a person instead?`,
            [
                { label: 'Try again', onClick: () => goAskOrderNumber(intent) },
                { label: 'Contact Support', onClick: goContactSupport }
            ]
        );
    }

    function goOrderResult(intent, orderNumber, record) {
        let body = '';
        if (intent === 'trackOrder') {
            body = `Here's the latest update for order <b>${escapeHtml(orderNumber)}</b>:
        <ul>
          <li>\ud83d\ude9a <span><b>Status:</b> ${record.status}</span></li>
          <li>\ud83d\udcc5 <span><b>Estimated Delivery:</b> ${record.eta}</span></li>
          <li>\ud83d\udccd <span><b>Last Update:</b> ${record.lastUpdate}</span></li>
        </ul>`;
        } else if (intent === 'shippedCheck') {
            body = record.shipped
                ? `Yes \u2014 order <b>${escapeHtml(orderNumber)}</b> has shipped. ${record.lastUpdate}, with delivery estimated ${record.eta}.`
                : `Not yet \u2014 order <b>${escapeHtml(orderNumber)}</b> is still being processed. Current status: ${record.status}.`;
        } else if (intent === 'notArrived') {
            body = `Sorry about that. Order <b>${escapeHtml(orderNumber)}</b> currently shows: <b>${record.status}</b>, last update: ${record.lastUpdate}. If the estimated delivery date (${record.eta}) has already passed, I'd recommend contacting support so we can look into it.`;
        }

        addBotTurn(body + `<br><br>Is there anything else I can help you with?`, [
            { label: 'Start Over', onClick: goRoot },
            { label: 'Contact Support', onClick: goContactSupport }
        ]);
    }

    function goReturnsResult(intent, orderNumber, record) {
        let body = '';
        if (intent === 'eligibility') {
            body = record.eligible
                ? `Good news \u2014 order <b>${escapeHtml(orderNumber)}</b> is eligible for return within our ${record.returnWindowDays}-day window.`
                : `Order <b>${escapeHtml(orderNumber)}</b> is outside our ${record.returnWindowDays}-day return window, so it isn't eligible for a standard return.`;
        } else if (intent === 'refundStatus' || intent === 'refundNotArrived') {
            body = `Refund status for order <b>${escapeHtml(orderNumber)}</b>: <b>${record.refundStatus}</b>. Estimated time to reach you: ${record.refundEta}.`
                + (intent === 'refundNotArrived'
                    ? ` If that window has already passed, I'd recommend contacting support so we can check with the payment provider.`
                    : '');
        }

        addBotTurn(body + `<br><br>Is there anything else I can help you with?`, [
            { label: 'Start Over', onClick: goRoot },
            { label: 'Contact Support', onClick: goContactSupport }
        ]);
    }

    function goFallback() {
        addBotTurn(
            `I couldn't find an option that matches your issue.`,
            [
                { label: 'Contact Support', onClick: goContactSupport },
                { label: 'Start Over', onClick: goRoot }
            ]
        );
    }

    function goContactSupport() {
        addBotTurn(
            `No problem \u2014 I'll route this to a member of our support team. They typically respond within our business hours (Mon\u2013Fri 08:00\u201320:00, Sat\u2013Sun 09:00\u201317:00).`,
            [
                { label: 'Start Over', onClick: goRoot }
            ]
        );
    }

    function escapeHtml(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    /* ==========================================================
       Composer — only active during an "enter order number" state
       ========================================================== */
    function handleTextSubmit() {
        if (!pendingTextIntent) return; // guided-options only otherwise
        const val = input.value.trim();
        if (!val) return;
        handleOrderNumberSubmit(val);
    }

    sendBtn.addEventListener('click', handleTextSubmit);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleTextSubmit();
    });

    /* ==========================================================
       Entry points that jump directly into the tree
       (quick-help cards, sidebar nav, recent conversations)
       ========================================================== */
    const FLOW_ENTRY_POINTS = {
        root: goRoot,
        orderStatusRoot: goOrderStatusRoot,
        returnsRoot: goReturnsRoot
    };

    document.querySelectorAll('[data-flow]').forEach((el) => {
        el.addEventListener('click', () => {
            const key = el.getAttribute('data-flow');
            const entry = FLOW_ENTRY_POINTS[key];
            if (entry) {
                clearTextInputMode();
                entry();
            }
        });
    });

    document.querySelectorAll('.nav-item').forEach((el) => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.nav-item').forEach((n) => n.classList.remove('active'));
            el.classList.add('active');
        });
    });

    document.querySelectorAll('.recent-item').forEach((el) => {
        el.addEventListener('click', () => {
            document.querySelectorAll('.recent-item').forEach((n) => n.classList.remove('active'));
            el.classList.add('active');
        });
    });

    backBtn.addEventListener('click', () => window.history.back());

    /* ==========================================================
       Boot
       ========================================================== */
    clearTextInputMode();
    goRoot();
});