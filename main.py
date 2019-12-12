from copy import deepcopy

import curses

import battle
import part
import robot


def main():
    sparts = [
        part.Part.new_chassis(
            "data/parts/material/wood.json", "data/parts/chassis/used.json"
        ),
        part.Part.new_controller("data/parts/controller/pi.json"),
        part.Part.new_mover(
            "data/parts/material/plastic.json", "data/parts/mover/castor.json"
        ),
        part.Part.new_mover(
            "data/parts/material/plastic.json", "data/parts/mover/castor.json"
        ),
        part.Part.new_mover(
            "data/parts/material/plastic.json", "data/parts/mover/castor.json"
        ),
        part.Part.new_mover(
            "data/parts/material/plastic.json", "data/parts/mover/castor.json"
        ),
        part.Part.new_mover(
            "data/parts/material/wood.json", "data/parts/mover/propellor.json"
        ),
        part.Part.new_weapon(
            "data/parts/material/wood.json", "data/parts/weapon/crossbow.json"
        ),
        part.Part.new_generator("data/parts/power/generator/battery.json"),
    ]

    tparts = [
        part.Part.new_chassis(
            "data/parts/material/plastic.json", "data/parts/chassis/contracted.json"
        ),
        part.Part.new_controller("data/parts/controller/pi.json"),
        part.Part.new_mover(
            "data/parts/material/steel.json", "data/parts/mover/treads.json"
        ),
        part.Part.new_mover(
            "data/parts/material/steel.json", "data/parts/mover/treads.json"
        ),
        part.Part.new_weapon(
            "data/parts/material/plastic.json", "data/parts/weapon/spinner.json"
        ),
        part.Part.new_generator("data/parts/power/generator/engine.json"),
    ]

    stupidbot = robot.Robot("Stupidbot 5000", sparts)
    tankbot = robot.Robot("Beef Supreme", tparts)

    b = battle.Battle(stupidbot, tankbot)
    curses.wrapper(b.run)


if __name__ == "__main__":
    main()
