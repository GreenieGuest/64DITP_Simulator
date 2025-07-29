import random
from time import sleep
from colorama import Fore, Style

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
# Player Names
season_name = "64 Days in the Pit - The Ewowltimate Showdown"
names = ["losered","TieTiePerson","scorb","#1 sigma Rizz lord","4DJumpman256","X_Ry","Dark","J_duude","Shorky","MayUnderFlowers","Purplegaze","Sparrowcat","JujuMas","GreenieGuest","iRDM","Xyloba","CloudySkyes","RainbowKnight","Brandy?","ThePinkBunnyEmpire","ALITL","Snoozingnewt","SinisterShovel","Midnight Light","whitecyclosa","terminatedslime","Catworld","xXBombs_AwayXx","ArnoobExtra","recc","Grammar Lee","Nerdy Gal","Koopa472","IceKeyHammer","Cohaki","Water Chestnut","LemonVenom","PoliteCheese1414","DogeBone3","PlasmicTrojan","hydrogencitrus","Srimochi","Gizmote","tr_","Deckardv","Juhmatok","mazuat","goobrey","Himo","Paintspot Infez","IntersectingPlanes","Yume Flamigiri","TrainGoBoom","MineFlex_B","#zackd","Twiggy","sictoabu","Swift Smartypants","cloverpepsi","thanos whale.","Onchú","kuminda.water.supply","Indigo","PengiQuin"]
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

# If you know what you're doing, have fun tweaking below! ----------------------------------------------------------------------------------

# [[ IMPORTANT SIMULATION STUFF ]] ----------------------------------------------------------------------------------
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

# [[ SIM FUNCTIONS ]] ----------------------------------------------------------------------------------

def Elimination(Team):

    # Future voting logic goes here.

    eliminated = random.choice(Team) # For now (and as in 2018) the eliminated contestant is random

    print(f"{65 - numPlayers}{suffix(65 - numPlayers)} person voted out of {season_name}...")
    sleep(3)
    print(f"{eliminated.name}. {numPlayers - 1} remain.\n")
    Team.remove(eliminated)

    if numPlayers < 17:
        print(f"They are inducted as the {17 - numPlayers}{suffix(17 - numPlayers)} member of the {juryName}.\n")
        jury.append(eliminated)

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

# [[ SIMULATION ]] ----------------------------------------------------------------------------------

players = [Player(item, 0, 0, None, None, None, random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), 0, "Unaffiliated") for item in names]
notChosen = players.copy()

teams = [[],[],[],[]]
teamNames = q1Names
teamColors = q1Colors

print(f"{season_name}")
print(f"{Fore.GREEN}[[DAY ONE SCHOOLYARD PICK]]{Style.RESET_ALL}")
teamId = 0
while len(notChosen) > 0:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    player.color1 = teamColors[teamId]
    notChosen.remove(player)
    teamId += 1
    if teamId > 3:
        teamId = 0

printTeams(True)
print(f"{Fore.GREEN}[[FIRST QUARTER - FOUR-TEAM PHASE]]{Style.RESET_ALL}")
proceed()

while numPlayers > 48:
    print(f"[- Day {65 - numPlayers} -]\n")
    losers = random.randint(0, 3)
    print(f"{teamNames[losers]} lost the challenge!")

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    sleep(2)
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
    print(f"[- Day {65 - numPlayers} -]\n")
    losers = random.randint(0, 2)
    print(f"{teamNames[losers]} lost the challenge!")

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    sleep(2)
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
    print(f"[- Day {65 - numPlayers} -]\n")
    losers = random.randint(0, 1)
    print(f"{teamNames[losers]} lost the challenge!")

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    sleep(2)
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
    print(f"[- Day {65 - numPlayers} -]\n")

    teams = [[],[]]
    teamNames = ["Immune","Lost the Challenge"]
    teamColors = q4Colors
    teamId = 0
    while len(notChosen) > 0:   
        player = random.choice(notChosen)
        teams[teamId].append(player)
        notChosen.remove(player)
        teamId += 1
        if teamId > 1:
           teamId = 0
    printTeams(False)
    sleep(2)

    Elimination(teams[1])
    numPlayers -= 1
    clearTeams()

    proceed()
