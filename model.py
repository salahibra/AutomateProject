from graphviz import Digraph
import tools


class Etat:
    def __init__(self, idEtat, labelEtat, typeEtat):
        self.idEtat = idEtat
        self.labelEtat = labelEtat
        self.typeEtat = typeEtat
    def get_idEtat(self):
        return self.idEtat

    def set_labelEtat(self, labelEtat):
        self.labelEtat = labelEtat

    def get_labelEtat(self):
        return self.labelEtat

    def set_typeEtat(self, typeEtat):
        self.typeEtat = typeEtat

    def get_typEtat(self):
        return self.typeEtat
    def __str__(self):
        return f"{self.labelEtat}"
    def __repr__(self):
        return "({})".format(self.idEtat)


class Alphabet:
    def __init__(self, idAlphabet, valAlphabet):
        self.idAlphabet = idAlphabet
        self.valAlphabet = valAlphabet
    def get_idAlphabet(self):
        return self.idAlphabet

    def set_valAlphabet(self, valAlphabet):
        self.valAlphabet = valAlphabet

    def get_valAlphabet(self):
        return self.valAlphabet
    def __str__(self):
        return f"{self.valAlphabet}"
    def __repr__(self):
        return "({})".format(self.valAlphabet)


class Transition:
    def __init__(self, idTransition, etatSource, etatDestination, alphabet):
        self.idTransition = idTransition
        self.etatSource = etatSource
        self.etatDestination = etatDestination
        self.alphabet = alphabet
    def get_idTransition(self):
        return self.idTransition

    def set_etatSource(self, etatSource):
        self.etatSource = etatSource

    def get_etatSource(self):
        return self.etatSource

    def set_etatDestination(self, etatDestination):
        self.etatDestination = etatDestination

    def get_etatDestination(self):
        return self.etatDestination

    def set_alphabet(self, alphabet):
        self.alphabet = alphabet

    def get_alphabet(self):
        return self.alphabet

    def __repr__(self):
        return "({},{},{})".format(self.etatSource, self.alphabet, self.etatDestination)


