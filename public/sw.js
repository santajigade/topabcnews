// Top ABC News service worker: web push only
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
self.addEventListener('push', (event) => {
  let d = {};
  try { d = event.data ? event.data.json() : {}; } catch (e) { d = { title: 'Top ABC News', body: event.data && event.data.text() }; }
  event.waitUntil(self.registration.showNotification(d.title || 'Top ABC News', {
    body: d.body || '',
    icon: '/icon-192.png',
    badge: '/badge-72.png',
    image: d.image,
    tag: 'topabcnews-daily',
    data: { url: d.url || '/' },
  }));
});
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const url = event.notification.data && event.notification.data.url || '/';
  event.waitUntil(clients.matchAll({ type: 'window', includeUncontrolled: true }).then((list) => {
    for (const c of list) { if (c.url === url && 'focus' in c) return c.focus(); }
    return clients.openWindow(url);
  }));
});