print("The Have-Gots vs. Have-Nots phase is over. Individual immunity is now in effect.")
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (INDIVIDUAL IMMUNITY)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 3:
    print(f"[- Day {65 - numPlayers} -]\n")
    printPlayersIn(notChosen, mergeName, mergeColor, False)
    immune = random.choice(notChosen)
    notChosen.remove(immune)
    print(f"{immune.name} won {immunityName}.")
    
    sleep(2)

    Elimination(notChosen)
    numPlayers -= 1
    notChosen.append(immune)

    proceed()
printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"[- Day 62 -]\n")
print("The final challenge, to decide which of the final 3 makes it to the final 2, is a marathon of every previous challenge in order. The player with the least wins after all 61 rounds will fail to qualify.")
print(f"{Fore.GREEN}[[FINAL THREE CHALLENGE - THE ULTIMATE SHOWDOWN]]{Style.RESET_ALL}")
proceed()

# Ultimate Showdown

for x in range(61):
    challengeWinner = random.choice(notChosen)
    challengeWinner.showdownPoints += 1

    print(f"Round {x+1}: {challengeWinner.name} wins. | {notChosen[0].name}: {notChosen[0].showdownPoints}, {notChosen[1].name}: {notChosen[1].showdownPoints}, {notChosen[2].name}: {notChosen[2].showdownPoints}")
    sleep(0.5)

fallenAngel = None
if notChosen[0].showdownPoints < notChosen[1].showdownPoints and notChosen[0].showdownPoints < notChosen[2].showdownPoints:
    fallenAngel = notChosen[0]
elif notChosen[1].showdownPoints < notChosen[0].showdownPoints and notChosen[1].showdownPoints < notChosen[2].showdownPoints:
    fallenAngel = notChosen[1]
elif notChosen[2].showdownPoints < notChosen[0].showdownPoints and notChosen[2].showdownPoints < notChosen[1].showdownPoints:
    fallenAngel = notChosen[2]
else: #Tie
    fallenAngel = random.choice(notChosen) # replace with tiebreaker later

notChosen.remove(fallenAngel)
print(f"{fallenAngel.name} failed to qualify for the finale after the Ultimate Showdown, and was eliminated in 3rd place.")
print(f"They are inducted as the {17 - numPlayers}th and final member of the {juryName}.\n")
numPlayers -= 1
jury.append(fallenAngel)

printPlayersIn(notChosen, mergeName, mergeColor, True)
print(f"[- Day 64 -]\n")
print("The members of the jury, who all were eliminated after the merge, will now decide the winner.")
print(f"{Fore.GREEN}[[FINAL TWO - JURY VOTE]]{Style.RESET_ALL}")
proceed()

for x in range(len(jury)):
    votePick = random.choice(notChosen)
    votePick.juryVotes += 1

    print(f"{jury[x].name} votes for {votePick.name}.\nThat's {notChosen[0].juryVotes} votes {notChosen[0].name}, {notChosen[1].juryVotes} votes {notChosen[1].name}, {len(jury) - (x + 1)} votes left.")
    sleep(1)

runnerUp = None
if notChosen[0].juryVotes < notChosen[1].juryVotes:
    runnerUp = notChosen[0]
elif notChosen[1].juryVotes < notChosen[0].juryVotes:
    runnerUp = notChosen[1]
else: #Tie
    print(f"The votes tied. {fallenAngel.name}, the final {juryName} member, will cast an additional final vote.")
    sleep(1)
    votePick = random.choice(notChosen)
    votePick.juryVotes += 1
    print(f"They vote for {votePick.name}.")

    if notChosen[0].juryVotes < notChosen[1].juryVotes:
        runnerUp = notChosen[0]
    else:
        runnerUp = notChosen[1]

notChosen.remove(runnerUp)
print(f"{runnerUp.name} failed to win the {juryName} Vote, and was eliminated in 2nd place as the runner-up.\n")
numPlayers -= 1

winner = random.choice(notChosen)
notChosen.remove(winner)
print(f"{winner.name} is the winner of {season_name}.")

sleep(10)
