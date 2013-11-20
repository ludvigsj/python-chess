import copy

WHITE = 1; BLACK = 0

PAWN = {"pat": ["P","P1","PA"], "syms": ("\u265F","\u2659"), "attackableBehind": False, "type": "P"}
KING = {"pat": ["K"], "syms": ("\u265A","\u2654"), "attackableBehind": False, "type": "K"}
KNIGHT = {"pat": ["N"], "syms": ("\u265E","\u2658"), "attackableBehind": False, "type": "N"}
QUEEN = {"pat": [[True,True]], "syms": ("\u265B","\u2655"), "attackableBehind": False, "type": "Q"}
BISHOP = {"pat": [[False,True]], "syms": ("\u265D","\u2657"), "attackableBehind": False, "type": "B"}
ROOK = {"pat": [[True,False]], "syms": ("\u265C","\u2656"), "attackableBehind": False, "type": "R"}
ROW = (ROOK,KNIGHT,BISHOP,QUEEN,KING,BISHOP,KNIGHT,ROOK)

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}
COLOR_NAMES = ("Svart", "Hvit")

kingposs=[(4,7),(4,0)]

class IllegalMoveError(Exception):pass;

def main():
    current = WHITE
    board = [[None for i in range(8)] for j in range(8)]
    for color in (0,1):
        for x in range(8):
            board[x][6-5*color] = copy.deepcopy(PAWN);
            board[x][6-5*color]["sym"] = board[x][6-5*color]["syms"][color]
            board[x][6-5*color]["col"] = color
            board[x][7-7*color] = copy.deepcopy(ROW[x])
            board[x][7-7*color]["sym"] = board[x][7-7*color]["syms"][color]
            board[x][7-7*color]["col"] = color
    while not isCheckMate(board, current):
        print(boardString(board))
        command = parseCommand(input("%s, skriv inn kommando"%COLOR_NAMES[current]))
        nextBoard = copy.deepcopy(board)
        try: execCom(command, nextBoard, current)
        except IllegalMoveError:
            print("Ugyldig trekk")
            continue
        if not isInCheck(nextBoard, kingposs[color]): board = nextBoard
        else:
            print("Du kan ikke sette din egen konge i sjakk")
        runPawnConverter(board,current)
        current = (current+1)%2
    print("%s spiller vant"%COLOR_NAMES[(current+1)%2])
        
def isCheckMate(board, color):
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece:
                if piece["col"] == color:
                    legals = []
                    for pattern in piece["pat"]:
                        legals += getLegal(pattern, (x, y), board, color)
                    for legal in legals:
                        potentialBoard = board.copy()
                        print()
                        print(potentialBoard[x][y])
                        potentialBoard[legal[0]][legal[1]] = piece
                        potentialBoard[x][y] = None
                        print(potentialBoard[legal[0]][legal[1]])
                        if not (isInCheck(potentialBoard, (legal[0],legal[1]) if potentialBoard[legal[0]][legal[1]]["type"] == "K" else kingposs[color])):
                            return False
    return True
                    
            

def isInCheck(nextBoard, kingpos):
    for x in range(8):
        for y in range(8):
            piece = nextBoard[x][y]
            legals = []
            if piece:
                for pattern in piece["pat"]:
                    legals += getLegal(pattern, (x, y), nextBoard, piece["col"])
                if kingpos in legals:
                    return True
    return False
        
def runPawnConverter(board,color):
    for x in range(8):
        if board[x][0+7*color]["type"] == "P":
            changeTo = input("Hva vil du forfremme bonden til? (Q/B/N/R): ")
            while True:
                if changeTo == "Q": board[x][0+7*color] = copy.deepcopy(QUEEN)
                elif changeTo == "B": board[x][0+7*color] = copy.deepcopy(BISHOP)
                elif changeTo == "N": board[x][0+7*color] = copy.deepcopy(KNIGHT)
                elif changeTo == "R": board[x][0+7*color] = copy.deepcopy(ROOK)
                else:
                    changeTo = input("Du kan ikke forfremme til %s\nHva vil du forfremme bonden til? (Q/B/N/R): "%changeTo)
                    continue
                board[x][0+7*color]["sym"] = board[x][0+7*color]["syms"][color]
                board[x][0+7*color]["col"] = color
    
        
