import pygame

class TextInput:
    """Text input field with Minecraft-inspired styling"""
    
    def __init__(self, x, y, width, height, font, placeholder="Type here...", 
                 max_length=100, border_color=(30, 30, 30), bg_color=(220, 220, 220)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.text = ""
        self.placeholder = placeholder
        self.max_length = max_length
        self.border_color = border_color
        self.bg_color = bg_color
        self.active = False
        self.cursor_pos = 0
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_speed = 500  # milliseconds
        
        # Scrolling text handling
        self.text_offset = 0
        self.visible_width = width - 20  # Padding
    
    def draw(self, surface):
        # Draw border with 3D effect (Minecraft style)
        border_rect = pygame.Rect(self.rect.x - 2, self.rect.y - 2, 
                                 self.rect.width + 4, self.rect.height + 4)
        pygame.draw.rect(surface, (0, 0, 0), border_rect)  # Outer border
        
        # Draw inset effect if active
        if self.active:
            inset_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, 
                                    self.rect.width + 2, self.rect.height + 2)
            pygame.draw.rect(surface, (100, 100, 255), inset_rect)  # Highlight color
        
        # Draw main background
        pygame.draw.rect(surface, self.bg_color, self.rect)  # Background
        
        # Draw text or placeholder
        if self.text:
            text_surf = self.font.render(self.text, True, (0, 0, 0))
            
            # Handle text scrolling if too long
            text_width = text_surf.get_width()
            if text_width > self.visible_width:
                # Calculate cursor position in pixels
                cursor_text = self.text[:self.cursor_pos]
                cursor_pos_pixels = self.font.render(cursor_text, True, (0, 0, 0)).get_width()
                
                # Adjust offset to keep cursor visible
                if cursor_pos_pixels - self.text_offset > self.visible_width:
                    self.text_offset = cursor_pos_pixels - self.visible_width + 10
                elif cursor_pos_pixels < self.text_offset:
                    self.text_offset = max(0, cursor_pos_pixels - 10)
                
                # Create a subsurface for clipping
                text_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 
                                       self.visible_width, self.rect.height - 10)
                
                # Use clipping to only show visible portion
                old_clip = surface.get_clip()
                surface.set_clip(text_rect)
                surface.blit(text_surf, (text_rect.x - self.text_offset, text_rect.y))
                surface.set_clip(old_clip)
            else:
                # Text fits, no scrolling needed
                surface.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))
            
            # Draw cursor if active and visible
            if self.active and self.cursor_visible:
                cursor_text = self.text[:self.cursor_pos]
                cursor_x = self.rect.x + 5 + self.font.render(cursor_text, True, (0, 0, 0)).get_width() - self.text_offset
                
                # Only draw cursor if it's in the visible area
                if cursor_x >= self.rect.x and cursor_x <= self.rect.x + self.rect.width:
                    pygame.draw.line(surface, (0, 0, 0), 
                                    (cursor_x, self.rect.y + 5), 
                                    (cursor_x, self.rect.y + self.rect.height - 5), 2)
        else:
            # Draw placeholder text
            placeholder_surf = self.font.render(self.placeholder, True, (100, 100, 100))
            surface.blit(placeholder_surf, (self.rect.x + 5, self.rect.y + 5))
    
    def update(self, events):
        # Handle cursor blinking
        self.cursor_timer += pygame.time.get_ticks() % 60  # Add time since last frame
        if self.cursor_timer >= self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        # Process events
        for event in events:
            # Mouse click activates/deactivates the input field
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    # Set cursor position based on click position
                    click_x = event.pos[0] - self.rect.x - 5 + self.text_offset
                    self.cursor_pos = len(self.text)
                    
                    # Find best cursor position based on click
                    if self.text:
                        best_dist = float('inf')
                        for i in range(len(self.text) + 1):
                            text_width = self.font.render(self.text[:i], True, (0, 0, 0)).get_width()
                            dist = abs(text_width - click_x)
                            if dist < best_dist:
                                best_dist = dist
                                self.cursor_pos = i
                else:
                    self.active = False
            
            # Handle keyboard input when active
            elif event.type == pygame.KEYDOWN and self.active:
                # Navigation keys
                if event.key == pygame.K_LEFT:
                    self.cursor_pos = max(0, self.cursor_pos - 1)
                    self.cursor_visible = True
                    self.cursor_timer = 0
                elif event.key == pygame.K_RIGHT:
                    self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
                    self.cursor_visible = True
                    self.cursor_timer = 0
                elif event.key == pygame.K_HOME:
                    self.cursor_pos = 0
                    self.cursor_visible = True
                    self.cursor_timer = 0
                elif event.key == pygame.K_END:
                    self.cursor_pos = len(self.text)
                    self.cursor_visible = True
                    self.cursor_timer = 0
                
                # Editing keys
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                        self.cursor_pos -= 1
                        self.cursor_visible = True
                        self.cursor_timer = 0
                elif event.key == pygame.K_DELETE:
                    if self.cursor_pos < len(self.text):
                        self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
                        self.cursor_visible = True
                        self.cursor_timer = 0
                
                # Normal character input
                elif event.unicode and len(self.text) < self.max_length:
                    # Filter out control characters
                    if ord(event.unicode) >= 32:
                        self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                        self.cursor_pos += 1
                        self.cursor_visible = True
                        self.cursor_timer = 0
        
        return self.text
    
    def get_text(self):
        return self.text
    
    def set_text(self, text):
        self.text = text
        self.cursor_pos = len(text)
    
    def clear(self):
        self.text = ""
        self.cursor_pos = 0
