
"""
Requirements:

- Read data from file
- Write data to file
- Command line inputs
- Display data in some way
- OOP (classes)

Idea:
Program starts. Player is prompted to choose a starter pokemon. Before battles, player can look 
at their pokemon's information. Player battles an enemy trainer. Upon victory, player can either
teach their pokemon a new move, evolve, or swap pokemon. Player is allowed to save after battles.
3 total battles of increasing difficulty. If player wins, they can choose for their pokemon to
be put back at the beginning as a starter for future runs. 

OOP part: 

- Trainer Class
    - has Pokemon
    - has Name

- Rocket Grunt extends Trainer
    - has catchphrase
    - has defeat quote

- Pokemon class
    - has Moves
    - has Cry (entering battle and fainting)
    - has Attack, Defense, Speed

Important Aspects:

- method to display a pokemon's information
- method to save a pokemon 
- method to load a pokemon
- method loop to handle battling
"""

import json
import os
import random

class Trainer:
    def __init__(self, name, pokemon = None):
        self.name = name
        self.battles_won = 0
        if pokemon != None:
            self.pokemon = pokemon

    def setPokemon(pokemon):
        self.pokemon = pokemon


class Pokemon:
    def __init__(self, name, moves, cry, stats):

        self.name = name
        self.moves = []
        self.cry = cry
        self.maxHealth = 0
        self.current_HP = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0 
        self.battles_won = 0

        for move in moves:
            moveName = move.split()[0]
            moveDamage = move.split()[1]
            self.moves.append(Move(moveName, moveDamage))

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


class Move:
    def __init__(self, name, dmg):
        self.name = name
        self.dmg = dmg





def beginSequence():

    player_name = input("What's your name?\n")
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

    starter = Pokemon(data['name'], data['moves'], data['cry'], data['stats'])
    player = Trainer(player_name, starter)

    loop = True
    while loop:
        response = input("\nAre you ready for your first battle?\n")
        if response.lower() == "yes":
            loop = False
        else:
            print("Quickly! Prepare yourself!\n")

    beginFirstBattle(player)

    # Pokemon strength increase (level up)
    # Opportunity to save
    # Next battle

