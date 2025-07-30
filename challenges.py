import random
from colorama import Fore, Style

def test():
    print("Hello world!")

def teamChallenge(challenges, teams, teamNames, teamColors):
    challengeTypes = ["physical", "memory", "teamwork", "puzzle", "obby", "endurance", "trivia", "elimination", "combination", "luck"]
    challenge = random.choice(challengeTypes)
    challenges.append(challenge)

    teamSize = teams.copy()
    teamSize.sort(key=len)

    participating = len(teamSize[0]) # Sit out extra members to make things fair

    teamPoints = [0] * len(teams)
    loserId = None
    match challenge:
        case "physical":
            # Generic Challenge Format
            print("Challenge: Physical")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    for x in range(4):
                        playerRoll = random.randint(1, teams[team][player].physStat)
                        if playerRoll < 2:
                            teams[team][player].notoriety += 5
                        points += playerRoll
                teamPoints[team] = points
        case "mental":
            print("Challenge: Memory")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    for x in range(4):
                        playerRoll = random.randint(1, teams[team][player].stratStat)
                        if playerRoll < 2:
                            teams[team][player].notoriety += 5
                        points += playerRoll
                teamPoints[team] = points
        case "teamwork":
            print("Challenge: Teamwork")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    for x in range(4):
                        playerRoll = random.randint(1, teams[team][player].physStat)
                        if playerRoll < 2:
                            teams[team][player].notoriety += 5
                        points += playerRoll
                teamPoints[team] = points
        case "puzzle":
            print("Challenge: Puzzle")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll1 = random.randint(1, teams[team][player].socStat)
                    playerRoll2 = random.randint(1, teams[team][player].stratStat)
                    points += (playerRoll1 * playerRoll2)
                teamPoints[team] = points
        case "obby":
            print("Challenge: Obstacle Course")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll1 = random.randint(1, teams[team][player].physStat)
                    playerRoll2 = random.randint(1, teams[team][player].stratStat)
                    points += (playerRoll1 * playerRoll2)
                teamPoints[team] = points
        case "endurance":
            print("Challenge: Endurance")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll = 1
                    while playerRoll > 0:
                        playerRoll = random.randint(0, teams[team][player].physStat)
                        points += 1
                teamPoints[team] = points
        case "trivia":
            print("Challenge: Trivia")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll = 1
                    while playerRoll > 0:
                        playerRoll = random.randint(0, teams[team][player].stratStat)
                        points += 1
                teamPoints[team] = points
        case "elimination":
            print("Challenge: Elimination")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll = 1
                    while playerRoll > 0:
                        playerRoll = random.randint(0, teams[team][player].socStat)
                        points += 1
                teamPoints[team] = points
        case "combination":
            print("Challenge: Combination")
            for team in range(0, len(teams)):
                points = 0
                for player in range(participating):
                    playerRoll1 = random.randint(1, teams[team][player].physStat)
                    playerRoll2 = random.randint(1, teams[team][player].stratStat)
                    playerRoll3 = random.randint(1, teams[team][player].socStat)

                    points += (playerRoll1 + playerRoll2 + playerRoll3)
                teamPoints[team] = points
        case _:
            print("Challenge: Luck")
            for team in range(0, len(teams)):
                points = random.randint(1, 20)
                teamPoints[team] = points

    # Sort the points per team, then find the team with lowest points and declare them the loser.
    # Functionality for multiple losers later

    results = teamPoints.copy()
    results.sort()
    
    print(f"Results:")
    for x in range(len(teams)):
        print(f"{teamColors[x]}{teamNames[x]}{Style.RESET_ALL}: {teamPoints[x]}")
    loserId = teamPoints.index(results[0]) # First element in results is losing team
    return loserId

def challengeMerge(ultimateShowdown, showdownRound, challenges, notChosen):
    if ultimateShowdown == True:
        challenge = challenges[showdownRound]
    else:
        challengeTypes = ["physical", "memory", "obby", "endurance", "trivia", "elimination", "combination"]
        challenge = random.choice(challengeTypes)
        challenges.append(challenge)

    playerPoints = [0] * len(notChosen)
    match challenge:
        case "physical":
            # Generic Challenge Format
            print("Challenge: Physical")
            for player in range(len(notChosen)):
                for x in range(4):
                    playerRoll = random.randint(1, notChosen[player].physStat)
                    playerPoints[player] += playerRoll
        case "memory":
            print("Challenge: Memory")
            for player in range(len(notChosen)):
                for x in range(4):
                    playerRoll = random.randint(1, notChosen[player].stratStat)
                    playerPoints[player] += playerRoll
        case "teamwork":
            print("Challenge: Teamwork")
            for player in range(len(notChosen)):
                for x in range(4):
                    playerRoll = random.randint(1, notChosen[player].socStat)
                    playerPoints[player] += playerRoll
        case "puzzle":
            print("Challenge: Puzzle")
            for player in range(len(notChosen)):
                playerRoll1 = random.randint(1, notChosen[player].socStat)
                playerRoll2 = random.randint(1, notChosen[player].stratStat)
                points = (playerRoll1 * playerRoll2)
                playerPoints[player] = points
        case "obby":
            print("Challenge: Obstacle Course")
            for player in range(len(notChosen)):
                playerRoll1 = random.randint(1, notChosen[player].physStat)
                playerRoll2 = random.randint(1, notChosen[player].stratStat)
                points = (playerRoll1 * playerRoll2)
                playerPoints[player] = points
        case "endurance":
            print("Challenge: Endurance")
            for player in range(len(notChosen)):
                playerRoll = 1
                while playerRoll > 0:
                    playerRoll = random.randint(0, notChosen[player].physStat)
                    playerPoints[player] += 1
        case "trivia":
            print("Challenge: Trivia")
            for player in range(len(notChosen)):
                playerRoll = 1
                while playerRoll > 0:
                    playerRoll = random.randint(0, notChosen[player].stratStat)
                    playerPoints[player] += 1
        case "elimination":
            print("Challenge: Elimination")
            for player in range(len(notChosen)):
                playerRoll = 1
                while playerRoll > 0:
                    playerRoll = random.randint(0, notChosen[player].socStat)
                    playerPoints[player] += 1
        case "combination":
            print("Challenge: Combination")
            for player in range(len(notChosen)):
                playerRoll1 = random.randint(1, notChosen[player].physStat)
                playerRoll2 = random.randint(1, notChosen[player].stratStat)
                playerRoll3 = random.randint(1, notChosen[player].socStat)
                points = (playerRoll1 + playerRoll2 + playerRoll3)
                playerPoints[player] = points
        case _:
            print("Challenge: Luck")
            for player in range(len(notChosen)):
                points = random.randint(1, 20)

                playerPoints[player] = points

    # Sort the points per player, returning a list of players from MOST POINTS to LEAST.

    results = playerPoints.copy()
    results.sort(reverse=True)
    
    print(f"Results:")
    for x in range(len(notChosen)):
        print(f"{notChosen[x].name}: {playerPoints[x]}")
    for x in range(len(results)):

        index = playerPoints.index(results[x])
        results[x] = index
        playerPoints[index] = 0 # Clears the player's index so that repeat values aren't used. This breaks the sim

    return results

