<?php
// CatPaws Booking — intentionally vulnerable upload (Hard)
// Players register a cat and upload a picture. Upload handler is weak to
// double-extension + MIME spoof → allows webshell (e.g., shell.jpg.phtml).

ini_set('display_errors', 0);
ini_set('log_errors', 1);
error_reporting(E_ALL);

$uploadDir = __DIR__ . '/uploads';
$dataDir   = __DIR__ . '/data';
$dbFile    = $dataDir . '/cats.json';

if (!is_dir($uploadDir)) { mkdir($uploadDir, 0775, true); }
if (!is_dir($dataDir))   { mkdir($dataDir,   0775, true); }
if (!file_exists($dbFile)) { file_put_contents($dbFile, json_encode([])); }

$flash = [];
$cats  = json_decode(@file_get_contents($dbFile), true);
if (!is_array($cats)) { $cats = []; }

function is_image_suffix($name) {
  return (bool)preg_match('/\.(png|jpe?g|gif)$/i', $name);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
  $f = $_FILES['file'];
  $name  = trim($_POST['cat_name'] ?? '');
  $breed = trim($_POST['breed'] ?? '');
  $age   = trim($_POST['age'] ?? '');
  $notes = trim($_POST['notes'] ?? '');

  if ($f['error'] === UPLOAD_ERR_OK) {
    $origName   = $f['name'];
    $tmp        = $f['tmp_name'];
    $clientType = $f['type']; // trusting client MIME (bypass with Burp/curl)

    // 🚩 Naive checks → vulnerable to .jpg.phtml & MIME spoof
    $extOk   = (bool)preg_match('/\.(png|jpe?g|gif)/i', $origName);        // not anchored (double-ext bypass)
    $imgInfo = @getimagesize($tmp);                                        // superficial check
    $mimeOk  = (bool)preg_match('/^image\//i', $clientType);               // trusts client header

    if ($extOk || $mimeOk) {
      // Preserve full suffix (e.g., .jpg.phtml) so double-extension remains exploitable
      $safeName = preg_replace('/[^A-Za-z0-9\._-]/', '_', $origName);
      $newName  = 'up_' . bin2hex(random_bytes(4)) . '_' . $safeName;
      $dest     = $uploadDir . '/' . $newName;

      if (move_uploaded_file($tmp, $dest)) {
        $flash[] = ['ok',
          'Uploaded as <code>' . htmlspecialchars($newName, ENT_QUOTES) . '</code>' .
          ($imgInfo ? ' (image detected)' : ' (image check inconclusive)')
        ];
        // Save registration only after successful upload
        $cats[] = [
          'id'         => substr(bin2hex(random_bytes(4)), 0, 8),
          'name'       => $name !== '' ? $name : 'Unnamed Cat',
          'breed'      => $breed,
          'age'        => $age,
          'notes'      => $notes,
          'filename'   => $newName,
          'created_at' => date('c')
        ];
        @file_put_contents($dbFile, json_encode($cats, JSON_PRETTY_PRINT));
      } else {
        $flash[] = ['err', 'Failed to move the uploaded file.'];
      }
    } else {
      $flash[] = ['err', 'File rejected: not an image.'];
    }
  } else {
    $flash[] = ['err', 'Upload error code: ' . (int)$f['error']];
  }
}

// Build gallery list but hide dotfiles and any file starting with "flag"
$files = array_values(array_filter(scandir($uploadDir), function ($n) {
  if ($n === '.' || $n === '..') return false;
  if ($n[0] === '.') return false;                      // hide dotfiles like .flag
  if (preg_match('/^flag(\.|$)/i', $n)) return false;   // hide flag, flag.txt, etc.
  return true;
}));
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>CatPaws Booking</title>
  <link rel="stylesheet" href="/style.css" />
  <style>
    .thumb{display:block;width:100%;height:auto;border-radius:10px}
    .meta{font-size:12px;color:#9aa6b2;margin-top:6px;word-break:break-all}
    .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px}
  </style>
