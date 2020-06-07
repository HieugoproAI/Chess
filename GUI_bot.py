import cv2
import numpy as np
import tkinter as tk
from piece import *
import time

class GameBoard(tk.Frame):
    def __init__(self, parent, chessboard,rows=8, columns=8, size=128, color1="white", color2="grey"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}
        self.traces={}
        self.chessboard=chessboard
        self.pop=True
        self.turn =BLACK
        self.GameDone=False
        self.message=None


        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        #self.canvas.bind("<Button-1>",self.click_start)
        self.canvas.bind("<Button-1>",self.click)
    
    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(0,0,image=image, tags=(name, "piece"))
        self.placepiece(name, row, column)

    
    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.traces[(row,column)]=name
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size/2)
        y0 = (row * self.size) + int(self.size/2)
        self.canvas.coords(name, x0, y0)

    
    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        for name in self.pieces:
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
    
    def click(self, event):
        if self.GameDone:
            print("Game Done ")
            return -1

        # Figure out which square we've clicked
        # col_size = row_size = event.widget.master.square_size
        # if self.pop = true : pick that piece , else put the piece is picking to that position
        
        if self.pop:
            current_column = int(event.x/115)
            current_row = int(event.y /115)
            self.start_pos=(current_row,current_column)
            if self.start_pos not in self.chessboard:
                print("No piece")
                return 0
            #print("Available Move:")
            #print(self.chessboard[self.start_pos].availableMoves(self.start_pos[0],self.start_pos[1],self.chessboard))
            if self.turn != BLACK:
                print("Not your turn")
                return 0
            #print(self.message)
            self.pop=False
            #print(self.chessboard[self.start_pos].getValue())
        else:
            current_column = int(event.x/115)
            current_row = int(event.y /115)
            self.end_pos=(current_row,current_column)
            piece=self.chessboard[self.start_pos]
            if self.end_pos in piece.availableMoves(self.start_pos[0],self.start_pos[1],self.chessboard):
                self.move(self.start_pos,self.end_pos)
                self.turn=WHITE
                if (isinstance(self.chessboard[self.end_pos],Pawn)):
                    self.chessboard[self.end_pos].Moved()
                
            else:
                print("Cannot move")
                
            
            #self.move((1,2),(5,2))
            #do alpha beta pruning
            if self.turn==WHITE:
                self.start_pos,self.end_pos= minimaxRoot(3,self.chessboard,True)
                self.move(self.start_pos,self.end_pos)
                if (isinstance(self.chessboard[self.end_pos],Pawn)):
                    self.chessboard[self.end_pos].Moved()
                self.turn=BLACK
            self.pop=True
    
    
    
    def move(self,startpos,endpos):
        Image={ "♙":tk.PhotoImage(file="img/whitep.png"), 
                "♖":tk.PhotoImage(file="img/whiter.png"), 
                "♘":tk.PhotoImage(file="img/whiten.png"), 
                "♗":tk.PhotoImage(file="img/whiteb.png") , 
                "♔":tk.PhotoImage(file="img/whitek.png"), 
                "♕":tk.PhotoImage(file="img/whiteq.png") , 
                "♟":tk.PhotoImage(file="img/blackp.png"), 
                "♜":tk.PhotoImage(file="img/blackr.png"),
                "♞":tk.PhotoImage(file="img/blackn.png"), 
                "♝":tk.PhotoImage(file="img/blackb.png") , 
                "♚":tk.PhotoImage(file="img/blackk.png"), 
                "♛":tk.PhotoImage(file="img/blackq.png")}
        
        #Pawn_test=Pawn(name="kt",color=None, direction=-1)
        if endpos not in self.traces:
            # no piece in endpos
            name=self.traces[startpos]
            piece=self.chessboard[startpos]
            self.addpiece(name=self.traces[startpos], image=Image[self.traces[startpos][0]],row=endpos[0],column=endpos[1])
            self.traces[endpos]=name
            self.traces.pop(startpos)
            self.chessboard[endpos]=piece
            self.chessboard.pop(startpos)
            
        else: 
            #remove the endpos, take the piece from startpos to the endpos
            endpos_name=self.traces[endpos]
            self.addpiece(name=endpos_name,image=None,row=999,column=999)
            startpos_name=self.traces[startpos]
            self.addpiece(name=startpos_name,image=Image[self.traces[startpos][0]],row=endpos[0],column=endpos[1])
            self.traces[endpos]=startpos_name
            self.traces.pop(startpos)
            self.chessboard[self.end_pos]=self.chessboard[self.start_pos]
            self.chessboard.pop(startpos)
            if endpos_name[0]== "♔":
                self.GameDone=True
                print("Black Win")
                return 0
            elif endpos_name[0]== "♚":
                self.GameDone=True
                print("White win")
                return 0
        if self.chessboard[self.end_pos].Color==BLACK:
            self.turn =WHITE
        else : self.turn=BLACK
        if self.isCheck():
            print(self.message)

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
           
        
        
