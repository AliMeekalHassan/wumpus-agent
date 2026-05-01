from flask import Flask, render_template, jsonify, request
from logic import KnowledgeBase, WumpusWorld

app = Flask(__name__)

world=None
kb=None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start():
    global world,kb
    data=request.json
    rows=int(data["rows"])
    cols=int(data["cols"])

    world=WumpusWorld(rows,cols)
    kb=KnowledgeBase()
    kb.safe_cells.add((0,0))

    return jsonify({"msg":"started"})

@app.route("/step")
def step():
    global world,kb
    r,c=world.agent

    breeze, stench = world.percepts()
    neighbors = world.neighbors(r,c)

    kb.tell_percepts((r,c),breeze,stench,neighbors)

    # choose next SAFE cell
    moved=False
    for n in neighbors:
        if n not in world.visited and kb.is_safe(n):
            world.agent=n
            world.visited.add(n)
            moved=True
            break

    percept_text=[]
    percept_text.append("Breeze" if breeze else "No Breeze")
    percept_text.append("Stench" if stench else "No Stench")

    # build grid view
    grid=[]
    for i in range(world.rows):
        row=[]
        for j in range(world.cols):
            cell=(i,j)

            if cell in kb.pit_cells or cell in kb.wumpus_cells:
                row.append("danger")
            elif cell in kb.safe_cells:
                row.append("safe")
            else:
                row.append("unknown")

        grid.append(row)

    return jsonify({
        "grid":grid,
        "percepts":percept_text,
        "steps":kb.inference_steps
    })

if __name__=="__main__":
    app.run()