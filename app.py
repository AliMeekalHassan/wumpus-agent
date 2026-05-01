from flask import Flask, render_template, request, jsonify, session
import random
from logic import KnowledgeBase

app = Flask(__name__)
app.secret_key = "wumpus_secret"  # needed for session storage

# this function builds wumpus world
def build_world(rows, cols):
    grid = [["" for _ in range(cols)] for _ in range(rows)]
    # place wumpus randomly
    w_row, w_col = random.randint(0, rows-1), random.randint(0, cols-1)
    grid[w_row][w_col] = "W"
    # place pits randomly
    for _ in range((rows*cols)//6):  # ~16% pits
        p_row, p_col = random.randint(0, rows-1), random.randint(0, cols-1)
        if grid[p_row][p_col] == "":
            grid[p_row][p_col] = "P"
    return grid, (0,0)  # agent starts at (0,0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    rows = int(request.json["rows"])
    cols = int(request.json["cols"])
    grid, agent_pos = build_world(rows, cols)
    kb = KnowledgeBase(rows, cols)
    session["grid"] = grid
    session["agent"] = agent_pos
    session["kb"] = kb.__dict__  # store KB state
    return jsonify({"grid": grid, "agent": agent_pos})

@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    grid = session["grid"]
    agent = session["agent"]
    kb = KnowledgeBase(session["kb"]["rows"], session["kb"]["cols"])
    kb.clauses = session["kb"]["clauses"]
    kb.steps = session["kb"]["steps"]

    r, c = agent
    if direction == "right": c += 1
    elif direction == "left": c -= 1
    elif direction == "up": r -= 1
    elif direction == "down": r += 1

    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return jsonify({"error": "Invalid move"})

    agent = (r,c)
    percepts = []
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] == "P": percepts.append("Breeze")
            if grid[nr][nc] == "W": percepts.append("Stench")

    kb.tell(agent, percepts)
    safe = kb.ask_safe(agent)

    session["agent"] = agent
    session["kb"] = kb.__dict__

    return jsonify({"agent": agent, "percepts": percepts, "safe": safe, "steps": kb.steps})

if __name__ == "__main__":
    app.run(debug=True)