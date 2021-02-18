import datetime
class Timestep(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
        if self.start > self.end:
            self.start, self.end = self.end, self.start
        self.end_in_mins = self.end.hour*60 + self.end.minute
        self.start_in_mins = self.start.hour * 60 + self.start.minute
        self.duration_in_mins = self.end_in_mins - self.start_in_mins
        self.duration = datetime.time(self.duration_in_mins//60, self.duration_in_mins%60)

    def __hash__(self):
        return self.start_in_mins*self.end_in_mins

    def __eq__(self, other):
        if isinstance(other, Timestep):
            return (self.start == other.start and
                    self.end == other.end)
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Timestep):
            if self.end <= other.start:
                return False
            elif self.start < other.start:
                return False
            elif self.start == other.start and self.duration > other.duration:
                return False
            else:
                return True
        else:
            return NotImplemented

    def __str__(self):
        return f'{self.start}-{self.end}'

    def is_in_timestep(self, time):
        if isinstance(time, Timestep):
            if self.start < time.start and self.end > time.start or self.end > time.end and self.start < time.end or\
               self.start < time.start and self.end > time.end:
                return True
            return False
        if self.start < time < self.end:
            return True
        return False

    def set_in_mins(self, start, time):
        if start:
            self.start_in_mins = time
            self.start = datetime.time(self.start_in_mins//60, self.start_in_mins%60)
        else:
            self.end_in_mins = time
            self.end = datetime.time(self.end_in_mins//60, self.end_in_mins%60)

class Railway(object):
    def __init__(self, stations, distance=None):
        self.stations = stations
        self.timetable = {}
        self.distance = distance

    def add(self, timestamp, train):
        self.timetable[timestamp] = train

    def check(self, timestep):
        for i in self.timetable.keys():
            if i.is_in_timestep(timestep):
                return True
        return False

    def check_wt(self, timestep):
        for i in self.timetable.keys():
            if i.is_in_timestep(timestep):
                return [True, self.timetable[i]]
        return [False, None]

class Train(object):
    def __init__(self, speed, direction, StationsCount, number):
        self.TopSpeed = speed
        self.direction = direction
        self.number = number
        self.timetable = {}
        self.get_default_timetable(StationsCount)

    def __eq__(self, other):
        if isinstance(other, Train):
            return self.number == other.number
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Train):
            return self.TopSpeed < other.TopSpeed
        else:
            return NotImplemented

    def __str__(self):
        responce = '\n'
        for i, j in self.timetable.items():
            responce += f'{i}: {j}\n'
        return f'Train number {self.number}\n' \
               f'Train top speed: {self.TopSpeed}\n' \
               f'Train direction {f"101-{101+len(self.timetable)}" if self.direction else f"{101+len(self.timetable)}-101"}' \
               f'\nTrain timetable: {responce}'

    def get_default_timetable(self, count):
        if self.direction:
            for i in range(101, count+101):
                self.timetable[(i, i+1)] = Timestep(datetime.time(00, 00), datetime.time(00, 00))
        else:
            for i in range(count+101, 101, -1):
                self.timetable[(i, i-1)] = Timestep(datetime.time(00, 00), datetime.time(00, 00))