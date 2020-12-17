def chaine_a_liste(liste_argument):
    sub_liste_1 = []
    for i in liste_argument:
        if i.isnumeric():
            sub_liste_1 .append(int(i))
    sub_liste_2 = []
    for i in range(len(sub_liste_1)):
        if i % 2 == 0:
            sub_liste_2.append((sub_liste_1[i], sub_liste_1[i + 1]))
    return sub_liste_2

if __name__ == '__main__':
    chaine_a_liste(list("[(1, 4), (1, 5), (2, 3), (3, 2), (5, 1)]"))
    print(list("[(1, 4), (1, 5), (2, 3), (3, 2), (5, 1)]"))
    chaine_a_liste(list("[(2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]"))
    print(list("[(2, 4), (2, 5), (3, 3), (3, 4), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]"))
    chaine_a_liste(list("[(1, 4), (1, 5), (2, 3), (3, 2), (5, 1)]"))
    print(list("[(1, 4), (1, 5), (2, 3), (3, 2), (5, 1)]"))