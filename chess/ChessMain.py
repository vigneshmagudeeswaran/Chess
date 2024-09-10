"""This is our main driver file . It will be responsible for handling user input and displaying the current Game state"""

import pygame as p
from ChessEngine import GameState,Move
# from .ChessGraphics import ChessEngine

p.init()
WIDTH = HEIGHT = 512#400 is another possible choice
DIMENSION = 8 #dimensions of a chess board ar 8*8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # for animations
IMAGES = {}

"""_summary_
This function is responsible for loading all the images that we will need to display our game.
"""
def loadImages():
    pieces=['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for pieces in pieces:
        IMAGES[pieces]=p.transform.scale(p.image.load("chess/images/"+pieces+".png"),(SQ_SIZE,SQ_SIZE))
    # note that we can access an image by saying IMAGES['wp'] or IMAGES['wP']
"""_summary_
The main driver for our cod. This will handle user input and updating the grap

"""

def main():
    p.init()
    screen =p.display.set_mode((WIDTH,HEIGHT))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    
    moveMade = False #flag variables  for when  a move is made
    gs=GameState()
    print(gs.board)
    validMoves = gs.getValidMoves()
    loadImages()#only do this once, before the while loop
    running =True
    sqSelected =() # no square is selected. keep track of the last click of the user(tuple:row, col)
    playerClicks=[]#keep track of player clicks (tow tuples:[(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running=False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()# (x,y) location of the mouse
                col = location[0]//SQ_SIZE # to pick x axis mouse location
                row = location[1]//SQ_SIZE #to pick y axis mouse location
                if sqSelected== (row,col): # the user clicked the same square twice
                    sqSelected =() #deselect
                    playerClicks =[] #clear player clicks
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected) # append for both 1st and 2nd click
                if len(playerClicks)==2: #after 2nd click
                    move = Move(playerClicks[0],playerClicks[1],gs.board)
                    if move in validMoves:
                        print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade =True
                        sqSelected=() #reset user clicks
                        playerClicks=[]
                    else:
                        playerClicks =[sqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:#undo whrn 'z' is pressed
                    gs.undo()
                    moveMade=True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade=False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
        
def drawGameState(screen,gs):
    drawBoard(screen)#draw squares on the board
    #add in pieces highlighting or move suggestion    
    drawPieces(screen,gs.board)#draw pieces on top of the squares

"""
Draw the squares on the board. Top left square is always light
"""
def drawBoard(screen):
    """
    Draws the chess board on the screen.

    :param screen: The surface to draw the board on.
    """
    colors = (p.Color('white'), p.Color('gray'))
    
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            if screen is not None:
                color = colors[(r+c)%2] #alternates between white and gray
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            color=colors[(r+c)%2]
            p.draw.rect(screen,color,p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

            
"""
Draw the pieces on the board using current using the currentState.board
"""  
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range (DIMENSION):
            piece = board[r][c]
            if piece != "--":   #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
    

if __name__ =="__main__":  
    main() 