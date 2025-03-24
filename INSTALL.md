# Installation Guide for MotivaPlant

This guide provides detailed instructions for installing and running MotivaPlant.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Option 1: Using a Virtual Environment (Recommended)

Using a virtual environment is recommended to avoid conflicts with other Python packages.

### On Windows:

```
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python run_game.py
```

### On macOS/Linux:

```
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python run_game.py
```

## Option 2: Direct Installation

If you prefer not to use a virtual environment, you can install the dependencies directly:

```
# Install dependencies
pip install -r requirements.txt

# Run the game
python run_game.py
```

## Assets

Before running the game, make sure to download the required assets:

1. Font: Download the Minecraft font from https://www.dafont.com/minecraft.font and save it to `assets/fonts/minecraft.ttf`
2. Sound effects: 
   - Download water.wav from https://freesound.org/people/Mafon2/sounds/371274/ and save to `assets/sounds/water.wav`
   - Download grow.wav from https://freesound.org/people/LittleRobotSoundFactory/sounds/270402/ and save to `assets/sounds/grow.wav`
   - Download click.wav from https://freesound.org/people/LittleRobotSoundFactory/sounds/270324/ and save to `assets/sounds/click.wav`

The game can run without these assets, but the experience will be better with them.

## Troubleshooting

### Missing modules

If you encounter "ModuleNotFoundError", make sure you've installed all required dependencies:

```
pip install -r requirements.txt
```

### Sound issues

If you encounter sound issues, the game will run without sound. To fix this, make sure:

1. Your system supports audio playback
2. The sound files are valid WAV files
3. The file paths are correct

### Font issues

If you encounter font issues, the game will use system fonts. To fix this, make sure:

1. You've downloaded the Minecraft font
2. The file is correctly placed at `assets/fonts/minecraft.ttf`

## Building an Executable

To create a standalone executable, follow these steps:

```
# Install PyInstaller
pip install pyinstaller

# Create icon (optional)
python create_icon.py

# Build the executable
python build_exe.py
```

The executable will be created in the `dist` folder.