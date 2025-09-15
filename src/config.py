from colorama import Fore, Style
from time import sleep

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
season_name = "Winners at War"
# Player Names
names = ["2-D"]
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
mergeName = "Merge"
q4Colors = [Fore.GREEN, Fore.RED]
mergeColor = Fore.YELLOW
# Jury Name
juryName = "Jury"
# Invincibility Name
immunityName = "Individual Immunity"

firstSwapThreshold = 14 # Default: 48 out of 64
secondSwapThreshold = 13 # Default: 32 out of 64
mergeThreshold = 12 # Default: 16 out of 64
finalThreshold = 10 # Default: 8 out of 64

startingTeams = 3 # Default: 4 // If you're adding more than 4, you're gonna have to make new names and colors for them
mergeatory = False # Default: True

FASTFORWARD = False

PRESET_PROFILES = True
PROFILE_FILE_PATH = 'profiles.json'