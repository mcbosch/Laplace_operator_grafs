import random
import classes
import funcions

# este programa calcula y guarda en un archivo 1000 vectores y sus respectivas imágenes

nom_graf = 'G1'
vector_positiu = 'true' # esta variable decide si queremos los valores del vector de entrada positivos o no
n = 1000    # nombre de vectors que es crearan


graf = classes.Graf.llegir_fitxer(nom_graf+'.txt')
graf.visualitzar_graf(nom_graf)
vectors = []    # lista de los vectors creados:
if vector_positiu:
    desti = "fitxers/operadors/in/entrada_positiva/" + nom_graf + '.txt'
    for i in range(n):
        v = []
        for j in range(len(graf)):
            n = random.randint(0, 20)
            v.append(n)
        vectors.append(v)

else:
    desti = "fitxers/operadors/in/entrada_qualsevol/" + nom_graf + '.txt'
    for i in range(n):
        v = []
        for j in range(len(graf)):
            n = random.randint(-20, 20)
            v.append(n)
        vectors.append(v)

fitxer = open(desti, 'w')
fitxer.write(nom_graf)
fitxer.write('\n')

for v in vectors:
    i_v = funcions.laplace_operator(graf, v)
    linia_e = 'e: (' + str(v[0])
    linia_s = 's: (' + str(i_v[0])
    for i in range(1, len(v)):
        linia_e = linia_e + ', ' + str(v[i])
        linia_s = linia_s + ', ' + str(i_v[i])

    linia = linia_e + ')' + chr(9) + '-> ' + linia_s + ')\n'
    fitxer.write(linia)
fitxer.close()
