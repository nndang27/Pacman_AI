import sys, pygame
from pygame.locals import*

width=1000
height=500
Color_screen=(49,150,100)
Color_line=(255,0,0)

def main():
    screen=pygame.display.set_mode((width,height))
    screen.fill(Color_screen)
    
    pygame.draw.line(screen,Color_line,(60,80),(60,400))
    pygame.display.flip()
    while True:
        for events in pygame.event.get():
            if events.type == QUIT:

                sys.exit(0)
main()
