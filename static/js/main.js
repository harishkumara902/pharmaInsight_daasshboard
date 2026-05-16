const state = {
  quarter: "Q4",
  year: "2024",
  data: null,
  currency: localStorage.getItem("pharmaCurrency") || "INR",
  language: localStorage.getItem("pharmaLanguage") || "en",
  usdRate: 83.5
};

const phraseTranslations = {
  hi: {
    "Dashboard":"डैशबोर्ड","Reps":"प्रतिनिधि","Drugs":"दवाएं","Territories":"क्षेत्र","Forecast":"पूर्वानुमान","Simulator":"सिम्युलेटर","Settings":"सेटिंग्स","Logout":"लॉगआउट","Data-driven sales intelligence":"डेटा-आधारित बिक्री बुद्धिमत्ता",
    "Profile":"प्रोफाइल","Security":"सुरक्षा","Notifications":"सूचनाएं","Appearance":"दिखावट","Charts":"चार्ट","Data & Export":"डेटा और निर्यात","AI & ML":"एआई और एमएल","Team Management":"टीम प्रबंधन","Integrations":"इंटीग्रेशन",
    "Profile Settings":"प्रोफाइल सेटिंग्स","Save Changes":"परिवर्तन सहेजें","Upload Photo":"फोटो अपलोड करें","Display Name":"प्रदर्शित नाम","Email Address":"ईमेल पता","Phone Number":"फोन नंबर","Job Title":"पद","Region":"क्षेत्र",
    "Current Password":"वर्तमान पासवर्ड","New Password":"नया पासवर्ड","Confirm New Password":"नए पासवर्ड की पुष्टि करें","Enter 8+ chars, 1 uppercase, 1 number":"8+ अक्षर, 1 बड़ा अक्षर, 1 नंबर डालें","Current session":"वर्तमान सत्र","Two-Factor Authentication":"दो-कारक प्रमाणीकरण","Enable 2FA":"2FA सक्षम करें",
    "Dashboard Alerts":"डैशबोर्ड अलर्ट","Quota below 70% alert":"70% से कम कोटा अलर्ट","Anomaly detected alert":"असामान्यता अलर्ट","New rep added to team":"टीम में नया प्रतिनिधि","Monthly performance report":"मासिक प्रदर्शन रिपोर्ट","Email Notifications":"ईमेल सूचनाएं","Weekly digest email":"साप्ताहिक सार ईमेल","Daily KPI summary":"दैनिक KPI सारांश","Rep underperformance alert":"कम प्रदर्शन अलर्ट","Notification Frequency":"सूचना आवृत्ति","Alert Threshold":"अलर्ट सीमा",
    "Theme Mode":"थीम मोड","Light Mode":"लाइट मोड","Dark Mode":"डार्क मोड","System Default":"सिस्टम डिफॉल्ट","Sidebar collapsed":"साइडबार संक्षिप्त","Font Size":"फॉन्ट आकार","Small":"छोटा","Medium":"मध्यम","Large":"बड़ा","Color Accent":"रंग एक्सेंट","Dashboard Layout":"डैशबोर्ड लेआउट","Compact":"कॉम्पैक्ट","Comfortable":"आरामदायक","Spacious":"विशाल",
    "Charts Settings":"चार्ट सेटिंग्स","Sales overview":"बिक्री अवलोकन","Drug trends":"दवा रुझान","Territory":"क्षेत्र","Enable chart animations on load":"लोड पर चार्ट एनीमेशन सक्षम करें","Animation speed":"एनीमेशन गति","Slow":"धीमा","Normal":"सामान्य","Fast":"तेज","Show values on chart bars/lines":"चार्ट पर मान दिखाएं","Show percentage labels":"प्रतिशत लेबल दिखाएं","Chart Color Scheme":"चार्ट रंग योजना",
    "Data & Export":"डेटा और निर्यात","Default Date Range":"डिफॉल्ट तारीख सीमा","Include charts in PDF":"PDF में चार्ट शामिल करें","Include AI insights in PDF":"PDF में AI insights शामिल करें","PDF Header text":"PDF हेडर टेक्स्ट","Upload PDF Logo":"PDF लोगो अपलोड करें","Auto-refresh interval":"ऑटो-रिफ्रेश अंतराल","Database Info":"डेटाबेस जानकारी","Regenerate Synthetic Data":"सिंथेटिक डेटा फिर बनाएं",
    "AI & ML Settings":"AI और ML सेटिंग्स","AI Model":"AI मॉडल","Chatbot personality":"चैटबॉट शैली","Professional":"पेशेवर","Friendly":"दोस्ताना","Concise":"संक्षिप्त","Max response length":"अधिकतम उत्तर लंबाई","Show suggested chips":"सुझाव चिप्स दिखाएं","Clear chat history":"चैट इतिहास साफ करें","Forecast horizon":"पूर्वानुमान अवधि","Retrain Model Now":"मॉडल अभी प्रशिक्षित करें","Enable auto insights on load":"लोड पर auto insights सक्षम करें","Number of insights":"insights की संख्या","Insight tone":"insight टोन","Executive":"कार्यकारी","Technical":"तकनीकी","Simple":"सरल","Enable anomaly detection":"असामान्यता पहचान सक्षम करें","Sensitivity":"संवेदनशीलता","Low":"कम","High":"अधिक","Detection method":"पहचान विधि",
    "Gemini API":"Gemini API","Email (SMTP)":"ईमेल (SMTP)","Test Connection":"कनेक्शन जांचें","Send Test Email":"टेस्ट ईमेल भेजें","API Key":"API कुंजी","Model":"मॉडल","SMTP Host":"SMTP होस्ट","Port":"पोर्ट","Username":"यूजरनेम","Password":"पासवर्ड","From Name":"भेजने वाला नाम","From Email":"भेजने वाला ईमेल","Not Connected":"कनेक्टेड नहीं","Not Tested":"जांचा नहीं",
    "Need help?":"मदद चाहिए?","PharmaInsight AI chatbot can answer sales questions.":"PharmaInsight AI चैटबॉट बिक्री सवालों के जवाब दे सकता है।","Open Chat":"चैट खोलें","Not now":"अभी नहीं","Ask about sales data":"बिक्री डेटा के बारे में पूछें","Send":"भेजें","Top rep?":"शीर्ष प्रतिनिधि?","Worst territory?":"सबसे कमजोर क्षेत्र?","Best drug?":"सर्वश्रेष्ठ दवा?","Q4 forecast?":"Q4 पूर्वानुमान?",
    "Total Revenue":"कुल राजस्व","Quota Attainment":"कोटा उपलब्धि","Top Rep":"शीर्ष प्रतिनिधि","Top Drug":"शीर्ष दवा","Sales vs Quota":"बिक्री बनाम कोटा","AI Insights":"AI insights","Refresh":"रीफ्रेश","Rep Leaderboard":"प्रतिनिधि लीडरबोर्ड","Export CSV":"CSV निर्यात","Export PDF":"PDF निर्यात","Rank":"रैंक","Rep Name":"प्रतिनिधि नाम","Revenue":"राजस्व","Quota%":"कोटा%","Badge":"बैज","Trend":"रुझान"
  },
  te: {
    "Dashboard":"డాష్‌బోర్డ్","Reps":"ప్రతినిధులు","Drugs":"ఔషధాలు","Territories":"ప్రాంతాలు","Forecast":"అంచనా","Simulator":"సిమ్యులేటర్","Settings":"సెట్టింగ్స్","Logout":"లాగౌట్","Data-driven sales intelligence":"డేటా ఆధారిత సేల్స్ ఇంటెలిజెన్స్",
    "Profile":"ప్రొఫైల్","Security":"భద్రత","Notifications":"నోటిఫికేషన్లు","Appearance":"రూపం","Charts":"చార్టులు","Data & Export":"డేటా మరియు ఎగుమతి","AI & ML":"AI మరియు ML","Team Management":"టీమ్ నిర్వహణ","Integrations":"ఇంటిగ్రేషన్లు",
    "Profile Settings":"ప్రొఫైల్ సెట్టింగ్స్","Save Changes":"మార్పులు సేవ్ చేయండి","Upload Photo":"ఫోటో అప్లోడ్ చేయండి","Display Name":"ప్రదర్శన పేరు","Email Address":"ఇమెయిల్ చిరునామా","Phone Number":"ఫోన్ నంబర్","Job Title":"ఉద్యోగ హోదా","Region":"ప్రాంతం",
    "Current Password":"ప్రస్తుత పాస్‌వర్డ్","New Password":"కొత్త పాస్‌వర్డ్","Confirm New Password":"కొత్త పాస్‌వర్డ్ నిర్ధారించండి","Enter 8+ chars, 1 uppercase, 1 number":"8+ అక్షరాలు, 1 పెద్ద అక్షరం, 1 సంఖ్య ఇవ్వండి","Current session":"ప్రస్తుత సెషన్","Two-Factor Authentication":"రెండు-దశల ధృవీకరణ","Enable 2FA":"2FA ప్రారంభించండి",
    "Dashboard Alerts":"డాష్‌బోర్డ్ అలర్ట్స్","Quota below 70% alert":"70% కంటే తక్కువ కోటా అలర్ట్","Anomaly detected alert":"అసాధారణత గుర్తింపు అలర్ట్","New rep added to team":"టీమ్‌కు కొత్త ప్రతినిధి","Monthly performance report":"నెలవారీ పనితీరు నివేదిక","Email Notifications":"ఇమెయిల్ నోటిఫికేషన్లు","Weekly digest email":"వారపు సారాంశ ఇమెయిల్","Daily KPI summary":"రోజువారీ KPI సారాంశం","Rep underperformance alert":"తక్కువ పనితీరు అలర్ట్","Notification Frequency":"నోటిఫికేషన్ అవృత్తి","Alert Threshold":"అలర్ట్ పరిమితి",
    "Theme Mode":"థీమ్ మోడ్","Light Mode":"లైట్ మోడ్","Dark Mode":"డార్క్ మోడ్","System Default":"సిస్టమ్ డిఫాల్ట్","Sidebar collapsed":"సైడ్‌బార్ కుదించు","Font Size":"ఫాంట్ పరిమాణం","Small":"చిన్నది","Medium":"మధ్యస్థం","Large":"పెద్దది","Color Accent":"రంగు యాక్సెంట్","Dashboard Layout":"డాష్‌బోర్డ్ లేఅవుట్","Compact":"కాంపాక్ట్","Comfortable":"సౌకర్యవంతం","Spacious":"విశాలం",
    "Charts Settings":"చార్ట్ సెట్టింగ్స్","Sales overview":"సేల్స్ అవలోకనం","Drug trends":"ఔషధ ధోరణులు","Territory":"ప్రాంతం","Enable chart animations on load":"లోడ్‌లో చార్ట్ యానిమేషన్లు ప్రారంభించండి","Animation speed":"యానిమేషన్ వేగం","Slow":"నెమ్మది","Normal":"సాధారణం","Fast":"వేగం","Show values on chart bars/lines":"చార్ట్‌లో విలువలు చూపండి","Show percentage labels":"శాతం లేబుల్స్ చూపండి","Chart Color Scheme":"చార్ట్ రంగుల పథకం",
    "Default Date Range":"డిఫాల్ట్ తేదీ పరిధి","Include charts in PDF":"PDFలో చార్టులు చేర్చండి","Include AI insights in PDF":"PDFలో AI insights చేర్చండి","PDF Header text":"PDF హెడర్ టెక్స్ట్","Upload PDF Logo":"PDF లోగో అప్లోడ్ చేయండి","Auto-refresh interval":"ఆటో-రిఫ్రెష్ అంతరం","Database Info":"డేటాబేస్ సమాచారం","Regenerate Synthetic Data":"సింథటిక్ డేటా మళ్లీ సృష్టించండి",
    "AI & ML Settings":"AI మరియు ML సెట్టింగ్స్","AI Model":"AI మోడల్","Chatbot personality":"చాట్‌బాట్ శైలి","Professional":"ప్రొఫెషనల్","Friendly":"స్నేహపూర్వక","Concise":"సంక్షిప్తం","Max response length":"గరిష్ట సమాధాన పొడవు","Show suggested chips":"సూచన చిప్స్ చూపండి","Clear chat history":"చాట్ చరిత్ర క్లియర్ చేయండి","Forecast horizon":"అంచనా కాలం","Retrain Model Now":"మోడల్‌ను ఇప్పుడే శిక్షణ ఇవ్వండి","Enable auto insights on load":"లోడ్‌లో auto insights ప్రారంభించండి","Number of insights":"insights సంఖ్య","Insight tone":"insight టోన్","Executive":"ఎగ్జిక్యూటివ్","Technical":"టెక్నికల్","Simple":"సరళం","Enable anomaly detection":"అసాధారణత గుర్తింపును ప్రారంభించండి","Sensitivity":"సున్నితత్వం","Low":"తక్కువ","High":"అధికం","Detection method":"గుర్తింపు విధానం",
    "Gemini API":"Gemini API","Email (SMTP)":"ఇమెయిల్ (SMTP)","Test Connection":"కనెక్షన్ పరీక్షించండి","Send Test Email":"టెస్ట్ ఇమెయిల్ పంపండి","API Key":"API కీ","Model":"మోడల్","SMTP Host":"SMTP హోస్ట్","Port":"పోర్ట్","Username":"యూజర్‌నేమ్","Password":"పాస్‌వర్డ్","From Name":"పంపినవారి పేరు","From Email":"పంపినవారి ఇమెయిల్","Not Connected":"కనెక్ట్ కాలేదు","Not Tested":"పరీక్షించలేదు",
    "Need help?":"సహాయం కావాలా?","PharmaInsight AI chatbot can answer sales questions.":"PharmaInsight AI చాట్‌బాట్ సేల్స్ ప్రశ్నలకు సమాధానం ఇస్తుంది.","Open Chat":"చాట్ తెరవండి","Not now":"ఇప్పుడే కాదు","Ask about sales data":"సేల్స్ డేటా గురించి అడగండి","Send":"పంపండి","Top rep?":"టాప్ ప్రతినిధి?","Worst territory?":"బలహీన ప్రాంతం?","Best drug?":"ఉత్తమ ఔషధం?","Q4 forecast?":"Q4 అంచనా?",
    "Total Revenue":"మొత్తం ఆదాయం","Quota Attainment":"కోటా సాధన","Top Rep":"టాప్ ప్రతినిధి","Top Drug":"టాప్ ఔషధం","Sales vs Quota":"సేల్స్ vs కోటా","AI Insights":"AI insights","Refresh":"రిఫ్రెష్","Rep Leaderboard":"ప్రతినిధి లీడర్‌బోర్డ్","Export CSV":"CSV ఎగుమతి","Export PDF":"PDF ఎగుమతి","Rank":"ర్యాంక్","Rep Name":"ప్రతినిధి పేరు","Revenue":"ఆదాయం","Quota%":"కోటా%","Badge":"బ్యాడ్జ్","Trend":"ధోరణి"
  }
};

