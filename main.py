import math
import sys
import datetime

# using pygame as a way to add delays easily as well as easily draw a "game" board
# since I am somewhat familiar with the library; unsure if there are better libraries for this
# functionality that I have not yet explored
import pygame


# global vars such as dimensions and colour values
boardWidth = 800
boardHeight = 400
squareSize = 20
menuWidth = 400
white = (255, 255, 255)
black = (0, 0, 0)
startColour = (0, 0, 255)
endColour = (38, 215, 1)
searchingColour = (3, 252, 240)
pathColour = (255, 162, 0)
searchDelay = 200
pygame.init()
clock = pygame.time.Clock()
mainFont = pygame.font.SysFont('arial', 22)

# draw "game" board using pygame
def drawBoard(totalX, totalY, squareSize, menuWidth):
    board = pygame.display.set_mode((totalX + menuWidth, totalY))
    pygame.draw.rect(board, white, pygame.Rect(0, 0, totalX+menuWidth, totalY))
    for i in range(0, int(totalX / squareSize)):
        for j in range(0, int(totalY / squareSize)):
            pygame.draw.lines(board, (95, 0, 0), False, [(i * squareSize, j * squareSize),
                                                         (i * squareSize + squareSize, j * squareSize),
                                                         (i * squareSize + squareSize, j * squareSize + squareSize),
                                                         (i * squareSize, j * squareSize + squareSize)])
    return board

# update is called initially to load the solver
def update():
    boardWindow = drawBoard(boardWidth, boardHeight, squareSize, menuWidth)
    running = True
    mode = 0
    pathList = []
    while running:
        modeText = mainFont.render("Mode: " + str(mode),
                           True, black, white)
        instructionsFont = pygame.font.SysFont('arial', 15)
        instructions1 = instructionsFont.render("To change modes press 'Space'.",
                                               True, black, white)
        instructions2 = instructionsFont.render("Mode 0: Wall    Mode 1: Source    Mode 2: Target", True, black, white)
        instructions3 = instructionsFont.render("'G': Dijkstra", True, black, white)
        boardWindow.blit(instructions1, (boardWidth + 20, 200))
        boardWindow.blit(instructions2, (boardWidth+20, 223))
        boardWindow.blit(instructions3, (boardWidth+20, 246))
        boardWindow.blit(modeText, (boardWidth + 20, 0))

        solText = mainFont.render("The solution is " + str(len(pathList)) + " squares long", True, black, white)

        if len(pathList) != 0:
            boardWindow.blit(solText, (boardWidth + 20, 69))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #change type of square being placed on next click
                    if mode == 2:
                        mode = 0
                    else:
                        mode += 1
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_g:
                    print("Source: ", source, "Target: ", target)
                    pathList = Dijkstra(boardWindow, source, target)
                    print("Path list:") # may want to incorporate in a nicer format but printing for now
                    print(pathList)
                    for point in pathList:
                        squareX = point[0]
                        squareY = point[1]
                        pygame.draw.rect(boardWindow, pathColour,
                                         pygame.Rect(squareX, squareY, squareSize, squareSize))
                        pygame.display.flip()
                        pygame.time.wait(200) #slowing solving down for human to be able to see completed path being drawn
                if event.key == pygame.K_t:
                    print("Source: ", source, "Target: ", target)
                    pathList = aStar(boardWindow, source, target)
                    print(pathList)
                    for point in pathList:
                        squareX = point[0]
                        squareY = point[1]
                        pygame.draw.rect(boardWindow, pathColour,
                                         pygame.Rect(squareX, squareY, squareSize, squareSize))
                        pygame.display.flip()
                        pygame.time.wait(200)

                    #  Try and have a menu on left side with the grid part on the right

        #       if event.key == pygame.K_c:
        #         create()
        #create a random maze of dots (first just make it random, then focus on being solvable)
        if pygame.mouse.get_pressed()[0]:

            cursorPos = pygame.mouse.get_pos()
            print("CursorPos: " + str(cursorPos)) #debugging
            if mode == 0:
                # create wall
                Create_wall(cursorPos, boardWindow)
            if mode == 1:
                # create start pt
                source = Create_start_pt(cursorPos, boardWindow)
            if mode == 2:
                # create end pt
                target = Create_end_pt(cursorPos, boardWindow)
        if pygame.mouse.get_pressed()[2]:  #erase whatever is in that square
            print("RMB pressed")
            cursorPos = pygame.mouse.get_pos()
            print("CursorPos: " + str(cursorPos))
            erase(cursorPos, boardWindow)
        pygame.display.flip()
        clock.tick(30)
    while not running:
        print("Not running")
        quit()


