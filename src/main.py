from colorama import Fore, Style
from pathlib import Path
import random
import math
import json
import os

file = Path(__file__)
parent = file.parent
os.chdir(parent)

from challenges import teamChallenge, challengeMerge
from gamefunctions import gameEvents, schoolyardPick, elimination
from utils import suffix, getShowdownPoints, proceed, wait, printTeamNotation
from config import season_name, names, q1Names, q1Colors, q2Names, q2Colors, q3Names, q3Colors, mergeName, q4Colors, mergeColor, juryName, immunityName, firstSwapThreshold, secondSwapThreshold, mergeThreshold, finalThreshold, startingTeams, mergeatory, PRESET_PROFILES, PROFILE_FILE_PATH

# If you know what you're doing, have fun tweaking below! ----------------------------------------------------------------------------------

# [[ SIM FUNCTIONS ]] ----------------------------------------------------------------------------------

class Player:
    def __init__(self, name, physStat, stratStat, socStat, notoriety, faction):
        self.name = name
        # Game Points
        self.showdownPoints = 0
        self.juryVotes = 0

        self.idols = []

        # Team Colors
        self.color1 = None
        self.color2 = None
        self.color3 = None

        # Stats
        self.physStat = physStat
        self.stratStat = stratStat
        self.socStat = socStat
        self.notoriety = notoriety
        self.faction = faction

def decode(obj):
    return Player(obj['name'], obj['physStat'], obj['stratStat'], obj['socStat'], obj['notoriety'], obj['faction'])

def logBootOrder():
    with open("simulations.txt", "w") as log:
        for x in range(len(bootOrder)):
            log.write(f"{bootOrder[x].name}\n") # {x+1}{suffix(x+1)}: 
        log.write("\n")

    print("Simulation boot order logged in simulations.txt")

def printIdols():
    print(f"{Fore.GREEN}[[ Idols ]]{Style.RESET_ALL}")
    for player in players:
        if len(player.idols):
            for x in player.idols:
                print(player.name + " - " + x)

def printTeams(showTeams):
    for x in range(len(teams)):
        print(f"{teamColors[x]}[[{teamNames[x]}]]{Style.RESET_ALL}")
        for z in teams[x]:
            if showTeams == True:
                print(z.name + printTeamNotation(z))
            else:
                if z.faction == "Unaffiliated":
                    print(z.name + f" [{z.notoriety}]")
                else:
                    print(z.name + f" [{z.notoriety}] ({Style.DIM}{z.faction.color}{z.faction.name}{Style.RESET_ALL})")
        print(" ")
        
def printPlayersIn(Team, name, color, showTeams):
    print(f"{color}[[{name}]]{Style.RESET_ALL}")
    for x in Team:
        if showTeams == True:
            print(x.name + printTeamNotation(x))
        else:
            if x.faction == "Unaffiliated":
                print(x.name + f" [{x.notoriety}]")
            else:
                print(x.name + f" [{x.notoriety}] ({Style.DIM}{x.faction.color}{x.faction.name}{Style.RESET_ALL})")
    print(" ")

def clearTeams():
    for x in teams:
        notChosen.extend(x)
    teams.clear()

def mergeElimination(originalNominated, originalVotingPool):
    printIdols()
    wait(2)

    eliminated, votingNotation = elimination(originalNominated, originalVotingPool)

    print(f"{castSize + 1 - numPlayers}{suffix(castSize + 1 - numPlayers)} person voted out of {season_name}...")
    wait(3)
    print(f"{eliminated.name}. {numPlayers - 1} remain.\n")
    print(f"Vote Notation: {votingNotation}")
    
    Eliminate(eliminated, originalNominated, votingNotation)

def getSmallestTeamSize():
    teamSize = teams.copy()
    teamSize.sort(key=len)

    return len(teamSize[0])

def teamRound():
    global numPlayers
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        gameEvents(team, quarter)
    wait(1)
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        gameEvents(team, quarter)
    wait(1)

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    printIdols()
    wait(2)
    eliminated, votingNotation = elimination(teams[losers], teams[losers])

    print(f"{castSize + 1 - numPlayers}{suffix(castSize + 1 - numPlayers)} person voted out of {season_name}...")
    wait(3)
    print(f"{eliminated.name}. {numPlayers - 1} remain.\n")
    print(f"Vote Notation: {votingNotation}")
    
    Eliminate(eliminated, teams[losers], votingNotation)
    
    proceed()

