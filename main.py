from Afd import Afd


def read_file(file_name: str):
    try:
        with open(file_name, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f'O arquivo "{file_name}" não foi encontrado.')



if __name__ == '__main__':
    automato = Afd()
    content = read_file('exemple.txt')

    automato.load_afd(content)
    print(automato.states)
    print(automato.alphabet)
    print(automato.transctions)
    print(automato.inital)
    print(automato.finals)

