// SHA-256 hashes for accepted flags (to keep plaintext out of source):
// "{log_mastery_rocks}"                -> fe624fcc1cf2a8ae6cfee31c99139a45353e7481aa4cae714d4760db4f3407ee
// "CTF{log_mastery_rocks}"             -> df970945abf6e74969404ccd968a812f1d7ddaca128b403b96cc7715b43afed8

const ACCEPTED_SHA256 = new Set([
  "fe624fcc1cf2a8ae6cfee31c99139a45353e7481aa4cae714d4760db4f3407ee",
  "df970945abf6e74969404ccd968a812f1d7ddaca128b403b96cc7715b43afed8",
]);

// Lightweight SHA-256 (Web Crypto)
async function sha256Hex(str) {
  const enc = new TextEncoder().encode(str);
  const buf = await crypto.subtle.digest("SHA-256", enc);
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
}

const form = document.getElementById("flagForm");
const input = document.getElementById("flagInput");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const guess = (input.value || "").trim();
  if (!guess) return;
  result.textContent = "Checking…";

  try {
    const hex = await sha256Hex(guess);
    if (ACCEPTED_SHA256.has(hex)) {
      result.className = "result ok";
      result.textContent = "Correct! Great work.";
    } else {
      result.className = "result no";
      result.textContent = "Not quite. Keep digging in the logs.";
    }
  } catch (err) {
    result.className = "result no";
    result.textContent = "Error while checking. Try again.";
  }
});
