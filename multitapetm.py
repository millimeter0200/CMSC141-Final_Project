# δ(q, [X1, X2, . . . , Xk]) = (p, [Y1, Y2, . . . , Yk], [D0, D1, . . . , Dk)


class State:

    # Constructor for the State
    def __init__(self, name):
        self.name = name
        self.next = None

    # δ(q, [X1, X2, ..., Xk]), tapeHeads refers to the set of pointers of X
    # returns the (p, [Y1, Y2, ..., Yk], [D0, D1, ..., Dk) based on the tapeHeads
    def delta(self, tapeHeads):

        # placeholder remove None Later and add code here
        return None

    # δ(q, [X1, X2, ..., Xk]) = (p, [Y1, Y2, ..., Yk], [D0, D1, ..., Dk)
    # p refers to the next state
    # new_tapeHeads refers to the set of pointers of Y that will change from X
    # instructions refers to the set of instructions to be done on the pointers
    def setNext(self, tapeHeads, p, new_tapeHeads, instructions):

        # placeholder remove None Later and add code here
        return None



class MultiTapeTM:

    # Constructor for the MultiTapeTM
    # q refers to the set of all states
    # f refers to the set of all final states
    # sigma refers to set of all input symbols

    # tapeHead refers to the current state (or index of state).
    def __init__(self, q, f, number_of_states, sigma):
        self.q = q
        self.f = f
        self.sigma = sigma

        # Sets up the tapes with [B, ... , B] for all tapes
        # Sets up the pointers to the tapeHeads all to 0
        self.tape = [['B', 'B'] for _ in range(number_of_states)]
        self.tapeHeads = [0 for _ in range(number_of_states)]

    def DeltaHat(self, input_string) -> bool:
        self.tape[0] = ['B'] + list(input_string) + ['B']
        self.tapeHeads[0] = 1



# Example Set Up
q0 = State("q0")
q1 = State("q1")
all_states = [q0, q1]
final_states = [q1]

mtm = MultiTapeTM(all_states, final_states, 3, ['0', '1'])
mtm.DeltaHat('10001')




