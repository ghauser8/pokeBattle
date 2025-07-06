import random

from pokemon import Pokemon, PokemonManager

class Player:
    def __init__(self, name, pokemon):
        self.name = name
        self.pokemon = pokemon
        self.active_pokemon = pokemon[0]

    def has_alive_pokemon(self):
        return any(pokemon.is_alive() for pokemon in self.pokemon)

    def swap_pokemon(self, index):
        if 0 <= index < len(self.pokemon) and self.pokemon[index].is_alive():
            self.active_pokemon = self.pokemon[index]
            return True
        return False

def display_status(player, computer):
    print("\n****************************")
    print("******** New Round! ********")
    print("****************************\n")
    print(f"\n{player.name}'s {player.active_pokemon.name}: {player.active_pokemon.hp}/{player.active_pokemon.max_hp} HP")
    print(f"Computer's {computer.active_pokemon.name}: {computer.active_pokemon.hp}/{computer.active_pokemon.max_hp} HP\n")

def player_turn(player, computer):
    print(f"{player.name}'s turn!")
    print(f"Active Pokemon: {player.active_pokemon.name}")
    print("Available actions:")
    print("1. Attack")
    print("2. Swap Pokemon")
    print("3. Forfeit")
    
    while True:
        choice = input("Choose an action (1-3): ").strip()
        if choice == "1":
            i = 1
            choice_map = {}
            for attack in player.active_pokemon.attacks:
                if i == 1:
                    print(f"Attacks: {i}. {attack} ({player.active_pokemon.attacks[attack]} dmg)")
                else:
                    print(f"         {i}. {attack} ({player.active_pokemon.attacks[attack]} dmg)")

                choice_map[i] = attack
                i += 1

            attack_choice = input(f"Choose attack (1-{i-1}): ").strip()

            if attack_choice in ["1", "2"]:
                damage = computer.active_pokemon.take_damage(player.active_pokemon.attacks[choice_map[int(attack_choice)]])
                print(f"{player.active_pokemon.name} used {choice_map[int(attack_choice)]} and dealt {damage} damage!")
                input("\t Enter to continue...\n")
                return True
            else:
                print("Invalid attack choice. Try again.")
        elif choice == "2":
            print("Available Pokemon:")
            for i, pokemon in enumerate(player.pokemon):
                status = "Alive" if pokemon.is_alive() else "Fainted"
                print(f"{i+1}. {pokemon.name} ({pokemon.hp}/{pokemon.max_hp} HP, {status})")
            swap_choice = input(f"Choose Pokemon to swap to (1-{len(player.pokemon)}, 0 to cancel): ").strip()
            if swap_choice == "0":
                continue
            try:
                index = int(swap_choice) - 1
                if player.swap_pokemon(index):
                    print(f"{player.name} swapped to {player.active_pokemon.name}!")
                    return True
                else:
                    print("Invalid choice or Pokemon is fainted. Try again.")
            except ValueError:
                print("Invalid input. Try again.")
        elif choice == "3":
            print(f"{player.name} forfeited the battle!")
            return False
        else:
            print("Invalid choice. Try again.")

def computer_turn(computer, player, difficulty=2):
    print(f"Computer's turn!")
    # Computer prioritizes attack if active pokemon is strong, else swaps or attacks randomly
    available_pokemon = [i for i, pokemon in enumerate(computer.pokemon) if pokemon.is_alive() and pokemon != computer.active_pokemon]
    if random.random() < 0.5 + 0.1 * difficulty or not available_pokemon:
        attack_choice = random.choice([i for i in range(len(computer.active_pokemon.attacks.keys()))])
        akey = list(computer.active_pokemon.attacks.keys())[attack_choice]
        damage = player.active_pokemon.take_damage(computer.active_pokemon.attacks[akey])
        print(f"{computer.active_pokemon.name} used {akey} and dealt {damage} damage!")
        input("\t Enter to continue...\n")

    else:  # Swap to a random alive pokemon
        swap_index = random.choice(available_pokemon)
        computer.swap_pokemon(swap_index)
        print(f"Computer swapped to {computer.active_pokemon.name}!")
        input("\t Enter to continue...\n")
    return True

