import random
from colorama import Fore, Style

def challenge(challenge, player):
    # Universal challenge modus
    earnedPoints = 0

    match challenge:
        case "Physical":
            # Generic Challenge Format
            for x in range(4):
                earnedPoints += random.randint(1, player.physStat)
        case "Mental":
            for x in range(4):
                earnedPoints += random.randint(1, player.stratStat)
        case "Teamwork":
            for x in range(4):
                earnedPoints += random.randint(1, player.socStat)
        case "Puzzle":
            playerRoll1 = random.randint(1, player.socStat)
            playerRoll2 = random.randint(1, player.stratStat)
            earnedPoints = (playerRoll1 * playerRoll2)
        case "Obstacle Course":
            playerRoll1 = random.randint(1, player.physStat)
            playerRoll2 = random.randint(1, player.stratStat)
            earnedPoints = (playerRoll1 * playerRoll2)
        case "Endurance":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.physStat)
                earnedPoints += 1
        case "Memory":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.stratStat)
                earnedPoints += 1
        case "Elimination":
            playerRoll = 1
            while playerRoll > 0:
                playerRoll = random.randint(0, player.socStat)
                earnedPoints += 1
        case "Combination":
            playerRoll1 = random.randint(1, player.physStat)
            playerRoll2 = random.randint(1, player.stratStat)
            playerRoll3 = random.randint(1, player.socStat)
            earnedPoints = (playerRoll1 + playerRoll2 + playerRoll3)
        case _:
            earnedPoints = random.randint(1, 20)
            
    return earnedPoints

def teamChallenge(challenges, teams, teamNames, teamColors):
    challengeTypes = ["Physical", "Mental", "Teamwork", "Puzzle", "Obstacle Course", "Endurance", "Trivia", "Elimination", "Combination", "Luck"]
    challengeName = random.choice(challengeTypes)
    challenges.append(challengeName)

    teamSize = teams.copy()
    teamSize.sort(key=len)

    participating = len(teamSize[0]) # Sit out extra members to make things fair

    teamPoints = [0] * len(teams)
    loserId = None
    print(f"Challenge: {challengeName}")
            
    for team in range(0, len(teams)):
        points = 0
        participants = random.sample(teams[team], participating) # Allows for random sitouts
        for player in participants:
            performance = challenge(challengeName, player)
            if performance < 2:
                print(f"{player.name} completely failed the challenge.")
                player.notoriety += 5
            points += performance
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
        challengeName = challenges[showdownRound]
    else:
        challengeTypes = ["Physical", "Mental", "Obstacle Course", "Endurance", "Memory", "Elimination", "Combination"]
        challengeName = random.choice(challengeTypes)
        challenges.append(challengeName)

    playerPoints = [0] * len(notChosen)
    print(f"Challenge: {challengeName}")

    for player in range(len(notChosen)):
        playerPoints[player] = challenge(challengeName, notChosen[player])

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

