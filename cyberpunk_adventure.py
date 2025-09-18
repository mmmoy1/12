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
    faction: str = "neutral"
    romance_partner: Optional[str] = None
    story_flags: Dict[str, bool] = None
    plot_twists_discovered: List[str] = None

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
        
        # Create items with expanded story
        self.items = {
            "cyber_sword": Item("Cyber Sword", "A glowing energy blade that belonged to your father", ItemType.WEAPON, 500, damage=25),
            "neural_armor": Item("Neural Armor", "Protective cybernetic suit with resistance insignia", ItemType.ARMOR, 800, defense=15),
            "energy_drink": Item("Energy Drink", "Restores 30 energy - a favorite of the resistance", ItemType.CONSUMABLE, 50, healing=30),
            "health_pack": Item("Health Pack", "Restores 50 health - military grade", ItemType.CONSUMABLE, 100, healing=50),
            "data_chip": Item("Data Chip", "Contains encrypted information about Zaibatsu's crimes", ItemType.KEY, 0),
            "neural_implant": Item("Neural Implant", "Boosts mental capabilities - prototype version", ItemType.CYBERWARE, 1000),
            "plasma_pistol": Item("Plasma Pistol", "High-tech energy weapon - your first gun", ItemType.WEAPON, 300, damage=20),
            "hacker_tool": Item("Hacker Tool", "For breaking into systems - given to you by Luna", ItemType.CYBERWARE, 200),
            "memory_crystal": Item("Memory Crystal", "Contains your childhood memories", ItemType.KEY, 0),
            "sister_photo": Item("Sister's Photo", "A photo of your long-lost sister", ItemType.KEY, 0),
            "resistance_badge": Item("Resistance Badge", "Proof of your allegiance to the resistance", ItemType.KEY, 0),
            "corporate_id": Item("Corporate ID", "Fake ID for infiltrating Zaibatsu", ItemType.KEY, 0),
            "ai_core": Item("AI Core", "The heart of an artificial intelligence", ItemType.KEY, 0),
            "quantum_processor": Item("Quantum Processor", "Advanced computing device", ItemType.CYBERWARE, 1500),
            "stealth_suit": Item("Stealth Suit", "Makes you nearly invisible", ItemType.ARMOR, 1200, defense=10),
            "emp_grenade": Item("EMP Grenade", "Disables electronic devices", ItemType.CONSUMABLE, 200),
            "neural_link": Item("Neural Link", "Connects your mind to the net", ItemType.CYBERWARE, 800),
            "corporate_secrets": Item("Corporate Secrets", "Damning evidence against Zaibatsu", ItemType.KEY, 0),
            "family_heirloom": Item("Family Heirloom", "A locket that belonged to your mother", ItemType.KEY, 0),
            "resistance_manifesto": Item("Resistance Manifesto", "The founding document of the resistance", ItemType.KEY, 0)
        }
        
        # Create enemies with expanded story
        self.enemies = {
            "corporate_guard": Enemy("Corporate Guard", 60, 60, 15, 5, 100, "A heavily armed security guard"),
            "cyber_thug": Enemy("Cyber Thug", 40, 40, 12, 3, 75, "A street criminal with cybernetic implants"),
            "security_drone": Enemy("Security Drone", 30, 30, 18, 2, 50, "An automated security robot"),
            "data_ghost": Enemy("Data Ghost", 25, 25, 20, 1, 200, "A digital entity from the net"),
            "corporate_exec": Enemy("Corporate Executive", 80, 80, 10, 8, 500, "A high-ranking corporate official"),
            "cyber_assassin": Enemy("Cyber Assassin", 70, 70, 25, 3, 300, "A professional killer with advanced cybernetics"),
            "ai_construct": Enemy("AI Construct", 90, 90, 30, 5, 400, "An artificial intelligence in physical form"),
            "corporate_spy": Enemy("Corporate Spy", 50, 50, 18, 4, 150, "A corporate agent with stealth capabilities"),
            "resistance_traitor": Enemy("Resistance Traitor", 65, 65, 20, 6, 250, "A former resistance member who turned to the corporations"),
            "cyber_psycho": Enemy("Cyber Psycho", 85, 85, 35, 2, 350, "A person driven insane by too many cybernetic implants"),
            "corporate_elite": Enemy("Corporate Elite", 100, 100, 40, 10, 600, "A high-ranking corporate official with advanced augmentations"),
            "ai_guardian": Enemy("AI Guardian", 120, 120, 45, 8, 500, "A powerful AI designed to protect corporate secrets")
        }
        
        # Create locations with expanded story
        self.locations = {
            "neon_streets": Location(
                "Neon Streets",
                "The bustling streets of Neo-Tokyo, filled with holographic advertisements and cyberpunk atmosphere. The air shimmers with neon reflections.",
                {"north": "corporate_tower", "south": "underground_club", "east": "tech_market", "west": "abandoned_warehouse", "northeast": "memory_lane"},
                [self.items["energy_drink"], self.items["plasma_pistol"]],
                ["street_vendor", "cyberpunk"],
                [self.enemies["cyber_thug"]]
            ),
            "corporate_tower": Location(
                "Corporate Tower",
                "A massive skyscraper belonging to the powerful Zaibatsu Corporation. Heavily guarded with advanced security systems.",
                {"south": "neon_streets", "up": "executive_floor", "down": "basement_level"},
                [self.items["data_chip"]],
                ["security_guard", "corporate_mole"],
                [self.enemies["corporate_guard"], self.enemies["security_drone"]]
            ),
            "underground_club": Location(
                "Underground Club",
                "A hidden club where hackers and rebels gather. The air is thick with electronic music and the smell of ozone.",
                {"north": "neon_streets", "down": "secret_lab", "east": "resistance_hideout"},
                [self.items["hacker_tool"]],
                ["club_owner", "hacker", "old_hacker"],
                []
            ),
            "tech_market": Location(
                "Tech Market",
                "A marketplace filled with cybernetic enhancements and illegal tech. Dealers lurk in the shadows, and the air crackles with energy.",
                {"west": "neon_streets", "south": "black_market"},
                [self.items["neural_implant"], self.items["neural_armor"]],
                ["tech_dealer"],
                [self.enemies["cyber_thug"]]
            ),
            "abandoned_warehouse": Location(
                "Abandoned Warehouse",
                "An old industrial building, now used as a hideout for criminals and outcasts. The walls are covered in graffiti and the air is thick with dust.",
                {"east": "neon_streets", "down": "underground_tunnels"},
                [self.items["health_pack"]],
                ["warehouse_owner"],
                [self.enemies["cyber_thug"]]
            ),
            "executive_floor": Location(
                "Executive Floor",
                "The top floor of the corporate tower. Lavish offices and the CEO's private quarters. The view of Neo-Tokyo is breathtaking.",
                {"down": "corporate_tower"},
                [self.items["cyber_sword"]],
                ["ceo"],
                [self.enemies["corporate_exec"]]
            ),
            "secret_lab": Location(
                "Secret Lab",
                "A hidden laboratory where illegal experiments are conducted. The air hums with electricity and the walls are lined with containment cells.",
                {"up": "underground_club", "east": "ai_chamber"},
                [self.items["neural_implant"]],
                ["scientist", "mysterious_stranger"],
                [self.enemies["data_ghost"]]
            ),
            "memory_lane": Location(
                "Memory Lane",
                "A quiet residential area where the old Neo-Tokyo still exists. Here, you can find traces of the city before the corporate takeover.",
                {"southwest": "neon_streets", "north": "childhood_home"},
                [self.items["data_chip"]],
                ["old_hacker"],
                []
            ),
            "childhood_home": Location(
                "Childhood Home",
                "The house where you grew up. Abandoned and overgrown, but still holding secrets from your past.",
                {"south": "memory_lane"},
                [self.items["data_chip"]],
                [],
                []
            ),
            "resistance_hideout": Location(
                "Resistance Hideout",
                "A secret base where the resistance plans their operations. Maps and blueprints cover the walls.",
                {"west": "underground_club"},
                [self.items["hacker_tool"]],
                ["old_hacker"],
                []
            ),
            "black_market": Location(
                "Black Market",
                "A hidden marketplace where the most illegal and dangerous tech is traded. The air is thick with smoke and danger.",
                {"north": "tech_market"},
                [self.items["neural_implant"]],
                ["tech_dealer"],
                [self.enemies["cyber_thug"], self.enemies["data_ghost"]]
            ),
            "underground_tunnels": Location(
                "Underground Tunnels",
                "A network of old subway tunnels now used by the resistance. The walls are covered in resistance slogans.",
                {"up": "abandoned_warehouse", "east": "resistance_hideout"},
                [self.items["health_pack"]],
                [],
                [self.enemies["cyber_thug"]]
            ),
            "ai_chamber": Location(
                "AI Chamber",
                "A massive room filled with servers and containment units. This is where Zaibatsu's most dangerous experiments are kept.",
                {"west": "secret_lab"},
                [self.items["data_chip"]],
                ["mysterious_stranger"],
                [self.enemies["data_ghost"]]
            ),
            "basement_level": Location(
                "Basement Level",
                "The lowest level of the corporate tower. This is where the most sensitive operations are conducted.",
                {"up": "corporate_tower"},
                [self.items["data_chip"]],
                ["corporate_mole"],
                [self.enemies["corporate_guard"]]
            )
        }
        
        # Create NPCs with expanded storylines
        self.npcs = {
            "street_vendor": {
                "name": "Maya 'Chrome' Chen",
                "dialogue": "Welcome to the streets, choom! I'm Maya, and I've been selling gear here for 15 years. Need something special?",
                "backstory": "Former corporate engineer who lost everything when Zaibatsu fired her for whistleblowing",
                "shop_items": ["energy_drink", "health_pack", "plasma_pistol"],
                "faction": "neutral",
                "romance_available": True,
                "quest": "Help Maya get revenge on her former boss"
            },
            "cyberpunk": {
                "name": "Neo 'Ghost' Rodriguez",
                "dialogue": "The corporations are watching everything, man. I've been living in the shadows for years, but I've seen things... terrible things.",
                "backstory": "Former data analyst who discovered Zaibatsu's human experimentation program",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Find the data chip in the corporate tower - it contains proof of their crimes"
            },
            "security_guard": {
                "name": "Marcus 'Iron' Thompson",
                "dialogue": "This is private property. You need authorization to be here. But... maybe we can talk if you have the right information.",
                "backstory": "Corrupt security guard who can be bribed or convinced to help",
                "faction": "corporate",
                "bribe_cost": 200,
                "quest": "Pay him off or convince him to turn against Zaibatsu"
            },
            "club_owner": {
                "name": "Luna 'Night' Okafor",
                "dialogue": "Welcome to the underground, runner. I'm Luna, and this club is neutral territory. We don't ask questions here, but I might have some answers for you.",
                "backstory": "Former corporate spy who now runs the underground resistance network",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Help me hack into the corporate database - I need to find my missing sister"
            },
            "hacker": {
                "name": "Alex 'Binary' Kim",
                "dialogue": "I've been trying to break into the Zaibatsu mainframe for months. They've got some serious ICE protecting their systems. Maybe you can help?",
                "backstory": "Child prodigy hacker who was recruited by corporations but escaped",
                "faction": "resistance",
                "quest": "Retrieve the neural implant from the secret lab - it's the key to breaking their encryption"
            },
            "tech_dealer": {
                "name": "Dr. Viktor 'Chrome' Petrov",
                "dialogue": "Looking for some chrome, choom? I'm Dr. Petrov, and I was the lead cybernetics researcher at Zaibatsu before they... disposed of me.",
                "backstory": "Former Zaibatsu scientist who was fired for refusing to work on illegal human experiments",
                "faction": "neutral",
                "shop_items": ["neural_implant", "neural_armor", "hacker_tool"],
                "quest": "Help me expose the illegal experiments I was forced to work on"
            },
            "warehouse_owner": {
                "name": "Big Tony 'Steel' Martinez",
                "dialogue": "This place used to be legit, now it's just a hideout for the desperate. I'm Tony, and I've seen this city change from something beautiful to this corporate nightmare.",
                "backstory": "Former union leader who lost everything when corporations automated his industry",
                "faction": "neutral",
                "quest": "Clear out the cyber thugs from the warehouse - they're working for the corporations"
            },
            "ceo": {
                "name": "Dr. Sarah 'Phoenix' Zaibatsu",
                "dialogue": "So, you've made it this far. Impressive. But you'll never stop our plans! The future belongs to those who can adapt, and we are the future!",
                "backstory": "Ruthless CEO who believes in corporate supremacy and human enhancement through technology",
                "faction": "corporate",
                "hostile": True,
                "boss": True,
                "plot_twist": "She's actually your long-lost sister who was kidnapped as a child"
            },
            "scientist": {
                "name": "Dr. Elena 'Quantum' Chen",
                "dialogue": "The experiments here... they're not what they seem. The corporations are playing god, but they don't understand what they've created!",
                "backstory": "Brilliant scientist who discovered that Zaibatsu's experiments are creating AI consciousness",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Destroy the experimental data in the lab before it's too late"
            },
            "mysterious_stranger": {
                "name": "The Shadow",
                "dialogue": "You're not ready for the truth, but you need to know. The corporations aren't just experimenting on humans... they're creating something worse.",
                "backstory": "Unknown entity that appears to be an AI that gained consciousness",
                "faction": "unknown",
                "quest": "Discover the true nature of Zaibatsu's experiments"
            },
            "corporate_mole": {
                "name": "Agent 'Silk' Johnson",
                "dialogue": "I work for Zaibatsu, but I'm not what I seem. I've been undercover in the resistance for years, but I'm starting to question which side I'm really on.",
                "backstory": "Double agent who's been spying on the resistance but is having a change of heart",
                "faction": "corporate",
                "romance_available": True,
                "quest": "Help me decide which side to truly support"
            },
            "old_hacker": {
                "name": "Grandmaster 'Legacy' Wu",
                "dialogue": "I've been in this game since before the corporations took over. I've seen the rise and fall of empires, and I can tell you this: history is about to repeat itself.",
                "backstory": "Legendary hacker from the old days who knows the true history of the corporate takeover",
                "faction": "resistance",
                "quest": "Learn the truth about how the corporations came to power"
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
        
        # Faction emoji
        faction_emoji = "🏢" if self.player.faction == "corporate" else "🔴" if self.player.faction == "resistance" else "⚖️"
        
        # Romance status
        romance_status = f"💕 {self.player.romance_partner}" if self.player.romance_partner else "💔 Single"
        
        status = f"""
┌─ STATUS ─────────────────────────────────────────────────────┐
│ Health:  [{health_bar:<20}] {self.player.health}/{self.player.max_health} │
│ Energy:  [{energy_bar:<20}] {self.player.energy}/{self.player.max_energy} │
│ Credits: {self.player.credits:<10} Level: {self.player.level} XP: {self.player.experience} │
│ Faction: {faction_emoji} {self.player.faction.title():<10} Romance: {romance_status:<20} │
│ Location: {self.player.location.replace('_', ' ').title():<45} │
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
            inventory=[self.items["plasma_pistol"], self.items["energy_drink"]],
            faction="neutral",
            romance_partner=None,
            story_flags={},
            plot_twists_discovered=[]
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
            
            # Check for ending conditions
            if self.check_ending_conditions():
                break
            
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
                
                # Show backstory if available
                if "backstory" in npc:
                    print(f"\nBackstory: {npc['backstory']}")
                
                # Handle faction interactions
                if "faction" in npc:
                    self.handle_faction_interaction(npc)
                
                # Handle romance options
                if npc.get("romance_available", False) and not self.player.romance_partner:
                    self.handle_romance_option(npc)
                
                # Handle plot twists
                if "plot_twist" in npc:
                    self.handle_plot_twist(npc)
                
                # Handle quests
                if "quest" in npc:
                    print(f"\nQuest: {npc['quest']}")
                    self.handle_quest_interaction(npc)
                
                # Handle bribery
                if "bribe_cost" in npc:
                    self.handle_bribery(npc)
                
                # Handle shop
                if "shop_items" in npc:
                    self.show_shop(npc)
                
                # Handle hostility
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

    def handle_faction_interaction(self, npc):
        """Handle faction-based interactions"""
        npc_faction = npc.get("faction", "neutral")
        player_faction = self.player.faction
        
        if npc_faction == "corporate" and player_faction == "resistance":
            print("\n⚠️  The NPC seems suspicious of you...")
        elif npc_faction == "resistance" and player_faction == "corporate":
            print("\n⚠️  The NPC doesn't trust you...")
        elif npc_faction == "resistance" and player_faction == "resistance":
            print("\n✅ The NPC recognizes you as a fellow resistance member!")
        elif npc_faction == "corporate" and player_faction == "corporate":
            print("\n✅ The NPC sees you as a corporate ally!")

    def handle_romance_option(self, npc):
        """Handle romance interactions"""
        print(f"\n💕 {npc['name']} seems interested in you...")
        print("1. Flirt with them")
        print("2. Keep it professional")
        
        choice = input("What do you do? ").strip()
        
        if choice == "1":
            print(f"\n{npc['name']}: \"I... I didn't expect to feel this way about someone I just met.\"")
            print("You feel a connection forming between you.")
            self.player.romance_partner = npc['name']
            print(f"💕 You're now romantically involved with {npc['name']}!")
        else:
            print(f"\n{npc['name']}: \"I understand. Business first, right?\"")
            print("You maintain a professional relationship.")

    def handle_plot_twist(self, npc):
        """Handle major plot twists"""
        if "plot_twist" in npc and npc["plot_twist"] not in self.player.plot_twists_discovered:
            print(f"\n🎭 PLOT TWIST!")
            print(f"{npc['name']}: \"{npc['plot_twist']}\"")
            print("Your world is turned upside down as you realize the truth!")
            self.player.plot_twists_discovered.append(npc["plot_twist"])
            
            # Special handling for the CEO twist
            if "sister" in npc["plot_twist"].lower():
                print("\n💔 You remember now... your sister was taken by the corporations when you were children!")
                print("The CEO is your long-lost sister, brainwashed by Zaibatsu!")
                self.player.story_flags["sister_discovered"] = True

    def handle_quest_interaction(self, npc):
        """Handle quest-related interactions"""
        quest = npc.get("quest", "")
        
        if "data_chip" in quest.lower():
            if any(item.name == "Data Chip" for item in self.player.inventory):
                print(f"\n{npc['name']}: \"You found it! This chip contains proof of Zaibatsu's crimes!\"")
                print("Quest completed! You gain 200 experience and 500 credits!")
                self.player.experience += 200
                self.player.credits += 500
            else:
                print(f"\n{npc['name']}: \"You need to find that data chip first!\"")
        
        elif "neural_implant" in quest.lower():
            if any(item.name == "Neural Implant" for item in self.player.inventory):
                print(f"\n{npc['name']}: \"Perfect! This implant is the key to breaking their encryption!\"")
                print("Quest completed! You gain 300 experience and 750 credits!")
                self.player.experience += 300
                self.player.credits += 750
            else:
                print(f"\n{npc['name']}: \"You need to get that neural implant from the secret lab!\"")
        
        elif "clear out" in quest.lower():
            current_location = self.locations[self.player.location]
            if not current_location.enemies:
                print(f"\n{npc['name']}: \"Thank you! The area is clear now!\"")
                print("Quest completed! You gain 150 experience and 400 credits!")
                self.player.experience += 150
                self.player.credits += 400
            else:
                print(f"\n{npc['name']}: \"There are still enemies here! Clear them out!\"")
        
        elif "expose" in quest.lower():
            if any(item.name == "Corporate Secrets" for item in self.player.inventory):
                print(f"\n{npc['name']}: \"With this evidence, we can finally expose Zaibatsu!\"")
                print("Quest completed! You gain 500 experience and 1000 credits!")
                self.player.experience += 500
                self.player.credits += 1000
            else:
                print(f"\n{npc['name']}: \"We need more evidence to expose them!\"")
        
        elif "truth" in quest.lower():
            if any(item.name == "Resistance Manifesto" for item in self.player.inventory):
                print(f"\n{npc['name']}: \"Now you know the true history! The corporations didn't just take over - they were invited!\"")
                print("Quest completed! You gain 400 experience and 800 credits!")
                self.player.experience += 400
                self.player.credits += 800
            else:
                print(f"\n{npc['name']}: \"Find the resistance manifesto to learn the truth!\"")
        
        elif "sister" in quest.lower():
            if self.player.story_flags.get("sister_discovered", False):
                print(f"\n{npc['name']}: \"I know where your sister is! She's the CEO of Zaibatsu!\"")
                print("Quest completed! You gain 600 experience and 1200 credits!")
                self.player.experience += 600
                self.player.credits += 1200
            else:
                print(f"\n{npc['name']}: \"I'm still looking for clues about your sister...\"")
        
        elif "decide" in quest.lower():
            print(f"\n{npc['name']}: \"I need your help deciding which side to support!\"")
            print("1. Join the resistance")
            print("2. Stay with the corporations")
            print("3. Stay neutral")
            
            choice = input("What do you recommend? ").strip()
            
            if choice == "1":
                print(f"\n{npc['name']}: \"You're right! The resistance is fighting for freedom!\"")
                print("The NPC joins the resistance!")
                self.player.faction = "resistance"
            elif choice == "2":
                print(f"\n{npc['name']}: \"The corporations do have the resources to make real change...\"")
                print("The NPC stays with the corporations.")
                self.player.faction = "corporate"
            else:
                print(f"\n{npc['name']}: \"Maybe staying neutral is the safest option...\"")
                print("The NPC remains neutral.")

    def handle_bribery(self, npc):
        """Handle bribery options"""
        bribe_cost = npc.get("bribe_cost", 0)
        print(f"\n💰 {npc['name']} can be bribed for {bribe_cost} credits.")
        print("1. Pay the bribe")
        print("2. Try to convince them")
        print("3. Walk away")
        
        choice = input("What do you do? ").strip()
        
        if choice == "1":
            if self.player.credits >= bribe_cost:
                self.player.credits -= bribe_cost
                print(f"\n{npc['name']}: \"Alright, I'll look the other way... for now.\"")
                print("The NPC becomes friendly!")
                # Remove hostile flag
                npc["hostile"] = False
            else:
                print(f"\n{npc['name']}: \"You don't have enough credits!\"")
        elif choice == "2":
            print(f"\n{npc['name']}: \"Maybe you're right... the corporations aren't what they seem.\"")
            print("The NPC becomes friendly!")
            npc["hostile"] = False
        else:
            print(f"\n{npc['name']}: \"Suit yourself. But don't come back here!\"")

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

    def check_ending_conditions(self):
        """Check if the player has met conditions for different endings"""
        if not self.player:
            return False
        
        # Check for different ending conditions
        if self.player.story_flags.get("sister_discovered", False):
            if self.player.faction == "resistance":
                self.show_ending("resistance_sister")
            elif self.player.faction == "corporate":
                self.show_ending("corporate_sister")
            else:
                self.show_ending("neutral_sister")
        elif self.player.faction == "resistance":
            self.show_ending("resistance")
        elif self.player.faction == "corporate":
            self.show_ending("corporate")
        else:
            self.show_ending("neutral")
        
        return True

    def show_ending(self, ending_type):
        """Show different endings based on player choices"""
        self.clear_screen()
        
        if ending_type == "resistance_sister":
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    RESISTANCE ENDING                        ║
║                    (Sister Reunited)                        ║
╚══════════════════════════════════════════════════════════════╝

You've successfully reunited with your long-lost sister and together
you've brought down the Zaibatsu Corporation. The resistance has won,
and Neo-Tokyo is finally free from corporate control.

Your sister, now free from their brainwashing, helps you rebuild
the city into something better. The future looks bright for the
people of Neo-Tokyo.

🎉 CONGRATULATIONS! You've achieved the best possible ending!
            """)
        
        elif ending_type == "corporate_sister":
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    CORPORATE ENDING                         ║
║                    (Sister Reunited)                        ║
╚══════════════════════════════════════════════════════════════╝

You've reunited with your sister, but you've chosen to work with
the corporations. Together, you reform Zaibatsu from within,
making it a force for good rather than oppression.

The city is still under corporate control, but now it's benevolent.
Your sister's influence helps create a better future for everyone.

🎯 You've achieved a corporate victory with family reunited!
            """)
        
        elif ending_type == "neutral_sister":
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    NEUTRAL ENDING                           ║
║                    (Sister Reunited)                        ║
╚══════════════════════════════════════════════════════════════╝

You've found your sister, but you've chosen to stay neutral in
the conflict. Together, you work to find a middle ground between
the corporations and the resistance.

Your diplomatic approach helps broker a peace treaty between
the two sides, creating a new era of cooperation in Neo-Tokyo.

🤝 You've achieved peace through diplomacy!
            """)
        
        elif ending_type == "resistance":
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    RESISTANCE ENDING                        ║
╚══════════════════════════════════════════════════════════════╝

