import pygame as pg
import sys

pg.init()

#Velikost okna
screen = pg.display.set_mode((800, 600))

time = pg.time.Clock()

#vytvoření plochy
surface = pg.Surface((200, 300))

#barva plochy
surface.fill((100, 0, 0))

while True:
    #Zavírání okna
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    
    #barva pozadí
    screen.fill((156, 212, 230))


    
    #Neustále aktualizuje okno
    pg.display.update()

    #fps
    time.tick(60)