class State:
    def __init__(self, name):
        self.name = name
        # key: tuple of symbols read from each tape
        # value: (nextStateName, writeSymbolsList, moveList)
        self.next = {}

    def setNext(self, readSymbols, nextState, writeSymbols, moves):
        """
        readSymbols: tuple of symbols read from each tape
        nextState: string (name of next state)
        writeSymbols: list of symbols to write on each tape
        moves: list of directions for each tape: 'L', 'R', 'S'
        """

        #check if deterministic
        key = tuple(readSymbols)
        if key in self.next:
            raise ValueError(
                f"Nondeterministic transition in state {self.name} on {key}"
            )

        self.next[tuple(readSymbols)] = (nextState, writeSymbols, moves)

    def delta(self, readSymbols):
        """Return the transition for the given readSymbols tuple."""
        return self.next.get(tuple(readSymbols), None)


class MultiTapeTM:
    def __init__(self, states, finalStates, sigma, numTapes):
        """
        states: list of State objects
        finalStates: list of final state names
        sigma: list of input alphabet symbols
        numTapes: number of tapes in the TM
        """
        self.numTapes = numTapes
        self.sigma = sigma
        self.blank = "_"

        self.q = {s.name: s for s in states}  # state lookup
        self.f = set(finalStates)             # final states

        # initial state = first state in list
        self.startState = states[0].name

    def initializeTapes(self, inputString):
        """Prepare tapes and heads."""

        padding = [self.blank, self.blank]
        tapes = [padding + list(inputString) + padding]  # Tape 1

        for _ in range(1, self.numTapes):
            tapes.append(padding + padding)                # Tapes 2 & 3
        
        # all heads start after padding
        tapeHead = [len(padding)] * self.numTapes 
        return tapes, tapeHead

    def safeRead(self, tape, headPos):
        """Read symbol; if out of bounds, return blank."""
        if headPos < 0 or headPos >= len(tape):
            return self.blank
        return tape[headPos]

    def safeWrite(self, tape, headPos, symbol):
        """Write symbol; auto-extend tape if needed."""
        # extend left
        if headPos < 0:
            tape.insert(0, self.blank)
            return 0

        # extend right
        while headPos >= len(tape):
            tape.append(self.blank)

        tape[headPos] = symbol
        return headPos

    def enforcePadding(self, tapes, tapeHead):
        """Ensure each tape has 2 blanks at both ends and adjust heads."""
        for i in range(self.numTapes):
            # left padding
            if tapeHead[i] < 2:  #adjust head if too close to left edge
                while tapeHead[i] < 2:
                    tapes[i].insert(0, self.blank)
                    tapeHead[i] += 1
            # right padding
            while len(tapes[i]) - tapeHead[i] <= 2:
                tapes[i].append(self.blank)

    def deltaHat(self, inputString, maxSteps=10000, printing=True):
        """
        Runs the multitape TM on the input string.
        Returns True if accepted, False if rejected.
        """
        tapes, tapeHead = self.initializeTapes(inputString)
        currentState = self.startState
        steps = 0

        # frozen copy of original tape
        originalTapes = [list(t) for t in tapes]  

        if printing:
            print("Original tapes:")
            for i, t in enumerate(originalTapes):
                print(f"Tape {i+1}: {''.join(t)}")
            print("-" * 40)

        while True:
            if steps > maxSteps:
                print("Machine halted: max steps exceeded.")
                return False

            #check if final state reached
            if currentState in self.f:
                print(f"ACCEPTED at step {steps}")
                # print final tapes
                if printing:
                    print("Final tapes:")
                    for i, t in enumerate(tapes):
                        print(f"Tape {i+1}: {''.join(t)}")
                return True

            #read symbols from each tape
            readSymbols = []
            for i in range(self.numTapes):
                readSymbols.append(self.safeRead(tapes[i], tapeHead[i]))

            #get transition for current read symbols
            stateObj = self.q[currentState]
            transition = stateObj.delta(tuple(readSymbols))

            #reject no transition defined
            if transition is None:
                print(f"REJECTED at state {currentState}, symbols {readSymbols}")
                if printing:
                    print("Final tapes:")
                    for i, t in enumerate(tapes):
                        print(f"Tape {i+1}: {''.join(t)}")
                return False

            nextState, writeSymbols, moves = transition
            currentState = nextState

            #write to tapes
            for i in range(self.numTapes):
                tapeHead[i] = self.safeWrite(tapes[i], tapeHead[i], writeSymbols[i])

            #move heads
            for i in range(self.numTapes):
                if moves[i] == "L":
                    tapeHead[i] -= 1
                elif moves[i] == "R":
                    tapeHead[i] += 1
                else:            #"S" no movement
                    pass

            # enforce padding after every step
            self.enforcePadding(tapes, tapeHead)
            
            # print current tapes at each step
            if printing:
                print(f"Step {steps}: Current State={currentState}, Heads={tapeHead}")
                for i, t in enumerate(tapes):
                    print(f"Tape {i+1} current: {''.join(t)}")
                print("-" * 40)


            steps += 1


