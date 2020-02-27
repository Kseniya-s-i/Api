import os
import sys

import pygame
import requests

response = None
coords = ["37.530887", "55.703118"]  # долгота(-180, 180), широта(-90, 90)
spns = ["0.002", "0.002"]

pygame.init()
screen = pygame.display.set_mode((600, 450))

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if -180 < float(coords[0]) + float(spns[0]) < 180:
                coords[0] = str(float(coords[0]) + float(spns[0]))
            # print('r')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if -180 < float(coords[0]) - float(spns[0]) < 180:
                coords[0] = str(float(coords[0]) - float(spns[0]))
            # print('l')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if -90 < float(coords[1]) + float(spns[0]) / 2 < 90:
                coords[1] = str(float(coords[1]) + float(spns[0]) / 2)
            # print('u')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if -90 < float(coords[1]) - float(spns[0]) / 2 < 90:
                coords[1] = str(float(coords[1]) - float(spns[0]) / 2)
            # print('d')
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            if 0 < float(spns[0]) + float(spns[0]) * 0.5 < 181:
                spns[0] = spns[1] = str(float(spns[0]) + float(spns[0]) * 0.5)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            if 0 < float(spns[0]) - float(spns[0]) * 0.5 < 181:
                spns[0] = spns[1] = str(float(spns[0]) - float(spns[0]) * 0.5)

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}&spn={spns[0]},{spns[1]}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.fill(pygame.Color('white'))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)

