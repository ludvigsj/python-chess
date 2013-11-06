# -*- coding: utf-8 -*-
import movecheckfuncs
from copy import deepcopy

PAWN=   {"leg": movecheckfuncs.pawnGetLegals, "hasMoved": False, "col": -1, "sym": ("B","b"), "letter": "", "name":"en bonde"}
KNIGHT= {"leg": movecheckfuncs.knightGetLegals, "col": -1, "sym": ("S","s"), "letter": "S", "name":"en springer"}
BISHOP= {"leg": movecheckfuncs.bishopGetLegals, "col": -1, "sym": ("L","l"), "letter": "L", "name":"en løper"}
ROOK=   {"leg": movecheckfuncs.rookGetLegals, "col": -1, "sym": ("T","t"), "letter": "T", "name":"et tårn"}
QUEEN=  {"leg": movecheckfuncs.queenGetLegals, "col": -1, "sym": ("D","d"), "letter": "D", "name":"en dronning"}
KING=   {"leg": movecheckfuncs.kingGetLegals, "col": -1, "sym": ("K","k"), "letter": "K", "name":"en konge"}

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}

WHITE = 1; #TESTUR
BLACK = 0

def main():
    currentColor = WHITE
    board=createBoard(True)
    printHelp()
    printBoard(board)
    while True:
        command = input(("Hvit, " if currentColor == WHITE else "Svart, ") + "skriv inn trekk: ").split("-")
        try:
            startTile = (LETTERS[command[0][0].upper()],int(command[0][1])-1)
            endTile = (LETTERS[command[1][0].upper()],int(command[1][1])-1)
        except:
            print("Ugyldig kommandoformat. Skriv på formen fra-felt + bindestrek + til-felt")
            continue
        results = move(currentColor,startTile,endTile,board)
        if not results == -1:
            board = results
            printBoard(board)
            if isCheckMate(WHITE,board):
                print("Sjakkmatt! Svart spiller vant")
                break
            if isCheckMate(BLACK,board):
                print("Sjakkmatt! Hvit spiller vant")
                break
            currentColor = (currentColor+1)%2
            if isInCheck(currentColor,board):
                print("Din konge står i sjakk")
        
    
def printHelp():
    print("Velkommen til Python-chess! Skriv inn kommandoer på formen [fra-felt]-[til-felt], for eksempel E6-E7")
    
def createBoard(initPieces):
    board=[[None for i in range(8)] for i in range(8)]
    if initPieces:
        for x in range(8):
            board[x][1] = createPiece(PAWN,WHITE)
            board[x][6] = createPiece(PAWN,BLACK)
        for color in range(2):
            board[0][7-7*color] = createPiece(ROOK,color)
            board[1][7-7*color] = createPiece(KNIGHT,color)
            board[2][7-7*color] = createPiece(BISHOP,color)
            board[3][7-7*color] = createPiece(QUEEN,color)
            board[4][7-7*color] = createPiece(KING,color)
            board[5][7-7*color] = createPiece(BISHOP,color)
            board[6][7-7*color] = createPiece(KNIGHT,color)
            board[7][7-7*color] = createPiece(ROOK,color)
    return board

    
def isAttacked(pos,board):
    ownColor = board[pos[0]][pos[1]]["col"]
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece["col"] != ownColor and (pos in piece["leg"](piece,(x,y),board)):
                return True
    return False

def isCheckMate(color,board):
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece["col"] == color:
                for move in piece["leg"](piece,(x,y),board):
                    newBoard = getMoveRes(color,(x,y),move,board)
                    if not isInCheck(color,newBoard):
                        return False
    return True
                

def printBoard(board):
    print("    A    B    C    D    E    F    G    H")
    print(" ┌"+"─"*5*8+"╖")
    for y in range(7,-1,-1):
        padLine = " │"
        line = "%i│"%(y+1)
        for x in range(8):
            padLine += ("     " if (x%2+y%2)%2 else "█████")
            line += ("  " if (x%2+y%2)%2 else "██")
            if board[x][y]:
                line += board[x][y]["sym"][board[x][y]["col"]]
            else:
                line += (" " if (x%2+y%2)%2 else "█")
            line += ("  " if (x%2+y%2)%2 else "██")
        print(padLine+"║")
        print(line+"║%i"%(y+1))
        print(padLine+"║")
    print(" ╘"+"═"*5*8+"╝")
    print("    A    B    C    D    E    F    G    H")
            
def isInCheck(color,board):
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece and piece["letter"] == "K" and piece["col"] == color:
                return isAttacked((x,y),board)

def move(color,startPos,endPos,board):
    newBoard = getMoveRes(color,startPos,endPos,board)
    if newBoard == -1:
        return -1
    if isInCheck(color,newBoard):
        print("Ulovlig trekk: Du kan ikke sette din egen konge i sjakk")
        return -1
    else:
        return newBoard

def getMoveRes(color,startPos,endPos,board):
    newBoard = deepcopy(board)
    piece = newBoard[startPos[0]][startPos[1]]
    if piece and piece["col"] == color:
        if endPos in piece["leg"](piece,startPos,newBoard):
            if newBoard[endPos[0]][endPos[1]]:
                print(("Svart " if color else "Hvit ") + "mistet " + newBoard[endPos[0]][endPos[1]]["name"])
            newBoard[endPos[0]][endPos[1]] = newBoard[startPos[0]][startPos[1]]
            newBoard[endPos[0]][endPos[1]]["hasMoved"] = True
            newBoard[startPos[0]][startPos[1]] = None
        else:
            print("Ulovlig trekk!")
            return -1
    else:
        print("Ingen brikke på det feltet" if not piece else "Du kan ikke flytte på motstanderens brikker")
        return -1
    return newBoard
            

def createPiece(type, color):
    piece = deepcopy(type)
    piece["col"] = color
    return piece

main()
