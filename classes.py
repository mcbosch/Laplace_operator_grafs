import graphviz

class Conjunt:

    def __init__(self):

        self.__conj = []

    def afegir(self, x):

        if x not in self.__conj:
            self.__conj.append(x)

    def eliminar(self, x):

        if x in self.__conj:
            self.__conj.remove(x)

    def cardinal(self):
        return len(self.__conj)

    def unio(self, o):

        unio = Conjunt()
        for i in self.__conj:
            unio.afegir(i)
        for i in o.__conj:
            unio.afegir(i)
        return unio

    def __intecar(self, o):
        intersec = Conjunt()
        for i in self.__conj:
            if i in o.__conj:
                intersec.afegir(i)
        return intersec

    def interseccio(self, o):
        c = self.__intecar(o)
        return c

    def disjunts(self, o):
        c = self.__intecar(o)
        return c.cardinal() == 0

    def pertany(self, e):

        return e in self.__conj

    def __str__(self):
        string = ""
        for i in self.__conj:
            if i == self.__conj[0]:
                string = f"({i}"
            else:
                string = string + ", " + f"{i}"
        string = string + ")"
        return string

class Matriu:

    def __init__(self, n):
        self.__matriu = []
        self.__n = n

        for i in range(n):
            fila = [0] * n
            self.__matriu.append(fila)

    def modificar_valor(self, fila, columna, valor):

        if -1 < fila < self.__n and -1 < columna < self.__n:
            self.__matriu[fila][columna] = valor

    def get_valor(self, fila, columna):
        return self.__matriu[fila][columna]

    # Sobreescrivim la funció len de Python, aquest mètode retorna la mida de la matriu.
    def __len__(self):

        return self.__n

    def mostrar_per_pantalla(self):

        n = self.__n

        for i in range(n):
            for j in range(n):
                if self.__matriu[i][j] < 10:
                    print("0", end="")
                print(self.__matriu[i][j], end=" ")

            print("")

    def matriu_com_string(self):

        n = self.__n
        frase = ''

        for i in range(n):
            for j in range(n):
                if self.__matriu[i][j] < 10:
                    frase = frase + "0"
                frase = frase + f'{self.__matriu[i][j]}'+' '
            frase = frase + '\n'

        return frase

