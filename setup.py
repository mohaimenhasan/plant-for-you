from setuptools import setup, find_packages

setup(
    name="MotivaPlant",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.0",
        "pyglet>=2.0.0",
        "pillow>=10.0.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.25.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A motivational plant game to help with confidence and mindset",
    keywords="game, motivation, plant, minecraft",
    python_requires=">=3.8",
)