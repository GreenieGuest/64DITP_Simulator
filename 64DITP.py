import random
import math
from time import sleep
from colorama import Fore, Style
import json
from challenges import teamChallenge, challengeMerge
import os
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

FASTFORWARD = True

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

class Faction:
    def __init__(self, name, color, founder):
        self.name = name
        self.color = color
        self.founder = founder
        self.members = [founder]
        
    def add_member(self, player):
        self.members.append(player)
        player.faction = self

    def disband(self):
        for member in self.members:
            member.faction = "Unaffiliated"
        self.members.clear()
        
def decode(obj):
    return Player(obj['name'], 0, 0, None, None, None, obj['physStat'], obj['stratStat'], obj['socStat'], obj['notoriety'], obj['faction'])
    
# [[ SIM FUNCTIONS ]] ----------------------------------------------------------------------------------

def teamEvents(team):
    for playerA in team:
        # Form Alliance
        playerB = random.choice(team)
        if playerA != playerB and socScope(playerA) >= 3:
            if playerB.faction == "Unaffiliated":
                compatibility = abs(socScope(playerA) - socScope(playerB)) + abs(stratScope(playerA) - stratScope(playerB))
                if compatibility <= 2:
                    playerA.faction = f"{playerA.name}'s Alliance"
                    playerB.faction = f"{playerA.name}'s Alliance"
                    print(f"{playerA.name} has formed an alliance with {playerB.name}")
            elif playerA.faction != "Unaffiliated" and playerB.faction != "Unaffiliated":
                # Breakaway Alliance
                if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerA.faction != f"{playerA.name}'s Alliance":
                    print(f"{playerA.name} and {playerB.name} have left {playerA.faction} to form their own alliance!")
                    playerA.faction = f"{playerA.name}'s Alliance"
                    playerB.faction = f"{playerA.name}'s Alliance"
                    playerA.notoriety += 3
                    playerB.notoriety += 3
            else:
                if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerB.faction != playerA.faction:
                    print(f"{playerB.name} has left {playerB.faction} to form an alliance with {playerA.name}")
                    playerA.faction = f"{playerA.name}'s Alliance"
                    playerB.faction = f"{playerA.name}'s Alliance"
                    playerB.notoriety += 3

        # Disband Alliance
        if socScope(playerA) < 2 and playerA.faction != "Unaffiliated":
            agree = True
            count = 1
            for playerB in players:
                if playerA != playerB and playerB.faction == playerA.faction:
                    count += 1
                    if socScope(playerB) < 2 and agree == True:
                        agree = True
                    else:
                        agree = False

            if agree == True or count == 1:
                for player in players:
                    if player != playerA and player.faction == playerA.faction:
                        player.faction = "Unaffiliated"
                print(f"{playerA.faction} has disbanded.")
                playerA.faction = "Unaffiliated"

        # Invite into Alliance
        teammates = random.sample(team, 3)
        for playerB in teammates:
            if playerA != playerB and socScope(playerA) >= 3 and playerA.faction != "Unaffiliated":
                if playerB.faction == "Unaffiliated":
                    compatibility = abs(socScope(playerA) - socScope(playerB)) + abs(stratScope(playerA) - stratScope(playerB))
                    if compatibility <= 2:
                        print(f"{playerA.name} invited {playerB.name} to join {playerA.faction}")
                        playerB.faction = playerA.faction
                else:
                    if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerB.faction != playerA.faction:
                        print(f"{playerA.name} convinced {playerB.name} to leave {playerB.faction} and join {playerA.faction}")
                        playerB.faction = playerA.faction
                        playerB.notoriety += 3

        # Alliance Fracturing
        if socScope(playerA) < 3 and playerA.faction != "Unaffiliated":
            opposition = False
            count = 1
            for playerB in team:
                if playerA != playerB and playerB.faction == playerA.faction:
                    count += 1
                elif playerB.faction != playerA.faction and opposition == False:
                    opposition = True

            if count > 6 or opposition == False: # If the alliance has more than 6 members or they are the only alliance remaining on the team, it will fracture
                for playerB in team:
                    if playerB != playerA and playerB.faction == playerA.faction:
                        if socScope(playerB) < 2 or stratScope(playerA) > 4:
                            playerB.faction = f"{playerA.name}'s Alliance"
                print(f"{playerA.faction} has fractured.")
                playerA.faction = f"{playerA.name}'s Alliance"


        dynamics = socScope(playerA)
        if dynamics > 3 and playerA.notoriety > 50:
            playerA.notoriety -= (dynamics - 3)
            print(f"{playerA.name} lowers their threat level at camp.")
        elif dynamics == 1:
            playerA.notoriety += 1
            print(f"{playerA.name}'s name is discussed at camp as a potential target.")
        if playerA.notoriety < 0:
            playerA.notoriety = 0

