# Typing Cat Game

The Typing Cat Game is a fun and educational Python-based game designed to enhance players' typing skills while delivering an enjoyable gaming experience. Players are challenged to type words falling before they reach the bottom of the screen.

![Typing Cat Game Gif](/game/screenshot/game_gif.gif)

## Table of Contents
- [Introduction](#introduction)
- [Gameplay](#gameplay)
- [Installation](#installation)
- [Development](#development)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#disclaimer)
- [License](#license)

## Introduction
The Typing Cat Game is a fun and educational game designed to improve players' typing skills while providing an enjoyable gaming experience. Players are challenged to type the words falling before they reach the bottom of the screen.

### Motivation
The motivation for this project stemmed from the desire to practice touch typing in a fun way. While excellent tools are available, I perceived this as an opportunity to create something custom-made and hone my skills. Additionally, I chose to develop this project as the final assignment for my Harvard CS50 course.

## Gameplay
- **Objective**: Defeat enemies by typing the words falling before they reach the bottom of the screen.
- **Intro Screen**: The game starts with an introduction screen where you need to type "PLAY" to start the game or "QUIT" to exit.
- **Playing the Game**: Once in the game, control your cat's attacks by using the keyboard to type words displayed on the screen.
- **Defeating Enemies**: Type the correct words to defeat enemies. Be quick and accurate to prevent enemies from reaching you.

![Typing Cat Game Screenshot](/game/screenshot/screenshot.png)

### Additional Controls
- **ENTER Key**: Submit typed word
- **BACKSPACE Key**: Delete the last character in the input field

### Word List
You are free to update or import your own words.

1. Navigate to the words folder
2. Update the file or import your own (make sure to rename it as words.txt or change the path in the code)

### Setting the Difficulty
Right now, there is no way to change the difficulty in-game, but you can make the following changes to the code:

1. Locate the difficulty_control function.
2. Change the numbers for the range of enemy and word spawn.
3. The higher the min range, the less frequently a spawn will occur.
4. If you want fewer enemies, raise the values. For more words, do the opposite.

It is also possible to change the duration of the wave by accessing the GameProgress class.

## Installation
To set up the development environment and run the game, follow these steps:

1. Clone the repository to your local machine.
2. Install Python and Pygame.
3. Navigate to the project directory.
4. Run the game using the `main.py` file.

### Dependencies
- Python 3.11.6
- Pygame library

## Development
### Improvement opportunities
There are many features I would like to implement in the game to make it more appealing:

- Addition of more enemy waves
- Addition of a boss battle after the wave is defeated
- Handle enemy health individually per sprite
- Refactor the code to be able to implement a replay button without the need for calling main()
- Possibility to choose the difficulty level
- Inclusion of WPM statistics

If you're interested in contributing to the project, you can fork the repository, make your changes, and submit a pull request.

## Acknowledgements

First of all, I would like to acknowledge the creators of the Pygame library for providing the foundation for this game and so many others.

### Credits
- Background: [Free Pixel Art Forest](https://edermunizz.itch.io/free-pixel-art-forest)
- Player Sprite: [Cat Adventure](https://bdragon1727.itch.io/cat-adventure)
- Enemies Sprites: [Monsters Creatures Fantasy](https://luizmelo.itch.io/monsters-creatures-fantasy)
- Fonts: [PimpawCat Font](assets/fonts/PimpawCat-lg3dd.ttf), [Bohemian Typewriter Font](assets/fonts/bohemian-typewriter.regular.ttf)
- Sounds were downloaded from [Pixabay](https://pixabay.com/) and are all royalty-free

## Disclaimer
The Typing Cat Game was developed for educational purposes, with a focus on learning game development concepts and programming skills. As such, the game may not exhibit perfect balance in its mechanics, and the graphics may not have received extensive attention. The primary goal of this project was to explore and apply programming principles in a practical context.

Please note that while efforts have been made to create an enjoyable gaming experience, the game's design and features may not align with the standards of commercial or fully polished games. The Typing Cat Game serves as a learning exercise and a demonstration of programming techniques rather than a fully refined commercial product.

## License
This game is open-source and released under the [GNU General Public License (GPL)](LICENSE). Feel free to modify and distribute it as per the license terms.

**Enjoy playing Typing Cat!**