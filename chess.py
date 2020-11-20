import sys
import math
import cfg
import pygame
import piece
import board
from board import Board
from pygame.locals import *

gameBoard = Board()
running = True
mousePos = (-1, -1)
# pickedUp = False #if a piece is currently picked up
pieceToMove = None
validMoves = None
whiteTurn = True

def main():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                mousePos = convertMousePos(mousePos)
            elif event.type == pygame.MOUSEBUTTONUP:
                newPos = pygame.mouse.get_pos()
                newPos = convertMousePos(newPos)
                if clickedSameSpot(mousePos, newPos):
                    onClick(newPos[0], newPos[1])
                mousePos = (-1, -1)

        drawAll()
        pygame.display.update()

def drawAll():
    gameBoard.draw(validMoves)

def convertMousePos(pos): #converts pixel position to grid position (1,1)
    return (math.floor(pos[0]//cfg.SIZE), math.floor(pos[1]//cfg.SIZE))

def clickedSameSpot(oldPos, newPos):
    return oldPos == newPos

def onClick(mouseX, mouseY):
    global pieceToMove
    global whiteTurn
    global validMoves
    if pieceToMove is None:
        pieceToMove = gameBoard.getPiece(mouseX, mouseY)
        if pieceToMove is None:
            return
        elif ((pieceToMove.isWhite and not whiteTurn) or (not pieceToMove.isWhite and whiteTurn)):
            pieceToMove = None
            # print('Invalid piece to move')
        else:
            validMoves = pieceToMove.allValidMoves(gameBoard)
            pieceToMove.pickedUp = True
        #show possible moves
    elif pieceToMove is not None:
        moved = gameBoard.movePiece(mouseX, mouseY, pieceToMove, validMoves)
        whiteTurn = (not whiteTurn) if moved else (whiteTurn) #switch turns if piece moved
        pieceToMove.pickedUp = False
        pieceToMove = None
        validMoves = None
    
if __name__ == '__main__':
    main()