import random
import math
import json
import os
from time import sleep
from colorama import Fore, Style
from challenges import teamChallenge, challengeMerge
from pathlib import Path

file = Path(__file__)
parent = file.parent
os.chdir(parent)

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
# Player Names
season_name = "64 Days in the Pit - The Ultimate Showdown"
names = ["Death Man","Boxy","Polandball","Satan","Stunt Devil","Lukey","Koda","Mitochondria","Pencil","Ronny the Banana","Tom Brady","Atom","Chad","King Lorenzo","Sticky Joe","Trogdor the Burninator","Boat Crew","Terezi Pyrope","Homestar Runner","Carl Grimes","Mr Wilson","Gamer","Hexbug","Four","ChrisPop","Muscles","Erika Faust","Ellie Lander","Teresa Tayliss","Dr Horrible","Billy Blockhead","Nagito Komaeda","Joe","Boston Rob","Dog","Tommy Walter","Germanyball","Americaball","Big Rig","Transparent Red","Joey","Petra","Isaac Creighton","Hunter Moses","Jack Dawson","Josephine Mercier","Roco","Horatio Caine","Frederick","Watch","V2","Nitro","Vriska Serket","Todd","Jackson","2-D","OG","Mr Ben","Tom","Lauren","Martin","Captain Hammer","Heathcliff","The Miser"]
# First Quarter Tribe Names
q1Names = ["Tomamasi","Raging Rapids","Dangerous Dynamites","Eclipsed Survivors"]
q1Colors = [Fore.YELLOW, Fore.BLUE, Fore.RED, Fore.GREEN]
# Second Quarter Tribe Names
q2Names = ["Orange Lionhearts","Fuchsia Rulers","Serene Sealions"]
q2Colors = [Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
# Third Quarter Tribe Names
q3Names = ["Hazardous Dukes","Midnight Lights"]
q3Colors = [Fore.YELLOW, Fore.BLUE]
# Merge Tribe Name
mergeName = "Elite 16"
q4Colors = [Fore.GREEN, Fore.RED]
mergeColor = Fore.YELLOW
# Jury Name
juryName = "Jury"
# Invincibility Name
immunityName = "Individual Immunity"

FASTFORWARD = False

PRESET_PROFILES = True
PROFILE_FILE_PATH = 'profiles.json'

# If you know what you're doing, have fun tweaking below! ----------------------------------------------------------------------------------

# [[ IMPORTANT SIMULATION STUFF ]] ----------------------------------------------------------------------------------
castSize = len(names)
numPlayers = len(names)
jury = []
bootOrder = []
challenges = []
quarter = 1

class Player:
    def __init__(self, name, showdownPoints, juryVotes, color1, color2, color3, physStat, stratStat, socStat, notoriety, faction):
        self.name = name
        # Game Points
        self.showdownPoints = showdownPoints
        self.juryVotes = juryVotes

        # Team Colors
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3

        # Stats
        self.physStat = physStat
        self.stratStat = stratStat
        self.socStat = socStat
        self.notoriety = notoriety
        self.faction = faction

def decode(obj):
    return Player(obj['name'], 0, 0, None, None, None, obj['physStat'], obj['stratStat'], obj['socStat'], obj['notoriety'], obj['faction'])
    
# [[ SIM FUNCTIONS ]] ----------------------------------------------------------------------------------

def Elimination(Team):

    # Future voting logic goes here.

    chances = Team.copy()
    for x in Team:
        chances.extend(addWeight(x, x.notoriety))

    eliminated = random.choice(chances) # For now (and as in 2018) the eliminated contestant is random

    print(f"{castSize + 1 - numPlayers}{suffix(castSize + 1 - numPlayers)} person voted out of {season_name}...")
    wait(3)
    print(f"{eliminated.name}. {numPlayers - 1} remain.\n")
    Team.remove(eliminated)

    if numPlayers < 17:
        print(f"They are inducted as the {17 - numPlayers}{suffix(17 - numPlayers)} member of the {juryName}.\n")
        jury.append(eliminated)

    bootOrder.insert(0, eliminated)

def printTeams(showTeams):
    for x in range(len(teams)):
        print(f"{teamColors[x]}[[{teamNames[x]}]]{Style.RESET_ALL}")
        for z in teams[x]:
            if showTeams == True:
                match quarter:
                    case 2:
                        print(z.name + f" [{z.color1}*{Style.RESET_ALL}]")
                    case 3:
                        print(z.name + f" [{z.color1}*{z.color2}*{Style.RESET_ALL}]")
                    case 4:
                        print(z.name + f" [{z.color1}*{z.color2}*{z.color3}*{Style.RESET_ALL}]")
                    case _:
                        print(z.name)
            else:
                print(z.name)
        print(" ")
        
def printPlayersIn(Team, name, color, showTeams):
    print(f"{color}[[{name}]]{Style.RESET_ALL}")
    for x in Team:
        if showTeams == True:
            match quarter:
                case 2:
                    print(x.name + f" [{x.color1}*{Style.RESET_ALL}]")
                case 3:
                    print(x.name + f" [{x.color1}*{x.color2}*{Style.RESET_ALL}]")
                case 4:
                    print(x.name + f" [{x.color1}*{x.color2}*{x.color3}*{Style.RESET_ALL}]")
                case _:
                    print(x.name)
        else:
            print(x.name)
    print(" ")

def suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def proceed():
    proceed = input("Press enter to proceed.")
    print(" ")

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

def randomScope(player):
    """
    Get a stat.
    """
    return random.randint(1, 64)

def addWeight(player, stat):
    weight = []
    for x in range(stat):
        weight.append(player)

    return weight

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

def clearTeams():
    for x in teams:
        notChosen.extend(x)
    teams.clear()

def wait(time): # Lua relic
    if FASTFORWARD == False:
        sleep(time)

# [[ SIMULATION ]] ----------------------------------------------------------------------------------

players = [Player(item, 0, 0, None, None, None, random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), 0, "Unaffiliated") for item in names]

