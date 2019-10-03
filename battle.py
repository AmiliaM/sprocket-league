from sys import stdin
import random

class Battle:
    def __init__(self, *robots):
        self.combatants = set(robots)

    def show_status(self):
        print(f"There are {len(self.combatants)} combatants:")
        for r in self.combatants:
            print(r)

    def in_progress(self):
        return sum(map(int, map(lambda x: x.is_alive(), self.combatants))) > 1

    def run(self):
        while self.in_progress():
            #self.show_status()
            stdin.readline()
            for c in self.combatants:
                if not c.has_brain():
                    print(f"Robot {c.name} is unable to move!")
                    continue
                candidates = self.combatants.copy()
                candidates.remove(c)
                target = random.choice(list(candidates))
                weapon = c.pick_alive_part('weapon')
                if weapon is None:
                    print(f"Robot {c.name} has no weapons!")
                    continue
                target_candidate_parts = target.alive_parts()
                target_part = random.choices(target_candidate_parts, weights = list(map(lambda x: x.size, target_candidate_parts)))[0]
                damage = random.randint(0, 5)
                hit_chance = 100
                if target_part.size < 5:
                    hit_chance = 80
                hit = random.randint(0, 100)
                if hit > hit_chance:
                    print(f"Robot {c.name} tries to attack {target.name}'s {target_part.name} with {weapon.name} but misses!")
                else:
                    target_part.take_damage(damage)
                    print(f"Robot {c.name} battered {target.name}'s {target_part.name} with {weapon.name}")
                    if target_part.is_destroyed():
                        print(f"{target.name}'s {target_part.name} was destroyed!")
                    print(f"{target.name} chassis is", target._parts_of_type("chassis"), "and health is", target._parts_of_type("chassis")[0].health)
                    if not target.is_alive():
                        print(f"{target.name} was destroyed!")