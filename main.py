from copy import deepcopy

import curses

import battle
import part
import robot


def main():
    parts = list(map(part.Part.from_file, part.find_part_files("data/")))

    r = robot.Robot("Blep", parts)
    r2 = robot.Robot("Mlem", deepcopy(parts))

    b = battle.Battle(r, r2)
    curses.wrapper(b.run)


if __name__ == "__main__":
    main()
