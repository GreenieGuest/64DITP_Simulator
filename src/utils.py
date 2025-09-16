import random
from time import sleep
from config import FASTFORWARD, AUTORUN
from colorama import Fore, Style

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

def getAveragePlacement(player):
    """
    Get a stat.
    """
    return sum(player.data) / len(player.data)

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

def allScope(player):
    """
    Get a stat.
    """
    return random.randint(1, player.physStat) + random.randint(1, player.stratStat) + random.randint(1, player.socStat)

def randomScope(player):
    """
    Get a stat.
    """
    return random.randint(1, 100)

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
    if not AUTORUN:
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

        if not notation:
            notation = "0-0"
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

        if not notation:
            notation = "0-0"
        notation += f" ({oldnotation})"
    else:
        for num in votecount:
            if not notation and num > 0:
                notation = str(num)
            elif num > 0:
                notation += f"-{num}"
    
    return notation

def printTeamNotation(Player):
    if Player.color3:
        return f" [{Player.color1}*{Player.color2}*{Player.color3}*{Style.RESET_ALL}]"
    elif Player.color2:
        return f" [{Player.color1}*{Player.color2}*{Style.RESET_ALL}]"
    elif Player.color1:
        return f" [{Player.color1}*{Style.RESET_ALL}]"
    else:
        return ""

def findPlayerWithName(players, name):
    for x in players:
        if x.name == name:
            return x
    return None