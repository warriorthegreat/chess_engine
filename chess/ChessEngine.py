#這用來儲存現在資訊的狀態，特別是一些關於違法棋步。

class GameState():
    def __init__(self) :
        #西洋棋盤的規格，是一個8x8的2d list，每一個元素在列表裡面都有兩個character
        #第一個字元代表黑或白（b,w），第二字元代表角色（如城堡為rook,代號R），bp wp 則是代表士兵。
        # "--"代表沒有棋子是空格。
        self.board = [ 
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.whiteToMove = True
        self.moveLog = [] #用來記錄目前動到哪邊，同時也保證一些動棋子的權益正常（例如說，一次只能移動一個棋子）

    def makeMove(self, move):           #使棋子圖片移動的方法，裡面的方法透過繼承得到。(不過這個方法不適用於入堡、、士兵升變、吃過路兵的情況。)
        self.board[move.startRow][move.startCol] = "--"  #因為棋子移動了，所以原本的格子變成空格。
        self.board[move.endRow][move.endCol] = move.pieceMoved  #移動到的格子將會變成在piecemoved在棋盤數據上對應的棋子。例如你移動士兵，"wp""寫在對應的row&col上。
        self.moveLog.append(move) #如果要悔棋可以從這邊的紀錄開始，這裡的move是一個物件（包含了棋步進入class Move的各種資訊）
        self.whiteToMove = not self.whiteToMove #swap players
       
#以下的方法是悔棋至上一步。
    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop() #回傳物件值
            print(move)
            self.board[move.startRow][move.startCol] = move.pieceMoved  #把pieceMoved對應的棋子移回start row &col 
            self.board[move.endRow][move.endCol] = move.pieceCaptured #把先前記錄的移回去end.
            self.whiteToMove = not self.whiteToMove #swap players 

class Move():  
    # 讓key 可以對應到value
    #key:value 
    #棋盤的(8,8)代表在二為矩陣裡的(0,0)，因此要做一下轉換，整理對應的數字與英文字母。 
    ranksToRows = {"1": 7,  "2": 6, "3": 5, "4": 4, 
                   "5": 3, "6": 2, "7": 1, "8": 0 }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0,  "b": 1, "c": 2, "d": 3, 
                   "e": 4, "f": 5, "g": 6, "h": 7 }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board) :
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol= endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol] #開始的行列將對應到棋盤的格子aka棋子或者是空格 （例如說一開始選擇(1, 1))
        print(self.startRow,self.startCol)
        self.pieceCaptured = board[self.endRow][self.endCol] #結束的行列將對應到棋盤的格子  aka棋子或者是空格  ((例如說移動到(3, 3))
    
    def getChessNotaiton(self):
        return self.getRankFile(self.startRow , self.startCol) + self.getRankFile(self.endRow , self.endCol)
    #顯示移動，用getRankFile 將數字變成對應棋譜代碼。

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    #把矩陣數字變成棋譜代碼，例如(0,0 )=> (a,8)



        