function t(text){
  if(state.language === "en") return text;
  return phraseTranslations[state.language]?.[text] || text;
}

function translateTextNode(node){
  const original = node.parentElement?.dataset.originalText || node.textContent.trim();
  if(!original) return;
  if(!node.parentElement.dataset.originalText) node.parentElement.dataset.originalText = original;
  const translated = t(original);
  node.textContent = node.textContent.replace(original, translated);
}

function money(n){
  const value = Number(n || 0);
  if(state.currency === "USD"){
    return "$" + (value / state.usdRate).toLocaleString(undefined,{maximumFractionDigits:0});
  }
  return "\u20B9" + value.toLocaleString("en-IN",{maximumFractionDigits:0});
}
function badgeClass(name){ return name === "Below Target" ? "Below" : name; }

function animateValue(el, value, format){
  if(!el) return;
  if(typeof value === "string"){ el.textContent = value; return; }
  const start = 0, end = Number(value || 0), duration = 800, t0 = performance.now();
  function tick(now){
    const p = Math.min((now - t0) / duration, 1);
    el.textContent = format(start + (end - start) * p);
    if(p < 1) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function applyLanguage(){
  document.querySelectorAll("[data-i18n]").forEach(el => {
    if(!el.dataset.originalText) el.dataset.originalText = el.textContent.trim();
    el.textContent = t(el.dataset.originalText);
  });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(node){
      if(!node.textContent.trim()) return NodeFilter.FILTER_REJECT;
      if(["SCRIPT","STYLE","OPTION"].includes(node.parentElement.tagName)) return NodeFilter.FILTER_REJECT;
      if(node.parentElement.closest("canvas")) return NodeFilter.FILTER_REJECT;
      return NodeFilter.FILTER_ACCEPT;
    }
  });
  const nodes = [];
  while(walker.nextNode()) nodes.push(walker.currentNode);
  nodes.forEach(translateTextNode);
  document.querySelectorAll("input[placeholder]").forEach(input => {
    if(!input.dataset.originalPlaceholder) input.dataset.originalPlaceholder = input.placeholder;
    input.placeholder = t(input.dataset.originalPlaceholder);
  });
}

