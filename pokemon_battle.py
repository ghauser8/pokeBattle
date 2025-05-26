import random

class Animal:
    def __init__(self, name, hp, attack1_name, attack1_dmg, attack2_name, attack2_dmg):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack1_name = attack1_name
        self.attack1_dmg = attack1_dmg
        self.attack2_name = attack2_name
        self.attack2_dmg = attack2_dmg

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
    print(f"Active animal: {player.active_animal.name}")
    print("Available actions:")
    print("1. Attack")
    print("2. Swap animal")
    print("3. Forfeit")
    
    while True:
        choice = input("Choose an action (1-3): ").strip()
        if choice == "1":
            print(f"Attacks: 1. {player.active_animal.attack1_name} ({player.active_animal.attack1_dmg} dmg)")
            print(f"         2. {player.active_animal.attack2_name} ({player.active_animal.attack2_dmg} dmg)")
            attack_choice = input("Choose attack (1-2): ").strip()
            if attack_choice == "1":
                damage = computer.active_animal.take_damage(player.active_animal.attack1_dmg)
                print(f"{player.active_animal.name} used {player.active_animal.attack1_name} and dealt {damage} damage!")
                return True
            elif attack_choice == "2":
                damage = computer.active_animal.take_damage(player.active_animal.attack2_dmg)
                print(f"{player.active_animal.name} used {player.active_animal.attack2_name} and dealt {damage} damage!")
                return True
            else:
                print("Invalid attack choice. Try again.")
        elif choice == "2":
            print("Available animals:")
            for i, animal in enumerate(player.animals):
                status = "Alive" if animal.is_alive() else "Fainted"
                print(f"{i+1}. {animal.name} ({animal.hp}/{animal.max_hp} HP, {status})")
            swap_choice = input("Choose animal to swap to (1-3, 0 to cancel): ").strip()
            if swap_choice == "0":
                continue
            try:
                index = int(swap_choice) - 1
                if player.swap_animal(index):
                    print(f"{player.name} swapped to {player.active_animal.name}!")
                    return True
                else:
                    print("Invalid choice or animal is fainted. Try again.")
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
    if random.random() < 0.7 or not available_animals:  # 70% chance to attack
        attack_choice = random.choice([1, 2])
        if attack_choice == 1:
            damage = player.active_animal.take_damage(computer.active_animal.attack1_dmg)
            print(f"{computer.active_animal.name} used {computer.active_animal.attack1_name} and dealt {damage} damage!")
        else:
            damage = player.active_animal.take_damage(computer.active_animal.attack2_dmg)
            print(f"{computer.active_animal.name} used {computer.active_animal.attack2_name} and dealt {damage} damage!")
    else:  # Swap to a random alive animal
        swap_index = random.choice(available_animals)
        computer.swap_animal(swap_index)
        print(f"Computer swapped to {computer.active_animal.name}!")
    return True

def main():
    # Define animals
    animals = [
        Animal("Lion", 100, "Bite", 20, "Roar", 10),
        Animal("Eagle", 80, "Talon Strike", 15, "Screech", 12),
        Animal("Bear", 120, "Claw Swipe", 18, "Slam", 22)
    ]
    
    player = Player("Player", [Animal(a.name, a.hp, a.attack1_name, a.attack1_dmg, a.attack2_name, a.attack2_dmg) for a in animals])
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
