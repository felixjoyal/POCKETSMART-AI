function money(v){return new Intl.NumberFormat("en-IN",{style:"currency",currency:"INR",maximumFractionDigits:0}).format(v||0)}
function escapeHtml(v){return String(v??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&#039;")}
function formValue(id){return document.getElementById(id)?.value?.trim()||""}
function renderResult(r,targetId){
 const t=document.getElementById(targetId); if(!t)return;
 let h=`<div class="card"><h2>${escapeHtml(r.title)}</h2><div class="stats">
 <div class="stat">Budget<strong>${money(r.budget)}</strong></div>
 <div class="stat">Estimated total<strong>${money(r.estimated_total)}</strong></div>
 <div class="stat">Remaining<strong>${money(r.remaining_budget)}</strong></div></div>
 <div class="summary" style="margin-top:15px">${escapeHtml(r.summary)}</div></div>`;
 for(const s of r.sections||[]){h+=`<div class="card" style="margin-top:16px"><h3>${escapeHtml(s.category)}</h3><p class="muted">Planned allocation: ${money(s.allocation)}</p>`;
  for(const i of s.items||[]){h+=`<div class="item"><div class="item-top"><div><h3>${escapeHtml(i.name)}</h3><p>${escapeHtml(i.description)}</p></div><div class="price">${money(i.estimated_price*i.quantity)}</div></div>
  <div class="tags"><span class="tag">${escapeHtml(i.platform)}</span><span class="tag">Qty: ${escapeHtml(i.quantity)}</span><span class="tag">${escapeHtml(i.category)}</span></div>
  <p class="muted"><strong>Why:</strong> ${escapeHtml(i.reason)}</p><a class="btn secondary" target="_blank" rel="noopener noreferrer" href="${escapeHtml(i.url||"#")}">Search on ${escapeHtml(i.platform)}</a></div>`}
  h+=`</div>`}
 if((r.tips||[]).length){h+=`<div class="card" style="margin-top:16px"><h3>Planning tips</h3><ul>${r.tips.map(x=>`<li>${escapeHtml(x)}</li>`).join("")}</ul><p class="muted">${escapeHtml(r.disclaimer)}</p></div>`}
 t.innerHTML=h;t.scrollIntoView({behavior:"smooth",block:"start"})
}
async function postJson(url,data,targetId,button){
 const l=document.querySelector(".loading");if(l)l.classList.add("show");if(button)button.disabled=true;
 try{const res=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});const p=await res.json();if(!res.ok)throw new Error(p.detail||"Request failed.");renderResult(p,targetId)}
 catch(e){document.getElementById(targetId).innerHTML=`<div class="alert">${escapeHtml(e.message)}</div>`}
 finally{if(l)l.classList.remove("show");if(button)button.disabled=false}
}
