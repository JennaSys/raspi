import os
import sys
import pygame

def reset_screen(res) :
    screen = pygame.display.set_mode(res)
    pygame.display.set_caption("pyview")
    return screen

imgfile = ""
if len(sys.argv) < 2 :
    print "USAGE: %s [FILENAME]" % sys.argv[0]
    sys.exit()
imgfile = sys.argv[1]
if not os.path.exists(imgfile):
    print "USAGE: %s [FILENAME]" % sys.argv[0]
    sys.exit()

S = pygame.image.load(imgfile)
screen = reset_screen((S.get_width(), S.get_height()))
S = S.convert() # Need screen init

while True :
    for e in pygame.event.get() :
        if e.type == pygame.QUIT :
            sys.exit()
        if e.type == pygame.KEYDOWN :
            if e.key == pygame.K_ESCAPE :
                sys.exit()
            if e.key == pygame.K_MINUS :
                S = pygame.transform.scale(S, (S.get_width()/2, S.get_height()/2))
                screen = reset_screen((S.get_width(), S.get_height()))

            if e.key == pygame.K_EQUALS :
                S = pygame.transform.scale(S, (S.get_width()*2, S.get_height()*2))
                screen = reset_screen((S.get_width(), S.get_height()))
    screen.blit(S, (0,0))
    pygame.display.flip()
    pygame.time.delay(25)
