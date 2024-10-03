
import json
import os
import random


# Save special utility strings
bold_char = '\033[1m'
end_char = '\033[0m'
underscores = "--------------------------------------------------"  # 50 underscores
tab_spacing = "\t\t\t\t"

class Trainer:

    def __init__(self, name, pokemon = None):

        self.name = name
        self.battles_won = 0
        if pokemon != None:
            self.pokemon = pokemon

    def setPokemon(pokemon):
        self.pokemon = pokemon


class Pokemon:

    def __init__(self, name, cry, stats):

        self.name = name
        self.cry = cry
        self.maxHealth = 0
        self.current_HP = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0 
        #self.battles_won = 0

        for stat in stats:

            stat_type = stat.split()[0]
            value = stat.split()[1]

            if stat_type == "Attack":
                self.attack = int(value)
            elif stat_type == "Defense":
                self.defense = int(value)
            elif stat_type == "Speed":
                self.speed = int(value)
            elif stat_type == "Health":
                self.maxHealth = int(value)
                self.current_HP = int(value)
            # error handling here TODO

    def changeMaxHealth(self, value):
        self.maxHealth += value

    def changeAttack(self, value):
        self.attack += value

    def changeDefense(self, value):
        self.defense += value

    def changeSpeed(self, value):
        self.speed += value

    def changeCurrentHP(self, value):

        self.current_HP += value
        if self.current_HP > self.maxHealth:
            self.current_HP = self.maxHealth
        if self.current_HP < 0:
            self.current_HP = 0

        return value

    # def __str__



def beginSequence():


    player_name = input("What's your name?\n")
    player_name = player_name.strip().title()
    print("\nYour Pokemon options are: Squirtle, Charmander, or Bulbasaur.\n")

    pokemon_choice = input("Choose wisely!\n")
    pokemon_choice.strip().title()

    loop = True
    while loop:

        if pokemon_choice.lower() == "squirtle":
            with open("./Project 0/squirtleBase.json", 'r') as file:
                data = json.load(file)
                loop = False
        elif pokemon_choice.lower() == "charmander":
            with open("./Project 0/charmanderBase.json", 'r') as file:
                data = json.load(file)
                loop = False
        elif pokemon_choice.lower() == "bulbasaur":
            with open("./Project 0/bulbasaurBase.json", 'r') as file:
                data = json.load(file)
                loop = False
        else:
            print("Sorry, I didn't catch that.")
            pokemon_choice = input("Would you like Squirtle, Charmander, or Bulbasaur?\n")
            loop = True

    starter = Pokemon(data['name'], data['cry'], data['stats'])
    player = Trainer(player_name, starter)

    loop = True
    while loop:

        response = input("\nAre you ready for your first battle?\n")
        if response.lower() == "yes":
            loop = False
        else:
            print("Quickly! Prepare yourself!\n")

    # load rival pokemon based on starter choice
    if starter.name.lower() == "squirtle":
        with open("./Project 0/bulbasaurBase.json", 'r') as file:
                data = json.load(file)
    elif starter.name.lower() == "charmander":
        with open("./Project 0/squirtleBase.json", 'r') as file:
                data = json.load(file)
    elif starter.name.lower() == "bulbasaur":
        with open("./Project 0/charmanderBase.json", 'r') as file:
                data = json.load(file)

    rival_pokemon = Pokemon(data['name'], data['cry'], data['stats'])

    # increase enemy stats per battle that the player has won (can be saved)
    #rival_pokemon.changeMaxHealth()

    beginFirstBattle(player, rival_pokemon)

    # Pokemon strength increase (level up)
    # IF VICTORIOUS, gain exp
    experienceGain(player.pokemon)

    # Opportunity to save
    saveOpportunity(player)

    # TODO start next battle

def experienceGain(pokemon):

    print("Your " + pokemon.name + " has gotten so much stronger! Which stat will " + pokemon.name + " focus on now?\n")
    stat_choice = input(bold_char + "Health\t\tAttack\t\tDefense\t\tSpeed\n\n" + end_char)
    stat_choice.strip().lower()

    if stat_choice == 'health':
        pokemon.changeMaxHealth(5)
    elif stat_choice == 'attack':
        pokemon.changeAttack(5)
    elif stat_choice == 'defense':
        pokemon.changeDefense(5)
    elif stat_choice == 'speed':
        pokemon.changeSpeed(5)

    print("\n\n")


def saveOpportunity(player):

    save = input("Would you like to save your progress? This will overwrite previous saves.\n")
    save.strip().lower()

    if save == 'yes' or save == 'y':
        #save
        pass
    elif save == 'no' or save == 'n':
        # do not save
        pass
    else:
        saveOpportunity(player)


