import pygame as pg
from settings import *
from nodes import *

class Game:
    def __init__(self) -> None:
        pg.init()
        self.running = True
        self.window = pg.display.set_mode((WIDTH, HEIGHT), flags=pg.RESIZABLE)
        self.clock = pg.time.Clock()
        self.nodes = Nodes(self)
        self.events = pg.event.get()

    def checkEvents(self):
        self.events = pg.event.get()
        for event in self.events:
            if event.type == pg.QUIT:
                self.running = False

    def draw(self):
        self.nodes.draw()

    def update(self):
        self.window.fill('black')
        self.draw()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"FPS: [{round(self.clock.get_fps())}]           MOUSE: [{pg.mouse.get_pos()}]")
        self.nodes.update()
        pg.display.update()


    def run(self):
        while self.running:
            self.update()
            self.checkEvents()

if __name__ == '__main__':
    game = Game()
    game.run()
    pg.quit()