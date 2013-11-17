WHITE = 1
BLACK = 0
Y = 1
X = 0
bounds = lambda x: x <= 7 and x >= 0

def pawnGetLegals(piece, startPos, board):
        
    Y0 = startPos[Y]
    X0 = startPos[X]
    
    results = []
    
    if piece.color == WHITE:
        incr = 1
    elif piece.color == BLACK:
        incr = -1
    if bounds(Y0+incr) and not board.getPiece(X0, Y0+incr):
        results.append((X0,Y0+incr))
    if not piece.hasMoved and bounds(Y0+2*incr) and not board.getPiece(X0, Y0+2*incr):
        results.append((X0,Y0+2*incr))
    results += [(X0+amt,Y0+incr) for amt in (-1,1) if bounds(Y0+incr) and bounds(X0+amt) and board.getPiece(X0+amt, Y0+incr) and (board.getPiece(X0+amt, Y0+incr).color != piece.color)]
    return results
    
    
def rookGetLegals(piece, startPos, board):
    
    X0 = startPos[X]
    Y0 = startPos[Y]
    
    results = []
    
    def addAllXInRange(rng):
        for x in rng:
            if board.getPiece(x,Y0):
                if board.getPiece(x,Y0).color != piece.color: results.append((x,Y0))
                break
            results.append((x,Y0))
        
    def addAllYInRange(rng):
        for y in rng:
            if board.getPiece(X0,y):
                if board.getPiece(X0,y).color != piece.color: results.append((X0,y))
                break
            results.append((X0,y))
    
    addAllXInRange(range(X0+1,8))
    addAllXInRange(range(X0-1,-1,-1))
    addAllYInRange(range(Y0+1,8))
    addAllYInRange(range(Y0-1,-1,-1))
            
    return results

def bishopGetLegals(piece, startPos, board):
    
    X0 = startPos[X]
    Y0 = startPos[Y]
    
    results = []
    
    def ettEllerAnnet(x,y):
        for dist in range(1,8):
            if bounds(X0+x*dist) and bounds(Y0+y*dist):
                if board.getPiece(X0+x*dist,Y0+y*dist):
                    if board.getPiece(X0+x*dist,Y0+y*dist).color != piece.color: results.append((X0+x*dist,Y0+y*dist))
                    return
                results.append((X0+x*dist,Y0+y*dist))
    
    ettEllerAnnet(1,1)
    ettEllerAnnet(1,-1)
    ettEllerAnnet(-1,1)
    ettEllerAnnet(-1,-1)
     
    return results
            
def queenGetLegals(piece, startPos, board):
    return rookGetLegals(piece, startPos, board) + bishopGetLegals(piece, startPos, board)

def kingGetLegals(piece, startPos, board):
    X0 = startPos[X]
    Y0 = startPos[Y]    
    return [(x,y) for x in range(X0-1,X0+2) for y in range(Y0-1,Y0+2) if bounds(x) and bounds(y) and ((board.getPiece(x,y) and board.getPiece(x,y).color != piece.color) or (not board.getPiece(x,y)))]

def knightGetLegals(piece, startPos, board):
    Y0 = startPos[Y]
    X0 = startPos[X]
    
    results = []
    
    for x in (-1,1):
        for y in (-1,1):
            if bounds(X0+2*x) and bounds(Y0+y):
                if board.getPiece(X0+2*x,Y0+y):
                    if board.getPiece(X0+2*x,Y0+y).color != piece.color:
                        results.append((X0+2*x,Y0+y))
                else:
                    results.append((X0+2*x,Y0+y))
            if bounds(X0+x) and bounds(Y0+2*y):
                if board.getPiece(X0+x,Y0+2*y):
                    if board.getPiece(X0+x,Y0+2*y).color != piece.color:
                        results.append((X0+x,Y0+2*y))
                else:
                    results.append((X0+x,Y0+2*y))
                        
    return results