def Create_wall(cursorPos, board):
    squareX = squareSize * math.floor(cursorPos[0] / squareSize)
    squareY = squareSize * math.floor(cursorPos[1] / squareSize)
    pygame.draw.rect(board, black, pygame.Rect(squareX, squareY, squareSize, squareSize))


def Create_start_pt(cursorPos, board):
    squareX = squareSize * math.floor(cursorPos[0] / squareSize)
    squareY = squareSize * math.floor(cursorPos[1] / squareSize)
    pygame.draw.rect(board, startColour, pygame.Rect(squareX, squareY, squareSize, squareSize))
    return (squareX, squareY)


def Create_end_pt(cursorPos, board):
    squareX = squareSize * math.floor(cursorPos[0] / squareSize)
    squareY = squareSize * math.floor(cursorPos[1] / squareSize)
    pygame.draw.rect(board, endColour, pygame.Rect(squareX, squareY, squareSize, squareSize))
    return (squareX, squareY)

def Dijkstra(grid, start, target):
    # Implement dijkstra's algo here
    sourceCoordText = mainFont.render("Starting vertex: " + str(start),
                           True, black, white)
    targetCoordText = mainFont.render("Ending vertex: " + str(target),
                           True, black, white)
    # textRect = text.get_rect()
    grid.blit(sourceCoordText, (boardWidth + 20, 23))
    grid.blit(targetCoordText, (boardWidth + 20, 46))
    graph = []
    startTime = datetime.datetime.now()
    for i in range(0, boardWidth, squareSize):
        for j in range(0, boardHeight, squareSize):
            if (grid.get_at((i, j))[:3] != (0, 0, 0)):
                graph.append((i, j))

    queue = []
    dist = dict()
    prev = dict()
    for vertex in graph:
        dist[vertex] = sys.maxsize
        prev[vertex] = None
        queue.append(vertex)
    dist[start] = 0

    # just calculate order of nodes and then have minimum dist function just return next and remove from list

    while len(queue) > 0:
        t = datetime.datetime.now()
        delta = t - startTime
        if int((delta.total_seconds())*1000) > (((boardHeight/squareSize) * (boardWidth/squareSize) * searchDelay) + 1000):
            print('Took too long / is impossible.  Ending program')
            break
        u = minimumDist(grid, queue, start)
        if u == -1:
            print('Took oto long / is impossible.  Ending program')
            break

        pygame.draw.rect(grid, searchingColour, pygame.Rect(u[0], u[1], squareSize, squareSize))
        pygame.display.flip()
        pygame.time.wait(searchDelay)

        queue.remove(u)

        if u == target:
            break

        neighbours = []
        neighbours = theBetterFindNeighbours(graph, u)

        for v in neighbours:
            alternatePath = dist[u] + distBetween(u, v)

            if alternatePath < dist[v]:
                dist[v] = alternatePath
                prev[v] = u

    Traceback = []
    u = target
    if (prev[u] != None) or (u == start):
        while (u != None):
            Traceback.insert(0, u)
            u = prev[u]

    return Traceback


# helper function
def distBetween(u, v):
    distX = u[0] - v[0]
    distY = u[1] - v[1]
    dist = float(math.sqrt(float(distX ** 2 + distY ** 2)))

    return dist

