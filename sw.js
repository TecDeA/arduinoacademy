/* Service Worker de Arduino Academy.
   Alcance relativo (./) para convivir con los portales que alojan la app
   en subcarpeta (p. ej. tecdea.github.io/ArduinoAcademy o su fork). */

// Versión de la app: se muestra en el chip del banner. Al cambiarla,
// se activa un nuevo SW y se purga la caché antigua.
const APP_VERSION = '1.0.0';

const CACHE_NAME = `arduino-academy-v${APP_VERSION}`;

const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './img/icon-192.png',
  './img/icon-512.png',
  './img/icon-maskable-192.png',
  './img/icon-maskable-512.png',
  './img/apple-touch-icon.png',
  './img/favicon-32.png',
  './img/favicon-16.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

/* Solo interceptamos peticiones dentro de nuestro propio alcance,
   para no interferir con el portal que aloja la app ni con otras apps. */
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);
  const scope = new URL(self.registration.scope);

  if (url.origin !== scope.origin || !url.pathname.startsWith(scope.pathname)) {
    return;
  }

  // Navegaciones: red primero, caché como respaldo (offline).
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .then((response) => {
          const copy = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put('./index.html', copy));
          return response;
        })
        .catch(() => caches.match('./index.html'))
    );
    return;
  }

  // Resto de recursos propios: caché primero, luego red.
  event.respondWith(
    caches.match(event.request).then(
      (cached) =>
        cached ||
        fetch(event.request).then((response) => {
          if (response.ok && url.origin === location.origin) {
            const copy = response.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
          }
          return response;
        })
    )
  );
});

// Responde con la versión actual cuando la página la pide (chip del banner).
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'GET_VERSION') {
    event.source.postMessage({ type: 'APP_VERSION', version: APP_VERSION });
  }
});