def battleSequence(player, rival_pokemon):

    damage_multiplier = -0.35
    counter_multiplier = 2
    rest_multiplier = 2
    recover_percentage = 0.2

    # Make sure both Pokemon have full HP before battle
    rival_pokemon.current_HP = rival_pokemon.maxHealth
    player.pokemon.current_HP = player.pokemon.maxHealth

    # Repeating loop per turn    
    while player.pokemon.current_HP > 0 and rival_pokemon.current_HP > 0:


        # use colored underscores to show HP? 

        print("\n" + underscores)   
        print(f"Enemy {rival_pokemon.name}" + tab_spacing + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
        print(underscores)
        print(f"{player.pokemon.name}" + tab_spacing + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
        print(underscores)

        action = input("\nWhat will you do?\n\n" + bold_char + "Attack\t\tCounter\t\tRest\n\n" + '\033[0m \n\n')

        if action.lower() == "exit":
            exit()

        # Attack does damage. Highest speed moves first
        # Counter does damage only if attacked. 2x of what was recieved. Always goes first.
        # Rest restores 20% HP. Vulnerable to attacks by 1.5x while resting

        # TODO enemy class has attribute of an action list

        enemy_options = ["attack", "counter", "rest"]
        enemy_action = random.choice(enemy_options)

        if player.pokemon.speed >= rival_pokemon.speed:
            if action.lower() == 'counter':     # Player attempts to counter
                if enemy_action == 'counter':   # Enemy counters
                    print(player.pokemon.name + " tried to counter! " + rival_pokemon.name + " responds with... a counter of its own! Nothing happened.")

                elif enemy_action == 'attack':  # Enemy attacks, player counters
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage, but " + player.pokemon.name + " was ready for it!\n")
                    dmg = rival_pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " retaliates for " + str(-1*round(dmg)) + " damage!\n")

                elif enemy_action == 'rest':             # Enemy rests
                    # Enemy restores HP, ally does nothing
                    print(rival_pokemon.name + " takes a brief respite! But " + player.pokemon.name + " tried to counterattack!")
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)

            elif action.lower() == 'rest':
                # restore HP
                if enemy_action == 'attack':
                    # Restore ally HP then ally takes boosted damage
                    print(player.pokemon.name + " momentarily lowers its guard to recover!\n")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)
                    dmg = player.pokemon.changeCurrentHP(rest_multiplier * damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " takes the opportunity to deal a massive " + str(-1*round(dmg)) + " damage!\n")

                elif enemy_action == 'counter':
                    # Restore ally HP, enemy does nothing
                    print(player.pokemon.name + " keeps its distance! But " + rival_pokemon.name + " tried to counter!")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)

                elif enemy_action == 'rest':  
                    # Both ally and enemy restore HP
                    print("Both Pokemon are prowling around, sizing each other up.")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)

            # Ally attacks first
            elif action == 'attack':
                if enemy_action == 'attack':    
                    # Both attack
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")

                elif enemy_action == 'counter':
                    # Ally does damage, enemy counters for bonus damage
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = player.pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " countered " + player.pokemon.name + "'s attack for " + str(-1*round(dmg)) + " damage!\n")

                elif enemy_action == 'rest':  
                    # Ally attacks, enemy restores HP
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    print(rival_pokemon.name + " takes a moment to recover some stamina!\n")
                    rival_pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)
                    
        # Enemy pokemon faster
        else:       
            # Enemy attack
            if enemy_action == 'attack':
                if action.lower() == 'counter':   
                    # Enemy deals damage, then takes bonus counter damage
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = rival_pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print("A brutal reversal by " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")

                elif action == 'rest': 
                    # Enemy attacks, player rests
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    print(player.pokemon.name + " backs off to catch its breath.\n")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)

                elif action.lower() == 'counter':
                    # Both take damage 
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")

            elif enemy_action == 'counter':         # Enemy attempts to counter
                if action.lower() == 'counter':   
                    # Nothing happens
                    print(rival_pokemon.name+ " tried to counter! " + player.pokemon.name + " responds with... a counter of its own! Nothing happened.")

                elif action == 'rest': 
                    # Player restores HP
                    print(player.pokemon.name + " keeps its distance! But " + rival_pokemon.name + " tried to counter!")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)

                elif action == 'attack':
                    # Ally attacks, enemy counters
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = player.pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " retaliates for " + str(-1*round(dmg)) + " damage!\n")
                    
            elif enemy_action == 'rest':
                # Enemy rests
                if action.lower() == 'counter':   
                    # Enemy restores HP
                    print(rival_pokemon.name + " keeps its distance! But " + player.pokemon.name + " tried to counter!")
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)

                elif action == 'rest': 
                    # Both restore HP
                    print("Both Pokemon are prowling around, sizing each other up. ")
                    player.pokemon.changeCurrentHP(recover_percentage * player.pokemon.maxHealth)
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)

                elif action == 'attack':
                    # Ally attacks, enemy takes bonus resting damage
                    print(rival_pokemon.name + " backs off to catch its breath.\n")
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)
                    dmg = rival_pokemon.changeCurrentHP(rest_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print("But " + player.pokemon.name + " isn't letting up! " + rival_pokemon.name + " takes a considerable " + str(-1*round(dmg)) + " damage!\n")

    if player.pokemon.current_HP > 0 and rival_pokemon.current_HP <= 0:
        # player wins, time to save and move on
        pass               
    elif player.pokemon.current_HP <= 0 and rival_pokemon.current_HP > 0:
        # enemy wins. restart
        pass
    else:
        # Both have fainted. It's a draw
        pass

    print("Battle completed. Results: ")
    print("\n" + underscores)
    print(f"Enemy {rival_pokemon.name}" + tab_spacing + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
    print(underscores)
    print(f"{player.pokemon.name}" + tab_spacing + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
    print(underscores)
    


def beginFirstBattle(player, rival_pokemon):

    starter_name = player.pokemon.name
    player_name = player.name

    print(bold_char + "\n...\n\nBANG!\n" + end_char + "\nYour rival, Gary, has burst into the room!")
    print(f"{player_name}! You're going down! " + rival_pokemon.name + " will make sure of it! ... " + rival_pokemon.cry + "\n")
    print(f"... {starter_name}, I choose you!" + "\n" + player.pokemon.cry)

    battleSequence(player, rival_pokemon)



beginSequence()




