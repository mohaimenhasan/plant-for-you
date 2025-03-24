import pygame
from ..ui.button import Button, TextButton
from ..ui.panel import Panel, MessagePanel
from ..ui.text_input import TextInput

class JournalScene:
    """Journal scene where the player can record thoughts and reflections"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen_rect = game_manager.screen_rect
        
        # Initialize UI elements
        self.create_ui()
        
        # For managing keyboard focus
        self.active_input = None
        
        # Journal prompts
        self.journal_prompts = [
            "What made you feel proud today?",
            "What's one thing you learned recently that surprised you?",
            "What small win can you celebrate today?",
            "If your future self could give you advice, what would they say?",
            "What's a challenge that felt impossible but you overcame?",
            "What would you do in your field if you knew you couldn't fail?",
            "What's something nice someone said that you could tell yourself?",
            "What's a skill you're better at than you give yourself credit for?",
            "What small step could you take today toward a goal?",
            "What would you try if other people's opinions didn't matter?",
            "What's one thing that makes you unique in your approach to problems?",
            "When do you feel most confident in your abilities?",
            "What would you tell a friend who felt the same doubts you do?",
            "What's one thing you accomplished that you didn't think you could?",
            "What qualities do you admire in others that you also possess?"
        ]
        self.current_prompt = self.journal_prompts[0]
    
    def create_ui(self):
        """Create UI elements"""
        # Main panel background
        panel_width = self.screen_rect.width - 100
        panel_height = self.screen_rect.height - 100
        panel_x = (self.screen_rect.width - panel_width) // 2
        panel_y = (self.screen_rect.height - panel_height) // 2
        
        self.main_panel = Panel(
            panel_x, panel_y, panel_width, panel_height,
            color=(240, 240, 230)  # Soft cream color
        )
        
        # Journal entries panel
        entries_width = panel_width // 3
        entries_height = panel_height - 80
        entries_x = panel_x + 20
        entries_y = panel_y + 60
        
        self.entries_panel = MessagePanel(
            entries_x, entries_y, entries_width, entries_height,
            self.game_manager.small_font, "Your Journal Entries", self.game_manager.main_font,
            color=(230, 230, 230)
        )
        
        # Input area
        input_width = panel_width - entries_width - 60
        input_height = panel_height - 200
        input_x = entries_x + entries_width + 20
        input_y = entries_y
        
        self.journal_input = TextInput(
            input_x, input_y, input_width, input_height,
            self.game_manager.small_font, 
            placeholder="Write your thoughts here...",
            max_length=500
        )
        
        # Buttons
        button_width = 150
        button_height = 50
        button_y = input_y + input_height + 20
        
        # Save button
        save_x = input_x + input_width - button_width
        self.save_button = Button(
            save_x, button_y, button_width, button_height,
            "Save Entry", self.game_manager.main_font,
            self.save_entry,
            color=(100, 180, 100), hover_color=(130, 210, 130)
        )
        
        # New prompt button
        prompt_x = save_x - button_width - 20
        self.prompt_button = Button(
            prompt_x, button_y, button_width, button_height,
            "New Prompt", self.game_manager.main_font,
            self.new_prompt,
            color=(180, 180, 100), hover_color=(210, 210, 130)
        )
        
        # Back button
        back_x = panel_x + 20
        back_y = panel_y + panel_height - button_height - 20
        self.back_button = Button(
            back_x, back_y, button_width, button_height,
            "Back", self.game_manager.main_font,
            self.go_back,
            color=(200, 200, 200), hover_color=(230, 230, 230)
        )
    
    def reset(self):
        """Reset scene state when returning to it"""
        # Refresh entries list
        journal_entries = self.game_manager.player_data.journal_entries
        
        # Format entries for display
        formatted_entries = []
        for entry in journal_entries:
            formatted_entries.append(f"[{entry['date']}]\n{entry['text']}")
        
        self.entries_panel.set_messages(formatted_entries)
        
        # Reset input
        self.journal_input.clear()
        
        # Pick a random prompt
        self.new_prompt()
    
    def handle_event(self, event):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        
        # Get all current events for text input
        all_events = [event]
        
        # Check button interactions
        self.save_button.update(mouse_pos, mouse_clicked)
        self.prompt_button.update(mouse_pos, mouse_clicked)
        self.back_button.update(mouse_pos, mouse_clicked)
        
        # Handle scrolling in entries panel
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.entries_panel.scroll(-1)
            elif event.button == 5:  # Scroll down
                self.entries_panel.scroll(1)
        
        # Update text input
        self.journal_input.update(all_events)
    
    def update(self):
        """Update scene state"""
        # Nothing to update regularly in this scene
        pass
    
    def draw(self, surface):
        """Draw the scene"""
        # Draw main background panel
        self.main_panel.draw(surface)
        
        # Draw title
        title_surf = self.game_manager.title_font.render("Journal", True, (50, 50, 50))
        title_rect = title_surf.get_rect(midtop=(self.screen_rect.centerx, self.main_panel.rect.top + 20))
        surface.blit(title_surf, title_rect)
        
        # Draw entries panel
        self.entries_panel.draw(surface)
        
        # Draw current prompt
        prompt_surf = self.game_manager.main_font.render("Prompt:", True, (50, 50, 50))
        prompt_x = self.journal_input.rect.left
        prompt_y = self.entries_panel.rect.top - 30
        surface.blit(prompt_surf, (prompt_x, prompt_y))
        
        prompt_text_surf = self.game_manager.small_font.render(self.current_prompt, True, (50, 50, 150))
        surface.blit(prompt_text_surf, (prompt_x + prompt_surf.get_width() + 10, prompt_y + 5))
        
        # Draw text input
        self.journal_input.draw(surface)
        
        # Draw buttons
        self.save_button.draw(surface)
        self.prompt_button.draw(surface)
        self.back_button.draw(surface)
    
    def save_entry(self):
        """Save the current journal entry"""
        entry_text = self.journal_input.get_text().strip()
        
        if entry_text:
            # Add the entry to player data
            self.game_manager.player_data.add_journal_entry(entry_text)
            
            # Play sound
            if 'click' in self.game_manager.sounds:
                self.game_manager.sounds['click'].play()
            
            # Reset input and refresh entries
            self.journal_input.clear()
            self.reset()
    
    def new_prompt(self):
        """Get a new random journal prompt"""
        import random
        self.current_prompt = random.choice(self.journal_prompts)
    
    def go_back(self):
        """Return to main scene"""
        self.game_manager.change_scene('main')