</head>
<body>
  <div class="container">
    <h1>CatPaws Booking</h1>
    <p>Register your cat and upload a photo. (Psst: our devs rushed the uploader…)</p>

    <?php foreach ($flash as $msg): ?>
      <div class="flash <?php echo $msg[0]==='err'?'err':''; ?>"><?php echo $msg[1]; ?></div>
    <?php endforeach; ?>

    <h2>Register a Cat</h2>
    <form method="post" enctype="multipart/form-data">
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;width:100%">
        <input type="text"   name="cat_name" placeholder="Cat name" />
        <input type="text"   name="breed"    placeholder="Breed" />
        <input type="number" name="age"      placeholder="Age" min="0" />
      </div>
      <textarea name="notes" placeholder="Notes (optional)" style="width:100%;margin-top:8px;height:70px"></textarea>
      <div style="display:flex;gap:12px;align-items:center;margin-top:8px">
        <input type="file" name="file" required />
        <button type="submit">Save Cat</button>
      </div>
    </form>
    <div class="note">Allowed: looks like images. Max size ~2MB. No brute force required.</div>

    <h2>Registered Cats</h2>
    <div class="grid">
      <?php if (!$cats): ?>
        <div class="card">No cats registered yet.</div>
      <?php else: foreach (array_reverse($cats) as $cat): ?>
        <?php $href = '/uploads/' . rawurlencode($cat['filename']); ?>
        <div class="card">
          <?php if (is_image_suffix($cat['filename'])): ?>
            <a href="<?php echo $href; ?>" target="_blank" title="Open original">
              <img class="thumb" src="<?php echo $href; ?>" alt="<?php echo htmlspecialchars($cat['name'], ENT_QUOTES); ?>">
            </a>
          <?php else: ?>
            <div><strong>File:</strong> <a href="<?php echo $href; ?>" target="_blank"><?php echo htmlspecialchars($cat['filename'], ENT_QUOTES); ?></a></div>
          <?php endif; ?>
          <div class="meta">
            <strong><?php echo htmlspecialchars($cat['name'], ENT_QUOTES); ?></strong>
            <?php if ($cat['breed']): ?> · <?php echo htmlspecialchars($cat['breed'], ENT_QUOTES); ?><?php endif; ?>
            <?php if ($cat['age']!==''): ?> · Age <?php echo htmlspecialchars($cat['age'], ENT_QUOTES); ?><?php endif; ?>
          </div>
          <?php if ($cat['notes']): ?><div class="meta"><?php echo htmlspecialchars($cat['notes'], ENT_QUOTES); ?></div><?php endif; ?>
        </div>
      <?php endforeach; endif; ?>
    </div>

    <h2>All Uploads</h2>
    <div class="list">
      <?php if (!$files): ?>
        <div class="card">No uploads yet.</div>
      <?php else: foreach ($files as $n): ?>
        <div class="card">
          <?php $href = '/uploads/' . rawurlencode($n); ?>
          <?php if (is_image_suffix($n)): ?>
            <a href="<?php echo $href; ?>" target="_blank" title="Open original">
              <img class="thumb" src="<?php echo $href; ?>" alt="<?php echo htmlspecialchars($n, ENT_QUOTES); ?>">
            </a>
            <div class="meta"><?php echo htmlspecialchars($n, ENT_QUOTES); ?></div>
          <?php else: ?>
            <div><strong>Name:</strong> <a href="<?php echo $href; ?>" target="_blank"><?php echo htmlspecialchars('/uploads/'.$n, ENT_QUOTES); ?></a></div>
          <?php endif; ?>
        </div>
      <?php endforeach; endif; ?>
    </div>

    <hr style="margin:24px 0;border:0;border-top:1px solid #1d2632" />
    <p class="note">Hint: Filenames and Content-Type headers matter more than you think. 🐾</p>
  </div>
</body>
</html>