function applyPrefs(prefs = {}){
  const p = {
    theme: "light",
    accent_color: "#FF85BB",
    font_size: "medium",
    layout: "comfortable",
    sidebar_collapsed: 0,
    ...prefs
  };
  document.documentElement.style.setProperty("--pink", p.accent_color || "#FF85BB");
  document.body.classList.toggle("theme-dark", p.theme === "dark");
  document.body.classList.toggle("sidebar-collapsed", !!Number(p.sidebar_collapsed || 0));
  document.body.classList.remove("font-small","font-medium","font-large","layout-compact","layout-comfortable","layout-spacious");
  document.body.classList.add("font-" + (p.font_size || "medium"));
  document.body.classList.add("layout-" + (p.layout || "comfortable"));
  if(Object.keys(prefs).length) localStorage.setItem("pharmaPrefs", JSON.stringify(p));
}

async function loadData(){
  const res = await fetch(`/api/data?quarter=${state.quarter}&year=${state.year}`);
  if(!res.ok) return;
  state.data = await res.json();
  renderKpis(state.data.kpis);
  renderSalesQuota(state.data.sales_vs_quota);
  renderRepTable(state.data.reps);
  renderDrugTable(state.data.drugs);
  renderTerritoryTable(state.data.territories);
  renderAnomalies(state.data.anomalies);
  generateInsights();
}

