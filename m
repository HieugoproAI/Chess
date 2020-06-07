def minimax(depth, board, is_maximizing,alpha,beta):
    if(depth == 0):
        return -evaluation(board)
    possibleMoves = getChildNode(board,depth)
    
    if(is_maximizing):
        bestMove = -9999
        for move  in possibleMoves:
            bestMove = max(bestMove,minimax(depth - 1, move, not is_maximizing,alpha,beta))
            alpha=max(bestMove,alpha)
            if alpha>=beta:
                break
        return bestMove
    else:
        bestMove = 9999
        for move  in possibleMoves:
           
            bestMove = min(bestMove, minimax(depth - 1, move, not is_maximizing,alpha,beta))
            beta=min(bestMove,beta)
            if beta <= alpha:
                break
        return bestMove
