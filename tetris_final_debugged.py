from time import sleep 
from random import randint
# from os import system


import msvcrt
from sys import exit
import pygame

class Tetris:
    def __init__(self):
        self.board = [["." for _ in range(10)] for _ in range(24)] # generate 20 x 10 board with 4 x 10 extra for spawning the tetromino
        self.tetrominoDict = {
            1: {(1,3),(2,3),(1,2),(2,2)}, # O
            2: {(1,0),(1,1),(1,2),(1,3)}, # I
            3: {(0,2),(1,2),(1,3),(2,2)}, # T
            4: {(0,3),(1,3),(1,2),(2,2)}, # S
            5: {(0,2),(1,2),(1,3),(2,3)}, # Z
            6: {(0,3),(1,1),(1,2),(1,3)}, # J
            7: {(1,1),(1,2),(1,3),(2,3)} # L 
        }
        self.dropTime = 0.15


    def resetBoard(self):
        self.board = [["." for _ in range(10)] for _ in range(24)] 

    def printBoard(self): # print self.board
        for y in range(len(self.board)):
            temp = ""
            for x in self.board[y]:
                temp += x * 3
            
            if y == 10:
                print(" " * 10 + temp + "      SCORE")
                print(" " * 10 + temp + f"         {self.score}")
            elif y == 15:
                print(" " * 10 + temp + "      LEVEL")
                print(" " * 10 + temp + f"         {self.level}")
            else: 
                print(" " * 10 + temp)
                print(" " * 10 + temp)
        #print(self.offsetX, self.offsetY)
        # if self.x == 1: exit()
        # if self.stop: self.x = 1
        

    # def generateTet(self,type=1):  # testng purposes
    #     replacePixels = self.tetrominoDict[type]
    #     board = [["." for _ in range(4)] for _ in range(4)] # 4x4 space for the tetromino
    #     for tuple in replacePixels:
    #         board[tuple[1]][tuple[0]] = "0"
    #     return board

    # def displayTet(self, board): # testng purposes
    #     longtemp = ''''''
    #     for y in board:
    #         temp = ""
    #         for x in y:
    #             temp += x
    #         longtemp+=temp
    #     print(longtemp)

    def insert(self):#),type=1,rotation=1):
        self.offsetX = 0
        self.offsetY = 0
        coords = list(self.tetrominoDict[self.curTetType])
        #print(coords) 
        coords = self.rotate(coords,"cw",True)
        #print(coords)
        ##board = [["." for _ in range(4)] for _ in range(4)] 
        for tuple in coords:
            self.board[tuple[1]][tuple[0]+3] = "O"
        
        newCoords = []
        for coord in coords:
            newCoords.append((coord[0]+3,coord[1]))

        self.offsetX = 3
        return newCoords

    def fall(self, coords):#, curTetType, curTetRot,curTetY, tempHeight):
        # coords = []
        # for y in range(curTetY, curTetY+4-tempHeight): this was O(nm), we changed it to O(1) :)
        #     for x in range(len(self.board[y])):
        #         if self.board[y][x] == "O":
        #             coords.append((x,y))
        #             self.board[y][x] = "."
        
            
        newCoords = []
        hasLanded = False

        #this code looks so ugly
        for coord in coords: 
            if coord[1]+1 == len(self.board) or self.board[coord[1]+1][coord[0]] == "0": # if reached the bottom or if the character under is 0
                hasLanded = True
            if hasLanded and self.offsetY == 0:
                self.end()
                

        for coord in coords:
            self.board[coord[1]][coord[0]] = "."

        for coord in coords: 
            if hasLanded:
                self.board[coord[1]][coord[0]] = "0"
                newCoords.append(coord)
            else:
                self.board[coord[1]+1][coord[0]] = "O"
                newCoords.append((coord[0],coord[1]+1))
        
        self.coords = newCoords
        self.offsetY += 1

        return not hasLanded 

    def shift(self,move,coords):
        # coords = []
        # for y in range(len(self.board)):
        #     for x in range(len(self.board[y])):
        #         if self.board[y][x] == "O":
        #             coords.append((x,y))
        #             self.board[y][x] = "."
        for coord in coords:
            self.board[coord[1]][coord[0]] = "." # also causes blinking effect when trying to move out of bounds..
            # FEATURE NOT A BUG

        newCoords = []

        for coord in coords: # first, verify
            if (move == "left" and (coord[0]-1 == -1 or self.board[coord[1]][coord[0]-1] == "0") ): return
            # checks left boundaries, if at the corner or if there is a piece there. same for below
            elif (move == "right" and (coord[0]+1 == len(self.board[0]) or self.board[coord[1]][coord[0]+1] == "0")) : return
           
        for coord in coords: 
            if move == "left":
                #if coord[0]-1 == -1: break

                self.board[coord[1]][coord[0]-1] = "O"
                newCoords.append((coord[0]-1,coord[1]))
                # print(self.offsetX)
                
                # print(self.offsetX)
            else:#if move == "right":
                #if coord[0]+1 == len(self.board[0]): break

                self.board[coord[1]][coord[0]+1] = "O"
                newCoords.append((coord[0]+1,coord[1]))
                

        if move == "left" : self.offsetX -= 1
        else: self.offsetX += 1

        # if len(newCoords) == 4:
        self.coords = newCoords

        

    # def _insert(self,x,y): # testng purposes
    #     self.board[y][x] = "O"
    def rotate(self, coords, direction="cw", isFirst = False):
        for coord in coords:
            self.board[coord[1]][coord[0]] = "." # also causes blinking effect when trying to move out of bounds..
            # FEATURE NOT A BUG

        def applyRotation(rotCoords, direction="cw"):
            #rotMatrVal = 1 if direction == "cw" else -1

            if self.curTetType == 1: return rotCoords
            elif self.curTetType == 2:
                if direction == "cw": 
                    matrixMult = [[0,-1,self.offsetX+self.offsetY+3],[1,0,-self.offsetX+self.offsetY],[0,0,1]] 
                else:
                    matrixMult = [[0,1,self.offsetX-self.offsetY],[-1,0,self.offsetX+self.offsetY+3],[0,0,1]] 
            else:
                if direction == "cw":
                    matrixMult = [[0,-1,self.offsetX+self.offsetY+3],[1,0,-self.offsetX+self.offsetY+1],[0,0,1]]
                else:
                    matrixMult = [[0,1,self.offsetX-self.offsetY-1],[-1,0,self.offsetX+self.offsetY+3],[0,0,1]]


            newCoords = []
            for coord in rotCoords: 
                coord = list(coord)
                coord.append(1) # this is so that the matrix multiplication can work, to multiply a 3x3 to a 3x1 instead of a 2x1.
                curTuple = []
                for row in matrixMult:
                    answer = 0
                    for item in range(len(row)):
                        answer += row[item] * coord[item]
                    curTuple.append(answer)
                newCoords.append(tuple(curTuple[:-1])) #return the new coordinates after appending the tuple but remove the trailing 1
            
            for coord in newCoords:
                if self.board[coord[1]][coord[0]] == "0":
                    return rotCoords
                for num in coord:
                    if num < 0:
                        return rotCoords
            return newCoords
                
                


        if isFirst:
            #print(coords ,self.curTetRot, "into", self.offsetX, self.offsetY)
            for i in range(self.curTetRot-1):
                coords = applyRotation(coords,direction)
                #print(coords ,self.curTetRot)
        else:
            #print(coords, self.offsetX, self.offsetY)
            coords = applyRotation(coords,direction)
            #print(coords, self.offsetX, self.offsetY)
            self.stop = True

        return coords
    def lineCheck(self):
        clearRows = []
        for row in range(len(self.board)):
            skipLine = False
            for char in self.board[row]:
                if char != "0":
                    skipLine = True
                    break
            if skipLine: continue
            else:
                clearRows.append(row)

        for row in clearRows:
            self.board[row] = ["." for _ in range(10)]
            self.printBoard()
            sleep(0.02)
            del self.board[row]
            self.board.insert(0, ["." for _ in range(10)])
            self.printBoard()


        return len(clearRows)
                

    def pollKey(self):
        '''
            Returns value given keypress:

            no keypress = 0
            esc = 27
            m = 109
            up = 72
            down = 80
            left = 75
            right = 77
            space = 32
            enter = 13
        '''       
        
        x = msvcrt.kbhit()

        key = ord(msvcrt.getch()) if x else 0


        if key == 75:
            self.shift("left", self.coords)
        elif key == 77:
            self.shift("right", self.coords)
        elif key == 72:
            self.coords = self.rotate(self.coords,"cw") # up is rotate cw
        elif key == 80:
            self.coords = self.rotate(self.coords,"ccw") # down is rotatce ccw
        elif key == 109:
            if self.isPaused: pygame.mixer.music.unpause()
            else: pygame.mixer.music.pause()
            self.isPaused = not self.isPaused
        elif key == 32: # spacebar is hard drop
            self.dropTime = 0.001
        elif key == 27: # esc stops the game
            return "exit"
        return "continue"
            
    def start(self):

        print("\n\n     Welcome to TETRIS in Python!\n")
        print("         Press enter to start.")
        print("         Press esc to stop playing.")
        print("         Press m to mute/unmute the music.\n")
        print("         Levels advance after every 3000 points. Level 21 is virtually impossible.")
        input()

        pygame.init()
        pygame.mixer.music.load('Tetris_Music.mp3')
        pygame.mixer.music.play(-1)
        self.isPaused = False

        #self.printBoard()
        #self.insert(3,3)
        #print("")
        #self.printBoard()
        #self.displayTet(self.generateTet(1))
        print("\n "*10000)
        self.level = 1
        self.score = 0
        self.dropTime = 1
        #self.combo = (False, 0)
        while True:
            
            
            
            #curTetY = 0 if curTetType == 1 else 1 if curTetType == 3 else 2 # rotation value for the tetromino, temporary (remove soon)
            #tempHeight = curTetY
            
            self.dropTime = 0.21 - self.level * 0.01 if self.dropTime > 0.00001 else 0.005
            self.curTetType = randint(1,7) # second value is inclusive 
            self.curTetRot = randint(1,4) # rotation value for the tetromino
            self.coords = self.insert()#self.curTetType, self.curTetRot)
            while True:
                print("\n")
                self.printBoard()
                #system('cls')
                scoringList = [100,300,500,800,0]
                self.score += scoringList[self.lineCheck()-1] * self.level
                self.level = (self.score // 3000) + 1

                sleep(self.dropTime)
                if not self.fall(self.coords): break#, curTetType, curTetRot, curTetY, tempHeight): break
                #curTetY += 1
                if self.pollKey() == "exit": # self.pollJey still detects whatever the key is, just that when returns "exit" it stops the game
                    self.end()
                     

    def end(self):
        print(f"\n\n        GG, you got {self.score} points and reached level {self.level}!")
        if self.level >= 20:
            print("\n\n        Wait, you got past 19? Wow, really good job. Send a recording and Ill add your name in the hall of fame...")
        exit()
                                                


gameInst = Tetris()

if __name__ == "__main__" :
    gameInst.start()



# def rotate(coords, curTetType, rotDirection):
#     '''
#     https://ibb.co/FgsJvK1

#     Uses a rotation matrix to rotate the coordinates:
#     [[1,0,1.5],
#      [0,1,1.5],
#      [0,0,1]] 
#      x 
#     [[0,-1,0],
#      [1,0,0],
#      [0,0,1]] 
#      x 
#     [[1,0,-1.5],
#      [0,1,-1.5],
#      [0,0,1]] 
#      x 
#     [[1],
#      [0],
#      [1]] 


#     '''

#     if curTetType == 1:
#         return
#     elif curTetType == 2:
#         return
#     else:
#         return




'''
O piece will just not do anything if rotated...

I piece rotation plan
    raw: [[1,0,1.5],[0,1,1.5],[0,0,1]][[0,-1,0],[1,0,0],[0,0,1]][[1,0,-1.5],[0,1,-1.5],[0,0,1]][[1],[0],[1]]
    https://ibb.co/FgsJvK1

    Uses transformation and rotation matrices to rotate the coordinates for the I piece:
    [[1,0,1.5+offset..], # 1.5 is the centre of rotation. in order to change this to match whatever the current coordinates are, we also have to implement offsetx and offsety
     [0,1,1.5+offset..],
     [0,0,1]] 
     x 
    [[0,-1,0], # Actually does the reverse because of how array indexing works, our y value is actually the negative when rotated
     [1,0,0], # this means that even though this matrix is normally ccw, it's now cw.
     [0,0,1]] # to change, switch the -1 and 1 in (0,1) and (1,0)
     x 
    [[1,0,-1.5-offset..], 
     [0,1,-1.5-offset..],
     [0,0,1]] 
     x 
    [[1],
     [0],
     [1]] 

the operations basically go like this:
 
 coordinates -> offset to change centre of rotation to the centre (in the I piece case, shift 1.5 from base position) -> rotate the coordinates (remember, the rotation is now reversed, explained above) -> move the coordinates back to the orignal place

note: 

    [[1,0,1.5], 
     [0,1,1.5],
     [0,0,1]] 
     x 
    [[0,-1,0], 
     [1,0,0], 
     [0,0,1]]
     =
    [[0,-1,1.5], 
     [1,0,1.5], 
     [0,0,1]]


3x3 piece rotation will be based off (1,2) as the centre
matrix calculations:
raw: [[0,-1,1],[1,0,2],[0,0,1]][[1,0,-1],[0,1,-2],[0,0,1]][[1],[3],[1]]
works for all

offsetX = 0
offsetY = 0
matrixMult = [[0,-1,offsetX+offsetY],[1,0,-offsetX+offsetY],[0,0,1]]

4x4 rotation

(1,3)(2,3)(1,2)(2,2)
....
....
.00.
.00.

(1,0)(1,1)(1,2)(1,3) R ->
(3,1)(2,1)(1,1)(0,1)
(2,3)(2,2)(2,1)(2,0)
(0,2)(1,2)(2,2)(3,2) L <-
.0..
.0..
.0..
.0..


(1,3)(1,2)(2,2)(1,1) L <- 
(0,2)(1,2)(1,3)(2,2) R ->
(1,1)(1,2)(0,2)(1,3)
....
....
000.
.0..

(0,3)(1,3)(1,2)(2,2)
....
....
.00.
00..

(0,2)(1,2)(1,3)(2,3)
....
....
00..
.00.

(0,3)(1,1)(1,2)(1,3)
....
.0..
.0..
00..

(1,1)(1,2)(1,3)(2,3)
....
.0..
.0..
.00.

project idea dump
piano note detector
music generator from classical pieces
stock tracker with info
japanese sentence web scraper
tictactoe ai minmax thing
chess + ai
math quirks library - fast inverse square root library in python


'''


'''
code log
17/12  
made a lot of the starting code to render the board and make the pieces fall. started with 4 pieces: I, O, S, and L

18/12 - 
added rest of the pieces, added movement left and right with continous keyboard inputs 
refactored some stuff to take coordinates, made a plan for rotating the tetrominos with matrices

19/12 -
added check for borders when shifting left and right
added full rotation capabilities using matrix multiplication
decided to scrap plan of adding wallkicks
added music
added scoring system and failed system.
'''