if PRESET_PROFILES == True:
    try:
        with open(PROFILE_FILE_PATH, 'r') as f:
            data = json.load(f, object_hook=decode)

            for player in range(len(data)): # If not 64 players, then replace up to that many players
                players[player] = data[player]
    except FileNotFoundError:
        print(f"Error: file '{PROFILE_FILE_PATH}' not found")
    except json.JSONDecodeError:
        print(f"Error: syntax error in '{PROFILE_FILE_PATH}'")
    except Exception as e:
        print(f"Error: {e}")
proceed()

notChosen = players.copy()

teams = [[],[],[],[]]
teamNames = q1Names
teamColors = q1Colors

teamCaptains = [None, None, None, None] # Purely cosmetic
captainPreference = [None, None, None, None]

print(f"{season_name}")
print(f"{Fore.GREEN}[[DAY ONE SCHOOLYARD PICK]]{Style.RESET_ALL}")
teamId = 0

for x in range(4):
    teamCaptain = random.choice(notChosen)
    teams[teamId].append(teamCaptain)
    teamCaptain.color1 = teamColors[teamId]
    teamCaptains[teamId] = teamCaptain
    notChosen.remove(teamCaptain)
    teamId += 1
    if teamId > 3:
        teamId = 0

print(f"The team captains are randomly selected as {teamCaptains[0].name}, {teamCaptains[1].name}, {teamCaptains[2].name}, and {teamCaptains[3].name}.")
for x in range(len(captainPreference)):
    preference = random.randint(1, 6)
    match preference:
        case 1: # Smart Team
            captainPreference[x] = preference
            print(f"{teamCaptains[x].name} wants to choose a team of intelligent players.")
        case 2: # Social Team
            captainPreference[x] = preference
            print(f"{teamCaptains[x].name} wants to choose a team of social players.")
        case 3: # Random Team
            captainPreference[x] = preference
            print(f"{teamCaptains[x].name} has no team preference.")
        case _: # Strong Team
            captainPreference[x] = preference
            print(f"{teamCaptains[x].name} wants to pick a physically strong team.")

wait(1)

while len(notChosen) > 0:
    match captainPreference[teamId]:
        case 1: # Smart Team
            notChosen.sort(reverse=True, key=stratScope)
        case 2: # Social Team
            notChosen.sort(reverse=True, key=socScope)
        case 3: # Random Team
            notChosen.sort(reverse=True, key=randomScope)
        case _: # Strong Team
            notChosen.sort(reverse=True, key=physScope)

    player = notChosen[0]

    print(f"{teamCaptains[teamId].name} chooses {player.name}.")
    teams[teamId].append(player)
    player.color1 = teamColors[teamId]
    notChosen.remove(player)
    teamId += 1
    if teamId > 3:
        teamId = 0
    wait(.5)

