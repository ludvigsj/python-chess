# -*- coding: utf-8 -*-

from classes import Piece, Board

COMMAND_PROMPT = "%s, skriv inn en kommando: "
PARSE_ERROR = "Du skrev inn en ugyldig kommando. Formatet er A1-E4 osv."
CASTLING_FAILED = "Det trekket er ikke gyldig akkurat nå"
HELP_COMMANDS = ("help", "hjelp", "--help", "?")

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}

COLOR_NAMES = ("Svart", "Hvit")

WHITE = 1
BLACK = 0

SHORT_CASTLING = "0-0"
LONG_CASTLING = "0-0-0"

class CastlingError(Exception):pass;
class IllegalMoveError(Exception):pass;

def start(setUp=True):
    board = Board()
    if setUp: board.startSetup(); playing = WHITE
    while True:
        print(board.getGraphicString())
        commandString = input(COMMAND_PROMPT%(COLOR_NAMES[playing]))
        if commandString.lower() in HELP_COMMANDS:
            printHelp()
            continue
        if commandString == LONG_CASTLING or commandString == SHORT_CASTLING:
            try: castle(commandString, board, playing)
            except CastlingError:
                print(CASTLING_FAILED)
                continue
        try:
            command = parseCommand(commandString)
        except:
            print(PARSE_ERROR)
            continue
        try:
            execCom(command, board)
        except IllegalMoveError:
            print("Ulovlig trekk")
            continue
        
        playing = (playing+1)%2
        
            
def execCom(command, board):
    piece = board.getPiece(command[0][0],command[0][1])
    endPos = (command[1][0],command[1][1])
    if endPos in piece.findLegalFields():
        piece.setPos(endPos[0],endPos[1])
    else:
        raise IllegalMoveError()

def castle(length, board, color):

    y = 7-7*color
    king = board.getPiece(4,y)
    if length == LONG_CASTLING:
        if (board.getPiece(1,y) or board.getPiece(2,y) or board.getPiece(3,y)):
            raise CastlingError("Could not castle")
        rook = board.getPiece(0,y)
        newKingX = king.x - 2
        newRookX = rook.x + 3
    elif length == SHORT_CASTLING:
        if (board.getPiece(5,y) or board.getPiece(6,y)):
            raise CastlingError("Could not castle")
        rook = board.getPiece(7,y)
        newKingX = king.x + 2
        newRookX = rook.x - 2
    else:
        raise ValueError("must be castling-value")
    if rook and not rook.hasMoved and king and not king.hasMoved:
        rook.setPos(newRookX,y)
        king.setPos(newKingX,y)
    else:
        raise CastlingError("Could not castle")

def parseCommand(commandString):
    command = commandString.split("-")
    x1 = LETTERS[command[0][0].upper()]
    y1 = int(command[0][1])-1
    x2 = LETTERS[command[1][0].upper()]
    y2 = int(command[1][1])-1
    return ((x1,y1),(x2,y2))

def printHelp():
    print("""
    Velkommen til PyChess.

    Kommandoer skrives på formen [Fra-felt]-[Til-felt] (For eksempel E2-E4)
    Spesialkommandoer:
     - Kort rokade: 0-0
     - Lang rokade: 0-0-0

    Sjakkbrikkene vises ved første forbokstav i navnet. b = bonde, l = løper osv.
    Små bokstaver er hvite brikker, store bokstaver er svarte
    """)
    input("Trykk enter for å fortsette...")
            
def main():
    start()
    while input("Omkamp? (y/n)").lower == "y":
        start()
        
main()