def battle(settings = {}):
    # Load Pokemon
    manager = PokemonManager()
    if settings['pick_limit']:
        pick_limit = settings['pick_limit']

    
    # player and computer take turns picking pokemon from common list
    print("Welcome to Pokemon Battle!")
    print("Each Pokemon has two attacks and health points. Take turns to attack, swap, or forfeit.")
    print("First, take turns selecting your Pokemon. Player goes first!")
    input("\t Enter to continue...\n")
    unselected = {p.name: p for p in manager.pokemon}
    players_pokemon = []
    computer_pokemon = []
    choice_map = {}
    while len(players_pokemon) < pick_limit:
        # print out the remaining pokemon names to choose from
        print(f"Select your next Pokemon. You have {pick_limit - len(players_pokemon)} of {pick_limit} selections left:")
        choice_map = {}
        c = 1
        for p in unselected:
            print(f"  {c}. {p}\n")
            choice_map[str(c)] = p
            c += 1

        player_choice = input(f"Pick a Pokemon (1-{c-1}): ")
        players_pokemon.append(unselected[choice_map[player_choice]])
        player_pick = choice_map[player_choice]
        del unselected[choice_map[player_choice]]
        print(f"You picked {player_pick}!")

        # computer selects a pokemon
        choice_map = {
            i: p for i,p in enumerate(unselected.keys())
        }
        if len(unselected) - 1 > 0:
            computer_choice = random.randint(0,len(unselected)-1)
        else:
            computer_choice = 0
        computer_pokemon.append(unselected[choice_map[computer_choice]])
        computer_pick = choice_map[computer_choice]
        del unselected[choice_map[computer_choice]]
        print(f"Computer picked {computer_pick}!")
        input("\t Enter to continue...\n")
        
    player = Player("Player", players_pokemon)
    computer = Player("Computer", computer_pokemon)
    
    
    while player.has_alive_pokemon() and computer.has_alive_pokemon():
        display_status(player, computer)
        
        # Player's turn
        if not player_turn(player, computer):
            print("Computer wins!\n")
            print(ASCII_ART['computer_wins'])
            break
            
        if not computer.active_pokemon.is_alive():
            print(f"Computer's {computer.active_pokemon.name} fainted!")
            print(ASCII_ART['fainted'])
            input("\t Enter to continue...\n")
            alive_pokemon = [i for i, pokemon in enumerate(computer.pokemon) if pokemon.is_alive()]
            if alive_pokemon:
                computer.swap_pokemon(alive_pokemon[0])
                print(f"Computer sent out {computer.active_pokemon.name}!")
            else:
                print("Player wins!\n")
                print(ASCII_ART['player_wins'])
                break
                
        if not computer.has_alive_pokemon():
            print("Player wins!\n")
            print(ASCII_ART['player_wins'])
            break
            
        # Computer's turn
        if settings['difficulty']:
            computer_turn(computer, player, settings['difficulty'])
        else:
            computer_turn(computer, player)
        
        if not player.active_pokemon.is_alive():
            print(f"Player's {player.active_pokemon.name} fainted!")
            print(ASCII_ART['fainted'])
            input("\t Enter to continue...\n")
            alive_pokemon = [i for i, pokemon in enumerate(player.pokemon) if pokemon.is_alive()]
            if alive_pokemon:
                print("Available Pokemon:")
                for i, pokemon in enumerate(player.pokemon):
                    status = "Alive" if pokemon.is_alive() else "Fainted"
                    print(f"{i+1}. {pokemon.name} ({pokemon.hp}/{pokemon.max_hp} HP, {status})")
                while True:
                    swap_choice = input("Choose Pokemon to swap to (1-3): ").strip()
                    try:
                        index = int(swap_choice) - 1
                        if player.swap_pokemon(index):
                            print(f"{player.name} swapped to {player.active_pokemon.name}!")
                            break
                        else:
                            print("Invalid choice or Pokemon is fainted. Try again.")
                    except ValueError:
                        print("Invalid input. Try again.")
            else:
                print("Computer wins!\n")
                print(ASCII_ART['computer_wins'])
                break

def check_int_choice(choice, allowable_inputs: list) -> bool:

    try:
        choice = int(choice)
        if choice in allowable_inputs:
            return True
        return False
    except:
        return False

def settings_menu() -> dict:
    print("---- Settings ----")
    pick_limit = input("How many Pokemon should each player start with? (1-3) ")
    good_pick = check_int_choice(pick_limit, [i+1 for i in range(3)])
    while not good_pick:
        pick_limit = input("Try again. How many pokemon should each player start with? (1-3) ")
        good_pick = check_int_choice(pick_limit, [i+1 for i in range(3)])

    difficulty = input("How good should the computer be? (1-5, 1=easiest, 5=hardest) ")
    good_difficulty = check_int_choice(difficulty, [1,2,3,4,5])
    while not good_difficulty:
        difficulty = input("Try again. How good should the coputer be? (1-5) ")
        good_difficulty = check_int_choice(difficulty, [1,2,3,4,5])

    print('Settings successfully changed!\n')
    return {
        'pick_limit': int(pick_limit),
        'difficulty': int(difficulty)
    }