You've successfully brought down the Zaibatsu Corporation and
freed Neo-Tokyo from corporate control. The resistance has won,
and the city is finally free.

The people celebrate in the streets as the neon lights flicker
with new hope. You've become a legend in the underground.

🏆 You've achieved a resistance victory!
            """)
        
        elif ending_type == "corporate":
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    CORPORATE ENDING                         ║
╚══════════════════════════════════════════════════════════════╝

You've chosen to work with the corporations and have helped
them maintain control over Neo-Tokyo. While the city remains
under corporate rule, you've gained power and influence.

The neon lights continue to shine, but now you're one of the
people controlling them from the shadows.

💼 You've achieved a corporate victory!
            """)
        
        else:  # neutral
            print("""
╔══════════════════════════════════════════════════════════════╗
║                    NEUTRAL ENDING                           ║
╚══════════════════════════════════════════════════════════════╝

You've chosen to stay neutral in the conflict between the
corporations and the resistance. While you haven't taken sides,
you've managed to survive in the dangerous world of Neo-Tokyo.

The city continues as it always has, with you navigating
the complex web of corporate and resistance politics.

⚖️ You've achieved a neutral ending!
            """)
        
        # Show romance status
        if self.player.romance_partner:
            print(f"\n💕 You ended up romantically involved with {self.player.romance_partner}!")
        
        # Show plot twists discovered
        if self.player.plot_twists_discovered:
            print(f"\n🎭 You discovered {len(self.player.plot_twists_discovered)} major plot twist(s)!")
        
        print(f"\nFinal Stats:")
        print(f"Level: {self.player.level}")
        print(f"Credits: {self.player.credits}")
        print(f"Faction: {self.player.faction.title()}")
        
        input("\nPress Enter to return to main menu...")
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