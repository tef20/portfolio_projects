### Monty Hall  

This is an interactive game inspired by [The Monty Hall Problem](https://en.wikipedia.org/wiki/Monty_Hall_problem) -- a probability puzzle based on the classic, counterintuitive television game-show, Let's Make a Deal, whose host was Monty Hall.  

There are two versions of the game to play:
1. to play within your terminal, simply run MH_CLI_game.py
2. to play using a GUI, run MH_GUI_game.py  

#### Motivation  
* Make first 'from scratch' GUI application (having encountered tkinter library during Code in Place course)
* Practice OOP and building classes in Python (having encountered OOP style program structures in CS50ai)
* Practice planning and implementing reusable, expandable code, avoiding repetition and too many interdependencies 

#### Goals
* Make a game that was both fun and potentially educational
* Make CLI and GUI versions of the game, which interact with the same underlying class
* Produce a product within time constraints

#### Features
* Underlying game mechanics
* CLI gameplay
* GUI gameplay
* A doors class, representing a graphical door object

#### Assessment / Reflections  
##### Positives:  
Overall I am fairly pleased with this project.  
* I learned alot
* It accurately encodes the underlying dynamics of the game
* It can be played either as a CLI or GUI game (although not interchangeably)
* Many aspects of the project adhere to good design principles such as DRY (code and information)
* I expect it to be expandable in future

##### Ideas for further features:
* More educational features to help player improve probabilistic intuition 
  * Run n automated rounds, to show decision outcomes
  * Alternative scenario with n doors, to show impact Monty's decision
  * Decision tree visualisation 
* Better / more dynamic animations
* More engaging text to improve game play / player understanding

##### Areas for improvement:
* I would like to have incorporated more systematic testing, eg. doctests
* The project ran over time by 2x, this reflected:
  * My unfamiliarity with the tkinter library and some of its behaviours
  * Inexperience managing data dependencies, which forced some redesigning
* Some attempts at DRY code failed and make the code less flexible
* Widget geometry is quite static and so could cause future problems
* I have not attempted to make it resilient across operating systems 
  * Pathlib would help with management of files
