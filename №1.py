import datetime
from Classes import Railway, Timestep
from GlobalFunctions import check_linear

L = int(input())
n = int(input())
p = int(input())*2
u = [int(c) for c in input().split()]
a, b = [], []
for i in range(p):
    a.append([k for k in input().split()])

for j in range(p):
    b.append([k for k in input().split()])

c = []
c1 = []
c2 = []
dic = {}
for i, k in enumerate(a, 1):
    c = []
    k.pop(0) if i % 2 == 1 else k.pop(len(b[i-1])-1)
    c1 = k
    b[i-1].pop(len(b[i-1])-1) if i % 2 == 1 else b[i-1].pop(0)
    c2 = b[i-1]
    if i % 2 == 1:
        for j, l in enumerate(c1):
            c.append(Timestep((lambda x: datetime.time(int(x[0]), int(x[1])))(c2[j].split('.')),
                         (lambda x: datetime.time(int(x[0]), int(x[1])))(l.split('.'))))
    else:
        c1 = c1[::-1]
        c2 = c2[::-1]
        for j, l in enumerate(c1):
            c.append(Timestep((lambda x: datetime.time(int(x[0]), int(x[1])))(c2[j].split('.')),
                             (lambda x: datetime.time(int(x[0]), int(x[1])))(l.split('.'))))
    dic[i] = c if i % 2 == 1 else c[::-1]

del c
del c1
del c2

m = check_linear(dic, u, L/(n))
if m != True:
    print(m)
    raise SystemExit

del m
del L
del u

railways = {}
for i in range(n-1):
    railways[i+1] = Railway([100+i+1, 100+i+2])
for i, j in dic.items():
    for k, l in enumerate(j, 1):
        if not railways[k].check_wt(l)[0]:
            railways[k].add(l, i)
        else:
            print(f'Расписание нереализуемо. Поезд {i} столкнулся с поездом {railways[k].check_wt(l)[1]} '
                  f'между станциями {railways[k].stations[0]} и {railways[k].stations[1]}.')
            raise SystemExit
print('Расписание реализуемо.')
