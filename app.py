from flask import Flask, render_template, request, jsonify
import random
from logic import KnowledgeBase

app = Flask(__name__)

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
    request.session = {"grid": grid, "agent": agent_pos, "kb": kb}
    return jsonify({"grid": grid, "agent": agent_pos})

@app.route("/move", methods=["POST"])
def move():
    direction = request.json["direction"]
    grid = request.session["grid"]
    agent = request.session["agent"]
    kb = request.session["kb"]

    r, c = agent
    if direction == "right": c += 1
    elif direction == "left": c -= 1
    elif direction == "up": r -= 1
    elif direction == "down": r += 1

    if r < 0 or c < 0 or r >= len(grid) or c >= len(grid[0]):
        return jsonify({"error": "Invalid move"})

    agent = (r,c)
    percepts = []
    # check percepts
    for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] == "P": percepts.append("Breeze")
            if grid[nr][nc] == "W": percepts.append("Stench")

    # tell KB
    kb.tell(agent, percepts)
    safe = kb.ask_safe(agent)

    request.session["agent"] = agent
    return jsonify({"agent": agent, "percepts": percepts, "safe": safe, "steps": kb.steps})

if __name__ == "__main__":
    app.run(debug=True)