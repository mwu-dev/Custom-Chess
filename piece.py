import pygame
import cfg
import os

images = []
for i in range(0, 12):
    images.append(pygame.image.load(os.path.join('sprite', 'piece_'+str(i)+'.png')))

class Piece:
    #(x,y) coords not pixel coords, i.e. (1,2) instead of (100,200)
    def __init__(self, x, y, white, img, moved = False, pickedUp = False):
        self.x = x
        self.y = y
        self.isWhite = white
        self.img = pygame.transform.scale(img, (cfg.SIZE, cfg.SIZE))
        self.moved = moved
        self.pickedUp = pickedUp
    
    def draw(self):
        boardPos = (self.x*cfg.SIZE, self.y*cfg.SIZE)
        if self.pickedUp:
            imgScaled = pygame.transform.scale(self.img, (int(cfg.SIZE*1.25), int(cfg.SIZE*1.25)))
            cfg.screen.blit(imgScaled, boardPos)
        else:
            cfg.screen.blit(self.img, boardPos)

    def allValidMoves(self, board):
        return [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
                (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),
                (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),
                (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),
                (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),
                (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),
                (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]

    def removeOutBounds(self, moves):
        valid = moves.copy()
        for move in moves:
            if not (0 <= move[0] <= 7) or not (0 <= move[1] <= 7):
                valid.remove(move)
        return valid

    #defines whether or not there are pieces in the way of movement to target (x,y)
    def pieceInBetween(self, x, y, board):
        if (x-self.x) > 0: x_vector = 1
        elif (x-self.x) < 0: x_vector = -1
        else: x_vector = 0
        if (y-self.y) > 0: y_vector = 1
        elif (y-self.y) < 0: y_vector = -1
        else: y_vector = 0

        targetX = self.x + x_vector
        targetY = self.y + y_vector
        while not(targetX == x and targetY == y):
            if board.getPiece(targetX, targetY) is not None:
                return True
            targetX += x_vector
            targetY += y_vector
        return False

    #moves self to position (x,y) and removes piece at (x,y) if there is one
    def move(self, x, y, board):
        board.removePiece(x, y)
        self.x = x
        self.y = y

class King(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[0]
        else:
            img = images[6]
        super().__init__(x, y, white, img)
    
    def allValidMoves(self, board):
        valid = []
        t1 = (self.x-1, self.y)
        t2 = (self.x-1, self.y-1)
        t3 = (self.x, self.y-1)
        t4 = (self.x+1, self.y-1)
        t5 = (self.x+1, self.y)
        t6 = (self.x+1, self.y+1)
        t7 = (self.x, self.y+1)
        t8 = (self.x-1, self.y+1)
        allTargets = [t1, t2, t3, t4, t5, t6, t7, t8]
        for target in allTargets:
            pieceAtTarget = board.getPiece(target[0], target[1])
            if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                valid.append(target)
        valid = Piece.removeOutBounds(self, valid)
        return valid

class Queen(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[1]
        else:
            img = images[7]
        super().__init__(x, y, white, img)

    def allValidMoves(self, board):
        valid = []
        #horizontal moves
        for i in range(0, 8):
            targetX = i
            targetY = self.y
            if not (targetX == self.x):
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        #vertical moves
        for j in range(0, 8):
            targetX = self.x
            targetY = j
            if not (targetY == self.y):
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        for i in range(0, 8):
            targetX = i
            targetY = self.y - self.x + i
            if not targetX == self.x:
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        for j in range(0, 8):
            targetX = self.x + self.y - j
            targetY = j
            if not targetX == self.x:
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        valid = Piece.removeOutBounds(self, valid)
        return valid

class Bishop(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[2]
        else:
            img = images[8]
        super().__init__(x, y, white, img)
    
    def allValidMoves(self, board):
        valid = []
        for i in range(0, 8):
            targetX = i
            targetY = self.y - self.x + i
            if not targetX == self.x:
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        for j in range(0, 8):
            targetX = self.x + self.y - j
            targetY = j
            if not targetX == self.x:
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        valid = Piece.removeOutBounds(self, valid)
        return valid

class Knight(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[3]
        else:
            img = images[9]
        super().__init__(x, y, white, img)
    
    def allValidMoves(self, board):
        valid = []
        t1 = (self.x-1, self.y-2)
        t2 = (self.x+1, self.y-2)
        t3 = (self.x-2, self.y-1)
        t4 = (self.x+2, self.y-1)
        t5 = (self.x-2, self.y+1)
        t6 = (self.x+2, self.y+1)
        t7 = (self.x-1, self.y+2)
        t8 = (self.x+1, self.y+2)
        allTargets = [t1, t2, t3, t4, t5, t6, t7, t8]
        for target in allTargets:
            pieceAtTarget = board.getPiece(target[0], target[1])
            if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                valid.append(target)
        valid = Piece.removeOutBounds(self, valid)
        return valid

class Rook(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[4]
        else:
            img = images[10]
        super().__init__(x, y, white, img)

    def allValidMoves(self, board):
        valid = []
        #horizontal moves
        for i in range(0, 8):
            targetX = i
            targetY = self.y
            if not (targetX == self.x):
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        #vertical moves
        for j in range(0, 8):
            targetX = self.x
            targetY = j
            if not (targetY == self.y):
                pieceAtTarget = board.getPiece(targetX, targetY)
                if pieceAtTarget is None or not (pieceAtTarget.isWhite == self.isWhite):
                    if not Piece.pieceInBetween(self, targetX, targetY, board):
                        valid.append((targetX, targetY))
        valid = Piece.removeOutBounds(self, valid)
        return valid

class Pawn(Piece):
    def __init__(self, x, y, white):
        if white:
            img = images[5]
        else:
            img = images[11]
        super().__init__(x, y, white, img)

    def allValidMoves(self, board):
        valid = []
        if self.isWhite: #moves up
            if self.y == 6: #move up twice
                target = (self.x, self.y-2)
                if board.getPiece(target[0], target[1]) is None:
                    if not Piece.pieceInBetween(self, target[0], target[1], board):
                        valid.append(target)
            if board.getPiece(self.x, self.y-1) is None: #move up once
                valid.append((self.x, self.y-1))
            pieceToTake = board.getPiece(self.x-1, self.y-1) #take piece diagonal left
            if pieceToTake is not None and not (pieceToTake.isWhite == self.isWhite): 
                valid.append((self.x-1, self.y-1))
            pieceToTake = board.getPiece(self.x+1, self.y-1) #take piece diagonal right
            if pieceToTake is not None and not (pieceToTake.isWhite == self.isWhite):
                valid.append((self.x+1, self.y-1))
        elif not self.isWhite: #moves down
            if self.y == 1:
                target = (self.x, self.y+2)
                if board.getPiece(target[0], target[1]) is None:
                    if not Piece.pieceInBetween(self, target[0], target[1], board):
                        valid.append(target)
            if board.getPiece(self.x, self.y+1) is None:
                valid.append((self.x, self.y+1))
            pieceToTake = board.getPiece(self.x-1, self.y+1) #take piece diagonal left
            if pieceToTake is not None and not (pieceToTake.isWhite == self.isWhite): 
                valid.append((self.x-1, self.y+1))
            pieceToTake = board.getPiece(self.x+1, self.y+1) #take piece diagonal right
            if pieceToTake is not None and not (pieceToTake.isWhite == self.isWhite):
                valid.append((self.x+1, self.y+1))
        valid = Piece.removeOutBounds(self, valid)
        return valid