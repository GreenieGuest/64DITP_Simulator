import random
from time import sleep
from config import FASTFORWARD

import os
from pathlib import Path

file = Path(__file__)
parent = file.parent
os.chdir(parent)

def suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    
# Sorting Functions

def getShowdownPoints(player):
    """
    Get a stat.
    """
    return player.showdownPoints

def physScope(player):
    """
    Get a stat.
    """
    return random.randint(1, player.physStat)

def stratScope(player):
    """
    Get a stat.
    """
    return random.randint(1, player.stratStat)

def socScope(player):
    """
    Get a stat.
    """
    return random.randint(1, player.socStat)

def notorietyScope(player):
    """
    Get a stat.
    """
    return random.randint(0, player.notoriety)

def randomScope(player):
    """
    Get a stat.
    """
    return random.randint(1, 64)

def rollPass(stat):
    """
    The basic scheme for randomizing performance based on a stat.
    """
    playerRoll = random.randint(1, stat)
    threshold = random.randint(1, 6)
    
    if playerRoll >= threshold:
        return True
    else:
        return False

def proceed():
    proceed = input("Press enter to proceed.")
    print(" ")

def wait(time): # Lua relic
    if FASTFORWARD == False:
        sleep(time)

def printVoteNotation(votecount, revotecount, nullifiedcount):
    notation = None
    oldnotation = None
    if revotecount and nullifiedcount:
        for num in revotecount:
            if not notation and num > 0:
                notation = str(num)
            elif num > 0:
                notation += f"-{num}"
        for num in votecount:
            if not oldnotation and num > 0:
                oldnotation = str(num)
            elif num > 0:
                oldnotation += f"-{num}"
        for num in nullifiedcount:
            if not oldnotation:
                oldnotation = num
            else:
                oldnotation += f"-{num}"

        notation += f" ({oldnotation})"
    elif nullifiedcount:
        for num in votecount:
            if not notation and num > 0:
                notation = str(num)
            elif num > 0:
                notation += f"-{num}"
        for num in nullifiedcount:
            if not notation:
                notation = num
            else:
                notation += f"-{num}"
    elif revotecount:
        for num in revotecount:
            if not notation and num > 0:
                notation = str(num)
            elif num > 0:
                notation += f"-{num}"
        for num in votecount:
            if not oldnotation and num > 0:
                oldnotation = str(num)
            elif num > 0:
                oldnotation += f"-{num}"

        notation += f" ({oldnotation})"
    else:
        for num in votecount:
            if not notation and num > 0:
                notation = str(num)
            elif num > 0:
                notation += f"-{num}"
    
    return notation