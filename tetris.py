from time import sleep # Used for waiting to generate each frame
from random import randint # Used to randomly select a tetromino 
from msvcrt import kbhit, getch # Used for keypresses
from sys import exit # Used to end the game
import pygame # Used for music

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

    def printBoard(self): # Prints the board
        for y in range(len(self.board)):
            temp = "" # Stores the final current board row state
            for x in self.board[y]:
                temp += x * 3 # Adds 3 to the temp to compensate for height
            
            # Adds score and level next to the board
            center = 30
            if y == 10:
                print(" " * center + temp + "      SCORE") 
                print(" " * center + temp + f"      {self.score}")
            elif y == 15:
                print(" " * center + temp + "      LEVEL")
                print(" " * center + temp + f"      {self.level}")
            else: 
                print(" " * center + temp)
                print(" " * center + temp)

    def insert(self): # Spawns a new tetromino and inserts it into the board
        self.offsetX = 0
        self.offsetY = 0

        coords = list(self.tetrominoDict[self.curTetType]) # Takes the list given the random number from the dictionary
        coords = self.rotate(coords,"cw",True) # Calls rotate. cw = clockwise, ccw = counterclockwise

        for coord in coords: # Inserts "O" at each coordinate given
            self.board[coord[1]][coord[0]+3] = "O" # +3 used to offset X
        
        newCoords = []
        for coord in coords:
            newCoords.append((coord[0]+3,coord[1])) # Also changes all the coordinates to be offset

        self.offsetX = 3 # Offset X is accounted for here, just needed 0 at the start for the initial rotation
        return newCoords

    def fall(self, coords): # Makes the tetromino fall continuously until it reaches an illegal state

        newCoords = [] 
        hasLanded = False

        for coord in coords: 
            if coord[1]+1 == len(self.board) or self.board[coord[1]+1][coord[0]] == "0": # Checks if has reached the bottom or if the character under is 0
                hasLanded = True
            if hasLanded and self.offsetY == 0: # If it has landed but it hasn't moved yet, then it must have reached the ceiling. End the game.
                self.end() 
                
        for coord in coords: # Changes all the "O"s into "."s
            self.board[coord[1]][coord[0]] = "."

        for coord in coords: 
            if hasLanded:
                self.board[coord[1]][coord[0]] = "0" # If it's landed, change the characters to signify this.
                newCoords.append(coord) # Do nothing to the original coordinates
            else:
                self.board[coord[1]+1][coord[0]] = "O" # Else, move it down 1.
                newCoords.append((coord[0],coord[1]+1)) # Change the original coordinates
        
        self.coords = newCoords # Set the coordinates of the new piece to be the new coordiantes
        self.offsetY += 1 # Increase the offset for the rotation

        return not hasLanded # Will continuously fall until it has landed

    def shift(self,coords,move): # Makes the tetromino move left or right depending on what is given
        for coord in coords:
            self.board[coord[1]][coord[0]] = "." # Erases all current "O"s
            # Note: Causes blinking effect when trying to move out of bounds
            # FEATURE NOT A BUG

        newCoords = []
        for coord in coords: # First, verify if this is a legal move
            if (move == "left" and (coord[0]-1 == -1 or self.board[coord[1]][coord[0]-1] == "0") ): return
            # Checks left boundaries, if at the edge or if there is a piece there. 
            elif (move == "right" and (coord[0]+1 == len(self.board[0]) or self.board[coord[1]][coord[0]+1] == "0")) : return
            # Checks right boundaries with the same logic.
        
        # Only if it's a legal move can we actually move it there.
        for coord in coords: 
            if move == "left": # If we're moving left
                self.board[coord[1]][coord[0]-1] = "O"
                newCoords.append((coord[0]-1,coord[1])) # Move it left
            else: # If we're moving right
                self.board[coord[1]][coord[0]+1] = "O"
                newCoords.append((coord[0]+1,coord[1])) # Move it right             

        # Determines what should be done to the offset
        if move == "left" : self.offsetX -= 1
        else: self.offsetX += 1

        self.coords = newCoords # No return value because the coordinates are modified here already


    def rotate(self, coords, direction="cw", isFirst = False):

        for coord in coords:
            self.board[coord[1]][coord[0]] = "." # Erases all current "O"s
            # Note: Causes blinking effect when trying to move out of bounds
            # FEATURE NOT A BUG

        def applyRotation(rotCoords, direction="cw"):
            # This is pretty complicated to explain. See the bottom of the code for a more detailed explanation
            if self.curTetType == 1: return rotCoords # The O piece does not rotate
            elif self.curTetType == 2: # The I piece will rotate a unique way
                if direction == "cw": 
                    matrixMult = [[0,-1,self.offsetX+self.offsetY+3],[1,0,-self.offsetX+self.offsetY],[0,0,1]] 
                else:
                    matrixMult = [[0,1,self.offsetX-self.offsetY],[-1,0,self.offsetX+self.offsetY+3],[0,0,1]] 
            else: # The rest of the pieces will rotate the same
                if direction == "cw": 
                    matrixMult = [[0,-1,self.offsetX+self.offsetY+3],[1,0,-self.offsetX+self.offsetY+1],[0,0,1]]
                else:
                    matrixMult = [[0,1,self.offsetX-self.offsetY-1],[-1,0,self.offsetX+self.offsetY+3],[0,0,1]]


            newCoords = []
            for coord in rotCoords: # For each coordinate in the given coordinates
                coord = list(coord) 
                coord.append(1) # This is so that the matrix multiplication can work, so that we're multiplying a 3x3 to a 3x1 instead of a 2x1.
                curTuple = [] # Stores the coordinates of the final output

                for row in matrixMult: # Implementation of matrix multiplication
                    answer = 0
                    for item in range(len(row)):
                        answer += row[item] * coord[item]
                    curTuple.append(answer)

                newCoords.append(tuple(curTuple[:-1])) # Return the new coordinates after appending the tuple but remove the trailing 1
            
            # Final checks.
            for coord in newCoords:
                if self.board[coord[1]][coord[0]] == "0": # If any of the coordinates is already occupied, return the original coordinates
                    return rotCoords
                for num in coord: # If any of the coordinates has a number less than 0, return the original coordinates
                    if num < 0:
                        return rotCoords
                if coord[1] >= len(self.board): # If any of the x coordinates has a number greater than the size of the board, return the original coordinates
                    return rotCoords

            return newCoords # Returns the final rotated coordinates if successful
                
                


        if isFirst: # If the piece has just spawned, rotate it multiple times
            for i in range(self.TetRot-1):
                coords = applyRotation(coords,direction)
        else: # Otherwise, just rotate it once
            coords = applyRotation(coords,direction)
            self.stop = True

        return coords

    def lineCheck(self):
        # Loops through each line and checks whether or not that line is full

        clearRows = [] # Indices of rows which are clear
        for row in range(len(self.board)): 
            skipLine = False
            for char in self.board[row]:
                if char != "0": # If one of the members is not a piece
                    skipLine = True
                    break # Skip to the next row

            if skipLine: continue
            else: # If it is a full row, add it to the clearRows list
                clearRows.append(row)

        for row in clearRows: # Go through all the clear Rows
            self.board[row] = ["." for _ in range(10)] # Make the row empty
            self.printBoard() # Display the row without the full row for 1 frame
            sleep(0.02)
            del self.board[row] # Delete the row
            self.board.insert(0, ["." for _ in range(10)]) # Reinsert the row back to the start
            self.printBoard() 

        return len(clearRows) # Used for scoring
                

    def pollKey(self): # Takes in the input
        '''
            Useful return values given keypress:

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
        
        inp = kbhit() # This is magic idk how this works, i got it off stack overflow
        key = ord(getch()) if inp else 0

        if key == 75:
            self.shift(self.coords,"left") # move left
        elif key == 77:
            self.shift(self.coords,"right") # move right
        elif key == 72:
            self.coords = self.rotate(self.coords,"cw") # up is rotate cw
        elif key == 80:
            self.coords = self.rotate(self.coords,"ccw") # down is rotate ccw
        elif key == 109:
            if self.isPaused: pygame.mixer.music.unpause()
            else: pygame.mixer.music.pause()
            self.isPaused = not self.isPaused
        elif key == 32: # spacebar simulates hard drop
            self.dropTime = 0.001 # by setting the interval of each frame to a really low number
        elif key == 27: # esc stops the game
            return "exit"
        return "continue"
            
    def start(self): # Starts the game
        print("\n\n                 Welcome to TETRIS in Python by CryoSolace!\n")
        print("                     Press enter to start.")
        print("                     Press left/right to move and up/down to Rotate.")
        print("                     Press esc to stop playing.")
        print("                     Press m to mute/unmute the music.\n")
        print("                     Levels advance after every 2000 points. Level 21 is virtually impossible.")
        print("                     ps. No combos, no wall kicks, I think no T-spins either :( ")
        input()

        pygame.init() # Solely used to loop music
        try:
            pygame.mixer.music.load('Tetris_Music.mp3')# <---- Here!
            pygame.mixer.music.play(-1) # -1 = Loop the music
        except:
            print("\n\n                 Music not loaded. Try replacing the directory in line 243 with wherever the music file is.")
            print("                 Alternatively: https://www.youtube.com/watch?v=VCrxWHTCNo8")
            print("                 Press enter to continue.")
            input()
            
        
        self.isPaused = False # Used to toggle on/off for the music

        print("\n"*10000) # Basically a clear screen

        # Extra initialisation relevant to the game
        self.level = 1
        self.score = 0
        self.dropTime = 0.20

        while True:
            
            self.dropTime = 0.21 - self.level * 0.01 if self.dropTime > 0.00001 else 0.005 # Rules for the level system
            self.curTetType = randint(1,7) # Chooses from 1 of 7 tetrominos
            self.TetRot = randint(1,4) # Chooses a random rotation
            self.coords = self.insert() # Insertwws the tetromino on the board, taking into account rotation

            while True:
                print("\n")
                self.printBoard()
                scoringList = [100,300,500,800,0] # Scoring system. 0 is at the end because in the line below, selflineCheck()-1 will return -1 if there are no full lines.
                self.score += scoringList[self.lineCheck()-1] * self.level 
                self.level = (self.score // 2000) + 1 # Level systems, advances every 2000 points.

                sleep(self.dropTime) # Determines the speed of each frame.

                if not self.fall(self.coords): break # The tetromino will fall until self.fall detects that it shouldn't, at which point it breaks the loop

                if self.pollKey() == "exit": # self.pollKey detects whatever the key is, but if it returns "exit" it stops the game
                    self.end()
                     

    def end(self): # Ending messages
        print(f"\n\n                    GG, you got {self.score} points and reached level {self.level}!")
        if self.level >= 20:
            print("\n\n                     Wait, you got past 19? Wow, really good job. Send a recording and Ill add your name in the hall of fame...")
        exit() # this is sys.exit()
                                                

gameInst = Tetris()

if __name__ == "__main__" :
    gameInst.start()



'''
Notes on the rotation:

