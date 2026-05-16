const panel = document.querySelector("#chat-panel");
const historyBox = document.querySelector("#chat-history");
let chatHistory = JSON.parse(sessionStorage.getItem("pharmaChat") || "[]");

function paintChat(){
  if(!historyBox) return;
  historyBox.innerHTML = chatHistory.map(m => `<div class="msg ${m.role}">${m.text}</div>`).join("");
  historyBox.scrollTop = historyBox.scrollHeight;
}
async function sendChat(text){
  if(!text.trim()) return;
  chatHistory.push({role:"user", text});
  chatHistory.push({role:"ai", text:"<span class='typing'>...</span>"});
  paintChat();
  const res = await fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text,history:chatHistory,quarter:state.quarter,year:state.year})});
  const data = await res.json();
  chatHistory.pop();
  chatHistory.push({role:"ai", text:data.answer});
  sessionStorage.setItem("pharmaChat", JSON.stringify(chatHistory.slice(-20)));
  paintChat();
}
document.querySelector("#chat-toggle")?.addEventListener("click", () => panel.classList.toggle("open"));
document.querySelector("#chat-nudge-open")?.addEventListener("click", () => {
  panel.classList.add("open");
  document.querySelector("#chat-nudge")?.classList.add("hide");
  localStorage.setItem("chatNudgeClosed", "1");
});
document.querySelector("#chat-nudge-close")?.addEventListener("click", () => {
  document.querySelector("#chat-nudge")?.classList.add("hide");
  localStorage.setItem("chatNudgeClosed", "1");
});
if(localStorage.getItem("chatNudgeClosed") === "1"){
  document.querySelector("#chat-nudge")?.classList.add("hide");
}
document.querySelector("#chat-form")?.addEventListener("submit", e => { e.preventDefault(); const input = document.querySelector("#chat-input"); sendChat(input.value); input.value=""; });
document.querySelectorAll(".chips button").forEach(b => b.addEventListener("click", () => sendChat(b.textContent)));
paintChat();