def parseCommand(commandString):
    command = commandString.split("-")
    x1 = LETTERS[command[0][0].upper()]
    y1 = int(command[0][1])-1
    x2 = LETTERS[command[1][0].upper()]
    y2 = int(command[1][1])-1
    return ((x1,y1),(x2,y2))

def execCom(command, board, color):
    piece = board[command[0][0]][command[0][1]]
    if not piece or piece["col"] !=  color: raise IllegalMoveError()
    endPos = (command[1][0],command[1][1])
    legals = []
    for pattern in piece["pat"]:
        legals += getLegal(pattern, (command[0][0], command[0][1]), board, color)
    if endPos in legals:
        board[command[0][0]][command[0][1]] = None
        board[endPos[0]][endPos[1]] = piece
        if piece["type"] == "K": kingposs[color] = (endPos[0],endPos[1])
        if piece["attackableBehind"]: piece["attackableBehind"] = False
        if "P1" in piece["pat"]:
            piece["pat"].remove("P1")
            piece["attackableBehind"] = True
            
    else:
        raise IllegalMoveError()

def returnContOpen(pat, pos, board, withEnds=False):
    results = []
    ends = []
    def appendContinous(direction):
        for field in [(pos[0]+d*direction[0],pos[1]+d*direction[1]) for d in range(1,8)]:
                try:
                    if board[field[0]][field[1]]:
                        ends.append(field)
                        break
                    else: results.append(field);
                except IndexError: break
    if pat[1]:
        for direction in ((1,1),(1,-1),(-1,1),(-1,-1)): appendContinous(direction)
    if pat[0]:
        for direction in ((1,0),(-1,0),(0,1),(0,-1)): appendContinous(direction)
    if withEnds: return results, ends
    else: return results

def getLegal(pat, pos, board, colr):
    col = 1 if colr == WHITE else -1
    results = []
    if pat == "K":
        for field in [(pos[0]+x,pos[1]+y) for x in (-1,0,1) for y in (-1,0,1)]:
            try:
                if not (board[field[0]][field[1]]) or isAttackable(field,board,col): results.append(field)
            except IndexError: continue
    elif pat == "N":
        for field in [(pos[0]+x,pos[1]+y) for x in (-2,0,2) for y in (-1,0,1)]:
            try:
                if (not board[field[0]][field[1]]) or isAttackable(field,board,col): results.append(field)
                if (not board[field[1]][field[0]]) or isAttackable((field[1],field[0]),board,col): results.append((field[1],field[0]))
            except IndexError: continue
    elif pat == "P":
        try:
            if not board[pos[0]][pos[1]+col]: results.append((pos[0],pos[1]+col))
        except IndexError: pass
    elif pat == "P1":
        try:
            if not board[pos[0]][pos[1]+2*col]: results.append((pos[0],pos[1]+2*col))
        except IndexError: pass
        results+=getLegal("P",pos,board,col)
    elif pat == "PA":
        for dirct in (-1,1):
            try:
                if isAttackable((pos[0]+dirct,pos[1]+col),board,col): results.append((pos[0]+dirct,pos[1]+col))
            except IndexError: continue
    else:
        cont, ends = returnContOpen(pat,pos,board, True)
        return cont + [f for f in ends if isAttackable(f,board,col)]
    return results

def isAttackable(pos,board,color):
    piece = board[pos[0]][pos[1]]
    if piece:
        if piece["col"] != color: return True
    else:
        possiblePawn = board[pos[0]][pos[1]-color]
        if possiblePawn and possiblePawn["attackableBehind"]: return True
    return False
        
def boardString(board):
    string = ("    A     B     C     D     E     F     G     H\n")
    string += (" ┌"+"─"*6*8+"╖\n")
    for y in range(7,-1,-1):
        padLine = " │"
        line = "%i│"%(y+1)
        for x in range(8):
            padLine += ("      " if (x%2+y%2)%2 else "██████")
            line += ("  " if (x%2+y%2)%2 else "██")
            if board[x][y]:
                line += board[x][y]["sym"]
                line += " " 
            else:
                line += ("  " if (x%2+y%2)%2 else "██")
            line += ("  " if (x%2+y%2)%2 else "██")
        string += (padLine+"║\n")
        string += (line+"║%i\n"%(y+1))
        string += (padLine+"║\n")
    string += (" ╘"+"═"*6*8+"╝\n")
    string += ("    A     B     C     D     E     F     G     H")
    return string 

main()