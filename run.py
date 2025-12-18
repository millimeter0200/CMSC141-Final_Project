from deterministic_multitape_tm import MultiTapeTM, State

if __name__ == "__main__":

    # Create states
    stateNames = ["q0", "q1", "q2", "q3", "q4", "q5", "qf"]
    states = [State(name) for name in stateNames]

    # Shortcut lookup
    s = {state.name: state for state in states}

    # q0: scan first operand (Tape 1)
    s["q0"].setNext(("0","_","_"), "q0", ["0","_","_"], ["R","S","S"])
    s["q0"].setNext(("1","_","_"), "q0", ["1","_","_"], ["R","S","S"])
    s["q0"].setNext(("+","_","_"), "q1", ["+","_","_"], ["R","R","S"])

    # q1: copy second operand to Tape 2
    s["q1"].setNext(("0","_","_"), "q1", ["_","0","_"], ["R","R","S"])
    s["q1"].setNext(("1","_","_"), "q1", ["_","1","_"], ["R","R","S"])
    s["q1"].setNext(("=","_","_"), "q2", ["_","_","_"], ["L","S","S"])

    # q2: move to the end of the first operand
    s["q2"].setNext(("_","_","_"), "q2", ["_","_","_"], ["L","S","S"])
    s["q2"].setNext(("+","_","_"), "q2", ["_","_","_"], ["L","L","S"])

    s["q2"].setNext(("0","0","_"), "q3", ["0","0","_"], ["S","S","S"])
    s["q2"].setNext(("1","1","_"), "q3", ["1","1","_"], ["S","S","S"])
    s["q2"].setNext(("0","1","_"), "q3", ["0","1","_"], ["S","S","S"])
    s["q2"].setNext(("1","0","_"), "q3", ["1","0","_"], ["S","S","S"])
    s["q2"].setNext(("0","_","_"), "q3", ["0","_","_"], ["S","S","S"])
    s["q2"].setNext(("1","_","_"), "q3", ["1","_","_"], ["S","S","S"])
    s["q2"].setNext(("_","1","_"), "q3", ["_","1","_"], ["S","S","S"])
    s["q2"].setNext(("_","0","_"), "q3", ["_","0","_"], ["S","S","S"])

    # q3: addition without carry
    s["q3"].setNext(("0","0","_"), "q3", ["0","0","0"], ["L","L","L"])
    s["q3"].setNext(("0","1","_"), "q3", ["0","1","1"], ["L","L","L"])
    s["q3"].setNext(("1","0","_"), "q3", ["1","0","1"], ["L","L","L"])
    s["q3"].setNext(("1","1","_"), "q4", ["1","1","0"], ["L","L","L"])
    s["q3"].setNext(("0","_","_"), "q3", ["0","_","0"], ["L","L","L"])
    s["q3"].setNext(("1","_","_"), "q3", ["1","_","1"], ["L","L","L"])
    s["q3"].setNext(("_","0","_"), "q3", ["_","0","0"], ["L","L","L"])
    s["q3"].setNext(("_","1","_"), "q3", ["_","1","1"], ["L","L","L"])
    s["q3"].setNext(("_","_","_"), "qf", ["_","_","_"], ["S","S","S"])  # finished

    # q4: addition with carry
    s["q4"].setNext(("0","0","_"), "q3", ["0","0","1"], ["L","L","L"])
    s["q4"].setNext(("0","1","_"), "q4", ["0","1","0"], ["L","L","L"])
    s["q4"].setNext(("1","0","_"), "q4", ["1","0","0"], ["L","L","L"])
    s["q4"].setNext(("1","1","_"), "q4", ["1","1","1"], ["L","L","L"])
    s["q4"].setNext(("0","_","_"), "q3", ["0","_","1"], ["L","L","L"])
    s["q4"].setNext(("1","_","_"), "q4", ["1","_","0"], ["L","L","L"])
    s["q4"].setNext(("_","0","_"), "q3", ["_","0","1"], ["L","L","L"])
    s["q4"].setNext(("_","1","_"), "q4", ["_","1","0"], ["L","L","L"])
    s["q4"].setNext(("_","_","_"), "q5", ["_","+","1"], ["S","S","L"])  # final carry

    # q5: move to the end of the result
    s["q5"].setNext(("0","_","_"), "q5", ["0","_","_"], ["L","S","S"])
    s["q5"].setNext(("1","_","_"), "q5", ["1","_","_"], ["L","S","S"])
    s["q5"].setNext(("_","+","_"), "qf", ["_","+","="], ["S","S","L"])

    # initialize TM
    tm = MultiTapeTM(
        states=states,
        finalStates=["qf"],
        sigma=["0","1","+","="],
        numTapes=3
    )


    # run TM on input
    input_string = "101+11="
    tm.deltaHat(input_string, printing=True)