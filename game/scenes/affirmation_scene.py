import pygame
import random
from ..ui.button import Button
from ..ui.panel import Panel, MessagePanel

class AffirmationScene:
    """Scene for daily affirmations and positive self-talk exercises"""
    
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.screen_rect = game_manager.screen_rect
        
        # Initialize UI elements
        self.create_ui()
        
        # Set up affirmations and challenges
        self.setup_content()
        
        # Track state
        self.current_step = 0
        self.affirm_done = False
        self.selected_option = None
    
    def create_ui(self):
        """Create UI elements"""
        # Main panel background
        panel_width = self.screen_rect.width - 100
        panel_height = self.screen_rect.height - 100
        panel_x = (self.screen_rect.width - panel_width) // 2
        panel_y = (self.screen_rect.height - panel_height) // 2
        
        self.main_panel = Panel(
            panel_x, panel_y, panel_width, panel_height,
            color=(220, 220, 240)  # Soft purple color
        )
        
        # Content panel for affirmations and prompts
        content_width = panel_width - 80
        content_height = panel_height - 200
        content_x = panel_x + 40
        content_y = panel_y + 80
        
        self.content_panel = MessagePanel(
            content_x, content_y, content_width, content_height,
            self.game_manager.main_font, title=None,
            color=(240, 240, 255)
        )
        
        # Option buttons for multiple choice
        button_width = content_width // 2 - 20
        button_height = 60
        button_spacing = 20
        button_y = content_y + content_height + 20
        
        # Option 1 button
        option1_x = content_x
        self.option1_button = Button(
            option1_x, button_y, button_width, button_height,
            "Option 1", self.game_manager.main_font,
            lambda: self.select_option(0),
            color=(150, 150, 220), hover_color=(180, 180, 250)
        )
        
        # Option 2 button
        option2_x = content_x + button_width + button_spacing
        self.option2_button = Button(
            option2_x, button_y, button_width, button_height,
            "Option 2", self.game_manager.main_font,
            lambda: self.select_option(1),
            color=(150, 150, 220), hover_color=(180, 180, 250)
        )
        
        # Next button
        next_width = 150
        next_height = 50
        next_x = panel_x + panel_width - next_width - 30
        next_y = panel_y + panel_height - next_height - 30
        
        self.next_button = Button(
            next_x, next_y, next_width, next_height,
            "Next", self.game_manager.main_font,
            self.next_step,
            color=(100, 180, 100), hover_color=(130, 210, 130)
        )
        
        # Back button
        back_x = panel_x + 30
        back_y = next_y
        
        self.back_button = Button(
            back_x, back_y, next_width, next_height,
            "Back", self.game_manager.main_font,
            self.go_back,
            color=(200, 200, 200), hover_color=(230, 230, 230)
        )
    
    def setup_content(self):
        """Set up the affirmation content and exercises"""
        # Introduction content
        self.intro_text = [
            "Welcome to your daily affirmation!",
            "\nEach day, we'll practice positive self-talk and challenge negative thoughts.",
            "\nThis helps build confidence and resilience, especially when facing challenges in your studies."
        ]
        
        # Core affirmations list
        self.affirmations = [
            "I am capable of learning difficult concepts with time and practice.",
            "My worth is not defined by my grades or performance.",
            "I belong in computer science just as much as anyone else.",
            "Making mistakes is how I learn and grow stronger.",
            "I don't need to know everything right away - learning is a journey.",
            "I have unique perspectives and ideas that are valuable to my field.",
            "I can overcome challenges by breaking them into smaller steps.",
            "Asking for help shows wisdom, not weakness.",
            "I am resilient and can adapt to new challenges.",
            "Today I choose to focus on progress, not perfection.",
            "I trust my ability to figure things out even when they seem difficult.",
            "I celebrate my small victories along the learning path.",
            "My voice and ideas matter in group discussions and projects.",
            "I am building skills that grow stronger with every challenge.",
            "I approach problems with curiosity instead of fear."
        ]
        
        # Thought challenges (CBT-inspired exercises)
        self.thought_challenges = [
            {
                "prompt": "When I don't understand a concept immediately, it means...",
                "options": [
                    "I'm not smart enough for this field.",
                    "This is a normal part of learning something complex."
                ],
                "correct": 1,
                "feedback": [
                    "Everyone feels lost sometimes! Complex subjects take time to understand. Einstein said, 'It's not that I'm so smart, it's just that I stay with problems longer.'",
                    "Exactly! Learning complex subjects takes time for everyone. Even experienced programmers constantly learn new things and feel confused sometimes."
                ]
            },
            {
                "prompt": "When I see others in my class who seem to understand everything...",
                "options": [
                    "They probably have moments of confusion too, I just don't see it.",
                    "They must be naturally smarter than me, so I'll never catch up."
                ],
                "correct": 0,
                "feedback": [
                    "That's right! Everyone struggles, but we usually only see others' successes, not their struggles. Many of your classmates probably feel exactly like you do.",
                    "Actually, what looks like 'natural talent' is usually just prior experience or practice behind the scenes. Your classmates have their own struggles you don't see."
                ]
            },
            {
                "prompt": "When I need to ask for help in class or office hours...",
                "options": [
                    "It shows I'm not cut out for computer science.",
                    "It shows I'm taking active steps to learn and grow."
                ],
                "correct": 1,
                "feedback": [
                    "Asking questions is actually a sign of intelligence and engagement! Professional programmers ask questions and seek help constantly.",
                    "Exactly! The best students and professionals are those who know when to seek help. It's an essential skill in any field."
                ]
            },
            {
                "prompt": "When I compare myself to more experienced programmers...",
                "options": [
                    "I should feel bad that I'm not at their level yet.",
                    "I should remember they all started where I am now."
                ],
                "correct": 1,
                "feedback": [
                    "Comparison is rarely helpful. Instead of feeling bad, try to be inspired by what's possible with time and practice. Everyone starts as a beginner!",
                    "That's right! Every expert was once a beginner. What matters is your own growth over time, not how you compare to others right now."
                ]
            },
            {
                "prompt": "When I make an error or my code doesn't work...",
                "options": [
                    "It's an opportunity to learn something new about how things work.",
                    "It proves I'm not detail-oriented enough for programming."
                ],
                "correct": 0,
                "feedback": [
                    "Exactly! Errors are learning opportunities. Professional developers make mistakes constantly - debugging is a normal part of the process.",
                    "Actually, making errors is universal in programming. Even the most senior developers make syntax errors and logical mistakes every day!"
                ]
            }
        ]
        
        # Randomly select today's content
        self.daily_affirmation = random.choice(self.affirmations)
        self.daily_challenge = random.choice(self.thought_challenges)
    
    def reset(self):
        """Reset scene state when returning to it"""
        self.current_step = 0
        self.affirm_done = self.game_manager.player_data.affirmation_done_today
        self.selected_option = None
        
        # Reset content if needed
        if not self.affirm_done:
            self.setup_content()
        
        # Set initial content
        self.update_content()
    
    def update_content(self):
        """Update the content panel based on current step"""
        if self.affirm_done:
            # Already completed today
            self.content_panel.set_messages(["You've already completed your affirmation for today!", 
                                           "\nCome back tomorrow for a new exercise.", 
                                           "\nRemember: growth takes time and consistent practice."])
            # Hide option buttons
            self.option1_button = None
            self.option2_button = None
            return
        
        if self.current_step == 0:
            # Introduction
            self.content_panel.set_messages(self.intro_text)
            # Hide option buttons
            self.option1_button = None
            self.option2_button = None
            
        elif self.current_step == 1:
            # Daily affirmation
            self.content_panel.set_messages(["Repeat this affirmation to yourself:\n", 
                                           f"\n{self.daily_affirmation}", 
                                           "\n\n(Try saying it out loud three times)"])
            # Hide option buttons
            self.option1_button = None
            self.option2_button = None
            
        elif self.current_step == 2:
            # Thought challenge
            self.content_panel.set_messages(["Let's challenge negative thoughts:\n", 
                                           f"\n{self.daily_challenge['prompt']}", 
                                           "\n\nWhich response is more helpful?"])
            # Show and update option buttons
            if self.option1_button and self.option2_button:
                self.option1_button.text = self.daily_challenge['options'][0]
                self.option2_button.text = self.daily_challenge['options'][1]
            else:
                # Recreate buttons if they were hidden
                button_width = self.content_panel.rect.width // 2 - 20
                button_height = 60
                button_spacing = 20
                button_y = self.content_panel.rect.bottom + 20
                
                # Option 1 button
                option1_x = self.content_panel.rect.left
                self.option1_button = Button(
                    option1_x, button_y, button_width, button_height,
                    self.daily_challenge['options'][0], self.game_manager.small_font,
                    lambda: self.select_option(0),
                    color=(150, 150, 220), hover_color=(180, 180, 250)
                )
                
                # Option 2 button
                option2_x = self.content_panel.rect.left + button_width + button_spacing
                self.option2_button = Button(
                    option2_x, button_y, button_width, button_height,
                    self.daily_challenge['options'][1], self.game_manager.small_font,
                    lambda: self.select_option(1),
                    color=(150, 150, 220), hover_color=(180, 180, 250)
                )
            
        elif self.current_step == 3:
            # Feedback on thought challenge
            correct = self.daily_challenge['correct']
            user_correct = self.selected_option == correct
            
            feedback = self.daily_challenge['feedback'][self.selected_option]
            
            if user_correct:
                self.content_panel.set_messages(["Great choice!\n", 
                                               f"\n{feedback}", 
                                               "\n\nThis kind of positive self-talk makes a real difference over time."])
            else:
                self.content_panel.set_messages(["Let's reframe that thought:\n", 
                                               f"\n{feedback}", 
                                               "\n\nIt's natural to have negative thoughts sometimes, but we can practice replacing them."])
            
            # Hide option buttons
            self.option1_button = None
            self.option2_button = None
            
        elif self.current_step == 4:
            # Completion
            self.content_panel.set_messages(["Great job completing today's affirmation!\n", 
                                           "\nRegular practice of positive self-talk helps build confidence", 
                                           "\nand resilience over time - just like watering your plant!"])
            # Hide option buttons
            self.option1_button = None
            self.option2_button = None
            
            # Mark as completed if not already done
            if not self.affirm_done:
                self.game_manager.player_data.complete_affirmation()
                self.affirm_done = True
                
                # Play sound
                if 'grow' in self.game_manager.sounds:
                    self.game_manager.sounds['grow'].play()
    
    def handle_event(self, event):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
        
        # Handle buttons
        self.next_button.update(mouse_pos, mouse_clicked)
        self.back_button.update(mouse_pos, mouse_clicked)
        
        # Handle option buttons if visible
        if self.current_step == 2 and self.option1_button and self.option2_button:
            self.option1_button.update(mouse_pos, mouse_clicked)
            self.option2_button.update(mouse_pos, mouse_clicked)
    
    def update(self):
        """Update scene state"""
        # Nothing to update regularly in this scene
        pass
    
    def draw(self, surface):
        """Draw the scene"""
        # Draw main background panel
        self.main_panel.draw(surface)
        
        # Draw title
        title_surf = self.game_manager.title_font.render("Daily Affirmation", True, (50, 50, 100))
        title_rect = title_surf.get_rect(midtop=(self.screen_rect.centerx, self.main_panel.rect.top + 20))
        surface.blit(title_surf, title_rect)
        
        # Draw content panel
        self.content_panel.draw(surface)
        
        # Draw option buttons if visible
        if self.current_step == 2 and self.option1_button and self.option2_button:
            self.option1_button.draw(surface)
            self.option2_button.draw(surface)
        
        # Draw navigation buttons
        self.next_button.draw(surface)
        self.back_button.draw(surface)
    
    def select_option(self, option_index):
        """Handle option selection for thought challenge"""
        self.selected_option = option_index
        
        # Highlight selected button
        if option_index == 0 and self.option1_button:
            self.option1_button.color = (100, 200, 100)
            self.option1_button.hover_color = (130, 230, 130)
            if self.option2_button:
                self.option2_button.color = (150, 150, 220)
                self.option2_button.hover_color = (180, 180, 250)
        elif option_index == 1 and self.option2_button:
            self.option2_button.color = (100, 200, 100)
            self.option2_button.hover_color = (130, 230, 130)
            if self.option1_button:
                self.option1_button.color = (150, 150, 220)
                self.option1_button.hover_color = (180, 180, 250)
        
        # Play sound
        if 'click' in self.game_manager.sounds:
            self.game_manager.sounds['click'].play()
    
    def next_step(self):
        """Move to the next step in the exercise"""
        # Only proceed if an option is selected when required
        if self.current_step == 2 and self.selected_option is None:
            return
            
        if self.affirm_done or self.current_step < 4:
            self.current_step += 1
            
            # Loop back to start if at the end
            if self.current_step > 4:
                self.go_back()
                return
                
            # Update content for the new step
            self.update_content()
            
            # Play sound
            if 'click' in self.game_manager.sounds:
                self.game_manager.sounds['click'].play()
    
    def go_back(self):
        """Return to main scene"""
        self.game_manager.change_scene('main')
