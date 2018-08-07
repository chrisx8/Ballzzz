# Ballzzz

A CMU 15-112 Term Project.

## Design Proposal

- [Project Proposal](docs/project_proposal.md)
- [Storyboard](docs/storyboard.png)

## Run the game

- Download these files from the root directory
  - `ballzzz.py`
  - `ballzzz_icon.ico`
  - `requirements.txt`
- Download everything in `gameObjects`
- Install `requests` and its dependencies using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

- Run `ballzzz.py`

## Changelog

### Changes since TP1

- Scores are automatically uploaded to the scoreboard server.
- Game Over UI changes to show ranking.
- Added special targets. When the ball hits a target, player gets an extra ball.
- Fixed a block collision bug. Insufficient collision checking in the `Ball` class was causing every collisions to be detected as top/bottom collision.
- Prevent infinite bouncing from happening.
- Randomize initial position of the ball.
- When player has more than one balls, draw all balls and handle their collisions independently.