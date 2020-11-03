import pygame
import random
import tkinter
pygame.init()

WIDTH = 500
HEIGHT = 500
ROWS = 20
COLS = 20
GAP = WIDTH // ROWS

class cube(object):
    def __init__(self, start, color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color
        
    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)
    
    def draw(self, win, eyes=False):
        i = self.pos[0]
        j = self.pos[1]

        pygame.draw.rect(win, self.color, (i*GAP+1, j*GAP+1, GAP-2, GAP-2))

        if eyes:
            centre = GAP // 2
            radius = 3
            leftEyePos = (i*GAP+centre-radius, j*GAP+8)
            rightEyePos = (i*GAP+GAP-radius*2, j*GAP+8)
            pygame.draw.circle(win, (0,0,0), leftEyePos, radius)
            pygame.draw.circle(win, (0,0,0), rightEyePos, radius)
        

class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)

        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.dirnx = -1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_RIGHT]:
                self.dirnx = 1
                self.dirny = 0
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_UP]:
                self.dirnx = 0
                self.dirny = -1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
            elif keys[pygame.K_DOWN]:
                self.dirnx = 0
                self.dirny = 1
                self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        
        for i, c in enumerate(self.body):
            p = c.pos[:]        # c.pos[:] return the cube position as a list
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)
            else:
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (COLS-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= COLS-1: c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= ROWS-1: c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0], ROWS-1)
                else: c.move(c.dirnx, c.dirny)

    def reset(self, pos):
        self.body = []
        self.head = cube(pos)
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1, tail.pos[1])))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1]+1)))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1]-1)))
        
        

    def draw(self, win):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(win, True)
            else:
                c.draw(win)


def drawGrid(win):

    x, y = 0, 0
    for i in range(1, ROWS):
        x = i * GAP
        y = i * GAP

        pygame.draw.line(win, (255, 255, 255), (x,0), (x,HEIGHT))
        pygame.draw.line(win, (255, 255, 255), (0,y), (WIDTH,y))
        

def redrawWindow(win):
    win.fill((0,0,0))
    s.draw(win)
    snack.draw(win)
    drawGrid(win)
    pygame.display.update()


def randomSnack(s):
    positions = s.body

    while True:
        x = random.randrange(ROWS)
        y = random.randrange(ROWS)
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:       # get all the Snack position which is same as the position of a body
            continue
        else:
            break
    return (x,y)



def message_box(subject, content):
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    tkinter.messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def main():
    global s, snack
    win = pygame.display.set_mode((WIDTH, HEIGHT))

    s = snake((255, 0, 0), (10, 10))

    clock = pygame.time.Clock()
    run = True
    snack = cube(randomSnack(s), color = (0, 255, 0))
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(s), color=(0,255,0))
        
        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break
        redrawWindow(win)



main()
