import curses

import battle
import part
import robot


def main():
    sparts = [
        part.Part("chassis", "used", "plastic"),
        part.Part("controller", "pi"),
        part.Part("mover", "castor", "plastic"),
        part.Part("mover", "castor", "plastic"),
        part.Part("mover", "castor", "plastic"),
        part.Part("mover", "castor", "plastic"),
        part.Part("mover", "propellor", "wood"),
        part.Part("weapon", "crossbow", "wood"),
        part.Part("generator", "battery"),
    ]

    tparts = [
        part.Part("chassis", "contracted", "wood"),
        part.Part("controller", "pi"),
        part.Part("mover", "treads", "steel"),
        part.Part("mover", "treads", "steel"),
        part.Part("weapon", "spinner", "plastic"),
        part.Part("generator", "engine"),
    ]

    parts2 = [
        part.Part("chassis", "custom", "aluminum"),
        part.Part("controller", "pi"),
        part.Part("mover", "legs", "steel"),
        part.Part("mover", "treads", "steel"),
        part.Part("weapon", "spinner", "plastic"),
        part.Part("generator", "engine"),
    ]

    stupidbot = robot.Robot("Stupidbot 5000", sparts)
    tankbot = robot.Robot("Beef Supreme", tparts)
    r2 = robot.Robot("r2", parts2)

    b = battle.Battle(stupidbot, tankbot, r2)
    curses.wrapper(b.run)


if __name__ == "__main__":
    main()
