// --- Config (hard-coded for this static challenge page) ---
const CORRECT_FLAG = "CTF{wrong_extension_is_fun}";

// --- Elements ---
const input = document.getElementById("flagInput");
const btn = document.getElementById("submitBtn");
const statusEl = document.getElementById("status");
const confettiCanvas = document.getElementById("confetti");
const ctx = confettiCanvas.getContext("2d");

// --- Init ---
function sizeCanvas(){
  confettiCanvas.width = window.innerWidth;
  confettiCanvas.height = window.innerHeight;
}
window.addEventListener("resize", sizeCanvas);
sizeCanvas();

// --- UI helpers ---
function setStatus(type, msg){
  statusEl.className = "status " + (type === "success" ? "success" : "error");
  statusEl.textContent = msg;
}

function wiggle(el){
  el.style.transition = "transform 60ms ease";
  let i = 0;
  const seq = [-4,4,-3,3,-2,2,-1,1,0];
  const t = setInterval(()=>{
    el.style.transform = `translateX(${seq[i]}px)`;
    i++; if(i>=seq.length){ clearInterval(t); }
  }, 40);
}

// --- Flag check ---
function checkFlag(){
  const value = (input.value || "").trim();
  if(!value){
    setStatus("error","Please enter a flag.");
    input.focus();
    return;
  }
  if(value === CORRECT_FLAG){
    setStatus("success","Correct! Nicely done.");
    launchConfetti();
  }else{
    setStatus("error","Incorrect flag. Try again.");
    wiggle(input);
  }
}

btn.addEventListener("click", checkFlag);
input.addEventListener("keydown", (e)=>{ if(e.key === "Enter") checkFlag(); });

// --- Confetti (lightweight) ---
let confettiPieces = [];

function launchConfetti(){
  confettiCanvas.style.display = "block";
  confettiPieces = [];
  const count = Math.min(220, Math.floor(window.innerWidth * 0.25));
  for(let i=0;i<count;i++){
    confettiPieces.push({
      x: Math.random() * confettiCanvas.width,
      y: -10 - Math.random()*40,
      w: 6 + Math.random()*6,
      h: 10 + Math.random()*10,
      vx: -1 + Math.random()*2,
      vy: 2 + Math.random()*2,
      rot: Math.random()*Math.PI,
      vr: -0.15 + Math.random()*0.3,
      o: 0.75 + Math.random()*0.25
    });
  }
  animateConfetti();
  setTimeout(()=> { confettiCanvas.style.display = "none"; }, 2500);
}

function animateConfetti(){
  if(confettiCanvas.style.display !== "block") return;
  ctx.clearRect(0,0,confettiCanvas.width, confettiCanvas.height);
  for(const p of confettiPieces){
    p.x += p.vx; p.y += p.vy; p.rot += p.vr;
    ctx.save();
    ctx.globalAlpha = p.o;
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot);
    const hue = Math.floor((p.x + p.y) % 360);
    ctx.fillStyle = `hsl(${hue} 80% 60%)`;
    ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
    ctx.restore();
  }
  requestAnimationFrame(animateConfetti);
}
