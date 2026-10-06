const form=document.getElementById("studentForm");
const result=document.getElementById("result");
const errorBox=document.getElementById("error");
const btn=document.getElementById("predictBtn");

form.addEventListener("submit",async(e)=>{
  e.preventDefault();
  errorBox.classList.add("hidden");
  result.classList.add("hidden");
  btn.disabled=true;
  btn.innerHTML="Analyzing Student Data…";
  const data={};
  new FormData(form).forEach((v,k)=>{
    const numeric=["Age","Class","Study_Hours_Per_Day","Attendance_Percentage","Math_Score","Science_Score","English_Score","Previous_Year_Score"];
    data[k]=numeric.includes(k)?Number(v):v;
  });
  try{
    const res=await fetch("/api",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});
    const out=await res.json();
    if(!res.ok) throw new Error(out.error||"Prediction failed.");
    document.getElementById("level").textContent=out.performance_level;
    document.getElementById("summary").textContent=`${out.pass_fail} status · ${out.risk} intervention risk`;
    document.getElementById("risk").textContent=`${out.risk} Risk`;
    document.getElementById("percentage").textContent=`${out.predicted_percentage}%`;
    document.getElementById("passfail").textContent=out.pass_fail;
    document.getElementById("confidence").textContent=`${out.confidence}%`;
    const ul=document.getElementById("recommendations");
    ul.innerHTML="";
    out.recommendations.forEach(x=>{const li=document.createElement("li");li.textContent=x;ul.appendChild(li)});
    result.classList.remove("hidden");
    result.scrollIntoView({behavior:"smooth",block:"center"});
  }catch(err){
    errorBox.textContent=err.message;
    errorBox.classList.remove("hidden");
  }finally{
    btn.disabled=false;
    btn.innerHTML='Predict Student Performance <span>→</span>';
  }
});
