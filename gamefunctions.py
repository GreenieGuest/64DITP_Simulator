import random
from colorama import Fore, Style

import os
from pathlib import Path

file = Path(__file__)
parent = file.parent
os.chdir(parent)

from utils import physScope, stratScope, socScope, notorietyScope, randomScope, allScope, wait, printVoteNotation

class Faction: #Unused for now
    def __init__(self, name, founder):
        self.name = name
        self.color = random.choice([Fore.YELLOW, Fore.BLUE, Fore.RED, Fore.GREEN, Fore.MAGENTA, Fore.CYAN])
        self.founder = founder
        self.members = [founder]

        self.target = None
        self.rival = None
        
    def add_member(self, player):
        if player not in self.members:
            self.members.append(player)
        if player.faction != self and player.faction != "Unaffiliated":
            player.faction.kick_member(player)
        player.faction = self
        
    def kick_member(self, player):
        if player in self.members:
            self.members.remove(player)
        player.faction = "Unaffiliated"

    def disband(self):
        for member in self.members:
           member.faction = "Unaffiliated"
        self.members.clear()

def gameEvents(team, quarter):
    for playerA in team:
        statusTypes = ["formAlliance", "disbandAlliance", "inviteIntoAlliance", "fractureAlliance", "manageNotoriety", "idolHunt", "targetAlliance"]
        
        for status in random.sample(statusTypes, 3):
            match status: # Players can only do three game moves per free time event realistically (they get plenty of opportunities)
                case "formAlliance":
                    # Form Alliance
                    playerB = random.choice(team)
                    if playerA != playerB and socScope(playerA) >= 3:
                        if playerB.faction == "Unaffiliated" and playerA.faction == "Unaffiliated":
                            compatibility = abs(socScope(playerA) - socScope(playerB)) + abs(stratScope(playerA) - stratScope(playerB))
                            if compatibility <= 2:
                                playerA.faction = Faction(f"{playerA.name}'s Alliance", playerA)
                                playerA.faction.add_member(playerB)
                                print(f"{playerA.name} has formed an alliance with {playerB.name}")
                        elif playerA.faction != "Unaffiliated" and playerB.faction != "Unaffiliated" and playerA.faction.founder != playerA:
                            # Breakaway Alliance (Dupes not allowed!)
                            if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerA.faction != f"{playerA.name}'s Alliance":
                                print(f"{playerA.name} and {playerB.name} have left {playerA.faction.name} to form their own alliance!")
                                playerA.faction.kick_member(playerA)
                                playerA.faction = Faction(f"{playerA.name}'s Alliance", playerA)
                                playerA.faction.add_member(playerB)
                                playerA.notoriety += 2
                                playerB.notoriety += 2
                        elif playerA.faction == "Unaffiliated":
                            if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerB.faction != playerA.faction:
                                print(f"{playerB.name} has left {playerB.faction.name} to form an alliance with {playerA.name}")
                                playerA.faction = Faction(f"{playerA.name}'s Alliance", playerA)
                                playerA.faction.add_member(playerB)
                                playerB.notoriety += 2
                case "disbandAlliance":
                    # Disband Alliance
                    if socScope(playerA) < 2 and playerA.faction != "Unaffiliated":
                        agree = True
                        for playerB in playerA.faction.members:
                            if socScope(playerB) < 2 and agree == True:
                                agree = True
                            else:
                                agree = False

                        if agree == True or len(playerA.faction.members) == 1:
                            print(f"{playerA.faction.name} has disbanded.")
                            playerA.faction.disband()
                case "inviteIntoAlliance":
                    # Invite into Alliance
                    if len(team) < 3:
                        teammates = random.sample(team, 1)
                    else:
                        teammates = random.sample(team, 3)
                    for playerB in teammates:
                        if playerA != playerB and socScope(playerA) >= 3 and playerA.faction != "Unaffiliated":
                            if playerB.faction == "Unaffiliated":
                                compatibility = abs(socScope(playerA) - socScope(playerB)) + abs(stratScope(playerA) - stratScope(playerB))
                                if compatibility <= 3:
                                    print(f"{playerA.name} invited {playerB.name} to join {playerA.faction.name}")
                                    playerA.faction.add_member(playerB)
                            else:
                                if stratScope(playerB) > 4 and socScope(playerB) < 3 and playerB.faction != playerA.faction:
                                    print(f"{playerA.name} convinced {playerB.name} to leave {playerB.faction.name} and join {playerA.faction.name}")
                                    playerA.faction.add_member(playerB)
                                    playerB.notoriety += 2
                case "fractureAlliance":
                    # Alliance Fracturing
                    if socScope(playerA) < 3 and playerA.faction != "Unaffiliated" and playerA.faction.founder != playerA:
                        opposition = False
                        for playerB in team:
                            if playerB.faction != playerA.faction and opposition == False:
                                opposition = True

                        if len(playerA.faction.members) > 7 or opposition == False: # If the alliance has more than 7 members or they are the only alliance remaining on the team, it will fracture
                            willingToLeave = []
                            for playerB in team:
                                if playerB != playerA and playerB.faction == playerA.faction:
                                    if socScope(playerB) < 2 or stratScope(playerA) > 4:
                                        willingToLeave.append(playerB)
                            if len(willingToLeave) >= 2:
                                print(f"{playerA.faction.name} has fractured.")
                                playerA.faction.kick_member(playerA)
                                playerA.faction = Faction(f"{playerA.name}'s Alliance", playerA)
                                for player in willingToLeave:
                                    playerA.faction.add_member(player)

                case "manageNotoriety":
                    dynamics = socScope(playerA)
                    if dynamics > 3 and playerA.notoriety > 10:
                        playerA.notoriety -= (dynamics - 2)
                        print(f"{playerA.name} lowers their threat level at camp.")
                    elif dynamics == 1:
                        playerA.notoriety += 1
                        print(f"{playerA.name}'s name is discussed at camp as a potential target.")
                    if playerA.notoriety < 0:
                        playerA.notoriety = 0
                case "idolHunt":
                    # Find Idol
                    idolHunt = randomScope(playerA)
                    if idolHunt > 95 and physScope(playerA) > 2:
                        print(f"{playerA.name} finds a Savior.")
                        playerA.idols.append("Savior")
                    elif idolHunt == 95 and physScope(playerA) > 2:
                        print(f"{playerA.name} finds a Guardian Angel.")
                        playerA.idols.append("Guardian Angel")
                case "targetAlliance":
                    # Convince alliance to target someone
                    if (stratScope(playerA) > 3 or socScope(playerA) > 3) and playerA.faction != "Unaffiliated":
                        threatRanking = team.copy()
                        for teammate in threatRanking:
                            if teammate.faction == playerA.faction:
                                threatRanking.remove(teammate)
                        if quarter == 1:
                            threatBasis = random.randint(1, 6)
                            match threatBasis:
                                case 1:
                                    threatRanking.sort(key=physScope)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for poor challenge performance.")
                                case 2:
                                    threatRanking.sort(key=stratScope)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being untrustworthy.")
                                case 3:
                                    threatRanking.sort(key=socScope)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being a social outcast.")
                                case _:
                                    threatRanking.sort(key=allScope)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} to strengthen the team.")

                            playerA.faction.target = threatRanking[0]
                        else:
                            threatBasis = random.randint(1, 6)
                            match threatBasis:
                                case 1:
                                    threatRanking.sort(key=physScope, reverse=True)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being a challenge threat.")
                                case 2:
                                    threatRanking.sort(key=stratScope, reverse=True)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being a strategic threat.")
                                case 3:
                                    threatRanking.sort(key=socScope, reverse=True)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being a social threat.")
                                case _:
                                    threatRanking.sort(key=allScope, reverse=True)
                                    print(f"{playerA.name} convinces {playerA.faction.name} to start targetting {threatRanking[0].name} for being an overall threat.")

                            playerA.faction.target = threatRanking[0]

    print(" ")

