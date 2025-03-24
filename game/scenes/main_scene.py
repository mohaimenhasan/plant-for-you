import pygame
import random
import math
from ..ui.button import Button
from ..ui.panel import MessagePanel
from ..plant_renderer import PlantRenderer

class MainScene:
    """Main game scene with the plant and core interactions"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen_rect = game_manager.screen_rect
        
        # Create plant renderer
        self.plant_renderer = PlantRenderer(self.screen_rect)
        
        # Track time for animations
        self.elapsed_time = 0
        
        # Initialize UI elements
        self.create_ui()
        
        # Motivational quotes
        self.quotes = [
            "Believe in yourself. You are braver than you think, more talented than you know.",
            "Your struggles today develop your strengths for tomorrow.",
            "The best way to predict your future is to create it.",
            "Don't compare your beginning to someone else's middle.",
            "Learning CS is like growing a plant - it takes consistent care and patience.",
            "Your value doesn't decrease based on someone's inability to see your worth.",
            "Everyone in CS feels like an impostor sometimes. It's part of the journey.",
            "The expert in anything was once a beginner.",
            "Your hardest times often lead to the greatest moments of your life.",
            "It's okay to not know all the answers. That's how you grow.",
            "Trust your journey, even when you don't understand it.",
            "The only opinion about your life that really matters is your own.",
            "You are capable of more than you know. Keep going!",
            "Computer science isn't about being the smartest; it's about persisting.",
            "Your worth is not measured by your productivity."
        ]
        
        # Animation variables
        self.water_effect_active = False
        self.water_timer = 0
        self.sparkle_positions = []
        
    def create_ui(self):
        """Create UI elements"""
        # Create buttons
        button_width = 180
        button_height = 50
        button_spacing = 20
        
        # Position buttons at the bottom of the screen
        button_y = self.screen_rect.height - button_height - 30
        
        # Water button
        water_x = self.screen_rect.width // 2 - button_width - button_spacing // 2
        self.water_button = Button(
            water_x, button_y, button_width, button_height,
            "Water Plant", self.game_manager.main_font,
            self.water_plant,
            color=(100, 150, 200), hover_color=(130, 180, 230)
        )
        
        # Affirmation button
        affirm_x = self.screen_rect.width // 2 + button_spacing // 2
        self.affirm_button = Button(
            affirm_x, button_y, button_width, button_height,
            "Daily Affirmation", self.game_manager.main_font,
            self.show_affirmation,
            color=(150, 120, 200), hover_color=(180, 150, 230)
        )
        
        # Journal button
        journal_x = self.screen_rect.width - button_width - 30
        self.journal_button = Button(
            journal_x, button_y, button_width, button_height,
            "Journal", self.game_manager.main_font,
            self.show_journal,
            color=(120, 180, 120), hover_color=(150, 210, 150)
        )
        
        # Quote panel
        quote_width = 400
        quote_height = 100
        quote_x = (self.screen_rect.width - quote_width) // 2
        quote_y = 20
        
        self.quote_panel = MessagePanel(
            quote_x, quote_y, quote_width, quote_height,
            self.game_manager.small_font,
            color=(230, 230, 250, 200),  # Light purple with transparency
            text_color=(50, 50, 50)
        )
        
        # Set initial quote
        self.quote_panel.set_messages([random.choice(self.quotes)])
        
        # Messages panel (for unlocked growth messages)
        message_width = 300
        message_height = 150
        message_x = 20
        message_y = 20
        
        self.messages_panel = MessagePanel(
            message_x, message_y, message_width, message_height,
            self.game_manager.small_font, "Growth Journal", self.game_manager.main_font,
            color=(220, 240, 220, 220),  # Light green with transparency
            text_color=(50, 50, 50)
        )
    
    def update_messages_panel(self):
        """Update the messages shown in the panel"""
        # Get the most recent messages
        messages = self.game_manager.player_data.unlocked_messages[-3:]
        self.messages_panel.set_messages(messages)
    
    def reset(self):
        """Reset the scene state when returning to it"""
        self.update_messages_panel()
        self.water_effect_active = False
        self.plant_renderer.water_particles = []
        
        # Update quote randomly
        if random.random() < 0.3:  # 30% chance to get a new quote
            self.quote_panel.set_messages([random.choice(self.quotes)])
        
        # Create some random sparkle positions
        self.sparkle_positions = [
            (random.randint(0, self.screen_rect.width),
             random.randint(0, self.screen_rect.height),
             random.uniform(0.5, 2.0))  # size
            for _ in range(20)
        ]
    
    def handle_event(self, event):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        
        # Check button interactions
        self.water_button.update(mouse_pos, mouse_clicked)
        self.affirm_button.update(mouse_pos, mouse_clicked)
        self.journal_button.update(mouse_pos, mouse_clicked)
        
        # Handle scrolling in message panel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.messages_panel.scroll(-1)
            elif event.button == 5:  # Scroll down
                self.messages_panel.scroll(1)
    
    def update(self):
        """Update scene state"""
        dt = pygame.time.get_ticks() % 60  # Time since last frame in ms
        self.elapsed_time += dt
        
        # Update plant animations
        self.plant_renderer.update(dt)
        
        # Update water effect
        if self.water_effect_active:
            self.water_timer -= dt
            if self.water_timer <= 0:
                self.water_effect_active = False
        
        # Update sparkle animations
        for i, (x, y, size) in enumerate(self.sparkle_positions):
            # Move sparkles slowly
            new_y = (y - 0.2 * dt) % self.screen_rect.height
            self.sparkle_positions[i] = (x, new_y, size)
    
    def draw(self, surface):
        """Draw the scene"""
        # Draw background decorations
        self._draw_background(surface)
        
        # Draw plant
        player_data = self.game_manager.player_data
        self.plant_renderer.draw(
            surface,
            player_data.plant_level,
            player_data.plant_growth
        )
        
        # Draw UI panels
        self.messages_panel.draw(surface)
        self.quote_panel.draw(surface)
        
        # Draw buttons
        self.water_button.draw(surface)
        self.affirm_button.draw(surface)
        self.journal_button.draw(surface)
        
        # Draw status indicators
        self._draw_status_indicators(surface)
    
    def _draw_background(self, surface):
        """Draw background elements like sparkles and clouds"""
        # Draw some background sparkles
        for x, y, size in self.sparkle_positions:
            # Make sparkles twinkle
            alpha = int(150 + 105 * abs(math.sin(self.elapsed_time * 0.001 + x * 0.1)))
            sparkle_color = (255, 255, 200, alpha)
            
            pygame.draw.circle(
                surface,
                sparkle_color,
                (int(x), int(y)),
                int(size)
            )
    
    def _draw_status_indicators(self, surface):
        """Draw indicators for daily activities"""
        player_data = self.game_manager.player_data
        font = self.game_manager.small_font
        
        # Plant level
        level_text = f"Plant Level: {player_data.plant_level}"
        level_surf = font.render(level_text, True, (255, 255, 255))
        surface.blit(level_surf, (20, self.screen_rect.height - 70))
        
        # Watered today
        water_status = "✓" if player_data.watered_today else "✗"
        water_color = (100, 200, 100) if player_data.watered_today else (200, 100, 100)
        water_text = f"Watered Today: {water_status}"
        water_surf = font.render(water_text, True, water_color)
        surface.blit(water_surf, (20, self.screen_rect.height - 45))
        
        # Affirmation done
        affirm_status = "✓" if player_data.affirmation_done_today else "✗"
        affirm_color = (100, 200, 100) if player_data.affirmation_done_today else (200, 100, 100)
        affirm_text = f"Daily Affirmation: {affirm_status}"
        affirm_surf = font.render(affirm_text, True, affirm_color)
        surface.blit(affirm_surf, (20, self.screen_rect.height - 20))
        
        # Growth progress bar
        bar_width = 200
        bar_height = 15
        bar_x = self.screen_rect.width - bar_width - 20
        bar_y = self.screen_rect.height - 30
        
        # Background bar
        pygame.draw.rect(surface, (50, 50, 50), 
                         (bar_x, bar_y, bar_width, bar_height))
        
        # Progress fill
        fill_width = int(bar_width * player_data.plant_growth)
        pygame.draw.rect(surface, (100, 200, 100), 
                         (bar_x, bar_y, fill_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (200, 200, 200), 
                         (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Label
        growth_text = "Growth Progress"
        growth_surf = font.render(growth_text, True, (255, 255, 255))
        surface.blit(growth_surf, (bar_x, bar_y - 25))
    
    def water_plant(self):
        """Handle watering the plant"""
        player_data = self.game_manager.player_data
        
        if not player_data.watered_today:
            success = player_data.water_plant()
            if success:
                # Trigger water animation
                self.water_effect_active = True
                self.water_timer = 1000  # ms
                self.plant_renderer.add_water_effect()
                self.plant_renderer.add_growth_effect()
                
                # Play sound
                if 'water' in self.game_manager.sounds:
                    self.game_manager.sounds['water'].play()
                
                # Update message panel
                self.update_messages_panel()
    
    def show_affirmation(self):
        """Switch to affirmation scene"""
        self.game_manager.change_scene('affirmation')
    
    def show_journal(self):
        """Switch to journal scene"""
        self.game_manager.change_scene('journal')
