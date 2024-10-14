import json
import os
import random
import mysql.connector
from mysql.connector import Error

# Save special utility/formatting strings
bold_char = '\033[1m'
end_char = '\033[0m'
underscores = "--------------------------------------------------"  # 50 underscores
tab_spacing = "\t\t\t\t"


class Trainer:

    def __init__(self, name, battles_won = 0, pokemon = None):

        self.name = name
        self.battles_won = battles_won
        if pokemon != None:
            self.pokemon = pokemon

    def setPokemon(pokemon):
        self.pokemon = pokemon

    def battleWin(self):
        self.battles_won += 1


class Pokemon:

    def __init__(self, name, cry, stats):

        self.name = name
        self.cry = cry
        self.maxHealth = 0
        self.current_HP = 0
        self.attack = 0
        self.defense = 0
        self.speed = 0 

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
        if self.current_HP <= 0:
            self.current_HP = 0

        return value
    
    


def beginSequence():

    save_option = input("Would you like to load a previous save?\n")
    if save_option.lower() == "yes":
        with open("./Project 0/playerSave1.json", 'r') as file:
                data = json.load(file)
        pokemon = Pokemon(data['pokemon']['name'], data['pokemon']['cry'], data['pokemon']['stats'])
        player = Trainer(data['name'], data['battles_won'], pokemon)
        
    else:
        # Basic start

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
            elif pokemon_choice.lower() == "save1":
                with open("./Project 0/playerSave1.json", 'r') as file:
                    data = json.load(file)
                    loop = False
                pass
            else:
                print("Sorry, I didn't catch that.")
                pokemon_choice = input("Would you like Squirtle, Charmander, or Bulbasaur?\n")
                loop = True

        starter = Pokemon(data['name'], data['cry'], data['stats'])
        player = Trainer(player_name, 0, starter)

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

        battle_result = beginFirstBattle(player, rival_pokemon)

        # Pokemon strength increase (level up)
        # IF VICTORIOUS, gain exp
        if battle_result == 1:
            experienceGain(player.pokemon)
            player.battleWin()

            # Opportunity to save
            saveOpportunity(player)

            response = input("Continue?\n")
            if response.lower() == "no":
                return
        else:
            return


    connection = initializeDatabase()

    endlessBattleLoop(player, connection)

    if connection.is_connected():
        connection.close()
        print("Connection closed.")


def initializeDatabase():

    host = 'localhost'
    user = 'root'
    password = '1q2w3e4r'
    db_name = 'pokemon'

    conn = create_connection(host, user, password, db_name)
    create_database(conn, db_name)
    
    query = f"CREATE DATABASE IF NOT EXISTS {db_name};"
    execute_query(conn, query)
    query = """ CREATE TABLE IF NOT EXISTS pokemon 
        (dex_number INT PRIMARY KEY, 
        evolution_stage INT,
        name VARCHAR(255) NOT NULL, 
        max_hp INT, 
        attack INT, 
        defense INT, 
        speed INT); """

    execute_query(conn, query)

    insert_pokemon(conn, 1, 1, 'Bulbasaur', 60, 35, 35, 30)
    insert_pokemon(conn, 2, 2, 'Ivysaur', 80, 55, 55, 50)
    insert_pokemon(conn, 3, 3, 'Venusaur', 100, 75, 75, 70)
    insert_pokemon(conn, 4, 1, 'Charmander', 45, 45, 30, 45)
    insert_pokemon(conn, 7, 1, 'Squirtle', 50, 35, 45, 35)
    insert_pokemon(conn, 19, 1, 'Rattata', 30, 40, 30, 50)
    insert_pokemon(conn, 21, 1, 'Spearow', 25, 45, 20, 55)
    insert_pokemon(conn, 25, 1, 'Pikachu', 45, 50, 35, 50)
    insert_pokemon(conn, 37, 1, 'Vulpix', 40, 45, 30, 45)
    insert_pokemon(conn, 39, 1, 'Jigglypuff', 55, 30, 40, 35)
    insert_pokemon(conn, 52, 1, 'Meowth', 35, 50, 30, 45)
    insert_pokemon(conn, 92, 1, 'Gastly', 20, 55, 15, 45)
    insert_pokemon(conn, 93, 2, 'Haunter', 40, 75, 35, 65)
    insert_pokemon(conn, 94, 3, 'Gengar', 60, 95, 55, 85)
    insert_pokemon(conn, 129, 1, 'Magikarp', 10, 10, 10, 10)
    insert_pokemon(conn, 130, 2, 'Gyarados', 75, 75, 60, 75)
    insert_pokemon(conn, 78, 2, 'Rapidash', 60, 50, 40, 70)
    insert_pokemon(conn, 82, 2, 'Magneton', 80, 45, 90, 15)
    insert_pokemon(conn, 149, 3, 'Dragonite', 100, 100, 80, 90)
    insert_pokemon(conn, 65, 3, 'Alakazam', 75, 95, 50, 80)
    insert_pokemon(conn, 31, 3, 'Nidoqueen', 90, 70, 90, 60)
    insert_pokemon(conn, 34, 3, 'Nidoking', 80, 80, 70, 70)
    insert_pokemon(conn, 59, 2, 'Arcanine', 70, 85, 60, 85)
    insert_pokemon(conn, 8, 2, 'Wartortle', 60, 50, 60, 40)
    insert_pokemon(conn, 9, 3, 'Blastoise', 80, 80, 80, 30)
    insert_pokemon(conn, 6, 3, 'Charizard', 65, 90, 60, 90)
    

    return conn


