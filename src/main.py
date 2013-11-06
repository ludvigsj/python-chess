from classes import Piece, Board

COMMAND_PROMPT = "%s, skriv inn en kommando: "
PARSE_ERROR = "Du skrev inn en ugyldig kommando. Formatet er A1-E4 osv."
HELP_COMMANDS = ("help", "hjelp", "--help", "?")

LETTERS={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5, "G":6, "H":7}

COLOR_NAMES = ("Svart", "Hvit")

WHITE = 1
BLACK = 0

SHORT_CASTLING = "0-0"
LONG_CASTLING = "0-0-0"

def start(setUp=True):
    board = Board()
    if setUp: self.board.startSetup(); self.playing = WHITE
    while True:
        print(self.board.getGraphicString())
        commandString = input(COMMAND_PROMPT%(COLOR_NAMES[self.playing]))
        print(HELP_COMMANDS)
        if commandString.lower() in HELP_COMMANDS:
            printHelp()
            continue
        if commandString == LONG_CASTLING or commandString == SHORT_CASTLING:
            tryCastling
        try:
            command = parseCommand(commandString)
        except:
            print(PARSE_ERROR)

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
            
def main():
    start()
    while input("Omkamp? (y/n)").lower == "y":
        start()
        
main()