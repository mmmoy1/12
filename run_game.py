#!/usr/bin/env python3
"""
Cyberpunk Adventure Launcher
============================

Simple launcher script for the Cyberpunk Adventure game.
This script checks for Python version compatibility and launches the game.
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("❌ Error: Python 3.6 or higher is required.")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        return False
    return True

def main():
    """Main launcher function"""
    print("🎮 Cyberpunk Adventure Launcher")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return
    
    print("✅ Python version check passed")
    print("🚀 Starting Cyberpunk Adventure...")
    print()
    
    # Check if game file exists
    game_file = "cyberpunk_adventure.py"
    if not os.path.exists(game_file):
        print(f"❌ Error: {game_file} not found!")
        print("   Make sure you're running this from the correct directory.")
        input("Press Enter to exit...")
        return
    
    try:
        # Import and run the game
        from cyberpunk_adventure import CyberpunkAdventure
        game = CyberpunkAdventure()
        game.run()
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing Cyberpunk Adventure!")
    except Exception as e:
        print(f"\n❌ Error starting game: {e}")
        print("   Please check that all files are present and try again.")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()