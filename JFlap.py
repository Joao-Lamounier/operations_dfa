import xml.dom.minidom
from Afd import Afd
from datetime import datetime


class JFlap:

    @staticmethod
    def load(file_name):
        def read_states_nodes():
            states = automaton_tag.getElementsByTagName('state')
            for state in states:
                id = int(state.getAttribute('id'))
                automaton.create_state(id)

                initial = state.getElementsByTagName('initial')
                final = state.getElementsByTagName('final')

                if len(initial) > 0:
                    automaton.initial = id
                if len(final) > 0:
                    automaton.finals.add(id)

        def read_transitions_nodes():
            transitions = automaton_tag.getElementsByTagName('transition')
            for transition in transitions:
                origin = int(transition.getElementsByTagName('from')[0].firstChild.nodeValue)
                destin = int(transition.getElementsByTagName('to')[0].firstChild.nodeValue)
                symbol = str(transition.getElementsByTagName('read')[0].firstChild.nodeValue)
                alphabet.add(symbol)
                automaton.create_transition(origin, symbol, destin, check_alph=False)

        doc = xml.dom.minidom.parse(file_name)
        automaton_tag = doc.getElementsByTagName('automaton')[0]
        alphabet = set()

        automaton = Afd()
        read_states_nodes()
        read_transitions_nodes()
        automaton.create_alphabet(' '.join(map(str, alphabet)))

        return automaton

    @staticmethod
    def save(automaton: Afd):
        def create_states_nodes():
            base_position = 100

            def initialize_states_position():
                return base_position, base_position

            def create_state_attr():
                id = str(state)
                name = "q" + id
                state_tag.setAttribute("id", id)
                state_tag.setAttribute("name", name)

            def get_state_position(cur_x: int, cur_y: int):
                if cur_x % 500 == 0:
                    cur_x = base_position
                    cur_y += base_position
                else:
                    cur_x = base_position * ((i + 1) % 5)

                return cur_x, cur_y

            def create_coordinated_nodes():
                x_tag = doc.createElement("x")
                x_tag.appendChild(doc.createTextNode(str(x)))
                state_tag.appendChild(x_tag)

                y_tag = doc.createElement("y")
                y_tag.appendChild(doc.createTextNode(str(y)))
                state_tag.appendChild(y_tag)

            def set_initial_state_node():
                if automaton.initial == state:
                    initial_tag = doc.createElement("initial")
                    state_tag.appendChild(initial_tag)

            def set_final_state_node():
                if state in automaton.finals:
                    final_tag = doc.createElement("final")
                    state_tag.appendChild(final_tag)

            x, y = initialize_states_position()
            for i, state in enumerate(automaton.states):
                state_tag = doc.createElement("state")
                create_state_attr()
                automaton_tag.appendChild(state_tag)

                x, y = get_state_position(x, y)
                create_coordinated_nodes()

                set_initial_state_node()
                set_final_state_node()

        def create_transitions_nodes():
            def create_from_node():
                from_tag = doc.createElement("from")
                from_tag.appendChild(doc.createTextNode(str(state)))
                transition.appendChild(from_tag)

            def create_to_node():
                to_tag = doc.createElement("to")
                to_tag.appendChild(doc.createTextNode(str(automaton.transitions[state, symbol])))
                transition.appendChild(to_tag)

            def create_read_node():
                read_tag = doc.createElement("read")
                read_tag.appendChild(doc.createTextNode(symbol))
                transition.appendChild(read_tag)

            for state in automaton.states:
                for symbol in automaton.alphabet.split():
                    if not automaton.checked_transitions(state, symbol):
                        break

                    transition = doc.createElement("transition")
                    automaton_tag.appendChild(transition)

                    create_from_node()
                    create_to_node()
                    create_read_node()
        
        doc = xml.dom.minidom.Document()

        root = doc.createElement("structure")
        doc.appendChild(root)

        type_tag = doc.createElement("type")
        type_tag.appendChild(doc.createTextNode("fa"))
        root.appendChild(type_tag)

        automaton_tag = doc.createElement("automaton")
        root.appendChild(automaton)

        create_states_nodes()
        create_transitions_nodes()

        date = datetime.now()
        file_name = date.strftime("%Y%m%d%H%M%S") + '.jff'
        with open(file_name, 'w', encoding='utf-8') as file:
            doc.writexml(file, addindent="\t", newl="\n", encoding='utf-8', standalone=False)

