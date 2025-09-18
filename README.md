# 64DITP
64DITP (Survivor-esque competition with 64 competitors) simulator. Inspired by Brantsteele.

Very crude. I made this out of boredom because I like doing these types of competitions. Beware!
# Configuration
Edit src/config.py to edit tribe names, tribe colors, game twists, etc.
You can decrease the cast size to your custom amount by changing the size of the list 'names'.

### Names only (randomly generated profiles):
Use a site (I prefer https://commaquote.azurewebsites.net) to format 64 names of your choice into string format. Then, replace the "names" list with your cast's names.
### Names with profiles:
To create your own pre-set profiles I recommend using excel or google sheets, exporting to CSV and putting it through a CSV to json converter (I personally use https://csvjson.com/csv2json).

Lastly if you want to add other aspects such as tweaking game phases, adding custom challenges, etc, have at it.

# Saving results
You can automatically set the simulation to run a certain amount of times by setting AUTORUN to true.
The simulation will automatically export placements data to a list after each finale.
After the autorunner is finished or the player exits, statistics data including average placement will also be exported.

<img width="574" height="768" alt="image" src="https://github.com/user-attachments/assets/465573e9-07bd-42b3-a7b7-fc950e8c4c32" />

<img width="1544" height="946" alt="image" src="https://github.com/user-attachments/assets/43a4c3ae-415b-49ab-8c53-03e670674e59" />
