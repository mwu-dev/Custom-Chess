import pygame
import cfg
import piece
from piece import King, Queen, Bishop, Knight, Rook, Pawn

BLACK = False
WHITE = True

class Board:

    def __init__(self): #setup board and pieces
        self.blackPieces = []
        self.whitePieces = []
        
        self.blackPieces.append(King(4, 0, BLACK))
        self.blackPieces.append(Queen(3, 0, BLACK))
        self.blackPieces.append(Bishop(2, 0, BLACK))
        self.blackPieces.append(Bishop(5, 0, BLACK))
        self.blackPieces.append(Knight(1, 0, BLACK))
        self.blackPieces.append(Knight(6, 0, BLACK))
        self.blackPieces.append(Rook(0, 0, BLACK))
        self.blackPieces.append(Rook(7, 0, BLACK))
        for i in range(0, 8):
            self.blackPieces.append(Pawn(i, 1, BLACK))

        self.whitePieces.append(King(4, 7, WHITE))
        self.whitePieces.append(Queen(3, 7, WHITE))
        self.whitePieces.append(Bishop(2, 7, WHITE))
        self.whitePieces.append(Bishop(5, 7, WHITE))
        self.whitePieces.append(Knight(1, 7, WHITE))
        self.whitePieces.append(Knight(6, 7, WHITE))
        self.whitePieces.append(Rook(0, 7, WHITE))
        self.whitePieces.append(Rook(7, 7, WHITE))
        for i in range(0, 8):
            self.whitePieces.append(Pawn(i, 6, WHITE))

    def getPiece(self, x, y):
        #returns piece currently at position (x,y), None if no piece
        for piece in self.blackPieces:
            if x == piece.x and y == piece.y:
                return piece
        for piece in self.whitePieces:
            if x == piece.x and y == piece.y:
                return piece
        return None

    def removePiece(self, x, y):
        #removes piece currently at position (x,y)
        #returns True if sucessfully removed, False otherwise
        pieceToRemove = self.getPiece(x, y)
        if pieceToRemove is not None:
            if pieceToRemove.isWhite:
                self.whitePieces.remove(pieceToRemove)
            else:
                self.blackPieces.remove(pieceToRemove)
            return True
        return False

    def movePiece(self, x, y, piece, valid = None):
        #move the given piece to (x,y), takes enemy piece if there is one, returns boolean
        #indicating whether the move was successful
        #takes into account collision with any other pieces in the path
        target = (x,y)
        if valid is None:
            valid = piece.allValidMoves(self)
        if target in valid:
            piece.move(x, y, self)
            return True
        return False

    def draw(self, validMoves = None):
        for i in range(0, 8):
            for j in range(0, 8):
                tileRect = (i*100, j*100, 100, 100)
                if (i+j)%2 == 0:
                    pygame.draw.rect(cfg.screen, cfg.whiteTile, tileRect, 0)
                else:
                    pygame.draw.rect(cfg.screen, cfg.blackTile, tileRect, 0)
        #draw possible moves for picked up piece
        if validMoves is not None:
            for moves in validMoves:
                tileRect = (moves[0]*100, moves[1]*100, 100, 100)
                pygame.draw.rect(cfg.screen, cfg.greenTile, tileRect, 10)
        #draw pieces
        for piece in self.blackPieces:
            piece.draw()
        for piece in self.whitePieces:
            piece.draw()
