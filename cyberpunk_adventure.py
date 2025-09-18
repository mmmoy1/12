#!/usr/bin/env python3
"""
CYBERPUNK ADVENTURE - A Text-Based RPG
=====================================

A Nintendo-style cyberpunk text adventure game featuring:
- Turn-based combat system
- Inventory management
- Multiple locations to explore
- NPCs with dialogue
- Main storyline with side quests
- ASCII art interface
- Save/Load functionality

Story: You are a cyberpunk hacker in Neo-Tokyo 2087, trying to uncover
a corporate conspiracy while surviving the dangerous streets.
"""

import json
import os
import random
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    COMBAT = "combat"
    INVENTORY = "inventory"
    DIALOGUE = "dialogue"
    GAME_OVER = "game_over"

class ItemType(Enum):
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    KEY = "key"
    CYBERWARE = "cyberware"

@dataclass
class Item:
    name: str
    description: str
    item_type: ItemType
    value: int
    damage: int = 0
    defense: int = 0
    healing: int = 0
    special_effect: str = ""

@dataclass
class Player:
    name: str
    health: int
    max_health: int
    energy: int
    max_energy: int
    credits: int
    level: int
    experience: int
    location: str
    inventory: List[Item]
    equipped_weapon: Optional[Item] = None
    equipped_armor: Optional[Item] = None

@dataclass
class Enemy:
    name: str
    health: int
    max_health: int
    damage: int
    defense: int
    credits: int
    description: str

@dataclass
class Location:
    name: str
    description: str
    exits: Dict[str, str]
    items: List[Item]
    npcs: List[str]
    enemies: List[Enemy]
    visited: bool = False

