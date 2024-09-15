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
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.checkMate=False
        self.staleMate=False
        self.enpassantPossible = () #coordinates for the square where en passant is possible

            
    # def makeMove(self,move):
    #     self.board[move.startRow][move.startCol]="--"
    #     self.board[move.endRow][move.endCol]=move.pieceMoved
    #     self.moveLog.append(move)# log the move so we can undo it later
    #     self.whiteToMove=not self.whiteToMove#swap players
    #     #update the king's location if moved
    #     if move.pieceMoved=='wK':
    #         self.whiteKingLocation=(move.endRow,move.endCol)
    #     elif move.pieceMoved=='bK':
    #         self.blackKingLocation=(move.endRow,move.endCol)
        
    #     #pawn promotion
    #     if move.isPawnPromotion:
    #         self.board[move.endRow][move.endCol]=move.pieceMoved[0] + 'Q'
        
    #     #enpassant move
    #     if move.isEnpassantMove:
    #         self.board[move.endRow][move.endCol] = '--'  # Clear the landing square
    #         # Correct the captured pawn position based on pawn color:
    #         if self.whiteToMove:
    #             self.board[move.endRow + 1][move.endCol] = '--'  # Capturing a black pawn
    #         else:
    #             self.board[move.endRow - 1][move.endCol] = '--'  # Capturing a white pawn

    #     if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2: #a pawn moved 2 squares
    #         self.enpassantPossible=((move.endRow+move.startRow)//2, move.endCol)
    #     else:
    #         self.enpassantPossible=()
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move for undo
        self.whiteToMove = not self.whiteToMove  # swap players
        
        # Update the king's location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # Pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # En passant move
        if move.isEnpassantMove:
            if self.whiteToMove:
                self.board[move.endRow + 1][move.endCol] = '--'  # Captured black pawn
            else:
                self.board[move.endRow - 1][move.endCol] = '--'  # Captured white pawn

        # Update en passant possible square
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # pawn double move
            self.enpassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()        
    
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"  # Clear the start square
        self.board[move.endRow][move.endCol] = move.pieceMoved  # Place the moved piece
        self.moveLog.append(move)  # Log the move
        self.whiteToMove = not self.whiteToMove  # Swap players
        
        # Update the king's position if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # Pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        # Handle en passant
        if move.isEnpassantMove:
            if move.pieceMoved == 'wp':
                self.board[move.endRow + 1][move.endCol] = '--'  # Capturing black pawn
            else:
                self.board[move.endRow - 1][move.endCol] = '--'  # Capturing white pawn
        
        # Update en passant square
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()

    '''
    Undo the last move made
    # ''' 
    # def undo(self):
    #     if len(self.moveLog)!=0:
    #         #makes sure that there is a move to undo
    #         move = self.moveLog.pop()
    #         self.board[move.startRow][move.startCol]=move.pieceMoved
    #         self.board[move.endRow][move.endCol]=move.pieceCaptured
    #         self.whiteToMove = not self.whiteToMove # toogle back the turn
    #         if move.pieceMoved=='wK':
    #             self.whiteKingLocation=(move.startRow,move.startCol)
    #         elif move.pieceMoved=='bK':
    #             self.blackKingLocation=(move.startRow,move.startCol)
            
    #         # undo en passant
    #         if move.isEnpassantMove:
    #             self.board[move.endRow][move.endCol]=='--' # leave a '--' in the end
    #             self.board[move.startRow][move.endCol]=move.pieceCaptured
    #             self.enpassantPossible = (move.endRow,move.endCol)
    #         # undo a 2 square pawn advance
    #         if move.pieceMoved[1]=='p' and abs(move.startRow-move.endRow)==2:
    #             self.enpassantPossible=((move.startRow+move.endRow)//2,move.endCol)
    
    def undo(self):
        if len(self.moveLog) != 0:  # make sure there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # swap back players

            # Update the king's location if moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # Undo en passant move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'  # Clear landing square
                if self.whiteToMove:  # Restore black pawn
                    self.board[move.endRow + 1][move.endCol] = move.pieceCaptured
                else:  # Restore white pawn
                    self.board[move.endRow - 1][move.endCol] = move.pieceCaptured

            # # Restore en passant possibility
            # self.enpassantPossible = move.enpassantPossible            
    
    def undo(self):
        if len(self.moveLog) != 0:  # Ensure there's a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # Swap turns back

            # Update king's position if the king was moved
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # Undo en passant
            if move.isEnpassantMove:
                if move.pieceMoved == 'wp':
                    self.board[move.endRow + 1][move.endCol] = 'bp'  # Restore black pawn
                else:
                    self.board[move.endRow - 1][move.endCol] = 'wp'  # Restore white pawn
                self.board[move.endRow][move.endCol] = '--'  # Clear the landing square
            
            # Restore en passant possibility
            self.enpassantPossible = move.isEnpassantMove

    ''' All moves considering checks'''
    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        #1.) generate all possible moves
        moves=self.getAllPossibleMoves()
        #2.) for each move, make the move
        for i in range(len(moves)-1,-1,-1): #when removing from a list go backwards
            self.makeMove(moves[i])
        #3.) generate all opponent's moves
        #4.) for each of those moves, see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i]) #5.) if they do attack your king, not valid
            self.whiteToMove = not self.whiteToMove
            self.undo()
        if len(moves)==0: # either checkmate or stalemate
            if self.inCheck():
                self.checkMate=True
            else:
                self.staleMate = True
        else:
            self.checkMate =False
            self.staleMate =False
        self.enpassantPossible = tempEnpassantPossible
        return moves
        
        
    '''Determin if the current player is in check'''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0],self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0],self.blackKingLocation[1])
    
    '''Determine if enemy can attack the square r,c'''
    def squareUnderAttack(self,r,c):
        self.whiteToMove= not self.whiteToMove #switch to opponent's turn
        oppMoves=self.getAllPossibleMoves()
        self.whiteToMove= not self.whiteToMove #switch turn back
        for move in oppMoves:
            if move.endRow ==r and move.endCol==c: #square is under attack
                return True
        return False
    
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
    # def getPawnMoves(self,r,c,moves):
    #     if self.whiteToMove: #white pawn moves
    #         if self.board[r-1][c]=='--':
    #             moves.append(Move((r,c),(r-1,c),self.board))
    #             if r==6 and self.board[r-2][c]=="--":
    #                 moves.append(Move((r,c),(r-2,c),self.board))
    #         if c-1 >=0:# capture to the left
    #             if self.board[r-1][c-1][0]=='b':# enemy piece in capture
    #                 moves.append(Move((r,c),(r-1,c-1),self.board))
    #             elif (r-1,c-1) == self.enpassantPossible:
    #                 moves.append(Move((r,c),(r-1,c-1),self.board,enpassantPossible=True))
    #         if c+1 <=7:# capture to the right
    #             if self.board[r-1][c+1][0]=='b':# enemy piece in capture
    #                 moves.append(Move((r,c),(r-1,c+1),self.board))
    #             elif (r-1,c-1) == self.enpassantPossible:
    #                 moves.append(Move((r,c),(r-1,c+1),self.board,enpassantPossible=True))
    #     else: #black pawn moves
    #         if self.board[r+1][c]=='--':
    #             moves.append(Move((r,c),(r+1,c),self.board))
    #             if r==1 and self.board[r+2][c]=="--":
    #                 moves.append(Move((r,c),(r+2,c),self.board))
    #         if c-1 >=0:# capture to the left
    #             if self.board[r+1][c-1][0]=='w':# enemy piece in capture
    #                 moves.append(Move((r,c),(r+1,c-1),self.board))
    #             elif (r+1,c-1) == self.enpassantPossible:
    #                 moves.append(Move((r,c),(r+1,c-1),self.board,enpassantPossible=True))
    #         if c+1 <=7:# capture to the right
    #             if self.board[r+1][c+1][0]=='w':# enemy piece in capture
    #                 moves.append(Move((r,c),(r+1,c+1),self.board))
    #             elif (r+1,c+1) == self.enpassantPossible:
    #                 moves.append(Move((r,c),(r+1,c+1),self.board,enpassantPossible=True))
        
    #     #add pawn promotions later
        
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == '--':
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # capture to the left
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enpassantPossible=True))

            if c + 1 <= 7:  # capture to the right
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enpassantPossible=True))

        else:  # black pawn moves
            if self.board[r + 1][c] == '--':
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # capture to the left
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, enpassantPossible=True))

            if c + 1 <= 7:  # capture to the right
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enpassantPossible=True))

         
    
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
    
    def __init__(self, startSq, endSq, board, enpassantPossible=False, isCastleMove=False):
        self.startRow=startSq[0]
        self.startCol=startSq[1]
        self.endRow = endSq[0]
        self.endCol=endSq[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)
        # self.promotionChoice = 'Q'
        self.isEnpassantMove = enpassantPossible
        if self.isEnpassantMove:
            self.pieceCaptured ='wp' if self.pieceCaptured == 'bp' else 'bp'
        
        
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