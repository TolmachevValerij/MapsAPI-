import pygame, requests, sys, os



class MapParams(object):
    def __init__(self):
        self.lat = 65.583376
        self.lon = 57.136572
        self.z = 4
        self.t = "sat"


    def ll(self):
        return '%s%s'%(str(self.lon), '%2C')+"-"+str(self.lat)

def load_map(mp):
    mrequest = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.z, type=mp.t)
    response = requests.get(mrequest)
    if not response:
        print("Ошибка выполнения запроса:")
        print(mrequest)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:  # Выход из программы
           break
        map_file = load_map(mp)
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)

if __name__ == "__main__":
    main()
