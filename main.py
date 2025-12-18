"""
Wall Pong Accelerator - A single-player pong game with high score tracking
Author: Sam Creviston
"""

import arcade
import math
import random
from constants import *


class Ball:
    """Represents the ball in the game"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = INITIAL_BALL_SPEED
        self.angle = random.uniform(3*math.pi/4, 5*math.pi/4)  # Start angle toward paddle (leftward)
        self.velocity_x = self.speed * math.cos(self.angle)
        self.velocity_y = self.speed * math.sin(self.angle)
        
    def update(self, delta_time):
        """Update ball position"""
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
    def bounce_vertical(self):
        """Bounce off top/bottom walls"""
        self.velocity_y = -self.velocity_y
        
    def bounce_horizontal(self):
        """Bounce off left wall or paddle"""
        self.velocity_x = -self.velocity_x
        # Accelerate the ball
        self.speed = min(self.speed + BALL_ACCELERATION, MAX_BALL_SPEED)
        self._update_velocity()
        
    def bounce_paddle(self, paddle_y):
        """Bounce off paddle with angle based on where it hits"""
        # Calculate relative hit position (-1 to 1)
        relative_hit = (self.y - paddle_y) / (PADDLE_HEIGHT / 2)
        relative_hit = max(-1, min(1, relative_hit))  # Clamp to [-1, 1]
        
        # New angle based on hit position (bounce toward left side)
        self.angle = math.pi - (relative_hit * math.pi/3)  # Bounce leftward with angle
        self.velocity_x = self.speed * math.cos(self.angle)  # Always bounce left
        self.velocity_y = self.speed * math.sin(self.angle)
        
        # Accelerate the ball
        self.speed = min(self.speed + BALL_ACCELERATION, MAX_BALL_SPEED)
        self._update_velocity()
        
    def _update_velocity(self):
        """Update velocity components based on current speed and angle"""
        length = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        if length > 0:
            self.velocity_x = (self.velocity_x / length) * self.speed
            self.velocity_y = (self.velocity_y / length) * self.speed
    
    def draw(self):
        """Draw the ball"""
        arcade.draw_circle_filled(self.x, self.y, BALL_SIZE // 2, BALL_COLOR)


class Paddle:
    """Represents the player's paddle"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        
    def update(self, delta_time, up_pressed, down_pressed):
        """Update paddle position based on input"""
        if up_pressed:
            self.velocity_y = PADDLE_SPEED
        elif down_pressed:
            self.velocity_y = -PADDLE_SPEED
        else:
            self.velocity_y = 0
            
        # Update position
        self.y += self.velocity_y * delta_time
        
        # Keep paddle within bounds
        self.y = max(PADDLE_MIN_Y, min(PADDLE_MAX_Y, self.y))
        
    def draw(self):
        """Draw the paddle with rounded ends"""
        # Draw main rectangle body
        arcade.draw_lrbt_rectangle_filled(
            self.x - PADDLE_WIDTH // 2,
            self.x + PADDLE_WIDTH // 2,
            self.y - PADDLE_HEIGHT // 2 + PADDLE_WIDTH // 2,
            self.y + PADDLE_HEIGHT // 2 - PADDLE_WIDTH // 2,
            PADDLE_COLOR
        )
        
        # Draw rounded ends (half circles)
        arcade.draw_circle_filled(
            self.x, self.y + PADDLE_HEIGHT // 2 - PADDLE_WIDTH // 2,
            PADDLE_WIDTH // 2, PADDLE_COLOR
        )
        arcade.draw_circle_filled(
            self.x, self.y - PADDLE_HEIGHT // 2 + PADDLE_WIDTH // 2,
            PADDLE_WIDTH // 2, PADDLE_COLOR
        )
        
    def get_collision_rect(self):
        """Get paddle collision rectangle"""
        return {
            'left': self.x - PADDLE_WIDTH // 2,
            'right': self.x + PADDLE_WIDTH // 2,
            'bottom': self.y - PADDLE_HEIGHT // 2,
            'top': self.y + PADDLE_HEIGHT // 2
        }