def main():
    ''' outer menu for seleting battle or manager or settings change '''
    manager = PokemonManager()
    settings = None
    print('\nWelcome to PokeBattle!')
    while True:
        print("\n+++++++++++++++++++++++++")
        print("+++++++ Main Menu +++++++")
        print("+++++++++++++++++++++++++\n")
        print('What would you like to do?')
        print('\t 1. Battle!')
        print('\t 2. Manage Pokemon')
        print('\t 3. Change settings')
        print('\t 4. Quit')

        menu_choice = input("Choose (1-4): ")
        good_choice = check_int_choice(menu_choice, [1,2,3,4])
        while not good_choice:
            menu_choice = input("That didn't make sense. Choose (1-4): ")
            good_choice = check_int_choice(menu_choice, [1,2,3,4])
        
        if not settings:
            settings = {'pick_limit': 2, 'difficulty': 3}
        match int(menu_choice):
            case 1:
                battle(settings)
            case 2:
                manager.run()
            case 3:
                settings = settings_menu()
            case 4:
                print('Goodbye!')
                return
    
ASCII_ART = {
    'player_wins': 
r"""
__/\\\________/\\\_____________________________                  
 _\///\\\____/\\\/______________________________                 
  ___\///\\\/\\\/________________________________                
   _____\///\\\/__________/\\\\\_____/\\\____/\\\_               
    _______\/\\\_________/\\\///\\\__\/\\\___\/\\\_              
     _______\/\\\________/\\\__\//\\\_\/\\\___\/\\\_             
      _______\/\\\_______\//\\\__/\\\__\/\\\___\/\\\_            
       _______\/\\\________\///\\\\\/___\//\\\\\\\\\__           
        _______\///___________\/////______\/////////___          
__/\\\______________/\\\_________________________/\\\____        
 _\/\\\_____________\/\\\_______________________/\\\\\\\__       
  _\/\\\_____________\/\\\__/\\\________________/\\\\\\\\\_      
   _\//\\\____/\\\____/\\\__\///___/\\/\\\\\\___\//\\\\\\\__     
    __\//\\\__/\\\\\__/\\\____/\\\_\/\\\////\\\___\//\\\\\___    
     ___\//\\\/\\\/\\\/\\\____\/\\\_\/\\\__\//\\\___\//\\\____   
      ____\//\\\\\\//\\\\\_____\/\\\_\/\\\___\/\\\____\///_____  
       _____\//\\\__\//\\\______\/\\\_\/\\\___\/\\\_____/\\\____ 
        ______\///____\///_______\///__\///____\///_____\///_____
""",
    'computer_wins':
r"""
 ____ ____ ____ ____ ____ ____ ____ ____ _________ ____ ____ ____ ____ 
||C |||o |||m |||p |||u |||t |||e |||r |||       |||W |||i |||n |||s ||
||__|||__|||__|||__|||__|||__|||__|||__|||_______|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|/__\|
""",
    'fainted':
r"""
     ___           ___                       ___           ___           ___           ___     
    /\  \         /\  \          ___        /\__\         /\  \         /\  \         /\  \    
   /::\  \       /::\  \        /\  \      /::|  |        \:\  \       /::\  \       /::\  \   
  /:/\:\  \     /:/\:\  \       \:\  \    /:|:|  |         \:\  \     /:/\:\  \     /:/\:\  \  
 /::\~\:\  \   /::\~\:\  \      /::\__\  /:/|:|  |__       /::\  \   /::\~\:\  \   /:/  \:\__\ 
/:/\:\ \:\__\ /:/\:\ \:\__\  __/:/\/__/ /:/ |:| /\__\     /:/\:\__\ /:/\:\ \:\__\ /:/__/ \:|__|
\/__\:\ \/__/ \/__\:\/:/  / /\/:/  /    \/__|:|/:/  /    /:/  \/__/ \:\~\:\ \/__/ \:\  \ /:/  /
     \:\__\        \::/  /  \::/__/         |:/:/  /    /:/  /       \:\ \:\__\    \:\  /:/  / 
      \/__/        /:/  /    \:\__\         |::/  /     \/__/         \:\ \/__/     \:\/:/  /  
                  /:/  /      \/__/         /:/  /                     \:\__\        \::/__/   
                  \/__/                     \/__/                       \/__/         ~~       
"""
    }

if __name__ == "__main__":
    main()





