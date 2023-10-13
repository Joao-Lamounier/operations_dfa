import copy
from enum import Enum


class Afd:
    comparison_status = Enum('ComparisonStatus', ['EQUIVALENT', 'INEQUIVALENT', 'PENDENT'])

    def __init__(self):
        self.states = set()
        self.alphabet = ""
        self.transitions = dict()
        self.initial = None
        self.finals = set()
        self.__curr_state = None
        self.__error = False

    def __str__(self):
        states_str = f"Estados: {', '.join(map(str, self.states))}\n"
        initial_str = f"Estado Inicial: {self.initial}\n"
        final_str = f"Estados Finais: {', '.join(map(str, self.finals))}\n"
        transitions_str = "Transições:\n"
        for (start_id, symbol), end_id in self.transitions.items():
            transitions_str += f"{start_id} --({symbol})--> {end_id}\n"
        return states_str + initial_str + final_str + transitions_str

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
        if final:
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

        n_functions = len(content) - 2

        for i in range(2, n_functions):
            values = content[i].split()
            origin, symbol, destin = map(int, values)
            self.create_transition(origin, symbol, destin)

        self.create_state(content[n_functions], initial=True)

        state_values = map(int, content[n_functions + 1].split())

        for value in state_values:
            self.create_state(value, final=True)

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

    def __trivially_valid(self):
        afd_dict = dict()
        states_list = list(self.states)
        for i in range(1, len(states_list)):
            for j in range(0, i):
                if self.is_final(states_list[i]) != self.is_final(states_list[j]):
                    afd_dict[i, j] = self.comparison_status.INEQUIVALENT
                else:
                    afd_dict[i, j] = None
        return afd_dict

    def equivalent_states(self):
        afd_dict = self.__trivially_valid()
        states_list = list(self.states)
        cs = self.comparison_status

        pendent = True
        change = False
        while pendent and not change:
            change = True
            pendent = True
            for i in range(1, len(states_list)):
                equal = True
                for j in range(0, i):
                    if afd_dict[i, j] is None or afd_dict[i, j] == cs.PENDENT:
                        pendent = False
                        parts = self.alphabet.split()
                        for part in parts:
                            if (i + 1, part) not in self.transitions or (j + 1, part) not in self.transitions:
                                equal = False
                                afd_dict[i, j] = cs.INEQUIVALENT
                                break
                            row = self.transitions[i + 1, part] - 1
                            col = self.transitions[j + 1, part] - 1
                            if col > row:
                                col, row = row, col

                            if col != row and afd_dict[row, col] is cs.INEQUIVALENT:
                                equal = False
                                change = False
                                afd_dict[i, j] = cs.INEQUIVALENT
                                break
                            elif col != row and (afd_dict[row, col] is None or afd_dict[row, col] == cs.PENDENT):
                                equal = False
                                change = False
                                afd_dict[i, j] = cs.PENDENT
                                break
                        if equal:
                            change = False
                            afd_dict[i, j] = cs.EQUIVALENT
        self.__not_marked(afd_dict)
        return afd_dict

    def __not_marked(self, afd_dict):
        for i in range(1, len(list(self.states))):
            for j in range(0, i):
                if afd_dict[i, j] == self.comparison_status.PENDENT:
                    afd_dict[i, j] = self.comparison_status.EQUIVALENT

    def get_disconnected(self):
        states_cpy = self.states.copy()
        for state in self.states:
            for symbol in self.alphabet.split():
                if (state, symbol) in self.transitions:
                    rm_state = self.transitions[(state, symbol)]
                    if rm_state in states_cpy:
                        states_cpy.remove(rm_state)

        return states_cpy

    def minimize(self):
        self.states = self.states.symmetric_difference(self.get_disconnected())
        afd_dict = self.equivalent_states()
        state_list = list(self.states)
        cs = self.comparison_status
        mapper = dict()

        for i in range(1, len(state_list)):
            for j in range(0, i):
                if afd_dict[i, j] == cs.EQUIVALENT:
                    rm_state, state = i, j
                    if state_list[i] == self.initial:
                        state, rm_state = rm_state, state
                    mapper[state_list[rm_state]] = state_list[state]

        if len(list(mapper)) == 0:
            return

        for state in self.states:
            for symbol in self.alphabet.split():
                key = (state, symbol)
                if key in self.transitions:
                    if state in mapper:
                        self.transitions.pop(key)
                    elif self.transitions[key] in mapper:
                        key_map = mapper[self.transitions[key]]
                        while key_map in mapper:
                            key_map = mapper[key_map]
                        self.transitions[key] = key_map


    def print_dict(self, afd_dict):
        for i in range(1, len(list(self.states))):
            for j in range(0, i):
                print(afd_dict[i, j].name[0], end=" ")
            print()

    def is_equivalent(self, afd):
        alphabet1 = self.alphabet.split()
        alphabet2 = afd.alphabet.split()

        if len(set(alphabet1).symmetric_difference(alphabet2)) != 0:
            return self.comparison_status.INEQUIVALENT.name

        afd_concat = Afd()
        afd_concat.create_alphabet(self.alphabet)
        size = len(list(self.states))

        x = self.__rename_states(afd_concat, self, 1)
        y = self.__rename_states(afd_concat, afd, size)

        equivalences = afd_concat.__equivalent_states()

        return equivalences[y, x].name

    @staticmethod
    def __rename_states(afd1, afd2, prefix=0):
        x = 0
        backup = dict()
        for i, state in enumerate(afd2.states):
            afd1.create_state(i + prefix, final=afd2.is_final(state))
            backup[state] = i + prefix
            if afd2.initial == state:
                x = backup[afd2.initial]

        for i, state in enumerate(afd2.states):
            for symbol in afd2.alphabet.split():
                destin = backup[afd2.transitions[(state, symbol)]]
                afd1.create_transition(i + prefix, symbol, destin)

        return x