def schoolyardPick(playerPool, teams, teamColors):
    teamCaptains = [None] * len(teams)
    captainPreference = [None] * len(teams)

    print(f"{Fore.GREEN}[[DAY ONE SCHOOLYARD PICK]]{Style.RESET_ALL}")
    teamId = 0

    for x in range(len(teams)):
        teamCaptain = random.choice(playerPool)
        teams[teamId].append(teamCaptain)
        teamCaptain.color1 = teamColors[teamId]
        teamCaptains[teamId] = teamCaptain
        playerPool.remove(teamCaptain)
        teamId += 1
        if teamId > len(teams) - 1:
            teamId = 0

    print(f"The team captains are randomly selected as {', '.join(o.name for o in teamCaptains)}.")
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

    while len(playerPool) > 0:
        match captainPreference[teamId]:
            case 1: # Smart Team
                playerPool.sort(reverse=True, key=stratScope)
            case 2: # Social Team
                playerPool.sort(reverse=True, key=socScope)
            case 3: # Random Team
                playerPool.sort(reverse=True, key=randomScope)
            case _: # Strong Team
                playerPool.sort(reverse=True, key=physScope)

        player = playerPool[0]

        print(f"{teamCaptains[teamId].name} chooses {player.name}.")
        teams[teamId].append(player)
        player.color1 = teamColors[teamId]
        playerPool.remove(player)
        teamId += 1
        if teamId > len(teams) - 1:
            teamId = 0
        wait(.5)