The rotations for this uses rotation and transformation matrices to reposition the centre of the tetromino, rotate it as if it were about 
the origin, then transform it back to the original position. However, rotation is reversed (explained below)

O piece will just not do anything if rotated.

I piece rotation:

    raw sample: [[1,0,1.5],[0,1,1.5],[0,0,1]],[[0,-1,0],[1,0,0],[0,0,1]][[1,0,-1.5],[0,1,-1.5],[0,0,1]][[1],[0],[1]]
    https://ibb.co/FgsJvK1

    Uses transformation and rotation matrices to rotate the coordinates for the I piece:
    [[1,0,1.5+offsetX], # 1.5 is the centre of rotation. in order to change this to match whatever the current coordinates are, we also have to implement offsetx and offsety
     [0,1,1.5+offsetY],
     [0,0,1]] 
     x 
    [[0,-1,0], # Actually does the reverse because of how array indexing works, our y value is actually the negative when rotated
     [1,0,0], # this means that even though this matrix is normally ccw, it's now cw.
     [0,0,1]] # to change, switch the -1 and 1 in (0,1) and (1,0)
     x 
    [[1,0,-1.5-offsetX], # Reposition back
     [0,1,-1.5-offsetY],
     [0,0,1]] 
     x 
    [[1], # Your coordinates
     [0],
     [1]] # Ignore this 1

