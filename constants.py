# constants.py - Game configuration constants

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Wall Pong Accelerator"

# Colors (8-bit style)
BACKGROUND_COLOR = (70, 130, 130)   # Faded teal
WALL_COLOR = (80, 50, 30)           # Dark brown
BALL_COLOR = (255, 200, 150)        # Orange tan
PADDLE_COLOR = (200, 120, 80)       # Faded orange
TEXT_COLOR = (255, 255, 255)        # White

# Game object sizes
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 10
WALL_THICKNESS = 20

# Game physics
INITIAL_BALL_SPEED = 300            # pixels per second
PADDLE_SPEED = 400                  # pixels per second
BALL_ACCELERATION = 20              # speed increase per bounce
MAX_BALL_SPEED = 800               # maximum ball speed

# Game area boundaries
WALL_LEFT = WALL_THICKNESS
WALL_RIGHT = SCREEN_WIDTH - WALL_THICKNESS
WALL_TOP = SCREEN_HEIGHT - WALL_THICKNESS
WALL_BOTTOM = WALL_THICKNESS

# Paddle constraints
PADDLE_RIGHT = WALL_RIGHT - 20       # Distance from right wall
PADDLE_MIN_Y = WALL_BOTTOM + PADDLE_HEIGHT // 2
PADDLE_MAX_Y = WALL_TOP - PADDLE_HEIGHT // 2

# High score file
HIGH_SCORE_FILE = "highscore.txt"