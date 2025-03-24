#!/usr/bin/env python
import os
import sys
import pygame
from game.game_manager import GameManager

def main():
    try:
        # Initialize pygame
        pygame.init()
        
        # Initialize mixer with error handling
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Warning: Could not initialize sound mixer: {e}")
            print("The game will run without sound.")
        
        # Set up the game window
        screen_width = 1280
        screen_height = 720
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("MotivaPlant - Grow Together")
        
        # Set icon for the window (commented out for now)
        # try:
        #     pygame.display.set_icon(pygame.image.load('assets/images/icon.png'))
        # except (FileNotFoundError, pygame.error):
        #     print("Warning: Could not load icon file.")
        
        # Create game manager
        game = GameManager(screen)
        
        # Main game loop
        running = True
        clock = pygame.time.Clock()
        
        while running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    game.handle_event(event)
            
            # Update game state
            game.update()
            
            # Draw everything
            screen.fill((62, 88, 156))  # Sky blue background
            game.draw()
            pygame.display.flip()
            
            # Cap the frame rate
            clock.tick(60)
        
        # Clean up
        pygame.quit()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Make sure we always clean up
        try:
            pygame.quit()
        except:
            pass
        sys.exit()

if __name__ == "__main__":
    main()
