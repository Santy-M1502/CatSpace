import pygame
from settings import *
from random import *
import math
from assets_imports import *

pygame.init()
pygame.mixer.init()
pygame.display.set_caption("SpaceCat")
clock = pygame.time.Clock()

main_font = pygame.font.Font(assets["font"]["space_font"], 24)

background = pygame.image.load(assets["images"]["background"])
background_rect = background.get_rect()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bg_width = background.get_width()
tiles = math.ceil(WIDTH / bg_width) + 2

title = pygame.image.load(assets["images"]["title"])
title_rect = title.get_rect()
title = pygame.transform.scale(title, (600, 400))
title_rect.center = (350, 180)
title_rect.y += 50

pause = pygame.image.load(assets["images"]["pause"])
pause_rect = pause.get_rect()
pause = pygame.transform.scale(pause, (50,50))

exit_ = pygame.image.load(assets["images"]["exit"])
exit_ = pygame.transform.scale(exit_, (60,60))
exit_rect = exit_.get_rect()
exit_rect.center = (690, 45)

mute_on = pygame.image.load(assets["images"]["mute_on"])
mute_on = pygame.transform.scale(mute_on, (60,60))
mute_rect = mute_on.get_rect()

mute_off = pygame.image.load(assets["images"]["mute_off"])
mute_off = pygame.transform.scale(mute_off, (60,60))

background_music = pygame.mixer.music.load(assets["music"]["background_music"])
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

