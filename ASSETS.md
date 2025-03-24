# Assets for MotivaPlant

To complete the game setup, you'll need to download these assets:

## Required Fonts

1. Download the Minecraft font:
   - URL: https://www.dafont.com/minecraft.font
   - Save it to: `assets/fonts/minecraft.ttf`

## Required Sound Effects

1. Download these sound effects (or use any similar .wav files you prefer):
   - Water sound: https://freesound.org/people/Mafon2/sounds/371274/
     - Save as: `assets/sounds/water.wav`
   - Growth/achievement sound: https://freesound.org/people/LittleRobotSoundFactory/sounds/270402/
     - Save as: `assets/sounds/grow.wav`
   - Click sound: https://freesound.org/people/LittleRobotSoundFactory/sounds/270324/
     - Save as: `assets/sounds/click.wav`

## Alternatives

If you prefer, you can replace these with any font or sound effects of your choice by changing the filenames in the code or using different assets.

## Creating Assets Package

To create a properly packaged game with all required assets:

1. Create the directory structure:
   ```
   assets/
     ├── fonts/
     ├── sounds/
     └── images/
   ```

2. Download the required assets mentioned above and place them in their corresponding folders.

3. Run the icon creation script to generate the application icon:
   ```
   python create_icon.py
   ```

## For Executable Distribution

When building the executable with `build_exe.py` or `build_windows_exe.bat`, the assets folder is automatically included. 

However, if any assets are missing when the executable is built, they'll be missing in the final application. 
Make sure all assets are in place before building the executable.