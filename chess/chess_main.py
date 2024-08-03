#這個是主程式，用來儲存玩家的輸入動作（例如決定動哪一步）以及表現現在遊戲的素材如何呈現（就是動到哪邊）。
import pygame as p
import ChessEngine #原本是要寫成 from chess import chessEngine,那個chess是資料夾的名字，但因為我把main&engine放在一起，所以可以直接import。

width = height = 512  
dimension = 8  #棋盤是8*8
sq_size = height // dimension #square size  = 每一個方塊是64*64
max_fps = 15 #later on use on animation.
images = {} # 放棋子的圖片

#Initialized a global dictionary of images. This will called once in the main .
#載入圖片的方法只做一次。

def loadImages():
    #images["wp"] = p.image.load("images/wp.png")
   
    pieces = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
         #we can load images by saying like : images["wp"] 
        images[piece] = p.transform.scale(p.image.load("images/"+ piece + ".png"),(sq_size,sq_size))

    

        #簡單來說，就是創建了一個名為piece的list，用for迴圈將每一張圖片的名字都讀取出來，並且做：
        # 1. 根據image模組的load方法載入圖片
        # 2. 根據transform模組的scale方法調整圖片的大小。
        # 3.透過images[piece]在dict裡面建立以piece為名字的key，並且值是1. 2. 轉換好的圖片內容。 
        

#the  main driver of code. this handle user input & updating the graphics.
#主要的方法，管理使用者的輸入以及更新圖片（例如讓圖片符合棋盤數據的情況）
def main():
    p.init()
    screen = p.display.set_mode((width,height))  #初始化顯示的視窗。
    clock = p.time.Clock() #追蹤時間的物件。
    screen.fill(p.Color("white")) 
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  #flag變數，當棋子移動時會使用。
    loadImages() #這只做一次，所以要寫在迴圈之外。
    running = True
    sqSelected = () #目前沒有任何方塊被選取。用來追蹤目前玩家選取的方塊是哪一個。（tuple:(6, 4)）
    playerClicks = []#追蹤玩家的方塊點擊。（2個tuple :[(6, 4),(3, 4)]）

    while running :
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #以下是滑鼠的操控指令們 
            elif e.type == p.MOUSEBUTTONDOWN: #如果event狀態是按下老鼠的話
                location = p.mouse.get_pos()  #創建一個location函數，追蹤老鼠的位置position (x,y)
                col = location[0] // sq_size #要知道滑鼠現在在哪一排，就用location的位置整除以格子大小
                row = location[1] // sq_size #注意(x, y)對應(location[0], location[1])，同除以64之後對應x的位置（col)與y的位置（row)。

                if sqSelected == (row, col):#如果玩家點選同一個方塊
                   sqSelected = () #清空玩家目前選取並記錄的位置
                   playerClicks = [] #清空玩家的點擊，因為重複了。如[(6, 6),(6, 6)]。
                else:
                    sqSelected = (row,col) #記錄現在的點擊的位置
                    playerClicks.append(sqSelected) #把選取的方塊位置加入玩家的點擊紀錄。兩次點擊都是。

                if len (playerClicks) == 2 : #如果點擊紀錄等於兩次（用資料長度計算），就移動。
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1], gs.board) #move = Move方法
                    print(move.getChessNotaiton())
                    if move in validMoves : # 如果move在validMove列表裡 ＝ 是合法棋步的話
                        gs.makeMove(move)  # 把點選的內容輸入進makeMove()，讓他移動。 
                        moveMade == True  

                    sqSelected = () #移動結束把點擊紀錄清空
                    playerClicks = [] #同上
            #悔棋
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  
                    gs.undoMove()
                    moveMade == True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade == False 

        drawGameState(screen,gs) #根據現在的棋盤進度畫出棋盤。
        clock.tick(max_fps) #控制每一幀更新的速度（也就是遊戲中更新循環的速度），避免不同電腦性能不同造成遊戲速度不同。
        p.display.flip() #update the content of entire display. 


# Down in responsible for all graphics within current game state.
#以下的程式碼負責產生所有當前遊戲狀態的圖片
            
def drawGameState(screen, gs):
    drawBoard(screen) #畫出棋盤大小(512x512)
    drawPiecies(screen, gs.board) # draw pieces on top of these squares.

#Down are draw the squares on the board . 
#畫出棋盤（512*512，包括灰白格子）
def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension): #row
        for c in range(dimension): #column
            color = colors[((r+c) % 2)] 
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size)) 
#依照數學的角度來看，灰色格子在對應的r,c相加再除2的餘數之下都會是奇數性質，因此我們知道當數字輪到奇數的時候就是灰色格子。
#因此在colors白色是index的0，灰色是index的1，因此算到colors [0]  = 白色；等於1就是創造灰色格子。
# draw模組裡面的rect方法，color就是依照列表裡面的索引來選擇要使用什麼樣的顏色。
#螢幕，要用灰色白色，依照rect模組內存的座標大小開始創造格子。

                        
#draw pieces on board using the current GameState. board .
# 根據現在的棋盤數據內容，將棋子圖片畫上去。
def drawPiecies(screen, board): 
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c] #指定board list裡面的特定格子，（0, 0)就是指第一格。
            if piece != "--" :# 如果格子不是空的("--")
                screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
# blit(source, dest, area=None, special_flags=0) -> source是指要畫上去的圖片來源，dest是指畫上去的座標
# 把格子畫上去。



   
if __name__ == "__main__": #if module isn't running directly , it won't runing main()
    main()




 