def insert_pokemon(conn, dex_number, evo_stage, name, max_hp, attack, defense, speed):

    query = """
    INSERT IGNORE INTO pokemon (dex_number, evolution_stage, name, max_hp, attack, defense, speed)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    data = (dex_number, evo_stage, name, max_hp, attack, defense, speed)
    execute_query(conn, query, data)


def endlessBattleLoop(player, connection):

    player_name = player.name
    player_pokemon = player.pokemon

    # Load opponent
    stage = 1
    if player.battles_won >= 5:
        stage = 2
    elif player.battles_won >= 10:
        stage = 3

    query = """ 
    SELECT * FROM pokemon 
    WHERE evolution_stage = """ + str(stage) + """
    ORDER BY RAND()
    LIMIT 1;
    """
    retrieved = read_data(connection, query)[0]

    # Increase opponent power per battles_won
    exp_battle_multiplier = 5
    increase = player.battles_won * exp_battle_multiplier

    # TODO what to do with cry?
    cry = retrieved[1]

    opponent_pokemon = Pokemon(retrieved[2], cry, ["Health " + str(retrieved[3]+increase),
                                                "Attack " + str(retrieved[4]+increase),
                                                "Defense " + str(retrieved[5]+increase),
                                                "Speed " + str(retrieved[6]+increase)])

    # Battle
    battle_result = battleSequence(player, opponent_pokemon)

    # Experience gain
    if battle_result == 1:
        experienceGain(player.pokemon)
        player.battleWin()

        # Save
        saveOpportunity(player)

        # Continue/Exit
        choice = input("Continue?\n")
        if choice.lower() == 'yes':
            endlessBattleLoop(player, connection)
        else:
            print("Terminating program.")
            pass
    


def create_connection(host_name, user_name, user_password, db_name):

    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name, user=user_name, 
            password=user_password
        )
        print("Connection to database successful")

    except Error as e:
        print("ERROR: " + e)

    return connection

def create_database(connection, db_name):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        print(f"Database '{db_name}' created or already exists")
        cursor.execute(f"USE {db_name};")
    except Error as e:
        print(f"ERROR: '{e}'")

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        #print("Query executed successfully")
    except Error as e:
        print(f"ERROR: '{e}'")


def read_data(connection, query):

    cursor = connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    return data


def experienceGain(pokemon):

    print("\nYour " + pokemon.name + " has gotten so much stronger! Which stat will " + pokemon.name + " focus on now?\n")
    stat_choice = input(bold_char + "Health\t\tAttack\t\tDefense\t\tSpeed\n" + end_char)
    print("\n\n")

    stat_choice.strip().lower()

    if stat_choice == 'health':
        pokemon.changeMaxHealth(5)
    elif stat_choice == 'attack':
        pokemon.changeAttack(5)
    elif stat_choice == 'defense':
        pokemon.changeDefense(5)
    elif stat_choice == 'speed':
        pokemon.changeSpeed(5)
    else:
        print("\nLets try that again.")
        experienceGain(pokemon)


def saveOpportunity(player):

    save = input("Would you like to save your progress? This will overwrite previous saves.\n")
    print("\n\n")
    save.strip().lower()

    if save == 'yes' or save == 'y':
        # gather data and save
        
        pokemonToSave = {"name":player.pokemon.name, "cry":player.pokemon.cry, 
                "stats":["Health " + str(player.pokemon.maxHealth), "Attack " + str(player.pokemon.attack), 
                "Defense " + str(player.pokemon.defense), "Speed " + str(player.pokemon.speed)]}
        trainerToSave = {"name":player.name, "battles_won":player.battles_won, "pokemon":pokemonToSave}

        file_name = "Project 0/playerSave1.json"
        with open(file_name, 'w') as json_file:
            json.dump(trainerToSave, json_file, indent=4)

    elif save == 'no' or save == 'n':
        # do not save
        pass
    else:
        saveOpportunity(player)


def battleSequence(player, rival_pokemon):

    damage_multiplier = -0.35
    counter_multiplier = 2
    rest_multiplier = 1.5
    recover_percentage = 0.2

    # Make sure both Pokemon have full HP before battle
    rival_pokemon.current_HP = rival_pokemon.maxHealth
    player.pokemon.current_HP = player.pokemon.maxHealth

    # Repeating loop per turn    
    while player.pokemon.current_HP > 0 and rival_pokemon.current_HP > 0:

        # TODO use colored underscores to show HP? 

        print("\n" + underscores)   
        print(f"Enemy {rival_pokemon.name}" + tab_spacing + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
        print(underscores)
        print(f"{player.pokemon.name}" + tab_spacing + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
        print(underscores)

        action = input("\nWhat will you do?\n\n" + bold_char + "Attack\t\tCounter\t\tRest\n\n" + '\033[0m')
        print("\n\n")

        if action.lower() == "exit":
            exit()

        # Attack does damage. Highest speed moves first
        # Counter does damage only if attacked. 2x of what was recieved. Always goes first.
        # Rest restores 20% HP. Vulnerable to attacks while resting

        enemy_options = ["attack", "attack", "attack", "counter", "counter", "rest"]
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

                elif action.lower() == 'attack':
                    # Both take damage 
                    dmg = player.pokemon.changeCurrentHP(damage_multiplier * (rival_pokemon.attack / player.pokemon.defense) * rival_pokemon.attack)
                    print(rival_pokemon.name + " attacked " + player.pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")
                    dmg = rival_pokemon.changeCurrentHP(damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print(player.pokemon.name + " attacked " + rival_pokemon.name + " for " + str(-1*round(dmg)) + " damage!\n")

            elif enemy_action == 'counter':         # Enemy attempts to counter
                if action.lower() == 'counter':   
                    # Nothing happens
                    print(rival_pokemon.name+ " tried to counter! " + player.pokemon.name + " also tried to counterattack! Nothing happened.")

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
                    print(rival_pokemon.name + " backs off out of fear!\n")
                    rival_pokemon.changeCurrentHP(recover_percentage * rival_pokemon.maxHealth)
                    dmg = rival_pokemon.changeCurrentHP(rest_multiplier * damage_multiplier * (player.pokemon.attack / rival_pokemon.defense) * player.pokemon.attack)
                    print("But " + player.pokemon.name + " isn't letting up! " + rival_pokemon.name + " takes a considerable " + str(-1*round(dmg)) + " damage!\n")


    print("Battle completed. Final Results: ")
    print("\n" + underscores)
    print(f"Enemy {rival_pokemon.name}" + tab_spacing + format(rival_pokemon.current_HP/rival_pokemon.maxHealth, ".1%"))
    print(underscores)
    print(f"{player.pokemon.name}" + tab_spacing + format(player.pokemon.current_HP/player.pokemon.maxHealth, ".1%"))
    print(underscores + "\n\n")

    if player.pokemon.current_HP > 0 and rival_pokemon.current_HP <= 0:
        # player wins, time to save and move on
        print(rival_pokemon.name + " has been knocked out! " + player.name + " is victorious! \n")
        return 1              
    elif player.pokemon.current_HP <= 0 and rival_pokemon.current_HP > 0:
        # enemy wins. restart
        print(player.pokemon.name + " has been knocked out! " + player.name + " has been defeated!\n")
        return -1
    else:
        # Both have fainted. It's a draw
        print("Both " + player.pokemon.name + " and " + rival_pokemon.name + " have both collapsed! Neither one can continue. This battle is a draw!\n")
        return 0

    
    


def beginFirstBattle(player, rival_pokemon):

    starter_name = player.pokemon.name
    player_name = player.name

    print(bold_char + "\n...\n\nBANG!\n" + end_char + "\nYour rival, Gary, has burst into the room!")
    print(f"{player_name}! You're going down! " + rival_pokemon.name + " will make sure of it! ... " + rival_pokemon.cry + "\n")
    print(f"... {starter_name}, I choose you!" + "\n" + player.pokemon.cry)

    return battleSequence(player, rival_pokemon)



beginSequence()




