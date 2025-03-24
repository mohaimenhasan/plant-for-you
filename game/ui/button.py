import pygame

class Button:
    """Interactive button UI component with Minecraft-inspired style"""
    
    def __init__(self, x, y, width, height, text, font, action=None, 
                 hover_color=(158, 214, 125), color=(100, 180, 100), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False
        
        # Minecraft-style button has a border and different states
        self.border_size = 2
        self.shadow_offset = 4
        self.pressed = False
    
    def draw(self, surface):
        # Draw button shadow (3D effect)
        shadow_rect = pygame.Rect(self.rect.x, self.rect.y + self.shadow_offset, 
                                 self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (30, 30, 30), shadow_rect)  # Dark shadow
        
        # Draw main button
        current_color = self.hover_color if self.hovered else self.color
        offset = 2 if self.pressed else 0
        button_rect = pygame.Rect(self.rect.x, self.rect.y + offset, 
                                 self.rect.width, self.rect.height)
        
        pygame.draw.rect(surface, current_color, button_rect)  # Button fill
        pygame.draw.rect(surface, (30, 30, 30), button_rect, self.border_size)  # Border
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=button_rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self, mouse_pos, clicked=False):
        # Check if mouse is over button
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Handle button press and release
        if self.hovered and clicked:
            self.pressed = True
            if self.action:
                self.action()
            return True
        elif not clicked:
            self.pressed = False
        
        return False

class TextButton(Button):
    """Text-only button variant with subtle highlighting"""
    
    def __init__(self, x, y, text, font, action=None, 
                 hover_color=(255, 255, 150), color=(255, 255, 255)):
        # Calculate width based on text
        text_surf = font.render(text, True, color)
        width = text_surf.get_width() + 20  # Add padding
        height = text_surf.get_height() + 10  # Add padding
        
        super().__init__(x, y, width, height, text, font, action, 
                         hover_color=hover_color, color=color, text_color=(0, 0, 0))
        
        # Text buttons are more subtle
        self.border_size = 0
        self.shadow_offset = 2
    
    def draw(self, surface):
        # Text-only buttons just draw the text with a hover effect
        current_color = self.hover_color if self.hovered else self.color
        text_surf = self.font.render(self.text, True, current_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
