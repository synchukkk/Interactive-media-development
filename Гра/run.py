#!/usr/bin/env python3
"""Launcher script for Space Game"""
import subprocess
import sys
import os

def main():
    game_path = os.path.join(os.path.dirname(__file__), 'space_game.py')
    try:
        subprocess.run([sys.executable, game_path])
    except Exception as e:
        print(f"Error running game: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
