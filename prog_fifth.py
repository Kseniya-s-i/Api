from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import os
import sys
import pygame
import requests

information = ''


def isindex(resp):
    try:
        x = resp["metaDataProperty"] \
                        ["GeocoderMetaData"]["AddressDetails"]['Country']['AdministrativeArea']['Locality']['Thoroughfare'][
                        'Premise'][
                        'PostalCode']['PostalCodeNumber']
        return 1
    except BaseException:
        return 0


def ocrug(geocoder, ind=False):
    response = requests.get(geocoder)
    try:
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_address = toponym['Point']['pos'].split(' ')
            toponym_meta = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
            if ind:
                if isindex(toponym):
                    toponym_index = toponym["metaDataProperty"] \
                        ["GeocoderMetaData"]["AddressDetails"]['Country']['AdministrativeArea']['Locality']['Thoroughfare'][
                        'Premise'][
                        'PostalCode']['PostalCodeNumber']
                    return toponym_address, toponym_meta, toponym_index
                return toponym_address, toponym_meta, ''
            return toponym_address, toponym_meta
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            return 0
    except BaseException:
        return 0


last_coords = ["37.530887", "55.703118"]
last_index = False


class Form(QMainWindow):
    global information, last_coords

    def __init__(self):
        super().__init__()
        uic.loadUi('search.ui', self)
        self.initUI()

    def initUI(self):
        self.index = False
        self.setWindowTitle('Система')
        self.getsrch.clicked.connect(self.trysearch)
        self.deleting.clicked.connect(self.removee)
        self.show()

    def yes_ind(self):
        self.index = True

    def trysearch(self):
        global last_coords, information
        if self.index_btn.isChecked():
            self.yes_ind()
        else:
            self.index = False
        information = self.inquiry.text()
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/" \
                           f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={information}&format=json"
        geo = ocrug(geocoder_request, ind=self.index)
        if geo:
            crds = geo[0]
            if self.index:
                info = geo[1] + geo[2]
                # print(info)
            else:
                info = geo[1]
            if crds != 0:
                last_coords = crds
                self.info.setText(info)
                cards(crds, f'&pt={crds[0]},{crds[1]},pm2dgm')
            else:
                cards(last_coords, f'&pt={last_coords[0]},{last_coords[1]},pm2dgm')
        else:
            cards(last_coords, f'&pt={last_coords[0]},{last_coords[1]},pm2dgm')

    def removee(self):
        self.inquiry.setText('')
        self.info.setText('')
        cards(last_coords, '')

response = None
coords = ["37.530887", "55.703118"]  # долгота(-180, 180), широта(-90, 90)


def cards(coords, pts):
    spns = ["0.003", "0.003"]
    mode = ['map', 'sat', 'sat,skl']
    now_mode = mode[0]

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    clock = pygame.time.Clock()
    pygame.display.flip()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if -180 < float(coords[0]) + float(spns[0]) < 180:
                    coords[0] = str(float(coords[0]) + float(spns[0]) / 4)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if -180 < float(coords[0]) - float(spns[0]) < 180:
                    coords[0] = str(float(coords[0]) - float(spns[0]) / 4)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if -90 < float(coords[1]) + float(spns[0]) / 4 < 90:
                    coords[1] = str(float(coords[1]) + float(spns[0]) / 4)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if -90 < float(coords[1]) - float(spns[0]) / 4 < 90:
                    coords[1] = str(float(coords[1]) - float(spns[0]) / 4)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEUP:
                if 0.0005 < float(spns[0]) + float(spns[0]) * 0.5 < 181:
                    spns[0] = spns[1] = str(float(spns[0]) + float(spns[0]) * 0.5)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_PAGEDOWN:
                if 0.0005 < float(spns[0]) - float(spns[0]) * 0.5 < 181:
                    spns[0] = spns[1] = str(float(spns[0]) - float(spns[0]) * 0.5)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                now_mode = mode[1]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                now_mode = mode[0]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                now_mode = mode[2]
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                if __name__ == '__main__':
                    app = QApplication(sys.argv)
                    ex = Form()

        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if -90 < float(coords[1]) - float(spns[0]) / 4 < 90:
                coords[1] = str(float(coords[1]) - float(spns[0]) / 4)
        if pygame.key.get_pressed()[pygame.K_UP]:
            if -90 < float(coords[1]) + float(spns[0]) / 4 < 90:
                coords[1] = str(float(coords[1]) + float(spns[0]) / 4)
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            if -180 < float(coords[0]) - float(spns[0]) < 180:
                coords[0] = str(float(coords[0]) - float(spns[0]) / 4)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            if -180 < float(coords[0]) + float(spns[0]) < 180:
                coords[0] = str(float(coords[0]) + float(spns[0]) / 4)
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords[0]},{coords[1]}" \
                      f"&spn={spns[0]},{spns[1]}&l={now_mode}" + f'{pts}'
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
        clock.tick(90)
        pygame.display.flip()
    os.remove(map_file)
    pygame.quit()
    sys.exit(0)


cards(coords, '')
