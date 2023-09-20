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
    content = read_file('exemple.txt')

    # automato.load_afd(content)
    # write_file('exemple1.txt', automato.convert_format_file())

    automato.create_state(1, True)
    automato.create_state(2, False, True)
    automato.create_state(3)
    automato.create_state(4)
    automato.create_state(5)
    automato.create_state(6, False, True)
    automato.create_alphabet('0 1')
    automato.create_transition(1,0,2)
    automato.create_transition(1,1,3)
    automato.create_transition(2,0,2)
    automato.create_transition(2,1,3)
    automato.create_transition(3,0,5)
    automato.create_transition(3,1,4)
    automato.create_transition(4,0,1)
    automato.create_transition(4,1,3)
    automato.create_transition(5,0,6)
    automato.create_transition(5,1,4)
    automato.create_transition(6,0,2)
    automato.create_transition(6,1,4)

    cadeia = '0'
    state = automato.start(cadeia)

    if automato.is_final(state) and not automato.error():
        print('aceitou')
    else:
        print('rejeitou')

    copy = automato.copy()
    write_file('exemple3.txt', copy.convert_format_file())



