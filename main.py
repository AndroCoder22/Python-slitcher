import pygame as pg 
import math
from random import randrange as rr 

WIDTH, HEIGHT = 1150, 650

pg.init()
sc = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

#joystick
istouch = False
mouse2 = (-1000, -1000)
angler = 0

#World
scroll_x, scroll_y = 0, 0
eat = []
eat_p = 2000
eat_colors = []
generate = False
world_size = 10

#player
head = [100, 100]
tail_x = []
tail_y = []

snake_lenght = 2
snake_height = 20

snake_speed = 2

#SKINS
RUS_SKIN = {
    'colors': [[255,255,255], [0,0,255], [255,0,0], [123,123,213], [0,0,123]],
    'lenght': 50
}

current_skin = RUS_SKIN
skin = []

while 1:
    clock.tick(60)
    sc.fill((20, 20, 20))
    pg.display.set_caption(str(int(clock.get_fps())))
    mouse = pg.mouse.get_pos()

    if not generate:
        for i in range(eat_p):
            eat.append([rr(0, WIDTH * world_size), rr(0, HEIGHT * world_size)])
            eat_colors.append([rr(100, 255), rr(100, 255), rr(100, 255)])
        for l in range(len(current_skin['colors'])):
            for t in range(int(current_skin['lenght']/len(current_skin['colors']))):
                skin.append(current_skin['colors'][l])

        generate = True


    if generate:
        player_rect = pg.Rect((head[0]-snake_height-scroll_x, head[1]-snake_height-scroll_y), (snake_height*2, snake_height*2))
        for i in range(eat_p):
            eat_rect = pg.draw.circle(sc, eat_colors[i], (eat[i][0]-scroll_x, eat[i][1]-scroll_y), 20)
            if player_rect.colliderect(eat_rect):
                snake_lenght += 1
                snake_height += 0.1
                eat[i] = [rr(0, WIDTH*4), rr(0, HEIGHT*4)]

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                exit()

            if ev.type == pg.MOUSEBUTTONDOWN:
                istouch = True
                mouse2 = mouse 

            elif ev.type == pg.MOUSEBUTTONUP:
                istouch = False	

        if istouch:

            pg.draw.circle(sc, (100,100,100), mouse2, 100)
            cur_mouse = mouse[0] - mouse2[0], mouse[1] - mouse2[1]
            angler = math.atan2(cur_mouse[0], cur_mouse[1])
            distance  = math.sqrt(pow(cur_mouse[0], 2) + pow(cur_mouse[1], 2))
            current_angle = angler
            joy_pos = mouse2
            if distance > 80:
                si = math.sin(angler)
                co = math.cos(angler)
                joy_pos = (math.degrees(si)*1.4+mouse2[0], math.degrees(co)*1.4+mouse2[1])
                distance = 80
            else:
                joy_pos = mouse
        
            pg.draw.circle(sc, (234,234,234), joy_pos, 50)
        
        tail_x.insert(0, head[0])
        tail_y.insert(0, head[1])
        
        head[0] += math.sin(angler)*snake_speed
        head[1] += math.cos(angler)*snake_speed

        pg.draw.circle(sc, current_skin['colors'][0], (head[0]-scroll_x, head[1]-scroll_y), int(snake_height))
        for sn in range(int(snake_lenght)):
            try:
                pg.draw.circle(sc, skin[int(sn % current_skin['lenght'])], (tail_x[sn]-scroll_x, tail_y[sn]-scroll_y), int(snake_height))
            except:
                pg.draw.circle(sc, skin[int(sn % current_skin['lenght'])], (head[0]-scroll_x, head[1]-scroll_y), int(snake_height))
         
        if head[0] - scroll_x != WIDTH/2:
            scroll_x += (head[0] - (scroll_x + WIDTH/2)) / 100
        if head[1] - scroll_y != HEIGHT/2:
            scroll_y += (head[1] - (scroll_y + HEIGHT/2)) / 100

        pg.display.update()