def elimination(originalNominated, originalVotingPool):
    # Each player in votingPool will vote for one player in nominated
    # Their decision is mostly based on notoriety but can be affected by factors such as alliance and social
    tie_count = 0
    nominated = originalNominated.copy()
    votingPool = originalVotingPool.copy()
    votedFor = [] # Voted-for person per player are taken in order of their index in the original voting pool
    
    safeViaIdol = []

    # Vote Notation
    votecount = []
    revotecount = []
    nullifiedcount = []

    while tie_count < 2:
        # Vote counts per player are taken in order of their index in nominated
        votes = [0] * len(nominated)

        for voter in votingPool:
            weight = [0] * len(nominated)
            for i, player in enumerate(nominated):
                weight[i] += player.notoriety
                if player.faction == voter.faction and voter.faction != "Unaffiliated":
                    weight[i] -= 1000
                if player == voter:
                    weight[i] -= 1000
                if stratScope(player) > 3 and stratScope(voter) > 3: # Fear of idol play
                    weight[i] -= 5
                if voter.faction != "Unaffiliated" and player == voter.faction.target:
                    weight[i] += 5

            decision = weight.copy()
            decision.sort(reverse=True)
            n = next((i for i, x in enumerate(decision) if x != decision[0]), len(decision)) # see how many people r tied

            # if multiple people have the same weight, decide based on random social roll
            if n == 1:
                votes[weight.index(decision[0])] += 1
                votedFor.append(nominated[weight.index(decision[0])])
            else:
                choices = []
                # Force voter to decide between one of the people with the highest vote-out priority
                for i in range(n):
                    choices.append(nominated[weight.index(decision[i])])
                    weight[weight.index(decision[i])] = 0 # allows us to get every player with the same level of weight
                choices.sort(key=socScope)
                votes[nominated.index(choices[0])] += 1

                votedFor.append(nominated[nominated.index(choices[0])])

        # Tally the votes
        print("I'll go tally the votes...")
        wait(1)

        decision = votes.copy()
        votesRemaining = votes.copy() # for dramatic vote reading
        decision.sort(reverse=True)

        if tie_count == 0:
            print("If anybody has a Hidden Immunity Idol and you want to play it, now would be the time to do so...")
            wait(1)

            # Idol Plays (only doable before revote)
            # Savior Play (can be played before votes are read - requires strategic scope)
            for player in originalVotingPool:
                if ("Savior" in player.idols):
                    # Player Criteria: must be themselves, allied, and must not idol out another ally or themselves
                    threatIndex = nominated.copy()
                    threatIndex.sort(reverse=True, key=notorietyScope) # wrong readings happen for savior plays since votes are unknown at this point

                    biggestThreat = nominated[nominated.index(threatIndex[0])]
                    secondThreat = nominated[votes.index(decision[1])]

                    if (biggestThreat not in safeViaIdol) and (biggestThreat == player or (player.faction != "Unaffiliated" and biggestThreat.faction == player.faction and secondThreat.faction != player.faction and secondThreat != player)):
                        print(f"{Fore.GREEN}{player.name} plays their Savior for {biggestThreat.name}.{Style.RESET_ALL}")
                        player.notoriety += 3
                        # Add saved player to the list of the immune contestants to prevent them from being involved in rock draws
                        safeViaIdol.append(biggestThreat)

                        nullifiedcount.append(f"{votes[nominated.index(biggestThreat)]}*")
                        votes[nominated.index(biggestThreat)] = -2

                        # Remove the player's idol and reset the votes
                        player.idols.remove("Savior")
                        decision = votes.copy()
                        decision.sort(reverse=True)

            print("Alright, once the votes are read, the decision is final. Person with the most votes will be asked to leave the General Meeting area immediately. I'll read the votes.")
        print("First vote...")
        wait(1)
        # Dramatic vote reading
        currentMax = 1
        if safeViaIdol:
            for player in safeViaIdol:
                if votesRemaining[nominated.index(player)]:
                    for x in range(votesRemaining[nominated.index(player)]):
                        print(f"{player.name}. Does not count.")
                        votesRemaining[nominated.index(player)] -= 1
                        wait(1)
        while (max(votesRemaining) > 0):
            for x in range(len(votesRemaining)):
                if votesRemaining[x]:
                    print(f"{nominated[x].name}. That's {currentMax} vote{'' if currentMax == 1 else 's'} {nominated[x].name}.")
                    votesRemaining[x] -= 1
                    wait(1)
            currentMax += 1
            if sum(votesRemaining) == 1:
                print("One vote left.")
                wait(1)
                break


        # Guardian Angel Play (can be played after votes are read but NOT after a tie, meaning allies have certainty of outcome)
        for player in originalVotingPool:
            if ("Guardian Angel" in player.idols and tie_count == 0):
                # Player Criteria: must be themselves, allied, and must not idol out another ally or themselves
                inDanger = nominated[votes.index(decision[0])]
                nextInDanger = nominated[votes.index(decision[1])]

                if (inDanger not in safeViaIdol) and (inDanger == player or (player.faction != "Unaffiliated" and inDanger.faction == player.faction and nextInDanger.faction != player.faction and nextInDanger != player)):
                    print(f"{Fore.GREEN}{player.name} plays their Guardian Angel for {inDanger.name}.{Style.RESET_ALL}")
                    player.notoriety += 5
                    # Add saved player to the list of the immune contestants to prevent them from being involved in rock draws
                    safeViaIdol.append(inDanger)
                    nullifiedcount.append(f"{decision[0]}*")
                    votes[nominated.index(inDanger)] = -2

                    # Remove the player's idol and reset the votes
                    player.idols.remove("Guardian Angel")
                    decision = votes.copy()
                    decision.sort(reverse=True)

        n = next((i for i, x in enumerate(decision) if x != decision[0]), len(decision)) # see how many people r tied
        # If the votes don't tie, continue as normal
        if n == 1:
            eliminated = nominated[votes.index(decision[0])]
            match tie_count:
                case 0:
                    votecount = decision.copy()
                case 1:
                    revotecount = decision.copy()
            break
        elif n > 1: # If they do, re-vote - tied people are removed from the voting pool and are the only choices available to vote for
            tie_count += 1
            nominatedCopy = nominated.copy()
            nominated.clear()
            if tie_count == 1:
                votecount = decision.copy()
                print(f"{Fore.RED}The votes tied. We will have a re-vote: the tied players will not be able to vote, but the remaining voters will only be allowed to vote for one of the tied players.{Style.RESET_ALL}")
                for i in range(n):
                    tietiedPerson = nominatedCopy[votes.index(decision[i])]
                    nominated.append(tietiedPerson)
                    votingPool.remove(tietiedPerson)
                    votes[votes.index(decision[i])] = -1
            else: # Since votes tied twice, players go to rocks - players immune but in the voting pool are spared, along with tied players
                revotecount = decision.copy()
                print(f"{Fore.RED}The votes are deadlocked. We will now go to rocks - whoever draws the white rock is eliminated.{Style.RESET_ALL}")
                rockDrawers = votingPool.copy()
                for voter in votingPool:
                    if ((voter in originalVotingPool) and (voter not in originalNominated)) or (voter in safeViaIdol):
                        rockDrawers.remove(voter)
                if not rockDrawers: # All Players Immune due to two idols being played, causing a deadlock
                    print(f"{Fore.RED}Since there are no eligible players to vote for, all tied players' immunities will be nullified.{Style.RESET_ALL}")
                    # If a player used an idol or won individual immunity, they shall be spared
                    rockDrawers = originalNominated.copy()
                    for player in safeViaIdol:
                        rockDrawers.remove(player)
                    if not rockDrawers: # Special case where all of the remaining eligible players played idols (Almost Advantagegeddon), therefore no one can be voted for even with nullified tie immunity
                        print(f"{Fore.RED}There are still no eligible players to vote for. All idols will be nullified.{Style.RESET_ALL}")
                        rockDrawers = originalNominated.copy()
                        eliminated = random.choice(rockDrawers)
                    else:
                        eliminated = random.choice(rockDrawers)
                else:
                    eliminated = random.choice(rockDrawers)

    return eliminated, printVoteNotation(votecount, revotecount, nullifiedcount)
