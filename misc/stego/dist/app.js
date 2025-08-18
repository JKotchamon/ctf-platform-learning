(function () {
  // Hard-coded target as requested
  const CORRECT_FLAG = "CTF{hello_stego}";

  const $in = document.getElementById("flagInput");
  const $btn = document.getElementById("submitBtn");
  const $out = document.getElementById("result");

  function check() {
    const v = ($in.value || "").trim();
    if (!v) {
      $out.textContent = "Please enter a flag.";
      $out.className = "msg center bad";
      return;
    }
    if (v === CORRECT_FLAG) {
      $out.textContent = "Correct! Nicely done.";
      $out.className = "msg center ok";
    } else {
      $out.textContent = "Not quite. Keep listening to the quiet bits.";
      $out.className = "msg center bad";
    }
  }

  $btn.addEventListener("click", check);
  $in.addEventListener("keydown", (e) => { if (e.key === "Enter") check(); });
})();
