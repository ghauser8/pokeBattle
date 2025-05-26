import random

from pokemon import Pokemon, PokemonManager

class Animal(Pokemon):
    def __init__(self, **args):

        super().__init__(**args)
        self.hp = self.HP
        self.max_hp = self.HP

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return damage

class Player:
    def __init__(self, name, animals):
        self.name = name
        self.animals = animals
        self.active_animal = animals[0]

    def has_alive_animals(self):
        return any(animal.is_alive() for animal in self.animals)

    def swap_animal(self, index):
        if 0 <= index < len(self.animals) and self.animals[index].is_alive():
            self.active_animal = self.animals[index]
            return True
        return False

def display_status(player, computer):
    print(f"\n{player.name}'s {player.active_animal.name}: {player.active_animal.hp}/{player.active_animal.max_hp} HP")
    print(f"Computer's {computer.active_animal.name}: {computer.active_animal.hp}/{computer.active_animal.max_hp} HP\n")

def player_turn(player, computer):
    print(f"{player.name}'s turn!")
    print(f"Active Pokemon: {player.active_animal.name}")
    print("Available actions:")
    print("1. Attack")
    print("2. Swap Pokemon")
    print("3. Forfeit")
    
    while True:
        choice = input("Choose an action (1-3): ").strip()
        if choice == "1":
            i = 1
            choice_map = {}
            for attack in player.active_animal.attacks:
                if i == 1:
                    print(f"Attacks: {i}. {attack} ({player.active_animal.attacks[attack]} dmg)")
                else:
                    print(f"         {i}. {attack} ({player.active_animal.attacks[attack]} dmg)")

                choice_map[i] = attack

            attack_choice = input("Choose attack (1-2): ").strip()

            if attack_choice in ["1", "2"]:
                damage = computer.active_animal.take_damage(player.active_animal.attacks[choice_map[attack_choice]])
                print(f"{player.active_animal.name} used {player.active_animal.attacks[choice_map[attack_choice]]} and dealt {damage} damage!")
                return True
            else:
                print("Invalid attack choice. Try again.")
        elif choice == "2":
            print("Available Pokemon:")
            for i, animal in enumerate(player.animals):
                status = "Alive" if animal.is_alive() else "Fainted"
                print(f"{i+1}. {animal.name} ({animal.hp}/{animal.max_hp} HP, {status})")
            swap_choice = input("Choose Pokemon to swap to (1-3, 0 to cancel): ").strip()
            if swap_choice == "0":
                continue
            try:
                index = int(swap_choice) - 1
                if player.swap_animal(index):
                    print(f"{player.name} swapped to {player.active_animal.name}!")
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
    # Computer prioritizes attack if active animal is strong, else swaps or attacks randomly
    available_animals = [i for i, animal in enumerate(computer.animals) if animal.is_alive() and animal != computer.active_animal]
    if random.random() < 0.6 or not available_animals:  # 60% chance to attack
        attack_choice = random.choice([1, 2])
        akey = list(computer.active_animal.attacks.keys())[attack_choice]
        damage = player.active_animal.take_damage(computer.active_animal.attacks[akey])
        print(f"{computer.active_animal.name} used {akey} and dealt {damage} damage!")

    else:  # Swap to a random alive animal
        swap_index = random.choice(available_animals)
        computer.swap_animal(swap_index)
        print(f"Computer swapped to {computer.active_animal.name}!")
    return True

def main():
    # Load Pokemon
    manager = PokemonManager()
    animals = [
        Animal("Lion", 100, "Bite", 20, "Roar", 10),
        Animal("Eagle", 80, "Talon Strike", 15, "Screech", 12),
        Animal("Bear", 120, "Claw Swipe", 18, "Slam", 22)
    ]
    
    # player and computer take turns picking pokemon from common list
    unselected = {p.name: p for p in manager.pokemon}
    players_pokemon = []
    computer_pokemon = []
    choice_map = {}
    while len(unselected) > 0:
        # print out the remaining pokemon names to choose from
        c = 1
        for p in unselected:
            print(f"  {c}. {p}\n")
            choice_map[str(c)] = unselected[p]
            c += 1

        player_choice = input(f"Pick a Pokemon (1-{c}): ")
        players_pokemon.append(unselected[choice_map[player_choice]])
        del unselected[choice_map[player_choice]]

        # computer selects a pokemon
        pass
        
    player = Player("Player", manager.pokemon)
    computer = Player("Computer", [Animal(a.name, a.hp, a.attack1_name, a.attack1_dmg, a.attack2_name, a.attack2_dmg) for a in animals])
    
    print("Welcome to Animal Battle!")
    print("Each animal has two attacks and health points. Take turns to attack, swap, or forfeit.")
    
    while player.has_alive_animals() and computer.has_alive_animals():
        display_status(player, computer)
        
        # Player's turn
        if not player_turn(player, computer):
            print("Computer wins!")
            break
            
        if not computer.active_animal.is_alive():
            print(f"Computer's {computer.active_animal.name} fainted!")
            alive_animals = [i for i, animal in enumerate(computer.animals) if animal.is_alive()]
            if alive_animals:
                computer.swap_animal(alive_animals[0])
                print(f"Computer sent out {computer.active_animal.name}!")
            else:
                print("Player wins!")
                break
                
        if not computer.has_alive_animals():
            print("Player wins!")
            break
            
        # Computer's turn
        computer_turn(computer, player)
        
        if not player.active_animal.is_alive():
            print(f"Player's {player.active_animal.name} fainted!")
            alive_animals = [i for i, animal in enumerate(player.animals) if animal.is_alive()]
            if alive_animals:
                print("Available animals:")
                for i, animal in enumerate(player.animals):
                    status = "Alive" if animal.is_alive() else "Fainted"
                    print(f"{i+1}. {animal.name} ({animal.hp}/{animal.max_hp} HP, {status})")
                while True:
                    swap_choice = input("Choose animal to swap to (1-3): ").strip()
                    try:
                        index = int(swap_choice) - 1
                        if player.swap_animal(index):
                            print(f"{player.name} swapped to {player.active_animal.name}!")
                            break
                        else:
                            print("Invalid choice or animal is fainted. Try again.")
                    except ValueError:
                        print("Invalid input. Try again.")
            else:
                print("Computer wins!")
                break

if __name__ == "__main__":
    main()
