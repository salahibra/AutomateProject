from model import Etat, Transition, Automate, Alphabet
import re


class SimpleInterpreter:
    def __init__(self):
        self.variables = {}
        self.automate = Automate()
        self.current_state = None
        self.setup_automate()

    def setup_automate(self):
        # Initialiser les états de l'automate
        etat_neutre = Etat("neutre", "etat_neutre", "initial")
        etat_if = Etat("if", "etat_if", "intermediate")
        etat_while = Etat("while", "etat_while", "intermediate")
        etat_for = Etat("for", "etat_for", "intermediate")
        etat_var = Etat("assignement", "etat_var", "intermediate")
        etat_print = Etat("print", "etat_print", "intermediate")

        # Ajouter les états à l'automate
        self.automate.ajouter_etat(etat_neutre)
        self.automate.ajouter_etat(etat_if)
        self.automate.ajouter_etat(etat_while)
        self.automate.ajouter_etat(etat_for)
        self.automate.ajouter_etat(etat_var)
        self.automate.ajouter_etat(etat_print)

        # Initialiser les alphabets
        alpha_if = Alphabet(0, "if")
        alpha_while = Alphabet(1, "while")
        alpha_for = Alphabet(2, "for")
        alpha_var = Alphabet(3, "var")
        alpha_return = Alphabet(4, "return")
        alpha_print = Alphabet(5, "print")  # Ajout de l'alphabet pour l'instruction print

        # Ajouter les alphabets à l'automate
        self.automate.ajouter_alphabet(alpha_if)
        self.automate.ajouter_alphabet(alpha_while)
        self.automate.ajouter_alphabet(alpha_for)
        self.automate.ajouter_alphabet(alpha_var)
        self.automate.ajouter_alphabet(alpha_return)
        self.automate.ajouter_alphabet(alpha_print)  # Ajouter l'alphabet à l'automate

        # Ajouter les transitions
        self.automate.ajouter_transition(Transition(0, etat_neutre, etat_if, alpha_if))
        self.automate.ajouter_transition(Transition(1, etat_neutre, etat_while, alpha_while))
        self.automate.ajouter_transition(Transition(2, etat_neutre, etat_for, alpha_for))
        self.automate.ajouter_transition(Transition(3, etat_neutre, etat_var, alpha_var))
        self.automate.ajouter_transition(Transition(4, etat_if, etat_neutre,
                                                    alpha_return))  # Transition pour retourner à l'état neutre depuis etat_if
        self.automate.ajouter_transition(Transition(5, etat_while, etat_neutre,
                                                    alpha_return))  # Transition pour retourner à l'état neutre depuis etat_while
        self.automate.ajouter_transition(Transition(6, etat_for, etat_neutre,
                                                    alpha_return))  # Transition pour retourner à l'état neutre depuis etat_for
        self.automate.ajouter_transition(Transition(7, etat_var, etat_neutre,
                                                    alpha_return))  # Transition pour retourner à l'état neutre depuis etat_var
        self.automate.ajouter_transition(Transition(8, etat_print, etat_neutre, alpha_return))
        self.automate.ajouter_transition(Transition(8, etat_neutre, etat_print, alpha_print))

        # Définir l'état initial
        self.current_state = etat_neutre

    def parse_and_execute(self, code):
        # Pré-traiter le code pour le diviser en lignes et enlever les espaces inutiles
        code = self.preprocess_code(code)
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        index = 0
        while index < len(lines):
            line = lines[index]
            if line.startswith('if'):
                # Exécuter l'état if
                self.current_state = self.automate.destination(self.current_state, Alphabet(0, "if"))
                index = self.execute_if(line, lines, index)
            elif line.startswith('while'):
                # Exécuter l'état while
                self.current_state = self.automate.destination(self.current_state, Alphabet(1, "while"))
                index = self.execute_while(line, lines, index)
            elif line.startswith('for'):
                # Exécuter l'état for
                self.current_state = self.automate.destination(self.current_state, Alphabet(2, "for"))
                index = self.execute_for(line, lines, index)
            elif line.startswith('print'):
                # Exécuter l'instruction print
                self.current_state = self.automate.destination(self.current_state, Alphabet(5, "print"))
                self.execute_print(line)
            else:
                # Exécuter l'état var
                self.current_state = self.automate.destination(self.current_state, Alphabet(3, "var"))
                self.execute_assignment(line)
                # Revenir à l'état neutre après l'exécution de la commande
            index += 1
        # Revenir à l'état neutre après l'exécution de toutes les commandes
        self.current_state = self.automate.destination(self.current_state, Alphabet(4, "return"))
    def preprocess_code(self, code):
        # Ajouter des espaces autour du "=" uniquement pour l'affectation de variables
        code = re.sub(r'(\S)(=)(\S)', r'\1 \2 \3', code)
        return code

    def execute_assignment(self, line):
        if self.current_state != self.automate.destination(self.current_state, Alphabet(3, "var")):
            return  # Retourner à l'état initial si l'état actuel ne correspond pas
        if '=' not in line:
            return  # Ignorer les lignes qui ne contiennent pas d'affectation de variable

        # Séparer la variable et l'opérateur d'affectation/expression
        parts = line.split('=')
        var = parts[0].strip()
        expr = parts[1].strip()
        if var not in self.variables:
            self.variables[var] = 0
            # Vérifier s'il s'agit d'une opération d'incrémentation, de décrémentation, de multiplication ou de division
        if '+=' in expr:
            expr_parts = expr.split('+=')
            self.variables[var] += self.evaluate_expression(expr_parts[1].strip())
        elif '-=' in expr:
            expr_parts = expr.split('-=')
            self.variables[var] -= self.evaluate_expression(expr_parts[1].strip())
        elif '*=' in expr:
            expr_parts = expr.split('*=')
            self.variables[var] *= self.evaluate_expression(expr_parts[1].strip())
        elif '/=' in expr:
            expr_parts = expr.split('/=')
            self.variables[var] /= self.evaluate_expression(expr_parts[1].strip())
        else:
            # Affectation simple
            self.variables[var] = self.evaluate_expression(expr)

    def execute_if(self, line, lines, index):
        # Vérifie l'état actuel
        if self.current_state != self.automate.destination(self.current_state, Alphabet(0, "if")):
            return index  # Retourner l'index actuel si l'état actuel ne correspond pas

        start_idx = index
        line_if = lines[start_idx]
        if_indent = len(line_if) - len(line_if.lstrip())
        end_idx = 0
        # Trouver la fin du bloc
        for idx in range(start_idx , len(lines)):
            line_if = lines[idx]
            if len(line_if.strip()) == 0:  # Ignorer les lignes vides
                continue
            current_indent = len(line_if) - len(line_if.lstrip())
            if current_indent == if_indent and (line_if.startswith('elif') or line_if.startswith('else')):
                linesd = [line for line in code.strip().split('\n') if line.strip()]
                block, idx = self.extract_block(linesd, idx)
                end_idx = idx

        condition = line[line.index('(') + 1:line.index(')')].strip()
        linesd = [line for line in code.strip().split('\n') if line.strip()]
        block, index = self.extract_block(linesd, index )

        if self.evaluate_condition(condition):
            block_lines = block.strip().split('\n')

            # Itérer sur chaque ligne et exécuter l'affectation
            for lin in block_lines:
                self.execute_assignment(lin)
            return end_idx
        # Parcourir les lignes suivantes pour trouver les blocs if, elif et else
        while index < len(lines):
            next_line = lines[index].strip()
            if next_line.startswith('if') or next_line.startswith('elif') or next_line.startswith('else'):
                if next_line.startswith('if'):
                    # Extraire la condition de if
                    if_condition = next_line[next_line.index('(') + 1:next_line.index(')')].strip()
                    # Vérifier si la condition if est vraie
                    if self.evaluate_condition(if_condition):
                        # Exécuter le bloc if
                        block, index = self.extract_block(linesd, index)
                        block_lines = block.strip().split('\n')

                        # Itérer sur chaque ligne et exécuter l'affectation
                        for lin in block_lines:
                            self.execute_assignment(lin)
                        return end_idx
                    index += 1
                elif next_line.startswith('elif'):
                    # Extraire la condition de elif
                    elif_condition = next_line[next_line.index('(') + 1:next_line.index(')')].strip()
                    # Vérifier si la condition elif est vraie
                    if self.evaluate_condition(elif_condition):
                        # Exécuter le bloc elif
                        block, index = self.extract_block(linesd, index)
                        block_lines = block.strip().split('\n')

                        # Itérer sur chaque ligne et exécuter l'affectation
                        for lin in block_lines:
                            self.execute_assignment(lin)
                        return end_idx
                    index += 1
                elif next_line.startswith('else'):
                    # Exécuter le bloc elif
                    block, index = self.extract_block(linesd, index)
                    block_lines = block.strip().split('\n')
                    # Itérer sur chaque ligne et exécuter l'affectation
                    for lin in block_lines:
                        self.execute_assignment(lin)
                    return end_idx
            else:
                break
        return end_idx

    def execute_while(self, line, lines, index):
        if self.current_state != self.automate.destination(self.current_state, Alphabet(1, "while")):
            return 0  # Retourner à l'état initial si l'état actuel ne correspond pas
        condition = line[line.index('(') + 1:line.index(')')].strip()
        linesd = [line for line in code.strip().split('\n') if line.strip()]
        block, index = self.extract_block(linesd, index )
        while self.evaluate_condition(condition):
            block_lines = block.strip().split('\n')

            # Itérer sur chaque ligne et exécuter l'affectation
            for lin in block_lines:
                self.execute_assignment(lin)
        return index

    def execute_for(self, line, lines, index):
        # Vérifier l'état de l'automate pour la boucle for
        if self.current_state != self.automate.destination(self.current_state, Alphabet(2, "for")):
            return 0  # Retourner à l'état initial si l'état actuel ne correspond pas
        # Extraire le contenu entre les parenthèses du for
        for_declaration = line[line.index('(') + 1:line.index(')')].strip()
        linesd = [line for line in code.strip().split('\n') if line.strip()]
        # Initialiser iterable et variable
        iterable = None
        var = None
        values = [int(x.strip()) for x in for_declaration.split(',')]

        # Si la ligne contient un 'in', alors nous avons une variable et un itérable

        # Extraire le bloc de code du for
        block, index = self.extract_block(linesd, index)
        for var in range(*values):
            block_lines = block.strip().split('\n')
            # Itérer sur chaque ligne et exécuter l'affectation
            for lin in block_lines:
                self.execute_assignment(lin)

        # Revenir à l'état neutre après l'exécution du for
        self.current_state = self.automate.destination(self.current_state, Alphabet(4, "return"))

        return index

    def evaluate_expression(self, expr):
        try:
            # Remplacer les noms de variables par leurs valeurs dans l'expression
            for var, val in self.variables.items():
                expr = expr.replace(var, str(val))
            # Évaluer l'expression en utilisant la fonction eval
            return eval(expr)
        except Exception as e:
            raise ValueError(f"Erreur lors de l'évaluation de l'expression '{expr}': {e}")

    def evaluate_condition(self, condition):
        try:
            # Remplacer les noms de variables par leurs valeurs dans la condition
            for var, val in self.variables.items():
                condition = condition.replace(var, str(val))
            # Évaluer la condition en utilisant la fonction eval
            return eval(condition)
        except Exception as e:
            raise ValueError(f"Erreur lors de l'évaluation de la condition '{condition}': {e}")

    def extract_block(self, lines, index):
        start_idx = index + 1
        line = lines[start_idx]
        block_indent = len(line) - len(line.lstrip())

        # Trouver la fin du bloc
        for idx in range(start_idx, len(lines)):
            line = lines[idx]
            if len(line.strip()) == 0:  # Ignorer les lignes vides
                continue
            current_indent = len(line) - len(line.lstrip())
            if current_indent < block_indent:
                end_idx = idx
                break
        else:
            end_idx = len(lines)  # Aller jusqu'à la fin si aucun autre bloc de même niveau n'est trouvé
        index = end_idx  - 1
        # Exclure la ligne de début du bloc
        return '\n'.join(lines[start_idx:end_idx]), index

    def execute_print(self, line):
        if self.current_state != self.automate.destination(self.current_state, Alphabet(5, "print")):
            return  # Retourner à l'état initial si l'état actuel ne correspond pas
        # Extraire les parties de la ligne print entre les parenthèses
        parts = re.findall(r"'([^']*)'|\"([^\"]*)\"|(\w+)", line)
        printed_values = []
        for part in parts:
            if part[0]:
                # Si la partie est entre guillemets simples, ajouter la chaîne de caractères à la liste des valeurs imprimées
                printed_values.append(part[0])
            elif part[1]:
                # Si la partie est entre guillemets doubles, ajouter la chaîne de caractères à la liste des valeurs imprimées
                printed_values.append(part[1])
            elif part[2] and part[2] != "print":  # Vérifier si la partie est une variable et n'est pas 'print'
                # Si la partie est une variable, évaluer son expression et ajouter la valeur à la liste des valeurs imprimées
                var = part[2]
                if var in self.variables:
                    printed_values.append(str(self.variables[var]))
                else:
                    raise ValueError(f"Variable '{var}' is not defined.")
        # Afficher les valeurs imprimées séparées par des espaces
        print(" ".join(printed_values))
    def afficher__automate(self):
        print("liste des États:", self.automate.listEtats)
        print("liste des Alphabets:", self.automate.listAlphabets)
        print("liste des Transitions:", self.automate.listTransitions)


# Exemple de code à exécuter
code = """
x = 6
z = 1
if (x == 6):
    y = 2
    x = 4
else:
    y = 0
for i in range(0, 6):
    z = z + 1
while (x < 5):
    x = x + 1
    y = y * 2 + 2
print('x = ', x)
"""

interpreter = SimpleInterpreter()
interpreter.parse_and_execute(code)
print(interpreter.variables)

# Utilisation de l'automate
interpreter.afficher__automate()
# Affichage de l'automate sous forme de graphe
dot = interpreter.automate.afficher_automate()
dot.render("affichage automate_interpreter", format='png', view=True)


