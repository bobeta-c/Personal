import pygame
import sys
def main():

    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    image = logo

    pygame.display.set_icon(logo)
    pygame.display.set_caption('test')

    screen = pygame.display.set_mode((500, 580))
    screen.fill((0,120,255))
    screen.blit(image, (240-32,180-32))
    print(screen.get_size())
    pygame.draw.rect(screen,(0,0,0), pygame.Rect((0,0),(10,90)))
    pygame.draw.rect(screen,(0,0,0), pygame.Rect((50,50),(100,100)))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()


def avg(*args):
    for x in args:
        print(x)

if __name__ == "__main__":

    main()
