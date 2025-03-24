import pygame
import time
from .scenes.main_scene import MainScene
from .scenes.journal_scene import JournalScene
from .scenes.affirmation_scene import AffirmationScene
from .player_data import PlayerData

class GameManager:
    """Main game manager that handles scene transitions and overall game state"""
    
    def __init__(self, screen):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        # Initialize player data
        self.player_data = PlayerData()
        
        # Load fonts
        pygame.font.init()
        try:
            self.title_font = pygame.font.Font('assets/fonts/minecraft.ttf', 36)
            self.main_font = pygame.font.Font('assets/fonts/minecraft.ttf', 24)
            self.small_font = pygame.font.Font('assets/fonts/minecraft.ttf', 16)
        except (FileNotFoundError, pygame.error) as e:
            # Fallback to system font if custom font not found or invalid
            print(f"Warning: Could not load Minecraft font: {e}")
            print("Using system fonts instead. Please download the required fonts.")
            self.title_font = pygame.font.SysFont('Arial', 36)
            self.main_font = pygame.font.SysFont('Arial', 24)
            self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Set up scenes
        self.scenes = {
            'main': MainScene(self),
            'journal': JournalScene(self),
            'affirmation': AffirmationScene(self)
        }
        self.current_scene = 'main'
        
        # Track time for daily activities
        self.last_day = time.localtime().tm_yday
        self.check_daily_reset()
        
        # Initialize audio
        self.load_audio()
        
    def load_audio(self):
        """Load game audio resources"""
        self.sounds = {}
        try:
            self.sounds['water'] = pygame.mixer.Sound('assets/sounds/water.wav')
            self.sounds['grow'] = pygame.mixer.Sound('assets/sounds/grow.wav')
            self.sounds['click'] = pygame.mixer.Sound('assets/sounds/click.wav')
        except (FileNotFoundError, pygame.error) as e:
            print(f"Warning: Some audio files could not be loaded: {e}")
            print("Using the game without sound effects. Please download the required audio files.")
            
    def change_scene(self, scene_name):
        """Change to a different scene"""
        if scene_name in self.scenes:
            self.current_scene = scene_name
            self.scenes[scene_name].reset()
            
    def check_daily_reset(self):
        """Check if a day has passed to reset daily activities"""
        current_day = time.localtime().tm_yday
        if current_day != self.last_day:
            self.player_data.reset_daily()
            self.last_day = current_day
    
    def handle_event(self, event):
        """Pass events to the current scene"""
        self.scenes[self.current_scene].handle_event(event)
    
    def update(self):
        """Update the current scene"""
        self.check_daily_reset()
        self.scenes[self.current_scene].update()
    
    def draw(self):
        """Draw the current scene"""
        self.scenes[self.current_scene].draw(self.screen)
