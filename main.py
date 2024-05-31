import pygame as pg
import sys
import random
from pygame.math import Vector2

pg.init()

#Had
class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False
        self.score = 0  # Přidání score

        #Směry hlavy hada
        self.head_up = pg.image.load('head-up.png').convert_alpha()
        self.head_down = pg.image.load('head-down.png').convert_alpha()
        self.head_right = pg.image.load('head-right.png').convert_alpha()
        self.head_left = pg.image.load('head-left.png').convert_alpha()

        #Směry ocasu hada
        self.tail_up = pg.image.load('tail_down.png').convert_alpha()
        self.tail_down = pg.image.load('tail_up.png').convert_alpha()
        self.tail_right = pg.image.load('tail_left.png').convert_alpha()
        self.tail_left = pg.image.load('tail_right.png').convert_alpha()

    #vykreslení hada
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        
        for index, block in enumerate(self.body):
            x_position = int(block.x * cell_size)
            y_position = int(block.y * cell_size)
            block_rect = pg.Rect(x_position, y_position, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)

            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)

            else:
                pg.draw.rect(screen, (183, 111, 122), block_rect)

    #Všechny verze hlavy hada
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): 
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0): 
            self.head = self.head_right
        elif head_relation == Vector2(0, 1): 
            self.head = self.head_up
        elif head_relation == Vector2(0, -1): 
            self.head = self.head_down

    #Všechny verze ocasu
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    #pohyb hada
    def body_move(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def add_block(self):
        #poslední blok hada
        last_block = self.body[-1]
        #přidání bloku na konec hada
        self.body.append(Vector2(last_block.x, last_block.y))

    def draw_score(self, screen):  # Přidání parametru screen
        score_text = "Score: " + str(self.score)  # Přidání textu "Score: " před hodnotu skóre
        score_surface = pg.font.Font('POETSENONE-REGULAR.TTF', 35).render(score_text, True, (0, 0, 0))  # Použití score_text místo str(self.score)
        screen_width, _ = screen.get_size()  # Získání rozměrů obrazovky
        score_rect = score_surface.get_rect(topright = (screen_width - 20, 20))  # Použití šířky obrazovky
        screen.blit(score_surface, score_rect)
        
    def eat_food(self, food):  # Předpokládám, že máte funkci pro snězení jídla
        if self.body[0] == food.position:
            self.score += 1  # Zvýšení skóre
            self.new_block = True
            food.randomize()

#Jídlo
class FOOD:
    def __init__(self):
        #pozice jídla
        self.x = random.randint(0, numbers_of_cells - 1) #random x pozice
        self.y = random.randint(0, numbers_of_cells - 1) #random y pozice
        self.position = Vector2(self.x, self.y)

    def draw_food(self):
        #obdélník s horním rohem na random buňce
        food_rect = pg.Rect(int(self.position.x * cell_size), int(self.position.y * cell_size), cell_size, cell_size)
        
        screen.blit(mouse, food_rect) #vykreslení myši

        #vykreslení obdélníku - kde, barva, co vykreslí
        # pg.draw.rect(screen, (126, 166, 114), food_rect)

    def randomize(self):
        self.x = random.randint(0, numbers_of_cells - 1) #random x pozice
        self.y = random.randint(0, numbers_of_cells - 1) #random y pozice
        self.position = Vector2(self.x, self.y) 

    

#hra samotná
class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()

    def update(self):
        self.snake.body_move() #pohyb hada
        self.check_collision() #kontrola, jestli had narazí na jídlo
        self.check_crash()  # Kontrola, jestli had narazil na stěnu nebo sám na sebe

    def draw_elements(self):
        self.food.draw_food()
        self.snake.draw_snake()

    def check_collision(self):
        #kontrola, jestli had narazí na jídlo
        if self.food.position == self.snake.body[0]:
            self.food.randomize()
            self.snake.add_block()
            self.snake.score += 1  # Zvýšení skóre

    def check_crash(self):
        #Náraz hada na stěnu - kontroluje se x a y souřadnice hada, jestli hlava hada narazí na stěnu
        if not 0 <= self.snake.body[0].x < numbers_of_cells or not 0 <= self.snake.body[0].y < numbers_of_cells:
            self.game_over()

        #Náraz hlavy do hada
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        #nastavení fontu a velikosti
        font = pg.font.Font('KNIGHTWARRIOR-W16N8.OTF', 75)
        #vytvoření textu
        text = font.render("GAME OVER", True, (0, 0, 0))
        #vytvoření obdélníku kolem textu
        text_rect = text.get_rect()
        #vycentrování textu
        text_rect.center = (numbers_of_cells * cell_size // 2, numbers_of_cells * cell_size // 2)
        #vykreslení textu na obrazovku
        screen.blit(text, text_rect)
        #aktualizace obrazovky
        pg.display.flip()
        #čekání 3 sekundy před ukončením hry
        pg.time.wait(3000)
        pg.quit()
        sys.exit()

        


#Velikost buňky (px)
cell_size = 40

#Počet buněk
numbers_of_cells = 20

#Velikost okna
screen = pg.display.set_mode((cell_size * numbers_of_cells, cell_size * numbers_of_cells))

#Název hry
pg.display.set_caption("Snake")

#fps
time = pg.time.Clock()

#jídlo - myš
mouse = pg.image.load('mouse1.png').convert_alpha()



food = FOOD() #vytvoření jídla
snake = SNAKE() #vytvoření hada
main_game = GAME() #vytvoření hry

#Aktualizace hry
SCREEN_UPDATE = pg.USEREVENT 
pg.time.set_timer(SCREEN_UPDATE, 150) #časový interval

main_game = GAME()

while True:
    #Zavírání okna
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()

        #ovládání hada pomocí šipek - změna směru hada změnou vektoru (souřadnice x a y)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                #změna směru hada - pokud had jede dolů, nemůže jet nahoru - stejně tak u dalších podminek
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pg.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pg.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            if event.key == pg.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
    if snake.eat_food(food):  # Kontrola, zda had snědl jídlo
        snake.add_block()  # Přidání bloku k hadovi


    #barva pozadí
    screen.fill((156, 212, 230))

    main_game.draw_elements()

    main_game.snake.draw_score(screen)  # Vykreslení skóre
    
    #Neustále aktualizuje okno
    pg.display.update()

    #fps
    time.tick(60)
    snake.draw_score(screen)  # Vykreslení skóre