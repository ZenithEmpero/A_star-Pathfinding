import pygame as pg, math as m
from map import *
from settings import *
class Nodes:
    def __init__(self, game) -> None:
        self.game = game
        self.window = game.window
        self.nodes = []
        
        self.start_node = None
        self.end_node = None
        self.gen_path = True
        y = node_gap_size * .5
        un = 0
        for i in map:
            x = node_gap_size * .5
            for o in i:
                if o == 0:
                    node_color = 'white'
                elif o == 1:
                    node_color = '#383838'
                elif o == 2:
                    node_color = 'green'
                elif o == 3:
                    node_color = 'blue'
                self.nodes.append(Node(self, x, y, node_color, node_rect_size, un, o))
                un += 1
                x += node_add
            y += node_add
        
        for i in self.nodes:
            if i.node_type == 2:
               self.start_node = i
            if i.node_type == 3:
               self.end_node = i

    def draw(self):
        for i in self.nodes:
            pg.draw.rect(self.window, i.color, i.rect_val)

    def update(self):
        for i in self.nodes:
            i.update()
        self.genPath()

    def genPath(self):
        if self.gen_path:
            x = {}
            for i in self.nodes:
                if i.clicked == False and i.showText == True:
                    x[i.F] = i
            x = dict(sorted(x.items()))
            pg.time.delay(50)
            if len(x) != 0:
                x[list(x)[0]].clickEvent()

class Node:
    def __init__(self, nodes, x, y, color, size, num, nt) -> None:
        self.grid = nodes
        self.game = nodes.game
        self.window = nodes.window
        self.nodes = nodes.nodes
        self.pos = [x, y]
        self.cpos = [x + size//2, y + size//2]
        self.or_color = color
        self.color = color
        self.size = [size, size]
        self.rect_val = pg.Rect(x, y, self.size[0], self.size[1])
        self.unique_num = num
        self.node_type = nt
        self.origin_node = None
        self.or_origin_node = None
        self.activated = False
        

        #FONT
        self.font1 = pg.font.Font(None, 35)
        self.font2 = pg.font.Font(None, 20)
        self.showText = False
        self.clicked = False

        #IMG
        self.img_angle = 120
        self.or_arrow_img = pg.image.load('img/arrow_b.png')
        self.arrow_img = pg.transform.rotate(self.or_arrow_img, self.img_angle)
        self.arrow_img_rect = self.arrow_img.get_rect()
        self.arrow_img_rect.center = self.cpos
        self.showIMG = False
        

        self.G = 0
        self.H = 0
        self.F = 0

        self.mouse_hover = False
        self.surrounding_nodes = []

    def checkMouseHover(self):
        mouse_pos = pg.mouse.get_pos()
        if self.rect_val.collidepoint(mouse_pos):
            self.mouse_hover = True
        else:
            self.mouse_hover = False

    def draw(self):
        
        if self.showText:
            self.f_drawText()
            self.g_drawText()
            self.h_drawText()
        if self.node_type != 1:
            #self.drawArrow()
            pass

    def update(self):

        self.draw()
        self.checkMouseHover()
        self.checkEvents()
        self.checkFinished()

    def f_drawText(self):
        self.text_surf = self.font1.render(str(self.F), False, 'black')
        self.window.blit(self.text_surf, (self.cpos[0] - 14, self.cpos[1]))

    def g_drawText(self):
        self.text_surf = self.font2.render(str(self.G), False, 'black')
        self.window.blit(self.text_surf, (self.cpos[0] - 25, self.cpos[1] - 20))

    def h_drawText(self):
        self.text_surf = self.font2.render(str(self.H), False, 'black')
        self.window.blit(self.text_surf, (self.cpos[0] + 10, self.cpos[1] - 20))

    def checkEvents(self):
        for event in self.game.events:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and self.mouse_hover and self.node_type != 1:
                self.clickEvent()
                    

    def clickEvent(self):
        self.start_node = self.grid.start_node
        self.end_node = self.grid.end_node
        if self.node_type != 2 and self.node_type != 1:
            self.color = '#9cff59'
            self.showText = True
            self.calculateValues()
            self.clicked = True
            self.showIMG = True
        self.getSurroundingNodes()
        for i in self.surrounding_nodes:
            #if i.origin_node == None:
            i.origin_node = self
            i.or_origin_node = self
            i.showIMG = True
            i.start_node = self.grid.start_node
            i.end_node = self.grid.end_node
            if i.node_type != 2 and i.node_type != 1:
                if not i.clicked:
                    i.color = '#ff8000'
                i.showText = True
                i.calculateValues()
                    

    def calculateValues(self):
        if self.F == 0:
            g_x = abs(self.pos[0] - self.origin_node.pos[0])
            g_y = abs(self.pos[1] - self.origin_node.pos[1])
            h_x = abs(self.pos[0] - self.end_node.pos[0])
            h_y = abs(self.pos[1] - self.end_node.pos[1])
            self.G = round(m.sqrt(g_x**2 + g_y**2) / 6) + self.origin_node.G
            self.H = round(m.sqrt(h_x**2 + h_y**2) / 6) 
            self.F = self.G + self.H
        else:
            g_x = abs(self.pos[0] - self.origin_node.pos[0])
            g_y = abs(self.pos[1] - self.origin_node.pos[1])
            h_x = abs(self.pos[0] - self.end_node.pos[0])
            h_y = abs(self.pos[1] - self.end_node.pos[1])
            G = round(m.sqrt(g_x**2 + g_y**2) / 6) + self.origin_node.G
            H = round(m.sqrt(h_x**2 + h_y**2) / 6) 
            F = self.G + self.H
            if F > self.F:
                self.origin_node = self.or_origin_node
        
        

    def getSurroundingNodes(self):
        x = [[self.pos[0] - node_add, self.pos[1] - node_add],
             [self.pos[0], self.pos[1] - node_add],
             [self.pos[0] + node_add, self.pos[1] - node_add],
             [self.pos[0] + node_add, self.pos[1]],
             [self.pos[0] + node_add, self.pos[1] + node_add],
             [self.pos[0], self.pos[1] + node_add],
             [self.pos[0] - node_add, self.pos[1] + node_add],
             [self.pos[0] - node_add, self.pos[1]]]
        
        for i in self.nodes:
            for o in x:
                if o == i.pos:
                    self.surrounding_nodes.append(i)

    def drawArrow(self):
        if self.showIMG and self.origin_node != None:
            #CALCULATE THE ANGLE
            mp = self.origin_node.cpos
            dx = mp[0] - self.cpos[0]
            dy = mp[1] - self.cpos[1]
            self.img_angle = m.degrees(m.atan2(-dy, dx))
            self.arrow_img = pg.transform.rotate(self.or_arrow_img, self.img_angle)
            self.arrow_img_rect = self.arrow_img.get_rect()
            self.arrow_img_rect.center = self.cpos
            self.window.blit(self.arrow_img, self.arrow_img_rect)

    def checkFinished(self):

        if self.node_type == 3 and self.clicked:
            self.grid.gen_path = False