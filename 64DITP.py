import random
from time import sleep
from colorama import Fore, Style

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
# Player Names
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
# Jury Name
juryName = "Jury"
# Invincibility Name
immunityName = "Individual Immunity"

# [[ If you know what you're doing, have fun tweaking below! ]] ----------------------------------------------------------------------------------

numPlayers = 64
jury = []

class Player:
    def __init__(self, name, showdownPoints, juryVotes):
        self.name = name
        self.showdownPoints = showdownPoints
        self.juryVotes = juryVotes

def Elimination(Team):
    eliminated = random.choice(Team)
    print(f"{eliminated.name} was voted out. {numPlayers - 1} remain.\n")
    Team.remove(eliminated)

    if numPlayers < 17:
        print(f"They are inducted as member {17 - numPlayers} of the {juryName}.\n")
        jury.append(eliminated)

def printTeams():
    for x in range(len(teams)):
        print(f"{teamColors[x]}[[{teamNames[x]}]]{Style.RESET_ALL}")
        for z in teams[x]:
            print(z.name)
        print(" ")
        
def printPlayersInMerge(Team):
    print(f"{Fore.RED}[[{mergeName}]]{Style.RESET_ALL}")
    for x in Team:
        print(x.name)
    print(" ")

def proceed():
    proceed = input("Press enter to proceed.")
    print(proceed)

# names_string = input("Enter names of contestants, separated by a comma. (Example: 'Alpha,Bravo,...')\n")

players = [Player(item, 0, 0) for item in names]
notChosen = players.copy()

teams = [[],[],[],[]]
teamNames = q1Names
teamColors = q1Colors

print("64 Days in the Pit")
print(f"{Fore.GREEN}[[DAY ONE SCHOOLYARD PICK]]{Style.RESET_ALL}")
teamId = 0
while len(notChosen) > 1:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    notChosen.remove(player)
    teamId += 1
    if teamId > 3:
        teamId = 0

printTeams()
print(f"{Fore.GREEN}[[FIRST QUARTER - FOUR-TEAM PHASE]]{Style.RESET_ALL}")
proceed()

while numPlayers > 48:
    print(f"Day {65 - numPlayers}")
    losers = random.randint(0, 3)
    print(f"{teamNames[losers]} lost the challenge!")
    Elimination(teams[losers])
    numPlayers -= 1

    sleep(1)
printTeams()
print(f"{Fore.GREEN}[[SECOND QUARTER - THREE-TEAM PHASE]]{Style.RESET_ALL}")
proceed()
# First Quarter End
for x in teams:
    notChosen.extend(x)
teams.clear()

teams = [[],[],[]]
teamNames = q2Names
teamColors = q2Colors
teamId = 0
while len(notChosen) > 0:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    notChosen.remove(player)
    teamId += 1
    if teamId > 2:
        teamId = 0

printTeams()
print("The teams have been swapped randomly. The Second Quarter begins.")
proceed()

while numPlayers > 32:
    print(f"Day {65 - numPlayers}")
    losers = random.randint(0, 2)
    print(f"{teamNames[losers]} lost the challenge!")
    Elimination(teams[losers])
    numPlayers -= 1

    sleep(1)
printTeams()
print(f"{Fore.GREEN}[[THIRD QUARTER - TWO-TEAM PHASE]]{Style.RESET_ALL}")
proceed()

# Second Quarter End
for x in teams:
    notChosen.extend(x)
teams.clear()

teams = [[],[]]
teamNames = q3Names
teamColors = q3Colors
teamId = 0
while len(notChosen) > 0:
    player = random.choice(notChosen)
    teams[teamId].append(player)
    notChosen.remove(player)
    teamId += 1
    if teamId > 1:
        teamId = 0

printTeams()
print("The halfway point of players has been reached. The teams have been swapped again. The Third Quarter begins.")
proceed()

while numPlayers > 16:
    print(f"Day {65 - numPlayers}")
    losers = random.randint(0, 1)
    print(f"{teamNames[losers]} lost the challenge!")
    Elimination(teams[losers])
    numPlayers -= 1

    sleep(1)
printTeams()
proceed()
# Third Quarter End
print("The teams have officially merged. For the first half of the merge, the first half of competitors who win the challenge win immunity.")
for x in teams:
    notChosen.extend(x)
teams.clear()
printPlayersInMerge(notChosen)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (HAVE-GOTS vs. HAVE-NOTS)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 8:
    print(f"Day {65 - numPlayers}")

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
    printTeams()
    sleep(2)

    Elimination(teams[1])
    numPlayers -= 1
    for x in teams:
        notChosen.extend(x)
    teams.clear()

    sleep(3)
print("The Have-Gots vs. Have-Nots phase is over. Individual immunity is now in effect.")
printPlayersInMerge(notChosen)
print(f"{Fore.GREEN}[[FOURTH QUARTER - MERGE (INDIVIDUAL IMMUNITY)]]{Style.RESET_ALL}")
proceed()

while numPlayers > 3:
    print(f"Day {65 - numPlayers}")
    printPlayersInMerge(notChosen)
    immune = random.choice(notChosen)
    notChosen.remove(immune)
    print(f"{immune.name} won {immunityName}.")
    sleep(2)

    Elimination(notChosen)
    numPlayers -= 1
    notChosen.append(immune)

    sleep(3)
printPlayersInMerge(notChosen)
print(f"Day 62")
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
jury.append(fallenAngel)

printPlayersInMerge(notChosen)
print(f"Day 64")
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
    runnerUp = random.choice(notChosen) # replace with tiebreaker later
notChosen.remove(runnerUp)
print(f"{runnerUp.name} failed to win the {juryName} Vote, and was eliminated in 2nd place.")

winner = random.choice(notChosen)
notChosen.remove(winner)
print(f"{winner.name} won.")

sleep(10)
