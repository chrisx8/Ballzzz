# Project Proposal

## Project discription

Ballzzz is an enhanced version of Ballz (a popular game by Ketchapp), with different difficulty levels and 
customization options.

## Competitive Analysis

My project (Ballzzz) is based on Ballz (a popular game by Ketchapp), with most of its features, such as:

- When the game starts, a few blocks will be created at random locations.
- Each block has a number and a color associated with it, and the number represents how many times hits needed to clear 
the ball.
- Players shoot balls towards the blocks. The number associated with the block decreases by 1 on each hit.
- When the number of a block reaches 0, it's removed from the screen.
- The ball reflects on the edges of the board and blocks (if number is greater than 1).
- Players get additional balls by hitting special targets.
- On each shot, all balls are released.
- When a shot is complete, new blocks are randomly generated on the top row.
- When a block reaches the bottom of the screen, the game overs.

Since Ballzzz is simply Ballz on steroids, there are other features that doesn't exist in Ballz:

- Difficulty settings
- A "Super Ball" ([definition](#super-ball)) is awarded when one of these conditions are met:
  - Every 10 shots (only in Easy mode)
  - Average hits per ball ([definition](#average-hits-per-ball)) of a shot is greater than 10
- After the game is over, scores are sent to a server, and rankings are displayed on the game-over screen.
- Players can see the top scores on a webpage hosted on the same server.

### Definitions

#### Super Ball

A special type ball that doesn't bounce on blocks or edges of the screen. It destroys the first block it hits, then 
it's removed from screen.

#### Average hits per ball

The game tracks how many times balls hit the blocks in each shot (`TotalBlockHits`). After each completed shot (when a 
new row is generated), the average hits per ball is calculated.

`Average hits per ball = TotalBlockHits / NumberOfBalls`

## Structural Plan

Major game objects and UI elements are defined as objects. The board itself is stored in `data`, and its helper 
functions are stored in a separate file.

The final project will be organized in this structure:

```
Ballzzz
|── ballzzz_icon.ico                  (Tkinter windows icon)
|── ballzzz.py                        (Animations)
├── docs                              (Documentations)
    └── design_proposal.md            (this document)
    └── storyboard.png                (storyboard)
├── gameObjects
    ├── ball.py                       (Ball and SuperBall objects)
    ├── block.py                      (Block objects)
    ├── board.py                      (Board helper functions)
    └── ui.py                         (UI objects for drawing UI)
```
## Algorithmic Plan

- Ball bouncing will be calculated with reflection. As a ball hits a border or a block, its incoming angle is stored

## Timeline Plan

- TP1: Implement balls, blocks, the board, collision algorithm, and scoring
- TP2: Implement reflection algorithm, SuperBall, and special targets
- TP3: Integrate web service, enhance UI, difficulty settings, customization options
## Version Control Plan

I'm using Git for version coltrolling for the entire project. All project codes and assets will be available on 
[GitHub](https://github.com/chrisx8/Ballzzz/).