class CyberpunkAdventure:
    def __init__(self):
        self.state = GameState.MENU
        self.player = None
        self.current_enemy = None
        self.locations = {}
        self.npcs = {}
        self.game_running = True
        self.initialize_game_data()
        
    def initialize_game_data(self):
        """Initialize all game data including items, locations, and NPCs"""
        
        # Create items
        self.items = {
            "cyber_sword": Item("Cyber Sword", "A glowing energy blade", ItemType.WEAPON, 500, damage=25),
            "neural_armor": Item("Neural Armor", "Protective cybernetic suit", ItemType.ARMOR, 800, defense=15),
            "energy_drink": Item("Energy Drink", "Restores 30 energy", ItemType.CONSUMABLE, 50, healing=30),
            "health_pack": Item("Health Pack", "Restores 50 health", ItemType.CONSUMABLE, 100, healing=50),
            "data_chip": Item("Data Chip", "Contains encrypted information", ItemType.KEY, 0),
            "neural_implant": Item("Neural Implant", "Boosts mental capabilities", ItemType.CYBERWARE, 1000),
            "plasma_pistol": Item("Plasma Pistol", "High-tech energy weapon", ItemType.WEAPON, 300, damage=20),
            "hacker_tool": Item("Hacker Tool", "For breaking into systems", ItemType.CYBERWARE, 200),
        }
        
        # Create enemies
        self.enemies = {
            "corporate_guard": Enemy("Corporate Guard", 60, 60, 15, 5, 100, "A heavily armed security guard"),
            "cyber_thug": Enemy("Cyber Thug", 40, 40, 12, 3, 75, "A street criminal with cybernetic implants"),
            "security_drone": Enemy("Security Drone", 30, 30, 18, 2, 50, "An automated security robot"),
            "data_ghost": Enemy("Data Ghost", 25, 25, 20, 1, 200, "A digital entity from the net"),
            "corporate_exec": Enemy("Corporate Executive", 80, 80, 10, 8, 500, "A high-ranking corporate official"),
        }
        
        # Create locations
        self.locations = {
            "neon_streets": Location(
                "Neon Streets",
                "The bustling streets of Neo-Tokyo, filled with holographic advertisements and cyberpunk atmosphere.",
                {"north": "corporate_tower", "south": "underground_club", "east": "tech_market", "west": "abandoned_warehouse"},
                [self.items["energy_drink"], self.items["plasma_pistol"]],
                ["street_vendor", "cyberpunk"],
                [self.enemies["cyber_thug"]]
            ),
            "corporate_tower": Location(
                "Corporate Tower",
                "A massive skyscraper belonging to the powerful Zaibatsu Corporation. Heavily guarded.",
                {"south": "neon_streets", "up": "executive_floor"},
                [self.items["data_chip"]],
                ["security_guard"],
                [self.enemies["corporate_guard"], self.enemies["security_drone"]]
            ),
            "underground_club": Location(
                "Underground Club",
                "A hidden club where hackers and rebels gather. The air is thick with electronic music.",
                {"north": "neon_streets", "down": "secret_lab"},
                [self.items["hacker_tool"]],
                ["club_owner", "hacker"],
                []
            ),
            "tech_market": Location(
                "Tech Market",
                "A marketplace filled with cybernetic enhancements and illegal tech. Dealers lurk in the shadows.",
                {"west": "neon_streets"},
                [self.items["neural_implant"], self.items["neural_armor"]],
                ["tech_dealer"],
                [self.enemies["cyber_thug"]]
            ),
            "abandoned_warehouse": Location(
                "Abandoned Warehouse",
                "An old industrial building, now used as a hideout for criminals and outcasts.",
                {"east": "neon_streets"},
                [self.items["health_pack"]],
                ["warehouse_owner"],
                [self.enemies["cyber_thug"]]
            ),
            "executive_floor": Location(
                "Executive Floor",
                "The top floor of the corporate tower. Lavish offices and the CEO's private quarters.",
                {"down": "corporate_tower"},
                [self.items["cyber_sword"]],
                ["ceo"],
                [self.enemies["corporate_exec"]]
            ),
            "secret_lab": Location(
                "Secret Lab",
                "A hidden laboratory where illegal experiments are conducted. The air hums with electricity.",
                {"up": "underground_club"},
                [self.items["neural_implant"]],
                ["scientist"],
                [self.enemies["data_ghost"]]
            )
        }
        
        # Create NPCs
        self.npcs = {
            "street_vendor": {
                "name": "Street Vendor",
                "dialogue": "Welcome to the streets, choom! Need some gear? I got the best prices in Neo-Tokyo!",
                "shop_items": ["energy_drink", "health_pack", "plasma_pistol"]
            },
            "cyberpunk": {
                "name": "Cyberpunk",
                "dialogue": "The corporations are watching everything, man. Be careful out there.",
                "quest": "Find the data chip in the corporate tower"
            },
            "security_guard": {
                "name": "Security Guard",
                "dialogue": "This is private property. You need authorization to be here.",
                "hostile": True
            },
            "club_owner": {
                "name": "Club Owner",
                "dialogue": "Welcome to the underground, runner. We don't ask questions here.",
                "quest": "Help me hack into the corporate database"
            },
            "hacker": {
                "name": "Hacker",
                "dialogue": "I've been trying to break into the Zaibatsu mainframe for months. Maybe you can help?",
                "quest": "Retrieve the neural implant from the secret lab"
            },
            "tech_dealer": {
                "name": "Tech Dealer",
                "dialogue": "Looking for some chrome, choom? I got the latest neural implants and armor.",
                "shop_items": ["neural_implant", "neural_armor", "hacker_tool"]
            },
            "warehouse_owner": {
                "name": "Warehouse Owner",
                "dialogue": "This place used to be legit, now it's just a hideout for the desperate.",
                "quest": "Clear out the cyber thugs from the warehouse"
            },
            "ceo": {
                "name": "CEO",
                "dialogue": "So, you've made it this far. Impressive. But you'll never stop our plans!",
                "hostile": True,
                "boss": True
            },
            "scientist": {
                "name": "Scientist",
                "dialogue": "The experiments here... they're not what they seem. The corporations are playing god!",
                "quest": "Destroy the experimental data in the lab"
            }
        }

    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_header(self):
        """Print the game header with ASCII art"""
        header = """
╔══════════════════════════════════════════════════════════════╗
║                    CYBERPUNK ADVENTURE                      ║
║                    Neo-Tokyo 2087                           ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(header)

    def print_status_bar(self):
        """Print player status information"""
        if not self.player:
            return
            
        health_bar = "█" * (self.player.health // 5) + "░" * ((self.player.max_health - self.player.health) // 5)
        energy_bar = "█" * (self.player.energy // 5) + "░" * ((self.player.max_energy - self.player.energy) // 5)
        
        status = f"""
