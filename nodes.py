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
        

        #FONT
        self.font1 = pg.font.Font(None, 35)
        self.font2 = pg.font.Font(None, 20)
        self.showText = False
        self.clicked = False

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

    def update(self):
        self.draw()
        self.checkMouseHover()
        self.checkEvents()

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
                self.start_node = self.grid.start_node
                self.end_node = self.grid.end_node

                if self.node_type != 2 and self.node_type != 3 and self.node_type != 1:
                    self.color = '#9cff59'
                    print(f'Node Type: [{self.node_type}]')
                    self.showText = True
                    self.calculateValues()
                    self.clicked = True
                self.getSurroundingNodes()
                for i in self.surrounding_nodes:
                    i.start_node = self.grid.start_node
                    i.end_node = self.grid.end_node
                    if i.node_type != 2 and i.node_type != 3 and i.node_type != 1:
                        if not i.clicked:
                            i.color = 'red'
                        i.showText = True
                        i.calculateValues()
                    
                    

    def calculateValues(self):
        g_x = abs(self.pos[0] - self.start_node.pos[0])
        g_y = abs(self.pos[1] - self.start_node.pos[1])
        h_x = abs(self.pos[0] - self.end_node.pos[0])
        h_y = abs(self.pos[1] - self.end_node.pos[1])
        self.G = round(m.sqrt(g_x**2 + g_y**2) / 6)
        self.H = round(m.sqrt(h_x**2 + h_y**2) / 6) 
        self.F = self.G + self.H

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
