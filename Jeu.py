from Screen import resize_screen
import sys
from Grille import Grille
from Tick import Tick
import pygame
pygame.init()

class Jeu:
    def __init__(self):
        self.nb_tours = 0

        self.state = "pause"
        
        # police
        self.police = pygame.font.SysFont("arial", 40)

        self.grille = Grille(10)
        self.tick = Tick()
        self.tick_maj = 30  # temps entre les maj de la simulation
    
    def create_btn(self, texte):
        texte_btn = self.police.render(texte, True, "white")
        texte_rect = texte_btn.get_rect()
        texte_rect.width += 20
        texte_rect.height += 20
        
        image = pygame.surface.Surface((texte_rect.size), pygame.SRCALPHA)
        pygame.draw.rect(image, "grey", texte_rect, border_radius=20)
        image.blit(texte_btn, (10, 10))

        return (image, texte_rect)

    def get_cell(self, pos:tuple):
        dimension = self.grille.dimension
        x = (pos[0] - 420) // self.longueur_cell
        y = pos[1] // self.longueur_cell
        return (int(x), int(y))
    
    def run(self):
        pygame.display.set_caption("jeu de la vie")
        resize_screen.set_mode((1920*0.6, 1080*0.6), pygame.RESIZABLE)

        # création fond
        rect_jeu = pygame.rect.Rect((0, 0, 1080, 1080))
        rect_jeu.centerx = 1920//2

        # génération boutons
        run_image, run_rect = self.create_btn("lancer simulation")
        run_rect.topleft = (10, 10)
        pause_image, pause_rect = self.create_btn("arrêter simulation")
        pause_rect.topleft = (10, 10)

        random_image, random_rect = self.create_btn("génération aléatoire")
        random_rect.topleft = (10, pause_rect.bottom + 10)

        
        boucle = True
        clock = pygame.time.Clock()
        while boucle:
            clock.tick(60)
            resize_screen.fill((0,0,0))

            # blit infos
            tick_image, tick_rect = self.create_btn("ticks maj : " + str(self.tick_maj))
            tick_rect.topleft = (10, random_rect.bottom + 10)
            resize_screen.blit(tick_image, tick_rect.topleft)

            dimension_image, dimension_rect = self.create_btn("dimension : " + str(self.grille.dimension))
            dimension_rect.topleft = (10, tick_rect.bottom + 10)
            resize_screen.blit(dimension_image, dimension_rect.topleft)

            resize_screen.blit(random_image, random_rect.topleft)

            resize_screen.draw_rect("grey", rect_jeu)
            if self.state == "pause":
                resize_screen.blit(run_image, run_rect.topleft)
            elif self.state == "run":
                resize_screen.blit(pause_image, pause_rect.topleft)
            
            # affichage grille
            if self.state == "run" and self.tick.do_every(self.tick_maj, "run"):
                self.grille.next_turn()

            self.longueur_cell = rect_jeu.width / self.grille.dimension
            for y in range(self.grille.dimension):
                for x in range(self.grille.dimension):
                    if self.grille.grille[y][x] == True:
                        rect_cell = pygame.rect.Rect(rect_jeu.x + self.longueur_cell * x, rect_jeu.y + self.longueur_cell * y, self.longueur_cell, self.longueur_cell)
                        resize_screen.draw_rect("white", rect_cell)

            resize_screen.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if run_rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)) and self.state == "pause":
                        self.state = "run"
                    elif pause_rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)) and self.state == "run":
                        self.state = "pause"
                    
                    if self.state == "pause":
                        if rect_jeu.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            pos_cell = self.get_cell(resize_screen.get_calcul_mouse_cos(event.pos))

                            if event.button == 1:
                                self.grille.grille[pos_cell[1]][pos_cell[0]] = True
                            elif event.button == 3:
                                self.grille.grille[pos_cell[1]][pos_cell[0]] = False
                        
                        elif random_rect.collidepoint(resize_screen.get_calcul_mouse_cos(event.pos)):
                            self.grille.melanger()
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.tick_maj += 1
                    elif event.key == pygame.K_DOWN:
                        self.tick_maj = max(1, self.tick_maj - 1)
                    
                    elif event.key == pygame.K_RIGHT:
                        self.grille = Grille(self.grille.dimension + 1)
                    elif event.key == pygame.K_LEFT:
                        new_dimension = max(1, self.grille.dimension - 1)
                        self.grille = Grille(new_dimension)