def Elimination(originalNominated, originalVotingPool):
    # Each player in votingPool will vote for one player in nominated
    # Their decision is mostly based on notoriety but can be affected by factors such as alliance and social
    tie_count = 0
    nominated = originalNominated.copy()
    votingPool = originalVotingPool.copy()

    while tie_count < 2:
        votes = [0] * len(nominated)

        for voter in votingPool:
            weight = [0] * len(nominated)
            for i, player in enumerate(nominated):
                weight[i] += player.notoriety
                if player.faction == voter.faction and voter.faction != "Unaffiliated":
                    weight[i] -= 1000
                if player == voter:
                    weight[i] -= 1000

            decision = weight.copy()
            decision.sort(reverse=True)
            n = next((i for i, x in enumerate(decision) if x != decision[0]), len(decision)) # see how many people r tied

            # if multiple people have the same weight, decide based on random social roll
            if n == 1:
                votes[weight.index(decision[0])] += 1
                print(f"{voter.name} voted for {nominated[weight.index(decision[0])].name}. That's {votes[weight.index(decision[0])]} votes {nominated[weight.index(decision[0])].name}.")
            else:
                choices = []
                # Force voter to decide between one of the people with the highest vote-out priority
                for i in range(n):
                    choices.append(nominated[weight.index(decision[i])])
                    weight[weight.index(decision[i])] = 0 # allows us to get every player with the same level of weight
                choices.sort(key=socScope)
                votes[nominated.index(choices[0])] += 1

                votedFor = nominated[nominated.index(choices[0])].name

                print(f"{voter.name} decided to vote for {votedFor}. That's {votes[nominated.index(choices[0])]} votes {votedFor}.")
            wait(.5)


        decision = votes.copy()
        decision.sort(reverse=True)
        n = next((i for i, x in enumerate(decision) if x != decision[0]), len(decision)) # see how many people r tied
        # If the votes don't tie, continue as normal
        if n == 1:
            eliminated = nominated[votes.index(decision[0])]
            break
        elif n > 1: # If they do, re-vote - tied people are removed from the voting pool and are the only choices available to vote for
            tie_count += 1
            nominated.clear()
            if tie_count == 1:
                print(f"{Fore.RED}The votes tied. We will have a re-vote: the tied players will not be able to vote, but the remaining voters will only be allowed to vote for one of the tied players.{Style.RESET_ALL}")
                for i in range(n):
                    tietiedPerson = originalNominated[votes.index(decision[i])]
                    nominated.append(tietiedPerson)
                    votingPool.remove(tietiedPerson)
                    votes[votes.index(decision[i])] = 0
            else: # Since votes tied twice, players go to rocks - players immune but in the voting pool are spared, along with tied players
                print(f"{Fore.RED}The votes are deadlocked. We will now go to rocks - whoever draws the white rock is eliminated.{Style.RESET_ALL}")
                rockDrawers = votingPool.copy()
                for voter in votingPool:
                    if (voter in originalVotingPool) and (voter not in originalNominated):
                        rockDrawers.remove(voter)
                eliminated = random.choice(rockDrawers)

    print(f"{castSize + 1 - numPlayers}{suffix(castSize + 1 - numPlayers)} person voted out of {season_name}...")
    wait(3)
    print(f"{eliminated.name}. {numPlayers - 1} remain.\n")
    
    originalNominated.remove(eliminated)

    if numPlayers < 17:
        print(f"They are inducted as the {17 - numPlayers}{suffix(17 - numPlayers)} member of the {juryName}.\n")
        jury.append(eliminated)

    players.remove(eliminated)
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
            if x.faction == "Unaffiliated":
                print(x.name + f" [{x.notoriety}]")
            else:
                print(x.name + f" [{x.notoriety}] ({x.faction})")
    print(" ")

def suffix(n):
    if 11 <= n % 100 <= 13:
        return "th"
    else:
        return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")

def proceed():
    proceed = input("Press enter to proceed.")
    print(" ")

def clearTeams():
    for x in teams:
        notChosen.extend(x)
    teams.clear()

def wait(time): # Lua relic
    if FASTFORWARD == False:
        sleep(time)

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

# [[ SIMULATION ]] ----------------------------------------------------------------------------------

players = [Player(item, 0, 0, None, None, None, random.randint(1, 6), random.randint(1, 6), random.randint(1, 6), 0, "Unaffiliated") for item in names]

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
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)

    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)
    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers], teams[losers])
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
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)

    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers], teams[losers])
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
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)
    losers = teamChallenge(challenges, teams, teamNames, teamColors)
    for i, team in enumerate(teams):
        print(f"{teamColors[i]}[[{teamNames[i]} Events]]{Style.RESET_ALL}")
        teamEvents(team)

    print(f"\n{teamNames[losers]} lost the challenge!")
    wait(1)

    printPlayersIn(teams[losers], teamNames[losers], teamColors[losers], False)
    wait(2)
    Elimination(teams[losers], teams[losers])
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

    teamEvents(players)

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

    teamEvents(players)
    wait(2)
    printTeams(False)

    Elimination(teams[1], teams[0]+teams[1])
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
    teamEvents(players)
    wait(2)
    
    challengeResults = challengeMerge(False, 0, challenges, notChosen)
    immune = notChosen[challengeResults[0]] # In Elite 8 phase, only the top challenge performer is given immunity
    immune.notoriety += 1

    notChosen.remove(immune)
    print(f"{immune.name} won {immunityName}.")
    
    wait(2)
    teamEvents(players)
    wait(2)

    Elimination(notChosen, notChosen+[immune])
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