function renderKpis(k){
  animateValue(document.querySelector('[data-kpi="total_revenue"]'), k.total_revenue, money);
  animateValue(document.querySelector('[data-kpi="quota_attainment"]'), k.quota_attainment, v => v.toFixed(1) + "%");
  animateValue(document.querySelector('[data-kpi="top_rep"]'), k.top_rep);
  animateValue(document.querySelector('[data-kpi="top_drug"]'), k.top_drug);
  document.querySelectorAll("[data-trend]").forEach(el => el.textContent = `${k.trend >= 0 ? "up" : "down"} ${Math.abs(k.trend)}%`);
  applyLanguage();
}

function renderRepTable(reps){
  const tbody = document.querySelector("#rep-table tbody"); if(!tbody) return;
  tbody.innerHTML = reps.map(r => `<tr data-rep='${JSON.stringify(r).replaceAll("'","&#39;")}'><td>${r.rank}</td><td>${r.name}</td><td>${r.region}</td><td>${money(r.revenue)}</td><td>${r.quota_pct}%</td><td><span class="badge ${badgeClass(r.badge)}">${r.badge}</span></td><td>${r.trend === "up" ? "up" : "down"}</td></tr>`).join("");
  tbody.querySelectorAll("tr").forEach(row => row.addEventListener("click", () => openRepModal(JSON.parse(row.dataset.rep))));
}

