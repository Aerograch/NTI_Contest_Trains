def check(rw, speed, C, a):
    t = 0
    s = 0
    v = 0
    for i, j in enumerate(rw.values()):
        for k in j.timetable.keys():
            v = round(speed/3.6, 1)
            t = round(v/a, 1)
            s = (a*(t**2))/2
            s = s*2
            s = round(s/1000, 1)
            if k.duration_in_mins < round(t/60, 1)*2 + round((((C[i]-s)*1000)/v)/60, 1):
                return [True, j.timetable[k], j.stations[1]]
    return [False]

def check_all(rw, speed, C, a):
    t = 0
    s = 0
    v = 0
    f = False
    responce = []
    for i, j in enumerate(rw.values()):
        for k in j.timetable.keys():
            v = round(speed/3.6, 1)
            t = round(v/a, 1)
            s = (a*(t**2))/2
            s = s*2
            s = round(s/1000, 1)
            if k.duration_in_mins < round(t/60, 1)*2 + round((((C[i]-s)*1000)/v)/60, 1):
                f = True
                responce.append([j.timetable[k], j.stations[1]])
    if f:
        return [True, responce]
    return [False]

def check_linear(routes, speed, dist):
    a = 0
    for i, j in routes.items():
        for m, k in enumerate(j, 1):
            if k.duration_in_mins < dist//speed[i-1]*60:
                return f'Поезд {i} не успевает в расписание'
    return True

def mid_point(trains, stations):
    if stations % 2 == 1:
        return stations//2+1
    else:
        if sorted(trains)[0].direction:
            return stations//2
        return stations//2+1