# Minimax , alpha beta pruning
def minimaxRoot(depth, board,isMaximizing):
    start=time.time()
    possibleMoves = getChildNode(board,depth)

    bestMove = -9999
    secondBest = -9999
    thirdBest = -9999
    bestMoveFinal = None
    for childNode in possibleMoves:
        value = max(bestMove, minimax(depth - 1,childNode, not isMaximizing,-9999,9999))
        
        if( value > bestMove):
            #print("Best score: " ,str(bestMove))
            #print("Best move: ",str(bestMoveFinal))
            #print("Second best: ", str(secondBest))
            thirdBest = secondBest
            secondBest = bestMove
            bestMove = value
            bestMoveFinal = childNode
        start_pos=None
        end_pos=None
    for piece in board:
        if piece not in bestMoveFinal:
            start_pos=piece
            break
    for piece in bestMoveFinal:
        if piece not in board:
            end_pos=piece
            break
        if board[piece]!= bestMoveFinal[piece]:
            end_pos=piece
            break
    print("best move : From {} to {}".format(start_pos,end_pos))
    print("inference time: {} second".format(time.time() -start))
    return (start_pos,end_pos)

def minimax(depth, board, ismaximizing,alpha,beta):
    if(depth == 0):
        return evaluation(board)
    possibleMoves = getChildNode(board,depth)
    
    if(ismaximizing):
        bestMove = -9999
        for move  in possibleMoves:
            bestMove = max(bestMove,minimax(depth - 1, move, not ismaximizing,alpha,beta))
            alpha=max(bestMove,alpha)
            if alpha>=beta:
                break
        return bestMove
    else:
        bestMove = 9999
        for move  in possibleMoves:
           
            bestMove = min(bestMove, minimax(depth - 1, move, not ismaximizing,alpha,beta))
            beta=min(bestMove,beta)
            if beta <= alpha:
                break
        return bestMove





def evaluation(chessboard):
    value=0
    for piece in chessboard:
        if chessboard[piece].Color==BLACK:
            value-= chessboard[piece].getValue()
        else:
            value+=chessboard[piece].getValue()
    return value



def getChildNode(chessboard,turn):
  
    result=[]
    if (turn%2 ==1):#White Node

        for piece in chessboard:
            if chessboard[piece].Color== BLACK:
                continue    
            start_pos=piece
            for end_pos in chessboard[start_pos].availableMoves(start_pos[0],start_pos[1],chessboard):
                board=chessboard.copy()
                P=board[start_pos]
                board[end_pos]=board[piece]
                board.pop(start_pos)
                result.append(board)
        #print("Total available Move: {}".format(len(result)))
        return result
    else:
        for piece in chessboard:
            if chessboard[piece].Color== BLACK:
                continue    
            start_pos=piece
            for end_pos in chessboard[start_pos].availableMoves(start_pos[0],start_pos[1],chessboard):
                board=chessboard.copy()
                P=board[start_pos]
                board[end_pos]=board[piece]
                board.pop(start_pos)
                result.append(board)
        #print("Total available Move: {}".format(len(result)))
        return result




'''
#test the tkinter library

imagedata="/home/hieunk/NhapMonAI/img/blackb.png"
root = tk.Tk()
board = GameBoard(root)
board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
player1 = tk.PhotoImage(file=imagedata)
board.addpiece("player1", player1, 0,0)


root.mainloop()
''' 