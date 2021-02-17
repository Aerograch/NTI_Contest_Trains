import datetime
from Classes import Timestep, Railway, Train
from GlobalFunctions import mid_point
        
class Station(object):
    def __init__(self, number):
        self.arrivals = {}
        self.departures = {}
        self.number = number

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
        trains.append(Train(j, True, n-1, i+1))
    else:
        trains.append(Train(j, False, n-1, i+1))

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

print(*trains, '', sep='\n')

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

stations = {}
for i in range(1, n+1):
    stations[i+100] = Station(i+100)

for i in trains:
    for j, k in i.timetable.items():

        stations[j[0]].departures[i.number] = k.start
        stations[j[1]].arrivals[i.number] = k.end

for i in stations.values():
    for j in range(1, p+1):
        try:
            i.arrivals[j]
        except KeyError:
            i.arrivals[j] = i.departures[j]
        try:
            i.departures[j]
        except KeyError:
            i.departures[j] = i.arrivals[j]

ar = {}
dep = {}

for i in stations.values():
    for j in range(1, p+1):
        ar[j] = i.arrivals[j]
        dep[j] = i.departures[j]
    i.arrivals = ar
    i.departures = dep
    ar = {}
    dep = {}

print('поезда        ', end='')
for i in range(1, p+1):
    print(f'{i}                ', end='')

print(f'\nстанции  ', end='')
for i in range(1, p+1):
    print(f'приб.|отпр.      ', end='')

for i, j in stations.items():
    print(f'\n{i}      ', end='')
    for k in range(1, p+1):
        print(f'{j.arrivals[k].hour}.{"0" + str(j.arrivals[k].minute) if j.arrivals[k].minute<10 else j.arrivals[k].minute}/'
              if j.arrivals[k].hour>=10 else f'{j.arrivals[k].hour}.'
              f'{"0" + str(j.arrivals[k].minute) if j.arrivals[k].minute<10 else j.arrivals[k].minute} /', end='')
        print(f'{j.departures[k].hour}.{"0" + str(j.departures[k].minute) if j.departures[k].minute<10 else j.departures[k].minute}'
              if j.departures[k].hour>=10 else f'{j.departures[k].hour}.'
              f'{"0" + str(j.departures[k].minute) if j.departures[k].minute<10 else j.departures[k].minute} ', end='')
        print(f'      ', end='')

