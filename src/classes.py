import movecheckfuncs
from copy import deepcopy

COMMAND_PROMPT = "%s, skriv inn en kommando: "
PARSE_ERROR = "Du skrev inn en ugyldig kommando. Formatet er A1-E4 osv."
HELP_COMMAND = "help"

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}

COLOR_NAMES = ("Svart", "Hvit")

WHITE = 1
BLACK = 0

SHORT_CASTLING = "0-0"
LONG_CASTLING = "0-0-0"

def getStartSetup():
        startStp = [[None for i in range(8)] for j in range(8)]
        tp = Piece.Type
        mainRow = (tp.ROOK, tp.KNIGHT, tp.BISHOP, tp.QUEEN, tp.KING, tp.BISHOP, tp.KNIGHT, tp.ROOK)
        for x in range(len(mainRow)):
            pieceW = Piece(mainRow[x], WHITE)
            pieceW.x = x; pieceW.y = 0
            pawnW = Piece(tp.PAWN, WHITE)
            pawnW.x = x; pawnW.y = 1
            pieceB = Piece(mainRow[x], BLACK)
            pieceB.x = x; pieceB.y = 7
            pawnB = Piece(tp.PAWN, BLACK)
            pawnB.x = x; pawnB.y = 6
            startStp[x][0] = pieceW
            startStp[x][1] = pawnW
            startStp[x][6] = pawnB
            startStp[x][7] = pieceB
        return startStp

def parseCommand(commandString):
    if command == "0-0":
        return 
    command = commandString.split("-")
    x1 = letters[command[0][0].upper()]
    y1 = int(command[0][1])-1
    x2 = letters[command[1][0].upper()]
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

class ChessGame():
    def __init__(self, setUp=True):
        self.board = Board()
        if setUp: self.board.startSetup(); self.playing = WHITE    
    
    def start(self):
        while True:
            print(self.board.getGraphicString())
            commandString = input(COMMAND_PROMPT%(COLOR_NAMES[self.playing]))
            if commandString.lower() == HELP_COMMAND:
                printHelp()
                continue
            if commandString == LONG_CASTLING or commandString == SHORT_CASTLING:
                tryCastling
            try:
                command = parseCommand(commandString)
            except:
                print(PARSE_ERROR)
            
class Piece():
    class Type:
        PAWN=   {"leg": movecheckfuncs.pawnGetLegals, "sym": ("B","b"), "letter": "", "name":"en bonde"}
        KNIGHT= {"leg": movecheckfuncs.knightGetLegals, "sym": ("S","s"), "letter": "S", "name":"en springer"}
        BISHOP= {"leg": movecheckfuncs.bishopGetLegals, "sym": ("L","l"), "letter": "L", "name":"en løper"}
        ROOK=   {"leg": movecheckfuncs.rookGetLegals, "sym": ("T","t"), "letter": "T", "name":"et tårn"}
        QUEEN=  {"leg": movecheckfuncs.queenGetLegals, "sym": ("D","d"), "letter": "D", "name":"en dronning"}
        KING=   {"leg": movecheckfuncs.kingGetLegals, "sym": ("K","k"), "letter": "K", "name":"en konge"}    
        
    def __init__(self, type, color):
        self.color = color
        self.__checkfunc__ = type["leg"]
        self.symbol = type["sym"][color]
        self.letter = type["letter"]
        self.x = None
        self.y = None
        self.name = type["name"]
                
    def findLegalFields(self):
        return __checkfunc__()
    
class Board():
    def __init__(self):
        self.pieces = [[None for i in range(8)] for j in range(8)]
     
    def getPiece(self, x, y):
        return self.pieces[x][y]
    
    def addPiece(self, piece, x, y):
        piece.x = x; piece.y = y
        self.pieces[x][y] = piece
        
    def startSetup(self):
        self.pieces = getStartSetup()
        
    def getGraphicString(self):
        string = ("    A    B    C    D    E    F    G    H\n")
        string += (" ┌"+"─"*5*8+"╖\n")
        for y in range(7,-1,-1):
            padLine = " │"
            line = "%i│"%(y+1)
            for x in range(8):
                padLine += ("     " if (x%2+y%2)%2 else "█████")
                line += ("  " if (x%2+y%2)%2 else "██")
                if self.getPiece(x, y):
                    line += self.getPiece(x, y).symbol
                else:
                    line += (" " if (x%2+y%2)%2 else "█")
                line += ("  " if (x%2+y%2)%2 else "██")
            string += (padLine+"║\n")
            string += (line+"║%i\n"%(y+1))
            string += (padLine+"║\n")
        string += (" ╘"+"═"*5*8+"╝\n")
        string += ("    A    B    C    D    E    F    G    H")
        return string

def main():
    game = ChessGame()
    game.start()
    while input("Omkamp? (y/n)").lower == "y":
        game = ChessGame()
        game.start()
        
main()