printTeams(True)
print(f"{Fore.GREEN}[[FIRST QUARTER - FOUR-TEAM PHASE]]{Style.RESET_ALL}")
proceed()

while numPlayers > 48:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    losers = teamChallenge(challenges, teams, teamNames, teamColors)

    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)
    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers])
    numPlayers -= 1

    proceed()
printTeams(True)
print(f"{Fore.GREEN}[[SECOND QUARTER - THREE-TEAM PHASE]]{Style.RESET_ALL}")
quarter += 1
proceed()
# First Quarter End
clearTeams()

teams = [[],[],[]]
teamNames = q2Names
teamColors = q2Colors
teamId = 0
while len(notChosen) > 0:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    player.color2 = teamColors[teamId]
    notChosen.remove(player)
    teamId += 1
    if teamId > 2:
        teamId = 0

printTeams(True)
print("The teams have been swapped randomly. The Second Quarter begins.")
proceed()

while numPlayers > 32:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers])
    numPlayers -= 1

    proceed()
printTeams(True)
print(f"{Fore.GREEN}[[THIRD QUARTER - TWO-TEAM PHASE]]{Style.RESET_ALL}")
quarter += 1
proceed()

# Second Quarter End
clearTeams()

teams = [[],[]]
teamNames = q3Names
teamColors = q3Colors
teamId = 0
while len(notChosen) > 0:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    player.color3 = teamColors[teamId]
    notChosen.remove(player)
    teamId += 1
    if teamId > 1:
        teamId = 0

printTeams(True)
print("The halfway point of players has been reached. The teams have been swapped again. The Third Quarter begins.")
proceed()

while numPlayers > 16:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers])
    numPlayers -= 1

    proceed()
printTeams(False)
proceed()
# Third Quarter End
quarter += 1
print("The teams have officially merged. For the first half of the merge, the first half of competitors who win the challenge win immunity.")
clearTeams()
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (HAVE-GOTS vs. HAVE-NOTS)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 8:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")

    teams = [[],[]]
    teamNames = ["Immune","Lost the Challenge"]
    teamColors = q4Colors
    teamId = 0

    challengeResults = challengeMerge(False, 0, challenges, notChosen)
    threshold = math.ceil(numPlayers / 2)
    dangerzone = notChosen.copy()

    for x in range(threshold): # In first half of merge, number of immune contestants is always favored in odd rounds
        player = notChosen[challengeResults[x]] # Challenge results returns the indexes in order from best challenge performance to worst
        player.notoriety += 1

        teams[0].append(player) 
        dangerzone.remove(player)
    # Dump the losers in the loser team
    teams[1] = dangerzone.copy()
    del dangerzone
    notChosen.clear()

    printTeams(False)
    wait(2)

    Elimination(teams[1])
    numPlayers -= 1
    clearTeams()

    proceed()
print("The Have-Gots vs. Have-Nots phase is over. Individual immunity is now in effect.")
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (INDIVIDUAL IMMUNITY)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 3:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    printPlayersIn(notChosen, mergeName, mergeColor, False)
    
    challengeResults = challengeMerge(False, 0, challenges, notChosen)
    immune = notChosen[challengeResults[0]] # In Elite 8 phase, only the top challenge performer is given immunity
    immune.notoriety += 1

    notChosen.remove(immune)
    print(f"{immune.name} won {immunityName}.")
    
    wait(2)

    Elimination(notChosen)
    numPlayers -= 1
    notChosen.append(immune)

    proceed()
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"[- Day {castSize - 2} -]\n")
print("The final challenge, to decide which of the final 3 makes it to the final 2, is a marathon of every previous challenge in order. The player with the least wins after all 61 rounds will fail to qualify.")
print(f"{Fore.GREEN}[[FINAL THREE CHALLENGE - THE ULTIMATE SHOWDOWN]]{Style.RESET_ALL}")
proceed()

# Ultimate Showdown

