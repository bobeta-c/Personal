import pygame
import sys
def main():

    pygame.init()
    logo = pygame.image.load("logo32x32.png")
    image = logo

    pygame.display.set_icon(logo)
    pygame.display.set_caption('test')

    screen = pygame.display.set_mode((240, 180))
    screen.fill((0,120,255))
    screen.blit(image, (240-32,180-32))
    print(screen.get_size())
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()


if __name__ == "__main__":

    main()
