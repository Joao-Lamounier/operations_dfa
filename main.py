from Afd import Afd


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
        created = automatos[i].create_state(origin, symbol, destin)
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
        file_option = select_file_type()
        i = select_automaton()
        if file_option == 1:
            automatos[i].save_jflap()
        elif file_option == 2:
            pass
    elif option == 14:
        file_option = select_file_type()
        i = select_automaton()
        if file_option == 1:
            automatos[i].load_jflap()
        elif file_option == 2:
            automatos[i].load_afd()
    elif option == 15:
        i = select_automaton()
        afd = automatos[i].copy()
        automatos.append(afd)
        print(f"Automato copiado: {len(automatos) - 1}")


if __name__ == '__main__':
    automatos = []

    while True:
        print(
            " 1 - Criar Automato\n"
            " 2 - Definir Alfabeto\n"
            " 3 - Criar Estado\n"
            " 4 - Criar Transição\n"
            " 5 - Definir Inicial\n"
            " 6 - Denifir Final\n"
            " 7 - Visualizar Automato\n"
            " 8 - Intersecção de Automato\n"
            " 9 - União de Automato\n"
            "10 - Multiplicação de Automato\n"
            "11 - Complemento de Automato\n"
            "12 - Diferença de Automato\n"
            "13 - Salvar Automato\n"
            "14 - Carregar Automato\n"
            "15 - Copiar Automato\n"
            "0 - Sair\n"
        )
        option = int(input("Insira uma opção: "))
        if option == 0:
            break
        menu_option(option)
