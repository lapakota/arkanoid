# Arkanoid
Simple implementation of Arkanoid using pygame

# Dependencies
* Python 3.8
* pygame 2.0.1


# Usage

To start the game run

`python main.py`

* **Space**: Restart the game
* **Esc**: Quit
* **A or Arrow_left**: Move paddle left
* **D or Arrow_right**: Move paddle right
* **You can also move the paddle by moving the mouse by holding down the left mouse button**

The game is considered won if there are no blocks left on the field
and lost if the number of lives has become zero

Cheats:
* **Z**: Increases the width of the paddle
* **X**: Reduces the width of the paddle

Block types:

Normal blocks have a random color and are broken from 1 hit of the ball, and solid blocks have a gray color and are broken from three hits