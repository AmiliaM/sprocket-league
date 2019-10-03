import util
import random

class Robot:
    def __init__(self, name, parts=[]):
        self.name = name
        self.parts = parts

    def add_parts(self, *ps):
        self.parts.extend(ps)

    def is_valid(self):
        if  (len(self._parts_of_type('chassis')) == 1 and
            len(self._parts_of_type('controller')) == 1 and
            len(self._parts_of_type('power')) > 0):
           return True
        return False

    def is_alive(self):
        return self.is_valid() and self._parts_of_type('chassis')[0].health > 0

    def has_power(self):
        return any(map(lambda p: not p.is_destroyed(), self._parts_of_type('power')))

    def has_brain(self):
        return (self.is_valid() and
                not self._parts_of_type('controller')[0].is_destroyed() and
                self.has_power())

    def health(self):
        return sum(map(lambda p: p.health, self.parts))

    def size(self):
        return sum(map(lambda p: p.size, self.parts))

    def weighted_parts(self):
        return [x.size/self.size() for x in self.parts]

    def pick_alive_part(self, typ):
        if typ != 'any':
            return util.choice([p for p in self._parts_of_type(typ) if not p.is_destroyed()])
        return random.choices(self.alive_parts(), weights = list(map(lambda x: x.size, self.alive_parts())))[0]

    def alive_parts(self):
        return [p for p in self.parts if not p.is_destroyed()]

    def status(self):
        s = f"Robot {self.name}:\n"
        for p in self.parts:
            s += p.status()
        return s

    def _parts_of_type(self, typ):
        return [p for p in self.parts if p.typ == typ]
        #return filter(lambda p: p.typ == typ, self.parts)

    def __str__(self):
        return f"Robot {self.name} with {self.health()} hp and size {self.size()}"