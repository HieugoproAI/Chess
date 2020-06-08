from piece import *
import itertools
import GUI_bot
from GUI_bot  import *
import tkinter as tk 
#from ChessGame import *


WHITE = "white"
BLACK = "black"

uniDict = {WHITE : {Pawn : "♙", Rook : "♖", Knight : "♘", Bishop : "♗", King : "♔", Queen : "♕" }, 
            BLACK : {Pawn : "♟", Rook : "♜", Knight : "♞", Bishop : "♝", King : "♚", Queen : "♛" }}


class Game:
    def __init__(self):
        self.chessboard={}
        self.initPiece()
        
    def initPiece(self):
        placers=[Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
        for i in range(8):
            self.chessboard[(1,i)] = Pawn(WHITE,uniDict[WHITE][Pawn] ,1)
            
            self.chessboard[(6,i)] = Pawn(BLACK,uniDict[BLACK][Pawn],-1)
            
        placers = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
        
        for i in range(0,8):
            self.chessboard[(0,i)] = placers[i](WHITE,uniDict[WHITE][placers[i]])
            
        #placers.reverse()

        for i in range(8):
            self.chessboard[(7,i)]=placers[i](BLACK,uniDict[BLACK][placers[i]])
    
    def isCheck(self):
        #find the Kings
        king = King
        kingDict = {}
        pieceDict = {BLACK : [], WHITE : []}
        for position,piece in self.chessboard.items():
            if type(piece) == King:
                kingDict[piece.Color] = position
            
            pieceDict[piece.Color].append((piece,position))
        #white
        if self.canSeeKing(kingDict[WHITE],pieceDict[BLACK]):
            self.message = "White player is in check"
            return True
        if self.canSeeKing(kingDict[BLACK],pieceDict[WHITE]):
            self.message = "Black player is in check"
            return True
        return False
        
    def canSeeKing(self,kingpos,piecelist):
        for piece,position in piecelist:
            if piece.isValid(position,kingpos,piece.Color,self.chessboard):
                return True
    

  
game=Game()
root = tk.Tk()
root.title("Chess")
Image={ "♙":tk.PhotoImage(file="img/blackp.png"), 
                "♖":tk.PhotoImage(file="img/blackr.png"), 
                "♘":tk.PhotoImage(file="img/blackn.png"), 
                "♗":tk.PhotoImage(file="img/blackb.png") , 
                "♔":tk.PhotoImage(file="img/blackk.png"), 
                "♕":tk.PhotoImage(file="img/blackq.png") , 
                "♟":tk.PhotoImage(file="img/whitep.png"), 
                "♜":tk.PhotoImage(file="img/whiter.png"),
                "♞":tk.PhotoImage(file="img/whiten.png"), 
                "♝":tk.PhotoImage(file="img/whiteb.png") , 
                "♚":tk.PhotoImage(file="img/whitek.png"), 
                "♛":tk.PhotoImage(file="img/whiteq.png")}
game=Game()
board = GameBoard(root,chessboard=game.chessboard)
board.pack(side="bottom", fill="both", expand="true", padx=4, pady=4)
count=0


for piece in game.chessboard:
    Name=str(game.chessboard[piece])+str(count)
    board.addpiece(name=Name,image=Image[str(game.chessboard[piece])],row=piece[0],column=piece[1])
    count+=1

root.mainloop()






