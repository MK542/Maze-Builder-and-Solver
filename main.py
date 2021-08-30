import math
import pygame
import sys
import datetime

boardWidth = 800
boardHeight = 400
squareSize = 20
menuWidth = 400
white = (255, 255, 255)
black = (0, 0, 0)
start_colour = (0, 0, 255)
end_colour = (38, 215, 1)
searching_colour = (3, 252, 240)
path_colour = (255, 162, 0)
searchDelay = 200
pygame.init()
clock = pygame.time.Clock()
mainFont = pygame.font.SysFont('arial', 22)


def drawBoard(totalX, totalY, squareSize, menuWidth):
    board = pygame.display.set_mode((totalX + menuWidth, totalY))
    pygame.draw.rect(board, white, pygame.Rect(0, 0, totalX+menuWidth, totalY))
    for i in range(0, int(totalX / squareSize)):
        for j in range(0, int(totalY / squareSize)):
            pygame.draw.lines(board, (95, 0, 0), False, [(i * squareSize, j * squareSize),
                                                         (i * squareSize + squareSize, j * squareSize),
                                                         (i * squareSize + squareSize, j * squareSize + squareSize),
                                                         (i * squareSize, j * squareSize + squareSize)]);
    return board


def update():
    board_window = drawBoard(boardWidth, boardHeight, squareSize, menuWidth);
    running = True;
    mode = 0;
    pathList = []
    while running:
        modeText = mainFont.render("Mode: " + str(mode),
                           True, black, white)
        instructionsFont = pygame.font.SysFont('arial', 15)
        instructions1 = instructionsFont.render("To change modes press 'Space'.",
                                               True, black, white)
        instructions2 = instructionsFont.render("Mode 0: Wall    Mode 1: Source    Mode 2: Target", True, black, white)
        board_window.blit(instructions1, (boardWidth + 20, 200))
        board_window.blit(instructions2, (boardWidth+20, 223))
        board_window.blit(modeText, (boardWidth + 20, 0))
        solText = mainFont.render("The solution is " + str(len(pathList)) + " squares long", True, black, white)
        if len(pathList) != 0:
            board_window.blit(solText, (boardWidth + 20, 69))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False;
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mode == 2:
                        mode = 0;
                    else:
                        mode += 1;
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
                        pygame.draw.rect(board_window, path_colour,
                                         pygame.Rect(squareX, squareY, squareSize, squareSize));
                        pygame.display.flip()
                        pygame.time.wait(200)

        if pygame.mouse.get_pressed()[0]:  ##create a wall
            print("LMB pressed");
            cursor_pos = pygame.mouse.get_pos();
            print("Cursor_pos: " + str(cursor_pos));
            if mode == 0:
                # create wall
                create_wall(cursor_pos, board_window);
            if mode == 1:
                # create start pt
                source = create_start_pt(cursor_pos, board_window);
            if mode == 2:
                # create end pt
                target = create_end_pt(cursor_pos, board_window);
        if pygame.mouse.get_pressed()[2]:  ##erase whatever is in that square
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
    squareX = squareSize * math.floor(cursor_pos[0] / squareSize);
    squareY = squareSize * math.floor(cursor_pos[1] / squareSize);
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

def Dijkstra(grid, start, target):
    # Implement dijkstra's algo here
    sourceCoordText = mainFont.render("Starting vertex: " + str(start),
                           True, black, white)
    targetCoordText = mainFont.render("Ending vertex: " + str(target),
                           True, black, white)
    # textRect = text.get_rect()
    grid.blit(sourceCoordText, (boardWidth + 20, 23))
    grid.blit(targetCoordText, (boardWidth + 20, 46))
    graph = [];
    startTime = datetime.datetime.now()
    for i in range(0, boardWidth, squareSize):
        for j in range(0, boardHeight, squareSize):
            if (grid.get_at((i, j))[:3] != (0, 0, 0)):
                graph.append((i, j))

    queue = [];
    dist = dict();
    prev = dict();
    for vertex in graph:
        dist[vertex] = sys.maxsize;
        prev[vertex] = None;
        queue.append(vertex);
    dist[start] = 0;

    # just calculate order of nodes and then have minimum dist function just return next and remove from list

    while len(queue) > 0:
        t = datetime.datetime.now()
        delta = t - startTime
        if int((delta.total_seconds())*1000) > (((boardHeight/squareSize) * (boardWidth/squareSize) * searchDelay) + 1000):
            print('Took to long / is impossible.  Ending program')
            break
        u = minimumDist(grid, queue, start)
        if u == -1:
            print('Took to long / is impossible.  Ending program')
            break

        pygame.draw.rect(grid, searching_colour, pygame.Rect(u[0], u[1], squareSize, squareSize));
        pygame.display.flip()
        pygame.time.wait(searchDelay)

        queue.remove(u);

        if u == target:
            break

        neighbours = []
        neighbours = TheBetterFindNeighbours(graph, u)

        for v in neighbours:
            alternatePath = dist[u] + distBetween(u, v);
            if alternatePath < dist[v]:
                dist[v] = alternatePath;
                prev[v] = u;

    Traceback = [];
    u = target
    if (prev[u] != None) or (u == start):
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

    bestDist = sys.maxsize
    bestVertex = Q[0]
    for vertex in Q:
        # if :
        distX = vertex[0] - sourceX
        distY = vertex[1] - sourceY
        dist = float(math.sqrt(float(distX ** 2 + distY ** 2)))
        if (dist < bestDist) and (neighboursBlue(grid, vertex)):  ## sometimes overwrites black walls as blue...? tf?
            bestVertex = vertex
            bestDist = dist

    if bestVertex == Q[0] and not (neighboursBlue(grid, bestVertex)):
        return -1
    return bestVertex


