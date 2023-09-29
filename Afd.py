import copy


class Afd:

    def __init__(self):
        self.states = set()
        self.alphabet = ""
        self.transitions = dict()
        self.initial = None
        self.finals = set()
        self.__curr_state = None
        self.__error = False

    def error(self):
        return self.__error

    def curr_state(self):
        return self.__curr_state

    def checked_transitions(self, start_id, symbol):
        return (start_id, symbol) in self.transitions

    def create_state(self, key, initial=False, final=False):
        key = int(key)
        self.states.add(key)

        if initial:
            self.initial = key
            self.__curr_state = self.initial
        elif final:
            self.finals.add(key)

    def create_transition(self, origin, symbol, destin):
        symbol = str(symbol)
        origin = int(origin)
        destin = int(destin)
        if symbol not in self.alphabet or origin not in self.states or destin not in self.states:
            return False
        self.transitions[origin, symbol] = destin
        return True

    def create_alphabet(self, alphabet):
        self.alphabet = str(alphabet)

    def is_final(self, id) -> bool:
        return id in self.finals

    def load_afd(self, content):
        state_values = map(int, content[0].split())

        for value in state_values:
            self.create_state(value)

        self.alphabet = ''.join(map(str, content[1]))

        aux = self.alphabet.replace(' ', '')
        n_functions = len(self.states) * (len(aux) - 1)

        for i in range(2, n_functions + 2):
            values = content[i].split()
            origin, symbol, destin = map(int, values)
            self.create_transition(origin, symbol, destin)

        self.create_state(content[n_functions + 2], True)

        state_values = map(int, content[n_functions + 3].split())

        for value in state_values:
            self.create_state(value, False, True)

    def convert_format_file(self):
        content = ' '.join(map(str, self.states)) + '\n'
        content += self.alphabet

        for key, value in self.transitions.items():
            transitions = f"{key[0]} {key[1]} {value}\n"
            content += transitions

        content += str(self.initial) + '\n'
        content += ' '.join(map(str, self.finals)) + '\n'
        return content

    def start(self, word):
        for symbol in word:
            if symbol not in self.alphabet and not self.checked_transitions(self.__curr_state, symbol):
                self.__error = True
                break
            self.__curr_state = self.transitions[(self.__curr_state, symbol)]
        return self.__curr_state

    def copy(self):
        return copy.deepcopy(self)

    def __trivially_valid__(self):
        afd_dict = dict()
        states_list = list(self.states)
        for i in range(1, len(states_list)):
            for j in range(0, i):
                if self.is_final(states_list[i]) != self.is_final(states_list[j]):
                    afd_dict[i, j] = False
                else:
                    afd_dict[i, j] = None
        return afd_dict

    def equivalent_states(self):
        afd_dict = self.__trivially_valid__()
        states_list = list(self.states)

        pendent = True
        change = False
        while pendent and not change:
            change = True
            pendent = True
            for i in range(1, len(states_list)):
                equal = True
                for j in range(0, i):
                    if afd_dict[i, j] is None or afd_dict[i, j] == 'pendent':
                        pendent = False
                        parts = self.alphabet.split()
                        for part in parts:
                            row = self.transitions[i + 1, part] - 1
                            col = self.transitions[j + 1, part] - 1
                            if col > row:
                                col, row = row, col

                            if col != row and afd_dict[row, col] is False:
                                equal = False
                                change = False
                                afd_dict[i, j] = False
                                break
                            elif col != row and (afd_dict[row, col] is None or afd_dict[row, col] == 'pendent'):
                                equal = False
                                change = False
                                afd_dict[i, j] = 'pendent'
                                break
                        if equal:
                            change = False
                            afd_dict[i, j] = True
        self.not_marked(afd_dict)
        return afd_dict

    def not_marked(self, afd_dict):
        for i in range(1, len(list(self.states))):
            for j in range(0, i):
                if afd_dict[i, j] == 'pendent':
                    afd_dict[i, j] = True

    def print_dict(self, afd_dict):
        for i in range(1, len(list(self.states))):
            for j in range(0, i):
                print(afd_dict[i, j], end=" ")
            print()





