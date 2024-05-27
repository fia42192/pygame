import pygame as pg
import sys
import random
from pygame.math import Vector2

pg.init()

#Had
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(6, 10), Vector2(7, 10)]

    def draw_snake(self):
        for body1 in self.body:
            x_position = int(body1.x * cell_size)
            y_position = int(body1.y * cell_size)
            body1_rect = pg.Rect(x_position, y_position, cell_size, cell_size)
            pg.draw.rect(screen, (183, 111, 122), body1_rect)

#Jídlo
class FOOD:
    def __init__(self):
        #pozice jídla
        self.x = random.randint(0, numbers_of_cells - 1)
        self.y = random.randint(0, numbers_of_cells - 1)
        self.position = Vector2(self.x, self.y)

    def draw_food(self):
        #obdélník s horním rohem na random buňce
        food_rect = pg.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        
        #vykreslení obdélníku - kde, barva, co vykreslí
        pg.draw.rect(screen, (126, 166, 114), food_rect)

#Velikost buňky (px)
cell_size = 40

#Počet buněk
numbers_of_cells = 20

#Velikost okna
screen = pg.display.set_mode((cell_size * numbers_of_cells, cell_size * numbers_of_cells))

#Název hry
pg.display.set_caption("Snake")

time = pg.time.Clock()

food = FOOD()
snake = SNAKE()

while True:
    #Zavírání okna
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    #barva pozadí
    screen.fill((156, 212, 230))

    #vykreslení hada a jídla
    food.draw_food()
    snake.draw_snake()
    
    #Neustále aktualizuje okno
    pg.display.update()

    #fps
    time.tick(60)
    