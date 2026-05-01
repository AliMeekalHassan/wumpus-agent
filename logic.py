import random

class KnowledgeBase:
    def __init__(self):
        self.safe_cells = set()
        self.pit_cells = set()
        self.wumpus_cells = set()
        self.inference_steps = 0

    # tell percept rules
    def tell_percepts(self, cell, breeze, stench, neighbors):
        self.inference_steps += 1

        if not breeze:
            for n in neighbors:
                self.safe_cells.add(n)

        if not stench:
            for n in neighbors:
                self.safe_cells.add(n)

        # if breeze → possible pits
        if breeze:
            for n in neighbors:
                if n not in self.safe_cells:
                    self.pit_cells.add(n)

        # if stench → possible wumpus
        if stench:
            for n in neighbors:
                if n not in self.safe_cells:
                    self.wumpus_cells.add(n)

    def is_safe(self, cell):
        self.inference_steps += 1
        return cell in self.safe_cells
    
class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.agent = (0,0)
        self.visited = {(0,0)}
        self.pits = set()
        self.wumpus = None
        self.generate_world()

    def generate_world(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c)!=(0,0) and random.random()<0.18:
                    self.pits.add((r,c))

        while True:
            w = (random.randint(0,self.rows-1), random.randint(0,self.cols-1))
            if w not in self.pits and w!=(0,0):
                self.wumpus = w
                break

    def neighbors(self, r,c):
        dirs=[(1,0),(-1,0),(0,1),(0,-1)]
        return [(r+dr,c+dc) for dr,dc in dirs if 0<=r+dr<self.rows and 0<=c+dc<self.cols]

    def percepts(self):
        r,c=self.agent
        neigh=self.neighbors(r,c)
        breeze=any(n in self.pits for n in neigh)
        stench=any(n==self.wumpus for n in neigh)
        return breeze, stench