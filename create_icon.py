"""
Create a simple plant icon for the application.
This script generates a basic plant icon to use for the executable.
"""

from PIL import Image, ImageDraw
import os

def create_plant_icon():
    """Create a simple plant icon"""
    # Create directories if they don't exist
    os.makedirs("assets/images", exist_ok=True)
    
    # Icon dimensions
    icon_size = 256
    
    # Create a new image with transparent background
    icon = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    
    # Colors
    pot_color = (140, 90, 40)
    soil_color = (80, 50, 30)
    stem_color = (60, 160, 60)
    leaf_color = (100, 200, 100)
    bg_color = (180, 220, 255, 180)  # Light blue semi-transparent
    
    # Draw background circle
    padding = 10
    draw.ellipse((padding, padding, icon_size - padding, icon_size - padding), 
                 fill=bg_color)
    
    # Draw pot
    pot_width = icon_size * 0.6
    pot_height = icon_size * 0.3
    pot_left = (icon_size - pot_width) / 2
    pot_top = icon_size - pot_height - 20
    draw.rectangle((pot_left, pot_top, pot_left + pot_width, pot_top + pot_height), 
                  fill=pot_color, outline=(80, 50, 20), width=3)
    
    # Draw soil
    soil_height = pot_height * 0.25
    draw.rectangle((pot_left + 5, pot_top, pot_left + pot_width - 5, pot_top + soil_height), 
                  fill=soil_color)
    
    # Draw plant stem
    stem_width = 10
    stem_height = icon_size * 0.5
    stem_left = icon_size / 2 - stem_width / 2
    stem_top = pot_top - stem_height
    draw.rectangle((stem_left, stem_top, stem_left + stem_width, pot_top), 
                  fill=stem_color)
    
    # Draw leaves
    # Leaf 1 (left)
    leaf_width = icon_size * 0.25
    leaf_height = icon_size * 0.15
    draw.ellipse((stem_left - leaf_width + 10, stem_top + stem_height * 0.3,
                 stem_left + 10, stem_top + stem_height * 0.3 + leaf_height), 
                fill=leaf_color)
    
    # Leaf 2 (right)
    draw.ellipse((stem_left + stem_width - 10, stem_top + stem_height * 0.5,
                 stem_left + stem_width + leaf_width - 10, stem_top + stem_height * 0.5 + leaf_height), 
                fill=leaf_color)
    
    # Leaf 3 (top left)
    draw.ellipse((stem_left - leaf_width * 0.7 + 10, stem_top + stem_height * 0.1,
                 stem_left + 10, stem_top + stem_height * 0.1 + leaf_height * 0.8), 
                fill=leaf_color)
    
    # Leaf 4 (top right)
    draw.ellipse((stem_left + stem_width - 10, stem_top + stem_height * 0.2,
                 stem_left + stem_width + leaf_width * 0.7 - 10, stem_top + stem_height * 0.2 + leaf_height * 0.8), 
                fill=leaf_color)
    
    # Save icon in multiple resolutions for Windows
    icon_sizes = [16, 32, 48, 64, 128, 256]
    icons = []
    
    for size in icon_sizes:
        resized_icon = icon.resize((size, size), Image.LANCZOS)
        icons.append(resized_icon)
    
    # Save as ICO file
    icon_path = "assets/images/icon.ico"
    icons[0].save(icon_path, format='ICO', sizes=[(s, s) for s in icon_sizes], append_images=icons[1:])
    
    # Also save as PNG for other uses
    icon.save("assets/images/icon.png", format='PNG')
    
    print(f"Icon created and saved to {icon_path}")

if __name__ == "__main__":
    try:
        create_plant_icon()
    except Exception as e:
        print(f"Error creating icon: {e}")
        print("You'll need to provide your own icon.ico file in assets/images/")