import datetime
from Classes import Timestep, Railway, Train
from GlobalFunctions import mid_point
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
myFmt = mdates.DateFormatter('%H:%M')
plt.gca().xaxis.set_major_formatter(myFmt)

L = int(input())
n = int(input())
p = int(input())*2
k = input()
try:
    u = [int(i) for i in k.split(',')]
except ValueError:
    u = [int(i) for i in k.split()]
t = Timestep((lambda x: datetime.time(x[0], x[1]))([int(i) for i in input().split('.')]),
             (lambda x: datetime.time(x[0], x[1]))([int(i) for i in input().split('.')]))

trains = []
for i, j in enumerate(u):
    if i % 2 == 0:
        trains.append(Train(j, True, n - 1, i + 1))
    else:
        trains.append(Train(j, False, n - 1, i + 1))

mid = mid_point(trains, n) + 100

Ttrains = []
Ftrains = []
for i in trains:
    if i.direction:
        Ttrains.append(i)
    else:
        Ftrains.append(i)

c = 101
for i, j in enumerate(sorted(Ttrains, reverse=True)):
    for l, k in j.timetable.items():
        if c == 101:
            k.set_in_mins(True, t.start_in_mins + i * 10)
            k.set_in_mins(False, t.start_in_mins + i * 10 + round((L / j.TopSpeed) * 60))
            c += 1
            continue
        if c == mid:
            break
        k.set_in_mins(True, j.timetable[(l[0] - 1, l[1] - 1)].end_in_mins)
        k.set_in_mins(False, j.timetable[(l[0] - 1, l[1] - 1)].end_in_mins + round((L / j.TopSpeed) * 60))
        c += 1
    c = 101

c = 100 + n
for i, j in enumerate(sorted(Ftrains, reverse=True)):
    for l, k in j.timetable.items():
        if c == 100 + n:
            k.set_in_mins(True, t.start_in_mins + i * 10)
            k.set_in_mins(False, t.start_in_mins + i * 10 + round((L / j.TopSpeed) * 60))
            c -= 1
            continue
        if c == mid:
            break
        k.set_in_mins(True, j.timetable[(l[0] + 1, l[1] + 1)].end_in_mins)
        k.set_in_mins(False, j.timetable[(l[0] + 1, l[1] + 1)].end_in_mins + round((L / j.TopSpeed) * 60))
        c -= 1
    c = 100 + n

mid1 = sorted(Ttrains, key=lambda train: train.timetable[(mid-1, mid)].end, reverse=True)[0].timetable[(mid-1, mid)].end_in_mins
mid_time = max(sorted(Ftrains, key=lambda train: train.timetable[(mid+1, mid)].end, reverse=True)[0].timetable[(mid+1, mid)].end_in_mins, mid1)


c = 101
for i, j in enumerate(sorted(Ttrains, reverse=True)):
    for l, k in j.timetable.items():
        if c < mid:
            c += 1
            continue
        if c == mid:
            k.set_in_mins(True, mid_time + i*10)
            k.set_in_mins(False, mid_time + i*10 +round((L / j.TopSpeed) * 60))
            c += 1
            continue
        k.set_in_mins(True, j.timetable[(l[0] - 1, l[1] - 1)].end_in_mins)
        k.set_in_mins(False, j.timetable[(l[0] - 1, l[1] - 1)].end_in_mins + round((L / j.TopSpeed) * 60))
        c += 1
    c = 101

c = 100 + n
for i, j in enumerate(sorted(Ftrains, reverse=True)):
    for l, k in j.timetable.items():
        if c > mid:
            c -= 1
            continue
        if c == mid:
            k.set_in_mins(True, mid_time + i*10)
            k.set_in_mins(False, mid_time + i*10 +round((L / j.TopSpeed) * 60))
            c -= 1
            continue
        k.set_in_mins(True, j.timetable[(l[0] + 1, l[1] + 1)].end_in_mins)
        k.set_in_mins(False, j.timetable[(l[0] + 1, l[1] + 1)].end_in_mins + round((L / j.TopSpeed) * 60))
        c -= 1
    c = 100 + n

trains = Ttrains + Ftrains
trains = sorted(trains, key=lambda train: train.number)

date = datetime.date(year=1, month=1, day=1)
x = []
y = []
labels = []
for i, TheTrain in enumerate(trains):
    for i, k in TheTrain.timetable.items():
        x.append(i[0])
        x.append(i[1])
        y.append(datetime.datetime.combine(date, k.start))
        y.append(datetime.datetime.combine(date, k.end))

    labels.append(TheTrain.number)
    plt.plot(y, x, label='$y = {i}x + {i}$'.format(i=i))
    plt.legend(loc='best', labels=labels)
    x = []
    y = []
plt.show()
