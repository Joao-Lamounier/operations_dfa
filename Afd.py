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