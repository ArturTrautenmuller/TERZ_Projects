import numpy as np

A = np.array([[-8.0,3,1],[2,-4,1],[2,3,5]])


def Sassenfeld(A):
    coeficientes = []

    for i in range(len(A)):
        b = 0
        for j in range(len(A)):
            if (i != j and i == 0) or i < j:
                b += A[i][j]
            elif i != j and i != 0:
                b += A[i][j] * coeficientes[j]
        b /= A[i][i]
        coeficientes.append(b)

    maxCoef = max(coeficientes)
    if maxCoef < 1:
        return 'Critério de Sassenfeld satisfeito'
    else:
        return 'Critério de Sassenfeld não satisfeito'

def GaussSeidel(A,b,vetorSolucao,iteracoes):
    iteracao = 0
    while iteracao < iteracoes:
        for i in range(len(A)):
            x = b[i]
            for j in range(len(A)):
                if i != j:
                    x -= A[i][j]*vetorSolucao[j]
            x /= A[i][i]
            vetorSolucao[i] = x
        iteracao += 1
    return vetorSolucao

def Jacobi(A,b,vetorSolucao,iteracoes):
    iteracao = 0
    aux = []
    for k in range(len(vetorSolucao)):
        aux.append(0)
    while iteracao < iteracoes:
        for i in range(len(A)):
            x = b[i]
            for j in range(len(A)):
                if i != j:
                    x -= A[i][j] * vetorSolucao[j]
            x /= A[i][i]
            vetorSolucao[i] = x
        iteracao += 1

        for l in range(len(aux)):
            vetorSolucao[l] = aux[l]
    return vetorSolucao


#Q5 a)
resA = Sassenfeld(A)
print('Q5-a: '+resA)

#05 b)

A1 = np.array([[1,0.5,-0.1,0.1],[0.2,1,-0.2,-0.1],[-0.1,-0.2,1,0.2],[0.1,0.3,0.2,1]])
SfA1 = Sassenfeld(A1)
GSA1 = GaussSeidel(A1,[1,1,1,1],[0,0,0,0],10)
print('Q5-b, Sassenfeld A: '+SfA1)
print('Q5-b, Gauss-Seidel A: '+str(GSA1))

B1 = np.array([[2,1,3],[0,-1,1],[1,0,3]])

SfB1 = Sassenfeld(B1)
GSB1 = GaussSeidel(B1,[1,1,1],[0,0,0],10)
print('Q5-b, Sassenfeld B: '+SfB1)
print('Q5-b, Gauss-Seidel B: '+str(GSB1))

C1 = np.array([[1,1],[1,-3]])

SfC1 = Sassenfeld(C1)
GSC1 = GaussSeidel(C1,[1,1],[0,0],10)
JC1 = Jacobi(C1,[1,-1],[0,0],40)
print('Q5-b, Sassenfeld C: '+SfC1)
print('Q5-b, Gauss-Seidel C: '+str(GSC1))
print('Q5-b,Jacobi C: '+str(JC1))


