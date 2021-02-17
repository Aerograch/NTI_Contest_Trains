import datetime
from Classes import Train, Timestep
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

L = int(input())
n = int(input())
p = int(input())
t = int(input())
u = [int(i) for i in input().split()]
a, b = [], []

for i in range(p):
    a.append([k for k in input().split()])

for j in range(p):
    b.append([k for k in input().split()])

for i in a:
    i.pop(0)
for i in b:
    i.pop(2)

trains = []
for i, j in enumerate(u):
    if i % 2 == 0:
        trains.append(Train(j, True, n-1, i+1))
    else:
        trains.append(Train(j, False, n-1, i+1))


for i, j in enumerate(a):
    for k, l in trains[i].timetable.items():
        if i % 2 == 0:
            trains[i].timetable[k] = Timestep((lambda x: datetime.time(int(x[0]), int(x[1])))(a[i][k[0]-101].split('.')),
                                          (lambda x: datetime.time(int(x[0]), int(x[1])))(b[i][k[0]-101].split('.')))
        else:
            trains[i].timetable[k] = Timestep(
                (lambda x: datetime.time(int(x[0]), int(x[1])))(a[i][k[1] - 101].split('.')),
                (lambda x: datetime.time(int(x[0]), int(x[1])))(b[i][k[1] - 101].split('.')))

TheTrain = trains[t-1]

date = datetime.date(year=1, month=1, day=1)
x = []
y = []
for i, k in TheTrain.timetable.items():
    x.append(i[0])
    x.append(i[1])
    y.append(datetime.datetime.combine(date, k.start))
    y.append(datetime.datetime.combine(date, k.end))

x1, x2, y1, y2 = None, None, None, None
for i, k in TheTrain.timetable.items():
    x1 = i[0]
    y1 = datetime.datetime.combine(date, k.start)
    break

x2 = 100+n
y2 = datetime.datetime.combine(date, TheTrain.timetable[(100+n-1, 100+n)].end)

plt.axis([y1,y2,x2,x1])
plt.plot(y, x, '#000000')
plt.text(y[1], x[1], t)
plt.show()