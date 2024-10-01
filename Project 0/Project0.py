
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

# imports
import json
import os



class Trainer:
    def __init__(self, name, pokemon):
        self.name = name
        #self.pokemon = pokemon

    def setPokemon(pokemon):
        self.pokemon = pokemon

    # def __str__


class Pokemon:
    def __init__(self, name, moves, cry, stats):

        self.name = name
        self.moves = []
        self.cry = cry
        self.health = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0 

        for move in moves:
            moveName = move.split()[0]
            moveDamage = move.split()[1]
            self.moves.append(Move(moveName, moveDamage))

        for stat in stats:
            stat_type = stat.split()[0]
            value = stat.split()[1]
            if stat_type == "Attack":
                self.attack = value
            elif stat_type == "Defense":
                self.defense = value
            elif stat_type == "Speed":
                self.speed = value
            elif stat_type == "Health":
                self.health = value
            # error handling here TODO
    

    # def __str__




class Move:
    def __init__(self, name, dmg):
        self.name = name
        self.dmg = dmg





def beginSequence():

    #print("Current working directory:", os.getcwd())
    #print("Files in the current directory:", os.listdir('.'))

    player_name = input("What's your name?\n")
    print("Your Pokemon options are: Squirtle, Charmander, or Bulbasaur.\n")
    pokemon_choice = input("Choose wisely!\n")

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
    print(data['stats'])


    #player = Trainer(player_name, pokemon)







beginSequence()



