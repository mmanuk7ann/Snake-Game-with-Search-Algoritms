# 🐍 AI Snake Game

This project is an implementation of the classic Snake game, enhanced with AI path-finding algorithms to control the snake's movement intelligently.

---

## 🧠 About the Project

I designed an intelligent agent that plays Snake using two popular path-finding algorithms:

- **Greedy Best-First Search**
- **A\* Search (A-Star)**

These algorithms guide the snake toward the food efficiently while avoiding collisions with walls and itself.

---

## 🚀 Features

- Classic Snake game logic
- AI-controlled gameplay
- Switchable between Greedy and A\* algorithms
- Optional visual path-tracing for debugging and learning
- Adjustable grid size and speed for performance tuning

---

## 🛠️ Technologies Used

- Python 3
- [Pygame](https://www.pygame.org/) – for rendering the game
- Custom implementations of Greedy Best-First Search and A\* Search algorithms

---


## 📚 Path-Finding Overview

- **Greedy Best-First Search** chooses the next move based solely on the estimated distance (heuristic) to the food.
- **A\* Search** combines the actual cost from the start and the estimated cost to the goal, making it more reliable for avoiding traps or dead ends.


