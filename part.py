import json
import os


class Part:
    def __init__(self, typ, path, material=None):
        with open(f"data/part/{typ}/{path}.json") as f:
            obj = json.load(f)

        self.name = obj["name"]
        self.typ = typ
        self.size = obj["size"]

        self.weight = obj["weight"]
        self.health = obj["health"]
        self.cost = obj["cost"]

        if typ in ("controller", "motor", "generator"):
            self.power = obj["power"]
            return

        if typ == "weapon":
            self.damage = obj["damage"]
            self.range = obj["range"]
            self.damage_type = obj["damage_type"]
            self.rate = obj["rate"]
            if not obj["materialable"]:
                return

        assert material != None
        with open(f"data/material/{material}.json") as f:
            mat = json.load(f)

        if typ == "weapon":
            self.damage *= mat["damage_mult"]

        if typ == "mover":
            assert mat["mover"]
            self.speed = obj["speed"]
            self.accel = obj["accel"]
            self.turning = obj["turning"]

        self.health *= mat["health"]
        self.weight *= mat["weight_mult"]
        self.cost *= mat["cost_mult"]

    def take_damage(self, damage):
        self.health -= damage

    def is_destroyed(self):
        return self.health < 1

    def status(self):
        if self.health > 0:
            return f"{self.typ.capitalize()} {self.name}: {int(self.health)} hp\n"
        return f"{self.typ.capitalize()} {self.name} is broken\n"

    def verb(self):
        # fmt: off
        if self.typ == "chassis": return "holds"
        if self.typ == "controller": return "controls"
        if self.typ == "motor": return "drives"
        if self.typ == "mover": return "moves"
        if self.typ == "generator": return "powers"
        if self.typ == "armor": return "protects"
        if self.typ == "weapon":
            if self.damage_type == "cleaving": return "tears"
            if self.damage_type == "crushing": return "batters"
            if self.damage_type == "piercing": return "stabs"
            if self.damage_type == "slicing": return "slices"
            if self.damage_type == "fire": return "burns"
        return "touches"
        # fmt: on

    def __str__(self):
        return f"{self.typ}: {self.name} with {self.health} hp"

    def __repr__(self):
        return str(self)


def find_part_files(path):
    parts = []
    for root, _, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1] == ".json":
                parts.append(os.path.join(root, f))
    return parts
