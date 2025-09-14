<?php
/* LFI endpoint (intentionally vulnerable)
   - Allows including local files (absolute or relative).
   - Blocks remote wrappers (http/https/ftp/phar/data).
   - Blocks "flag" in the path to nudge toward RCE (log poisoning).
   - Friendly 404 reveals webroot and suggests trying absolute paths.
*/
error_reporting(0);

$param = $_GET['file'] ?? 'pages/home.php';

/* Deny obvious remote schemes */
$deny = ['http://','https://','ftp://','phar://','data://'];
foreach ($deny as $bad) {
  if (stripos($param, $bad) !== false) {
    http_response_code(400);
    die('Protocol not allowed.');
  }
}

/* Prevent direct reads of the flag (now under webroot) */
if (stripos($param, 'flag') !== false) {
  http_response_code(404);
  die('Not found.');
}

/* Resolve target (absolute and relative allowed) */
$target = $param;

/* Include and capture output */
ob_start();
$ok = @include($target);
$out = ob_get_clean();

if ($ok === false && $out === '') {
  http_response_code(404);
  die(
    'File not found under webroot: ' . dirname(__FILE__) .
    "<br><small>Hint: Try absolute paths like <code>/etc/passwd</code> or <code>/etc/nginx/nginx.conf</code>.</small>"
  );
}

echo $out;
