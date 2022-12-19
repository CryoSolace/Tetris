# offsetX = 0
# offsetY = 0
# matrixMult = [[0,-1,offsetX+offsetY+3],[1,0,-offsetX+offsetY],[0,0,1]]
# coords = [0,2,1]
# newCoords =[]
# for row in matrixMult:
#     answer = 0
#     for item in range(len(row)):
#         answer += row[item] * coords[item]
#     newCoords.append(answer)
# print(newCoords)

# '''
# (1,0)(1,1)(1,2)(1,3) 
# (3,1)(2,1)(1,1)(0,1)
# (2,3)(2,2)(2,1)(2,0)
# (0,2)(1,2)(2,2)(3,2) 
# '''
# ##

# offsetX = 0
# offsetY = 0
# matrixMult = [[0,-1,offsetX+offsetY+3],[1,0,-offsetX+offsetY],[0,0,1]]
# coords = [1,0,1]
# newCoords =[]
# for row in matrixMult:
#     answer = 0
#     for item in range(len(row)):
#         answer += row[item] * coords[item]
#     newCoords.append(answer)
# print(newCoords)

# ### 3x3 rotation
# '''
# (1,3)(1,2)(2,2)(1,1) L <- 
# (0,2)(1,2)(1,3)(2,2) R ->
# (1,1)(1,2)(0,2)(1,3)
# '''
# rotationDir = 1 if "right" else "left"
# offsetX = 0
# offsetY = 0
# matrixMult = [[0,-1,offsetX+offsetY+3],[1,0,-offsetX+offsetY+1],[0,0,1]]
# coords = [1,2,1]
# newCoords = []
# for row in matrixMult:
#     answer = 0
#     for item in range(len(row)):
#         answer += row[item] * coords[item]
#     newCoords.append(answer)
# print(newCoords[:-1])

class Game():


    def __init__(self) -> None:
        self.offsetX = 0
        self.offsetY = 0
        self.curTetType =3
    def mult(self,rotCoords):
            rotMatrVal = -1 

            if self.curTetType == 1: return rotCoords
            elif self.curTetType == 2: 
                if rotMatrVal == "cw":
                    matrixMult = [[0,-rotMatrVal,self.offsetX+self.offsetY+3],[rotMatrVal,0,-self.offsetX+self.offsetY],[0,0,1]] 
            else:
                matrixMult = [[0,rotMatrVal,self.offsetX+self.offsetY+3],[-rotMatrVal,0,-self.offsetX+self.offsetY+1],[0,0,1]]

            coords = rotCoords
            newCoords = []
            for coord in coords: 
                coord = list(coord)
                coord.append(1) # this is so that the matrix multiplication can work, to multiply a 3x3 to a 3x1 instead of a 2x1.
                print(coord)
                curTuple = []
                for row in matrixMult:
                    answer = 0
                    for item in range(len(row)):
                        print(row[item], coord[item], answer)
                        answer += row[item] * coord[item]
                        print(answer)
                    curTuple.append(answer)
                    print(curTuple)
                newCoords.append(tuple(curTuple[:-1])) #return the new coordinates after appending the tuple but remove the trailing 1
            print(newCoords)
                
                
g = Game()
g.mult([(1, 3)])