def menu():
    font = pygame.font.Font(None, 36)
    scroll = 0
    is_running = True
    i_name = "NickName"
    print_name = False
    name_ready = False
    mute_switch = mute_off
    mute_rect.center = (750,45)
    while is_running:

        for i in range(0, tiles):
            SCREEN.blit(background,(i * bg_width + scroll, 0))
        scroll -= 1
        if abs(scroll) > bg_width:
            scroll = 0
        SCREEN.blit(title, title_rect)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if print_name and name_ready == False:
                    if event.key == pygame.K_RETURN:
                        if i_name == "":
                            i_name = "Player_1"
                        name_ready = True
                    elif event.key == pygame.K_BACKSPACE:
                        i_name = i_name[:-1]
                    else:
                        i_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mute_rect.collidepoint((mouse_x, mouse_y)):
                    if pygame.mouse.get_pressed()[0]:
                        if mute_switch == mute_off:
                            mute_switch = mute_on
                            pygame.mixer_music.pause()
                        else:
                            mute_switch = mute_off
                            pygame.mixer_music.unpause()
                if button_name.collidepoint((mouse_x, mouse_y)):
                    if pygame.mouse.get_pressed()[0]:
                        print_name = True
                        i_name = ""
                if button_play.collidepoint((mouse_x, mouse_y)) and name_ready == True:
                    if pygame.mouse.get_pressed()[0]:
                        play(i_name)
                        is_running = False
                if button_records.collidepoint((mouse_x, mouse_y)):
                    if pygame.mouse.get_pressed()[0]:
                        records()
                        is_running = False
                if button_quit.collidepoint((mouse_x, mouse_y)):
                    if pygame.mouse.get_pressed()[0]:
                        is_running = False

        button_name = pygame.Rect((330 , HEIGHT // 2 - 30, 140, 50))
        button_play = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 30, 100, 50)
        button_records = pygame.Rect(330, HEIGHT // 2 + 90, 140, 50)
        button_quit = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 150, 100, 50)

        if name_ready == False:
            pygame.draw.rect(SCREEN, WHITE, button_name)
        else:
            pygame.draw.rect(SCREEN, WHITE, button_play)
            draw_text('PLAY', font, BLACK, SCREEN, WIDTH // 2, HEIGHT // 2 + 57)
        pygame.draw.rect(SCREEN, WHITE, button_records)
        pygame.draw.rect(SCREEN, WHITE, button_quit)

        
        if name_ready == False:
            text_surface = font.render(i_name, True, BLACK)
        SCREEN.blit(text_surface, (330 , HEIGHT // 2 - 20))
        draw_text('RECORDS', font, BLACK, SCREEN, WIDTH // 2, HEIGHT // 2 + 117)
        draw_text('SALIR', font, BLACK, SCREEN, WIDTH // 2, HEIGHT // 2 + 175)
        SCREEN.blit(mute_switch, mute_rect)

        pygame.display.flip()
    
    pygame.quit()


def options():
    pass

def game_over(nickname, segundos, milisegundos):
    from os import system
    lista = []
    lista.append({"name" : nickname, "second" : segundos, "milisecond" : milisegundos})
    with open(get_path_actual("records") + ".csv", "r", encoding="utf-8") as archivo:
        encabezado = archivo.readline().strip("\n").split(",")

        for linea in archivo.readlines():
            player = {}
            linea = linea.strip("\n").split(",")
            nick, second, milisecond = linea
            player["name"] = nick
            player["second"] = int(second)
            player["milisecond"] = int(milisecond)
            lista.append(player)

    ordenar_doble_ascendente(lista, "second", "milisecond")

    lista.pop()
    with open(get_path_actual("records") + ".csv", "w", encoding="utf-8") as archivo:
        encabezado = ",".join(list(lista[0].keys())) + "\n"
        archivo.write(encabezado)
        for i in range(len(lista)):
            l = ",".join(lista[i]) + "\n"
        
        for persona in lista:
            values = list(persona.values())
            l = []
            for value in values:
                if isinstance(value,int):
                    l.append(str(value))
                else:
                    l.append(value)
            linea = ",".join(l) + "\n"
            archivo.write(linea)


def play(nickname):
    scroll = 0
    is_running = True
    speed = 7
    mover_derecha = False
    mover_izquierda = False

    pos = [(0, 550),
        (-10, 100),
        (800, 100)]

    
    plataformas = [pygame.Rect(pos[0],(800, 50))]
    bordes = [pygame.Rect(pos[1],(15, 800)),pygame.Rect(pos[2],(15, 800))]
    bombuchas_i = [pygame.Rect(randint(-60,-30), randint(0, 600), 30,30)]
    bombuchas_d = [pygame.Rect(randint(830,860), randint(0, 600), 30,30)]

    saltar = False
    Y_GRAVITY = 0.5
    JUMP_HEIGHT = 20
    Y_VELOCITY = JUMP_HEIGHT
    contador_bombuchas = 0
    game_over_in = False
    segundos = 0
    milisegundos = 0
    font_name = pygame.font.Font(None, 36)
    font_game_over = pygame.font.Font(None, 70)
    font_try_again = pygame.font.Font(None, 45)
    text_game_over = font_game_over.render("GAME OVER ", True, (255,255,255))
    en_suelo = False
    cont_game_over = 0

    water_ball = pygame.mixer.Sound(assets["sounds"]["water_ball"])
    water_ball.set_volume(0.5)
    meow_lose = pygame.mixer.Sound(assets["sounds"]["cat_lose"])
    meow_lose.set_volume(0.2)
    meow_final = pygame.mixer.Sound(assets["sounds"]["cat_final"])
    meow_final.set_volume(0.2)
    cat_shaking = pygame.mixer.Sound(assets["sounds"]["cat_shaking"])
    cat_shaking.set_volume(0.2)
    cat_happy = pygame.mixer.Sound(assets["sounds"]["cat_happy"])
    cat_happy.set_volume(0.6)

    jump_flag = False
    jump_count = 0
    no_jump = False

    pausa = False
    lifes = 3
    SCREEN.fill(BLACK)

    cat = [pygame.image.load(assets["images"]["cat0"]),
           pygame.image.load(assets["images"]["cat1"]),
           pygame.image.load(assets["images"]["cat2"])]
    for i in range(len(cat)):
        cat[i] = escalar_img(cat[i], 3.1)
    cat_rect = cat[0].get_rect() 
    cat_rect.inflate_ip(-15, -37)
    cat_rect.center = (400, 500)

    cat_jumping = pygame.image.load(assets["images"]["cat_jumping"])
    cat_jumping = escalar_img(cat_jumping, 3.1)

    cat_lose = pygame.image.load(assets["images"]["cat_lose"])
    cat_lose = escalar_img(cat_lose, 3.1)
    

    bombshells = [pygame.image.load(assets["images"]["bombucha0"]),
           pygame.image.load(assets["images"]["bombucha1"]),
           pygame.image.load(assets["images"]["bombucha2"]),
           pygame.image.load(assets["images"]["bombucha3"])]
    for i in range(len(bombshells)):
        bombshells[i] = escalar_img(bombshells[i], 2)
    bombshells_rect = bombshells[0].get_rect() 
    bombshells_rect.inflate_ip(-15, -46)

    food_power = pygame.image.load(assets["images"]["food_power"])
    food_power = escalar_img(food_power, 3)

    floor = pygame.image.load(assets["images"]["floor"])

    indice_cat = 0
    indice_count_cat = 0

    indice_bombshells = 0
    indice_count_bombshells = 0


    flip_left = False
    flip_right = True

    sprite_lose = False
    cat_sprite = cat[0]

    shield_activate = False
    shield_count = 0
    shield = pygame.image.load(assets["images"]["shield"])
    shield = escalar_img(shield, 4.7)
    draw_shield = False

    mute_switch = mute_off
    mute_rect.center = (620,45)

    contador = 0
    while is_running:
        clock.tick(FPS)
        for i in range(0, tiles):
            SCREEN.blit(background,(i * bg_width + scroll, 0))
        scroll -= 0.3
        if abs(scroll) > bg_width:
            scroll = 0
        score_text = main_font.render(f"Tiempo: {segundos}:{milisegundos}", True, (255,255,255))
        if game_over_in == False:
            if not pausa:
                if mover_derecha:
                    cat_rect.x += speed
                    indice_count_cat += 1
                    if indice_count_cat == 10:
                            indice_cat += 1
                            indice_count_cat = 0

                if mover_izquierda:
                    cat_rect.x -= speed
                    indice_count_cat += 1
                    if indice_count_cat == 10:
                            indice_cat += 1
                            indice_count_cat = 0
                
                if indice_cat == 2:
                    indice_cat = 0
                
                indice_count_bombshells += 1
                if indice_count_bombshells == 10:
                    indice_bombshells += 1
                    indice_count_bombshells = 0
                    if indice_bombshells == 4:
                        indice_bombshells = 0
                    
                
                
                if detectar_colision(cat_rect, bordes[0]):
                    cat_rect.x = 0
                if detectar_colision(cat_rect, bordes[1]):
                    cat_rect.x = WIDTH - cat_rect.width

                for plataforma in plataformas:
                    if  detectar_colision(cat_rect, plataforma):
                        no_jump = False
                        jump_count = -1
                        Y_VELOCITY = JUMP_HEIGHT
                        en_suelo = True
                    else:
                        cat_rect.y += 4

                if saltar and en_suelo:
                    jump_flag = True
                    cat_rect.y -= Y_VELOCITY
                    Y_VELOCITY -= Y_GRAVITY
                    if no_jump:
                        saltar = False
                        Y_VELOCITY = JUMP_HEIGHT 
                    
                if jump_flag:
                    if jump_count == 0:
                        jump_count += 1
                    
                shield_count += 1
                if shield_count == 1200:
                    shield_power = pygame.Rect(randint(0, WIDTH), randint(HEIGHT // 2, HEIGHT - 70), 25, 25)
                if shield_count >= 1200:
                    SCREEN.blit(food_power, shield_power)
                    if detectar_colision(cat_rect, shield_power):
                        shield_count = 0
                        shield_activate = True
                        cat_happy.play()
            
                if not shield_activate:
                    for i in range(len(bombuchas_i)):
                        if detectar_colision(cat_rect, bombuchas_d[i]):
                            sprite_lose = True
                            lifes -= 1
                            shield_count = -1
                            shield_activate = True
                            bombuchas_d.remove(bombuchas_d[i])
                            agregar_entidad(bombuchas_d, pygame.Rect(randint(830,860), randint(0, 600), 30,30))
                            water_ball.play()
                            if lifes != 0:
                                meow_lose.play()
                        elif detectar_colision(cat_rect, bombuchas_i[i]):
                            sprite_lose = True
                            lifes -= 1
                            shield_count = -1
                            shield_activate = True
                            bombuchas_i.remove(bombuchas_i[i])
                            agregar_entidad(bombuchas_i, pygame.Rect(randint(-60,-30), randint(0, 600), 30,30))
                            water_ball.play()
                            if lifes != 0:
                                meow_lose.play()
                else:
                    draw_shield = True
                    if shield_count == 0:
                        shield_text = 3
                    elif shield_count == 60:
                        shield_text = 2
                        if sprite_lose:
                            cat_shaking.play()
                    elif shield_count == 120:
                        shield_text = 1
                    elif shield_count == 180:
                        sprite_lose = False
                        shield_activate = False
                        draw_shield = False
                    draw_text(f"Shield: {shield_text} segundos", main_font, WHITE, SCREEN, 220, 120)
                
                if saltar and en_suelo:
                    cat_sprite = cat_jumping
                    if flip_left:
                        cat_sprite = pygame.transform.flip(cat_sprite, True, False)
                elif sprite_lose:
                    cat_sprite = cat_lose
                    if flip_left:
                        cat_sprite = pygame.transform.flip(cat_sprite, True, False)
                else:
                    cat_sprite = cat[indice_cat]
                    if flip_left:
                        cat_sprite = pygame.transform.flip(cat_sprite, True, False)
                for i in range(len(bombuchas_i)):
                    if bombuchas_i[i].left <= WIDTH:
                        bombuchas_i[i].x += 4
                        bombuchas_i[i].y += 0.5
                    else:
                        bombuchas_i[i].center = (-30, randint(200, 400))
            
                for i in range(len(bombuchas_d)):
                    if bombuchas_d[i].right >= 0:
                        bombuchas_d[i].x -= 4
                        bombuchas_d[i].y += 0.5
                    else:
                        bombuchas_d[i].center = (830, randint(200, 400))

                contador_bombuchas += 1

                if contador_bombuchas >= 500:
                    bombuchas_i.append(pygame.Rect(randint(-60,-30), randint(0, 600), 30,30))
                    bombuchas_d.append(pygame.Rect(randint(830,860), randint(0, 600), 30,30))
                    contador_bombuchas = 0
                    
                if cat_rect.top >= 600:
                    lifes -= 1
                    shield_count = -1
                    shield_activate = True

                milisegundos += 1
                if milisegundos == 60:
                    segundos += 1
                    milisegundos = 0
                
                if lifes == 0:
                    meow_final.play()
                    game_over_in = True
                
            else:
                SCREEN.blit(exit_, exit_rect)
                draw_text("PAUSA", main_font, WHITE, SCREEN, WIDTH //2, HEIGHT // 2)
                SCREEN.blit(mute_switch, mute_rect)
            draw_text(F"VIDAS: {lifes}", main_font, WHITE, SCREEN, 110, 80)

            SCREEN.blit(floor, plataformas[0])
            SCREEN.blit(cat_sprite, cat_rect)
            SCREEN.blit(pause, (730, 20, 400, 400))
            button_pause = pygame.Rect(730, 20, 400, 400)
                
            if draw_shield:
                SCREEN.blit(shield, cat_rect)
        
        else:
            cont_game_over += 1
            if cont_game_over == 1:
                game_over(nickname, segundos, milisegundos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button_retry.collidepoint((mouse_x, mouse_y)):
                        if pygame.mouse.get_pressed()[0]:
                            bombuchas_i = [pygame.Rect(randint(-60,-30), randint(0, 600), 30,30)]
                            bombuchas_d = [pygame.Rect(randint(830,860), randint(0, 600), 30,30)]
                            cat_rect.center = (400, 500)
                            contador_bombuchas = 0
                            game_over_in = False
                            segundos = 0
                            milisegundos = 0
                            saltar = False
                            mover_izquierda = False
                            mover_derecha = False
                            shield_count = 0
                            lifes = 3
                            cont_game_over = 0
                            sprite_lose = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    flip_left = True
                    flip_right = False
                    mover_izquierda = True
                if event.key == pygame.K_d:
                    flip_right = True
                    flip_left =False
                    mover_derecha = True
                if event.key == pygame.K_w:
                    saltar = True
                    jump_count = 0
                    en_suelo = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izquierda = False
                    indice_count_cat = 0
                if event.key == pygame.K_d:
                    mover_derecha = False
                    indice_count_cat = 0
                if event.key == pygame.K_w:
                    saltar = False
                    no_jump = True
                if event.key == pygame.K_ESCAPE:
                    if pausa == False:
                            pausa = True
                    else:
                        pausa = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pause.collidepoint((mouse_x, mouse_y)):
                    if pygame.mouse.get_pressed()[0]:
                        if pausa == False:
                            pausa = True
                        else:
                            pausa = False
                if pausa:
                    if exit_rect.collidepoint(mouse_x, mouse_y):
                        if pygame.mouse.get_pressed()[0]:
                            is_running = False
                            menu()
                    if mute_rect.collidepoint(mouse_x, mouse_y):
                        if pygame.mouse.get_pressed()[0]:
                            if mute_switch == mute_off:
                                mute_switch = mute_on
                                pygame.mixer_music.pause()
                            else:
                                mute_switch = mute_off
                                pygame.mixer_music.unpause()

        if game_over_in == False:
            for i in range(len(bombuchas_i)):
                SCREEN.blit(bombshells[indice_bombshells], bombuchas_i[i])
            for i in range(len(bombuchas_d)):
                SCREEN.blit(bombshells[indice_bombshells], bombuchas_d[i])
            SCREEN.blit(score_text, (40,25))
        else:
            text_score = font_game_over.render(f"Sobreviviste: {segundos}:{milisegundos} segundos!", True, (255,255,255))
            SCREEN.blit(text_score, (70, 100))
            SCREEN.blit(text_game_over, (248, 250))
            button_retry = pygame.Rect((340 , 390, 120, 50))
            button_retry.center = (WIDTH // 2, 450)
            pygame.draw.rect(SCREEN, WHITE, button_retry)
            draw_text("Retry", font_try_again, BLACK, SCREEN, 400 , 450)
            
        pygame.display.flip()

def records():
    is_running = True
    scroll = 0
    background_menu = pygame.image.load(assets["images"]["background_menu"])
    fuente = pygame.font.Font(None, 30)
    while is_running:
        SCREEN.fill(BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_rect.collidepoint(mouse_x, mouse_y):
                    if pygame.mouse.get_pressed()[0]:
                        menu()
        
        for i in range(0, tiles):
            SCREEN.blit(background,(i * bg_width + scroll, 0))
        scroll -= 1
        if abs(scroll) > bg_width:
            scroll = 0
        
        SCREEN.blit(background_menu, (0, 0))
        SCREEN.blit(exit_, exit_rect)
        lista = []
        with open(get_path_actual("records") + ".csv", "r", encoding="utf-8") as archivo:
            encabezado = archivo.readline().strip("\n").split(",")

            for linea in archivo.readlines():
                player = {}
                linea = linea.strip("\n").split(",")
                nick, second, milisecond = linea
                player["name"] = nick
                player["second"] = int(second)
                player["milisecond"] = int(milisecond)
                lista.append(player)
            

            draw_text(f"ID             TIEMPO", fuente, WHITE, SCREEN, WIDTH - WIDTH // 2, HEIGHT - HEIGHT // 2 - 170)
            draw_text(f"               1.{lista[0]["name"]}         {lista[0]["second"]:2} : {lista[0]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 - 130)
            draw_text(f"               2.{lista[1]["name"]}         {lista[1]["second"]:2} : {lista[1]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 - 100)
            draw_text(f"               3.{lista[2]["name"]}         {lista[2]["second"]:2} : {lista[2]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 - 70)
            draw_text(f"               4.{lista[3]["name"]}         {lista[3]["second"]:2} : {lista[3]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 - 40)
            draw_text(f"               5.{lista[4]["name"]}         {lista[4]["second"]:2} : {lista[4]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 - 10)
            draw_text(f"               6.{lista[5]["name"]}         {lista[5]["second"]:2} : {lista[5]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 + 20)
            draw_text(f"               7.{lista[6]["name"]}         {lista[6]["second"]:2} : {lista[6]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 + 50)
            draw_text(f"               8.{lista[7]["name"]}         {lista[7]["second"]:2} : {lista[7]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 + 80)
            draw_text(f"               9.{lista[8]["name"]}         {lista[8]["second"]:2} : {lista[8]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 + 110)
            draw_text(f"              10.{lista[9]["name"]}        {lista[9]["second"]:2} : {lista[9]["milisecond"]}", fuente, WHITE, SCREEN, WIDTH - WIDTH // 1.7, HEIGHT - HEIGHT // 2 + 140)
        
        pygame.display.flip()


menu()
pygame.quit()