class WallPongGame(arcade.Window):
    """Main game class"""
    
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(BACKGROUND_COLOR)
        
        # Game objects
        self.ball = None
        self.paddle = None
        
        # Game state
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_running = True
        self.paused = False
        
        # Sound effects
        self.paddle_sounds = []
        self.game_over_sound = None
        self.game_start_sound = None
        
        # Input state
        self.up_pressed = False
        self.down_pressed = False
        
        # Text objects for better performance
        self.score_text = None
        self.high_score_text = None
        self.speed_text = None
        self.game_over_texts = []
        self.pause_texts = []
        
    def setup(self):
        """Set up the game and initialize variables"""
        # Create game objects
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.paddle = Paddle(PADDLE_RIGHT, SCREEN_HEIGHT // 2)
        
        # Generate arcade-style sounds
        self.create_sounds()
        
        # Create text objects for better performance
        self.create_text_objects()
        
        # Play game start sound
        if self.game_start_sound:
            arcade.play_sound(self.game_start_sound)
        
    def create_sounds(self):
        """Generate arcade-style sound effects"""
        import numpy as np
        import wave
        import os
        
        try:
            # Ensure assets directory exists
            os.makedirs("assets", exist_ok=True)
            
            # Create simple beep sounds as WAV files
            sample_rate = 22050
            duration = 0.1  # 100ms
            
            # Create two different frequency beeps (removed highest pitch)
            frequencies = [330, 220]  # Mid, low (removed 440Hz high pitch)
            self.paddle_sounds = []
            
            for i, freq in enumerate(frequencies):
                filename = f"beep_{i}.wav"
                filepath = os.path.join("assets", filename)
                
                # Generate sine wave
                t = np.linspace(0, duration, int(sample_rate * duration), False)
                wave_data = np.sin(freq * 2 * np.pi * t)
                
                # Add fade in/out to prevent clicks
                fade_samples = int(0.01 * sample_rate)  # 10ms fade
                wave_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
                wave_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
                
                # Convert to 16-bit integers
                wave_data = (wave_data * 32767).astype(np.int16)
                
                # Write WAV file
                with wave.open(filepath, 'w') as wav_file:
                    wav_file.setnchannels(1)  # mono
                    wav_file.setsampwidth(2)  # 16-bit
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(wave_data.tobytes())
                
                # Load the sound
                sound = arcade.load_sound(filepath)
                self.paddle_sounds.append(sound)
            
            # Create game over sound (descending beep)
            game_over_file = os.path.join("assets", "game_over.wav")
            t = np.linspace(0, 0.5, int(sample_rate * 0.5), False)
            freq_start, freq_end = 440, 110
            frequency = np.linspace(freq_start, freq_end, len(t))
            wave_data = np.sin(2 * np.pi * np.cumsum(frequency) / sample_rate)
            
            # Fade out
            fade_samples = int(0.1 * sample_rate)
            wave_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            wave_data = (wave_data * 32767).astype(np.int16)
            with wave.open(game_over_file, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(wave_data.tobytes())
            
            self.game_over_sound = arcade.load_sound(game_over_file)
            
            # Create game start sound (ascending beep)
            game_start_file = os.path.join("assets", "game_start.wav")
            t = np.linspace(0, 0.3, int(sample_rate * 0.3), False)
            freq_start, freq_end = 220, 440
            frequency = np.linspace(freq_start, freq_end, len(t))
            wave_data = np.sin(2 * np.pi * np.cumsum(frequency) / sample_rate)
            
            # Fade in and out
            fade_samples = int(0.05 * sample_rate)
            wave_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
            wave_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
            
            wave_data = (wave_data * 32767).astype(np.int16)
            with wave.open(game_start_file, 'w') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(wave_data.tobytes())
            
            self.game_start_sound = arcade.load_sound(game_start_file)
            
        except Exception as e:
            print(f"Could not create sounds: {e}")
            # Fallback - no sounds
            self.paddle_sounds = []
            self.game_over_sound = None
    def create_text_objects(self):
        """Create Text objects for better performance"""
        # Game UI text (moved away from wall and retro styled)
        font_name = "Consolas"  # Retro monospace font
        self.score_text = arcade.Text("", 35, SCREEN_HEIGHT - 55, TEXT_COLOR, 20, font_name=font_name)
        self.high_score_text = arcade.Text("", 35, SCREEN_HEIGHT - 85, TEXT_COLOR, 20, font_name=font_name)
        self.speed_text = arcade.Text("", 35, SCREEN_HEIGHT - 115, TEXT_COLOR, 16, font_name=font_name)
        
        # Game over screen texts
        self.game_over_texts = [
            arcade.Text("GAME OVER!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, TEXT_COLOR, 36, font_name=font_name, anchor_x="center"),
            arcade.Text("", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, TEXT_COLOR, 24, font_name=font_name, anchor_x="center"),  # Final score
            arcade.Text("Press R to restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, TEXT_COLOR, 20, font_name=font_name, anchor_x="center")
        ]
        
        # Pause screen texts
        self.pause_texts = [
            arcade.Text("PAUSED", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, TEXT_COLOR, 48, font_name=font_name, anchor_x="center"),
            arcade.Text("Press SPACE to continue", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, TEXT_COLOR, 20, font_name=font_name, anchor_x="center")
        ]

    def on_draw(self):
        """Render the game"""
        self.clear()
        
        # Draw walls
        # Left wall
        arcade.draw_lrbt_rectangle_filled(
            0, WALL_THICKNESS, 0, SCREEN_HEIGHT, WALL_COLOR
        )
        # Top wall
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, SCREEN_HEIGHT - WALL_THICKNESS, SCREEN_HEIGHT, WALL_COLOR
        )
        # Bottom wall
        arcade.draw_lrbt_rectangle_filled(
            0, SCREEN_WIDTH, 0, WALL_THICKNESS, WALL_COLOR
        )
        
        if self.game_running:
            # Draw game objects
            self.ball.draw()
            self.paddle.draw()
        
        # Draw score and info
        self.score_text.text = f"Score: {self.score}"
        self.score_text.draw()
        
        self.high_score_text.text = f"High Score: {self.high_score}"
        self.high_score_text.draw()
        
        # Draw speed indicator
        if self.ball:
            speed_percentage = int((self.ball.speed / INITIAL_BALL_SPEED) * 100)
            self.speed_text.text = f"Speed: {speed_percentage}%"
            self.speed_text.draw()
        
        if not self.game_running:
            # Game over screen
            self.game_over_texts[0].draw()  # "GAME OVER!"
            self.game_over_texts[1].text = f"Final Score: {self.score}"
            self.game_over_texts[1].draw()  # Final score
            self.game_over_texts[2].draw()  # "Press R to restart"
        elif self.paused:
            # Pause screen
            self.pause_texts[0].draw()  # "PAUSED"
            self.pause_texts[1].draw()  # "Press SPACE to continue"
        elif self.paused:
            # Pause screen
            arcade.draw_text(
                "PAUSED",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                TEXT_COLOR, 48,
                anchor_x="center"
            )
            arcade.draw_text(
                "Press SPACE to continue",
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                TEXT_COLOR, 20,
                anchor_x="center"
            )
            
    def on_update(self, delta_time):
        """Update game logic"""
        if not self.game_running or self.paused:
            return
            
        # Update game objects
        self.paddle.update(delta_time, self.up_pressed, self.down_pressed)
        self.ball.update(delta_time)
        
        # Ball collision with walls
        if self.ball.y >= WALL_TOP - BALL_SIZE // 2:
            self.ball.y = WALL_TOP - BALL_SIZE // 2
            self.ball.bounce_vertical()
            
        if self.ball.y <= WALL_BOTTOM + BALL_SIZE // 2:
            self.ball.y = WALL_BOTTOM + BALL_SIZE // 2
            self.ball.bounce_vertical()
            
        if self.ball.x <= WALL_LEFT + BALL_SIZE // 2:
            self.ball.x = WALL_LEFT + BALL_SIZE // 2
            self.ball.bounce_horizontal()
            
        # Ball collision with paddle
        paddle_rect = self.paddle.get_collision_rect()
        if (self.ball.x + BALL_SIZE // 2 >= paddle_rect['left'] and
            self.ball.x - BALL_SIZE // 2 <= paddle_rect['right'] and
            self.ball.y + BALL_SIZE // 2 >= paddle_rect['bottom'] and
            self.ball.y - BALL_SIZE // 2 <= paddle_rect['top'] and
            self.ball.velocity_x > 0):  # Only bounce if moving toward paddle
            
            self.ball.x = paddle_rect['left'] - BALL_SIZE // 2
            self.ball.bounce_paddle(self.paddle.y)
            self.score += 1
            
            # Play random paddle bounce sound
            if self.paddle_sounds:
                sound = random.choice(self.paddle_sounds)
                arcade.play_sound(sound)
            
        # Check if ball goes off right edge (game over)
        if self.ball.x > WALL_RIGHT + BALL_SIZE:
            self.game_over()
            
    def game_over(self):
        """Handle game over"""
        self.game_running = False
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
        # Play game over sound
        if self.game_over_sound:
            arcade.play_sound(self.game_over_sound)
            
    def restart_game(self):
        """Restart the game"""
        self.score = 0
        self.game_running = True
        self.paused = False
        self.setup()
        
    def on_key_press(self, key, modifiers):
        """Handle key presses"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.SPACE and self.game_running:
            self.paused = not self.paused
        elif key == arcade.key.R and not self.game_running:
            self.restart_game()
            
    def on_key_release(self, key, modifiers):
        """Handle key releases"""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
            
    def load_high_score(self):
        """Load high score from file"""
        try:
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0
            
    def save_high_score(self):
        """Save high score to file"""
        try:
            with open(HIGH_SCORE_FILE, 'w') as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"Could not save high score: {e}")


def main():
    """Main function to run the game"""
    game = WallPongGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()