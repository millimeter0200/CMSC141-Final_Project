# ------------------ STATE CLASS ------------------

class State:
    def __init__(self, name):
        self.name = name
        # state now remembers its own name
        # key: tuple of symbols read from each tape
        # value: (nextStateName, writeSymbolsList, moveList)
        self.next = {}

    # add one rule to the state
    # if I see 1, B, B, then write 1, B, B, move right, and go to q1
    def setNext(self, readSymbols, nextState, writeSymbols, moves):
        """
        readSymbols: tuple of symbols read from each tape
        nextState: string (name of next state)
        writeSymbols: list of symbols to write on each tape
        moves: list of directions for each tape: 'L', 'R', 'S'
        """

        #check if deterministic
        # ensures that the same combination of read symbols always maps to the same transition
        # a deterministic TM must have ONE RULE 
        key = tuple(readSymbols)
        if key in self.next:
            raise ValueError(
                f"Nondeterministic transition in state {self.name} on {key}"
            )

        self.next[tuple(readSymbols)] = (nextState, writeSymbols, moves)    #stores the rule

    # given what the machine is seeing right now, find the rule
    # if a rule exists → return it; if no rule exists → return None ... NONE = REJECTION since TM can't proceed w undefined transitions
    def delta(self, readSymbols):
        """Return the transition for the given readSymbols tuple."""
        return self.next.get(tuple(readSymbols), None)

# ------------------ MultiTapeTM CLASS ------------------
class MultiTapeTM:
    def __init__(self, states, finalStates, sigma, numTapes):
        """
        states: list of State objects
        finalStates: list of final state names
        sigma: list of input alphabet symbols
        numTapes: number of tapes in the TM
        """
        self.numTapes = numTapes    # stores how many tapes exist
        self.sigma = sigma          # stores allowed input symbols
        self.blank = "B"            # blank symbol

        self.q = {s.name: s for s in states}  # state lookup (self.q["q0"] → State object )
        self.f = set(finalStates)             # stores accepting states in a set so checking is fast          

        # initial state = first state in list
        self.startState = states[0].name

# ------------------ TAPE INITIALIZATION ------------------

    def initializeTapes(self, inputString):
        """Prepare tapes and heads."""

        # heads will move left and right
        padding = [self.blank, self.blank]
        tapes = [padding + list(inputString) + padding]  # Tape 1 is the input tape

        # add additional blank tapes      
        # for all remaining tapes  
        for _ in range(1, self.numTapes):
            tapes.append(padding + padding)                # Tapes 2 & 3 starts as B B B B because they don't have input initially
        
        # all heads start after padding
        tapeHead = [len(padding)] * self.numTapes 
        return tapes, tapeHead

# ------------------ SAFE READ/WRITE ------------------

    def safeRead(self, tape, headPos):
        """Read symbol; if out of bounds, return blank."""
        if headPos < 0 or headPos >= len(tape):
            return self.blank
        return tape[headPos]    # return the actual symbol at that position

    def safeWrite(self, tape, headPos, symbol):
        """Write symbol; auto-extend tape if needed."""
        # extend left
        # if the head move too far to the left, add a blank at the very start of the tape
        # and return position 0 (since we just added a new cell at position 0)
        if headPos < 0:
            tape.insert(0, self.blank)
            return 0

        # extend right
        # too far to the right → add blanks to the end of the tape
        # keep doing this until the head position exists
        while headPos >= len(tape):
            tape.append(self.blank)

        # if tape is big enough, write the symbol exactly where the head is
        # return the (possibly updated) head position
        tape[headPos] = symbol
        return headPos

# ------------------ ENFORCE PADDING ------------------

    def enforcePadding(self, tapes, tapeHead):
        """Ensure each tape has exactly 2 blanks at both ends and adjust heads accordingly."""

        # get the current tape for each tape
        for i in range(self.numTapes):
            tape = tapes[i]

            #LEFT PADDING
            leftBlanks = 0

            # count existing blanks at the left
            for symbol in tape:
                if symbol == self.blank:
                    leftBlanks += 1
                else:
                    break

            # add missing blanks to the front of the tape if fewer than 2
            if leftBlanks < 2:
                needed = 2 - leftBlanks
                tape = [self.blank] * needed + tape
                tapeHead[i] += needed  #shift head to keep pointing at same symbol

            #RIGHT PADDING
            rightBlanks = 0

            #count existing blanks at the right
            for symbol in reversed(tape):
                if symbol == self.blank:
                    rightBlanks += 1
                else:
                    break

            #add blanks if fewer than 2
            if rightBlanks < 2:
                needed = 2 - rightBlanks
                tape.extend([self.blank] * needed)

            #save back the modified tape
            tapes[i] = tape

# ------------------ DELTA HAT FUNCTION ------------------

    def deltaHat(self, inputString, maxSteps=10000, printing=True):
        """
        Runs the multitape TM on the input string.
        Returns True if accepted, False if rejected.
        """

        # input is placed on Tape 1 → other tapes are empty → heads are positioned → machine starts in the start state → step counter starts at 0
        tapes, tapeHead = self.initializeTapes(inputString)
        currentState = self.startState
        steps = 0

        # frozen copy of original tape
        originalTapes = [list(t) for t in tapes]  

        # only prints the original tapes once at the start 
        if printing:
            print("Original tapes:")
            for i, t in enumerate(originalTapes):
                print(f"Tape {i+1}: {''.join(t)}")
            print("-" * 40)

        while True:
            if steps > maxSteps:
                print("Machine halted: max steps exceeded.")
                return False

            # this is where acceptance is decided
            # check if final state reached
            if currentState in self.f:
                print(f"ACCEPTED at step {steps}")
                # print final tapes
                if printing:
                    print("Final tapes:")
                    for i, t in enumerate(tapes):
                        print(f"Tape {i+1}: {''.join(t)}")
                return True

            # this collects what each tape head sees
            # readSymbols = ["1", "B", "B"]
            readSymbols = []
            for i in range(self.numTapes):
                readSymbols.append(self.safeRead(tapes[i], tapeHead[i]))

            # this is where the machine decides what to do (given these symbols, what rule applies?)
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


