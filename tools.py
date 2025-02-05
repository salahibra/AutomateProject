def sous_ensembles(ensemble):
    P = [[]]
    for element in ensemble:
        P = P + [[element] + p for p in P]
    return P


def existe_intersection(ensemble1, ensemble2):
    for element in ensemble1:
        if element in ensemble2:
            return True
    return False


def ensembles_egaux(ensemble1, ensemble2):
    if len(ensemble1) != len(ensemble2):
        return False
    for e1 in ensemble1:
        if e1 in ensemble2:
            continue
        else:
            return False
    return True


def union(s1, s2):
    return list(set(s1) | set(s2))