The operations basically go like this:
 
Coordinates -> offset to change centre of rotation to the centre (in the I piece case, shift 1.5 from base position) -> rotate the coordinates (remember, the rotation is now reversed, explained above) -> move the coordinates back to the orignal place

Note: In the program, the value of the 3x3 matrices has been computed before hand, taking into account the offsets.


3x3 piece rotation will be based off (1,2) as the centre
matrix calculations:
raw: [[0,-1,1],[1,0,2],[0,0,1]][[1,0,-1],[0,1,-2],[0,0,1]][[1],[3],[1]]
works for all

offsetX = 0
offsetY = 0
matrixMult = [[0,-1,offsetX+offsetY],[1,0,-offsetX+offsetY],[0,0,1]]

4x4 rotation (Coords starting position is either alone or noted by R ->)

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

'''


'''
code log

17/12/22  
project started.
made a lot of the starting code to render the board and make the pieces fall. started with 4 pieces: I, O, S, and L

18/12/22 - 
added rest of the pieces, added movement left and right with continous keyboard inputs 
refactored some stuff to take coordinates, made a plan for rotating the tetrominos with matrices

19/12/22 -
added check for borders when shifting left and right
added full rotation capabilities using matrix multiplication
decided to scrap plan of adding wallkicks
added music
added scoring system and failed system.
fixed some bugs, refactored code, added comments
project completed.
'''
