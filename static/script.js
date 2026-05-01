let rows,cols;

async function start(){
 rows=document.getElementById("rows").value;
 cols=document.getElementById("cols").value;

 await fetch("/start",{method:"POST",
 headers:{'Content-Type':'application/json'},
 body:JSON.stringify({rows,cols})});

 draw([]);
}

async function step(){
 const res=await fetch("/step");
 const data=await res.json();

 draw(data.grid);
 document.getElementById("percepts").innerText =
 "Percepts: "+data.percepts.join(" | ");
 document.getElementById("steps").innerText =
 "Inference Steps: "+data.steps;
}

function draw(grid){
 const g=document.getElementById("grid");
 g.style.gridTemplateColumns=`repeat(${cols},45px)`;
 g.innerHTML="";

 for(let r=0;r<rows;r++){
  for(let c=0;c<cols;c++){
   const div=document.createElement("div");
   div.className="cell "+(grid[r]?.[c]||"unknown");
   g.appendChild(div);
  }
 }
}