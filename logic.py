import random

class KnowledgeBase:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.clauses = []
        self.inference_steps = 0

    # add clause to KB
    def tell(self, clause):
        self.clauses.append(set(clause))

    # simple resolution refutation
    def resolve(self, query):
        clauses = self.clauses.copy()
        clauses.append(set(query))

        new = []

        while True:
            self.inference_steps += 1
            pairs = [(clauses[i], clauses[j]) for i in range(len(clauses)) for j in range(i+1,len(clauses))]

            for (c1, c2) in pairs:
                resolvent = self.pl_resolve(c1, c2)
                if resolvent == set():
                    return True
                new.append(resolvent)

            if set(map(tuple,new)).issubset(set(map(tuple,clauses))):
                return False

            clauses.extend(new)

    def pl_resolve(self, c1, c2):
        for literal in c1:
            if f"¬{literal}" in c2:
                return (c1 - {literal}) | (c2 - {f'¬{literal}'})
        return set()
    
class WumpusWorld:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.agent = (0,0)
        self.pits = set()
        self.wumpus = None
        self.visited = set()
        self.safe = {(0,0)}
        self.generate_world()

    def generate_world(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r,c) != (0,0) and random.random() < 0.2:
                    self.pits.add((r,c))

        while True:
            w = (random.randint(0,self.rows-1), random.randint(0,self.cols-1))
            if w not in self.pits and w != (0,0):
                self.wumpus = w
                break

    def neighbors(self, r,c):
        dirs = [(1,0),(-1,0),(0,1),(0,-1)]
        return [(r+dr,c+dc) for dr,dc in dirs if 0<=r+dr<self.rows and 0<=c+dc<self.cols]

    def percepts(self):
        r,c = self.agent
        breeze = any(n in self.pits for n in self.neighbors(r,c))
        stench = any(n == self.wumpus for n in self.neighbors(r,c))
        return breeze, stench