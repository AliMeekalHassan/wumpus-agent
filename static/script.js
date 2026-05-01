let agent = null;
let grid = null;

async function startGame() {
  let rows = document.getElementById("rows").value;
  let cols = document.getElementById("cols").value;
  let res = await fetch("/start", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({rows, cols})
  });
  let data = await res.json();
  grid = data.grid;
  agent = data.agent;
  drawGrid();
}

async function move(direction) {
  let res = await fetch("/move", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({direction})
  });
  let data = await res.json();
  agent = data.agent;
  drawGrid();
  document.getElementById("metrics").innerText =
    "Percepts: " + data.percepts.join(", ") +
    " | Safe: " + data.safe +
    " | Steps: " + data.steps;
}

function drawGrid() {
  let rows = grid.length, cols = grid[0].length;
  let container = document.getElementById("grid");
  container.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
  container.innerHTML = "";
  for (let r=0; r<rows; r++) {
    for (let c=0; c<cols; c++) {
      let cell = document.createElement("div");
      cell.classList.add("cell","unknown");
      if (r === agent[0] && c === agent[1]) cell.classList.add("safe");
      if (grid[r][c] === "P" || grid[r][c] === "W") cell.classList.add("hazard");
      container.appendChild(cell);
    }
  }
}