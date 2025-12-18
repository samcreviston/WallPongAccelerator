# WallPongAccelerator

**Overview**

I built this project to stretch my Python knowledge and adopt the Arcade library into my skillset!

Wall-Pong is a single-player Python game built with **Arcade**. The player controls a paddle to bounce a ball off the walls and try to achieve the highest score possible. The game features dynamic speed acceleration, retro-style visuals, arcade sound effects, high score tracking, and a performance-optimized UI

{your YouTube demonstration.  It should be a 4-5 minute demo of the game being played and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

## Setup Instructions

1. **Navigate to project directory**  
   ```bash
   cd "WallPongAccelerator"

2. **Activate the virtual environment**
   ```bash
   .\.venv\Scripts\Activate.ps1

3. **Install required packages** (if not already installed)
   ```bash
   pip install arcade numpy

4. **Run the game**
   ```bash
   python main.py

## Alternative Setup (Direct Run)

If you prefer not to activate the virtual environment:
    ```bash
    ".\.venv\Scripts\python.exe" main.py

## Controls

- **↑ / W** - Move paddle up
- **↓ / S** - Move paddle down  
- **SPACE** - Pause/unpause game
- **R** - Restart game (when game over)

---

# Development Environment

I built this within VS Code in Python. I utilized mainly the Arvade library, as well as Numpy for some sound effects.

## Project Structure
WallPongAccelerator/
├── main.py              # Main game code with sound effects and pause functionality
├── constants.py         # Game constants (colors, speeds, dimensions)
├── assets/              # Generated sound files (beeps, game over, start sounds)
├── highscore.txt        # Persistent high score storage
├── .venv/              # Python virtual environment
└── README.md           # This file

**Files explained:**

- `main.py` – Complete game implementation with physics, sound system, pause functionality, and retro UI styling
- `constants.py` – All configurable values (colors, speeds, dimensions, file paths)
- `assets/` – Auto-generated WAV sound files for arcade-style audio experience
- `highscore.txt` – High score persistence between game sessions

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Arcade Explanation from Real Python](https://realpython.com/arcade-python-game-framework/)
* [Numpy documentation](https://numpy.org/doc/)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Item 1
* Item 2
* Item 3

