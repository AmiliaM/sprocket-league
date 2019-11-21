import curses
import display
import grid
import random

class Battle:
    def __init__(self, *robots):
        self.combatants = set(robots)
        if len(self.combatants) != len(set(map(lambda x: x.name, self.combatants))):
            raise ValueError("Expected unique field 'name' on parameters")

    def status(self):
        s = f"There are {len(self.combatants)} combatants:\n"
        for r in self.combatants:
            s += r.status()
            s += '\n'
        return s

    def in_progress(self):
        return sum(map(int, map(lambda x: x.is_alive(), self.combatants))) > 1

    def run(self, stdscr):
        # Init grid
        g_size = (10, 10)
        g = grid.Grid(g_size)

        for r in self.combatants:
            g.add_rand(r.name)

        # Init displays
        display.init()
        log = curses.newwin(curses.LINES, curses.COLS//4, 0, (curses.COLS-1)-curses.COLS//4)
        statuses = curses.newwin(curses.LINES, curses.COLS//3, 0, 0)
        arena = curses.newwin(g.size[1]*2, g.size[0]*4, curses.LINES-(g.size[1]+5), (curses.COLS//2)-(g.size[0]*2))

        arena.addstr(g.draw())
        arena.refresh()

        statuses.clear()
        statuses.addstr(0, 0, self.status())
        statuses.refresh()

        # Check quit status before starting
        inp = log.getkey()
        if inp == 'q':
            return

        # Game loop
        while self.in_progress():
            log.addstr('\n')

            # Processs turns
            for c in self.combatants:
                if not c.is_alive():
                    continue

                if not c.brain():
                    log.addstr(f"Robot {c.name} can't take a turn!\n", curses.color_pair(1))
                    continue

                # Process movement
                if not c.locomotions():
                    log.addstr(f"Robot {c.name} is unable to move!\n", curses.color_pair(1))
                else:
                    g.move(c.name, random.randint(-1, 1), random.randint(-1, 1))

                # Choose weapon
                weapon = c.pick_alive_part('weapon')
                if weapon is None:
                    log.addstr(f"Robot {c.name} has no weapons!\n", curses.color_pair(1))
                    continue

                # Choose a target robot and part
                candidates = self.combatants.copy()
                candidates.remove(c)
                target = random.choice(list(candidates))

                target_part = target.pick_alive_part('any')

                # Calculate damage
                damage = random.randint(0, 5)

                # Calculate hit chance
                hit_chance = 100
                if target_part.size < 5:
                    hit_chance = 80
                hit = random.randint(0, 100)

                # Report and process hit
                if hit > hit_chance:
                    log.addstr(f"Robot {c.name} tries to attack {target.name}'s {target_part.name} with {weapon.name} but misses!\n")
                else:
                    target_part.take_damage(damage)
                    log.addstr(f"Robot {c.name} battered {target.name}'s {target_part.name} with {weapon.name}\n")
                    if target_part.is_destroyed():
                        log.addstr(f"{target.name}'s {target_part.name} was destroyed!\n", curses.color_pair(1))
                    living, reason = target.alive_reason()
                    if not living:
                        log.addstr(f"{target.name} died because {reason}!\n", curses.color_pair(1))

            # Process displays
            log.refresh()

            statuses.clear()
            statuses.addstr(0, 0, self.status())
            statuses.refresh()

            arena.clear()
            arena.addstr(g.draw())
            arena.refresh()

            # Process keys
            inp = log.getkey()
            if inp == 'q':
                break

        statuses.addstr(f"\n\n{[r for r in self.combatants if r.is_alive()][0].name} wins!\n\n", curses.color_pair(2))
        statuses.addstr("Press q to exit")
        statuses.refresh()
        while True:
            inp = log.getkey()
            if inp == 'q':
                break
