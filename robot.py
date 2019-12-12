import random
import util


class Robot:
    # Construction methods

    def __init__(self, name, parts=[]):
        self.name = name
        self.parts = parts

    def add_parts(self, *ps):
        self.parts.extend(ps)

    # Check methods

    def is_valid(self):
        if (
            len(self._parts_of_type("chassis")) == 1
            and len(self._parts_of_type("controller")) == 1
            and self.power() > 0
        ):
            return True
        return False

    def is_alive(self):
        return self.is_valid() and self._parts_of_type("chassis")[0].health > 0

    def alive_reason(self):
        if not self.is_valid:
            return (False, "because it was invalid")
        if not self._parts_of_type("chassis")[0].health > 0:
            return (False, "because its chassis was destroyed")
        return (True, "")

    # Part methods

    def powers(self):
        if any(map(lambda p: not p.is_destroyed(), self._parts_of_type("power"))):
            return self._parts_of_type("power")
        return False

    def controller(self):
        if (
            self.is_valid()
            and not self._parts_of_type("controller")[0].is_destroyed()
            and self.power() > 0
        ):
            return self._parts_of_type("controller")[0]
        return False

    def movers(self):
        if self.power() > 0 and self.controller() and self._parts_of_type("mover"):
            return self._parts_of_type("mover")
        return False

    def weighted_parts(self):
        return [x.size / self.size() for x in self.parts]

    def alive_parts(self):
        return [p for p in self.parts if not p.is_destroyed()]

    def pick_alive_part(self, typ):
        if typ != "any":
            return util.choice(
                [p for p in self._parts_of_type(typ) if not p.is_destroyed()]
            )
        return random.choices(
            self.alive_parts(), weights=list(map(lambda x: x.size, self.alive_parts()))
        )[0]

    # Info methods

    def status(self):
        s = f"Robot {self.name}:\n"
        for p in self.parts:
            s += p.status()
        return s

    def health(self):
        return sum(map(lambda p: p.health, self.parts))

    def size(self):
        return sum(map(lambda p: p.size, self.parts))

    def power(self):
        return sum(
            [x.power for x in self._parts_of_type("generator") if not x.is_destroyed()]
        )

    # Helper methods

    def _parts_of_type(self, typ):
        return [p for p in self.parts if p.typ == typ]

    def __str__(self):
        return f"Robot {self.name} with {self.health()} hp and size {self.size()}"
