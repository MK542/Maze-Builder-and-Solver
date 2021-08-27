import math
import pygame
import sys
import time

boardWidth = 800;
boardHeight = 400;
squareSize = 20;
white = (255, 255, 255)
black = (0, 0, 0)
start_colour = (0, 0, 255)
end_colour = (38,215,1)
searching_colour = (3, 252, 240)
path_colour = (255, 162, 0)
pygame.init()
clock = pygame.time.Clock()

def drawBoard(totalX, totalY, squareSize):
    board = pygame.display.set_mode((totalX, totalY))
    pygame.draw.rect(board, white, pygame.Rect(0, 0, totalX, totalY))
    for i in range(0, int(totalX/squareSize)):
        for j in range(0, int(totalY/squareSize)):
                pygame.draw.lines(board, (95, 0, 0), False, [(i*squareSize, j*squareSize),
                                                        (i*squareSize + squareSize, j*squareSize),
                                                        (i*squareSize + squareSize, j*squareSize + squareSize),
                                                        (i*squareSize, j*squareSize + squareSize)]);
    return board

def update():
    board_window = drawBoard(boardWidth, boardHeight, squareSize);
    running = True;
    mode = 0;
    while running:
        font = pygame.font.SysFont('arial', 22)
        text = font.render("Mode: " + str(mode),
                           True, white, black)
        textRect = text.get_rect()
        board_window.blit(text, textRect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mode == 2:
                        mode = 0;
                    else:
                        mode+=1;
                if event.key == pygame.K_q:
                    running = False;
                if event.key == pygame.K_g:
                    print("Source: ", source, "Target: ", target)
                    pathList = Dijkstra(board_window, source, target);
                    print("Path list:")
                    print(pathList)
                    for point in pathList:
                        squareX = point[0]
                        squareY = point[1]
                        pygame.draw.rect(board_window, path_colour, pygame.Rect(squareX, squareY, squareSize, squareSize));
                        pygame.display.flip()
                        pygame.time.wait(200)

                    ##  Have it start running here.  Also have a button on GUI to start it
                    ##  Try and have a menu on left side with the grid part on the right
         ##       if event.key == pygame.K_c:
         ##          create();
                    ##create a random maze of dots (first just make it random, then focus on being solvable)
        if pygame.mouse.get_pressed()[0]:##create a wall
            print("LMB pressed");
            cursor_pos = pygame.mouse.get_pos();
            print("Cursor_pos: " + str(cursor_pos));
            if mode == 0:
                #create wall
                create_wall(cursor_pos, board_window);
            if mode == 1:
                #create start pt
                source = create_start_pt(cursor_pos, board_window);
            if mode == 2:
                #create end pt
                target = create_end_pt(cursor_pos, board_window);
        if pygame.mouse.get_pressed()[2]:##erase whatever is in that square
            print("RMB pressed");
            cursor_pos = pygame.mouse.get_pos();
            print("Cursor_pos: " + str(cursor_pos));
            erase(cursor_pos, board_window);
        pygame.display.flip()
        clock.tick(30)
    while not running:
        print("Not running");
        quit();

def create_wall(cursor_pos, board):
    squareX = squareSize*math.floor(cursor_pos[0]/squareSize);
    squareY = squareSize*math.floor(cursor_pos[1]/squareSize);
    pygame.draw.rect(board, black, pygame.Rect(squareX, squareY, squareSize, squareSize));
def create_start_pt(cursor_pos, board):
    squareX = squareSize * math.floor(cursor_pos[0] / squareSize);
    squareY = squareSize * math.floor(cursor_pos[1] / squareSize);
    pygame.draw.rect(board, start_colour, pygame.Rect(squareX, squareY, squareSize, squareSize));
    return (squareX, squareY)
def create_end_pt(cursor_pos, board):
    squareX = squareSize * math.floor(cursor_pos[0] / squareSize);
    squareY = squareSize * math.floor(cursor_pos[1] / squareSize);
    pygame.draw.rect(board, end_colour, pygame.Rect(squareX, squareY, squareSize, squareSize));
    return (squareX, squareY)

##def begin():
    #start the A* thing here

def Dijkstra(grid, start, target):
    #Implement dijkstra's algo here
    graph = [];
    for i in range(0, boardWidth, squareSize):
        for j in range(0, boardHeight, squareSize):
            graph.append((i, j))

    queue = [];
    dist = dict();
    prev = dict();
    for vertex in graph:

        dist[vertex] = sys.maxsize;
        prev[vertex] = None;
        queue.append(vertex);
    dist[start] = 0;

    while len(queue) > 0:
        u = minimumDist(grid, queue, start)
        print('Currently considering', u, 'with a distance of', dist[u])

        pygame.draw.rect(grid, searching_colour, pygame.Rect(u[0], u[1], squareSize, squareSize));
        pygame.display.flip()
        pygame.time.wait(250)

        queue.remove(u);

        if u == target:
            break

        neighbours = findNeighbours(grid, u)

        for v in neighbours:
            alternatePath = dist[u] + distBetween(u, v);
            # print("alternate path: ", alternatePath)
            # print("v", v)
            # print("dist", dist)
            # print("dist[v]", dist[v])
            if alternatePath < dist[v]:
                dist[v] = alternatePath;
                prev[v] = u;

    Traceback = [];
    u = target
    if (prev[u]!= None) or (u == start):
        while (u != None):
            Traceback.insert(0, u);
            u = prev[u];
    return Traceback;

def distBetween(u, v):
    distX = u[0] - v[0]
    distY = u[1] - v[1]
    dist = float(math.sqrt(float(distX ** 2 + distY ** 2)))

    return dist

def minimumDist(grid, Q, source):
    sourceX = source[0]
    sourceY = source[1]

    bestDist = 999999999
    bestVertex = Q[0]
    for vertex in Q:
        if ((grid.get_at((vertex[0] + int(squareSize/2), vertex[1] + int(squareSize/2))))[:3] != (0, 0, 0)):
            distX = vertex[0] - sourceX
            distY = vertex[1] - sourceY
            dist = float(math.sqrt(float(distX**2 + distY ** 2)))
            if dist < bestDist:
                bestVertex = vertex
                bestDist = dist
    return bestVertex

def findNeighbours(grid, u): ##consider walls here
    neighbours = []
    if ((u[0] >= squareSize) and (u[1] >= squareSize)
            and ((grid.get_at((u[0] - int(squareSize/2), u[1] - int(squareSize/2))))[:3] != (0, 0, 0))):
        neighbours.append((u[0] - squareSize, u[1] - squareSize));  ##top left
    if (u[1] >= squareSize) and ((grid.get_at((u[0], u[1] - int(squareSize/2))))[:3] != (0, 0, 0)):
        neighbours.append((u[0], u[1] - squareSize));  ##top
    if ((u[0] <= (boardWidth - 2 * squareSize)) and (u[1] >= squareSize)
        and ((grid.get_at((u[0] + int(squareSize/2), u[1] - int(squareSize/2))))[:3] != (0, 0, 0))):
            neighbours.append((u[0] + squareSize, u[1] - squareSize));  ##top right
    if u[0] >= squareSize and ((grid.get_at((u[0] - int(squareSize/2), u[1])))[:3] != (0, 0, 0)):
        neighbours.append((u[0] - squareSize, u[1]));  ##left
    if (u[0] <= (boardWidth - 2*squareSize)) \
            and ((grid.get_at((u[0] + int(squareSize/2), u[1])))[:3] != (0, 0, 0)):
        neighbours.append((u[0] + squareSize, u[1]));  ##right
    if ((u[0] >= squareSize) and (u[1] <= (boardHeight - 2*squareSize)))\
            and ((grid.get_at((u[0] - int(squareSize/2), u[1] + int(squareSize/2))))[:3] != (0, 0, 0)):
        neighbours.append((u[0] - squareSize, u[1] + squareSize))  ##bottom left
    if (u[1] <= (boardHeight - 2*squareSize))\
            and ((grid.get_at((u[0], u[1] + int(squareSize/2))))[:3] != (0, 0, 0)):
        neighbours.append((u[0], u[1] + squareSize));  ##bottom
    if ((u[0] <= (boardWidth - 2*squareSize)) and (u[1] <= (boardHeight - 2*squareSize)))\
            and ((grid.get_at((u[0] + int(squareSize/2), u[1] + int(squareSize/2))))[:3] != (0, 0, 0)):
        neighbours.append((u[0] + squareSize, u[1] + squareSize));  ##bottom right

    return neighbours

def erase(cursor_pos, board):
    squareX = squareSize * math.floor(cursor_pos[0] / squareSize);
    squareY = squareSize * math.floor(cursor_pos[1] / squareSize);
    pygame.draw.rect(board, white, pygame.Rect(squareX, squareY, squareSize, squareSize))
    pygame.draw.lines(board, (95, 0, 0), False, [
                                                 (squareX, squareY),
                                                 (squareX + squareSize, squareY),
                                                 (squareX + squareSize, squareY + squareSize),
                                                 (squareX, squareY + squareSize),
                                                 (squareX, squareY)
                                                ]);

update();
print("Should not get this far");



