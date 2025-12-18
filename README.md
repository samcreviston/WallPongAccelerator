# WallPongAccelerator

**Overview**

I built this project to stretch my Python knowledge and adopt the Arcade library into my skillset!

Wall-Pong is a single-player Python game built with **Arcade**. The player controls a paddle to bounce a ball off the walls and try to achieve the highest score possible. The game features dynamic speed acceleration, retro-style visuals, arcade sound effects, high score tracking, and a performance-optimized UI

[Software Demo Video](https://youtu.be/_sl3LzNsFLk)

## Setup Instructions

1. **Navigate to project directory**  
   ```bash
   cd "WallPongAccelerator"
   ```

2. **Initialize the virtual environment** (with python installed)
   ```bash
   python -m venv .venv
   ```
   
3. **Activate the virtual environment**
   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

4. **Install required packages** (if not already installed)
   ```bash
   pip install arcade numpy
   ```

5. **Run the game**
   ```bash
   python main.py
   ```

## Alternative Setup (Direct Run)

If you prefer not to activate the virtual environment:
```bash
".\.venv\Scripts\python.exe" main.py
```

## Controls

- **↑ / W** - Move paddle up
- **↓ / S** - Move paddle down  
- **SPACE** - Pause/unpause game
- **R** - Restart game (when game over)

---

# Development Environment

I built this within VS Code in Python. I utilized mainly the Arcade library, as well as Numpy for some sound effects.

## Project Structure
WallPongAccelerator/
- ├── main.py           # Main game code with physics, sound effects, and pause functionality
- ├── constants.py      # Game constants (colors, speeds, dimensions, file paths)
- ├── assets/           # Generated sound files (beeps, game over, start sounds)
- ├── highscore.txt     # Persistent high score storage
- ├── .venv/            # Python virtual environment (once initialized)


# Useful Websites
* [Arcade Explanation from Real Python](https://realpython.com/arcade-python-game-framework/)
* [Numpy documentation](https://numpy.org/doc/)

# Future Work
* Game modes such as two player
* Mode with extra lives
* Adjustable speed settings

