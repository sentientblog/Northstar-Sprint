
document.addEventListener('DOMContentLoaded', () => {
    const chatScroll = document.getElementById('chatScroll');
    const hero = document.getElementById('hero');
    const input = document.getElementById('msgInput');
    const sendBtn = document.getElementById('sendBtn');
    const composerInner = document.querySelector('.composer-inner');
    const backBtn = document.getElementById('backBtn');
    const API_BASE_URL = (window.NS_API_BASE_URL || 'http://127.0.0.1:5000').replace(/\/+$/, '');

    let pendingTextIntent = null;

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
        <div class="msg-meta">${nowTime()} <span class="check">✓✓</span></div>
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

    function addBotTurn(bodyHtml, options = []) {
        hideHero();
        showTyping();

        setTimeout(() => {
            removeTyping();

            const row = document.createElement('div');
            row.className = 'msg-row bot';

            const chipsId = 'chips-' + Math.random().toString(36).slice(2, 9);
            const chipsHtml = options.length
                ? `<div class="option-chips" id="${chipsId}">` +
                options.map((opt, i) =>
                    `<button class="option-chip" data-idx="${i}">
               <span>${opt.label}</span>
               <span class="arrow">›</span>
             </button>`
                ).join('') + `</div>`
                : '';

            row.innerHTML = `
        <div class="orb"></div>
        <div class="msg-col">
          <div class="bubble bot">${bodyHtml}${chipsHtml}</div>
          <div class="msg-meta">${nowTime()}</div>
        </div>`;
            chatScroll.appendChild(row);
            scrollToBottom();

            if (options.length) {
                const chipsEl = document.getElementById(chipsId);
                chipsEl.querySelectorAll('.option-chip').forEach((btn) => {
                    btn.addEventListener('click', () => {
                        const idx = Number(btn.getAttribute('data-idx'));
                        const chosen = options[idx];
                        chipsEl.querySelectorAll('.option-chip').forEach((b) => (b.disabled = true));
                        addUserBubble(chosen.label);
                        setTimeout(() => handleOption(chosen), 300);
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

    function getApiCandidates() {
        const candidates = [];

        if (API_BASE_URL) {
            candidates.push(`${API_BASE_URL}/api/chat`);
        }

        const sameHostIsBackend = (
            window.location.protocol !== 'file:' &&
            (window.location.port === '5000' || window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost')
        );

        if (sameHostIsBackend) {
            candidates.push(`${window.location.origin}/api/chat`);
        }

        candidates.push('http://localhost:5000/api/chat');
        candidates.push('http://127.0.0.1:5000/api/chat');

        return [...new Set(candidates)];
    }

    async function postChat(action, payload = {}) {
        const candidates = getApiCandidates();

        let lastError = null;

        for (const url of candidates) {
            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action, ...payload })
                });

                if (response.ok) {
                    return await response.json();
                }

                lastError = new Error(`HTTP ${response.status} for ${url}`);
            } catch (error) {
                lastError = error;
            }
        }

        console.error('Chat API error:', lastError);
        addBotTurn(
            'I\'m having trouble connecting to the support service right now. Please try again in a moment, or contact support directly.',
            [
                { label: 'Try again', action: 'start' },
                { label: 'Contact Support', action: 'contact_support' }
            ]
        );
        return null;
    }

    function renderBotResponse(data) {
        if (!data) return;
        if (data.input_mode && data.input_mode.intent) {
            setTextInputMode(data.input_mode.intent, data.input_mode.placeholder || 'Enter your order number');
        } else {
            clearTextInputMode();
        }

        addBotTurn(data.body_html || 'I’m not sure how to help with that yet.', data.options || []);
    }

    function handleOption(chosen) {
        if (!chosen) return;
        if (chosen.action === 'start') return goRoot();
        if (chosen.action === 'order_status_root') return goOrderStatusRoot();
        if (chosen.action === 'returns_root') return goReturnsRoot();
        if (chosen.action === 'return_instructions') return goHowToReturn();
        if (chosen.action === 'ask_order_number') return goAskOrderNumber(chosen.payload?.intent || 'track_order');
        if (chosen.action === 'fallback') return goFallback();
        if (chosen.action === 'contact_support') return goContactSupport();
        return goFallback();
    }

    function goRoot() {
        postChat('start').then(renderBotResponse);
    }

    function goOrderStatusRoot() {
        postChat('order_status_root').then(renderBotResponse);
    }

    function goReturnsRoot() {
        postChat('returns_root').then(renderBotResponse);
    }

    function goHowToReturn() {
        postChat('return_instructions').then(renderBotResponse);
    }

    function goAskOrderNumber(intent) {
        postChat('ask_order_number', { intent }).then(renderBotResponse);
    }

    async function handleOrderNumberSubmit(orderNumber) {
        const intent = pendingTextIntent;
        clearTextInputMode();
        addUserBubble(orderNumber);

        if (!intent) return;
        const data = await postChat('lookup_order', { intent, order_number: orderNumber });
        if (data) renderBotResponse(data);
    }

    function goFallback() {
        postChat('fallback').then(renderBotResponse);
    }

    function goContactSupport() {
        postChat('contact_support').then(renderBotResponse);
    }

    function handleTextSubmit() {
        if (!pendingTextIntent) return;
        const val = input.value.trim();
        if (!val) return;
        handleOrderNumberSubmit(val);
    }

    sendBtn.addEventListener('click', handleTextSubmit);
    input.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') handleTextSubmit();
    });

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

    clearTextInputMode();
    goRoot();
});
