import random

def choice(seq):
    if len(seq) == 0:
        return None
    else:
        return random.choice(seq)
