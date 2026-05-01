from flask import Flask, render_template, jsonify, request
from logic import KnowledgeBase, WumpusWorld

app = Flask(__name__)

world = None
kb = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global world, kb
    data = request.json
    rows = int(data["rows"])
    cols = int(data["cols"])

    world = WumpusWorld(rows, cols)
    kb = KnowledgeBase(rows, cols)

    return jsonify({"msg":"world created"})

@app.route("/step")
def step():
    global world, kb

    r,c = world.agent
    breeze, stench = world.percepts()

    percepts = []
    if breeze: percepts.append("Breeze")
    if stench: percepts.append("Stench")

    # TELL KB percept rules
    if breeze:
        kb.tell([f"P{r}{c}"])
    if stench:
        kb.tell([f"W{r}{c}"])

    world.visited.add((r,c))

    # move randomly to safe neighbor (demo)
    for n in world.neighbors(r,c):
        if n not in world.visited:
            world.agent = n
            break

    grid = []
    for i in range(world.rows):
        row = []
        for j in range(world.cols):
            if (i,j) in world.visited:
                row.append("safe")
            else:
                row.append("unknown")
        grid.append(row)

    return jsonify({
        "grid": grid,
        "percepts": percepts,
        "inference": kb.inference_steps
    })

if __name__ == "__main__":
    app.run()