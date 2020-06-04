
import piece
import Game
import GUI
from Game import *
from GUI import *


def minimaxRoot(depth, board,isMaximizing):
    possibleMoves = getChildNode(board)

    bestMove = -9999
    secondBest = -9999
    thirdBest = -9999
    bestMoveFinal = None
    for childNode in possibleMoves:
        print(childNode)
       
        value = max(bestMove, minimax(depth - 1,childNode, not isMaximizing))
        
        if( value > bestMove):
            print("Best score: " ,str(bestMove))
            print("Best move: ",str(bestMoveFinal))
            print("Second best: ", str(secondBest))
            thirdBest = secondBest
            secondBest = bestMove
            bestMove = value
            bestMoveFinal = childNode
    for piece in board:
        if piece not in bestMoveFinal:
            start_pos=piece
    for piece in bestMoveFinal:
        if piece not in board:
            end_pos=piece
    return (start_pos,end_pos)

def minimax(depth, board, is_maximizing):
    if(depth == 0):
        return -evaluation(board)
    possibleMoves = getChildNode(board)
    
    if(is_maximizing):
        bestMove = -9999
        for move  in possibleMoves:
           
            bestMove = max(bestMove,minimax(depth - 1, move, not is_maximizing))
            
        return bestMove
    else:
        bestMove = 9999
        for move  in possibleMoves:
           
            bestMove = min(bestMove, minimax(depth - 1, move, not is_maximizing))
        return bestMove





def evaluation(chessboard):
    value=0
    for piece in chessboard:
        if chessboard[piece].Color==BLACK:
            value-= chessboard[piece].getValue()
        else:
            value+=chessboard[piece].getValue()
    return value



def getChildNode(chessboard):
  
    result=[]
    for piece in chessboard:
        
        start_pos=piece
        for end_pos in chessboard[start_pos].availableMoves(start_pos[0],start_pos[1],chessboard):
            board=chessboard.copy()
            P=board[start_pos]
            board[end_pos]=board[piece]
            board.pop(start_pos)
            result.append(board)
    #print("Total available Move: {}".format(len(result)))
    return result





def main():
    game=Game()
    board=game.getChessBoard()
    print(minimaxRoot(3,board,True))

    


if __name__== "__main__":
    main()




        