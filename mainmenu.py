import pygame, sys

import os

from button import Button

from app_class import *



pygame.init()



SCREEN = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Menu")



BG = pygame.image.load("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\assets\Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size

    return pygame.font.Font("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\assets\\font.ttf", size)




class MAIN:

    def __init__(self):

        self.name = None

    def play(self,mapfile):

        while True:

            #PLAY_MOUSE_POS = pygame.mouse.get_pos()



            SCREEN.fill("black")

            app = App(mapfile)

            app.run()

        

    def maps(self):

        while True:

            

            

            SCREEN.blit(BG, (0, 0))



            MAPS_TEXT = get_font(45).render("Select the special case.", True, "#b68f40")

            MAPS_RECT = MAPS_TEXT.get_rect(center=(640, 260))



            MAP1 = get_font(30).render("Case 1", True, "#b68f40")

            MAP2 = get_font(30).render("Case 2", True, "#b68f40")

            MAP3 = get_font(30).render("Case 3", True, "#b68f40")

            MAP4 = get_font(30).render("Case 4", True, "#b68f40")




            SCREEN.blit(MAP1, MAP1.get_rect(center=(400, 460)))

            SCREEN.blit(MAP2, MAP2.get_rect(center=(880, 460)))

            SCREEN.blit(MAP3, MAP3.get_rect(center=(400, 560)))

            SCREEN.blit(MAP4, MAP4.get_rect(center=(880, 560)))

            SCREEN.blit(MAPS_TEXT, MAPS_RECT)



            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()

                    sys.exit()

                #App.select_map()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_1 :

                       self.play("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\walls1.txt")

                    if event.key == pygame.K_2 :

                       self.play("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\walls2.txt")

                    if event.key == pygame.K_3 :

                       self.play("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\walls4.txt")
                    if event.key == pygame.K_4 :
    
                       self.play("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\walls3.txt")   

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:

                        self.main_menu()



            pygame.display.update()




    def main_menu(self):

        while True:

            SCREEN.blit(BG, (0, 0))



            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")

            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))



            PLAY_TEXT = get_font(50).render("1. PLAY", True, "#b68f40")

            PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 450))



            MAP_TEXT = get_font(50).render("2. MAP", True, "#b68f40")

            MAP_RECT = MAP_TEXT.get_rect(center=(640, 550))



            SCREEN.blit(MENU_TEXT, MENU_RECT)

            SCREEN.blit(PLAY_TEXT, PLAY_RECT)

            SCREEN.blit(MAP_TEXT, MAP_RECT)

            

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()

                    sys.exit()

                if event.type == pygame.KEYDOWN :

                    if event.key == pygame.K_1 :

                        self.play("E:\\Menu-System-PyGame-main\\Menu-System-PyGame-main\\walls.txt")

                    if event.key == pygame.K_2 :

                        self.maps()

                    if event.key == pygame.K_3 :

                        pygame.quit()

                        sys.exit()



            pygame.display.update()