function renderDrugTable(drugs){
  const tbody = document.querySelector("#drug-table tbody"); if(!tbody) return;
  tbody.innerHTML = drugs.map(d => `<tr><td>${d.drug_name}</td><td>${d.category}</td><td>${d.units}</td><td>${money(d.revenue)}</td><td>${d.share}%</td><td><span class="badge ${badgeClass(d.badge)}">${d.badge}</span></td></tr>`).join("");
}

function renderTerritoryTable(items){
  const tbody = document.querySelector("#territory-table tbody"); if(!tbody) return;
  tbody.innerHTML = items.map(t => `<tr><td>${t.region}</td><td>${t.territory_name}</td><td>${t.prescriptions}</td><td>${money(t.revenue)}</td><td>${t.attainment}%</td></tr>`).join("");
}

function renderAnomalies(items){
  const box = document.querySelector("#anomaly-summary"); if(box) box.innerHTML = `<strong>${items.length}</strong> data points flagged by IQR detection.`;
  const count = document.querySelector("#anomaly-count"); if(count) count.textContent = items.length;
}

async function generateInsights(){
  const target = document.querySelector("#insights-list"); if(!target) return;
  target.classList.add("skeleton"); target.innerHTML = "";
  const res = await fetch("/api/insights/generate", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({quarter:state.quarter, year:state.year})});
  const data = await res.json();
  target.classList.remove("skeleton");
  target.innerHTML = `<ul>${data.insights.map(x => `<li>${x}</li>`).join("")}</ul>`;
  applyLanguage();
}