def teamSwap(colorSlot):
    teamId = 0
    while len(notChosen) > 0:
        player = random.choice(notChosen)
        teams[teamId].append(player)
        match colorSlot:
            case 2:
                player.color2 = teamColors[teamId]
            case 2:
                player.color3 = teamColors[teamId]
        notChosen.remove(player)
        teamId += 1
        if teamId > len(teams) - 1:
            teamId = 0

def Eliminate(Player, team, voteNotation):
    global numPlayers
    if numPlayers < 3:
        print(" ")
    elif numPlayers == 3:
        print(f"They are inducted as the {mergeThreshold + 1 - numPlayers}th and final member of the {juryName}.\n")
        jury.append(Player)
    elif numPlayers <= mergeThreshold:
        print(f"They are inducted as the {mergeThreshold + 1 - numPlayers}{suffix(mergeThreshold + 1 - numPlayers)} member of the {juryName}.\n")
        jury.append(Player)
    numPlayers -= 1
    bootOrder.insert(0, Player)
    team.remove(Player)
    players.remove(Player)
    voteNotations.append(voteNotation)


    if Player.faction != "Unaffiliated":
        Player.faction.kick_member(Player)


# [[ SIMULATION ]] ----------------------------------------------------------------------------------

players = [Player(item, random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), 0, "Unaffiliated") for item in names]

if PRESET_PROFILES == True:
    try:
        with open(PROFILE_FILE_PATH, 'r') as f:
            data = json.load(f, object_hook=decode)

            for player in range(min(len(players), len(data))): # If not 64 players, then replace up to that many players
                players[player] = data[player]

            # if more than default entries, add them to the pile so they might be picked out via random sample
            if len(data) > len(players):
                players.extend(data[len(players):])
    except FileNotFoundError:
        print(f"Error: file '{PROFILE_FILE_PATH}' not found")
    except json.JSONDecodeError:
        print(f"Error: syntax error in '{PROFILE_FILE_PATH}'")
    except Exception as e:
        print(f"Error: {e}")

castSize = len(players)
numPlayers = len(players)
jury = []
bootOrder = []
voteNotations = []
factions = []
challenges = []
quarter = 1

proceed()

notChosen = players.copy()

print(f"{season_name}")

if (startingTeams > 4):

    teams = [[],[],[],[]]
    teamNames = q1Names
    teamColors = q1Colors

    schoolyardPick(notChosen, teams, teamColors)
    
    printTeams(True)
    print(f"{Fore.GREEN}[[FIRST QUARTER - FOUR-TEAM PHASE]]{Style.RESET_ALL}")
    proceed()

    while numPlayers > firstSwapThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(True)
    print(f"{Fore.GREEN}[[SECOND QUARTER - THREE-TEAM PHASE]]{Style.RESET_ALL}")
    quarter += 1
    proceed()
    # First Quarter End
    clearTeams()

    teams = [[],[],[]]
    teamNames = q2Names
    teamColors = q2Colors
    teamSwap(2)

    printTeams(True)
    print("The teams have been swapped randomly. The Second Quarter begins.")
    proceed()

    while numPlayers > secondSwapThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(True)
    print(f"{Fore.GREEN}[[THIRD QUARTER - TWO-TEAM PHASE]]{Style.RESET_ALL}")
    quarter += 1
    proceed()

    # Second Quarter End
    clearTeams()

    teams = [[],[]]
    teamNames = q3Names
    teamColors = q3Colors
    teamSwap(3)

    printTeams(True)
    print("The halfway point of players has been reached. The teams have been swapped again. The Third Quarter begins.")
    proceed()

    while numPlayers > mergeThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(False)
    proceed()
    # Third Quarter End
    quarter += 1
elif (startingTeams == 3):
    teams = [[],[],[]]
    teamNames = q2Names
    teamColors = q2Colors

    schoolyardPick(notChosen, teams, teamColors)
    
    printTeams(True)
    print(f"{Fore.GREEN}[[THREE-TEAM PHASE]]{Style.RESET_ALL}")
    proceed()

    while numPlayers > firstSwapThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(True)
    print(f"{Fore.GREEN}[[TWO-TEAM PHASE]]{Style.RESET_ALL}")
    quarter += 2
    proceed()
    # First Quarter End
    clearTeams()

    teams = [[],[]]
    teamNames = q3Names
    teamColors = q3Colors
    teamSwap(2)

    printTeams(True)
    print("The teams have been swapped randomly. The Second Quarter begins.")
    proceed()

    while numPlayers > mergeThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(True)
    print(f"{Fore.GREEN}[[THIRD QUARTER - TWO-TEAM PHASE]]{Style.RESET_ALL}")
    proceed()
    # Third Quarter End
    quarter += 1
