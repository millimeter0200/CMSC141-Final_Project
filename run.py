from multitape_tm import MultiTapeTM, State

if __name__ == "__main__":

    # Create states
    stateNames = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "qf"]
    states = [State(name) for name in stateNames]

    # Shortcut lookup
    s = {state.name: state for state in states}

    # q0: scan first operand (Tape 1)
    s["q0"].setNext(("0","B","B"), "q0", ["0","B","B"], ["R","S","S"])
    s["q0"].setNext(("1","B","B"), "q0", ["1","B","B"], ["R","S","S"])
    s["q0"].setNext(("|","B","B"), "q1", ["|","B","B"], ["R","S","S"])

    # q1: copy second operand to Tape 2
    s["q1"].setNext(("0","B","B"), "q1", ["B","0","B"], ["R","R","S"])
    s["q1"].setNext(("1","B","B"), "q1", ["B","1","B"], ["R","R","S"])
    s["q1"].setNext(("=","B","B"), "q2", ["B","B","B"], ["L","S","S"])

    # q2: move to the end of the first operand
    s["q2"].setNext(("B","B","B"), "q2", ["B","B","B"], ["L","S","S"])
    s["q2"].setNext(("|","B","B"), "q3", ["B","B","B"], ["L","L","S"])

    # q3: add operands from right to left, write to Tape 3
    s["q3"].setNext(("0","0","B"), "q3", ["0","0","0"], ["L","L","L"])
    s["q3"].setNext(("0","1","B"), "q3", ["0","1","1"], ["L","L","L"])
    s["q3"].setNext(("1","0","B"), "q3", ["1","0","1"], ["L","L","L"])
    s["q3"].setNext(("1","1","B"), "q3", ["1","1","1"], ["L","L","L"])

    s["q3"].setNext(("B","B","B"), "q4", ["B","B","B"], ["S","S","R"])

    # q4: checking the third tape
    s["q4"].setNext(("B","B","0"), "q4", ["B","B","0"], ["S","S","R"])
    s["q4"].setNext(("B","B","1"), "q5", ["B","B","1"], ["S","S","R"])
    s["q4"].setNext(("B","B","B"), "q6", ["B","B","="], ["S","S","R"])

    # q5: found 1, go to the rightmost of tape 3 into the blanks
    s["q5"].setNext(("B","B","0"), "q5", ["B","B","0"], ["S","S","R"])
    s["q5"].setNext(("B","B","1"), "q5", ["B","B","1"], ["S","S","R"])
    s["q5"].setNext(("B","B","B"), "q7", ["B","B","="], ["S","S","R"])

    # q6: or = 0, did not find 1 in the 3rd tape
    s["q6"].setNext(("B","B","B"), "qf", ["B","B","0"], ["S","S","S"])

    # q7: or = 1, found 1 in the 3rd tape
    s["q7"].setNext(("B","B","B"), "qf", ["B","B","1"], ["S","S","S"])

    # initialize TM
    tm = MultiTapeTM(
        states=states,
        finalStates=["qf"],
        sigma=["0","1","|","="],
        numTapes=3  # change number of tapes here
    )


    # run TM on input
    input_string = "101|100="
    tm.deltaHat(input_string, printing=True)
