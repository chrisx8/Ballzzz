# Project Proposal

## Project description

Ballzzz is an enhanced version of Ballz (a popular game by Ketchapp) with more features.

The game starts with a row of random blocks. In this game, the players shoots the ball(s) to the user-provided direction via mouse clicks. All balls are released when player shoots. The ball(s) refects when blocks or borders are hit. The player is able to get additional balls by hitting special targets. Then game ends when a block reaches the bottom row.

After each completed shot, the board shifts down one row, and new blocks are generated on the top row. Player gets rewarded 1 point each time the board shifts.

When the players reach a score of 50, the game automatically changes into "hard mode". Player also has the option to switch to hard mode at any time.

Optionally, player can create their own board by drawing a pattern, a board is generated based on the pattern. 

When the game ends, scores are automatically sent to a server. Player can see their ranking on the server and a leaderboard, both in-game and on a website.

## Competitive Analysis

**Below is a list of features that will possibly be part of this project. Checked items are implemented. Not all of the more complicated features may be implemented.**

**My project (Ballzzz) is based on Ballz (a popular game by Ketchapp), with most of its features**, such as:

- [x] When the game starts, a few blocks will be created at random locations.
- [x] Each block has a number and a color associated with it, and the number represents how many times hits needed to clear the ball.
- [x] Players shoot balls towards the blocks. The number associated with the block decreases by 1 on each hit.
- [x] When the number of a block reaches 0, it's removed from the screen.
- [x] The ball reflects on the edges of the board and blocks (if number is greater than 1).
- [x] Players get additional balls by hitting special targets.
- [x] On each shot, all balls are released.
- [x] When a shot is complete, new blocks are randomly generated on the top row.
- [x] When a block reaches the bottom of the screen, the game overs.
- [x] Player can pause game.

**Since Ballzzz is simply Ballz on steroids, other more complicated features will (probablyy) be implemented**:

- [x] [EASY] After the game is over, scores are sent to a server, and rankings are displayed on the game-over screen.
- [x] [EASY] Players can see the top scores on a webpage hosted on the same server.
- [x] [EASY] Players can see the top ten scores in the game.
- [x] [EASY] A "Super Ball" ([definition](#super-ball)) is awarded when one of these conditions are met:
  - [x] Every 10 shots (only in Easy mode)
  - [x] Average hits per ball ([definition](#average-hits-per-ball)) of a shot is greater than 10
- [x] [MEDIUM] Generate board based on a shape that the player draws
- [x] [MEDIUM] Store game state
- [x] [MEDIUM] Difficulty selection
- [x] [MEDIUM] Increased difficulty when score is a multiple of 50
- [ ] [HARD] Multiplayer mode. Two players shoot from opposite sides of the board.
- [ ] [HARD] The balls can bounce off of each other
- [ ] [HARD] A "cheat mode" that finds the best way to make the current move.

### Definitions

#### Super Ball

A special type ball that doesn't bounce on blocks or edges of the screen. It destroys the first block it hits, then it's removed from screen.

#### Average hits per ball

The game tracks how many times balls hit the blocks in each shot (`TotalBlockHits`). After each completed shot (when a new row is generated), the average hits per ball is calculated.

`Average hits per ball = TotalBlockHits / NumberOfBalls`

## Structural Plan

Major game objects and UI elements are defined as objects. The board itself is stored in `data`, and its helper functions are stored in a separate file.

The final project will be organized in this structure:

```
Ballzzz
|── ballzzz_icon.ico                  (Tkinter windows icon)
|── ballzzz.py                        (Animations)
├── docs                              (Documentations)
    └── design_proposal.md            (this document)
    └── storyboard.png                (storyboard)
├── gameObjects
    ├── api.py                        (API interaction object)
    ├── ball.py                       (Ball and SuperBall objects)
    ├── block.py                      (Block objects)
    ├── board.py                      (Board helper functions)
    └── ui.py                         (UI objects for drawing UI)
├── scoreboard                        (MVC webapp for scoring)
    ├── api.py                        (Score submission API)
    ├── common.py                     (Shared helpers in the webapp)
    ├── config.example.py             (DB config sample)
    ├── config.py                     (DB config - not commited to git)
    ├── models.py                     (DB objects)
    ├── Procfile                      (Heroku deployment file)
    ├── requirements.txt              (Third-party Python modules and dependencies)
    ├── runtime.txt                   (Heroku Python runtime)
    ├── static                        (Static files)
    │   └── favicon.png
    ├── templates                     (HTML Templates)
    │   ├── base.html
    │   ├── index.html
    │   └── scoreboard.html
    ├── views.py                      (Views for frontend)
    └── wsgi.py                       (Initializes the actual app object)

```

## Algorithmic Plan

### Handling Collisions

- The ball reflects when it hits the edges or a block
- When the user clicks on the screen, the ball's initial angle of movement is calculated.

  ```
  Calculation for the angle:
        distanceToClick / sin(pi/2) = (e.y-ballY) / sin(angle)
  Simplified to:
        angle = math.asin(abs(event.y-ballY) / distanceToClick)
  ```

- The direction of movement is processed as quadrants
- When collision happens, quadrant changes. For example, when a ball moving in an angle of pi/4 (Quadrant 1) hits the right border, it'll continue to move in an angle of 3*pi/4 (Quadrant 2)

### Pathfinding: Dijkstra's algorithm

- Cited from the [Wikipedia page for Dijkstra's algorithm](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- Begins with a "starting node" and an open set of candidate nodes (blocks in my case).
- At each step, the node in the open set with the lowest distance from the start is examined. The node is marked "closed", and all nodes adjacent to it are added to the open set if they have not already been examined.
- This process repeats until a path to the destination has been found. Since the lowest distance nodes are examined first, the first time the destination is found, the path to it will be the shortest path.
- In Ballzzz, the algorithm will be used to find the most optimal shot (largest average hits per ball) by mapping out possibilities of possible bounces and find the most optimal one.

## Timeline Plan

### TP1 (Sunday, 8/5/2018)

Implement most basic features, except for the capability of shooting multiple balls, award targets, and automatically shifting the board.

### TP2 (Tuesday, 8/7/2018)

Implement all basic features, clearer instructions on the UI, and a few slightly more difficult features, such as SuperBall and difficulty changes.

### TP3 - Final Project (Friday, 8/10/2018)

Integrate web service, add sound effects, build a more intuitive UX with mouse-navigable menus and better-looking assets, and add a few more advanced features.

## Version Control Plan

I'm using Git for version coltrolling for the entire project. All project codes and assets will be available on [GitHub](https://github.com/chrisx8/Ballzzz/).