def battleSequence(player, rival_pokemon):

    bold_char = '\033[1m'
    end_char = '\033[0m'

    damage_multiplier = -0.35
    counter_multiplier = 2
    rest_multiplier = 1.5

    # Make sure both Pokemon have full HP
    rival_pokemon.current_HP = rival_pokemon.maxHealth
    player.pokemon.current_HP = player.pokemon.maxHealth


    # Repeating loop per turn    
    while player.pokemon.current_HP > 0 and rival_pokemon.current_HP > 0:

        # use colored underscores to show HP? 
        print("\n----------------------------------------")   # 40 underscores
        print(f"Enemy {rival_pokemon.name}" + "\t\t\t" + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
        print("----------------------------------------")
        print(f"{player.pokemon.name}" + "\t\t\t" + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
        print("----------------------------------------")

        action = input("\nWhat will you do?\n\n" + '\033[1m' + "Attack\t\tCounter\t\tRest\n\n" + '\033[0m')
        print("\n")

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
                    
                else:              # Enemy rests
                    # Enemy restores HP, ally does nothing
                    print(rival_pokemon.name + " takes a brief respite! But " + player.pokemon.name + " tried to counterattack!")
                    rival_pokemon.changeCurrentHP(0.2 * rival_pokemon.maxHealth)
                
            elif action.lower() == 'rest':
                # restore HP
                if enemy_action == 'attack':
                    # Restore ally HP then ally takes boosted damage
                    print(player.pokemon.name + " momentarily lowers its guard to recover!\n")
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    dmg = player.pokemon.changeCurrentHP(rest_multiplier * damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " takes the opportunity to deal a massive " + str(-1*round(dmg)) + " damage!\n")
                elif enemy_action == 'counter':
                    # Restore ally HP, enemy does nothing
                    print(player.pokemon.name + " keeps its distance! But " + rival_pokemon.name + " tried to counter!")
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                else:
                    # Both ally and enemy restore HP
                    print("Both Pokemon are prowling around, sizing each other up.")
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    rival_pokemon.changeCurrentHP(0.2 * rival_pokemon.maxHealth)
                
            # Ally attacks first
            else:
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
                else:
                    # Ally attacks, enemy restores HP
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    print(rival_pokemon.name + " briefly lowers its guard to recover!\n")
                    rival_pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    
        # Enemy pokemon faster
        else:       
            # Enemy attack
            if enemy_action == 'attack':
                if action.lower() == 'counter':   
                    # Enemy deals damage, then takes bonus counter damage
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = rival_pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")

                elif action == 'rest': 
                    # Enemy attacks, player rests
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    print(player.pokemon.name + " backs off to catch its breath.\n")
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    
                else:
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
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    
                else:
                    # Ally attacks, enemy counters
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = player.pokemon.changeCurrentHP(counter_multiplier * damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " retaliates for " + str(-1*round(dmg)) + " damage!\n")
                    
            else:
                # Enemy rests
                if action.lower() == 'counter':   
                    # Enemy restores HP
                    print(rival_pokemon.name + " keeps its distance! But " + player.pokemon.name + " tried to counter!")
                    rival_pokemon.changeCurrentHP(0.2 * rival_pokemon.maxHealth)
                    
                elif action == 'rest': 
                    # Both restore HP
                    print("Both Pokemon are prowling around, sizing each other up. ")
                    player.pokemon.changeCurrentHP(0.2 * player.pokemon.maxHealth)
                    rival_pokemon.changeCurrentHP(0.2 * rival_pokemon.maxHealth)
                    
                else:
                    # Ally attacks, enemy takes bonus resting damage
                    print(rival_pokemon.name + " backs off to catch its breath.\n")
                    rival_pokemon.changeCurrentHP(0.2 * rival_pokemon.maxHealth)
                    dmg = rival_pokemon.changeCurrentHP(rest_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print("But " + player.pokemon.name + " isn't letting up! " + rival_pokemon.name + " takes a considerable " + str(-1*round(dmg)) + " damage!\n")
                    
                   

    print("Battle completed. Results: ")
    print("\n----------------------------------------")   # 40 underscores
    print(f"Enemy {rival_pokemon.name}" + "\t\t\t" + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
    print("----------------------------------------")
    print(f"{player.pokemon.name}" + "\t\t\t" + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
    print("----------------------------------------")
    

def beginFirstBattle(player):

    bold_char = '\033[1m'
    end_char = '\033[0m'
    starter_name = player.pokemon.name
    player_name = player.name

    # load rival pokemon based on starter choice
    if starter_name.lower() == "squirtle":
        with open("./Project 0/bulbasaurBase.json", 'r') as file:
                data = json.load(file)
    elif starter_name.lower() == "charmander":
        with open("./Project 0/squirtleBase.json", 'r') as file:
                data = json.load(file)
    elif starter_name.lower() == "bulbasaur":
        with open("./Project 0/charmanderBase.json", 'r') as file:
                data = json.load(file)

    rival_pokemon = Pokemon(data['name'], data['moves'], data['cry'], data['stats'])
    # increase enemy stats per battle that the player has won (can be saved)
    #rival_pokemon.changeMaxHealth()

    print(bold_char + "\n...\n\nBANG!\n" + end_char + "\nYour rival, Gary, has burst into the room!")
    print(f"{player_name}! You're going down! " + rival_pokemon.name + " will make sure of it! ... " + rival_pokemon.cry + "\n")
    print(f"... {starter_name}, I choose you!" + "\n" + player.pokemon.cry)

    battleSequence(player, rival_pokemon)



beginSequence()