class Automate:
    def __init__(self, listAlphabets=[], listEtats=[], listInitiaux=[], listFinaux=[], listTransitions=[]):
        self.listAlphabets = listAlphabets
        self.listEtats = listEtats
        self.listInitiaux = listInitiaux
        self.listFinaux = listFinaux
        self.listTransitions = listTransitions
    def ajouter_etat(self, etat):
        if isinstance(etat, Etat):
            self.listEtats.append(etat)

    def supprimer_etat(self, etat):
        if etat in self.listEtats:
            self.listTransitions = [t for t in self.listTransitions if
                                    t.etatSource != etat and t.etatDestination != etat]
            self.listEtats.remove(etat)
            if etat in self.listInitiaux:
                self.listInitiaux.remove(etat)
            if etat in self.listFinaux:
                self.listFinaux.remove(etat)

    def modifier_etat(self, ancien_etat, nouveau_etat):
        index = self.listEtats.index(ancien_etat)
        self.listEtats[index] = nouveau_etat

    def ajouter_alphabet(self, alphabet):
        self.listAlphabets.append(alphabet)

    def supprimer_alphabet(self, alphabet):
        self.listAlphabets.remove(alphabet)
        self.listTransitions = [t for t in self.listTransitions if t.alphabet != alphabet]

    def modifier_alphabet(self, ancien_alphabet, nouveau_alphabet):
        index = self.listAlphabets.index(ancien_alphabet)
        self.listAlphabets[index] = nouveau_alphabet

    def ajouter_transition(self, transition):
        self.listTransitions.append(transition)

    def supprimer_transition(self, transition):
        self.listTransitions.remove(transition)

    def modifier_transition(self, ancienne_transition, nouvelle_transition):
        index = self.listTransitions.index(ancienne_transition)
        self.listTransitions[index] = nouvelle_transition

    def lire_automate(self, liste):
        self.listEtats = []
        self.listInitiaux = []
        self.listFinaux = []
        self.listAlphabets = []
        self.listTransitions = []
        alphabets, etats, initiaux, finaux, transitions = liste
        for i, alphabet in enumerate(alphabets):
            self.ajouter_alphabet(Alphabet(i, alphabet))
        for i, etat in enumerate(etats):
            if etat in finaux and etat in initiaux:
                e = Etat(i+1, etat, "initial-final")
                self.ajouter_etat(e)
                self.listInitiaux.append(e)
                self.listFinaux.append(e)
                continue
            elif etat in initiaux:
                e = Etat(i+1, etat, "initial")
                self.ajouter_etat(e)
                self.listInitiaux.append(e)
            elif etat in finaux:
                e = Etat(i+1, etat, "final")
                self.ajouter_etat(e)
                self.listFinaux.append(e)
            else:
                self.ajouter_etat(Etat(i+1, etat, "intermediate"))
        for i, transition in enumerate(transitions):
            source, alphabet, destination = transition
            etatSource = None
            etatDestination = None
            etiquette = None
            for etat in self.listEtats:
                if source == etat.labelEtat:
                    etatSource = etat
                if destination == etat.labelEtat:
                    etatDestination = etat
            for alpha in self.listAlphabets:
                if alphabet == alpha.valAlphabet:
                    etiquette = alpha
            self.ajouter_transition(Transition(i+1, etatSource, etatDestination, etiquette))

    def afficher_automate(self):
        dot = Digraph()
        for etat in self.listEtats:
            if etat.typeEtat == 'initial-final':
                dot.node(str(etat.idEtat), str(etat), color='blue')
            elif etat.typeEtat == 'initial':
                dot.node(str(etat.idEtat), str(etat), shape='doublecircle', color='green')
            elif etat.typeEtat == 'final':
                dot.node(str(etat.idEtat), str(etat), shape='doublecircle', color='red')
            else:
                dot.node(str(etat.idEtat), str(etat), shape='circle')
        for transition in self.listTransitions:
            dot.edge(str(transition.etatSource.idEtat), str(transition.etatDestination.idEtat),
                     label=transition.alphabet.valAlphabet)
        return dot
    def est_deterministe(self):
        if len(self.listInitiaux) > 1:
            return False
        n = 0
        for etat in self.listEtats:
            for alphabet in self.listAlphabets:
                for transition in self.listTransitions:
                    if transition.etatSource == etat and transition.alphabet == alphabet:
                        n += 1
                if n > 1:
                    return False
                else:
                    n = 0
        return True
    def est_complet(self):
        n = 0
        for etat in self.listEtats:
            for alphabet in self.listAlphabets:
                for transition in self.listTransitions:
                    if transition.etatSource == etat and transition.alphabet == alphabet:
                        n += 1
                if n < 1:
                    return False
                else:
                    n = 0
        return True
    def rendre_complet(self):
        if self.est_complet():
            print(" votre automate est deja complet !")
            return
        n = 0
        etat_puit = Etat(100, 101, "puit")
        for etat in self.listEtats:
            for alphabet in self.listAlphabets:
                for transition in self.listTransitions:
                    if transition.etatSource == etat and transition.alphabet == alphabet:
                        n = 1
                if n == 0:
                    nouveau_transition = Transition(len(self.listTransitions), etat, etat_puit, alphabet)
                    if etat_puit not in self.listEtats:
                        self.ajouter_etat(etat_puit)
                    self.ajouter_transition(nouveau_transition)
                else:
                    n = 0

    def destinations(self, etat, alphabet):  # fonction qui retourne liste des destination de etat-alphabet donne
        listDestinations = []
        for transition in self.listTransitions:
            if transition.etatSource == etat and transition.alphabet == alphabet:
                if transition.etatDestination not in listDestinations:
                    listDestinations.append(transition.etatDestination)
        return listDestinations
    def eliminer_etats_inaccessibles(self):
        etats_marques = [self.listInitiaux[0]]
        for etat in etats_marques:
            for alphabet in self.listAlphabets:
                for transition in self.listTransitions:
                    if transition.etatSource == etat and transition.alphabet == alphabet:
                        if transition.etatDestination not in etats_marques:
                            etats_marques += [transition.etatDestination]
        transitions = [t for t in self.listTransitions if t.etatSource in etats_marques
                       and t.etatDestination in etats_marques]
        initiaux = self.listInitiaux
        terminaux = [e for e in self.listFinaux if e in etats_marques]
        alphabets = self.listAlphabets
        return Automate(alphabets, etats_marques, initiaux, terminaux, transitions)
    def rendre_deterministe(self):
        if self.est_deterministe():
            print("votre automate est deja deterministe")
            return self
        sigma = self.listAlphabets.copy()    # la liste des alphabets
        I = [self.listInitiaux.copy()]   # etat initial
        Q = tools.sous_ensembles(self.listEtats.copy())        # partition Q
        Q = [q for q in Q if q]  # pour eliminer le vide des le debut
        F = []        # les etats finaux de l'automate deterministe
        for p in Q:
            if tools.existe_intersection(self.listFinaux.copy(), p):
                F += [p]
        i = 0
        T = []      # les nouveaux transitions
        for alphabet in sigma:
            for partie in Q:
                destinations = []
                for etat in partie:
                    destinations += self.destinations(etat, alphabet)
                    destinations = list(set(destinations))
                if destinations:
                    for q in Q:
                        if tools.ensembles_egaux(q, destinations):
                            nouveau_transition = Transition(i, partie, q, alphabet)
                            i += 1
                            T = tools.union(T, [nouveau_transition])
        I = [q for q in Q if tools.ensembles_egaux(q, I[0])]
        alphabets = [a.valAlphabet for a in sigma]
        etats = []
        initiaux = []
        finaux = []
        transitions = []
        for q in Q:
            s = ""
            for e in q:
                s += str(e.labelEtat)
            etats.append(s)
        for i in I:
            s = ""
            for j in i:
                s += str(j.labelEtat)
            initiaux.append(s)
        for f in F:
            s = ""
            for g in f:
                s += str(g.labelEtat)
            finaux.append(s)
        for t in T:
            s = ""
            d = ""
            for v in t.etatSource:
                s += str(v.labelEtat)
            for w in t.etatDestination:
                d += str(w.labelEtat)
            transitions.append((s, t.alphabet.valAlphabet, d))
        automate = Automate()
        automate.lire_automate([alphabets, etats, initiaux, finaux, transitions])
        return automate.eliminer_etats_inaccessibles()  # pour simplifier les etats inaccessibles
    def destination(self, etatSource, alphabet):
        for transition in self.listTransitions:
            if transition.etatSource == etatSource and transition.alphabet == alphabet:
                return transition.etatDestination
    def existe_transition(self, ensemble1, ensemble2, alphabet):
        s = False
        for e1 in ensemble1:
            for e2 in ensemble2:
                if self.destination(e1, alphabet) == e2:
                    s = True
                    break
        return s

    def split(self, X, a, Z):
        X_prime = [q for q in X if self.destination(q, a) in Z]
        X_double_prime = [q for q in X if q not in X_prime]
        return X_prime, X_double_prime
    def minimiser(self):
        automate = self
        if not automate.est_complet():
            automate.rendre_complet()
        if not automate.est_deterministe():
            automate = automate.rendre_deterministe()
        # on aura au final un automate deterministe complet accessible
        automate = automate.eliminer_etats_inaccessibles()
        # automate ayant un nombre minimal des etats et qui connait le meme langage
        A = [etat for etat in automate.listFinaux]
        B = [etat for etat in automate.listEtats if etat not in A]
        P = [B, A]        # 0 equivalence
        W = [(min(A, B, key=len), a) for a in automate.listAlphabets]
        while W:
            Z, a = W.pop()
            nouveau_P = []
            for X in P:
                if any(automate.destination(q, a) in Z for q in X):
                    X_prime, X_double_prime = automate.split(X, a, Z)
                    nouveau_P.extend([X_prime, X_double_prime])
                    for b in automate.listAlphabets:
                        if (X, b) in W:
                            W.remove((X, b))
                            W.append((X_prime, b))
                            W.append((X_double_prime, b))
                        else:
                            W.append((min(X_prime, X_double_prime, key=len), b))
                else:
                    nouveau_P.append(X)
            P = nouveau_P

        F = []
        for ensemble in P:
            if tools.existe_intersection(ensemble, automate.listFinaux):
                F.append(ensemble)
        T = []
        i = 0
        for alphabet in automate.listAlphabets:
            for ensemble1 in P:
                for ensemble2 in P:
                    if automate.existe_transition(ensemble1, ensemble2, alphabet):
                        transition = Transition(i, ensemble1, ensemble2, alphabet)
                        i += 1
                        T = tools.union(T, [transition])
        I = []
        for ensemble in P:
            if tools.existe_intersection(ensemble, automate.listInitiaux):
                I.append(ensemble)
        alphabets = [a.valAlphabet for a in automate.listAlphabets]
        etats = []
        initiaux = []
        finaux = []
        transitions = []
        for partie in P:
            s = ""
            for etat in partie:
                s += str(etat.labelEtat)
            if s:
                etats.append(s)
        for i in I:
            s = ""
            for j in i:
                s += str(j.labelEtat)
            initiaux.append(s)
        for f in F:
            s = ""
            for g in f:
                s += str(g.labelEtat)
            finaux.append(s)
        for t in T:
            s = ""
            d = ""
            for v in t.etatSource:
                s += str(v.labelEtat)
            for w in t.etatDestination:
                d += str(w.labelEtat)
            if d and s:
                transitions.append((s, t.alphabet.valAlphabet, d))
        liste = [alphabets, etats, initiaux, finaux, transitions]
        A = Automate()
        A.lire_automate(liste)
        A = A.eliminer_etats_inaccessibles()
        return A
