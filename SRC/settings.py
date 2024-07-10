import pygame
from random import randint, randrange
from os import system
WIDTH = 800
HEIGHT = 600
SCREEN_SIZE = (WIDTH, HEIGHT)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
CENTER_SCREEN = (WIDTH//2, HEIGHT//2)

FPS = 60

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
VIOLET = (74, 40, 130)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

COLOR_BG = (0,0,20)

def detectar_colision(rect_1, rect_2):
    """_summary_

    Args:
        rect_1 (_type_): rect1 a detectar colision con rect2
        rect_2 (_type_): rect2 a detectar colision con rect1

    Returns:
        _type_: retorna false si ningun punto esta dentro del otro rect
    """
    if punto_en_rectangulo(rect_1.topleft, rect_2) or \
        punto_en_rectangulo(rect_1.topright, rect_2) or \
        punto_en_rectangulo(rect_1.bottomleft, rect_2) or\
        punto_en_rectangulo(rect_1.bottomright, rect_2) or\
        punto_en_rectangulo(rect_2.topleft, rect_1) or \
        punto_en_rectangulo(rect_2.topright, rect_1) or \
        punto_en_rectangulo(rect_2.bottomleft, rect_1) or\
        punto_en_rectangulo(rect_2.bottomright, rect_1):
        return True
    else:
        return False

def punto_en_rectangulo(punto, rect):
    """_summary_

    Args:
        punto (_type_): punto a verificar dentro de rect
        rect (_type_): rect que verifique el punto

    Returns:
        _type_: retorna true si punto esta dentro del rect
    """
    x, y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom

def draw_text(text, font, color, surface,x, y):
    """_summary_

    Args:
        text (_type_): texto a escribir
        font (_type_): fuente de las letras
        color (_type_): color en el que se escribe
        surface (_type_): superficie sobre donde se escribe
        x (_type_): coordenada X donde se ubica
        y (_type_): coordenada Y donde se ubica
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def get_path_actual(nombre_archivo):
    """_summary_

    Args:
        nombre_archivo (_type_): Nombre del archivo actual

    Returns:
        _type_: la ubicacion del archivo en el que se trabaja
    """
    import os
    ubi = os.path.dirname(__file__)
    
    return os.path.join(ubi, nombre_archivo)

def swap_lista(lista:list, valor1, valor2):
    """_summary_

    Args:
        lista (list): lista a swapear
        valor1 (_type_): primer valor a swapear
        valor2 (_type_): segundo valor a swapear
    """
    aux = lista[valor1]
    lista[valor1] = lista[valor2]
    lista[valor2] = aux

def agregar_entidad(lista, rect):   
    lista.append(rect)

def escalar_img(image, scale:float):
    """_summary_

    Args:
        image (_type_): imagen a escalar
        scale (float): escala a escalar imagen

    Returns:
        _type_: la imagen nueva escalada
    """
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen    

def ordenar_doble_ascendente(lista:list, campo_uno:str, campo_dos:str):
    """_summary_

    Args:
        lista (list): Lista a ordenar
        campo_uno (str): primer campo a ordenar
        campo_dos (str): segundo campo a ordenar
    """
    for i in range(len(lista)- 1):
        for j in range(i + 1, len(lista)):
            if lista[i][campo_uno] < lista[j][campo_uno]:
                swap_lista(lista, i, j)
            elif lista[i][campo_uno] == lista[j][campo_uno]:
                if lista[i][campo_dos] < lista[j][campo_dos]:
                    swap_lista(lista, i, j)