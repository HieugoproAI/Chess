WHITE = "white"
BLACK = "black"



class Piece:
    
    def __init__(self,color,name):
        self.name = name
        self.position = None
        self.Color = color
    
    def isValid(self,startpos,endpos,Color,gameboard):
        #check  as can move from startpos to endpos
        if endpos in self.availableMoves(startpos[0],startpos[1],gameboard, Color = Color):
            return True
        return False
    
    def __repr__(self):
        return self.name
    
    def __str__(self):
        return self.name
    
    def availableMoves(self,x,y,gameboard):
        print("ERROR: no movement for base class")
        
    def AdNauseum(self,x,y,gameboard, Color, intervals):
        """repeats the given interval until another piece is run into. 
        if that piece is not of the same color, that square is added and
         then the list is returned"""
        answers = []
        for xint,yint in intervals:
            xtemp,ytemp = x+xint,y+yint
            while self.isInBounds(xtemp,ytemp):
                #print(str((xtemp,ytemp))+"is in bounds")
                
                target = gameboard.get((xtemp,ytemp),None)
                if target is None: answers.append((xtemp,ytemp))
                elif target.Color != Color: 
                    answers.append((xtemp,ytemp))
                    break
                else:
                    break
                
                xtemp,ytemp = xtemp + xint,ytemp + yint
        return answers
                
    def isInBounds(self,x,y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False
    
    def noConflict(self,gameboard,initialColor,x,y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x,y) and (((x,y) not in gameboard) or gameboard[(x,y)].Color != initialColor) : return True
        return False
    def getValue(self):
        if self is King:
            if self.Color==WHITE:
                return 5000
        return ValueDict[type(self)]
        
chessCardinals = [(1,0),(0,1),(-1,0),(0,-1)]
chessDiagonals = [(1,1),(-1,1),(1,-1),(-1,-1)]

def knightList(x,y,int1,int2):
    """sepcifically for the rook, permutes the values needed around a position for noConflict tests"""
    return [(x+int1,y+int2),(x-int1,y+int2),(x+int1,y-int2),(x-int1,y-int2),(x+int2,y+int1),(x-int2,y+int1),(x+int2,y-int1),(x-int2,y-int1)]
def kingList(x,y):
    return [(x+1,y),(x+1,y+1),(x+1,y-1),(x,y+1),(x,y-1),(x-1,y),(x-1,y+1),(x-1,y-1)]
  




class Knight(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers= [(xx,yy) for xx,yy in knightList(x,y,2,1) if self.noConflict(gameboard, Color, xx, yy)]
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers

        
class Rook(Piece):
    def availableMoves(self,x,y,gameboard ,Color = None):
        if Color is None : Color = self.Color
        answers= self.AdNauseum(x, y, gameboard, Color, chessCardinals)
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers

        
class Bishop(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers= self.AdNauseum(x, y, gameboard, Color, chessDiagonals)
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers

        
class Queen(Piece):
    
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers= self.AdNauseum(x, y, gameboard, Color, chessCardinals+chessDiagonals)
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers

        
class King(Piece):
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers= [(xx,yy) for xx,yy in kingList(x,y) if self.noConflict(gameboard, Color, xx, yy)]
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers

        
class Pawn(Piece):
    def __init__(self,color,name,direction):
        self.name = name
        self.Color = color
        self.direction = direction
        self.moved=False

    def Moved(self):
        self.moved=True

    
    
    def availableMoves(self,x,y,gameboard, Color = None):
        if Color is None : Color = self.Color
        answers = []
        if (x+self.direction,y+1) in gameboard and self.noConflict(gameboard, Color, x+self.direction, y+1) : 
            answers.append((x+self.direction,y+1))
        if (x+self.direction,y-1) in gameboard and self.noConflict(gameboard, Color, x+self.direction, y-1) : 
            answers.append((x+self.direction, y-1))
        if (x+self.direction,y) not in gameboard and Color == self.Color : 
            answers.append((x+self.direction,y))
            # the condition after the and is to make sure the non-capturing movement (the only fucking one in the game) is not used in the calculation of checkmate
        if (self.moved==False) and ((x+1*self.direction,y)  not in gameboard) and ((x+2*self.direction,y) not in gameboard):
            answers.append((x+2*self.direction,y)) 
        Answers=[]
        for answer in answers:
            if answer[0]>7 or answer[1]>7 or answer[0]<0 or answer[1]<0:
                continue
            else:
                Answers.append(answer)
        return Answers
ValueDict={Pawn:5, Rook:50,Knight:30,Bishop:30,Queen:90,King:2000}
uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}

