from Afd import Afd
from JFlap import JFlap

def read_file(file_name: str):
    try:
        with open(file_name, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f'O arquivo "{file_name}" não foi encontrado.')


def write_file(file_name: str, content: str):
    try:
        with open(file_name, 'w') as file:
            file.write(content)
    except Exception:
        raise print(f'Não foi possível escrever em "{file_name}"')


def select_automaton():
    ids = range(len(automatos))
    i = int(input(f"Selecione o automato ({', '.join(map(str, ids))}): "))
    return i


def select_file_type():
    option = int(input(
        "1 - JFlap\n"
        "2 - Texto\n"
        "Selecione uma opção: \n"
    ))
    return option


def menu_option(option):
    if option == 1:
        automatos.append(Afd())
    elif option == 2:
        i = select_automaton()
        alphabet = input("Insira o alfabeto, separando os símbolos por espaços: ")
        automatos[i].create_alphabet(alphabet)
    elif option == 3:
        i = select_automaton()
        state = int(input("Insira o id do estado: "))
        automatos[i].create_state(state)
    elif option == 4:
        i = select_automaton()
        origin = int(input("Insira o id do estado (origem): "))
        destin = int(input("Insira o id do estado (destino): "))
        symbol = input("Insira o símbolo da transição: ")
        created = automatos[i].create_transition(origin, symbol, destin)
        if not created:
            print("Verifique se o símbolo e os estados existem")
    elif option == 5:
        i = select_automaton()
        state = int(input("Insira o id do estado: "))
        automatos[i].create_state(state, initial=True)
    elif option == 6:
        i = select_automaton()
        state = int(input("Insira o id do estado: "))
        automatos[i].create_state(state, final=True)
    elif option == 7:
        i = select_automaton()
        print(automatos[i])
    elif option == 8:
        i = select_automaton()
        j = select_automaton()
        afd = automatos[i].intersection(automatos[j])
        automatos.append(afd)
        print(f"Automato intersecção: {len(automatos) - 1}")
    elif option == 9:
        i = select_automaton()
        j = select_automaton()
        afd = automatos[i].union(automatos[j])
        automatos.append(afd)
        print(f"Automato união: {len(automatos) - 1}")
    elif option == 10:
        i = select_automaton()
        j = select_automaton()
        afd = automatos[i].multiply(automatos[j])
        automatos.append(afd)
        print(f"Automato multiplicação: {len(automatos) - 1}")
    elif option == 11:
        i = select_automaton()
        afd = automatos[i].complement()
        automatos.append(afd)
        print(f"Automato complemento: {len(automatos) - 1}")
    elif option == 12:
        i = select_automaton()
        j = select_automaton()
        afd = automatos[i].difference(automatos[j])
        automatos.append(afd)
        print(f"Automato diferença: {len(automatos) - 1}")
    elif option == 13:
        i = select_automaton()
        automatos[i].print_dict()
    elif option == 14:
        i = select_automaton()
        j = select_automaton()
        print(automatos[i].is_equivalent(automatos[j]))
    elif option == 15:
        i = select_automaton()
        automatos[i].minimize()
        print(f"Automato minimizado: {i}")
    elif option == 16:
        file_option = select_file_type()
        i = select_automaton()
        if file_option == 1:
            JFlap.save(automatos[i])
        elif file_option == 2:
            automatos[i].save()
    elif option == 17:
        file_option = select_file_type()
        i = select_automaton()
        file_name = input('Insira o nome do arquivo: ')
        if file_option == 1:
            JFlap.load(file_name)
        elif file_option == 2:
            automatos[i].load(file_name)
    elif option == 18:
        i = select_automaton()
        afd = automatos[i].copy()
        automatos.append(afd)
        print(f"Automato copiado: {len(automatos) - 1}")


if __name__ == '__main__':
    automatos = []
    automato = Afd()
    automato2 = Afd()

    automato.create_state(1, initial=True, final=True)
    automato.create_state(2)
    automato.create_state(3, final=True)

    automato.create_alphabet('a b')
    automato.create_transition(1, 'a', 2)
    automato.create_transition(1, 'b', 3)
    automato.create_transition(2, 'a', 1)
    automato.create_transition(2, 'b', 2)
    automato.create_transition(3, 'a', 2)
    automato.create_transition(3, 'b', 3)

    automato2.create_alphabet('a b')
    automato2.create_state(1, initial=True)
    automato2.create_state(2, final=True)
    automato2.create_state(3)

    automato2.create_transition(1, 'a', 2)
    automato2.create_transition(1, 'b', 3)
    automato2.create_transition(2, 'a', 1)
    automato2.create_transition(2, 'b', 2)
    automato2.create_transition(3, 'a', 1)
    automato2.create_transition(3, 'b', 2)
    afd = automato.difference(automato2)
    automatos.append(automato)
    automatos.append(automato)
    automatos.append(afd)

    while True:
        print(
            "╭────────────────────────────────────────╮\n"
            "│            MENU PRINCIPAL              │\n"
            "├────────────────────────────────────────┤\n"
            "│ 1 - Criar Autômato                     │\n"
            "│ 2 - Definir Alfabeto                   │\n"
            "│ 3 - Criar Estado                       │\n"
            "│ 4 - Criar Transição                    │\n"
            "│ 5 - Definir Inicial                    │\n"
            "│ 6 - Definir Final                      │\n"
            "│ 7 - Visualizar Autômato                │\n"
            "│ 8 - Intersecção de Autômatos           │\n"
            "│ 9 - União de Autômatos                 │\n"
            "│10 - Multiplicação de Autômatos         │\n"
            "│11 - Complemento de Autômato            │\n"
            "│12 - Diferença de Autômatos             │\n"
            "│13 - Calcular estados equivalentes      │\n"
            "│14 - Equivalência entre autômatos       │\n"
            "│15 - Minimização de Autômato            │\n"
            "│16 - Salvar Autômato                    │\n"
            "│17 - Carregar Autômato                  │\n"
            "│18 - Copiar Autômato                    │\n"
            "│ 0 - Sair                               │\n"
            "╰────────────────────────────────────────╯\n"
        )
        option = int(input("Insira uma opção: "))
        if option == 0:
            break
        menu_option(option)

