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

    mydict = {1:1,2:3,3:12,4:12,5:123,6:1,7:0}
    print(list(mydict.keys())[:4])
    #main()
