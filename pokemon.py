import json
import os
from dataclasses import dataclass
from typing import List

@dataclass
class Pokemon:
    name: str
    type: str
    HP: int  
    stage: int  
    attacks: dict[str,int] 
    weakness: str
    resistance: str | None

    def __post_init__(self, **args):
        self.hp = self.HP
        self.max_hp = self.HP

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        self.hp = max(0, int(self.hp) - int(damage))
        return damage

class PokemonManager:
    def __init__(self, filename: str = "pokemon.json"):
        self.filename = filename
        self.pokemon: List[Pokemon] = []
        self.load_pokemon()

    def load_pokemon(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.pokemon = [Pokemon(**pokemon) for pokemon in data]

    def save_pokemon(self):
        with open(self.filename, 'w') as f:
            json.dump([vars(pokemon) for pokemon in self.pokemon], f, indent=2)

    def add_pokemon(self):
        try:
            name = input("Enter pokemon name: ").strip()
            pokemon_type = input("Enter pokemon type: ").strip()
            HP = int(input("Enter HP: "))
            stage = int(input("Enter stage: "))
            attacking = True
            attacks = []
            while attacking:
                attack_name = input("Enter attack name: (hit Enter if no more attacks): ")
                if attack_name == '': 
                    attacking = False
                    break
                attack_damage = int(input(f"Enter '{attack_name}' damage: "))
                attacks.append((attack_name, attack_damage))

            weakness = input("Enter weakness: ")
            resistance = input("Enter resistance: ")
            
            # if height <= 0 or weight <= 0 or age < 0:
            #     print("Height, weight, and age must be positive values.")
            #     return
            
            pokemon = Pokemon(
                name, 
                pokemon_type, 
                HP, 
                stage, 
                {attack_name: attack_damage 
                    for attack_name, attack_damage in attacks},
                weakness,
                resistance
            )

                
            self.pokemon.append(pokemon)
            self.save_pokemon()
            print(f"Added {name} successfully!")
        except ValueError:
            print("Invalid input. Height and weight must be numbers, age must be an integer.")

    def view_pokemon(self, namesOnly = False):
        if not self.pokemon:
            print("No pokemon in the database.")
            return
        for i, pokemon in enumerate(self.pokemon, 1):
            if namesOnly:
                print(f"\nPokemon {i}:")

            else:
                print(f"\nPokemon {i}:")
                print(f"  Name: {pokemon.name}")
                print(f"  Type: {pokemon.type}")
                print(f"  HP: {pokemon.HP}")
                print(f"  Stage: {pokemon.stage}")
                print(f"  Attacks: {pokemon.attacks}")
                print(f"  Weakness: {pokemon.weakness}")
                print(f"  Resistance: {pokemon.resistance}")

    def edit_pokemon(self):
        self.view_pokemon()
        if not self.pokemon:
            return
        try:
            index = int(input("Enter the pokemon number to edit: ")) - 1
            if 0 <= index < len(self.pokemon):
                pokemon = self.pokemon[index]
                print(f"Editing {pokemon.name}. Leave blank to keep current value.")
                
                name = input(f"New name ({pokemon.name}): ").strip()
                pokemon_type = input(f"New Type ({pokemon.type}): ").strip()
                HP = input(f"New HP ({pokemon.HP}): ").strip()
                stage = input(f"New stage ({pokemon.stage}): ").strip()
                print(f"New Attacks: ")
                updated_attacks = {}
                for attack in pokemon.attacks:
                    attack_name = input(f"New attack name: ({attack}): ").strip()
                    attack_damage = input(f"New attack damage: ({attack}: {pokemon.attacks[attack]}): ")
                    updated_attacks[attack_name] = attack_damage
                weakness = input(f"New Weakness ({pokemon.weakness}): ").strip()
                resistance = input(f"New Resistance ({pokemon.resistance}): ").strip()

                pokemon.name = name if name else pokemon.name
                pokemon.type = pokemon_type if pokemon_type else pokemon.type
                pokemon.HP = int(HP) if HP else pokemon.HP
                pokemon.stage = int(stage) if stage else pokemon.stage
                pokemon.attacks = updated_attacks if len(updated_attacks) > 0 else pokemon.attacks
                pokemon.weakness = weakness if weakness else pokemon.weakness
                pokemon.resistance = resistance if resistance else pokemon.resistance

                self.save_pokemon()
                print(f"Updated {pokemon.name} successfully!")
            else:
                print("Invalid pokemon number.")
        except ValueError:
            print("Invalid input. Height and weight must be numbers, age must be an integer.")

    def delete_pokemon(self):
        self.view_pokemon()
        if not self.pokemon:
            return
        try:
            index = int(input("Enter the pokemon number to delete: ")) - 1
            if 0 <= index < len(self.pokemon):
                pokemon = self.pokemon.pop(index)
                self.save_pokemon()
                print(f"Deleted {pokemon.name} successfully!")
            else:
                print("Invalid pokemon number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def run(self):
        while True:
            print("\nPokemon Manager")
            print("1. Add pokemon")
            print("2. View pokemon")
            print("3. Edit pokemon")
            print("4. Delete pokemon")
            print("5. Exit")
            
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                self.add_pokemon()
            elif choice == '2':
                self.view_pokemon()
            elif choice == '3':
                self.edit_pokemon()
            elif choice == '4':
                self.delete_pokemon()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    manager = PokemonManager()
    manager.run()
