# -*- coding: utf-8 -*-
import movecheckfuncs
from copy import deepcopy

PAWN=   {"leg": movecheckfuncs.pawnGetLegals, "hasMoved": False, "col": -1, "sym": ("♟","♙"), "letter": ""}
KNIGHT= {"leg": movecheckfuncs.knightGetLegals, "col": -1, "sym": ("♞","♘"), "letter": "S"}
BISHOP= {"leg": movecheckfuncs.bishopGetLegals, "col": -1, "sym": ("♝","♗"), "letter": "L"}
ROOK=   {"leg": movecheckfuncs.rookGetLegals, "col": -1, "sym": ("♜","♖"), "letter": "T"}
QUEEN=  {"leg": movecheckfuncs.queenGetLegals, "col": -1, "sym": ("♛","♕"), "letter": "D"}
KING=   {"leg": movecheckfuncs.kingGetLegals, "col": -1, "sym": ("♚","♔"), "letter": "K"}

WHITE = 1
BLACK = 0

def main():
    board=[[None for i in range(8)] for i in range(8)]
    
def checkForCheck(pos,board):
    ownColor = board[pos[0]][pos[1]]["col"]
    for x in board:
        for y in x:
            piece = board[x][y]
            if piece and piece["col"] != ownColor and (pos in piece["leg"](piece,(x,y),board)):
                return True
    return False

def checkForKingInCheck(color,board):
    for x in board:
        for y in x:
            piece = board[x][y]
            if piece["letter"] == "K" and piece["col"] == color:
                checkForCheck((x,y),board)

def Move(color,startPos,endPos,board):
    newBoard = getMoveRes(color,startPos,endPos,board)
    if newBoard != board:
        if checkForKingInCheck(color,board):
            print("Ulovlig trekk: Du kan ikke sette din egen konge i sjakk")
        else:
            board = newBoard
    else: print("Ulovlig trekk")

def getMoveRes(color,startPos,endPos,board):
    newBoard = board.copy()
    piece = newBoard[startPos[0]][startPos[1]]
    if piece and piece["col"] == color:
        if endPos in piece["leg"](piece,startPos,newBoard):
            newBoard[endPos[0]][endPos[1]] = newBoard[startPos[0]][startPos[1]]
            newBoard[startPos[0]][startPos[1]] = None
        else:
            return board
    return newBoard
            

def createPiece(type, color):
    piece = deepcopy(type)
    piece["col"] = color
    return piece

main()
