<?php /* Front page */ ?>
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>TinyCMS</title>
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <header><h1>TinyCMS</h1></header>
  <nav>
    <!-- Intentionally shows the vulnerable param usage -->
    <a href="/include.php?file=pages/home.php">Home</a>
    <a href="/include.php?file=pages/about.php">About</a>
  </nav>
  <main>
    <p>Welcome to TinyCMS demo.</p>
    <p>Pages are stitched together dynamically.</p>
  </main>
  <footer><small>© TinyCMS</small></footer>
</body>
</html>
