import pygame

class Panel:
    """A Minecraft-styled panel with 3D borders"""
    
    def __init__(self, x, y, width, height, color=(200, 200, 200), border_color=(50, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.border_color = border_color
        self.border_size = 4
        self.shadow_offset = 6
    
    def draw(self, surface):
        # Draw shadow for 3D effect
        shadow_rect = pygame.Rect(self.rect.x + self.shadow_offset, 
                                 self.rect.y + self.shadow_offset,
                                 self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (20, 20, 20, 100), shadow_rect, border_radius=2)  # Shadow
        
        # Draw panel background
        pygame.draw.rect(surface, self.color, self.rect, border_radius=2)  # Main panel
        
        # Draw borders - Minecraft style with darker edges
        # Top and left borders (lighter)
        pygame.draw.line(surface, (255, 255, 255, 150), 
                         (self.rect.left, self.rect.top), 
                         (self.rect.right, self.rect.top), 2)  # Top
        pygame.draw.line(surface, (255, 255, 255, 150), 
                         (self.rect.left, self.rect.top), 
                         (self.rect.left, self.rect.bottom), 2)  # Left
        
        # Bottom and right borders (darker)
        pygame.draw.line(surface, self.border_color, 
                         (self.rect.left, self.rect.bottom-1), 
                         (self.rect.right, self.rect.bottom-1), 2)  # Bottom
        pygame.draw.line(surface, self.border_color, 
                         (self.rect.right-1, self.rect.top), 
                         (self.rect.right-1, self.rect.bottom), 2)  # Right

class MessagePanel(Panel):
    """A panel with text content and optional title"""
    
    def __init__(self, x, y, width, height, font, title=None, title_font=None, 
                 color=(200, 200, 200), text_color=(20, 20, 20)):
        super().__init__(x, y, width, height, color)
        self.font = font
        self.title_font = title_font if title_font else font
        self.title = title
        self.text_color = text_color
        self.messages = []
        self.padding = 15
        self.line_spacing = 5
        
        # For scrolling long message lists
        self.scroll_offset = 0
        self.max_visible_lines = 0
        self.calculate_visible_lines()
    
    def calculate_visible_lines(self):
        """Calculate how many lines can be displayed at once"""
        available_height = self.rect.height - 2 * self.padding
        if self.title:
            title_height = self.title_font.render(self.title, True, self.text_color).get_height()
            available_height -= title_height + self.line_spacing * 2
        
        line_height = self.font.render("Test", True, self.text_color).get_height()
        self.max_visible_lines = available_height // (line_height + self.line_spacing)
    
    def set_messages(self, messages):
        """Set the list of messages to display"""
        self.messages = messages
        self.scroll_offset = 0  # Reset scroll position
    
    def add_message(self, message):
        """Add a single message to the panel"""
        self.messages.append(message)
    
    def scroll(self, amount):
        """Scroll the message panel"""
        max_offset = max(0, len(self.messages) - self.max_visible_lines)
        self.scroll_offset = max(0, min(self.scroll_offset + amount, max_offset))
    
    def draw(self, surface):
        # Draw the panel background and border
        super().draw(surface)
        
        # Draw title if provided
        y_offset = self.padding
        if self.title:
            title_surf = self.title_font.render(self.title, True, self.text_color)
            title_rect = title_surf.get_rect(midtop=(self.rect.centerx, self.rect.top + self.padding))
            surface.blit(title_surf, title_rect)
            y_offset = title_rect.bottom + self.line_spacing * 2
        
        # Draw messages with word wrapping
        visible_messages = self.messages[self.scroll_offset:self.scroll_offset + self.max_visible_lines]
        for message in visible_messages:
            # Simple word wrap - split by newlines first
            for line in message.split('\n'):
                # Check if line needs wrapping
                words = line.split()
                if not words:
                    y_offset += self.font.get_height() + self.line_spacing
                    continue
                    
                current_line = words[0]
                for word in words[1:]:
                    # Test if adding this word exceeds the width
                    test_line = current_line + " " + word
                    width = self.font.render(test_line, True, self.text_color).get_width()
                    
                    if width < self.rect.width - 2 * self.padding:
                        current_line = test_line  # Word fits, add it
                    else:
                        # Render current line and start new line
                        text_surf = self.font.render(current_line, True, self.text_color)
                        text_rect = text_surf.get_rect(left=self.rect.left + self.padding, top=y_offset)
                        surface.blit(text_surf, text_rect)
                        
                        y_offset += text_surf.get_height() + self.line_spacing
                        current_line = word
                
                # Render the last line
                if current_line:
                    text_surf = self.font.render(current_line, True, self.text_color)
                    text_rect = text_surf.get_rect(left=self.rect.left + self.padding, top=y_offset)
                    surface.blit(text_surf, text_rect)
                    y_offset += text_surf.get_height() + self.line_spacing
            
            # Add extra spacing between messages
            y_offset += self.line_spacing
            
        # Draw scroll indicators if needed
        if len(self.messages) > self.max_visible_lines:
            if self.scroll_offset > 0:
                # Draw up arrow
                pygame.draw.polygon(surface, (50, 50, 50), [
                    (self.rect.right - 20, self.rect.top + 15),
                    (self.rect.right - 10, self.rect.top + 5),
                    (self.rect.right - 30, self.rect.top + 5)
                ])
            
            if self.scroll_offset + self.max_visible_lines < len(self.messages):
                # Draw down arrow
                pygame.draw.polygon(surface, (50, 50, 50), [
                    (self.rect.right - 20, self.rect.bottom - 15),
                    (self.rect.right - 10, self.rect.bottom - 5),
                    (self.rect.right - 30, self.rect.bottom - 5)
                ])
