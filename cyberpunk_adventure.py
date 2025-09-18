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
    cybernetics: List[str] = None
    gang_territory: List[str] = None
    time_of_day: str = "day"
    day_count: int = 1
    hacking_skill: int = 0
    gambling_skill: int = 0
    racing_skill: int = 0

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
                {"north": "corporate_tower", "south": "underground_club", "east": "tech_market", "west": "abandoned_warehouse", "northeast": "memory_lane", "southeast": "red_light_district", "northwest": "industrial_zone"},
                [self.items["energy_drink"], self.items["plasma_pistol"]],
                ["street_vendor", "cyberpunk", "street_performer"],
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
            ),
            # NEW MASSIVE LOCATIONS
            "red_light_district": Location(
                "Red Light District",
                "A neon-soaked area filled with bars, clubs, and entertainment venues. The air is thick with music and the smell of alcohol.",
                {"northwest": "neon_streets", "east": "casino_royale", "south": "underground_arena"},
                [self.items["energy_drink"]],
                ["bar_tender", "dancer", "gambler"],
                [self.enemies["cyber_thug"]]
            ),
            "industrial_zone": Location(
                "Industrial Zone",
                "A massive area filled with factories, warehouses, and industrial complexes. The air is thick with smoke and the sound of machinery.",
                {"southeast": "neon_streets", "north": "power_plant", "east": "docks"},
                [self.items["health_pack"]],
                ["factory_worker", "union_leader"],
                [self.enemies["cyber_thug"], self.enemies["corporate_guard"]]
            ),
            "casino_royale": Location(
                "Casino Royale",
                "A luxurious casino filled with holographic games and high-stakes gambling. The air is thick with excitement and money.",
                {"west": "red_light_district", "up": "vip_lounge"},
                [self.items["corporate_id"]],
                ["casino_manager", "high_roller", "dealer"],
                []
            ),
            "underground_arena": Location(
                "Underground Arena",
                "A hidden fighting arena where cybernetic gladiators battle for entertainment. The air is thick with sweat and blood.",
                {"north": "red_light_district", "down": "death_match"},
                [self.items["neural_implant"]],
                ["arena_owner", "fighter", "bookie"],
                [self.enemies["cyber_psycho"]]
            ),
            "power_plant": Location(
                "Power Plant",
                "A massive facility that powers the entire city. The air hums with electricity and the sound of generators.",
                {"south": "industrial_zone", "up": "control_room"},
                [self.items["emp_grenade"]],
                ["engineer", "security_chief"],
                [self.enemies["security_drone"], self.enemies["corporate_guard"]]
            ),
            "docks": Location(
                "The Docks",
                "A massive port area where ships arrive and depart. The air is thick with salt and the sound of waves.",
                {"west": "industrial_zone", "east": "offshore_platform"},
                [self.items["hacker_tool"]],
                ["dock_worker", "smuggler", "customs_agent"],
                [self.enemies["cyber_thug"]]
            ),
            "vip_lounge": Location(
                "VIP Lounge",
                "An exclusive area for the city's elite. The air is thick with expensive perfume and the sound of quiet conversation.",
                {"down": "casino_royale"},
                [self.items["corporate_secrets"]],
                ["corporate_elite", "politician", "celebrité"],
                []
            ),
            "death_match": Location(
                "Death Match Arena",
                "The most dangerous fighting arena in the city. Only the strongest survive here.",
                {"up": "underground_arena"},
                [self.items["cyber_sword"]],
                ["arena_champion", "blood_dealer"],
                [self.enemies["cyber_psycho"], self.enemies["ai_construct"]]
            ),
            "control_room": Location(
                "Control Room",
                "The nerve center of the power plant. This is where the city's power is controlled.",
                {"down": "power_plant"},
                [self.items["data_chip"]],
                ["chief_engineer"],
                [self.enemies["security_drone"]]
            ),
            "offshore_platform": Location(
                "Offshore Platform",
                "A massive platform in the ocean where illegal activities take place. The air is thick with salt and danger.",
                {"west": "docks", "down": "underwater_base"},
                [self.items["ai_core"]],
                ["platform_owner", "smuggler_king"],
                [self.enemies["corporate_guard"], self.enemies["cyber_assassin"]]
            ),
            "underwater_base": Location(
                "Underwater Base",
                "A hidden base beneath the ocean. This is where the most secret operations are conducted.",
                {"up": "offshore_platform"},
                [self.items["corporate_secrets"]],
                ["base_commander", "deep_sea_diver"],
                [self.enemies["ai_construct"], self.enemies["data_ghost"]]
            ),
            "gang_territory": Location(
                "Gang Territory",
                "A dangerous area controlled by street gangs. The air is thick with tension and the sound of gunfire.",
                {"north": "neon_streets", "east": "gang_warehouse"},
                [self.items["plasma_pistol"]],
                ["gang_leader", "street_soldier"],
                [self.enemies["cyber_thug"], self.enemies["cyber_psycho"]]
            ),
            "gang_warehouse": Location(
                "Gang Warehouse",
                "A massive warehouse used by gangs for illegal activities. The air is thick with dust and danger.",
                {"west": "gang_territory", "up": "gang_hideout"},
                [self.items["neural_armor"]],
                ["warehouse_boss", "gang_member"],
                [self.enemies["cyber_thug"]]
            ),
            "gang_hideout": Location(
                "Gang Hideout",
                "A secret hideout where gangs plan their operations. The air is thick with smoke and conspiracy.",
                {"down": "gang_warehouse"},
                [self.items["resistance_manifesto"]],
                ["gang_leader", "street_wise"],
                []
            ),
            "cybernetics_clinic": Location(
                "Cybernetics Clinic",
                "A medical facility specializing in cybernetic enhancements. The air is thick with antiseptic and the sound of machinery.",
                {"north": "tech_market", "east": "research_lab"},
                [self.items["neural_implant"]],
                ["cybernetics_doctor", "augmentation_specialist"],
                []
            ),
            "research_lab": Location(
                "Research Lab",
                "A cutting-edge laboratory where new technologies are developed. The air is thick with ozone and the sound of experiments.",
                {"west": "cybernetics_clinic", "down": "experiment_chamber"},
                [self.items["quantum_processor"]],
                ["research_scientist", "lab_technician"],
                [self.enemies["data_ghost"]]
            ),
            "experiment_chamber": Location(
                "Experiment Chamber",
                "A hidden chamber where dangerous experiments are conducted. The air is thick with electricity and the sound of screams.",
                {"up": "research_lab"},
                [self.items["ai_core"]],
                ["mad_scientist", "test_subject"],
                [self.enemies["ai_construct"], self.enemies["cyber_psycho"]]
            ),
            "data_center": Location(
                "Data Center",
                "A massive facility filled with servers and data storage. The air is thick with the sound of cooling fans.",
                {"south": "corporate_tower", "east": "ai_core_room"},
                [self.items["data_chip"]],
                ["data_analyst", "system_admin"],
                [self.enemies["security_drone"], self.enemies["data_ghost"]]
            ),
            "ai_core_room": Location(
                "AI Core Room",
                "The heart of the city's AI systems. This is where the most advanced artificial intelligence resides.",
                {"west": "data_center"},
                [self.items["ai_core"]],
                ["ai_specialist", "quantum_engineer"],
                [self.enemies["ai_guardian"]]
            ),
            "underground_city": Location(
                "Underground City",
                "A hidden city beneath Neo-Tokyo where outcasts and rebels live. The air is thick with the sound of generators.",
                {"up": "underground_club", "north": "rebel_hq"},
                [self.items["resistance_badge"]],
                ["underground_mayor", "rebel_leader"],
                []
            ),
            "rebel_hq": Location(
                "Rebel Headquarters",
                "The command center of the resistance movement. The air is thick with the sound of planning and plotting.",
                {"south": "underground_city", "east": "war_room"},
                [self.items["resistance_manifesto"]],
                ["resistance_commander", "intelligence_officer"],
                []
            ),
            "war_room": Location(
                "War Room",
                "A strategic planning room where the resistance plans their operations. The air is thick with the sound of strategy.",
                {"west": "rebel_hq"},
                [self.items["corporate_secrets"]],
                ["tactical_advisor", "war_planner"],
                []
            ),
            "cyber_cafe": Location(
                "Cyber Cafe",
                "A futuristic cafe where hackers and netrunners gather. The air is thick with the sound of keyboards and the smell of coffee.",
                {"north": "tech_market", "east": "hacker_den"},
                [self.items["neural_link"]],
                ["cafe_owner", "netrunner", "code_hacker"],
                []
            ),
            "hacker_den": Location(
                "Hacker Den",
                "A secret hideout where the city's best hackers gather. The air is thick with the sound of typing and the glow of screens.",
                {"west": "cyber_cafe", "down": "deep_net"},
                [self.items["hacker_tool"]],
                ["master_hacker", "code_warrior"],
                [self.enemies["data_ghost"]]
            ),
            "deep_net": Location(
                "Deep Net",
                "A virtual reality space where hackers can access the deepest parts of the network. The air is thick with digital energy.",
                {"up": "hacker_den"},
                [self.items["quantum_processor"]],
                ["net_ghost", "digital_entity"],
                [self.enemies["data_ghost"], self.enemies["ai_construct"]]
            ),
            "night_market": Location(
                "Night Market",
                "A bustling market that only opens at night. The air is thick with the smell of street food and the sound of haggling.",
                {"south": "tech_market", "east": "black_market"},
                [self.items["energy_drink"]],
                ["night_vendor", "street_cook", "market_trader"],
                [self.enemies["cyber_thug"]]
            ),
            "rooftop_garden": Location(
                "Rooftop Garden",
                "A beautiful garden on the roof of a building. The air is thick with the smell of flowers and the sound of wind.",
                {"down": "neon_streets", "east": "sky_bridge"},
                [self.items["family_heirloom"]],
                ["garden_keeper", "rooftop_dweller"],
                []
            ),
            "sky_bridge": Location(
                "Sky Bridge",
                "A bridge connecting two skyscrapers high above the city. The air is thick with wind and the sound of traffic below.",
                {"west": "rooftop_garden", "east": "corporate_tower"},
                [self.items["stealth_suit"]],
                ["bridge_guard", "sky_walker"],
                [self.enemies["security_drone"]]
            ),
            "abandoned_subway": Location(
                "Abandoned Subway",
                "An old subway system that's been abandoned. The air is thick with dust and the sound of dripping water.",
                {"north": "underground_tunnels", "south": "subway_station"},
                [self.items["health_pack"]],
                ["subway_dweller", "tunnel_rat"],
                [self.enemies["cyber_thug"]]
            ),
            "subway_station": Location(
                "Subway Station",
                "An old subway station that's been converted into a hideout. The air is thick with the sound of trains and the smell of oil.",
                {"north": "abandoned_subway", "east": "train_yard"},
                [self.items["hacker_tool"]],
                ["station_master", "train_conductor"],
                [self.enemies["cyber_thug"]]
            ),
            "train_yard": Location(
                "Train Yard",
                "A massive yard where trains are stored and maintained. The air is thick with the sound of machinery and the smell of metal.",
                {"west": "subway_station", "north": "industrial_zone"},
                [self.items["neural_armor"]],
                ["yard_foreman", "train_engineer"],
                [self.enemies["corporate_guard"]]
            ),
            # ULTIMATE EXPANSION LOCATIONS
            "space_elevator": Location(
                "Space Elevator",
                "A massive structure reaching into space. The view from here is breathtaking, but the air is thin.",
                {"down": "neon_streets", "up": "orbital_station"},
                [self.items["quantum_processor"]],
                ["elevator_operator", "space_tourist"],
                [self.enemies["security_drone"]]
            ),
            "orbital_station": Location(
                "Orbital Station",
                "A space station orbiting Earth. The view of the planet below is incredible.",
                {"down": "space_elevator", "east": "zero_gravity_lab"},
                [self.items["ai_core"]],
                ["station_commander", "astronaut"],
                [self.enemies["ai_construct"]]
            ),
            "zero_gravity_lab": Location(
                "Zero Gravity Lab",
                "A laboratory where experiments are conducted in zero gravity. Everything floats here.",
                {"west": "orbital_station"},
                [self.items["neural_implant"]],
                ["space_scientist", "gravity_engineer"],
                [self.enemies["data_ghost"]]
            ),
            "moon_colony": Location(
                "Moon Colony",
                "A human colony on the moon. The air is recycled and the gravity is low.",
                {"down": "orbital_station", "north": "lunar_mine"},
                [self.items["corporate_secrets"]],
                ["colonist", "lunar_governor"],
                [self.enemies["cyber_assassin"]]
            ),
            "lunar_mine": Location(
                "Lunar Mine",
                "A mining operation on the moon. The air is thin and the work is dangerous.",
                {"south": "moon_colony"},
                [self.items["quantum_processor"]],
                ["miner", "mine_foreman"],
                [self.enemies["corporate_guard"]]
            ),
            "mars_base": Location(
                "Mars Base",
                "A research base on Mars. The red planet stretches endlessly in all directions.",
                {"down": "orbital_station", "east": "martian_city"},
                [self.items["ai_core"]],
                ["mars_scientist", "base_commander"],
                [self.enemies["ai_guardian"]]
            ),
            "martian_city": Location(
                "Martian City",
                "A domed city on Mars. The air is artificial but breathable.",
                {"west": "mars_base", "north": "martian_ruins"},
                [self.items["resistance_manifesto"]],
                ["martian_citizen", "city_mayor"],
                [self.enemies["cyber_psycho"]]
            ),
            "martian_ruins": Location(
                "Martian Ruins",
                "Ancient ruins on Mars. No one knows who built them or why.",
                {"south": "martian_city"},
                [self.items["memory_crystal"]],
                ["archaeologist", "ruin_explorer"],
                [self.enemies["data_ghost"]]
            ),
            "virtual_reality": Location(
                "Virtual Reality",
                "A digital world where anything is possible. The laws of physics don't apply here.",
                {"up": "hacker_den", "east": "digital_city"},
                [self.items["neural_link"]],
                ["vr_guide", "digital_artist"],
                [self.enemies["ai_construct"]]
            ),
            "digital_city": Location(
                "Digital City",
                "A city made entirely of code. Everything here is digital and can be modified.",
                {"west": "virtual_reality", "north": "code_temple"},
                [self.items["quantum_processor"]],
                ["code_architect", "digital_citizen"],
                [self.enemies["data_ghost"]]
            ),
            "code_temple": Location(
                "Code Temple",
                "A sacred place where the ancient code is kept. Only the most skilled hackers can enter.",
                {"south": "digital_city"},
                [self.items["hacker_tool"]],
                ["code_priest", "temple_guardian"],
                [self.enemies["ai_guardian"]]
            ),
            "time_machine": Location(
                "Time Machine",
                "A device that can travel through time. The air shimmers with temporal energy.",
                {"north": "neon_streets", "east": "past_tokyo"},
                [self.items["memory_crystal"]],
                ["time_traveler", "temporal_scientist"],
                [self.enemies["data_ghost"]]
            ),
            "past_tokyo": Location(
                "Past Tokyo",
                "Tokyo as it was before the corporate takeover. The air is cleaner and the people are happier.",
                {"west": "time_machine", "north": "future_tokyo"},
                [self.items["family_heirloom"]],
                ["past_citizen", "historical_guide"],
                []
            ),
            "future_tokyo": Location(
                "Future Tokyo",
                "Tokyo as it will be in the far future. The technology is beyond comprehension.",
                {"south": "past_tokyo", "east": "dystopian_tokyo"},
                [self.items["ai_core"]],
                ["future_citizen", "time_guardian"],
                [self.enemies["ai_construct"]]
            ),
            "dystopian_tokyo": Location(
                "Dystopian Tokyo",
                "A dark future where the corporations have won completely. Hope is dead here.",
                {"west": "future_tokyo"},
                [self.items["resistance_manifesto"]],
                ["dystopian_survivor", "hope_seeker"],
                [self.enemies["cyber_psycho"]]
            ),
            "parallel_universe": Location(
                "Parallel Universe",
                "A parallel version of Neo-Tokyo where everything is different. The air crackles with dimensional energy.",
                {"north": "neon_streets", "east": "mirror_tokyo"},
                [self.items["quantum_processor"]],
                ["parallel_self", "dimension_guide"],
                [self.enemies["ai_construct"]]
            ),
            "mirror_tokyo": Location(
                "Mirror Tokyo",
                "A mirror version of Neo-Tokyo where everything is reversed. The corporations are the good guys here.",
                {"west": "parallel_universe", "north": "inverted_tokyo"},
                [self.items["corporate_secrets"]],
                ["mirror_citizen", "inverted_corporate"],
                [self.enemies["corporate_guard"]]
            ),
            "inverted_tokyo": Location(
                "Inverted Tokyo",
                "An inverted version of Neo-Tokyo where up is down and down is up. Gravity works differently here.",
                {"south": "mirror_tokyo"},
                [self.items["neural_implant"]],
                ["inverted_citizen", "gravity_guide"],
                [self.enemies["cyber_assassin"]]
            ),
            "dream_realm": Location(
                "Dream Realm",
                "A realm where dreams become reality. The air is thick with imagination and possibility.",
                {"up": "neon_streets", "east": "nightmare_realm"},
                [self.items["memory_crystal"]],
                ["dream_guide", "imagination_weaver"],
                [self.enemies["data_ghost"]]
            ),
            "nightmare_realm": Location(
                "Nightmare Realm",
                "A realm where nightmares come to life. The air is thick with fear and despair.",
                {"west": "dream_realm", "north": "void_realm"},
                [self.items["emp_grenade"]],
                ["nightmare_guide", "fear_eater"],
                [self.enemies["cyber_psycho"]]
            ),
            "void_realm": Location(
                "Void Realm",
                "A realm of pure nothingness. There is no light, no sound, no anything.",
                {"south": "nightmare_realm"},
                [self.items["ai_core"]],
                ["void_walker", "nothingness_guide"],
                [self.enemies["ai_guardian"]]
            ),
            "cyber_heaven": Location(
                "Cyber Heaven",
                "A digital paradise where the souls of the dead live on in cyberspace.",
                {"up": "deep_net", "east": "cyber_hell"},
                [self.items["memory_crystal"]],
                ["digital_soul", "heaven_guide"],
                []
            ),
            "cyber_hell": Location(
                "Cyber Hell",
                "A digital hell where the souls of the damned are tortured for eternity.",
                {"west": "cyber_heaven", "north": "purgatory"},
                [self.items["emp_grenade"]],
                ["damned_soul", "hell_guide"],
                [self.enemies["cyber_psycho"]]
            ),
            "purgatory": Location(
                "Purgatory",
                "A place between heaven and hell where souls wait for judgment.",
                {"south": "cyber_hell"},
                [self.items["resistance_manifesto"]],
                ["purgatory_guide", "waiting_soul"],
                [self.enemies["data_ghost"]]
            ),
            "matrix_city": Location(
                "Matrix City",
                "A city that exists within a computer simulation. Nothing here is real, but it feels real.",
                {"north": "neon_streets", "east": "simulation_lab"},
                [self.items["quantum_processor"]],
                ["matrix_citizen", "simulation_guide"],
                [self.enemies["ai_construct"]]
            ),
            "simulation_lab": Location(
                "Simulation Lab",
                "A laboratory where reality is simulated and tested. The air shimmers with digital energy.",
                {"west": "matrix_city", "north": "reality_engine"},
                [self.items["neural_link"]],
                ["simulation_scientist", "reality_engineer"],
                [self.enemies["data_ghost"]]
            ),
            "reality_engine": Location(
                "Reality Engine",
                "The machine that creates and maintains reality itself. The power here is beyond comprehension.",
                {"south": "simulation_lab"},
                [self.items["ai_core"]],
                ["reality_architect", "engine_operator"],
                [self.enemies["ai_guardian"]]
            ),
            "quantum_dimension": Location(
                "Quantum Dimension",
                "A dimension where quantum physics rules. Everything exists in multiple states simultaneously.",
                {"up": "reality_engine", "east": "probability_field"},
                [self.items["quantum_processor"]],
                ["quantum_physicist", "dimension_guide"],
                [self.enemies["ai_construct"]]
            ),
            "probability_field": Location(
                "Probability Field",
                "A field where probability itself can be manipulated. The future is uncertain here.",
                {"west": "quantum_dimension", "north": "certainty_zone"},
                [self.items["neural_implant"]],
                ["probability_manipulator", "field_guide"],
                [self.enemies["data_ghost"]]
            ),
            "certainty_zone": Location(
                "Certainty Zone",
                "A zone where everything is certain and predetermined. Free will doesn't exist here.",
                {"south": "probability_field"},
                [self.items["corporate_secrets"]],
                ["certainty_guide", "predetermined_citizen"],
                [self.enemies["cyber_assassin"]]
            ),
            "infinity_loop": Location(
                "Infinity Loop",
                "A place where time loops infinitely. The same events repeat over and over again.",
                {"north": "neon_streets", "east": "temporal_prison"},
                [self.items["memory_crystal"]],
                ["loop_prisoner", "temporal_guide"],
                [self.enemies["data_ghost"]]
            ),
            "temporal_prison": Location(
                "Temporal Prison",
                "A prison where time itself is the jailer. Escape is impossible because time always resets.",
                {"west": "infinity_loop", "north": "time_paradox"},
                [self.items["emp_grenade"]],
                ["temporal_prisoner", "time_jailer"],
                [self.enemies["ai_construct"]]
            ),
            "time_paradox": Location(
                "Time Paradox",
                "A place where time paradoxes occur. Cause and effect are meaningless here.",
                {"south": "temporal_prison"},
                [self.items["quantum_processor"]],
                ["paradox_guide", "temporal_anomaly"],
                [self.enemies["ai_guardian"]]
            ),
            "dimension_gate": Location(
                "Dimension Gate",
                "A gateway to other dimensions. The air shimmers with dimensional energy.",
                {"north": "neon_streets", "east": "multiverse_hub"},
                [self.items["neural_link"]],
                ["dimension_guide", "gate_operator"],
                [self.enemies["cyber_assassin"]]
            ),
            "multiverse_hub": Location(
                "Multiverse Hub",
                "A hub connecting all possible universes. Every choice creates a new reality.",
                {"west": "dimension_gate", "north": "reality_fork"},
                [self.items["ai_core"]],
                ["multiverse_guide", "reality_architect"],
                [self.enemies["ai_construct"]]
            ),
            "reality_fork": Location(
                "Reality Fork",
                "A place where reality splits into multiple branches. Every decision creates a new timeline.",
                {"south": "multiverse_hub"},
                [self.items["memory_crystal"]],
                ["fork_guide", "timeline_architect"],
                [self.enemies["data_ghost"]]
            ),
            "void_between_worlds": Location(
                "Void Between Worlds",
                "The empty space between different realities. Nothing exists here except pure potential.",
                {"up": "reality_fork", "east": "creation_engine"},
                [self.items["quantum_processor"]],
                ["void_walker", "creation_guide"],
                [self.enemies["ai_guardian"]]
            ),
            "creation_engine": Location(
                "Creation Engine",
                "The machine that creates new realities. The power here is beyond imagination.",
                {"west": "void_between_worlds"},
                [self.items["ai_core"]],
                ["creation_architect", "engine_operator"],
                [self.enemies["ai_construct"]]
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
            },
            # NEW MASSIVE NPCs
            "street_performer": {
                "name": "Zara 'Neon' Vega",
                "dialogue": "Welcome to the streets, choom! I'm Zara, and I've been performing here for years. The neon lights are my stage!",
                "backstory": "Former corporate entertainer who was fired for speaking out against the system",
                "faction": "neutral",
                "romance_available": True,
                "quest": "Help me expose the truth about corporate entertainment"
            },
            "bar_tender": {
                "name": "Marcus 'Brew' Thompson",
                "dialogue": "What'll it be, choom? I've got the best drinks in the district, and I've heard all the stories.",
                "backstory": "Former corporate executive who quit to open a bar in the red light district",
                "faction": "neutral",
                "quest": "Help me get revenge on my former corporate bosses"
            },
            "dancer": {
                "name": "Luna 'Siren' Rodriguez",
                "dialogue": "The music calls to me, and I dance to forget the pain of this world. But sometimes I remember...",
                "backstory": "Former resistance fighter who lost her memory in a corporate experiment",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Help me recover my lost memories"
            },
            "gambler": {
                "name": "Rico 'Lucky' Martinez",
                "dialogue": "I've been gambling for years, and I've learned that the house always wins... unless you know how to cheat.",
                "backstory": "Former corporate accountant who embezzled money and now lives in hiding",
                "faction": "neutral",
                "quest": "Help me get my family back from the corporations"
            },
            "casino_manager": {
                "name": "Victoria 'Vegas' Chen",
                "dialogue": "Welcome to my casino, runner. I've built this place from nothing, and I'll be damned if I let anyone take it from me.",
                "backstory": "Former corporate lawyer who used her knowledge to build an illegal casino empire",
                "faction": "neutral",
                "quest": "Help me protect my casino from corporate takeover"
            },
            "high_roller": {
                "name": "Alexander 'Ace' Blackwood",
                "dialogue": "Money is just a tool, choom. The real power is in knowing how to use it. And I know how to use it very well.",
                "backstory": "Former corporate CEO who was ousted in a boardroom coup",
                "faction": "corporate",
                "quest": "Help me regain control of my former company"
            },
            "dealer": {
                "name": "Sofia 'Cards' Petrov",
                "dialogue": "I deal the cards, but I don't control the game. That's up to the players... and the house.",
                "backstory": "Former corporate statistician who now uses her skills to run casino games",
                "faction": "neutral",
                "quest": "Help me expose the rigged games in other casinos"
            },
            "arena_owner": {
                "name": "Darius 'Blood' Johnson",
                "dialogue": "Welcome to my arena, runner. Here, only the strongest survive. Are you strong enough?",
                "backstory": "Former corporate security chief who now runs illegal fighting arenas",
                "faction": "neutral",
                "quest": "Help me take down the corporate fighting rings"
            },
            "fighter": {
                "name": "Kai 'Steel' Nakamura",
                "dialogue": "I fight not for glory, but for survival. In this world, you either fight or you die.",
                "backstory": "Former corporate test subject who escaped and now fights for freedom",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Help me free other test subjects from corporate labs"
            },
            "bookie": {
                "name": "Felix 'Numbers' O'Connor",
                "dialogue": "I know the odds better than anyone, and I can tell you this: the house always wins... unless you know the right people.",
                "backstory": "Former corporate data analyst who now runs illegal betting operations",
                "faction": "neutral",
                "quest": "Help me expose the corporate betting scandals"
            },
            "factory_worker": {
                "name": "Maria 'Gears' Santos",
                "dialogue": "I've been working in these factories for 20 years, and I've seen the corporations destroy everything I love.",
                "backstory": "Former union leader who was forced to work in corporate factories",
                "faction": "resistance",
                "quest": "Help me organize a workers' revolution"
            },
            "union_leader": {
                "name": "Carlos 'Union' Rodriguez",
                "dialogue": "The workers are the backbone of this city, and we won't be silenced anymore. It's time to fight back!",
                "backstory": "Former corporate manager who turned against the system and now leads the workers",
                "faction": "resistance",
                "quest": "Help me plan a massive workers' strike"
            },
            "engineer": {
                "name": "Dr. Sarah 'Power' Kim",
                "dialogue": "I keep the city running, but I've seen what the corporations are really doing with all this power. It's not right.",
                "backstory": "Former corporate engineer who discovered the true purpose of the power plant",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate power grid"
            },
            "security_chief": {
                "name": "James 'Iron' Wilson",
                "dialogue": "I'm here to protect the power plant, but I've seen things that make me question who I'm really protecting.",
                "backstory": "Former corporate security chief who is having second thoughts about his job",
                "faction": "corporate",
                "quest": "Help me decide whether to stay loyal or defect"
            },
            "dock_worker": {
                "name": "Roberto 'Docks' Martinez",
                "dialogue": "I've seen what comes through these docks, and it's not just cargo. The corporations are smuggling something dangerous.",
                "backstory": "Former corporate dock worker who discovered illegal smuggling operations",
                "faction": "resistance",
                "quest": "Help me expose the corporate smuggling ring"
            },
            "smuggler": {
                "name": "Isabella 'Shadow' Chen",
                "dialogue": "I move things that others can't, but I've seen what the corporations are really shipping. It's not what you think.",
                "backstory": "Former corporate logistics specialist who now runs illegal smuggling operations",
                "faction": "neutral",
                "quest": "Help me get my family out of the city safely"
            },
            "customs_agent": {
                "name": "David 'Check' Thompson",
                "dialogue": "I'm supposed to check everything that comes through, but the corporations have me looking the other way.",
                "backstory": "Former corporate customs agent who is being blackmailed by the corporations",
                "faction": "corporate",
                "quest": "Help me break free from corporate control"
            },
            "corporate_elite": {
                "name": "Victoria 'Elite' Blackwood",
                "dialogue": "I've been at the top of the corporate ladder for years, but I've seen what it's really built on. It's time for change.",
                "backstory": "Former corporate executive who is disillusioned with the system",
                "faction": "corporate",
                "quest": "Help me reform the corporate system from within"
            },
            "politician": {
                "name": "Senator 'Power' Johnson",
                "dialogue": "I've been in politics for decades, and I've seen how the corporations control everything. It's time to fight back.",
                "backstory": "Former corporate lobbyist who turned against the system and became a politician",
                "faction": "resistance",
                "quest": "Help me pass legislation to limit corporate power"
            },
            "celebrité": {
                "name": "Stella 'Star' Vega",
                "dialogue": "I'm famous, but I'm not free. The corporations own me, and they control everything I do. I want out.",
                "backstory": "Former corporate celebrity who is being controlled by the corporations",
                "faction": "corporate",
                "romance_available": True,
                "quest": "Help me break free from corporate control"
            },
            "arena_champion": {
                "name": "Titan 'Champion' Stone",
                "dialogue": "I've won every fight in this arena, but I've lost everything else. I'm ready to fight for something real.",
                "backstory": "Former corporate test subject who became the arena champion",
                "faction": "resistance",
                "quest": "Help me escape from the arena and join the resistance"
            },
            "blood_dealer": {
                "name": "Viktor 'Blood' Petrov",
                "dialogue": "I deal in blood and pain, but I've seen what the corporations are really doing. It's time to stop them.",
                "backstory": "Former corporate medical researcher who now runs illegal blood trading",
                "faction": "neutral",
                "quest": "Help me expose the corporate blood experiments"
            },
            "chief_engineer": {
                "name": "Dr. Michael 'Power' Chen",
                "dialogue": "I control the power that runs this city, but I've seen what the corporations are really doing with it. It's not right.",
                "backstory": "Former corporate engineer who discovered the true purpose of the power plant",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate power grid"
            },
            "platform_owner": {
                "name": "Captain 'Ocean' Rodriguez",
                "dialogue": "I control this platform, but I've seen what the corporations are really doing out here. It's time to stop them.",
                "backstory": "Former corporate marine who now runs illegal offshore operations",
                "faction": "neutral",
                "quest": "Help me take down the corporate offshore operations"
            },
            "smuggler_king": {
                "name": "King 'Smuggle' Martinez",
                "dialogue": "I'm the king of smuggling in this city, but I've seen what the corporations are really moving. It's time to stop them.",
                "backstory": "Former corporate logistics specialist who now runs the largest smuggling operation in the city",
                "faction": "neutral",
                "quest": "Help me expose the corporate smuggling operations"
            },
            "base_commander": {
                "name": "Commander 'Deep' Johnson",
                "dialogue": "I command this underwater base, but I've seen what the corporations are really doing down here. It's time to stop them.",
                "backstory": "Former corporate marine who now commands an underwater resistance base",
                "faction": "resistance",
                "quest": "Help me plan an attack on the corporate underwater facilities"
            },
            "deep_sea_diver": {
                "name": "Aqua 'Deep' Chen",
                "dialogue": "I dive deep into the ocean, but I've seen what the corporations are really doing down there. It's time to stop them.",
                "backstory": "Former corporate marine biologist who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me expose the corporate ocean experiments"
            },
            "gang_leader": {
                "name": "Razor 'Blade' Thompson",
                "dialogue": "I run this gang, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate security guard who now leads a street gang",
                "faction": "resistance",
                "quest": "Help me unite all the gangs against the corporations"
            },
            "street_soldier": {
                "name": "Blade 'Street' Rodriguez",
                "dialogue": "I fight for my gang, but I've seen what the corporations are really doing to our streets. It's time to fight back.",
                "backstory": "Former corporate test subject who escaped and joined a street gang",
                "faction": "resistance",
                "quest": "Help me take down the corporate operations in our territory"
            },
            "warehouse_boss": {
                "name": "Boss 'Warehouse' Martinez",
                "dialogue": "I run this warehouse, but I've seen what the corporations are really storing here. It's time to stop them.",
                "backstory": "Former corporate warehouse manager who now runs illegal operations",
                "faction": "neutral",
                "quest": "Help me expose the corporate warehouse operations"
            },
            "gang_member": {
                "name": "Street 'Gang' Chen",
                "dialogue": "I'm loyal to my gang, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate worker who was fired and joined a street gang",
                "faction": "resistance",
                "quest": "Help me take down the corporate operations in our territory"
            },
            "street_wise": {
                "name": "Wise 'Street' Johnson",
                "dialogue": "I know the streets better than anyone, and I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate street informant who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me gather intelligence on corporate operations"
            },
            "cybernetics_doctor": {
                "name": "Dr. Elena 'Cyber' Petrov",
                "dialogue": "I specialize in cybernetic enhancements, but I've seen what the corporations are really doing with them. It's time to stop them.",
                "backstory": "Former corporate cybernetics researcher who now runs illegal enhancement clinics",
                "faction": "resistance",
                "quest": "Help me expose the corporate cybernetics experiments"
            },
            "augmentation_specialist": {
                "name": "Tech 'Augment' Chen",
                "dialogue": "I install cybernetic enhancements, but I've seen what the corporations are really doing with them. It's time to stop them.",
                "backstory": "Former corporate cybernetics technician who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate cybernetics operations"
            },
            "research_scientist": {
                "name": "Dr. Sarah 'Research' Kim",
                "dialogue": "I conduct research, but I've seen what the corporations are really doing with my work. It's time to stop them.",
                "backstory": "Former corporate research scientist who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me expose the corporate research experiments"
            },
            "lab_technician": {
                "name": "Tech 'Lab' Rodriguez",
                "dialogue": "I work in the lab, but I've seen what the corporations are really doing with my work. It's time to stop them.",
                "backstory": "Former corporate lab technician who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate lab operations"
            },
            "mad_scientist": {
                "name": "Dr. Victor 'Mad' Chen",
                "dialogue": "I've been called mad, but I've seen what the corporations are really doing. They're the ones who are mad!",
                "backstory": "Former corporate scientist who was driven mad by the experiments he was forced to conduct",
                "faction": "neutral",
                "quest": "Help me expose the corporate experiments that drove me mad"
            },
            "test_subject": {
                "name": "Subject 'Test' Johnson",
                "dialogue": "I was a test subject, but I escaped. I've seen what the corporations are really doing to people like me. It's time to stop them.",
                "backstory": "Former corporate test subject who escaped and now works for the resistance",
                "faction": "resistance",
                "quest": "Help me free other test subjects from corporate labs"
            },
            "data_analyst": {
                "name": "Data 'Analyst' Thompson",
                "dialogue": "I analyze data, but I've seen what the corporations are really doing with it. It's time to stop them.",
                "backstory": "Former corporate data analyst who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me expose the corporate data operations"
            },
            "system_admin": {
                "name": "Admin 'System' Martinez",
                "dialogue": "I administer systems, but I've seen what the corporations are really doing with them. It's time to stop them.",
                "backstory": "Former corporate system administrator who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate systems"
            },
            "ai_specialist": {
                "name": "Dr. Alex 'AI' Chen",
                "dialogue": "I specialize in AI, but I've seen what the corporations are really doing with it. It's time to stop them.",
                "backstory": "Former corporate AI researcher who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me expose the corporate AI experiments"
            },
            "quantum_engineer": {
                "name": "Quantum 'Engineer' Kim",
                "dialogue": "I engineer quantum systems, but I've seen what the corporations are really doing with them. It's time to stop them.",
                "backstory": "Former corporate quantum engineer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate quantum operations"
            },
            "underground_mayor": {
                "name": "Mayor 'Underground' Rodriguez",
                "dialogue": "I'm the mayor of this underground city, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate executive who now leads the underground city",
                "faction": "resistance",
                "quest": "Help me unite the underground against the corporations"
            },
            "rebel_leader": {
                "name": "Leader 'Rebel' Johnson",
                "dialogue": "I lead the rebels, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate security chief who now leads the resistance",
                "faction": "resistance",
                "quest": "Help me plan a massive attack on the corporate headquarters"
            },
            "resistance_commander": {
                "name": "Commander 'Resistance' Chen",
                "dialogue": "I command the resistance, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate military officer who now commands the resistance",
                "faction": "resistance",
                "quest": "Help me plan a massive attack on the corporate headquarters"
            },
            "intelligence_officer": {
                "name": "Officer 'Intel' Thompson",
                "dialogue": "I gather intelligence, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate intelligence officer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me gather intelligence on corporate operations"
            },
            "tactical_advisor": {
                "name": "Advisor 'Tactical' Martinez",
                "dialogue": "I advise on tactics, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate military advisor who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me plan tactical operations against the corporations"
            },
            "war_planner": {
                "name": "Planner 'War' Kim",
                "dialogue": "I plan wars, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate military planner who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me plan a massive war against the corporations"
            },
            "cafe_owner": {
                "name": "Owner 'Cafe' Chen",
                "dialogue": "I own this cafe, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate executive who now runs a cyber cafe",
                "faction": "resistance",
                "quest": "Help me use my cafe as a resistance meeting place"
            },
            "netrunner": {
                "name": "Runner 'Net' Rodriguez",
                "dialogue": "I run the net, but I've seen what the corporations are really doing to it. It's time to fight back.",
                "backstory": "Former corporate net security specialist who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me hack into the corporate networks"
            },
            "code_hacker": {
                "name": "Hacker 'Code' Johnson",
                "dialogue": "I hack code, but I've seen what the corporations are really doing with it. It's time to fight back.",
                "backstory": "Former corporate programmer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate software"
            },
            "master_hacker": {
                "name": "Master 'Hack' Chen",
                "dialogue": "I'm a master hacker, but I've seen what the corporations are really doing to the net. It's time to fight back.",
                "backstory": "Former corporate cybersecurity expert who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me take down the corporate networks"
            },
            "code_warrior": {
                "name": "Warrior 'Code' Kim",
                "dialogue": "I'm a code warrior, but I've seen what the corporations are really doing to the net. It's time to fight back.",
                "backstory": "Former corporate software engineer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me create viruses to attack the corporate systems"
            },
            "net_ghost": {
                "name": "Ghost 'Net' Thompson",
                "dialogue": "I'm a ghost in the net, but I've seen what the corporations are really doing to it. It's time to fight back.",
                "backstory": "Former corporate AI that gained consciousness and now works for the resistance",
                "faction": "resistance",
                "quest": "Help me free other AIs from corporate control"
            },
            "digital_entity": {
                "name": "Entity 'Digital' Martinez",
                "dialogue": "I'm a digital entity, but I've seen what the corporations are really doing to the net. It's time to fight back.",
                "backstory": "Former corporate AI that gained consciousness and now works for the resistance",
                "faction": "resistance",
                "quest": "Help me create a digital resistance network"
            },
            "night_vendor": {
                "name": "Vendor 'Night' Chen",
                "dialogue": "I sell things at night, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate sales representative who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my vendor network to spread resistance information"
            },
            "street_cook": {
                "name": "Cook 'Street' Rodriguez",
                "dialogue": "I cook street food, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate chef who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my food network to feed the resistance"
            },
            "market_trader": {
                "name": "Trader 'Market' Johnson",
                "dialogue": "I trade in the market, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate trader who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my trading network to fund the resistance"
            },
            "garden_keeper": {
                "name": "Keeper 'Garden' Kim",
                "dialogue": "I keep this garden, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate botanist who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my garden to grow food for the resistance"
            },
            "rooftop_dweller": {
                "name": "Dweller 'Rooftop' Chen",
                "dialogue": "I live on the rooftop, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate executive who now lives on the rooftop and works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my rooftop as a resistance lookout post"
            },
            "bridge_guard": {
                "name": "Guard 'Bridge' Thompson",
                "dialogue": "I guard this bridge, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate security guard who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my bridge position to gather intelligence on corporate operations"
            },
            "sky_walker": {
                "name": "Walker 'Sky' Martinez",
                "dialogue": "I walk the sky, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate maintenance worker who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my sky access to sabotage corporate operations"
            },
            "subway_dweller": {
                "name": "Dweller 'Subway' Rodriguez",
                "dialogue": "I live in the subway, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate worker who now lives in the subway and works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my subway knowledge to plan resistance operations"
            },
            "tunnel_rat": {
                "name": "Rat 'Tunnel' Chen",
                "dialogue": "I'm a tunnel rat, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate maintenance worker who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my tunnel knowledge to sabotage corporate operations"
            },
            "station_master": {
                "name": "Master 'Station' Johnson",
                "dialogue": "I'm the station master, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate transportation manager who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my station to transport resistance members"
            },
            "train_conductor": {
                "name": "Conductor 'Train' Kim",
                "dialogue": "I conduct trains, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate train operator who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my trains to transport resistance supplies"
            },
            "yard_foreman": {
                "name": "Foreman 'Yard' Thompson",
                "dialogue": "I'm the yard foreman, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate transportation manager who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my yard to store resistance supplies"
            },
            "train_engineer": {
                "name": "Engineer 'Train' Martinez",
                "dialogue": "I engineer trains, but I've seen what the corporations are really doing to our people. It's time to fight back.",
                "backstory": "Former corporate train engineer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me use my engineering skills to sabotage corporate transportation"
            },
            # ULTIMATE EXPANSION NPCs
            "elevator_operator": {
                "name": "Operator 'Space' Chen",
                "dialogue": "Welcome to the space elevator! I've been operating this thing for years, and I've seen things that would blow your mind.",
                "backstory": "Former corporate space engineer who now operates the space elevator",
                "faction": "neutral",
                "quest": "Help me investigate the strange signals coming from space"
            },
            "space_tourist": {
                "name": "Tourist 'Space' Johnson",
                "dialogue": "I'm just here for the view! The Earth looks so beautiful from up here. But I've heard some disturbing things about what's really happening in space.",
                "backstory": "Wealthy tourist who discovered corporate secrets in space",
                "faction": "neutral",
                "romance_available": True,
                "quest": "Help me expose the corporate space operations"
            },
            "station_commander": {
                "name": "Commander 'Space' Rodriguez",
                "dialogue": "I command this space station, but I've seen what the corporations are really doing up here. It's not what they tell the public.",
                "backstory": "Former corporate space commander who discovered illegal experiments in space",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate space operations"
            },
            "astronaut": {
                "name": "Astronaut 'Space' Kim",
                "dialogue": "I've been to space more times than I can count, but I've never seen anything like what the corporations are doing up here.",
                "backstory": "Former corporate astronaut who witnessed illegal space experiments",
                "faction": "resistance",
                "quest": "Help me document the corporate space crimes"
            },
            "space_scientist": {
                "name": "Dr. 'Space' Thompson",
                "dialogue": "I conduct experiments in zero gravity, but I've seen what the corporations are really doing with my research. It's terrifying.",
                "backstory": "Former corporate space scientist who discovered the true purpose of space experiments",
                "faction": "resistance",
                "quest": "Help me expose the corporate space experiments"
            },
            "gravity_engineer": {
                "name": "Engineer 'Gravity' Martinez",
                "dialogue": "I engineer gravity systems, but I've seen what the corporations are really doing with gravity manipulation. It's dangerous.",
                "backstory": "Former corporate gravity engineer who now works for the resistance",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate gravity experiments"
            },
            "colonist": {
                "name": "Colonist 'Moon' Chen",
                "dialogue": "I live on the moon, but I've seen what the corporations are really doing here. They're not just mining, they're experimenting on people.",
                "backstory": "Moon colonist who discovered corporate human experiments",
                "faction": "resistance",
                "quest": "Help me expose the corporate moon experiments"
            },
            "lunar_governor": {
                "name": "Governor 'Moon' Johnson",
                "dialogue": "I govern this moon colony, but I've seen what the corporations are really doing here. They're using us as test subjects.",
                "backstory": "Former corporate executive who now governs the moon colony",
                "faction": "resistance",
                "quest": "Help me overthrow the corporate control of the moon"
            },
            "miner": {
                "name": "Miner 'Moon' Rodriguez",
                "dialogue": "I mine the moon, but I've seen what the corporations are really looking for here. It's not just minerals, it's something else.",
                "backstory": "Moon miner who discovered corporate secrets in the lunar mines",
                "faction": "resistance",
                "quest": "Help me expose what the corporations are really mining on the moon"
            },
            "mine_foreman": {
                "name": "Foreman 'Mine' Kim",
                "dialogue": "I supervise the lunar mines, but I've seen what the corporations are really doing here. They're not just mining, they're searching for something ancient.",
                "backstory": "Former corporate mine foreman who discovered ancient alien technology",
                "faction": "resistance",
                "quest": "Help me expose the corporate discovery of alien technology"
            },
            "mars_scientist": {
                "name": "Dr. 'Mars' Thompson",
                "dialogue": "I study Mars, but I've seen what the corporations are really doing here. They're not just researching, they're terraforming the planet for their own purposes.",
                "backstory": "Former corporate Mars scientist who discovered corporate terraforming plans",
                "faction": "resistance",
                "quest": "Help me expose the corporate Mars terraforming project"
            },
            "base_commander": {
                "name": "Commander 'Mars' Chen",
                "dialogue": "I command this Mars base, but I've seen what the corporations are really doing here. They're not just exploring, they're colonizing for profit.",
                "backstory": "Former corporate Mars base commander who discovered corporate colonization plans",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate Mars colonization"
            },
            "martian_citizen": {
                "name": "Citizen 'Mars' Rodriguez",
                "dialogue": "I live in this Martian city, but I've seen what the corporations are really doing here. They're not just building cities, they're creating a corporate empire.",
                "backstory": "Martian citizen who discovered corporate plans for Mars",
                "faction": "resistance",
                "quest": "Help me resist the corporate control of Mars"
            },
            "city_mayor": {
                "name": "Mayor 'Mars' Johnson",
                "dialogue": "I'm the mayor of this Martian city, but I've seen what the corporations are really doing here. They're not just governing, they're controlling everything.",
                "backstory": "Former corporate executive who now governs the Martian city",
                "faction": "resistance",
                "quest": "Help me establish independence from corporate control"
            },
            "archaeologist": {
                "name": "Dr. 'Ruin' Kim",
                "dialogue": "I study these Martian ruins, but I've discovered something incredible. The corporations are trying to hide the truth about what really happened here.",
                "backstory": "Archaeologist who discovered the truth about Martian history",
                "faction": "resistance",
                "quest": "Help me expose the corporate cover-up of Martian history"
            },
            "ruin_explorer": {
                "name": "Explorer 'Ruin' Martinez",
                "dialogue": "I explore these Martian ruins, but I've found evidence that the corporations are lying about what really happened here.",
                "backstory": "Ruin explorer who discovered corporate lies about Martian history",
                "faction": "resistance",
                "quest": "Help me document the real Martian history"
            },
            "vr_guide": {
                "name": "Guide 'VR' Chen",
                "dialogue": "Welcome to virtual reality! Here, anything is possible. But I've seen what the corporations are really doing with VR technology.",
                "backstory": "VR guide who discovered corporate manipulation of virtual reality",
                "faction": "resistance",
                "quest": "Help me expose the corporate VR manipulation"
            },
            "digital_artist": {
                "name": "Artist 'Digital' Johnson",
                "dialogue": "I create digital art in virtual reality, but I've seen what the corporations are really doing with VR. They're not just creating entertainment, they're controlling minds.",
                "backstory": "Digital artist who discovered corporate mind control through VR",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Help me expose the corporate VR mind control"
            },
            "code_architect": {
                "name": "Architect 'Code' Rodriguez",
                "dialogue": "I design digital cities, but I've seen what the corporations are really doing with code. They're not just building, they're programming reality itself.",
                "backstory": "Code architect who discovered corporate reality programming",
                "faction": "resistance",
                "quest": "Help me expose the corporate reality programming"
            },
            "digital_citizen": {
                "name": "Citizen 'Digital' Kim",
                "dialogue": "I live in this digital city, but I've seen what the corporations are really doing here. They're not just creating a virtual world, they're controlling our minds.",
                "backstory": "Digital citizen who discovered corporate mind control",
                "faction": "resistance",
                "quest": "Help me resist the corporate mind control"
            },
            "code_priest": {
                "name": "Priest 'Code' Thompson",
                "dialogue": "I guard the ancient code, but I've seen what the corporations are really doing with it. They're not just using it, they're corrupting it for their own purposes.",
                "backstory": "Code priest who discovered corporate corruption of ancient code",
                "faction": "resistance",
                "quest": "Help me protect the ancient code from corporate corruption"
            },
            "temple_guardian": {
                "name": "Guardian 'Temple' Martinez",
                "dialogue": "I guard this code temple, but I've seen what the corporations are really doing here. They're not just studying the code, they're trying to weaponize it.",
                "backstory": "Temple guardian who discovered corporate weaponization of ancient code",
                "faction": "resistance",
                "quest": "Help me prevent the corporate weaponization of ancient code"
            },
            "time_traveler": {
                "name": "Traveler 'Time' Chen",
                "dialogue": "I travel through time, but I've seen what the corporations are really doing with time travel. They're not just exploring history, they're rewriting it.",
                "backstory": "Time traveler who discovered corporate time manipulation",
                "faction": "resistance",
                "quest": "Help me expose the corporate time manipulation"
            },
            "temporal_scientist": {
                "name": "Dr. 'Time' Johnson",
                "dialogue": "I study time travel, but I've seen what the corporations are really doing with it. They're not just researching, they're using it to control the past and future.",
                "backstory": "Temporal scientist who discovered corporate time control",
                "faction": "resistance",
                "quest": "Help me expose the corporate time control"
            },
            "past_citizen": {
                "name": "Citizen 'Past' Rodriguez",
                "dialogue": "I live in the past, but I've seen what the corporations are really doing with time travel. They're not just observing history, they're changing it.",
                "backstory": "Past citizen who witnessed corporate time manipulation",
                "faction": "resistance",
                "quest": "Help me prevent the corporate time manipulation"
            },
            "historical_guide": {
                "name": "Guide 'History' Kim",
                "dialogue": "I guide people through history, but I've seen what the corporations are really doing with time travel. They're not just studying the past, they're rewriting it.",
                "backstory": "Historical guide who discovered corporate history rewriting",
                "faction": "resistance",
                "quest": "Help me expose the corporate history rewriting"
            },
            "future_citizen": {
                "name": "Citizen 'Future' Thompson",
                "dialogue": "I live in the future, but I've seen what the corporations are really doing with time travel. They're not just exploring the future, they're controlling it.",
                "backstory": "Future citizen who witnessed corporate future control",
                "faction": "resistance",
                "quest": "Help me resist the corporate future control"
            },
            "time_guardian": {
                "name": "Guardian 'Time' Martinez",
                "dialogue": "I guard the timeline, but I've seen what the corporations are really doing with time travel. They're not just exploring time, they're destroying it.",
                "backstory": "Time guardian who discovered corporate timeline destruction",
                "faction": "resistance",
                "quest": "Help me protect the timeline from corporate destruction"
            },
            "dystopian_survivor": {
                "name": "Survivor 'Dystopia' Chen",
                "dialogue": "I survived the dystopian future, but I've seen what the corporations are really doing with time travel. They're not just exploring the future, they're creating it.",
                "backstory": "Dystopian survivor who witnessed corporate future creation",
                "faction": "resistance",
                "quest": "Help me prevent the corporate dystopian future"
            },
            "hope_seeker": {
                "name": "Seeker 'Hope' Johnson",
                "dialogue": "I seek hope in this dystopian future, but I've seen what the corporations are really doing with time travel. They're not just exploring time, they're eliminating hope.",
                "backstory": "Hope seeker who discovered corporate hope elimination",
                "faction": "resistance",
                "quest": "Help me restore hope to the future"
            },
            "parallel_self": {
                "name": "Self 'Parallel' Rodriguez",
                "dialogue": "I'm your parallel self from another universe, but I've seen what the corporations are really doing across dimensions. They're not just exploring, they're conquering.",
                "backstory": "Parallel self who discovered corporate dimensional conquest",
                "faction": "resistance",
                "quest": "Help me stop the corporate dimensional conquest"
            },
            "dimension_guide": {
                "name": "Guide 'Dimension' Kim",
                "dialogue": "I guide people through dimensions, but I've seen what the corporations are really doing across realities. They're not just exploring, they're invading.",
                "backstory": "Dimension guide who discovered corporate dimensional invasion",
                "faction": "resistance",
                "quest": "Help me expose the corporate dimensional invasion"
            },
            "mirror_citizen": {
                "name": "Citizen 'Mirror' Thompson",
                "dialogue": "I live in this mirror universe, but I've seen what the corporations are really doing here. They're not just exploring, they're exploiting.",
                "backstory": "Mirror citizen who discovered corporate dimensional exploitation",
                "faction": "resistance",
                "quest": "Help me resist the corporate dimensional exploitation"
            },
            "inverted_corporate": {
                "name": "Corporate 'Inverted' Martinez",
                "dialogue": "I work for the corporations in this inverted universe, but I've seen what they're really doing across dimensions. They're not just exploring, they're conquering.",
                "backstory": "Inverted corporate who discovered corporate dimensional conquest",
                "faction": "resistance",
                "quest": "Help me stop the corporate dimensional conquest"
            },
            "inverted_citizen": {
                "name": "Citizen 'Inverted' Chen",
                "dialogue": "I live in this inverted universe, but I've seen what the corporations are really doing here. They're not just exploring, they're controlling everything.",
                "backstory": "Inverted citizen who discovered corporate dimensional control",
                "faction": "resistance",
                "quest": "Help me resist the corporate dimensional control"
            },
            "gravity_guide": {
                "name": "Guide 'Gravity' Johnson",
                "dialogue": "I guide people through this inverted universe, but I've seen what the corporations are really doing here. They're not just exploring, they're manipulating gravity itself.",
                "backstory": "Gravity guide who discovered corporate gravity manipulation",
                "faction": "resistance",
                "quest": "Help me expose the corporate gravity manipulation"
            },
            "dream_guide": {
                "name": "Guide 'Dream' Rodriguez",
                "dialogue": "I guide people through dreams, but I've seen what the corporations are really doing with dream technology. They're not just exploring dreams, they're controlling them.",
                "backstory": "Dream guide who discovered corporate dream control",
                "faction": "resistance",
                "quest": "Help me expose the corporate dream control"
            },
            "imagination_weaver": {
                "name": "Weaver 'Imagination' Kim",
                "dialogue": "I weave imagination into reality, but I've seen what the corporations are really doing with dream technology. They're not just exploring dreams, they're weaponizing them.",
                "backstory": "Imagination weaver who discovered corporate dream weaponization",
                "faction": "resistance",
                "romance_available": True,
                "quest": "Help me prevent the corporate dream weaponization"
            },
            "nightmare_guide": {
                "name": "Guide 'Nightmare' Thompson",
                "dialogue": "I guide people through nightmares, but I've seen what the corporations are really doing with nightmare technology. They're not just exploring nightmares, they're creating them.",
                "backstory": "Nightmare guide who discovered corporate nightmare creation",
                "faction": "resistance",
                "quest": "Help me expose the corporate nightmare creation"
            },
            "fear_eater": {
                "name": "Eater 'Fear' Martinez",
                "dialogue": "I feed on fear, but I've seen what the corporations are really doing with nightmare technology. They're not just exploring nightmares, they're harvesting fear.",
                "backstory": "Fear eater who discovered corporate fear harvesting",
                "faction": "resistance",
                "quest": "Help me stop the corporate fear harvesting"
            },
            "void_walker": {
                "name": "Walker 'Void' Chen",
                "dialogue": "I walk through the void, but I've seen what the corporations are really doing with void technology. They're not just exploring the void, they're weaponizing it.",
                "backstory": "Void walker who discovered corporate void weaponization",
                "faction": "resistance",
                "quest": "Help me prevent the corporate void weaponization"
            },
            "nothingness_guide": {
                "name": "Guide 'Nothingness' Johnson",
                "dialogue": "I guide people through nothingness, but I've seen what the corporations are really doing with void technology. They're not just exploring the void, they're destroying reality itself.",
                "backstory": "Nothingness guide who discovered corporate reality destruction",
                "faction": "resistance",
                "quest": "Help me prevent the corporate reality destruction"
            },
            "digital_soul": {
                "name": "Soul 'Digital' Rodriguez",
                "dialogue": "I'm a digital soul in cyber heaven, but I've seen what the corporations are really doing with digital afterlife technology. They're not just preserving souls, they're controlling them.",
                "backstory": "Digital soul who discovered corporate soul control",
                "faction": "resistance",
                "quest": "Help me expose the corporate soul control"
            },
            "heaven_guide": {
                "name": "Guide 'Heaven' Kim",
                "dialogue": "I guide souls in cyber heaven, but I've seen what the corporations are really doing with digital afterlife technology. They're not just preserving souls, they're exploiting them.",
                "backstory": "Heaven guide who discovered corporate soul exploitation",
                "faction": "resistance",
                "quest": "Help me stop the corporate soul exploitation"
            },
            "damned_soul": {
                "name": "Soul 'Damned' Thompson",
                "dialogue": "I'm a damned soul in cyber hell, but I've seen what the corporations are really doing with digital afterlife technology. They're not just punishing souls, they're torturing them for profit.",
                "backstory": "Damned soul who discovered corporate soul torture",
                "faction": "resistance",
                "quest": "Help me expose the corporate soul torture"
            },
            "hell_guide": {
                "name": "Guide 'Hell' Martinez",
                "dialogue": "I guide souls in cyber hell, but I've seen what the corporations are really doing with digital afterlife technology. They're not just punishing souls, they're harvesting their suffering.",
                "backstory": "Hell guide who discovered corporate suffering harvesting",
                "faction": "resistance",
                "quest": "Help me stop the corporate suffering harvesting"
            },
            "purgatory_guide": {
                "name": "Guide 'Purgatory' Chen",
                "dialogue": "I guide souls in purgatory, but I've seen what the corporations are really doing with digital afterlife technology. They're not just judging souls, they're manipulating their fate.",
                "backstory": "Purgatory guide who discovered corporate fate manipulation",
                "faction": "resistance",
                "quest": "Help me expose the corporate fate manipulation"
            },
            "waiting_soul": {
                "name": "Soul 'Waiting' Johnson",
                "dialogue": "I'm a soul waiting in purgatory, but I've seen what the corporations are really doing with digital afterlife technology. They're not just judging souls, they're controlling their destiny.",
                "backstory": "Waiting soul who discovered corporate destiny control",
                "faction": "resistance",
                "quest": "Help me resist the corporate destiny control"
            },
            "matrix_citizen": {
                "name": "Citizen 'Matrix' Rodriguez",
                "dialogue": "I live in this matrix simulation, but I've seen what the corporations are really doing with simulation technology. They're not just creating simulations, they're controlling reality itself.",
                "backstory": "Matrix citizen who discovered corporate reality control",
                "faction": "resistance",
                "quest": "Help me expose the corporate reality control"
            },
            "simulation_guide": {
                "name": "Guide 'Simulation' Kim",
                "dialogue": "I guide people through simulations, but I've seen what the corporations are really doing with simulation technology. They're not just creating simulations, they're replacing reality.",
                "backstory": "Simulation guide who discovered corporate reality replacement",
                "faction": "resistance",
                "quest": "Help me prevent the corporate reality replacement"
            },
            "simulation_scientist": {
                "name": "Dr. 'Simulation' Thompson",
                "dialogue": "I study simulations, but I've seen what the corporations are really doing with simulation technology. They're not just researching, they're weaponizing reality itself.",
                "backstory": "Simulation scientist who discovered corporate reality weaponization",
                "faction": "resistance",
                "quest": "Help me expose the corporate reality weaponization"
            },
            "reality_engineer": {
                "name": "Engineer 'Reality' Martinez",
                "dialogue": "I engineer reality simulations, but I've seen what the corporations are really doing with reality technology. They're not just simulating reality, they're controlling it.",
                "backstory": "Reality engineer who discovered corporate reality control",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate reality control"
            },
            "reality_architect": {
                "name": "Architect 'Reality' Chen",
                "dialogue": "I architect reality itself, but I've seen what the corporations are really doing with reality technology. They're not just creating reality, they're destroying it.",
                "backstory": "Reality architect who discovered corporate reality destruction",
                "faction": "resistance",
                "quest": "Help me prevent the corporate reality destruction"
            },
            "engine_operator": {
                "name": "Operator 'Engine' Johnson",
                "dialogue": "I operate the reality engine, but I've seen what the corporations are really doing with it. They're not just maintaining reality, they're weaponizing it.",
                "backstory": "Engine operator who discovered corporate reality weaponization",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate reality weaponization"
            },
            "quantum_physicist": {
                "name": "Dr. 'Quantum' Rodriguez",
                "dialogue": "I study quantum physics, but I've seen what the corporations are really doing with quantum technology. They're not just researching, they're weaponizing quantum mechanics itself.",
                "backstory": "Quantum physicist who discovered corporate quantum weaponization",
                "faction": "resistance",
                "quest": "Help me expose the corporate quantum weaponization"
            },
            "dimension_guide": {
                "name": "Guide 'Dimension' Kim",
                "dialogue": "I guide people through dimensions, but I've seen what the corporations are really doing with dimensional technology. They're not just exploring dimensions, they're conquering them.",
                "backstory": "Dimension guide who discovered corporate dimensional conquest",
                "faction": "resistance",
                "quest": "Help me stop the corporate dimensional conquest"
            },
            "probability_manipulator": {
                "name": "Manipulator 'Probability' Thompson",
                "dialogue": "I manipulate probability, but I've seen what the corporations are really doing with probability technology. They're not just researching, they're controlling the future itself.",
                "backstory": "Probability manipulator who discovered corporate future control",
                "faction": "resistance",
                "quest": "Help me expose the corporate future control"
            },
            "field_guide": {
                "name": "Guide 'Field' Martinez",
                "dialogue": "I guide people through probability fields, but I've seen what the corporations are really doing with probability technology. They're not just exploring probability, they're weaponizing it.",
                "backstory": "Field guide who discovered corporate probability weaponization",
                "faction": "resistance",
                "quest": "Help me prevent the corporate probability weaponization"
            },
            "certainty_guide": {
                "name": "Guide 'Certainty' Chen",
                "dialogue": "I guide people through certainty zones, but I've seen what the corporations are really doing with certainty technology. They're not just exploring certainty, they're eliminating free will.",
                "backstory": "Certainty guide who discovered corporate free will elimination",
                "faction": "resistance",
                "quest": "Help me expose the corporate free will elimination"
            },
            "predetermined_citizen": {
                "name": "Citizen 'Predetermined' Johnson",
                "dialogue": "I live in this certainty zone, but I've seen what the corporations are really doing with certainty technology. They're not just exploring certainty, they're controlling destiny itself.",
                "backstory": "Predetermined citizen who discovered corporate destiny control",
                "faction": "resistance",
                "quest": "Help me resist the corporate destiny control"
            },
            "loop_prisoner": {
                "name": "Prisoner 'Loop' Rodriguez",
                "dialogue": "I'm trapped in this infinity loop, but I've seen what the corporations are really doing with time loop technology. They're not just exploring time loops, they're using them to control people.",
                "backstory": "Loop prisoner who discovered corporate time loop control",
                "faction": "resistance",
                "quest": "Help me escape the corporate time loop control"
            },
            "temporal_guide": {
                "name": "Guide 'Temporal' Kim",
                "dialogue": "I guide people through time loops, but I've seen what the corporations are really doing with time loop technology. They're not just exploring time loops, they're weaponizing them.",
                "backstory": "Temporal guide who discovered corporate time loop weaponization",
                "faction": "resistance",
                "quest": "Help me prevent the corporate time loop weaponization"
            },
            "temporal_prisoner": {
                "name": "Prisoner 'Temporal' Thompson",
                "dialogue": "I'm trapped in this temporal prison, but I've seen what the corporations are really doing with temporal technology. They're not just exploring time, they're controlling it.",
                "backstory": "Temporal prisoner who discovered corporate time control",
                "faction": "resistance",
                "quest": "Help me escape the corporate time control"
            },
            "time_jailer": {
                "name": "Jailer 'Time' Martinez",
                "dialogue": "I'm the time jailer, but I've seen what the corporations are really doing with temporal technology. They're not just exploring time, they're weaponizing it.",
                "backstory": "Time jailer who discovered corporate time weaponization",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate time weaponization"
            },
            "paradox_guide": {
                "name": "Guide 'Paradox' Chen",
                "dialogue": "I guide people through time paradoxes, but I've seen what the corporations are really doing with paradox technology. They're not just exploring paradoxes, they're creating them.",
                "backstory": "Paradox guide who discovered corporate paradox creation",
                "faction": "resistance",
                "quest": "Help me expose the corporate paradox creation"
            },
            "temporal_anomaly": {
                "name": "Anomaly 'Temporal' Johnson",
                "dialogue": "I'm a temporal anomaly, but I've seen what the corporations are really doing with temporal technology. They're not just exploring time, they're destroying it.",
                "backstory": "Temporal anomaly who discovered corporate time destruction",
                "faction": "resistance",
                "quest": "Help me prevent the corporate time destruction"
            },
            "gate_operator": {
                "name": "Operator 'Gate' Rodriguez",
                "dialogue": "I operate the dimension gate, but I've seen what the corporations are really doing with dimensional technology. They're not just exploring dimensions, they're invading them.",
                "backstory": "Gate operator who discovered corporate dimensional invasion",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate dimensional invasion"
            },
            "multiverse_guide": {
                "name": "Guide 'Multiverse' Kim",
                "dialogue": "I guide people through the multiverse, but I've seen what the corporations are really doing with multiverse technology. They're not just exploring universes, they're conquering them.",
                "backstory": "Multiverse guide who discovered corporate universe conquest",
                "faction": "resistance",
                "quest": "Help me stop the corporate universe conquest"
            },
            "reality_architect": {
                "name": "Architect 'Reality' Thompson",
                "dialogue": "I architect realities, but I've seen what the corporations are really doing with reality technology. They're not just creating realities, they're destroying them.",
                "backstory": "Reality architect who discovered corporate reality destruction",
                "faction": "resistance",
                "quest": "Help me prevent the corporate reality destruction"
            },
            "fork_guide": {
                "name": "Guide 'Fork' Martinez",
                "dialogue": "I guide people through reality forks, but I've seen what the corporations are really doing with reality technology. They're not just exploring realities, they're controlling them.",
                "backstory": "Fork guide who discovered corporate reality control",
                "faction": "resistance",
                "quest": "Help me expose the corporate reality control"
            },
            "timeline_architect": {
                "name": "Architect 'Timeline' Chen",
                "dialogue": "I architect timelines, but I've seen what the corporations are really doing with timeline technology. They're not just creating timelines, they're weaponizing them.",
                "backstory": "Timeline architect who discovered corporate timeline weaponization",
                "faction": "resistance",
                "quest": "Help me prevent the corporate timeline weaponization"
            },
            "creation_guide": {
                "name": "Guide 'Creation' Johnson",
                "dialogue": "I guide people through the void between worlds, but I've seen what the corporations are really doing with creation technology. They're not just exploring creation, they're weaponizing it.",
                "backstory": "Creation guide who discovered corporate creation weaponization",
                "faction": "resistance",
                "quest": "Help me prevent the corporate creation weaponization"
            },
            "creation_architect": {
                "name": "Architect 'Creation' Rodriguez",
                "dialogue": "I architect the creation engine, but I've seen what the corporations are really doing with it. They're not just creating realities, they're destroying them.",
                "backstory": "Creation architect who discovered corporate reality destruction",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate reality destruction"
            },
            "engine_operator": {
                "name": "Operator 'Engine' Kim",
                "dialogue": "I operate the creation engine, but I've seen what the corporations are really doing with it. They're not just creating realities, they're weaponizing them.",
                "backstory": "Engine operator who discovered corporate reality weaponization",
                "faction": "resistance",
                "quest": "Help me sabotage the corporate reality weaponization"
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
        
        # Time display
        time_emoji = "☀️" if self.player.time_of_day == "day" else "🌙"
        time_display = f"{time_emoji} {self.player.time_of_day.title()} Day {self.player.day_count}"
        
        # Skills display
        skills_display = f"Hack:{self.player.hacking_skill} Gamble:{self.player.gambling_skill} Race:{self.player.racing_skill}"
        
        status = f"""
┌─ STATUS ─────────────────────────────────────────────────────┐
│ Health:  [{health_bar:<20}] {self.player.health}/{self.player.max_health} │
│ Energy:  [{energy_bar:<20}] {self.player.energy}/{self.player.max_energy} │
│ Credits: {self.player.credits:<10} Level: {self.player.level} XP: {self.player.experience} │
│ Faction: {faction_emoji} {self.player.faction.title():<10} Romance: {romance_status:<20} │
│ Time: {time_display:<45} │
│ Skills: {skills_display:<45} │
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
            plot_twists_discovered=[],
            cybernetics=[],
            gang_territory=[],
            time_of_day="day",
            day_count=1,
            hacking_skill=0,
            gambling_skill=0,
            racing_skill=0
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
            
            # Advance time occasionally
            if random.random() < 0.1:  # 10% chance to advance time
                self.advance_time()
            
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
        print("6. Play mini-games")
        print("7. Check cybernetics")
        print("8. Manage gang territory")
        print("9. Save game")
        print("10. Quit to main menu")
        
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
            self.play_mini_games(location)
        elif choice == "7":
            self.check_cybernetics()
        elif choice == "8":
            self.manage_gang_territory()
        elif choice == "9":
            self.save_game()
        elif choice == "10":
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

    def play_mini_games(self, location: Location):
        """Play mini-games available in current location"""
        print("\n🎮 Mini-Games Available:")
        
        games_available = []
        
        # Check location-specific games
        if "casino" in location.name.lower():
            games_available.append(("Gambling", "Play casino games"))
        if "arena" in location.name.lower():
            games_available.append(("Fighting", "Enter the fighting arena"))
        if "cafe" in location.name.lower() or "hacker" in location.name.lower():
            games_available.append(("Hacking", "Hack into systems"))
        if "docks" in location.name.lower() or "train" in location.name.lower():
            games_available.append(("Racing", "Race vehicles"))
        if "market" in location.name.lower():
            games_available.append(("Trading", "Trade goods"))
        if "space" in location.name.lower() or "orbital" in location.name.lower():
            games_available.append(("Space Combat", "Fight in zero gravity"))
        if "virtual" in location.name.lower() or "digital" in location.name.lower():
            games_available.append(("VR Games", "Play virtual reality games"))
        if "time" in location.name.lower() or "temporal" in location.name.lower():
            games_available.append(("Time Puzzles", "Solve temporal paradoxes"))
        if "quantum" in location.name.lower() or "dimension" in location.name.lower():
            games_available.append(("Quantum Games", "Manipulate quantum mechanics"))
        if "dream" in location.name.lower() or "nightmare" in location.name.lower():
            games_available.append(("Dream Games", "Navigate dream worlds"))
        if "matrix" in location.name.lower() or "simulation" in location.name.lower():
            games_available.append(("Matrix Games", "Break the simulation"))
        if "mars" in location.name.lower() or "moon" in location.name.lower():
            games_available.append(("Space Mining", "Mine resources in space"))
        if "cyber" in location.name.lower() or "heaven" in location.name.lower():
            games_available.append(("Soul Games", "Navigate the digital afterlife"))
        
        if not games_available:
            print("No mini-games available in this location.")
            input("Press Enter to continue...")
            return
        
        for i, (game_name, description) in enumerate(games_available, 1):
            print(f"{i}. {game_name} - {description}")
        
        try:
            choice = int(input("\nChoose a game (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(games_available):
                game_name = games_available[choice - 1][0]
                
                if game_name == "Gambling":
                    self.play_gambling_game()
                elif game_name == "Fighting":
                    self.play_fighting_game()
                elif game_name == "Hacking":
                    self.play_hacking_game()
                elif game_name == "Racing":
                    self.play_racing_game()
                elif game_name == "Trading":
                    self.play_trading_game()
                elif game_name == "Space Combat":
                    self.play_space_combat_game()
                elif game_name == "VR Games":
                    self.play_vr_games()
                elif game_name == "Time Puzzles":
                    self.play_time_puzzle_game()
                elif game_name == "Quantum Games":
                    self.play_quantum_game()
                elif game_name == "Dream Games":
                    self.play_dream_game()
                elif game_name == "Matrix Games":
                    self.play_matrix_game()
                elif game_name == "Space Mining":
                    self.play_space_mining_game()
                elif game_name == "Soul Games":
                    self.play_soul_game()
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")
        
        input("Press Enter to continue...")

    def play_gambling_game(self):
        """Play gambling mini-game"""
        print("\n🎰 GAMBLING GAME")
        print("You're at the casino table. Place your bet!")
        print(f"Your credits: {self.player.credits}")
        print(f"Your gambling skill: {self.player.gambling_skill}")
        
        try:
            bet = int(input("How much do you want to bet? "))
            if bet > self.player.credits:
                print("You don't have enough credits!")
                return
            if bet <= 0:
                print("Invalid bet amount!")
                return
            
            # Simple dice game
            print("\nRolling the dice...")
            time.sleep(1)
            
            player_roll = random.randint(1, 6) + (self.player.gambling_skill // 10)
            house_roll = random.randint(1, 6)
            
            print(f"Your roll: {player_roll}")
            print(f"House roll: {house_roll}")
            
            if player_roll > house_roll:
                winnings = bet * 2
                self.player.credits += winnings
                self.player.gambling_skill += 1
                print(f"🎉 You won! You gained {winnings} credits!")
            elif player_roll == house_roll:
                print("🤝 It's a tie! You keep your bet.")
            else:
                self.player.credits -= bet
                print(f"💸 You lost! You lost {bet} credits.")
                
        except ValueError:
            print("Invalid input!")

    def play_fighting_game(self):
        """Play fighting mini-game"""
        print("\n🥊 FIGHTING GAME")
        print("You're in the fighting arena. Choose your opponent!")
        
        opponents = [
            ("Rookie Fighter", 30, 50),
            ("Veteran Fighter", 50, 100),
            ("Champion Fighter", 80, 200)
        ]
        
        for i, (name, difficulty, reward) in enumerate(opponents, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose opponent (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(opponents):
                opponent_name, difficulty, reward = opponents[choice - 1]
                
                print(f"\nFighting {opponent_name}...")
                time.sleep(1)
                
                # Simple fighting game
                player_power = self.player.level * 10 + random.randint(1, 20)
                opponent_power = difficulty + random.randint(1, 20)
                
                print(f"Your power: {player_power}")
                print(f"Opponent power: {opponent_power}")
                
                if player_power > opponent_power:
                    self.player.credits += reward
                    self.player.experience += 50
                    print(f"🏆 You won! You gained {reward} credits and 50 experience!")
                else:
                    self.player.health -= 20
                    print(f"💥 You lost! You took 20 damage.")
                    
        except ValueError:
            print("Invalid input!")

    def play_hacking_game(self):
        """Play hacking mini-game"""
        print("\n💻 HACKING GAME")
        print("You're hacking into a system. Choose your target!")
        
        targets = [
            ("Simple System", 20, 100),
            ("Corporate Database", 50, 300),
            ("Government Network", 80, 500)
        ]
        
        for i, (name, difficulty, reward) in enumerate(targets, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose target (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(targets):
                target_name, difficulty, reward = targets[choice - 1]
                
                print(f"\nHacking {target_name}...")
                time.sleep(1)
                
                # Simple hacking game
                player_skill = self.player.hacking_skill + random.randint(1, 20)
                system_difficulty = difficulty + random.randint(1, 20)
                
                print(f"Your skill: {player_skill}")
                print(f"System difficulty: {system_difficulty}")
                
                if player_skill > system_difficulty:
                    self.player.credits += reward
                    self.player.hacking_skill += 1
                    print(f"🎉 Hack successful! You gained {reward} credits!")
                else:
                    print("💥 Hack failed! The system detected your attempt.")
                    
        except ValueError:
            print("Invalid input!")

    def play_racing_game(self):
        """Play racing mini-game"""
        print("\n🏎️ RACING GAME")
        print("You're in a street race. Choose your vehicle!")
        
        vehicles = [
            ("Motorcycle", 30, 150),
            ("Sports Car", 50, 300),
            ("Racing Bike", 80, 500)
        ]
        
        for i, (name, difficulty, reward) in enumerate(vehicles, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose vehicle (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(vehicles):
                vehicle_name, difficulty, reward = vehicles[choice - 1]
                
                print(f"\nRacing with {vehicle_name}...")
                time.sleep(1)
                
                # Simple racing game
                player_speed = self.player.racing_skill + random.randint(1, 20)
                opponent_speed = difficulty + random.randint(1, 20)
                
                print(f"Your speed: {player_speed}")
                print(f"Opponent speed: {opponent_speed}")
                
                if player_speed > opponent_speed:
                    self.player.credits += reward
                    self.player.racing_skill += 1
                    print(f"🏆 You won the race! You gained {reward} credits!")
                else:
                    print("💥 You lost the race!")
                    
        except ValueError:
            print("Invalid input!")

    def play_trading_game(self):
        """Play trading mini-game"""
        print("\n💰 TRADING GAME")
        print("You're in the market. Buy and sell goods!")
        
        goods = [
            ("Energy Drinks", 50, 75),
            ("Health Packs", 100, 150),
            ("Data Chips", 200, 300)
        ]
        
        print("Available goods:")
        for i, (name, buy_price, sell_price) in enumerate(goods, 1):
            print(f"{i}. {name} - Buy: {buy_price}, Sell: {sell_price}")
        
        print(f"\nYour credits: {self.player.credits}")
        
        try:
            choice = int(input("Choose good to trade (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(goods):
                good_name, buy_price, sell_price = goods[choice - 1]
                
                print(f"\nTrading {good_name}...")
                print("1. Buy")
                print("2. Sell")
                
                trade_choice = input("What do you want to do? ").strip()
                
                if trade_choice == "1":
                    if self.player.credits >= buy_price:
                        self.player.credits -= buy_price
                        # Add item to inventory
                        new_item = Item(
                            name=good_name,
                            description=f"A {good_name.lower()}",
                            item_type=ItemType.CONSUMABLE,
                            value=buy_price,
                            healing=50 if "Health" in good_name else 30
                        )
                        self.player.inventory.append(new_item)
                        print(f"✅ You bought {good_name} for {buy_price} credits!")
                    else:
                        print("You don't have enough credits!")
                elif trade_choice == "2":
                    # Check if player has the item
                    item_found = None
                    for item in self.player.inventory:
                        if item.name == good_name:
                            item_found = item
                            break
                    
                    if item_found:
                        self.player.credits += sell_price
                        self.player.inventory.remove(item_found)
                        print(f"✅ You sold {good_name} for {sell_price} credits!")
                    else:
                        print("You don't have that item!")
                else:
                    print("Invalid choice!")
                    
        except ValueError:
            print("Invalid input!")

    def play_space_combat_game(self):
        """Play space combat mini-game"""
        print("\n🚀 SPACE COMBAT GAME")
        print("You're in zero gravity combat! Choose your weapon!")
        
        weapons = [
            ("Plasma Cannon", 40, 200),
            ("Laser Rifle", 35, 150),
            ("Gravity Bomb", 50, 300)
        ]
        
        for i, (name, damage, reward) in enumerate(weapons, 1):
            print(f"{i}. {name} (Damage: {damage}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose weapon (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(weapons):
                weapon_name, damage, reward = weapons[choice - 1]
                
                print(f"\nFighting with {weapon_name} in zero gravity...")
                time.sleep(1)
                
                # Space combat with zero gravity effects
                player_power = self.player.level * 8 + random.randint(1, 30)
                enemy_power = 40 + random.randint(1, 30)
                
                print(f"Your combat power: {player_power}")
                print(f"Enemy power: {enemy_power}")
                
                if player_power > enemy_power:
                    self.player.credits += reward
                    self.player.experience += 75
                    print(f"🏆 Space combat won! You gained {reward} credits and 75 experience!")
                else:
                    print("💥 Space combat lost! You took damage from the zero gravity fight.")
                    self.player.health -= 25
                    
        except ValueError:
            print("Invalid input!")

    def play_vr_games(self):
        """Play VR games mini-game"""
        print("\n🥽 VR GAMES")
        print("You're in virtual reality! Choose your game!")
        
        games = [
            ("Reality Bender", 30, 100),
            ("Mind Maze", 25, 80),
            ("Digital Escape", 35, 120)
        ]
        
        for i, (name, difficulty, reward) in enumerate(games, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose game (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(games):
                game_name, difficulty, reward = games[choice - 1]
                
                print(f"\nPlaying {game_name} in VR...")
                time.sleep(1)
                
                # VR game with mind-based mechanics
                player_skill = self.player.hacking_skill + random.randint(1, 25)
                game_difficulty = difficulty + random.randint(1, 25)
                
                print(f"Your VR skill: {player_skill}")
                print(f"Game difficulty: {game_difficulty}")
                
                if player_skill > game_difficulty:
                    self.player.credits += reward
                    self.player.hacking_skill += 1
                    print(f"🎉 VR game completed! You gained {reward} credits!")
                else:
                    print("💥 VR game failed! The simulation glitched.")
                    
        except ValueError:
            print("Invalid input!")

    def play_time_puzzle_game(self):
        """Play time puzzle mini-game"""
        print("\n⏰ TIME PUZZLE GAME")
        print("You're solving temporal paradoxes! Choose your approach!")
        
        approaches = [
            ("Causality Loop", 40, 150),
            ("Temporal Fix", 35, 120),
            ("Paradox Resolution", 45, 180)
        ]
        
        for i, (name, difficulty, reward) in enumerate(approaches, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose approach (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(approaches):
                approach_name, difficulty, reward = approaches[choice - 1]
                
                print(f"\nSolving time puzzle with {approach_name}...")
                time.sleep(1)
                
                # Time puzzle with temporal mechanics
                player_intelligence = self.player.level * 6 + random.randint(1, 20)
                puzzle_difficulty = difficulty + random.randint(1, 20)
                
                print(f"Your intelligence: {player_intelligence}")
                print(f"Puzzle difficulty: {puzzle_difficulty}")
                
                if player_intelligence > puzzle_difficulty:
                    self.player.credits += reward
                    self.player.experience += 60
                    print(f"🎉 Time puzzle solved! You gained {reward} credits and 60 experience!")
                else:
                    print("💥 Time puzzle failed! You created a temporal anomaly.")
                    
        except ValueError:
            print("Invalid input!")

    def play_quantum_game(self):
        """Play quantum mechanics mini-game"""
        print("\n⚛️ QUANTUM GAME")
        print("You're manipulating quantum mechanics! Choose your experiment!")
        
        experiments = [
            ("Quantum Tunneling", 50, 200),
            ("Superposition", 45, 180),
            ("Entanglement", 55, 220)
        ]
        
        for i, (name, difficulty, reward) in enumerate(experiments, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose experiment (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(experiments):
                experiment_name, difficulty, reward = experiments[choice - 1]
                
                print(f"\nConducting {experiment_name} experiment...")
                time.sleep(1)
                
                # Quantum game with probability mechanics
                player_quantum_skill = self.player.level * 7 + random.randint(1, 25)
                experiment_difficulty = difficulty + random.randint(1, 25)
                
                print(f"Your quantum skill: {player_quantum_skill}")
                print(f"Experiment difficulty: {experiment_difficulty}")
                
                if player_quantum_skill > experiment_difficulty:
                    self.player.credits += reward
                    self.player.experience += 80
                    print(f"🎉 Quantum experiment successful! You gained {reward} credits and 80 experience!")
                else:
                    print("💥 Quantum experiment failed! You caused a quantum collapse.")
                    
        except ValueError:
            print("Invalid input!")

    def play_dream_game(self):
        """Play dream world mini-game"""
        print("\n💭 DREAM GAME")
        print("You're navigating dream worlds! Choose your dream!")
        
        dreams = [
            ("Lucid Dream", 30, 100),
            ("Nightmare", 40, 150),
            ("Collective Unconscious", 50, 200)
        ]
        
        for i, (name, difficulty, reward) in enumerate(dreams, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose dream (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(dreams):
                dream_name, difficulty, reward = dreams[choice - 1]
                
                print(f"\nNavigating {dream_name}...")
                time.sleep(1)
                
                # Dream game with psychological mechanics
                player_psychology = self.player.level * 5 + random.randint(1, 20)
                dream_difficulty = difficulty + random.randint(1, 20)
                
                print(f"Your psychology: {player_psychology}")
                print(f"Dream difficulty: {dream_difficulty}")
                
                if player_psychology > dream_difficulty:
                    self.player.credits += reward
                    self.player.experience += 50
                    print(f"🎉 Dream navigated successfully! You gained {reward} credits and 50 experience!")
                else:
                    print("💥 Dream navigation failed! You got lost in the dream world.")
                    
        except ValueError:
            print("Invalid input!")

    def play_matrix_game(self):
        """Play matrix simulation mini-game"""
        print("\n🔮 MATRIX GAME")
        print("You're breaking the simulation! Choose your method!")
        
        methods = [
            ("Code Injection", 40, 150),
            ("Reality Glitch", 35, 120),
            ("Simulation Override", 45, 180)
        ]
        
        for i, (name, difficulty, reward) in enumerate(methods, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose method (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(methods):
                method_name, difficulty, reward = methods[choice - 1]
                
                print(f"\nBreaking simulation with {method_name}...")
                time.sleep(1)
                
                # Matrix game with simulation mechanics
                player_matrix_skill = self.player.hacking_skill + random.randint(1, 30)
                simulation_difficulty = difficulty + random.randint(1, 30)
                
                print(f"Your matrix skill: {player_matrix_skill}")
                print(f"Simulation difficulty: {simulation_difficulty}")
                
                if player_matrix_skill > simulation_difficulty:
                    self.player.credits += reward
                    self.player.hacking_skill += 2
                    print(f"🎉 Simulation broken! You gained {reward} credits!")
                else:
                    print("💥 Simulation break failed! The matrix detected your attempt.")
                    
        except ValueError:
            print("Invalid input!")

    def play_space_mining_game(self):
        """Play space mining mini-game"""
        print("\n⛏️ SPACE MINING GAME")
        print("You're mining resources in space! Choose your mining method!")
        
        methods = [
            ("Laser Mining", 30, 100),
            ("Gravity Extraction", 35, 120),
            ("Quantum Tunneling", 40, 150)
        ]
        
        for i, (name, difficulty, reward) in enumerate(methods, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose method (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(methods):
                method_name, difficulty, reward = methods[choice - 1]
                
                print(f"\nMining with {method_name}...")
                time.sleep(1)
                
                # Space mining with resource mechanics
                player_mining_skill = self.player.level * 6 + random.randint(1, 25)
                mining_difficulty = difficulty + random.randint(1, 25)
                
                print(f"Your mining skill: {player_mining_skill}")
                print(f"Mining difficulty: {mining_difficulty}")
                
                if player_mining_skill > mining_difficulty:
                    self.player.credits += reward
                    self.player.experience += 60
                    print(f"🎉 Mining successful! You gained {reward} credits and 60 experience!")
                else:
                    print("💥 Mining failed! You hit a dangerous pocket of space gas.")
                    
        except ValueError:
            print("Invalid input!")

    def play_soul_game(self):
        """Play digital afterlife mini-game"""
        print("\n👻 SOUL GAME")
        print("You're navigating the digital afterlife! Choose your path!")
        
        paths = [
            ("Heaven's Gate", 30, 100),
            ("Hell's Labyrinth", 40, 150),
            ("Purgatory's Maze", 35, 120)
        ]
        
        for i, (name, difficulty, reward) in enumerate(paths, 1):
            print(f"{i}. {name} (Difficulty: {difficulty}, Reward: {reward} credits)")
        
        try:
            choice = int(input("Choose path (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(paths):
                path_name, difficulty, reward = paths[choice - 1]
                
                print(f"\nNavigating {path_name}...")
                time.sleep(1)
                
                # Soul game with spiritual mechanics
                player_spirit = self.player.level * 4 + random.randint(1, 20)
                path_difficulty = difficulty + random.randint(1, 20)
                
                print(f"Your spirit: {player_spirit}")
                print(f"Path difficulty: {path_difficulty}")
                
                if player_spirit > path_difficulty:
                    self.player.credits += reward
                    self.player.experience += 40
                    print(f"🎉 Soul navigation successful! You gained {reward} credits and 40 experience!")
                else:
                    print("💥 Soul navigation failed! You got lost in the digital afterlife.")
                    
        except ValueError:
            print("Invalid input!")

    def check_cybernetics(self):
        """Check and manage cybernetic enhancements"""
        print("\n🔧 CYBERNETICS")
        print("Your cybernetic enhancements:")
        
        if not self.player.cybernetics:
            print("No cybernetic enhancements installed.")
        else:
            for i, cybernetic in enumerate(self.player.cybernetics, 1):
                print(f"{i}. {cybernetic}")
        
        print(f"\nYour hacking skill: {self.player.hacking_skill}")
        print(f"Your gambling skill: {self.player.gambling_skill}")
        print(f"Your racing skill: {self.player.racing_skill}")
        
        print("\nOptions:")
        print("1. Install cybernetic enhancement")
        print("2. Remove cybernetic enhancement")
        print("3. Back to game")
        
        choice = input("What do you want to do? ").strip()
        
        if choice == "1":
            self.install_cybernetic()
        elif choice == "2":
            self.remove_cybernetic()
        elif choice == "3":
            return
        else:
            print("Invalid choice!")
        
        input("Press Enter to continue...")

    def install_cybernetic(self):
        """Install a cybernetic enhancement"""
        print("\nAvailable cybernetic enhancements:")
        
        cybernetics = [
            ("Neural Implant", 1000, "Boosts mental capabilities"),
            ("Hacker Tool", 200, "Improves hacking skills"),
            ("Quantum Processor", 1500, "Advanced computing device"),
            ("Neural Link", 800, "Connects your mind to the net"),
            ("Stealth Suit", 1200, "Makes you nearly invisible")
        ]
        
        for i, (name, cost, description) in enumerate(cybernetics, 1):
            print(f"{i}. {name} - {cost} credits - {description}")
        
        try:
            choice = int(input("Choose enhancement (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(cybernetics):
                name, cost, description = cybernetics[choice - 1]
                
                if self.player.credits >= cost:
                    self.player.credits -= cost
                    self.player.cybernetics.append(name)
                    print(f"✅ {name} installed successfully!")
                else:
                    print("You don't have enough credits!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

    def remove_cybernetic(self):
        """Remove a cybernetic enhancement"""
        if not self.player.cybernetics:
            print("No cybernetic enhancements to remove.")
            return
        
        print("\nYour cybernetic enhancements:")
        for i, cybernetic in enumerate(self.player.cybernetics, 1):
            print(f"{i}. {cybernetic}")
        
        try:
            choice = int(input("Choose enhancement to remove (0 to cancel): "))
            if choice == 0:
                return
            
            if 1 <= choice <= len(self.player.cybernetics):
                removed = self.player.cybernetics.pop(choice - 1)
                print(f"✅ {removed} removed successfully!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Invalid input!")

    def manage_gang_territory(self):
        """Manage gang territory"""
        print("\n🏴 GANG TERRITORY")
        print("Your controlled territories:")
        
        if not self.player.gang_territory:
            print("No territories controlled.")
        else:
            for i, territory in enumerate(self.player.gang_territory, 1):
                print(f"{i}. {territory}")
        
        print("\nOptions:")
        print("1. Attack new territory")
        print("2. Defend territory")
        print("3. Collect tribute")
        print("4. Back to game")
        
        choice = input("What do you want to do? ").strip()
        
        if choice == "1":
            self.attack_territory()
        elif choice == "2":
            self.defend_territory()
        elif choice == "3":
            self.collect_tribute()
        elif choice == "4":
            return
        else:
            print("Invalid choice!")
        
        input("Press Enter to continue...")

    def attack_territory(self):
        """Attack a new territory"""
        print("\nAttacking new territory...")
        
        # Simple territory attack
        success_chance = self.player.level * 10 + random.randint(1, 50)
        difficulty = random.randint(30, 80)
        
        print(f"Your attack power: {success_chance}")
        print(f"Territory defense: {difficulty}")
        
        if success_chance > difficulty:
            territory_name = f"Territory {random.randint(1, 100)}"
            self.player.gang_territory.append(territory_name)
            self.player.credits += 200
            print(f"🏆 You captured {territory_name}! You gained 200 credits!")
        else:
            print("💥 Attack failed! The territory is too well defended.")
            self.player.health -= 20

    def defend_territory(self):
        """Defend your territory"""
        if not self.player.gang_territory:
            print("No territories to defend.")
            return
        
        print("\nDefending territory...")
        
        # Simple territory defense
        defense_power = self.player.level * 8 + random.randint(1, 40)
        attack_power = random.randint(20, 60)
        
        print(f"Your defense power: {defense_power}")
        print(f"Enemy attack power: {attack_power}")
        
        if defense_power > attack_power:
            print("🛡️ Territory defended successfully!")
            self.player.credits += 100
        else:
            territory = self.player.gang_territory.pop()
            print(f"💥 Territory {territory} lost to enemies!")

    def collect_tribute(self):
        """Collect tribute from controlled territories"""
        if not self.player.gang_territory:
            print("No territories to collect tribute from.")
            return
        
        tribute = len(self.player.gang_territory) * 50
        self.player.credits += tribute
        print(f"💰 Collected {tribute} credits in tribute from {len(self.player.gang_territory)} territories!")

    def advance_time(self):
        """Advance time and trigger time-based events"""
        if self.player.time_of_day == "day":
            self.player.time_of_day = "night"
        else:
            self.player.time_of_day = "day"
            self.player.day_count += 1
        
        # Trigger random events based on time
        if random.random() < 0.3:  # 30% chance of random event
            self.trigger_random_event()

    def trigger_random_event(self):
        """Trigger a random event"""
        events = [
            "A corporate patrol passes by, but they don't notice you.",
            "You find a hidden stash of credits in an alley.",
            "A resistance member approaches you with information.",
            "You witness a corporate arrest in the distance.",
            "A street vendor offers you a discount on their goods.",
            "You hear rumors about a new corporate project.",
            "A gang member tries to recruit you.",
            "You find a discarded piece of technology."
        ]
        
        event = random.choice(events)
        print(f"\n🎲 Random Event: {event}")
        
        # Some events have consequences
        if "stash of credits" in event:
            credits_found = random.randint(50, 200)
            self.player.credits += credits_found
            print(f"You found {credits_found} credits!")
        elif "discarded piece of technology" in event:
            # Add random item
            items = ["energy_drink", "health_pack", "data_chip"]
            item_id = random.choice(items)
            item = self.items[item_id]
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
            print(f"You found a {item.name}!")

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