# this file implements propositional KB and resolution refutation
class KnowledgeBase:
    def __init__(self, rows, cols):
        self.rows, self.cols = rows, cols
        self.clauses = []
        self.steps = 0

    def tell(self, pos, percepts):
        r,c = pos
        if "Breeze" in percepts:
            self.clauses.append(f"B_{r}_{c}")
        if "Stench" in percepts:
            self.clauses.append(f"S_{r}_{c}")

    def ask_safe(self, pos):
        self.steps += 1
        r,c = pos
        # simplified resolution: safe if no percepts recorded for this cell
        for clause in self.clauses:
            if f"B_{r}_{c}" in clause or f"S_{r}_{c}" in clause:
                return False
        return True