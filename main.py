import robot
import part
import battle
from copy import deepcopy

def main():
    r = robot.Robot('Blep')
    parts = list(map(part.Part.from_file, part.find_part_files('data/')))
    r.add_parts(*parts)
    r2 = robot.Robot('mlem')
    r2.add_parts(*deepcopy(parts))
    b = battle.Battle(r, r2)
    b.run()


if __name__=="__main__":
    main()