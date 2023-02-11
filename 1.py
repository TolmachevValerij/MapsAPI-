import pygame
import requests
import sys 
import os



def load_map():
    map_request = "https://static-maps.yandex.ru/1.x/?l=map&pt=65.534121,57.149484~65.540921,57.153502~65.537696,57.151173"
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
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
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
           break
        map_file = load_map()
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
    pygame.quit(
    os.remove(map_file)

if __name__ == "__main__":
    main()
