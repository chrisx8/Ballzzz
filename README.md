# Ballzzz

A CMU 15-112 Term Project.

The entire project is available on [GitHub](https://github.com/chrisx8/Ballzzz/).

## Design Proposal

- [Project Proposal](docs/project_proposal.md) (`docs/project_proposal.md`)
- [Storyboard](docs/storyboard.png) (`docs/scoreboard.png`)

## Run the game

**All files listed in this section are REQUIRED to run the game.**

- Download these files from the root directory
  - `ballzzz.py`
  - `ballzzz_icon.ico`
  - `requirements.txt`
- Download everything in `gameModules/` and everything in `assets/`
- Install `requests` using `pip`:

  ```bash
  pip install -r requirements.txt
  ```

- Run `ballzzz.py`

## Changelog

### Changes since TP2

- Player can draw a pattern on the drawboard, and the game board will be generated based on what the player draws.
- Fixed a bug where player pattern parsing may result in list-out-of-range error.
- Fixed a bug where a SuperBall can clear the entire board due to insufficient type checking.
- Implemented leaderboard, which shows the top ten players.
- Player can save the game and return to the main menu by pressing ESC.
- 
- Some minor UI improvements.
 
### Changes since TP1

- Scores are automatically uploaded to the scoreboard server.
- Start screen and Game Over UI included buttons, and are mouse-navigable.
- Added special targets. When the ball hits a target, player gets an extra ball.
- Fixed a block collision bug. Insufficient collision checking in the `Ball` class was causing every collisions to be detected as top/bottom collision.
- Prevent infinite bouncing from happening.
- Randomize initial position of the ball.
- When player has more than one balls, all balls are released at the same time and collisions are handled independently.
- Implemented SuperBall (twice as big as a regular ball and has an S inside)
- Difficulty changes when score is over 50, and allow user to change in-game by pressing D.
