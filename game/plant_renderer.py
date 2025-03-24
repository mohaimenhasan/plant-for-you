import pygame
import math
import random

class PlantRenderer:
    """Renders the plant in a Minecraft-inspired blocky pixel art style"""
    
    def __init__(self, screen_rect):
        self.screen_rect = screen_rect
        self.plant_levels = 10  # Maximum plant growth levels
        self.colors = {
            'pot': (140, 90, 40),  # Brown
            'pot_highlight': (160, 110, 60),
            'pot_shadow': (120, 70, 30),
            'soil': (80, 50, 30),  # Dark brown
            'plant_stem': (60, 160, 60),  # Green
            'plant_leaf': (100, 200, 100),  # Light green
            'plant_highlight': (150, 230, 150),  # Lighter green for highlights
            'flower': (230, 150, 220),  # Pink/purple
            'flower_center': (250, 230, 100),  # Yellow
        }
        
        # Calculate dimensions
        self.pot_width = min(screen_rect.width // 4, 150)
        self.pot_height = self.pot_width // 2
        self.plant_base_width = self.pot_width // 3
        
        # Animation variables
        self.sway_angle = 0
        self.sway_speed = 0.03
        self.sway_amount = 5
        
        # Particle effects for watering
        self.water_particles = []
        self.particle_timer = 0
        
        self.growth_flash = 0  # Flash effect for growth
        
    def update(self, dt):
        """Update animation variables"""
        # Update plant swaying
        self.sway_angle += self.sway_speed * dt
        
        # Update particles
        self.particle_timer -= dt
        if self.particle_timer <= 0:
            self.water_particles = [p for p in self.water_particles if p['life'] > 0]
        
        for particle in self.water_particles:
            particle['y'] += particle['speed'] * dt
            particle['life'] -= dt * 0.5
            
        # Update growth flash
        if self.growth_flash > 0:
            self.growth_flash -= dt * 0.05
    
    def add_water_effect(self):
        """Add water particle effect"""
        self.particle_timer = 600  # milliseconds
        
        # Create water droplets
        pot_center_x = self.screen_rect.centerx
        pot_top_y = self.screen_rect.centery + self.pot_height // 2
        
        for _ in range(20):
            self.water_particles.append({
                'x': pot_center_x + random.randint(-self.pot_width//2, self.pot_width//2),
                'y': pot_top_y - random.randint(100, 200),
                'speed': random.uniform(0.1, 0.3),
                'size': random.randint(2, 5),
                'life': random.uniform(0.5, 1.0)
            })
    
    def add_growth_effect(self):
        """Add growth flash effect"""
        self.growth_flash = 1.0
    
    def draw(self, surface, plant_level, growth_progress):
        """Draw the plant at the given growth level and progress"""
        center_x = self.screen_rect.centerx
        base_y = self.screen_rect.centery + self.pot_height // 2
        
        # Calculate current growth
        effective_level = plant_level - 1 + growth_progress
        
        # Draw pot (3D blocky style)
        self._draw_pot(surface, center_x, base_y)
        
        # Draw soil
        soil_rect = pygame.Rect(
            center_x - self.pot_width//2 + 10,
            base_y - 10,
            self.pot_width - 20,
            20
        )
        pygame.draw.rect(surface, self.colors['soil'], soil_rect)
        
        # Draw plant based on level
        if effective_level > 0:
            self._draw_plant(surface, center_x, base_y, effective_level)
        
        # Draw water particles
        for particle in self.water_particles:
            alpha = int(255 * particle['life'])
            color = (100, 150, 255, alpha)
            pygame.draw.circle(
                surface, 
                color, 
                (int(particle['x']), int(particle['y'])), 
                int(particle['size'])
            )
    
    def _draw_pot(self, surface, center_x, base_y):
        """Draw the Minecraft-style blocky pot"""
        # Main pot body
        pot_rect = pygame.Rect(
            center_x - self.pot_width // 2,
            base_y - self.pot_height,
            self.pot_width,
            self.pot_height
        )
        pygame.draw.rect(surface, self.colors['pot'], pot_rect)
        
        # 3D effect with highlights and shadows
        # Top highlight
        pygame.draw.line(
            surface,
            self.colors['pot_highlight'],
            (center_x - self.pot_width // 2, base_y - self.pot_height),
            (center_x + self.pot_width // 2, base_y - self.pot_height),
            3
        )
        
        # Left highlight
        pygame.draw.line(
            surface,
            self.colors['pot_highlight'],
            (center_x - self.pot_width // 2, base_y - self.pot_height),
            (center_x - self.pot_width // 2, base_y),
            3
        )
        
        # Bottom shadow
        pygame.draw.line(
            surface,
            self.colors['pot_shadow'],
            (center_x - self.pot_width // 2, base_y),
            (center_x + self.pot_width // 2, base_y),
            3
        )
        
        # Right shadow
        pygame.draw.line(
            surface,
            self.colors['pot_shadow'],
            (center_x + self.pot_width // 2, base_y - self.pot_height),
            (center_x + self.pot_width // 2, base_y),
            3
        )
        
        # Pot rim
        rim_rect = pygame.Rect(
            center_x - self.pot_width // 2 - 5,
            base_y - self.pot_height - 8,
            self.pot_width + 10,
            10
        )
        pygame.draw.rect(surface, self.colors['pot_shadow'], rim_rect)
    
    def _draw_plant(self, surface, center_x, base_y, level):
        """Draw the plant with Minecraft-inspired blocky style"""
        stem_base_x = center_x
        stem_base_y = base_y - 10  # Just above the soil
        
        # Calculate stem height based on level
        max_stem_height = 300
        stem_height = int(max_stem_height * (level / self.plant_levels))
        
        # Apply swaying effect
        sway = math.sin(self.sway_angle) * self.sway_amount
        
        # Apply growth flash effect
        highlight_factor = self.growth_flash * 50
        stem_color = tuple(min(255, c + int(highlight_factor)) for c in self.colors['plant_stem'])
        leaf_color = tuple(min(255, c + int(highlight_factor)) for c in self.colors['plant_leaf'])
        
        # Draw main stem
        stem_width = max(6, int(8 * (1 - level / self.plant_levels * 0.5)))  # Stem gets thinner as it grows
        stem_points = [
            (stem_base_x, stem_base_y)  # Base point
        ]
        
        # Create a slightly curved stem path
        segments = int(stem_height / 20)
        for i in range(1, segments + 1):
            segment_sway = sway * (i / segments) ** 2  # More sway at the top
            point_y = stem_base_y - (i * stem_height / segments)
            point_x = stem_base_x + segment_sway
            stem_points.append((point_x, point_y))
        
        # Draw stem segments
        for i in range(len(stem_points) - 1):
            pygame.draw.line(
                surface,
                stem_color,
                stem_points[i],
                stem_points[i+1],
                stem_width
            )
        
        # Draw leaves based on growth level
        num_leaf_pairs = min(5, int(level))
        leaf_size_base = 10
        
        for i in range(num_leaf_pairs):
            # Calculate leaf position along stem
            position_factor = 0.2 + (i / num_leaf_pairs) * 0.6  # Distribute leaves along stem
            index = min(len(stem_points) - 1, int(position_factor * len(stem_points)))
            
            leaf_center_x = stem_points[index][0]
            leaf_center_y = stem_points[index][1]
            
            # Leaf size grows with level
            leaf_growth = min(1.0, level / 5)  # Max size by level 5
            leaf_size = int(leaf_size_base + leaf_size_base * 2 * leaf_growth)
            
            # Alternate leaf directions
            left_leaf_angle = 180 + 20 + math.sin(self.sway_angle) * 5
            right_leaf_angle = 0 - 20 + math.sin(self.sway_angle) * 5
            
            # Draw left leaf
            self._draw_leaf(surface, leaf_center_x, leaf_center_y, leaf_size, left_leaf_angle, leaf_color)
            
            # Draw right leaf
            self._draw_leaf(surface, leaf_center_x, leaf_center_y, leaf_size, right_leaf_angle, leaf_color)
        
        # Draw flowers or fruit at higher levels
        if level >= 7:
            # Top of the plant
            top_x, top_y = stem_points[-1]
            
            # Draw a flower
            flower_size = int(15 + 10 * min(1.0, (level - 7) / 3))
            flower_color = self.colors['flower']
            
            # Draw petals
            for angle in range(0, 360, 60):
                petal_angle = angle + math.sin(self.sway_angle) * 5
                rad = math.radians(petal_angle)
                petal_x = top_x + math.cos(rad) * flower_size * 0.7
                petal_y = top_y + math.sin(rad) * flower_size * 0.7
                
                pygame.draw.circle(surface, flower_color, (int(petal_x), int(petal_y)), flower_size // 2)
            
            # Draw center
            pygame.draw.circle(surface, self.colors['flower_center'], (int(top_x), int(top_y)), flower_size // 3)
    
    def _draw_leaf(self, surface, center_x, center_y, size, angle, color):
        """Draw a single blocky leaf"""
        # For Minecraft style, we'll use rectangles for leaves
        rad = math.radians(angle)
        leaf_x = center_x + math.cos(rad) * size * 1.5
        leaf_y = center_y + math.sin(rad) * size * 1.5
        
        # Create a leaf polygon
        points = [
            (center_x, center_y),  # Stem connection point
            (leaf_x, leaf_y),  # Leaf tip
            (leaf_x + math.cos(rad + math.pi/4) * size, 
             leaf_y + math.sin(rad + math.pi/4) * size),  # Corner 1
            (leaf_x + math.cos(rad - math.pi/4) * size,
             leaf_y + math.sin(rad - math.pi/4) * size),  # Corner 2
        ]
        
        pygame.draw.polygon(surface, color, points)
        
        # Add vein
        pygame.draw.line(
            surface, 
            self.colors['plant_stem'],
            (center_x, center_y),
            (leaf_x, leaf_y),
            2
        )