# helper function
def minimumDist(grid, Q, source):
    sourceX = source[0]
    sourceY = source[1]

    bestDist = sys.maxsize
    bestVertex = Q[0]
    for vertex in Q:
        # if :
        distX = vertex[0] - sourceX
        distY = vertex[1] - sourceY
        dist = float(math.sqrt(float(distX ** 2 + distY ** 2)))
        if (dist < bestDist) and (neighboursBlue(grid, vertex)):  # sometimes overwrites black walls as blue...? come back to this
            bestVertex = vertex
            bestDist = dist

    if bestVertex == Q[0] and not (neighboursBlue(grid, bestVertex)):
        return -1
    return bestVertex

# likely a better way then a bunch of very similar if blocks, come back to this
# helper function
def neighboursBlue(grid, V):
    flag = False
    if (V[0] >= squareSize) and (V[1] >= squareSize):
        if ((grid.get_at((V[0] - int(squareSize), V[1] - int(squareSize))))[:3] == startColour) or \
                ((grid.get_at((V[0] - int(squareSize), V[1] - int(squareSize))))[:3] == searchingColour):
            flag = True  ##top left
    if V[1] >= squareSize:
        if (grid.get_at((V[0], V[1] - int(squareSize))))[:3] == startColour or \
                ((grid.get_at((V[0], V[1] - int(squareSize))))[:3] == searchingColour):
            flag = True  ##top
    if (V[0] <= (boardWidth - 2 * squareSize)) and (V[1] >= squareSize):
        if (grid.get_at((V[0] + int(squareSize), V[1] - int(squareSize))))[:3] == startColour or \
                ((grid.get_at((V[0] + int(squareSize), V[1] - int(squareSize))))[:3] == searchingColour):
            flag = True  ##top right
    if V[0] >= squareSize:
        if (grid.get_at((V[0] - int(squareSize), V[1])))[:3] == startColour or \
                ((grid.get_at((V[0] - int(squareSize), V[1])))[:3] == searchingColour):
            flag = True  ##left
    if V[0] <= (boardWidth - 2 * squareSize):
        if (grid.get_at((V[0] + int(squareSize), V[1])))[:3] == startColour or \
                ((grid.get_at((V[0] + int(squareSize), V[1])))[:3] == searchingColour):
            flag = True  ##right
    if (V[0] >= squareSize) and (V[1] <= (boardHeight - 2 * squareSize)):
        if (grid.get_at((V[0] - int(squareSize), V[1] + int(squareSize))))[:3] == startColour or \
                ((grid.get_at((V[0] - int(squareSize), V[1] + int(squareSize))))[:3] == searchingColour):
            flag = True  ##bottom left
    if V[1] <= (boardHeight - 2 * squareSize):
        if (grid.get_at((V[0], V[1] + int(squareSize))))[:3] == startColour or \
                ((grid.get_at((V[0], V[1] + int(squareSize))))[:3] == searchingColour):
            flag = True  ##bottom
    if (V[0] <= (boardWidth - 2 * squareSize)) and (V[1] <= (boardHeight - 2 * squareSize)):
        if (grid.get_at((V[0] + int(squareSize), V[1] + int(squareSize))))[:3] == startColour or \
                ((grid.get_at((V[0] + int(squareSize), V[1] + int(squareSize))))[:3] == searchingColour):
            flag = True  ##bottom right

    return flag

