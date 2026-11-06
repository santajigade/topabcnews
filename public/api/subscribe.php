<?php
// Saves a browser push subscription for Top ABC News.
// Data lives outside public_html: domains/topabcnews.com/push-data/subs/
header('Content-Type: application/json');
header('Cache-Control: no-store');
$origin = $_SERVER['HTTP_ORIGIN'] ?? '';
if ($_SERVER['REQUEST_METHOD'] !== 'POST' || ($origin !== '' && $origin !== 'https://topabcnews.com')) {
  http_response_code(405); echo '{"ok":false}'; exit;
}
$raw = file_get_contents('php://input', false, null, 0, 4096);
$sub = json_decode($raw, true);
$ep = $sub['endpoint'] ?? '';
$p256 = $sub['keys']['p256dh'] ?? '';
$auth = $sub['keys']['auth'] ?? '';
$host = parse_url($ep, PHP_URL_HOST) ?: '';
$okHost = preg_match('/(^|\.)(googleapis\.com|mozilla\.com|notify\.windows\.com|push\.apple\.com)$/', $host);
$b64 = '/^[A-Za-z0-9_\-=]{10,200}$/';
if (strpos($ep, 'https://') !== 0 || strlen($ep) > 1000 || !$okHost || !preg_match($b64, $p256) || !preg_match($b64, $auth)) {
  http_response_code(400); echo '{"ok":false}'; exit;
}
$dir = dirname(__DIR__, 2) . '/push-data/subs';
if (!is_dir($dir)) { mkdir($dir, 0700, true); }
$file = $dir . '/' . sha1($ep) . '.json';
if (!file_exists($file) && count(glob($dir . '/*.json')) > 500000) { http_response_code(507); echo '{"ok":false}'; exit; }
$data = ['endpoint' => $ep, 'keys' => ['p256dh' => $p256, 'auth' => $auth], 'at' => gmdate('c')];
file_put_contents($file, json_encode($data), LOCK_EX);
echo '{"ok":true}';
