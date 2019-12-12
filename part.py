import json
import os


class Part:
    def __init__(self, name, typ):
        self.name = name
        self.typ = typ

    @classmethod
    def new_chassis(cls, material, manufacturer):
        with open(material) as f:
            mat = json.load(f)
        with open(manufacturer) as f:
            man = json.load(f)
        with open("data/parts/base_chassis.json") as f:
            chassis = json.load(f)

        part = Part(chassis["name"], "chassis")

        part.health = man["health_mult"] * mat["health"]
        part.size = man["size"]
        part.cost = chassis["cost"] * man["cost_mult"] * mat["cost_mult"]
        part.weight = chassis["weight"] * mat["weight_mult"]
        return part

    @classmethod
    def new_controller(cls, file):
        with open(file) as f:
            con = json.load(f)

        part = Part(con["name"], "controller")
        part.health = con["health"]
        part.size = con["size"]
        part.cost = con["cost"]
        part.weight = con["weight"]
        return part

    @classmethod
    def new_motor(cls, file):
        with open(file) as f:
            motor = json.load(f)

        part = Part(motor["name"], "motor")
        part.health = motor["health"]
        part.size = motor["size"]
        part.cost = motor["cost"]
        part.weight = motor["weight"]
        return part

    @classmethod
    def new_mover(cls, material, mover):
        with open(material) as f:
            mat = json.load(f)
        with open(mover) as f:
            mov = json.load(f)

        part = Part(mov["name"], "mover")

        part.health = mat["health"] * mov["health_mult"]
        part.size = mov["size"]
        part.cost = mov["cost"] * mat["cost_mult"]
        part.weight = mov["weight"] * mat["weight_mult"]
        return part

    @classmethod
    def new_weapon(cls, material, weapon):
        with open(material) as f:
            mat = json.load(f)
        with open(weapon) as f:
            weap = json.load(f)

        part = Part(weap["name"], "weapon")
        part.size = weap["size"]
        part.range = weap["range"]
        part.damage_type = weap["damage_type"]
        part.rate = weap["rate"]
        part.cooldown = part.rate

        if weap["materialable"]:
            part.health = mat["health"] * weap["health"]
            part.cost = weap["cost"] * mat["cost_mult"]
            part.weight = weap["weight"] * mat["weight_mult"]
            part.damage = weap["damage"] * mat["damage_mult"]
        else:
            part.health = weap["health"]
            part.cost = weap["cost"]
            part.weight = weap["weight"]
            part.damage = weap["damage"]
        return part

    @classmethod
    def new_armor(cls, material):
        with open(material) as f:
            mat = json.load(f)
        with open("data/parts/armor.json") as f:
            armor = json.load(f)

        part = Part(armor["name"], "armor")
        part.health = mat["health"] * armor["health_mult"]
        part.cost = mat["cost_mult"] * armor["cost"]
        part.weight = mat["weight_mult"] * armor["weight"]
        part.size = armor["size"]
        return part

    @classmethod
    def new_generator(cls, file):
        with open(file) as f:
            gen = json.load(f)

        part = Part(gen["name"], "generator")
        part.health = gen["health"]
        part.cost = gen["cost"]
        part.weight = gen["weight"]
        part.size = gen["size"]
        part.power = gen["power"]
        return part

    def take_damage(self, damage):
        self.health -= damage

    def is_destroyed(self):
        return self.health < 1

    def status(self):
        if self.health > 0:
            return f"{self.typ.capitalize()} {self.name}: {self.health} hp\n"
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