def neighboursBlue(grid, V):
    flag = False;
    if (V[0] >= squareSize) and (V[1] >= squareSize):
        if ((grid.get_at((V[0] - int(squareSize), V[1] - int(squareSize))))[:3] == start_colour) or \
                ((grid.get_at((V[0] - int(squareSize), V[1] - int(squareSize))))[:3] == searching_colour):
            flag = True  ##top left
    if V[1] >= squareSize:
        if (grid.get_at((V[0], V[1] - int(squareSize))))[:3] == start_colour or \
                ((grid.get_at((V[0], V[1] - int(squareSize))))[:3] == searching_colour):
            flag = True  ##top
    if (V[0] <= (boardWidth - 2 * squareSize)) and (V[1] >= squareSize):
        if (grid.get_at((V[0] + int(squareSize), V[1] - int(squareSize))))[:3] == start_colour or \
                ((grid.get_at((V[0] + int(squareSize), V[1] - int(squareSize))))[:3] == searching_colour):
            flag = True  ##top right
    if V[0] >= squareSize:
        if (grid.get_at((V[0] - int(squareSize), V[1])))[:3] == start_colour or \
                ((grid.get_at((V[0] - int(squareSize), V[1])))[:3] == searching_colour):
            flag = True  ##left
    if V[0] <= (boardWidth - 2 * squareSize):
        if (grid.get_at((V[0] + int(squareSize), V[1])))[:3] == start_colour or \
                ((grid.get_at((V[0] + int(squareSize), V[1])))[:3] == searching_colour):
            flag = True  ##right
    if (V[0] >= squareSize) and (V[1] <= (boardHeight - 2 * squareSize)):
        if (grid.get_at((V[0] - int(squareSize), V[1] + int(squareSize))))[:3] == start_colour or \
                ((grid.get_at((V[0] - int(squareSize), V[1] + int(squareSize))))[:3] == searching_colour):
            flag = True  ##bottom left
    if V[1] <= (boardHeight - 2 * squareSize):
        if (grid.get_at((V[0], V[1] + int(squareSize))))[:3] == start_colour or \
                ((grid.get_at((V[0], V[1] + int(squareSize))))[:3] == searching_colour):
            flag = True  ##bottom
    if (V[0] <= (boardWidth - 2 * squareSize)) and (V[1] <= (boardHeight - 2 * squareSize)):
        if (grid.get_at((V[0] + int(squareSize), V[1] + int(squareSize))))[:3] == start_colour or \
                ((grid.get_at((V[0] + int(squareSize), V[1] + int(squareSize))))[:3] == searching_colour):
            flag = True  ##bottom right

    return flag


def TheBetterFindNeighbours(graph, u):
    neighbours = []
    if (u[0] - squareSize, u[1] - squareSize) in graph:
        neighbours.append((u[0] - squareSize, u[1] - squareSize));  ##top left
    if (u[0], u[1] - squareSize) in graph:
        neighbours.append((u[0], u[1] - squareSize));  ##top
    if (u[0] + squareSize, u[1] - squareSize) in graph:
        neighbours.append((u[0] + squareSize, u[1] - squareSize));  ##top right
    if (u[0] - squareSize, u[1]) in graph:
        neighbours.append((u[0] - squareSize, u[1]));  ##left
    if (u[0] + squareSize, u[1]) in graph:
        neighbours.append((u[0] + squareSize, u[1]));  ##right
    if (u[0] - squareSize, u[1] + squareSize) in graph:
        neighbours.append((u[0] - squareSize, u[1] + squareSize))  ##bottom left
    if (u[0], u[1] + squareSize) in graph:
        neighbours.append((u[0], u[1] + squareSize));  ##bottom
    if (u[0] + squareSize, u[1] + squareSize) in graph:
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
