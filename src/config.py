from colorama import Fore, Style
from time import sleep

# [[ CONFIGURATION ]] ----------------------------------------------------------------------------------
season_name = "64 Days in the Pit - The Ultimate Showdown"
# Player Names
names = ["2-D","Americaball","Atom","Big Rig","Billy Blockhead","Boat Crew","Boston Rob","Boxy","Captain Hammer","Carl Grimes","Cashy","Chad","ChrisPop","Death Man","Dog","Dr Horrible","Ellie Lander","Erika Faust","Four","Frederick","Gamer","Germanyball","Heathcliff","Hexbug","Homestar Runner","Horatio Caine","Hunter Moses","Isaac Creighton","Jack Dawson","Jackson","Joe","Joey","Josephine Mercier","King Lorenzo","Koda","Lauren","Lukey","Martin","Mitochondria","Mr Ben","Mr Wilson","Muscles","Nagito Komaeda","Nitro","OG","Pencil","Petra","Polandball","Roco","Ronny the Banana","Satan","Stunt Devil","Teresa Tayliss","Terezi Pyrope","The Miser","Todd","Tom","Tom Brady","Tommy Walter","Transparent Red","Trogdor the Burninator","V2","Vriska Serket","Watch"]
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

firstSwapThreshold = 48 # Default: 48 out of 64
secondSwapThreshold = 32 # Default: 32 out of 64
mergeThreshold = 16 # Default: 16 out of 64
finalThreshold = 8 # Default: 8 out of 64

startingTeams = 3 # Default: 4 // If you're adding more than 4, you're gonna have to make new names and colors for them
mergeatory = False # Default: True

FASTFORWARD = False

PRESET_PROFILES = True

PROFILE_FILE_PATH = 'profiles.json'
