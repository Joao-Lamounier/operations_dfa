class Afd:

    def __init__(self):
        self.states = set()
        self.alphabet = ""
        self.transctions = dict()
        self.inital = None
        self.finals = set()

    def create_state(self, key, initial=False, final=False):
        key = int(key)
        self.states.add(key)

        if initial:
            self.inital = key
        elif final:
            self.finals.add(key)

    def create_transition(self, origin, symbol, destin):
        symbol = str(symbol)
        origin = int(origin)
        destin = int(destin)
        if symbol not in self.alphabet or origin not in self.states or destin not in self.states:
            return False
        self.transctions[origin, symbol] = destin
        return True
    def load_afd(self, content):
        # Salvando o os estados
        state_values = map(int, content[0].split())

        for value in state_values:
            self.create_state(value)

        # Salvando o alfabeto
        self.alphabet = ''.join(map(str, content[1]))

        # Salvando as funções de transição
        aux = self.alphabet.replace(' ', '')
        n_functions = len(self.states) * (len(aux) - 1)

        for i in range(2, n_functions + 2):
            values = content[i].split()
            origin, symbol, destin = map(int, values)
            self.create_transition(origin, symbol, destin)

        #Salvando o estado inicial
        self.create_state(content[n_functions+2], True)

        #Salvando o(s) estado(s) fina(is)l
        state_values = map(int, content[n_functions+3].split())

        for value in state_values:
            self.create_state(value, False, True)
