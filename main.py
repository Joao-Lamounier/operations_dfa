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


def op_criar_automato(id_automato):
    op_criar_alfabeto(id_automato)

    n_estd = int(input("Insira quantos estados tera o automato: "))
    for i in range(n_estd):
        op_criar_estado(id_automato)

    n_trans = int(input("Insira quantas transições tera o automato: "))
    for i in range(n_trans):
        op_criar_transicao(id_automato)

    op_criar_est_inicial(id_automato)

    n_finals = int(input("Insira quantos estados finais tera o automato: "))
    for i in range(n_finals):
        op_criar_est_final(id_automato)
    print(f'Id do automato criado: {id_automato}')


def op_criar_alfabeto(id_automato):
    alphabet = input("Insira o alfabeto, separando os símbolos por espaços: ")
    automatos[id_automato].create_alphabet(alphabet)


def op_criar_estado(id_automato):
    state = int(input("Insira o id do estado: "))
    automatos[id_automato].create_state(state)


def op_criar_transicao(id_automato):
    origin = int(input("Insira o id do estado (origem): "))
    destin = int(input("Insira o id do estado (destino): "))
    symbol = input("Insira o símbolo da transição: ")
    created = automatos[id_automato].create_transition(origin, symbol, destin)
    if not created:
        print("Verifique se o símbolo e os estados existem")


def op_criar_est_inicial(id_automato):
    state = int(input("Insira o id do estado inicial: "))
    automatos[id_automato].create_state(state, initial=True)


def op_criar_est_final(id_automato):
    state = int(input("Insira o id do estado final: "))
    automatos[id_automato].create_state(state, final=True)


def menu_option(option):
    if option == 1:
        automatos.append(Afd())
        op_criar_automato(len(automatos) - 1)
    elif option == 2:
        i = select_automaton()
        op_criar_alfabeto(i)
    elif option == 3:
        i = select_automaton()
        op_criar_estado(i)
    elif option == 4:
        i = select_automaton()
        op_criar_transicao(i)
    elif option == 5:
        i = select_automaton()
        op_criar_est_inicial(i)
    elif option == 6:
        i = select_automaton()
        op_criar_est_final(i)
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