elif (startingTeams < 3):
    teams = [[],[]]
    teamNames = q3Names
    teamColors = q3Colors

    schoolyardPick(notChosen, teams, teamColors)
    
    printTeams(True)
    print(f"{Fore.GREEN}[[TWO-TEAM PHASE]]{Style.RESET_ALL}")
    proceed()

    while numPlayers > mergeThreshold and getSmallestTeamSize() > 1:
        teamRound()
    printTeams(True)
    proceed()
    # Third Quarter End
    quarter += 3

if mergeatory:
    print("The teams have officially merged. For the first half of the merge, the first half of competitors who win the challenge win immunity.")
    clearTeams()
    printPlayersIn(notChosen, mergeName, mergeColor, True)
    print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (HAVE-GOTS vs. HAVE-NOTS)]]{Style.RESET_ALL}")
    proceed()

    while numPlayers > finalThreshold:
        print(f"[- Day {castSize + 1 - numPlayers} -]\n")

        gameEvents(notChosen, quarter)

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

        gameEvents(teams[0] + teams[1], quarter)
        wait(2)
        printTeams(False)

        mergeElimination(teams[1], teams[0]+teams[1])
        clearTeams()

        proceed()
    print("The Have-Gots vs. Have-Nots phase is over. Individual immunity is now in effect.")
else:
    print("The teams have officially merged. Individual immunity is now in effect.")
    clearTeams()
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (INDIVIDUAL IMMUNITY)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 3:
    print(f"[- Day {castSize + 1 - numPlayers} -]\n")
    printPlayersIn(notChosen, mergeName, mergeColor, False)
    gameEvents(notChosen, quarter)
    wait(2)
    
    challengeResults = challengeMerge(False, 0, challenges, notChosen)
    immune = notChosen[challengeResults[0]] # In Elite 8 phase, only the top challenge performer is given immunity
    immune.notoriety += 1

    notChosen.remove(immune)
    print(f"{immune.name} won {immunityName}.")
    
    wait(2)
    gameEvents(notChosen, quarter)
    wait(2)

    mergeElimination(notChosen, notChosen+[immune])
    notChosen.append(immune)

    proceed()
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"[- Day {castSize - 2} -]\n")
print("The final challenge, to decide which of the final 3 makes it to the final 2, is a marathon of every previous challenge in order. The player with the least wins after all 61 rounds will fail to qualify.")
print(f"{Fore.GREEN}[[FINAL THREE CHALLENGE - THE ULTIMATE SHOWDOWN]]{Style.RESET_ALL}")
proceed()

# Ultimate Showdown

for x in range(len(challenges)):
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

showdownNotation = f"{notChosen[0].showdownPoints}-{notChosen[1].showdownPoints}-{notChosen[2].showdownPoints}"
print(f"{fallenAngel.name} failed to qualify for the finale after the Ultimate Showdown, and was eliminated in 3rd place.")
    
Eliminate(fallenAngel, notChosen, showdownNotation)

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
    winner = notChosen[1]
elif notChosen[1].juryVotes < notChosen[0].juryVotes:
    runnerUp = notChosen[1]
    winner = notChosen[0]
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
        winner = notChosen[1]
    else:
        runnerUp = notChosen[1]
        winner = notChosen[0]

print(f"{runnerUp.name} failed to win the {juryName} Vote, and was eliminated in 2nd place as the runner-up.\n")

print(f"{winner.name} is the winner of {season_name}.")

Eliminate(runnerUp, notChosen, f"{runnerUp.juryVotes}-{winner.juryVotes}")
Eliminate(winner, notChosen, f"{winner.juryVotes}-{runnerUp.juryVotes}") # even winners must die the same death

proceed()
if startingTeams > 3:
    for x in range(len(bootOrder)):
        if x < mergeThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].name}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        elif x < secondSwapThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color3}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        elif x < firstSwapThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color2}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        else:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color1}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
elif startingTeams == 3:
    for x in range(len(bootOrder)):
        if x < mergeThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].name}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        elif x < firstSwapThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color2}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        else:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color1}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
else:
    for x in range(len(bootOrder)):
        if x < mergeThreshold:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].name}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")
        else:
            print(f"{x+1}{suffix(x+1)}: {bootOrder[x].color1}{bootOrder[x].name}{Style.RESET_ALL}" + f"{printTeamNotation(bootOrder[x])} - {voteNotations[castSize - x - 1]}")

logBootOrder()
        
proceed()
