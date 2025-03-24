# MotivaPlant 🌱

A cute Minecraft-inspired motivational plant game designed to help build confidence, encourage self-reflection, and practice positive self-talk. Perfect for CS students experiencing imposter syndrome or anyone who needs a daily boost of positivity.

## Features

- **Interactive Plant Growth**: Water your plant daily to help it grow
- **Daily Affirmations**: Complete daily positive self-talk exercises to boost growth
- **Thought Challenges**: Practice reframing negative thoughts into positive ones
- **Reflective Journaling**: Record thoughts and respond to prompts to promote growth
- **Growth Tracking**: Watch your plant evolve through 10 stages as you care for it
- **Cute Minecraft-Inspired Graphics**: Blocky, adorable visuals with a soothing aesthetic

## Installation

### Option 1: Run as an Executable (Windows)

1. Download the MotivaPlant executable file
2. Double-click to run it - no installation required!

### Option 2: Run from Source (Developers)

1. Make sure you have Python 3.8 or higher installed
2. Clone or download this repository
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Download the required assets following the instructions in `ASSETS.md`
5. Run the game:

```bash
python run_game.py
```

## Building the Executable

To create a standalone executable that can run without Python installed:

1. Install the build requirements:

```bash
pip install -r requirements.txt
pip install pyinstaller pillow
```

2. Create the application icon:

```bash
python create_icon.py
```

3. Build the executable:

```bash
python build_exe.py
```

4. The executable will be created in the `dist` folder
5. Copy the entire `dist` folder to share the application

## How to Play

- **Main Screen**: This is where you'll see your growing plant
- **Water Plant**: Click once daily to water your plant and boost its growth
- **Daily Affirmation**: Complete a positive self-talk exercise to strengthen your mindset
- **Journal**: Record your thoughts and reflect on prompts to process experiences

## Daily Activities

For the best experience and maximum plant growth:

1. **Water your plant daily** - This represents basic self-care and consistency
2. **Complete daily affirmations** - Practice positive self-talk to reframe negative thoughts
3. **Journal regularly** - Self-reflection helps process experiences and clarify thoughts

## Motivation

This app was created to provide a gentle, nurturing way to practice self-compassion and build confidence. It's especially designed for CS students experiencing imposter syndrome, but can help anyone working through self-doubt or anxiety.

The growth of your plant mirrors your own growth journey - requiring patience, consistent care, and self-kindness.

## Requirements

- Python 3.8+
- pygame 2.5.0+
- pyglet 2.0.0+
- pillow 10.0.0+
- numpy 1.25.0+

## License

This project is open-source and free to use, modify, and share.

---

Remember: Just like your plant, growth takes time. Be patient with yourself! ❤️