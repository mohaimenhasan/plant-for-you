"""
Simple build script that uses a more direct approach to bundle the game.
"""

import PyInstaller.__main__

# Run PyInstaller with appropriate arguments
PyInstaller.__main__.run([
    '--name=MotivaPlant',
    '--onefile',
    '--windowed',
    '--clean',
    '--add-data=assets;assets',
    '--hidden-import=pygame',
    '--hidden-import=pygame.mixer',
    '--hidden-import=pygame.font',
    '--hidden-import=pygame.image',
    '--hidden-import=pygame.display',
    '--hidden-import=pygame.time',
    '--hidden-import=pygame.mixer_music',
    '--hidden-import=numpy',
    '--hidden-import=pyglet',
    '--hidden-import=PIL',
    '--hidden-import=PIL.Image',
    'main.py',
])

print("\nBuild complete!")
print("The executable is in the 'dist' folder.")
print("To distribute, share the entire 'dist' folder with the executable.")