┌─ STATUS ─────────────────────────────────────────────────────┐
│ Health:  [{health_bar:<20}] {self.player.health}/{self.player.max_health} │
│ Energy:  [{energy_bar:<20}] {self.player.energy}/{self.player.max_energy} │
│ Credits: {self.player.credits:<10} Level: {self.player.level} XP: {self.player.experience} │
│ Location: {self.player.location:<45} │
└─────────────────────────────────────────────────────────────┘
        """
        print(status)

    def main_menu(self):
        """Display main menu and handle user input"""
        while self.state == GameState.MENU:
            self.clear_screen()
            self.print_header()
            
            menu_text = """
┌─ MAIN MENU ─────────────────────────────────────────────────┐
│                                                             │
│  1. New Game                                                │
│  2. Load Game                                               │
│  3. Quit                                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
            """
            print(menu_text)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                self.new_game()
            elif choice == "2":
                self.load_game()
            elif choice == "3":
                self.game_running = False
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def new_game(self):
        """Start a new game"""
        self.clear_screen()
        self.print_header()
        
        print("Welcome to Neo-Tokyo 2087!")
        print("You are a cyberpunk hacker trying to survive in a dystopian future.")
        print("The powerful Zaibatsu Corporation controls everything, but rumors")
        print("of a massive conspiracy are spreading through the underground.")
        print()
        
        name = input("Enter your character name: ").strip()
        if not name:
            name = "Runner"
        
        # Create new player
        self.player = Player(
            name=name,
            health=100,
            max_health=100,
            energy=100,
            max_energy=100,
            credits=500,
            level=1,
            experience=0,
            location="neon_streets",
            inventory=[self.items["plasma_pistol"], self.items["energy_drink"]]
        )
        
        self.state = GameState.PLAYING
        self.game_loop()

    def load_game(self):
        """Load a saved game"""
        try:
            with open("cyberpunk_save.json", "r") as f:
                save_data = json.load(f)
            
            # Reconstruct player object
            self.player = Player(**save_data["player"])
            
            # Reconstruct items in inventory
            for i, item_data in enumerate(self.player.inventory):
                if isinstance(item_data, dict):
                    item_type = ItemType(item_data["item_type"])
                    self.player.inventory[i] = Item(
                        name=item_data["name"],
                        description=item_data["description"],
                        item_type=item_type,
                        value=item_data["value"],
                        damage=item_data.get("damage", 0),
                        defense=item_data.get("defense", 0),
                        healing=item_data.get("healing", 0),
                        special_effect=item_data.get("special_effect", "")
                    )
            
            self.state = GameState.PLAYING
            print(f"Game loaded! Welcome back, {self.player.name}!")
            input("Press Enter to continue...")
            self.game_loop()
            
        except FileNotFoundError:
            print("No save file found!")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"Error loading game: {e}")
            input("Press Enter to continue...")

    def save_game(self):
        """Save the current game state"""
        try:
            save_data = {
                "player": asdict(self.player)
            }
            
            with open("cyberpunk_save.json", "w") as f:
                json.dump(save_data, f, indent=2)
            
            print("Game saved successfully!")
            input("Press Enter to continue...")
            
        except Exception as e:
            print(f"Error saving game: {e}")
            input("Press Enter to continue...")

    def game_loop(self):
        """Main game loop"""
        while self.state == GameState.PLAYING and self.game_running:
            self.clear_screen()
            self.print_header()
            self.print_status_bar()
            
            current_location = self.locations[self.player.location]
            print(f"\n📍 {current_location.name}")
            print(f"{current_location.description}\n")
            
            # Check for enemies
            if current_location.enemies:
                enemy = random.choice(current_location.enemies)
                print(f"⚠️  A {enemy.name} appears!")
                self.start_combat(enemy)
                continue
            
            # Show available actions
            self.show_location_actions(current_location)

    def show_location_actions(self, location: Location):
        """Show available actions for current location"""
        print("Available actions:")
        print("1. Look around")
        print("2. Move to another location")
        print("3. Check inventory")
        print("4. Talk to NPCs")
        print("5. Search for items")
        print("6. Save game")
        print("7. Quit to main menu")
        
        choice = input("\nWhat do you want to do? ").strip()
        
        if choice == "1":
            self.look_around(location)
        elif choice == "2":
            self.move_location(location)
        elif choice == "3":
            self.show_inventory()
        elif choice == "4":
            self.talk_to_npcs(location)
        elif choice == "5":
            self.search_location(location)
        elif choice == "6":
            self.save_game()
        elif choice == "7":
            self.state = GameState.MENU
        else:
            print("Invalid choice!")
            input("Press Enter to continue...")

    def look_around(self, location: Location):
        """Look around the current location"""
        print(f"\nYou look around {location.name}...")
        print(location.description)
        
        if location.exits:
            print("\nExits:")
            for direction, destination in location.exits.items():
                print(f"  {direction.capitalize()}: {destination.replace('_', ' ').title()}")
        
        if location.npcs:
            print("\nYou see:")
            for npc in location.npcs:
                print(f"  - {self.npcs[npc]['name']}")
        
        input("\nPress Enter to continue...")

    def move_location(self, location: Location):
        """Move to another location"""
        if not location.exits:
            print("There are no exits from this location!")
            input("Press Enter to continue...")
            return
        
        print("\nWhere do you want to go?")
        for i, (direction, destination) in enumerate(location.exits.items(), 1):
            print(f"{i}. {direction.capitalize()} - {destination.replace('_', ' ').title()}")
        
        try:
            choice = int(input("Enter your choice: ")) - 1
            directions = list(location.exits.keys())
            
            if 0 <= choice < len(directions):
                direction = directions[choice]
                destination = location.exits[direction]
                self.player.location = destination
                print(f"You move {direction} to {destination.replace('_', ' ').title()}.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def show_inventory(self):
        """Display player inventory"""
        self.state = GameState.INVENTORY
        
        while self.state == GameState.INVENTORY:
            self.clear_screen()
            self.print_header()
            
            print("┌─ INVENTORY ─────────────────────────────────────────────────┐")
            print(f"│ Credits: {self.player.credits:<50} │")
            print("├─────────────────────────────────────────────────────────────┤")
            
            if not self.player.inventory:
                print("│ Your inventory is empty.                                │")
            else:
                for i, item in enumerate(self.player.inventory, 1):
                    print(f"│ {i:2d}. {item.name:<30} - {item.description:<25} │")
            
            print("├─────────────────────────────────────────────────────────────┤")
            print("│ Equipped Weapon: ", end="")
            if self.player.equipped_weapon:
                print(f"{self.player.equipped_weapon.name:<40} │")
            else:
                print("None" + " " * 40 + "│")
            
            print("│ Equipped Armor:  ", end="")
            if self.player.equipped_armor:
                print(f"{self.player.equipped_armor.name:<40} │")
            else:
                print("None" + " " * 40 + "│")
            
            print("└─────────────────────────────────────────────────────────────┘")
            
            print("\nOptions:")
            print("1. Use item")
            print("2. Equip weapon")
            print("3. Equip armor")
            print("4. Drop item")
            print("5. Back to game")
            
            choice = input("\nWhat do you want to do? ").strip()
            
            if choice == "1":
                self.use_item()
            elif choice == "2":
                self.equip_weapon()
            elif choice == "3":
                self.equip_armor()
            elif choice == "4":
                self.drop_item()
            elif choice == "5":
                self.state = GameState.PLAYING
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")

    def use_item(self):
        """Use an item from inventory"""
        if not self.player.inventory:
            print("Your inventory is empty!")
            input("Press Enter to continue...")
            return
        
        print("\nWhich item do you want to use?")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Enter item number: ")) - 1
            if 0 <= choice < len(self.player.inventory):
                item = self.player.inventory[choice]
                
                if item.item_type == ItemType.CONSUMABLE:
                    if item.healing > 0:
                        self.player.health = min(self.player.max_health, self.player.health + item.healing)
                        print(f"You used {item.name} and restored {item.healing} health!")
                    elif "energy" in item.name.lower():
                        self.player.energy = min(self.player.max_energy, self.player.energy + item.healing)
                        print(f"You used {item.name} and restored {item.healing} energy!")
                    
                    self.player.inventory.remove(item)
                else:
                    print(f"You can't use {item.name} right now.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def equip_weapon(self):
        """Equip a weapon from inventory"""
        weapons = [item for item in self.player.inventory if item.item_type == ItemType.WEAPON]
        
        if not weapons:
            print("You don't have any weapons!")
            input("Press Enter to continue...")
            return
        
        print("\nWhich weapon do you want to equip?")
        for i, weapon in enumerate(weapons, 1):
            print(f"{i}. {weapon.name} (Damage: {weapon.damage})")
        
        try:
            choice = int(input("Enter weapon number: ")) - 1
            if 0 <= choice < len(weapons):
                weapon = weapons[choice]
                self.player.equipped_weapon = weapon
                print(f"You equipped {weapon.name}!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def equip_armor(self):
        """Equip armor from inventory"""
        armors = [item for item in self.player.inventory if item.item_type == ItemType.ARMOR]
        
        if not armors:
            print("You don't have any armor!")
            input("Press Enter to continue...")
            return
        
        print("\nWhich armor do you want to equip?")
        for i, armor in enumerate(armors, 1):
            print(f"{i}. {armor.name} (Defense: {armor.defense})")
        
        try:
            choice = int(input("Enter armor number: ")) - 1
            if 0 <= choice < len(armors):
                armor = armors[choice]
                self.player.equipped_armor = armor
                print(f"You equipped {armor.name}!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def drop_item(self):
        """Drop an item from inventory"""
        if not self.player.inventory:
            print("Your inventory is empty!")
            input("Press Enter to continue...")
            return
        
        print("\nWhich item do you want to drop?")
        for i, item in enumerate(self.player.inventory, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Enter item number: ")) - 1
            if 0 <= choice < len(self.player.inventory):
                item = self.player.inventory[choice]
                self.player.inventory.remove(item)
                print(f"You dropped {item.name}.")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def talk_to_npcs(self, location: Location):
        """Talk to NPCs in current location"""
        if not location.npcs:
            print("There's no one to talk to here.")
            input("Press Enter to continue...")
            return
        
        print("\nWho do you want to talk to?")
        for i, npc_id in enumerate(location.npcs, 1):
            npc = self.npcs[npc_id]
            print(f"{i}. {npc['name']}")
        
        try:
            choice = int(input("Enter NPC number: ")) - 1
            if 0 <= choice < len(location.npcs):
                npc_id = location.npcs[choice]
                npc = self.npcs[npc_id]
                
                print(f"\n{npc['name']}: \"{npc['dialogue']}\"")
                
                if "quest" in npc:
                    print(f"\nQuest: {npc['quest']}")
                
                if "shop_items" in npc:
                    self.show_shop(npc)
                
                if npc.get("hostile", False):
                    print("\nThe NPC becomes hostile!")
                    # Create enemy from NPC
                    enemy = Enemy(
                        name=npc['name'],
                        health=60,
                        max_health=60,
                        damage=15,
                        defense=5,
                        credits=100,
                        description=npc['dialogue']
                    )
                    self.start_combat(enemy)
                    return
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def show_shop(self, npc):
        """Show shop interface"""
        if "shop_items" not in npc:
            return
        
        print(f"\n{npc['name']}'s Shop:")
        print("Items for sale:")
        
        for i, item_id in enumerate(npc['shop_items'], 1):
            item = self.items[item_id]
            print(f"{i}. {item.name} - {item.description} - {item.value} credits")
        
        print(f"\nYour credits: {self.player.credits}")
        
        try:
            choice = int(input("Enter item number to buy (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(npc['shop_items']):
                item_id = npc['shop_items'][choice - 1]
                item = self.items[item_id]
                
                if self.player.credits >= item.value:
                    self.player.credits -= item.value
                    # Create a copy of the item for the player
                    new_item = Item(
                        name=item.name,
                        description=item.description,
                        item_type=item.item_type,
                        value=item.value,
                        damage=item.damage,
                        defense=item.defense,
                        healing=item.healing,
                        special_effect=item.special_effect
                    )
                    self.player.inventory.append(new_item)
                    print(f"You bought {item.name} for {item.value} credits!")
                else:
                    print("You don't have enough credits!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

    def search_location(self, location: Location):
        """Search for items in current location"""
        if not location.items:
            print("You don't find anything useful here.")
            input("Press Enter to continue...")
            return
        
        print("You search the area...")
        time.sleep(1)
        
        found_item = random.choice(location.items)
        print(f"You found: {found_item.name} - {found_item.description}")
        
        # Create a copy of the item
        new_item = Item(
            name=found_item.name,
            description=found_item.description,
            item_type=found_item.item_type,
            value=found_item.value,
            damage=found_item.damage,
            defense=found_item.defense,
            healing=found_item.healing,
            special_effect=found_item.special_effect
        )
        
        self.player.inventory.append(new_item)
        location.items.remove(found_item)
        
        input("Press Enter to continue...")

    def start_combat(self, enemy: Enemy):
        """Start combat with an enemy"""
        self.state = GameState.COMBAT
        self.current_enemy = enemy
        
        while self.state == GameState.COMBAT:
            self.clear_screen()
            self.print_header()
            
            # Show combat status
            print("┌─ COMBAT ─────────────────────────────────────────────────────┐")
            print(f"│ Enemy: {enemy.name:<50} │")
            print(f"│ Health: {enemy.health}/{enemy.max_health:<45} │")
            print(f"│ Damage: {enemy.damage:<48} │")
            print("├─────────────────────────────────────────────────────────────┤")
            print(f"│ Your Health: {self.player.health}/{self.player.max_health:<40} │")
            print(f"│ Your Energy: {self.player.energy}/{self.player.max_energy:<40} │")
            print("└─────────────────────────────────────────────────────────────┘")
            
            print(f"\n{enemy.description}")
            print("\nCombat options:")
            print("1. Attack")
            print("2. Use item")
            print("3. Run away")
            
            choice = input("\nWhat do you want to do? ").strip()
            
            if choice == "1":
                self.player_attack(enemy)
            elif choice == "2":
                self.use_combat_item()
            elif choice == "3":
                if self.run_away():
                    self.state = GameState.PLAYING
                    return
            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
                continue
            
            # Check if enemy is defeated
            if enemy.health <= 0:
                self.defeat_enemy(enemy)
                break
            
            # Enemy attacks
            self.enemy_attack(enemy)
            
            # Check if player is defeated
            if self.player.health <= 0:
                self.game_over()
                break

    def player_attack(self, enemy: Enemy):
        """Player attacks enemy"""
        if not self.player.equipped_weapon:
            damage = random.randint(5, 15)
            print(f"You punch the {enemy.name} for {damage} damage!")
        else:
            weapon = self.player.equipped_weapon
            damage = weapon.damage + random.randint(-5, 5)
            damage = max(1, damage)  # Minimum 1 damage
            print(f"You attack with {weapon.name} for {damage} damage!")
        
        enemy.health -= damage
        self.player.energy -= 10
        
        if self.player.energy < 0:
            self.player.energy = 0
        
        input("Press Enter to continue...")

    def use_combat_item(self):
        """Use item during combat"""
        consumables = [item for item in self.player.inventory if item.item_type == ItemType.CONSUMABLE]
        
        if not consumables:
            print("You don't have any consumable items!")
            input("Press Enter to continue...")
            return
        
        print("\nWhich item do you want to use?")
        for i, item in enumerate(consumables, 1):
            print(f"{i}. {item.name} - {item.description}")
        
        try:
            choice = int(input("Enter item number: ")) - 1
            if 0 <= choice < len(consumables):
                item = consumables[choice]
                
                if item.healing > 0:
                    self.player.health = min(self.player.max_health, self.player.health + item.healing)
                    print(f"You used {item.name} and restored {item.healing} health!")
                elif "energy" in item.name.lower():
                    self.player.energy = min(self.player.max_energy, self.player.energy + item.healing)
                    print(f"You used {item.name} and restored {item.healing} energy!")
                
                self.player.inventory.remove(item)
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def run_away(self):
        """Attempt to run away from combat"""
        if random.random() < 0.7:  # 70% chance to escape
            print("You successfully run away!")
            return True
        else:
            print("You failed to escape!")
            return False

    def enemy_attack(self, enemy: Enemy):
        """Enemy attacks player"""
        damage = enemy.damage + random.randint(-3, 3)
        damage = max(1, damage)  # Minimum 1 damage
        
        # Apply armor defense
        if self.player.equipped_armor:
            damage -= self.player.equipped_armor.defense
            damage = max(1, damage)  # Minimum 1 damage
        
        self.player.health -= damage
        print(f"The {enemy.name} attacks you for {damage} damage!")
        
        input("Press Enter to continue...")

    def defeat_enemy(self, enemy: Enemy):
        """Handle enemy defeat"""
        print(f"\n🎉 You defeated the {enemy.name}!")
        
        # Gain credits and experience
        credits_gained = enemy.credits
        exp_gained = enemy.max_health // 2
        
        self.player.credits += credits_gained
        self.player.experience += exp_gained
        
        print(f"You gained {credits_gained} credits and {exp_gained} experience!")
        
        # Check for level up
        exp_needed = self.player.level * 100
        if self.player.experience >= exp_needed:
            self.level_up()
        
        # Remove enemy from location
        current_location = self.locations[self.player.location]
        if enemy in current_location.enemies:
            current_location.enemies.remove(enemy)
        
        self.state = GameState.PLAYING
        input("Press Enter to continue...")

    def level_up(self):
        """Handle player level up"""
        self.player.level += 1
        self.player.experience = 0
        
        # Increase stats
        health_increase = 20
        energy_increase = 10
        
        self.player.max_health += health_increase
        self.player.health = self.player.max_health
        self.player.max_energy += energy_increase
        self.player.energy = self.player.max_energy
        
        print(f"\n🎊 LEVEL UP! You are now level {self.player.level}!")
        print(f"Health increased by {health_increase}!")
        print(f"Energy increased by {energy_increase}!")

    def game_over(self):
        """Handle game over"""
        self.state = GameState.GAME_OVER
        self.clear_screen()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                        GAME OVER                            ║
╚══════════════════════════════════════════════════════════════╝

Your cyberpunk adventure has come to an end. The neon lights of Neo-Tokyo
fade as your consciousness slips away...

But every ending is a new beginning in the digital realm.
        """)
        
        input("Press Enter to return to main menu...")
        self.state = GameState.MENU

    def run(self):
        """Run the game"""
        while self.game_running:
            if self.state == GameState.MENU:
                self.main_menu()
            elif self.state == GameState.PLAYING:
                self.game_loop()
        
        print("Thanks for playing Cyberpunk Adventure!")

if __name__ == "__main__":
    game = CyberpunkAdventure()
    game.run()