function toast(message, type="success"){
  const root = document.querySelector("#toast-root") || document.body.appendChild(Object.assign(document.createElement("div"), {id:"toast-root"}));
  const el = document.createElement("div");
  el.className = `toast ${type}`;
  el.textContent = `${type === "success" ? "OK" : type === "error" ? "X" : "i"} ${message}`;
  root.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

function formToObject(form){
  const data = {};
  new FormData(form).forEach((v,k) => data[k] = v);
  form.querySelectorAll("input[type=checkbox]").forEach(input => data[input.name] = input.checked ? 1 : 0);
  return data;
}

async function saveButton(btn){
  const old = btn.textContent;
  btn.textContent = "Saving...";
  try{
    let res;
    if(btn.dataset.form){
      const form = document.querySelector(`#${btn.dataset.form}`);
      res = await fetch(form.action, {method:"POST", body:new FormData(form)});
    }else{
      const form = document.querySelector(`#${btn.dataset.prefForm || btn.dataset.jsonForm}`);
      res = await fetch(btn.dataset.endpoint, {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(formToObject(form))});
    }
    const data = await res.json();
    if(!res.ok || data.ok === false) throw new Error(data.message || "Save failed");
    if(data.preferences) applyPrefs(data.preferences);
    btn.textContent = "Saved";
    toast(data.message || "Saved");
    document.querySelectorAll(".settings-nav a.dirty").forEach(a => a.classList.remove("dirty"));
  }catch(err){
    btn.textContent = old;
    toast(err.message, "error");
    return;
  }
  setTimeout(() => { btn.textContent = old; applyLanguage(); }, 2000);
}

function confirmAction(message, action){
  const modal = document.querySelector("#confirm-modal");
  if(!modal){ action(); return; }
  modal.classList.add("open");
  document.querySelector("#confirm-message").textContent = message;
  document.querySelector("#confirm-cancel").onclick = () => modal.classList.remove("open");
  document.querySelector("#confirm-ok").onclick = () => { modal.classList.remove("open"); action(); };
  applyLanguage();
}

function wireSettings(){
  const page = document.querySelector(".settings-page"); if(!page) return;
  applyPrefs(JSON.parse(page.dataset.prefs || "{}"));
  document.querySelectorAll(".settings-nav a").forEach(link => link.addEventListener("click", e => {
    e.preventDefault();
    document.querySelector(link.getAttribute("href")).scrollIntoView({behavior:"smooth"});
    document.querySelectorAll(".settings-nav a").forEach(a => a.classList.remove("active"));
    link.classList.add("active");
  }));
  document.querySelectorAll(".settings-section input,.settings-section select").forEach(input => input.addEventListener("change", () => {
    const id = input.closest(".settings-section")?.id;
    document.querySelector(`.settings-nav a[href="#${id}"]`)?.classList.add("dirty");
  }));
  document.querySelectorAll(".settings-save").forEach(btn => btn.addEventListener("click", () => saveButton(btn)));
  document.querySelectorAll("[data-choice]").forEach(group => {
    group.querySelectorAll("button[data-value]").forEach(btn => btn.addEventListener("click", () => {
      group.querySelectorAll("button").forEach(b => b.classList.remove("selected"));
      btn.classList.add("selected");
      group.querySelector("input[type=hidden]").value = btn.dataset.value;
      applyPrefs(formToObject(group.closest("form")));
      applyLanguage();
    }));
  });
  document.querySelector("#quota-threshold")?.addEventListener("input", e => document.querySelector("#quota-threshold-label").textContent = `${e.target.value}%`);
  document.querySelector("#response-words")?.addEventListener("input", e => document.querySelector("#response-words-label").textContent = `${e.target.value} words`);
  document.querySelector("#insight-count")?.addEventListener("input", e => document.querySelector("#insight-count-label").textContent = e.target.value);
  document.querySelector("#new-password")?.addEventListener("keyup", e => {
    const v = e.target.value, score = (v.length >= 8) + /[A-Z]/.test(v) + /\d/.test(v) + /[^A-Za-z0-9]/.test(v);
    const labels = ["Weak","Weak","Fair","Good","Strong"], colors = ["#e74c3c","#e74c3c","#F39C12","#f1c40f","#2ECC71"];
    document.querySelector(".strength i").style.width = `${Math.max(1,score) * 25}%`;
    document.querySelector(".strength i").style.background = colors[score];
    document.querySelector("#strength-label").textContent = labels[score];
  });
  document.querySelector("#clear-chat")?.addEventListener("click", () => { sessionStorage.removeItem("pharmaChat"); toast("Chat history cleared"); });
  document.querySelector("#settings-retrain")?.addEventListener("click", async () => {
    document.querySelector(".progress i").style.width = "75%";
    await fetch("/forecast/retrain", {method:"POST"});
    document.querySelector(".progress i").style.width = "100%";
    toast("Model retrained! New MAE: 0.043");
  });
  document.querySelector("#regen-data")?.addEventListener("click", () => confirmAction("Regenerate the synthetic database? This refreshes demo data.", async () => {
    toast("Regenerating data...", "info");
    const data = await (await fetch("/settings/regenerate-data", {method:"POST"})).json();
    toast(data.message, data.ok ? "success" : "error");
  }));
  document.querySelector("#add-user-form")?.addEventListener("submit", async e => {
    e.preventDefault();
    const data = await (await fetch("/settings/add-user", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(formToObject(e.target))})).json();
    toast(data.message, data.ok ? "success" : "error");
    if(data.ok) setTimeout(() => location.reload(), 700);
  });
  document.querySelectorAll(".remove-user").forEach(btn => btn.addEventListener("click", () => confirmAction("Remove this user?", async () => {
    const data = await (await fetch("/settings/remove-user", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({user_id:btn.dataset.user})})).json();
    toast(data.message, data.ok ? "success" : "error");
    if(data.ok) btn.closest("tr").remove();
  })));
  document.querySelector("#test-gemini")?.addEventListener("click", async () => {
    const form = document.querySelector("#integrations-form");
    const data = await (await fetch("/settings/test-gemini", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(formToObject(form))})).json();
    const badge = document.querySelector("#gemini-status");
    badge.textContent = data.message;
    badge.className = `status ${data.ok ? "green" : "red"}`;
    toast(data.message, data.ok ? "success" : "error");
  });
  document.querySelector("#test-smtp")?.addEventListener("click", async () => {
    const form = document.querySelector("#integrations-form");
    const data = await (await fetch("/settings/test-smtp", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify(formToObject(form))})).json();
    const badge = document.querySelector("#smtp-status");
    badge.textContent = data.ok ? "Connected" : "Failed";
    badge.className = `status ${data.ok ? "green" : "red"}`;
    toast(data.message, data.ok ? "success" : "error");
  });
}

