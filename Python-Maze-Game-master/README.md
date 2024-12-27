## Project Name: 迷宮寶石王​
## Creators: Jian (Henry) Wee and Darren Tran
## Modifier: D1349095顏宏育、D1349362張政諺​、D1348863黃鼎堯、D1349290許仲佑 
## 哲維大帥哥

	
**HOW TO MOVE:**
* Use UP and DOWN arrow keys to navigate around main screen and settings. 
* Use ENTER key to select an option.
* Use LEFT and RIGHT arrow keys to change settings 

**GRID SIZE:**
 * Changes the size of the maze, ranges from 10 - 35 units. 

**SIDE LENGTH:**
 * Scales the size of the screen, ranges from 10 - 15 units

**NOTES:**
 * Once a game has been played, the settings will not be saved and will have to be selected again. 
 * Use ESC key to exit current game. 

# CODE STRUCTURE
**main.py:** 
 * Contains game mechanics and maze generation

**astar.py:**
 * astar algorithm that is used to calculate shortest path, running time of O(|E|log|E|)

**character.py:**
 * Contains character class for movement of character and game objectives

**ui_file.py:**
 * Contains code for main screen, settings and end game screen

**graph.py**
 * From lecture, aids in the generation of the maze.

# HOW TO RUN
1. If pygame is not installed, install pygame package by calling  'sudo pip3 install pygame' for systems running Ubuntu
2. run by calling 'python3 main.py' in terminal

