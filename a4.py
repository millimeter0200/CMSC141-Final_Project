class State:
    def __init__(self, name):
        self.name = name
        self.next = {}

    def set(self, r, n, w, m):
        self.next[tuple(r)] = (n, w, m)

    def delta(self, r):
        return self.next.get(tuple(r))


class HardCodedBinaryAddTM:
    def __init__(self):
        self.B = "B"
        self.states = {}
        self.final = "qf"

        # STATES
        for s in ["q0", "q1", "qadd", "qcarry", "qf"]:
            self.states[s] = State(s)

        # q0: scan first operand 
        self.states["q0"].set(("0","B","B"), "q0", ["0","B","B"], ["R","S","S"])
        self.states["q0"].set(("1","B","B"), "q0", ["1","B","B"], ["R","S","S"])
        self.states["q0"].set(("+","B","B"), "q1", ["+","B","B"], ["R","R","S"])

        # q1: copy second operand 
        self.states["q1"].set(("0","B","B"), "q1", ["B","0","B"], ["R","R","S"])
        self.states["q1"].set(("1","B","B"), "q1", ["B","1","B"], ["R","R","S"])
        self.states["q1"].set(("=","B","B"), "qadd", ["B","B","B"], ["L","L","S"])

        # qadd: addition (no carry) 
        self.states["qadd"].set(("0","0","B"), "qadd", ["0","0","0"], ["L","L","L"])
        self.states["qadd"].set(("0","1","B"), "qadd", ["0","1","1"], ["L","L","L"])
        self.states["qadd"].set(("1","0","B"), "qadd", ["1","0","1"], ["L","L","L"])
        self.states["qadd"].set(("1","1","B"), "qcarry", ["1","1","0"], ["L","L","L"])

        self.states["qadd"].set(("B","0","B"), "qadd", ["0","0","0"], ["L","L","L"])
        self.states["qadd"].set(("B","1","B"), "qadd", ["0","1","1"], ["L","L","L"])
        self.states["qadd"].set(("0","B","B"), "qadd", ["0","0","0"], ["L","L","L"])
        self.states["qadd"].set(("1","B","B"), "qadd", ["1","0","1"], ["L","L","L"])

        # skip '+' when moving left
        self.states["qadd"].set(("+","B","B"), "qadd", ["+","B","B"], ["L","S","S"])

        # finish when all consumed
        self.states["qadd"].set(("B","B","B"), "qf", ["B","+","="], ["S","S","S"])

        # qcarry: addition with carry
        self.states["qcarry"].set(("0","0","B"), "qadd", ["0","0","1"], ["L","L","L"])
        self.states["qcarry"].set(("0","1","B"), "qcarry", ["0","1","0"], ["L","L","L"])
        self.states["qcarry"].set(("1","0","B"), "qcarry", ["1","0","0"], ["L","L","L"])
        self.states["qcarry"].set(("1","1","B"), "qcarry", ["1","1","1"], ["L","L","L"])

        # skip '+' while carrying
        self.states["qcarry"].set(("+","B","B"), "qcarry", ["+","B","B"], ["L","S","S"])

        # overflow carry
        self.states["qcarry"].set(("B","B","B"), "qf", ["B","+","1"], ["S","S","S"])

        self.start = "q0"

    def run(self, inp):
        tapes = [list(inp), [self.B], [self.B]]
        heads = [0,0,0]
        cur = self.start

        while True:
            if cur == self.final:
                print("ACCEPTED")
                print("Final tapes:", tapes)
                return

            read = []
            for i in range(3):
                if heads[i] < 0 or heads[i] >= len(tapes[i]):
                    read.append(self.B)
                else:
                    read.append(tapes[i][heads[i]])

            tr = self.states[cur].delta(tuple(read))
            if tr is None:
                print("REJECTED at", cur, read)
                return

            nxt, write, move = tr
            cur = nxt

            for i in range(3):
                if heads[i] < 0:
                    tapes[i].insert(0, write[i])
                elif heads[i] >= len(tapes[i]):
                    while len(tapes[i]) <= heads[i]:
                        tapes[i].append(self.B)
                    tapes[i][heads[i]] = write[i]
                else:
                    tapes[i][heads[i]] = write[i]

            for i in range(3):
                if move[i] == "L":
                    heads[i] -= 1
                elif move[i] == "R":
                    heads[i] += 1


# RUN
tm = HardCodedBinaryAddTM()
tm.run("101+11=")
