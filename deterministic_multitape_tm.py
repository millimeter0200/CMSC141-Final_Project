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
        self.q = {state.name: state for state in states}
        self.f = finalStates
        self.sigma = sigma
        self.numTapes = numTapes
        self.blank = "_"

        # initial state = first state in list
        self.startState = states[0].name

    def initializeTapes(self, inputString):
        """Prepare tapes and heads."""
        tapes = []

        # Tape 1 contains input
        tapes.append(list(inputString))

        # Other tapes start blank
        for _ in range(1, self.numTapes):
            tapes.append([self.blank])

        # All heads start at position 0
        heads = [0 for _ in range(self.numTapes)]

        return tapes, heads

    def safeRead(self, tape, headPos):
        """Read symbol; if out of bounds, return blank."""
        if headPos < 0 or headPos >= len(tape):
            return self.blank
        return tape[headPos]

    def safeWrite(self, tape, headPos, symbol):
        """Write symbol; auto-extend tape if needed."""
        if headPos < 0:
            # extend left
            tape.insert(0, symbol)
        elif headPos >= len(tape):
            # extend right
            # pad with blanks until headPos exists
            while len(tape) <= headPos:
                tape.append(self.blank)
            tape[headPos] = symbol
        else:
            tape[headPos] = symbol

    def deltaHat(self, inputString, maxSteps=10000):
        """
        Runs the multitape TM on the input string.
        Returns True if accepted, False if rejected.
        """
        tapes, heads = self.initializeTapes(inputString)
        currentState = self.startState

        steps = 0
        while True:
            if steps > maxSteps:
                print("Machine halted: max steps exceeded.")
                return False

            # Check if final state reached
            if currentState in self.f:
                return True

            # Read symbols from each tape
            readSymbols = []
            for i in range(self.numTapes):
                readSymbols.append(self.safeRead(tapes[i], heads[i]))

            stateObj = self.q[currentState]
            transition = stateObj.delta(tuple(readSymbols))

            if transition is None:
                # No transition defined → reject
                return False

            nextState, writeSymbols, moves = transition
            currentState = nextState

            # Write to tapes
            for i in range(self.numTapes):
                self.safeWrite(tapes[i], heads[i], writeSymbols[i])

            # Move heads
            for i in range(self.numTapes):
                if moves[i] == "L":
                    heads[i] -= 1
                elif moves[i] == "R":
                    heads[i] += 1
                # If moves[i] == "S": do nothing

            steps += 1
