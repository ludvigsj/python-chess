# -*- coding: utf-8 -*-

import movecheckfuncs
from copy import deepcopy

COMMAND_PROMPT = "%s, skriv inn en kommando: "
PARSE_ERROR = "Du skrev inn en ugyldig kommando. Formatet er A1-E4 osv."
HELP_COMMAND = "help"

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}

COLOR_NAMES = ("Svart", "Hvit")

WHITE = 1
BLACK = 0

def getStartSetup(board):
        startStp = [[None for i in range(8)] for j in range(8)]
        tp = Piece.Type
        mainRow = (tp.ROOK, tp.KNIGHT, tp.BISHOP, tp.QUEEN, tp.KING, tp.BISHOP, tp.KNIGHT, tp.ROOK)
        for x in range(len(mainRow)):
            pieceW = Piece(mainRow[x], WHITE)
            pieceW.x = x; pieceW.y = 0; pieceW.board = board
            pawnW = Piece(tp.PAWN, WHITE)
            pawnW.x = x; pawnW.y = 1; pawnW.board = board
            pieceB = Piece(mainRow[x], BLACK)
            pieceB.x = x; pieceB.y = 7; pieceB.board = board
            pawnB = Piece(tp.PAWN, BLACK)
            pawnB.x = x; pawnB.y = 6; pawnB.board = board
            startStp[x][0] = pieceW
            startStp[x][1] = pawnW
            startStp[x][6] = pawnB
            startStp[x][7] = pieceB
        return startStp
            
class Piece():
    class Type:
        PAWN=   {"leg": movecheckfuncs.pawnGetLegals, "sym": ("\u265F","\u2659"), "letter": "", "name":"en bonde"}
        KNIGHT= {"leg": movecheckfuncs.knightGetLegals, "sym": ("\u265E","\u2658"), "letter": "S", "name":"en springer"}
        BISHOP= {"leg": movecheckfuncs.bishopGetLegals, "sym": ("\u265D","\u2657"), "letter": "L", "name":"en løper"}
        ROOK=   {"leg": movecheckfuncs.rookGetLegals, "sym": ("\u265C","\u2656"), "letter": "T", "name":"et tårn"}
        QUEEN=  {"leg": movecheckfuncs.queenGetLegals, "sym": ("\u265B","\u2655"), "letter": "D", "name":"en dronning"}
        KING=   {"leg": movecheckfuncs.kingGetLegals, "sym": ("\u265A","\u2654"), "letter": "K", "name":"en konge"}
        '''PAWN=   {"leg": movecheckfuncs.pawnGetLegals, "sym": ("a","A"), "letter": "", "name":"en bonde"}
        KNIGHT= {"leg": movecheckfuncs.knightGetLegals, "sym": ("s","S"), "letter": "S", "name":"en springer"}
        BISHOP= {"leg": movecheckfuncs.bishopGetLegals, "sym": ("l","L"), "letter": "L", "name":"en løper"}
        ROOK=   {"leg": movecheckfuncs.rookGetLegals, "sym": ("t","T"), "letter": "T", "name":"et tårn"}
        QUEEN=  {"leg": movecheckfuncs.queenGetLegals, "sym": ("d","D"), "letter": "D", "name":"en dronning"}
        KING=   {"leg": movecheckfuncs.kingGetLegals, "sym": ("k","K"), "letter": "K", "name":"en konge"}'''    
        
    def __init__(self, type, color):
        self.color = color
        self.__checkfunc__ = type["leg"]
        self.symbol = type["sym"][color]
        self.letter = type["letter"]
        self.x = None
        self.y = None
        self.name = type["name"]
        self.board = None
        self.hasMoved = False
        
    def setPos(self,x,y):
        self.board.setPiece(self.x,self.y,None)
        self.x = x
        self.y = y
        self.board.setPiece(self.x,self.y,self)
        self.hasMoved = True
                
    def findLegalFields(self):
        return self.__checkfunc__(self, (self.x,self.y), self.board)
    
class Board():
    def __init__(self):
        self.pieces = [[None for i in range(8)] for j in range(8)]
     
    def setPiece(self, x, y, val):
        self.pieces[x][y] = val
     
    def getPiece(self, x, y):
        return self.pieces[x][y]
    
    def addPiece(self, piece, x, y):
        piece.x = x; piece.y = y; piece.board = self
        self.pieces[x][y] = piece
        
    def startSetup(self):
        self.pieces = getStartSetup(self)
        
    def getGraphicString(self):
        string = ("    A     B     C     D     E     F     G     H\n")
        string += (" ┌"+"─"*6*8+"╖\n")
        for y in range(7,-1,-1):
            padLine = " │"
            line = "%i│"%(y+1)
            for x in range(8):
                padLine += ("      " if (x%2+y%2)%2 else "██████")
                line += ("  " if (x%2+y%2)%2 else "██")
                if self.getPiece(x, y):
                    line += self.getPiece(x, y).symbol
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