for x in range(61):
    challengeResults = challengeMerge(True, x, challenges, notChosen)
    challengeWinner = notChosen[challengeResults[0]]
    challengeWinner.showdownPoints += 1

    print(f"Round {x+1}: {challengeWinner.name} wins. | {notChosen[0].name}: {notChosen[0].showdownPoints}, {notChosen[1].name}: {notChosen[1].showdownPoints}, {notChosen[2].name}: {notChosen[2].showdownPoints}\n")
    wait(0.5)

fallenAngel = None
notChosen.sort(reverse=True, key=getShowdownPoints)
if notChosen[2].showdownPoints == notChosen[1].showdownPoints:
    # Two-Way Tie, leader decides. (Three-Way Tie is possible with 60 but not with 61.)
    print(f"{notChosen[1].name} and {notChosen[2].name} tied. {notChosen[0].name}, the frontrunner, will cast the final vote for elimination.")
    fallenAngel = random.choice([notChosen[1], notChosen[2]])
    wait(1)
    print(f"They vote for {fallenAngel.name}.")
else: #Tie
    fallenAngel = notChosen[2]

wait(1)

notChosen.remove(fallenAngel)
print(f"{fallenAngel.name} failed to qualify for the finale after the Ultimate Showdown, and was eliminated in 3rd place.")
print(f"They are inducted as the {17 - numPlayers}th and final member of the {juryName}.\n")
numPlayers -= 1
jury.append(fallenAngel)
bootOrder.insert(0, fallenAngel)

printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"[- Day {castSize} -]\n")
print("The members of the jury, who all were eliminated after the merge, will now decide the winner.")
print(f"{Fore.GREEN}[[FINAL TWO - JURY VOTE]]{Style.RESET_ALL}")
proceed()

for x in range(len(jury)):
    weight = random.randint(0, notChosen[0].notoriety + notChosen[1].notoriety) # Chances of one player being voted for is based on how much they've played the game by winning challenges, etc
    if weight < notChosen[0].notoriety:
        votePick = notChosen[0]
    else:
        votePick = notChosen[1]
    votePick.juryVotes += 1

    # Bitter juries don't exist in 64DITP

    print(f"{jury[x].name} votes for {votePick.name}.\nThat's {notChosen[0].juryVotes} votes {notChosen[0].name}, {notChosen[1].juryVotes} votes {notChosen[1].name}, {len(jury) - (x + 1)} votes left.")
    wait(1)

runnerUp = None
if notChosen[0].juryVotes < notChosen[1].juryVotes:
    runnerUp = notChosen[0]
elif notChosen[1].juryVotes < notChosen[0].juryVotes:
    runnerUp = notChosen[1]
else: #Tie
    print(f"The votes tied. {fallenAngel.name}, the final {juryName} member, will cast an additional final vote.")
    wait(1)
    weight = random.randint(0, notChosen[0].notoriety + notChosen[1].notoriety) # Chances of one player being voted for is based on how much they've played the game by winning challenges, etc
    if weight < notChosen[0].notoriety:
        votePick = notChosen[0]
    else:
        votePick = notChosen[1]
    votePick.juryVotes += 1
    print(f"They vote for {votePick.name}.")

    if notChosen[0].juryVotes < notChosen[1].juryVotes:
        runnerUp = notChosen[0]
    else:
        runnerUp = notChosen[1]

bootOrder.insert(0, runnerUp)
notChosen.remove(runnerUp)
print(f"{runnerUp.name} failed to win the {juryName} Vote, and was eliminated in 2nd place as the runner-up.\n")
numPlayers -= 1

winner = random.choice(notChosen)
bootOrder.insert(0, winner)
notChosen.remove(winner)
print(f"{winner.name} is the winner of {season_name}.")

proceed()
for x in range(len(bootOrder)):
    if x < 16:
        print(f"{x+1}{suffix(x+1)}: {bootOrder[x].name}" + f" [{bootOrder[x].color1}*{bootOrder[x].color2}*{bootOrder[x].color3}*{Style.RESET_ALL}]")
    elif x < 32:
        print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color3}{bootOrder[x].name}{Style.RESET_ALL}" + f" [{bootOrder[x].color1}*{bootOrder[x].color2}*{Style.RESET_ALL}]")
    elif x < 48:
        print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color2}{bootOrder[x].name}{Style.RESET_ALL}" + f" [{bootOrder[x].color1}*{Style.RESET_ALL}]")
    else:
        print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color1}{bootOrder[x].name}{Style.RESET_ALL}")
        
proceed()
