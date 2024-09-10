"""This class is responsible for storing all the information about the current state of a class game. 
It will als be responsible for determining the valid moves at current state. It will also keep of move log"""


class GameState():
    def __init__(self):
        """
        Initializes a new instance of the GameState class.
        
        This method sets up the initial state of the chess board, 
        including the positions of all pieces.
        
        Parameters:
        None
       
        Returns:
        None 
        """
        # board is an 8x8 2d list, each element of the list has 2 characters
        # the first character represents the color of the piece
        # the second character represents the type of the piece
        # "--" represents an empty space
        self.board=[['bR','bN','bB','bQ','bK','bB','bN','bR'],
                    ['bp','bp','bp','bp','bp','bp','bp','bp'],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ["--","--","--","--","--","--","--","--"],
                    ['wp','wp','wp','wp','wp','wp','wp','wp'],
                    ['wR','wN','wB','wQ','wK','wB','wN','wR']]
        self.moveFunctions={'p':self.getPawnMoves,
                            'R':self.getRookMoves,
                            'N':self.getKnightMoves,
                            'B':self.getBishopMoves,
                            'Q':self.getQueenMoves,
                            'K':self.getKingMoves}
        self.whiteToMove=True
        self.moveLog=[]

            
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)# log the move so we can undo it later
        self.whiteToMove=not self.whiteToMove#swap players
    '''
    Undo the last move made
    ''' 
    def undo(self):
        if len(self.moveLog)!=0:
            #makes sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # toogle back the turn
    ''' All moves considering checks'''
    def getValidMoves(self):
       return self.getAllPossibleMoves() #after now we will not worry about check
    
    '''All moves without considering checks'''
    def getAllPossibleMoves(self):
        moves =[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn=='w' and self.whiteToMove) or (turn=='b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    print(r,c)
                    print(piece)
                    # if piece =='p':
                    #     self.getPawnMoves(r,c,moves)
                    # elif piece =='R':
                    #     self.getRookMoves(r,c,moves)
                    self.moveFunctions[piece](r,c,moves)
        return moves
                        
                        
    'get all pawn moves for the pawn located at row, col and these moves to the list'
    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove: #white pawn moves
            if self.board[r-1][c]=='--':
                moves.append(Move((r,c),(r-1,c),self.board))
                if r==6 and self.board[r-2][c]=="--":
                    moves.append(Move((r,c),(r-2,c),self.board))
            if c-1 >=0:# capture to the left
                if self.board[r-1][c-1][0]=='b':# enemy piece in capture
                    moves.append(Move((r,c),(r-1,c-1),self.board))
            if c+1 <=7:# capture to the right
                if self.board[r-1][c+1][0]=='b':# enemy piece in capture
                    moves.append(Move((r,c),(r-1,c+1),self.board))
        else: #black pawn moves
            if self.board[r+1][c]=='--':
                moves.append(Move((r,c),(r+1,c),self.board))
                if r==1 and self.board[r+2][c]=="--":
                    moves.append(Move((r,c),(r+2,c),self.board))
            if c-1 >=0:# capture to the left
                if self.board[r+1][c-1][0]=='w':# enemy piece in capture
                    moves.append(Move((r,c),(r+1,c-1),self.board))
            if c+1 <=7:# capture to the right
                if self.board[r+1][c+1][0]=='w':# enemy piece in capture
                    moves.append(Move((r,c),(r+1,c+1),self.board))
        
        #add pawn promotions later
        
            
    
    """
    Returns a list of all possible moves for the rook located at row r and column c.
    
    Parameters:
    r (int): The row of the rook.
    c (int): The column of the rook.
    moves (list): The list to store the possible moves.
    
    Returns:
    None
    """
    def getRookMoves(self,r,c,moves):
        directions = ((-1,0),(0,-1),(1,0),(0,1)) #up, left, down, right
        enemyColor= "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<= endCol<8:
                    endPiece= self.board[endRow][endCol]
                    if endPiece =='--': # empty space valid
                        print('endrow',endRow,'endcol',endCol)
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor: # enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: #off board
                    break
                
    
    def getKnightMoves(self,r,c,moves):
        knightMoves = ((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor ='w' if self.whiteToMove else 'b'
        for n in knightMoves:
            endRow=r+n[0]
            endCol=c+n[1]
            if 0<=endRow<8 and 0<= endCol<8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0]!=allyColor:# not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))

    def getBishopMoves(self,r,c,moves):
        directions = ((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor= "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0<=endRow<8 and 0<= endCol<8:
                    endPiece= self.board[endRow][endCol]
                    if endPiece =='--': # empty space valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0]==enemyColor: # enemy piece valid
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else: # friendly piece invalid
                        break
                else: #off board
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

    def getKingMoves(self,r,c,moves):
        kingMoves=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        allyColor ='w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow=r+kingMoves[i][0]
            endCol=c+kingMoves[i][1]
            if 0<=endRow<8 and 0<= endCol<8:
                endPiece= self.board[endRow][endCol]
                if endPiece[0]!=allyColor:# not an ally piece (empty or enemy piece)
                    moves.append(Move((r,c),(endRow,endCol),self.board))
    
        
            
          
class Move():
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7} #a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7
    colsToFiles = {v: k for k, v in filesToCols.items()} #a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7
    
    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow = endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.moveId= self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print(self.moveId)
    '''
    Overiding the equals method
    '''
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveId == other.moveId
        return False
    def getChessNotation(self):
        # you can add to make this like a real chess notation
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]