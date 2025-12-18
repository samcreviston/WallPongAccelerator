# WallPongAccelerator

**Description:**  
Wall-Pong is a single-player Python game built with **Arcade**. The player controls a paddle to bounce a ball off the walls and try to achieve the highest score possible. The game features dynamic speed acceleration, retro-style visuals, arcade sound effects, and high score tracking.

---

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

---

## Game Features

✅ **Single-player wall-pong gameplay**  
✅ **Dynamic ball speed acceleration** (speed increases with each bounce)  
✅ **Arcade-style sound effects** (paddle bounces, game start/over sounds)  
✅ **Pause functionality** (SPACE to pause/unpause)  
✅ **High score tracking** (persists between sessions)  
✅ **Performance-optimized UI** (Text objects for smooth rendering)  
✅ **Retro color scheme** (faded teal background, dark brown walls, orange paddle, tan ball)
✅ **Retro monospace font styling**

---

## Controls

- **↑ / W** - Move paddle up
- **↓ / S** - Move paddle down  
- **SPACE** - Pause/unpause game
- **R** - Restart game (when game over)

---

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
   ```

---

## Alternative Setup (Direct Run)

If you prefer not to activate the virtual environment:
```bash
".\.venv\Scripts\python.exe" main.py
```

---

## Technical Details

**Dependencies:**
- `arcade` - Game framework for graphics, input, and sound
- `numpy` - For generating procedural audio waveforms

**Audio System:**
- Procedurally generated arcade-style beep sounds
- Two random paddle bounce frequencies (330Hz, 220Hz)
- Ascending start tone, descending game-over tone
- All sounds auto-generated as WAV files on first run

**Performance:**
- Efficient Text objects instead of draw_text() calls
- Optimized rendering pipeline for smooth 60 FPS
- Minimal memory footprint with reusable audio assets

