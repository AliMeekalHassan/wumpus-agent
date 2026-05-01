let rows, cols;

async function start(){
    rows = document.getElementById("rows").value;
    cols = document.getElementById("cols").value;

    await fetch("/start",{
        method:"POST",
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({rows,cols})
    });

    drawGrid([]);
}

async function step(){
    const res = await fetch("/step");
    const data = await res.json();
    drawGrid(data.grid);

    document.getElementById("percepts").innerText =
        "Percepts: " + data.percepts.join(", ");

    document.getElementById("steps").innerText =
        "Inference steps: " + data.inference;
}

function drawGrid(grid){
    const g = document.getElementById("grid");
    g.style.gridTemplateColumns = `repeat(${cols},40px)`;
    g.innerHTML="";

    for(let r=0;r<rows;r++){
        for(let c=0;c<cols;c++){
            const div=document.createElement("div");
            div.className="cell " + (grid[r]?.[c] || "unknown");
            g.appendChild(div);
        }
    }
}