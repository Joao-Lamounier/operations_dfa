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


if __name__ == '__main__':
    automato = Afd()
    automato2 = Afd()
    content = read_file('exemple.txt')

    # automato.load_afd(content)
    # write_file('exemple1.txt', automato.convert_format_file())

    automato.create_state(1, initial=True)
    automato.create_state(2, final=True)

    automato.create_alphabet('a b')
    automato.create_transition(1, 'a', 2)
    automato.create_transition(1, 'b', 1)
    automato.create_transition(2, 'a', 1)
    automato.create_transition(2, 'b', 2)

    automato2.create_alphabet('a b')
    automato2.create_state(3, initial=True)
    automato2.create_state(4, final=True)
    automato2.create_state(5)

    automato2.create_alphabet('a b')
    automato2.create_transition(3, 'a', 4)
    automato2.create_transition(3, 'b', 5)
    automato2.create_transition(4, 'a', 3)
    automato2.create_transition(4, 'b', 4)
    automato2.create_transition(5, 'a', 3)
    automato2.create_transition(5, 'b', 4)

    print(automato.is_equivalent(automato2))
    # cadeia = '0'
    # state = automato.start(cadeia)
    #
    # if automato.is_final(state) and not automato.error():
    #     print('aceitou')
    # else:
    #     print('rejeitou')
    #
    # print(automato)
    # automato.print_dict(automato.equivalent_states())
    #
    #
    # copy = automato.copy()
    # write_file('exemple3.txt', copy.convert_format_file())
    # automato.equivalent_states()
    # automato.minimize()
