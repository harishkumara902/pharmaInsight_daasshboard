let salesChart, sparkChart, forecastChart, simChart;

function renderSalesQuota(data){
  const canvas = document.querySelector("#salesQuotaChart"); if(!canvas) return;
  const labels = Object.keys(data);
  const actual = labels.map(q => data[q].actual);
  const quota = labels.map(q => data[q].quota);
  const attainment = labels.map(q => data[q].attainment);
  const config = {
    type:"bar",
    data:{labels,datasets:[{label:"Actual",backgroundColor:"#021A54",data:actual},{label:"Quota",backgroundColor:"#FF85BB",data:quota}]},
    options:{responsive:true,onClick:(e,els)=>{if(els.length){state.quarter=labels[els[0].index];document.querySelector("#global-quarter").value=state.quarter;loadData();}},plugins:{legend:{position:"bottom"},tooltip:{callbacks:{afterLabel:(ctx)=>ctx.datasetIndex===0?`Attainment: ${attainment[ctx.dataIndex]}%`:""}}},scales:{y:{grid:{color:"#F5F5F5"}},x:{grid:{color:"#F5F5F5"}}}}
  };
  if(salesChart){ salesChart.data = config.data; salesChart.options = config.options; salesChart.update(); }
  else salesChart = new Chart(canvas, config);
}

function openRepModal(rep){
  const modal = document.querySelector("#rep-modal"); if(!modal) return;
  document.querySelector("#modal-name").textContent = rep.name;
  document.querySelector("#modal-meta").textContent = `${rep.region} | ${money(rep.revenue)} | ${rep.quota_pct}% quota`;
  modal.classList.add("open");
  const ctx = document.querySelector("#repSparkline");
  if(sparkChart) sparkChart.destroy();
  sparkChart = new Chart(ctx,{type:"line",data:{labels:["Q1","Q2","Q3","Q4"],datasets:[{label:"Revenue",data:rep.trend_points,borderColor:"#FF85BB",backgroundColor:"#FFCEE3",fill:true,tension:.35}]},options:{plugins:{legend:{display:false}},scales:{y:{grid:{color:"#F5F5F5"}},x:{grid:{color:"#F5F5F5"}}}}});
}
document.addEventListener("click", e => { if(e.target.matches(".modal-close")) e.target.closest(".modal").classList.remove("open"); });

async function loadForecast(){
  const canvas = document.querySelector("#forecastChart"); if(!canvas) return;
  const drug = document.querySelector("#drug-select").value, region = document.querySelector("#region-select").value;
  const data = await (await fetch(`/api/forecast?drug_id=${drug}&region=${region}`)).json();
  const cfg = {type:"line",data:{labels:data.labels,datasets:[{label:"Historical actual",data:data.actual,borderColor:"#021A54",backgroundColor:"#FFCEE3",tension:.35},{label:"Forecast",data:data.forecast,borderColor:"#FF85BB",borderDash:[8,5],tension:.35}]},options:{plugins:{legend:{position:"bottom"}},scales:{y:{grid:{color:"#F5F5F5"}},x:{grid:{color:"#F5F5F5"}}}}};
  if(forecastChart){ forecastChart.data = cfg.data; forecastChart.update(); } else forecastChart = new Chart(canvas,cfg);
  document.querySelector("#mae").textContent = data.metrics.mae; document.querySelector("#rmse").textContent = data.metrics.rmse; document.querySelector("#r2").textContent = data.metrics.r2;
}
document.querySelector("#drug-select")?.addEventListener("change", loadForecast);
document.querySelector("#region-select")?.addEventListener("change", loadForecast);
document.querySelector("#retrain-btn")?.addEventListener("click", async e => { e.target.textContent="Training..."; await fetch("/forecast/retrain",{method:"POST"}); e.target.textContent="Retrain"; loadForecast(); });
loadForecast();

async function loadSim(){
  const canvas = document.querySelector("#simChart"); if(!canvas) return;
  const q = document.querySelector("#quota-slider").value, m = document.querySelector("#marketing-slider").value;
  document.querySelector("#quota-val").textContent = `${q}%`; document.querySelector("#marketing-val").textContent = `${m}%`;
  const data = await (await fetch(`/api/simulator?quota=${q}&marketing=${m}&quarter=${state.quarter}`)).json();
  document.querySelector("#hit-target").textContent = data.hit_target;
  const cfg = {type:"bar",data:{labels:["Before","After"],datasets:[{label:"Projected attainment",data:[data.before,data.after],backgroundColor:["#021A54","#FF85BB"]}]},options:{plugins:{legend:{display:false}},scales:{y:{grid:{color:"#F5F5F5"}}}}};
  if(simChart){ simChart.data = cfg.data; simChart.update(); } else simChart = new Chart(canvas,cfg);
}
document.querySelector("#quota-slider")?.addEventListener("input", loadSim);
document.querySelector("#marketing-slider")?.addEventListener("input", loadSim);
loadSim();
