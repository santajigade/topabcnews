// Top ABC News: soft prompt for daily news alerts (max 1 notification per day)
(function () {
  if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
  };
  function b64ToBytes(s) {
    s = s.trim(); var pad = '='.repeat((4 - s.length % 4) % 4);
    var raw = atob((s + pad).replace(/-/g, '+').replace(/_/g, '/'));
    var out = new Uint8Array(raw.length); for (var i = 0; i < raw.length; i++) out[i] = raw.charCodeAt(i); return out;
  }
  function subscribe() {
    return navigator.serviceWorker.register('/sw.js').then(function (reg) {
      return fetch('/push-key.txt', { cache: 'no-store' }).then(function (r) { return r.ok ? r.text() : Promise.reject('no key'); })
        .then(function (key) {
          return reg.pushManager.getSubscription().then(function (s) {
            return s || reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: b64ToBytes(key) });
          });
        });
    }).then(function (sub) {
      return fetch('/api/subscribe.php', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(sub) });
    }).then(function () { store.set('tabn_push_sync', String(Date.now())); });
  }
  // Already allowed: re-save subscription once a week
  if (Notification.permission === 'granted') {
    if (Date.now() - Number(store.get('tabn_push_sync') || 0) > 7 * 864e5) subscribe().catch(function () {});
    return;
  }
  if (Notification.permission === 'denied') return;
  if (Date.now() - Number(store.get('tabn_push_later') || 0) < 3 * 864e5) return;

  var shown = false;
  function show() {
    if (shown) return; shown = true;
    var box = document.createElement('div');
    box.className = 'push-prompt';
    box.setAttribute('role', 'dialog');
    box.innerHTML = '<img src="/favicon.svg" alt="" width="40" height="40"><div><strong>Get the top news story every day</strong><p>One alert a day. No spam. Turn off anytime.</p><div class="push-btns"><button class="push-later">Later</button><button class="push-allow">Allow</button></div></div>';
    document.body.appendChild(box);
    requestAnimationFrame(function () { box.classList.add('show'); });
    function close() { box.classList.remove('show'); setTimeout(function () { box.remove(); }, 300); }
    box.querySelector('.push-later').onclick = function () { store.set('tabn_push_later', String(Date.now())); close(); };
    box.querySelector('.push-allow').onclick = function () {
      close();
      Notification.requestPermission().then(function (p) {
        if (p === 'granted') subscribe().catch(function () {});
        else store.set('tabn_push_later', String(Date.now()));
      });
    };
  }
  setTimeout(show, 15000);
  window.addEventListener('scroll', function onS() {
    var h = document.documentElement;
    if (h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight) > 0.5) { window.removeEventListener('scroll', onS); show(); }
  }, { passive: true });
})();