class Graf:

    __visitats = [] # aquesta variable es farà servir per profunditat

    def __init__(self, n):
        self.__M = Matriu(n)
        self.__ordre = n

    def __len__(self):
        return self.__ordre

    def matriu(self):
        M = Matriu(self.__ordre)
        for i in range(len(self)):
            for j in range(len(self)):
                M.modificar_valor(i, j, self.__M.get_valor(i, j))
        return M

    def afegir_aresta(self, inici, final, pes):
        self.__M.modificar_valor(inici, final, pes)

    def eliminar_a(self, inici, final):
        self.__M.modificar_valor(inici, final, 0)

    @staticmethod
    def llegir_matriu(m):
        n = len(m)
        graf = Graf(n)

        for i in range(0, n):
            for j in range(0, n):
                pes = m.get_valor(i, j)
                graf.afegir_aresta(i, j, pes)
        return graf

    @staticmethod
    def llegir_fitxer(nom_fitxer):
        path = "fitxers/grafs/" + nom_fitxer
        graf = open(path)
        n = int(graf.readline())
        g = Graf(n)

        for linia in graf:
            aresta = linia.split(" ")
            g.afegir_aresta(int(aresta[0]), int(aresta[1]), int(aresta[2]))
        graf.close()

        return g

    @staticmethod
    def guardar_graf(g, nom):
        arestes = []

        for i in range(len(g)):
            for j in range(len(g)):
                if g.__M.get_valor(i, j) != 0:
                    arestes.append([i, j, g.__M.get_valor(i, j)])

        desti = "fitxers/" + nom + ".txt"
        fitxer = open(desti, 'w')
        fitxer.write(str(len(g.__M)))
        fitxer.write('\n')

        for aresta in arestes:
            linia = str(aresta[0]) + ' ' + str(aresta[1]) + ' ' + str(aresta[2]) + '\n'
            fitxer.write(linia)
        fitxer.close()

    @staticmethod
    def mostrar_matriu(g):
        g.__M.mostrar_per_pantalla()

    def __profunditat2(self, v0):
        n = len(self)
        Graf.__visitats.append(v0)
        for j in range(n):
            k = self.__M.get_valor(v0, j)
            if k != 0:
                if j not in Graf.__visitats:
                    self.__profunditat2(j)

    def profunditat(self, v0):
        Graf.__visitats = []
        self.__profunditat2(v0)

        return Graf.__visitats

    def warshall(self):
        graf = Graf(self.__ordre)
        graf.__M = self.matriu()

        for i in range(self.__ordre):
            for j in range(self.__ordre):
                for z in range(self.__ordre):
                    if graf.__M.get_valor(i, j) != 0:
                        graf.__M.modificar_valor(i, j, 1)
                        if graf.__M.get_valor(j, z) != 0:
                            graf.__M.modificar_valor(i, z, 1)
        return graf

    # Aquesta funcio ordena les arestes de menor a major pes
    def __simplificacio_matr(self):
        simpl = []

        for i in range(len(self)):
            for j in range(len(self)):
                if self.__M.get_valor(i, j) != 0:
                    simpl.append([i, j, self.__M.get_valor(i, j)])
        #ordenam segons el pes
        actualitzat = True
        mida = len(simpl)

        while actualitzat:
            actualitzat = False
            for j in range(0, mida - 1):
                if simpl[j][2] > simpl[j + 1][2]:
                    simpl[j], simpl[j + 1] = simpl[j + 1], simpl[j]
                    actualitzat = True
        return simpl

    def conex2(self):
        g = Graf(self.__ordre)
        for i in range(self.__ordre):
            for j in range(self.__ordre):

                if self.__M.get_valor(i, j) != 0:
                    g.__M.modificar_valor(i, j, 1)
                    g.__M.modificar_valor(j, i, 1)
        v_conectats = g.profunditat(0)

        return len(v_conectats) == self.__ordre

    def prim(self):
        conex = self.conex2()
        if conex:
            arestes_graf = self.__simplificacio_matr()
            arestes_noves = []
            nodes = Conjunt()

            min_aresta = arestes_graf[0]
            nodes.afegir(min_aresta[0])
            nodes.afegir(min_aresta[1])
            arestes_noves.append(min_aresta)
            arestes_graf.remove(min_aresta)

            while nodes.cardinal() < len(self.__M):
                nova_aresta = False
                aresta = 0

                while not nova_aresta:
                    condicio1 = nodes.pertany(arestes_graf[aresta][0]) and not nodes.pertany(arestes_graf[aresta][1])
                    condicio2 = not nodes.pertany(arestes_graf[aresta][0]) and nodes.pertany(arestes_graf[aresta][1])

                    if condicio1 or condicio2:
                        nova_aresta = True
                        min_aresta = arestes_graf[aresta]
                        nodes.afegir(min_aresta[0])
                        nodes.afegir(min_aresta[1])
                        arestes_noves.append(min_aresta)
                        arestes_graf.remove(min_aresta)
                    else:
                        aresta += 1
            return arestes_noves
        else:
            print('aquest arbre no es connex, no podem fer un arbre de extensio minima')

    def graf_prim(self):
        arestes = self.prim()
        graf = Graf(self.__ordre)
        for aresta in arestes:
            graf.afegir_aresta(aresta[0], aresta[1], aresta[2])

        return graf

    def visualitzar_graf(self, nom):
        graf = graphviz.Digraph(nom)
        for i in range(self.__ordre):
            graf.node(f'{i}', f'{i}')
        for i in range(self.__ordre):
            for j in range(self.__ordre):

                if self.__M.get_valor(i, j) != 0:
                    graf.edge(f'{i}', f'{j}', f'{self.__M.get_valor(i, j)}')

        graf.render(f'fitxers/imatges/{nom}/{nom}', view=True, overwrite_source=True)

    def __str__(self):
        return f'{self.__ordre}'
