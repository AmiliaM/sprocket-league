import random


def choice(seq):
    if not seq:
        return None
    return random.choice(seq)