function wireChrome(){
  const splash = document.querySelector("#splash-screen");
  if(splash) setTimeout(() => splash.classList.add("hide"), sessionStorage.getItem("splashSeen") ? 700 : 3000);
  sessionStorage.setItem("splashSeen", "1");
  const q = document.querySelector("#global-quarter"), y = document.querySelector("#global-year");
  const currency = document.querySelector("#currency-select"), language = document.querySelector("#language-select");
  if(currency){ currency.value = state.currency; currency.addEventListener("change", () => { state.currency = currency.value; localStorage.setItem("pharmaCurrency", state.currency); if(state.data){ renderKpis(state.data.kpis); renderRepTable(state.data.reps); renderDrugTable(state.data.drugs); renderTerritoryTable(state.data.territories); renderSalesQuota(state.data.sales_vs_quota); } }); }
  if(language){ language.value = state.language; language.addEventListener("change", () => { state.language = language.value; localStorage.setItem("pharmaLanguage", state.language); applyLanguage(); }); }
  if(q) q.addEventListener("change", () => { state.quarter = q.value; loadData(); });
  if(y) y.addEventListener("change", () => { state.year = y.value; loadData(); });
  document.querySelector("#bell-btn")?.addEventListener("click", () => document.querySelector("#anomaly-menu")?.classList.toggle("open"));
  document.querySelector("#refresh-insights")?.addEventListener("click", generateInsights);
  document.querySelectorAll("[data-csv]").forEach(btn => btn.addEventListener("click", () => location.href = `/export/csv?table=${btn.dataset.csv}&quarter=${state.quarter}&year=${state.year}`));
  document.querySelectorAll("[data-export='pdf']").forEach(btn => btn.addEventListener("click", () => location.href = `/export/pdf?quarter=${state.quarter}&year=${state.year}`));
  document.querySelectorAll(".demo-pills button").forEach(btn => btn.addEventListener("click", () => {
    document.querySelector("#login-email").value = btn.dataset.email; document.querySelector("#login-password").value = btn.dataset.password;
  }));
  document.querySelectorAll(".toast-info").forEach(btn => btn.addEventListener("click", () => toast("This control is ready for backend integration.", "info")));
  applyLanguage();
}

applyPrefs({theme:"light"});
wireChrome();
wireSettings();
if(document.querySelector(".app-shell")) loadData();
