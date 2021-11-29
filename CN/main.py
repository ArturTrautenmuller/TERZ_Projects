import math
#Método da Secante
def secante(p0,p1,tol,n):
    i = 2
    q0 = f(p0)
    q1 = f(p1)
    while(i <= n):
        p = p1 - q1*(p1 - p0)*(q1 - q0)
        if(abs(p - p1) < tol):
            return p
        i = i + 1
        p0 = p1
        q0 = q1
        p1 = p
        q1 = f(p)
    return 'failed'


#18
def f(x):
    return math.pow(math.e, -(math.pow(x, 2))) - math.cos(x)
x0 = 1
x1 = 2
tol = 0.00018553
n = 5
"""
#19
def f(x):
    return math.pow(x, 3) - x - 1

x0 = 0
x1 = 0.5
tol = 0.000008998843
n = 27

#20
def f(x):
    return 4*math.sin(x) - math.pow(math.e, x)

x0 = 0
x1 = 1
tol = 0.0000057404
n = 7

#21
def f(x):
    return x*math.log10(x) - 1

x0 = 2.3
x1 = 2.7
tol = 0.000080561
n = 3
"""


res = secante(x0,x1,tol,n)
print(res)
print(f(res))

"""
18: x = 1.7238661021129316 f(x) = 0.20368816310329158
19: x = 0.19343559053651704 f(x) = -1.1861977476592365
20: failed
21: x = 2.678023082615829 f(x) = 0.14569661330928363
"""