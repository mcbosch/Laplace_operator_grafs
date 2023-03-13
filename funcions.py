def laplace_operator(graf, vector):
    vector_solucio = []
    a = graf.matriu()
    for i in range(len(graf)):
        d_in = 0
        w = 0
        for j in range(len(graf)):  # calculam el grau d'entrada i el valor del sumatori del operador
            m = a.get_valor(j, i)
            d_in = d_in + m
            w = w + vector[j]*m

        if d_in == 0:
            vector_solucio.append(0)
        else:
            s = float(vector[i])-float(w/d_in)
            vector_solucio.append(s)
    return vector_solucio


def laplace_operator_out(graf, vector):
    vector_solucio = []
    a = graf.matriu()
    for i in range(len(graf)):
        d_out = 0
        w = 0
        for j in range(len(graf)):  # calculam el grau d'entrada i el valor del sumatori del operador
            m = a.get_valor(i, j)
            d_out = d_out + m
            w = w + vector[j] * m

        if d_out == 0:
            vector_solucio.append(0)
        else:
            s = float(vector[i]) - float(w/d_out)
            vector_solucio.append(s)
    return vector_solucio
