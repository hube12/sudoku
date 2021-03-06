from browser.local_storage import storage
import sys, time, random
from copy import deepcopy

def chooseRandom(matrix):
    for loop in range(17):
        w = random.randint(0, 80)
        n = random.randint(0, 1000)
        while matrix[w // 9][w % 9] != 0 or (n % 10) == 0:
            w = random.randint(0, 80)
            n = random.randint(0, 1000)
        matrix[w // 9][w % 9] = n % 10
    return matrix


def checkIt(matrix):
    if matrix == None or matrix == []:
        return False
    for i in range(2):
        for y in range(9):
            ligne = []
            for x in range(9):
                if i == 1 and matrix[x][y] != 0:
                    ligne.append(matrix[x][y])
                elif i == 0 and matrix[y][x] != 0:
                    ligne.append(matrix[y][x])
            for x in range(1, 10):
                try:
                    ligne.pop(ligne.index(x))
                except:
                    pass
            if len(ligne) > 0:
                return False
    for i in range(9):
        y = i % 3 * 3
        x = i // 3 * 3
        temp = []
        for j in range(3):
            for k in range(3):
                if matrix[y + j][x + k] != 0:
                    temp.append(matrix[y + j][x + k])
        for x in range(1, 10):
            try:
                temp.pop(temp.index(x))
            except:
                pass
        if len(temp) > 0:
            return False
        '''temp.sort()
        if temp!=list(map(int,range(1,10))):
            print(temp)
            return False #pour quand il est complet'''
    return True


def outpuIt(matrix):
    for i in matrix:
        print(" ".join(map(str, i)))


def resolveIt(matrix):
    # remplissage des colonnes et lignes manquant 1 élément
    subdivision = []
    for i in range(2):
        colonne = []
        for y in range(9):
            ligne = []
            vide = []
            for x in range(9):
                if i == 1:
                    if matrix[x][y] != 0:
                        ligne.append(matrix[x][y])
                    else:
                        vide.append((x, y))
                else:
                    if matrix[y][x] != 0:
                        ligne.append(matrix[y][x])
                    else:
                        vide.append((y, x))
            colonne.append((ligne, vide))
            if len(ligne) == 8:
                for m in range(1, 10):
                    try:
                        ligne.pop(ligne.index(m))
                    except:
                        matrix[vide[0][0]][vide[0][1]] = m
                        return vide[0], matrix
        subdivision.append(colonne)
    total = []
    # remplissage des sections manquant 1 élément
    for i in range(9):
        y = i % 3 * 3
        x = i // 3 * 3
        temp = []
        vide = []
        for j in range(3):
            for k in range(3):
                if matrix[y + j][x + k] != 0:
                    temp.append(matrix[y + j][x + k])
                else:
                    vide.append((y + j, x + k))
        total.append((temp, vide))
        if len(temp) == 8:
            for m in range(1, 10):
                try:
                    temp.pop(temp.index(m))
                except:
                    matrix[vide[0][0]][vide[0][1]] = m
                    return vide[0], matrix
    subdivision.append(total)
    return computation(subdivision, matrix)


def computation(s, matrix):
    ligne = s[0]
    colonne = s[1]
    section = s[2]
    # tests de solution evidente via la methode des colonnes et lignes (cas d'une restrictions unique)
    # maxi 6561 itérations (meme si ce nombre est impossible en moyenne)
    # test des colonnes
    for j in range(3):
        # selection case
        for i in range(1, 10):
            # selection des nombres
            for l in range(3):

                # selection des lignes/colonnes dans la case dont deux contiennent le nombre
                if (i in colonne[j * 3 + l][0]) and (i in colonne[j * 3 + ((l + 1) % 3)][0]) and not (
                            i in colonne[j * 3 + ((l + 2) % 3)][0]):
                    for m in range(3):
                        if not (i in section[m + j * 3][0]):
                            # on est dans le cas où entre deux lignes on en a une ou il manque un nombre precis ici i
                            partieInteressante = []
                            localSection = section[m + j * 3][1]
                            l1 = j * 3 + l
                            l2 = j * 3 + ((l + 1) % 3)
                            for k in range(len(localSection)):
                                if not (localSection[k][1] == l1 or localSection[k][1] == l2):
                                    partieInteressante.append(localSection[k])
                            # can be simplified be much more readable as it
                            if len(partieInteressante) > 0:
                                # on a va pouvoir remplir enfin la grille
                                if len(partieInteressante) == 1:
                                    matrix[partieInteressante[0][0]][partieInteressante[0][1]] = i
                                    return partieInteressante[0], matrix
                                elif len(partieInteressante) == 2:
                                    c1 = ligne[partieInteressante[0][0]][0]
                                    c2 = ligne[partieInteressante[1][0]][0]
                                    if i in c1:
                                        matrix[partieInteressante[1][0]][partieInteressante[1][1]] = i
                                        return partieInteressante[1], matrix
                                    if i in c2:
                                        matrix[partieInteressante[0][0]][partieInteressante[0][1]] = i
                                        return partieInteressante[0], matrix
                                else:
                                    cTot = [ligne[partieInteressante[0][0]][0], ligne[partieInteressante[1][0]][0],
                                            ligne[partieInteressante[2][0]][0]]
                                    for n in range(3):
                                        if i in cTot[n] and i in cTot[(n + 1) % 3]:
                                            matrix[partieInteressante[(n + 2) % 3][0]][
                                                partieInteressante[(n + 2) % 3][1]] = i
                                            return partieInteressante[(n + 2) % 3], matrix
    # test des lignes
    for j in range(3):
        # selection case
        for i in range(1, 10):
            # selection des nombres
            for l in range(3):
                # selection des lignes/colonnes dans la case dont deux contiennent le nombre
                if (i in ligne[j * 3 + l][0]) and (i in ligne[j * 3 + ((l + 1) % 3)][0]) and not (
                            i in ligne[j * 3 + ((l + 2) % 3)][0]):
                    for m in range(3):
                        if not (i in section[m * 3 + j][0]):
                            # on est dans le cas où entre deux lignes on en a une ou il manque un nombre precis ici i
                            partieInteressante = []
                            localSection = section[m * 3 + j][1]
                            l1 = j * 3 + l
                            l2 = j * 3 + ((l + 1) % 3)
                            for k in range(len(localSection)):
                                if not (localSection[k][0] == l1 or localSection[k][0] == l2):
                                    partieInteressante.append(localSection[k])
                            if len(partieInteressante) > 0:
                                if len(partieInteressante) == 1:
                                    # on a va pouvoir remplir enfin la grille
                                    matrix[partieInteressante[0][0]][partieInteressante[0][1]] = i
                                    return partieInteressante[0], matrix
                                elif len(partieInteressante) == 2:
                                    c1 = colonne[partieInteressante[0][1]][0]
                                    c2 = colonne[partieInteressante[1][1]][0]
                                    if i in c1:
                                        matrix[partieInteressante[1][0]][partieInteressante[1][1]] = i
                                        return partieInteressante[1], matrix
                                    if i in c2:
                                        matrix[partieInteressante[0][0]][partieInteressante[0][1]] = i
                                        return partieInteressante[0], matrix
                                else:
                                    cTot = [colonne[partieInteressante[0][1]][0], colonne[partieInteressante[1][1]][0],
                                            colonne[partieInteressante[2][1]][0]]
                                    for n in range(3):
                                        if i in cTot[n] and i in cTot[(n + 1) % 3]:
                                            matrix[partieInteressante[(n + 2) % 3][0]][
                                                partieInteressante[(n + 2) % 3][1]] = i
                                            return partieInteressante[(n + 2) % 3], matrix
    # Ce module est aléatoire en se basant sur les plus basse  possibilité mais en réalité j'etais tellement faineant que je n'est pas implementé
    # l'impossibilité de terminer le sudoku dans le cas d'un mauvais mouvement disons par exmple un restreint a une ligne dans une case alors que
    # cette ligne comporte 3 sur cette case d'ou pas possible de jouer ce numero
    t = 9
    v = []
    for i in range(9):
        for j in range(9):
            point = matrix[i][j]
            possibilité = []
            if point == 0:
                l = ligne[i][0]
                c = colonne[j][0]
                s = section[j // 3 * 3 + i // 3][0]
                for k in range(1, 10):
                    if not (k in l or k in c or k in s):
                        possibilité.append(k)
                if len(possibilité) == 0:
                    return (-1, -1), None
                if len(possibilité) <= t:
                    t = len(possibilité)
                    v.append((possibilité, (i, j)))
    if len(v) == 0:
        return (-1, -1), None
    choix = v[len(v) - 1]
    w = random.randint(0, len(choix[0]) - 1)
    nbr = choix[0][w]
    matrix[choix[1][0]][choix[1][1]] = nbr
    return choix[1], matrix


def go():
    pass
    for i in range(9):
        if len(ligne[i][0]) > t:
            t = len(ligne[i][0])
            v = ligne[i][0]
        if len(colonne[i][0]) > t:
            t = len(colonne[i][0])
            v = colonne[i][0]
        if len(section[i][0]) > t:
            t = len(section[i][0])
            v = section[i][0]




def main(matrix,g,traceback):
    i=17
    tracebackMoove=[]
    b=0
    while i < 81:
        mouvement, matrix = resolveIt(matrix)
        v = 0
        while not checkIt(matrix):
            if b>1000:
                return "error","error"
            b+=1
            if v > 3 or matrix is None:
                # on est dans le cas où toutes les solutions aléatoires on été essayées
                # on revient en arrière de 1
                i -= 1
                v = 0
                traceback.pop()

            if traceback == []:
                traceback = deepcopy(g)
                i=17
            matrix = traceback[-1]

            mouvement, matrix = resolveIt(matrix)
            v += 1
        # on a fait une etape correcte mais on est pas sur qu'elle n'influera pas la fin d'ou le traceback
        traceback.append(matrix)
        tracebackMoove.append(mouvement)
        i += 1
    outpuIt(matrix)

    return traceback,tracebackMoove
v="error"
while v=="error":
    matrix = [[0] * 9 for i in range(9)]
    matrix = chooseRandom(matrix)
    while not checkIt(matrix):
        matrix = [[0] * 9 for i in range(9)]
        matrix = chooseRandom(matrix)


    traceback=[deepcopy(matrix)]
    globalTraceback=deepcopy(traceback)
    v,w=main(matrix,globalTraceback,traceback)
from browser.object_storage import ObjectStorage

object_storage = ObjectStorage(storage)
object_storage[["start"]] = globalTraceback[0]
object_storage[["fin"]] = matrix
object_storage[["step"]] = w
