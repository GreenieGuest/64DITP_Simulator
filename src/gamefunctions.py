import random
from colorama import Fore, Style

import os
from pathlib import Path

file = Path(__file__)
parent = file.parent
os.chdir(parent)

from utils import physScope, stratScope, socScope, notorietyScope, randomScope, wait, printVoteNotation

def gameEvents(team, players):
    for playerA in team:
        statusTypes = ["formAlliance", "disbandAlliance", "inviteIntoAlliance", "fractureAlliance", "manageNotoriety", "idolHunt"]
        status = random.choice(statusTypes)

        match status: # Players can only do one game move per free time event realistically (they get plenty of opportunities)
            case "formAlliance":
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
            case "disbandAlliance":
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
            case "inviteIntoAlliance":
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
            case "fractureAlliance":
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
            case "manageNotoriety":
                dynamics = socScope(playerA)
                if dynamics > 3 and playerA.notoriety > 50:
                    playerA.notoriety -= (dynamics - 3)
                    print(f"{playerA.name} lowers their threat level at camp.")
                elif dynamics == 1:
                    playerA.notoriety += 1
                    print(f"{playerA.name}'s name is discussed at camp as a potential target.")
                if playerA.notoriety < 0:
                    playerA.notoriety = 0
            case "idolHunt":
                # Find Idol
                idolHunt = randomScope(playerA)
                if idolHunt > 60 and physScope(playerA) > 2:
                    print(f"{playerA.name} finds a Savior.")
                    playerA.idols.append("Savior")
                elif idolHunt == 59 and physScope(playerA):
                    print(f"{playerA.name} finds a Guardian Angel.")
                    playerA.idols.append("Guardian Angel")
    print(" ")

def schoolyardPick(playerPool, teams, teamColors):
    teamCaptains = [None, None, None, None] # Purely cosmetic
    captainPreference = [None, None, None, None]

    print(f"{Fore.GREEN}[[DAY ONE SCHOOLYARD PICK]]{Style.RESET_ALL}")
    teamId = 0

    for x in range(4):
        teamCaptain = random.choice(playerPool)
        teams[teamId].append(teamCaptain)
        teamCaptain.color1 = teamColors[teamId]
        teamCaptains[teamId] = teamCaptain
        playerPool.remove(teamCaptain)
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
        if teamId > 3:
            teamId = 0
        wait(.5)

def elimination(originalNominated, originalVotingPool):
    # Each player in votingPool will vote for one player in nominated
    # Their decision is mostly based on notoriety but can be affected by factors such as alliance and social
    tie_count = 0
    nominated = originalNominated.copy()
    votingPool = originalVotingPool.copy()
    safeViaIdol = []

    # Vote Notation
    votecount = []
    revotecount = []
    nullifiedcount = []

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
                if stratScope(player) > 3 and stratScope(voter) > 3: # Fear of idol play
                    weight[i] -= 5

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

        # Idol Plays (only doable before revote)
        # Savior Play (can be played before votes are read - requires strategic scope)
        for player in originalVotingPool:
            if ("Savior" in player.idols and tie_count == 0):
                # Player Criteria: must be themselves, allied, and must not idol out another ally or themselves
                threatIndex = nominated.copy()
                threatIndex.sort(reverse=True, key=notorietyScope) # wrong readings happen for savior plays since votes are unknown at this point

                biggestThreat = nominated[nominated.index(threatIndex[0])]
                secondThreat = nominated[votes.index(decision[1])]

                if (biggestThreat not in safeViaIdol) and (biggestThreat == player or (player.faction != "Unaffiliated" and biggestThreat.faction == player.faction and secondThreat.faction != player.faction and secondThreat != player)):
                    print(f"{Fore.GREEN}{player.name} plays their Savior for {biggestThreat.name}.{Style.RESET_ALL}")
                    player.notoriety += 5
                    # Add saved player to the list of the immune contestants to prevent them from being involved in rock draws
                    safeViaIdol.append(biggestThreat)

                    nullifiedcount.append(f"{votes[nominated.index(biggestThreat)]}*")
                    votes[nominated.index(biggestThreat)] = -2

                    # Remove the player's idol and reset the votes
                    player.idols.remove("Savior")
                    decision = votes.copy()
                    decision.sort(reverse=True)

        # Guardian Angel Play (can be played after votes are read but NOT after a tie, meaning allies have certainty of outcome)
        for player in originalVotingPool:
            if ("Guardian Angel" in player.idols and tie_count == 0):
                # Player Criteria: must be themselves, allied, and must not idol out another ally or themselves
                inDanger = nominated[votes.index(decision[0])]
                nextInDanger = nominated[votes.index(decision[1])]

                if (inDanger not in safeViaIdol) and (inDanger == player or (player.faction != "Unaffiliated" and inDanger.faction == player.faction and nextInDanger.faction != player.faction and nextInDanger != player)):
                    print(f"{Fore.GREEN}{player.name} plays their Guardian Angel for {inDanger.name}.{Style.RESET_ALL}")
                    player.notoriety += 10
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
                if not rockDrawers: # All Players Immune due to two idols being played, causing a deadlo0ck
                    print(f"{Fore.RED}Since there are no eligible players to vote for, all tied players' immunities will be nullified.{Style.RESET_ALL}")
                    # If a player used an idol or won individual immunity, they shall be spared
                    rockDrawers = originalNominated.copy()
                    for player in safeViaIdol:
                        rockDrawers.remove(player)
                    eliminated = random.choice(rockDrawers)
                else:
                    eliminated = random.choice(rockDrawers)
    return eliminated, printVoteNotation(votecount, revotecount, nullifiedcount)