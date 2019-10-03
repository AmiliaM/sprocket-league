import json
import os

class Part:
    def __init__(self, name, health, typ, size):
        self.name = name
        self.health = health
        self.typ = typ
        self.size = size

    @classmethod
    def from_file(cls, file):
        with open(file) as f:
            r = json.load(f)
        return Part(r['name'], r['health'], r['type'], r['size'])

    def take_damage(self, damage):
        self.health -= damage

    def is_destroyed(self):
        return self.health < 1

    def health_status(self):
        if self.health > 0:
            return f": {self.health} hp"
        else:
            return "is broken"

    def status(self):
        return f"{self.typ} {self.name} {self.health_status()}\n"

    def __str__(self):
        return f"{self.typ}: {self.name} with {self.health} hp"

    def __repr__(self):
        return str(self)

def find_part_files(path):
    parts = []
    for root, _, files in os.walk(path):
        for f in files:
            if os.path.splitext(f)[1] == '.json':
                parts.append(os.path.join(root, f))
    return parts