# helper function
def theBetterFindNeighbours(graph, u):
    neighbours = []
    if (u[0] - squareSize, u[1] - squareSize) in graph:
        neighbours.append((u[0] - squareSize, u[1] - squareSize))  ##top left
    if (u[0], u[1] - squareSize) in graph:
        neighbours.append((u[0], u[1] - squareSize)) ##top
    if (u[0] + squareSize, u[1] - squareSize) in graph:
        neighbours.append((u[0] + squareSize, u[1] - squareSize))  ##top right
    if (u[0] - squareSize, u[1]) in graph:
        neighbours.append((u[0] - squareSize, u[1]))  ##left
    if (u[0] + squareSize, u[1]) in graph:
        neighbours.append((u[0] + squareSize, u[1]))  ##right
    if (u[0] - squareSize, u[1] + squareSize) in graph:
        neighbours.append((u[0] - squareSize, u[1] + squareSize))  ##bottom left
    if (u[0], u[1] + squareSize) in graph:
        neighbours.append((u[0], u[1] + squareSize))  ##bottom
    if (u[0] + squareSize, u[1] + squareSize) in graph:
        neighbours.append((u[0] + squareSize, u[1] + squareSize))  ##bottom right

    return neighbours

# helper function
def diagonalDist(grid1, grid2):
    dx = abs(grid1[0] - grid2[0]) / 20
    dy = abs(grid1[1] - grid2[1]) / 20

    diagSquare = math.sqrt(squareSize ** 2 + squareSize ** 2)
    diagDist = squareSize * (dx + dy) + (diagSquare - 2*squareSize) * min(dx, dy)
    return diagDist

# work in progress
def aStar(vertices, start, target): #theoretically a combination of gFB and dijkstra
    toVisit = []
    explored = []

    gCost = dict()
    hCost = dict()
    fCost = dict()
    prevNode = dict()

    graph = []

    for i in range(0, boardWidth, squareSize):
        for j in range(0, boardHeight, squareSize):
            if (vertices.get_at((i, j))[:3] != (0, 0, 0)):
                graph.append((i, j))

    for vertex in graph:
        gCost[vertex] = sys.maxsize
        fCost[vertex] = sys.maxsize
        #hCost[vertex] = diagonalDist(vertex, target)    #may need this line, maybe not

    toVisit.append(start)
    gCost[start] = 0
    hCost[start] = diagonalDist(start, target)
    fCost[start] = hCost[start] + gCost[start] ##But gCost is always 0 since dist from node A to Node A (start to start) is 0!!

    while len(toVisit) > 0:
        #returns key that has smallest value in the dictionary (but need min element to still be in toVisit!!!!)
        #currentNode = min(fCost, key=fCost.get)

        minCost = sys.maxsize
        minNode = start
        for node in toVisit:
            if(fCost[node] < minCost):
                minNode = node
                minCost = fCost[node]

        currentNode = minNode
        print("Current Node: ")
        print(currentNode)
        toVisit.remove(currentNode)
        explored.append(currentNode)

        if currentNode == target:
            break

        neighbours = []
        neighbours = theBetterFindNeighbours(graph, currentNode)
        for neighbour in neighbours:
            if neighbour in explored:
                pass
                #skip to next neighbour
            else:
                altG = (diagonalDist(currentNode, neighbour) + gCost[currentNode])
                if (altG < gCost[neighbour]) or (not(neighbour in toVisit)):  #new path to neighbour is shorter
                    gCost[neighbour] = altG
                    hCost[neighbour] = diagonalDist(neighbour, target)
                    fCost[neighbour] = gCost[neighbour] + hCost[neighbour]

                    prevNode[neighbour] = currentNode
                    if not (neighbour in toVisit):
                        toVisit.append(neighbour)
    traceback = []
    node = target
    if (prevNode[node] != None) or (node == start):
        while (node != None):
            traceback.insert(0, node)
            node = prevNode[node]
    return traceback


def greedyBestFirst(): # implement me later
    pass

# erase square that is clicked
def erase(cursorPos, board):
    squareX = squareSize * math.floor(cursorPos[0] / squareSize)
    squareY = squareSize * math.floor(cursorPos[1] / squareSize)
    pygame.draw.rect(board, white, pygame.Rect(squareX, squareY, squareSize, squareSize))
    pygame.draw.lines(board, (95, 0, 0), False, [
        (squareX, squareY),
        (squareX + squareSize, squareY),
        (squareX + squareSize, squareY + squareSize),
        (squareX, squareY + squareSize),
        (squareX, squareY)
    ])

# start program
update()

