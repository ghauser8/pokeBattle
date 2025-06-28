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

            attack_choice = input("Choose attack (1-2): ").strip()

            if attack_choice in ["1", "2"]:
                damage = computer.active_pokemon.take_damage(player.active_pokemon.attacks[choice_map[int(attack_choice)]])
                print(f"{player.active_pokemon.name} used {player.active_pokemon.attacks[choice_map[int(attack_choice)]]} and dealt {damage} damage!")
                return True
            else:
                print("Invalid attack choice. Try again.")
        elif choice == "2":
            print("Available Pokemon:")
            for i, pokemon in enumerate(player.pokemon):
                status = "Alive" if pokemon.is_alive() else "Fainted"
                print(f"{i+1}. {pokemon.name} ({pokemon.hp}/{pokemon.max_hp} HP, {status})")
            swap_choice = input("Choose Pokemon to swap to (1-3, 0 to cancel): ").strip()
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

def computer_turn(computer, player):
    print(f"Computer's turn!")
    # Computer prioritizes attack if active pokemon is strong, else swaps or attacks randomly
    available_pokemon = [i for i, pokemon in enumerate(computer.pokemon) if pokemon.is_alive() and pokemon != computer.active_pokemon]
    if random.random() < 0.6 or not available_pokemon:  # 60% chance to attack
        attack_choice = random.choice([1, 2])
        akey = list(computer.active_pokemon.attacks.keys())[attack_choice]
        damage = player.active_pokemon.take_damage(computer.active_pokemon.attacks[akey])
        print(f"{computer.active_pokemon.name} used {akey} and dealt {damage} damage!")

    else:  # Swap to a random alive pokemon
        swap_index = random.choice(available_pokemon)
        computer.swap_pokemon(swap_index)
        print(f"Computer swapped to {computer.active_pokemon.name}!")
    return True

def main():
    # Load Pokemon
    manager = PokemonManager()
    # pokemon = [
    #     Pokemon("Lion", 100, "Bite", 20, "Roar", 10,
    #     pokemon("Eagle", 80, "Talon Strike", 15, "Screech", 12),
    #     pokemon("Bear", 120, "Claw Swipe", 18, "Slam", 22)
    # ]
    
    # player and computer take turns picking pokemon from common list
    unselected = {p.name: p for p in manager.pokemon}
    players_pokemon = []
    computer_pokemon = []
    choice_map = {}
    while len(players_pokemon) < 2:
        # print out the remaining pokemon names to choose from
        choice_map = {}
        c = 1
        for p in unselected:
            print(f"  {c}. {p}\n")
            choice_map[str(c)] = p
            c += 1

        player_choice = input(f"Pick a Pokemon (1-{c-1}): ")
        players_pokemon.append(unselected[choice_map[player_choice]])
        del unselected[choice_map[player_choice]]

        # computer selects a pokemon
        choice_map = {
            i: p for i,p in enumerate(unselected.keys())
        }
        if len(unselected) - 1 > 0:
            computer_choice = random.randint(0,len(unselected)-1)
        else:
            computer_choice = 0
        computer_pokemon.append(unselected[choice_map[computer_choice]])
        del unselected[choice_map[computer_choice]]
        
    player = Player("Player", players_pokemon)
    computer = Player("Computer", computer_pokemon)
    
    print("Welcome to Pokemon Battle!")
    print("Each Pokemon has two attacks and health points. Take turns to attack, swap, or forfeit.")
    
    while player.has_alive_pokemon() and computer.has_alive_pokemon():
        display_status(player, computer)
        
        # Player's turn
        if not player_turn(player, computer):
            print("Computer wins!")
            break
            
        if not computer.active_pokemon.is_alive():
            print(f"Computer's {computer.active_pokemon.name} fainted!")
            alive_pokemon = [i for i, pokemon in enumerate(computer.pokemon) if pokemon.is_alive()]
            if alive_pokemon:
                computer.swap_pokemon(alive_pokemon[0])
                print(f"Computer sent out {computer.active_pokemon.name}!")
            else:
                print("Player wins!")
                break
                
        if not computer.has_alive_pokemon():
            print("Player wins!")
            break
            
        # Computer's turn
        computer_turn(computer, player)
        
        if not player.active_pokemon.is_alive():
            print(f"Player's {player.active_pokemon.name} fainted!")
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
                print("Computer wins!")
                break

if __name__ == "__main__":
    main()
